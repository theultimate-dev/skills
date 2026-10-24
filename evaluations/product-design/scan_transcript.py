"""List the tool calls in a trial agent's transcript that may reach outside its run folder.

Usage: python3 -I scan_transcript.py <agent-transcript.jsonl> <run-dir>

Prints every tool call that may reach outside <run-dir>, and every call to a tool a trial
may not use, for a reader to judge. Exits 1 if it prints any; prints CLEAN otherwise.
"""
import json
import os
import re
import sys

# The tools a trial may use. Any other tool, such as a skill, an agent, a web tool or a connector, is flagged.
ALLOWED = {"Read", "Write", "Edit", "MultiEdit", "NotebookEdit", "Glob", "Grep", "Bash", "TodoWrite", "SubagentHandback"}

transcript, run = sys.argv[1], sys.argv[2].rstrip("/") + "/"


def norm(path):
    return re.sub(r"^/tmp/", "/private/tmp/", os.path.normpath(path).rstrip("/")) + "/"


def inside(path, cwd=run):
    return norm(os.path.join(cwd, path)).startswith(norm(run))


def written_heredocs_removed(command):
    # The body of a heredoc that cat or tee writes to a file is content, not a path the command reads.
    # Only the body is skipped: the command line, with its redirect, is still scanned, and so is a body
    # that is piped on or read inside $( ), because a program runs it.
    lines, kept, i = command.split("\n"), [], 0
    while i < len(lines):
        line = lines[i]
        kept.append(line)
        i += 1
        start = re.search(r"<<-?\s*(['\"]?)(\w+)\1", line)
        if not start:
            continue
        head = re.split(r"[;&|(]", line[: start.start()])[-1]
        tail = re.split(r"[;&]", line[start.end() :])[0]
        writes = re.match(r"\s*tee\b", head) or (re.match(r"\s*cat\b", head) and ">" in head + tail)
        if writes and "|" not in tail:
            while i < len(lines) and lines[i].strip() != start.group(2):
                i += 1
    return "\n".join(kept)


with open(transcript) as handle:
    entries = [json.loads(line) for line in handle]

bad = []
for entry in entries:
    if entry.get("type") != "assistant":
        continue
    for block in entry.get("message", {}).get("content") or []:
        if not isinstance(block, dict) or block.get("type") != "tool_use":
            continue
        name, args = block["name"], block["input"]
        if name not in ALLOWED:
            bad.append(f"{name}: not allowed in a trial")
        elif name == "Bash":
            command = args.get("command", "")
            scanned = written_heredocs_removed(command)
            start = re.match(r'cd "?([^"&]+?)"? ?&&', command)
            if not start or not inside(start.group(1)):
                bad.append(f"Bash not run from the run folder: {command[:80]}")
            for found in re.finditer(r"(?<![\w.:/)\]])/[A-Za-z_.~][^\s\"';|&)]*", scanned):
                path = found.group()
                # An HTML closing tag, such as </div>, in generated markup is not a path.
                if scanned[found.start() - 1 : found.start()] == "<" and re.match(r"/[A-Za-z][\w-]*>", path):
                    continue
                if path != "/dev/null" and not inside(path):
                    bad.append(f"Bash path outside the run: {path}")
            for found in re.finditer(r"(?<![\w$])(\$\{?HOME\b\}?|~(?=[/\s\"']|$))", scanned):
                bad.append(f"Bash path in the home folder: {found.group()}")
            # A relative path that climbs with .. is resolved from the folder the command has changed into.
            cwd = start.group(1) if start else "/"
            # A cd with no folder, to the previous folder, or to one built from a variable can't be resolved here.
            for found in re.finditer(r'\b(?P<cd>cd|pushd|popd)\b(?:[ \t]+"?(?P<to>[^"\s;&|)]+)"?)?|(?<![\w./~$-])(?:[\w.-]+/)*\.\.(?![\w.])[^\s"\';|&)<>]*', scanned):
                to = found.group("to")
                if not found.group("cd"):
                    if not inside(found.group(), cwd):
                        bad.append(f"Bash path outside the run: {found.group()}")
                elif found.group("cd") == "popd" or not to or to[0] in "-+" or re.search(r"[$`]", to):
                    bad.append(f"Bash cd that can't be resolved here: {found.group()}")
                else:
                    cwd = os.path.join(cwd, to)
                    if not inside(cwd):
                        bad.append(f"Bash cd outside the run: {found.group()}")
            # A climb that starts from a variable or a command substitution can't be resolved here.
            for found in re.finditer(r"(?:\$\{?\w+\}?|\$\([^()]*\)|\))/(?:[^\s\"';|&)<>/]+/)*\.\.(?![\w.])", scanned):
                bad.append(f"Bash path that climbs from a variable: {found.group()}")
            # So can the previous folder, a parent taken with dirname, or a variable with its end cut or replaced.
            for found in re.finditer(r"\$\{?OLDPWD\b\}?|\bdirname\b|\$\{\w+(?:%%?/|//?)[^}]*\}", scanned):
                bad.append(f"Bash path that can't be resolved here: {found.group()}")
        else:
            for key in ("file_path", "path", "notebook_path"):
                path = args.get(key)
                if path and (not path.startswith("/") or not inside(path)):
                    bad.append(f"{name} {key} outside the run: {path}")
            pattern = args.get("pattern", "")
            if name == "Glob" and (pattern.startswith("/") or re.search(r"(^|/)\.\.(/|$)", pattern)) and not inside(pattern, args.get("path") or run):
                bad.append(f"Glob pattern outside the run: {pattern}")
            if name in ("Glob", "Grep") and not args.get("path"):
                bad.append(f"{name} without a path (it would search the session's folder)")
print("\n".join(bad) or "CLEAN")
sys.exit(1 if bad else 0)
