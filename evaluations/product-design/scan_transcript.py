# usage: python3 -I scan_transcript.py <agent-transcript.jsonl> <run-dir>
# Prints every tool call that reaches outside <run-dir> or loads a skill, agent or web tool; exits 1 if any.
import json, os, re, sys

transcript, run = sys.argv[1], sys.argv[2].rstrip("/") + "/"


def norm(path):
    return re.sub(r"^/tmp/", "/private/tmp/", path.rstrip("/")) + "/"


bad = []
for line in open(transcript):
    entry = json.loads(line)
    if entry.get("type") != "assistant":
        continue
    for block in entry.get("message", {}).get("content") or []:
        if not isinstance(block, dict) or block.get("type") != "tool_use":
            continue
        name, args = block["name"], block["input"]
        if name in ("Skill", "Agent", "WebFetch", "WebSearch", "ToolSearch"):
            bad.append(f"{name}: not allowed in a trial")
        elif name == "Bash":
            command = args.get("command", "")
            # The body of a heredoc that cat or tee writes to a file is content, not a path the command reads.
            # Only the body is skipped: the command line, with its redirect, is still scanned.
            scanned = re.sub(r"(\b(?:cat|tee)\b[^\n;&|]*<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n).*?\n\2(?=\n|$)", r"\1", command, flags=re.S)
            start = re.match(r'cd "?([^"&]+?)"? ?&&', command)
            if not start or not norm(os.path.normpath(start.group(1))).startswith(norm(run)):
                bad.append(f"Bash not run from the run folder: {command[:80]}")
            for found in re.finditer(r"(?<![\w.:/)\]])/[A-Za-z_.~][^\s\"';|&)]*", scanned):
                path = found.group()
                # An HTML closing tag, such as </div>, in generated markup is not a path.
                if scanned[found.start() - 1 : found.start()] == "<" and re.match(r"/[A-Za-z][\w-]*>", path):
                    continue
                if path != "/dev/null" and not norm(path).startswith(norm(run)):
                    bad.append(f"Bash path outside the run: {path}")
        else:
            for key in ("file_path", "path", "notebook_path"):
                path = args.get(key)
                if path and not norm(path).startswith(norm(run)):
                    bad.append(f"{name} {key} outside the run: {path}")
            if name in ("Glob", "Grep") and not args.get("path"):
                bad.append(f"{name} without a path (it would search the session's folder)")
print("\n".join(bad) or "CLEAN")
sys.exit(1 if bad else 0)
