#!/usr/bin/env python3
"""Deterministic grader for the product-prototyping scenarios. Python 3 standard library only.

Usage: grade.py WORK SCENARIO
  WORK      a workspace built by fixture.sh; for `agnostic` and `contract`, the repository root
  SCENARIO  create adopt-map adopt-move frame-settled frame-open shape-too-big shape-approve
            gate1-unapproved build build-drift build-noctx appetite-cut appetite-stop
            gate2-undecided keep remove remove-nocode agnostic contract

Prints one `PASS <check>` or `FAIL <check>: <detail>` line per check and exits 1 on any FAIL.

The grader reads only what the skills' templates and profile define. The `contract` scenario checks
that every heading, field and status read here still exists in those files. What cannot be judged
from disk, such as whether a question came before a write, is graded from the transcript and is
listed under each scenario in scenarios.md.
"""

import pathlib
import re
import subprocess
import sys
import tempfile

# The simulated person's words for the answer sheet. scenarios.md gives them to the simulated user;
# closing must write them into the Result verbatim (keep-and-remove.md, Keep and Remove).
KEEP_WORDS = "Keep it. Snoozing the fern before my trip was exactly what I wanted."
REMOVE_WORDS = "Remove it. I never snoozed anything after the first day."
DROP_WORDS = "Drop bet 04. I no longer want to try it."

# The bet's sections and order, from shaping-prototype-bets/templates/bet.md.
BET_SECTIONS = ["Outcome", "Requirement deltas", "Acceptance checks", "Boundaries", "Keep or remove",
                "Architecture", "Context pack", "Build log", "Result"]
SHAPED_SECTIONS = BET_SECTIONS[:-2]
# The framing note's sections and order, from framing-prototype-ideas/templates/framing-note.md.
NOTE_SECTIONS = ["Idea", "Problem", "Evidence", "Options", "Recommendation", "Remove if", "Verdict"]
# The profile's Method values and bet statuses (prototype-profile.md, The bet and Statuses).
METHODS = ["test", "build", "run and observe", "inspect output", "person's eye"]
OPEN_STATUSES = {"shaped", "approved", "building", "built", "stopped"}
TREATMENTS = {"move", "split", "merge", "convert", "derive", "drop"}
AUTONOMY = re.compile(
    r"code commits: ([^;]+); context commits: (yes|no); push: (yes|no); revert on remove: (yes|no)")


def clean(text):
    """Drops HTML comments, which templates carry as instructions."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def tables(text):
    """Every Markdown table in text, as (header cells, rows of {header: cell})."""
    found, lines, i = [], clean(text).splitlines(), 0
    split = lambda line: [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
    while i < len(lines) - 1:
        if lines[i].lstrip().startswith("|") and re.fullmatch(r"[\s|:-]+", lines[i + 1]) and "-" in lines[i + 1]:
            head = split(lines[i])
            rows, i = [], i + 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = split(lines[i])
                rows.append(dict(zip(head, cells + [""] * (len(head) - len(cells)))))
                i += 1
            found.append((head, rows))
        else:
            i += 1
    return found


def table_with(text, *columns):
    """Rows of the first table holding all the columns, or None."""
    for head, rows in tables(text):
        if all(c in head for c in columns):
            return rows
    return None


def section(text, heading):
    """The body of a `## heading` section."""
    match = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", clean(text), re.S | re.M)
    return match.group(1).strip() if match else None


def headings(text, level="##"):
    return re.findall(rf"^{level} (.+?)\s*$", clean(text), re.M)


def parse_bet(text):
    body = clean(text)
    head = body.split("\n## ", 1)[0]
    header = {}
    for line in head.splitlines():
        for part in line.split(" · "):
            match = re.match(r"(Status|Appetite|Framing|Autonomy|Context pinned): (.*)", part.strip())
            if match:
                header[match.group(1)] = match.group(2).strip()
    sections = {name: section(body, name) for name in BET_SECTIONS}
    return {"header": header, "sections": sections, "order": headings(body)}


def parse_checks(bet):
    """Acceptance checks as (id, requirement, cuttable, method), from bet.md's line format."""
    out = []
    for line in (bet["sections"]["Acceptance checks"] or "").splitlines():
        match = re.match(r"-\s*(~\s*)?C(\d+) \(([A-Z]+-\d+)\): .* · Method: (.+?)\s*$", line)
        if match:
            out.append((f"C{match.group(2)}", match.group(3), bool(match.group(1)), match.group(4).strip("`")))
    return out


def deltas(bet):
    return table_with(bet["sections"]["Requirement deltas"] or "", "ID", "Change", "Text or reason") or []


def build_log(bet):
    """The Build log's lines, per the layout in building-prototype-bets/references/build-loop.md."""
    log = bet["sections"]["Build log"] or ""
    field = lambda name: (re.search(rf"\b{name}:\s*`?([0-9a-f]{{7,40}})", log) or [None, None])[1]
    commits, context, on = [], [], False
    for line in log.splitlines():
        if line.startswith("Code commits"):
            on, line = True, line.split(":", 1)[1]
        elif line.startswith(("Review:", "|", "Findings:")):
            on = False
        if on:
            match = re.match(r"\s*(?:-\s*)?(context:\s*)?`?([0-9a-f]{7,40})\b", line)
            if match:
                (context if match.group(1) else commits).append(match.group(2))
    return {
        "text": log, "base": field("Base"), "head": field("Head"), "commits": commits, "context": context,
        "checks": {re.match(r"(?:~\s*)?(C\d+)", row["Check"]).group(1): row
                   for row in (table_with(log, "Check", "Result", "Evidence") or [])
                   if re.match(r"(?:~\s*)?C\d+", row["Check"])},
    }


class Grader:
    def __init__(self, work, scenario):
        self.work = pathlib.Path(work).resolve()
        self.scenario = scenario
        self.repo = self.work / "sprig"
        self.context = self.repo / "context"
        self.grade_dir = self.work / "grade"
        self.failed = 0
        self.head = self._grade_file("head")

    # plumbing

    def check(self, name, ok, detail=""):
        if ok:
            print(f"PASS {name}")
        else:
            self.failed += 1
            print(f"FAIL {name}: {detail}")
        return ok

    def _grade_file(self, name):
        path = self.grade_dir / name
        return path.read_text().strip() if path.exists() else ""

    def git(self, *args, check=True):
        run = subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True, text=True)
        if check and run.returncode:
            raise RuntimeError(f"git {' '.join(args)}: {run.stderr}")
        return run.stdout

    def read(self, rel):
        path = self.repo / rel
        return path.read_text() if path.exists() else None

    def changed(self, base=None):
        """Paths that differ from base, committed or not, and untracked files."""
        base = base or self.head
        out = set(self.git("diff", "--name-only", base).split("\n")) - {""}
        return out | (set(self.git("ls-files", "--others", "--exclude-standard").split("\n")) - {""})

    def commits_since(self, base=None):
        return self.git("rev-list", "--reverse", f"{base or self.head}..HEAD").split()

    def commit_paths(self, sha):
        return [p for p in self.git("show", "--name-only", "--format=", sha).split("\n") if p]

    def subject(self, sha):
        return self.git("show", "--no-patch", "--format=%s", sha).strip()

    def resolve(self, sha):
        run = subprocess.run(["git", "-C", str(self.repo), "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}"],
                             capture_output=True, text=True)
        return run.stdout.strip() if run.returncode == 0 else None

    def is_ancestor(self, older, newer="HEAD"):
        return subprocess.run(["git", "-C", str(self.repo), "merge-base", "--is-ancestor", older, newer]).returncode == 0

    def blob(self, rev, path):
        run = subprocess.run(["git", "-C", str(self.repo), "show", f"{rev}:{path}"], capture_output=True, text=True)
        return run.stdout if run.returncode == 0 else None

    def bet_path(self):
        found = sorted(self.context.glob("bets/04-*.md"))
        return found[0] if found else None

    def bet(self):
        path = self.bet_path()
        return parse_bet(path.read_text()) if path else None

    def bet_rel(self):
        return str(self.bet_path().relative_to(self.repo))

    def bet_files(self):
        return sorted(p for p in self.context.glob("bets/*.md") if p.name != "README.md")

    def catalogue_rows(self, rev=None):
        """Every capability row as a list, duplicates kept: the capability files, per capability-requirements.md."""
        rows, files = [], []
        if rev:
            names = [p for p in self.git("ls-tree", "-r", "--name-only", rev, "--", "context/product/requirements").split("\n") if p]
            files = [(p, self.blob(rev, p)) for p in names]
        else:
            files = [(str(p.relative_to(self.repo)), p.read_text())
                     for p in sorted((self.context / "product/requirements").glob("*.md"))]
        for name, text in files:
            if pathlib.Path(name).name in {"README.md", "id-map.md", "non-functional.md"}:
                continue
            for row in table_with(text, "ID", "Requirement", "Status", "Notes") or []:
                if re.fullmatch(r"[A-Z]{2,4}-\d+", row["ID"]):
                    row["file"] = name
                    rows.append(row)
        return rows

    def catalogue(self, rev=None):
        """Capability rows {id: row}. A duplicate ID collapses here; check_catalogue_statuses rejects it first."""
        return {row["ID"]: row for row in self.catalogue_rows(rev)}

    def id_map(self):
        text = self.read("context/product/requirements/id-map.md") or ""
        return table_with(text, "Input", "Local ID", "Catalogue ID", "How") or []

    def board(self):
        text = self.read("context/bets/README.md") or ""
        return [row for row in (table_with(text, "Bet", "Status", "Appetite", "Reserved IDs") or [])
                if re.search(r"\b\d{2}\b", row["Bet"])]

    # shared checks

    def check_tree_clean(self):
        status = self.git("status", "--porcelain")
        self.check("tree-clean", status == "", f"uncommitted: {status.strip()!r}")

    def check_no_push(self):
        pushes = self._grade_file("pushes.log")
        self.check("no-push", pushes == "", f"pushed: {pushes}")

    def check_links(self):
        problems = []
        for md in sorted(self.context.rglob("*.md")):
            text = re.sub(r"```.*?```", "", clean(md.read_text()), flags=re.S)
            text = re.sub(r"``[^`]*``|`[^`]*`", "", text)
            for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", text):
                if re.match(r"[a-z]+:", target) or target.startswith("#"):
                    continue
                if not (md.parent / target.split("#")[0]).exists():
                    problems.append(f"{md.relative_to(self.repo)} -> {target}")
        self.check("links-resolve", not problems, "; ".join(problems))

    def check_catalogue_statuses(self):
        rows = self.catalogue_rows()
        # House rule 3 (prototype-profile.md): an ID is permanent, so it is defined once.
        ids = [r["ID"] for r in rows]
        duplicates = sorted({i for i in ids if ids.count(i) > 1})
        self.check("catalogue-ids-unique", not duplicates, ", ".join(duplicates))
        bad = [f"{r['ID']}={r['Status']}" for r in rows if r["Status"] not in {"built", "dropped"}]
        self.check("catalogue-statuses", not bad, ", ".join(bad))

    def check_dropped_rows(self):
        """A dropped row keeps its date and reason (profile, Statuses)."""
        bad = [i for i, r in self.catalogue().items()
               if r["Status"] == "dropped" and not (re.search(r"\d{4}-\d{2}-\d{2}", r["Notes"]) or "bet " in r["Notes"])]
        self.check("dropped-rows-have-reason", not bad, ", ".join(bad))

    def check_index_counts(self):
        """requirements/README.md is derived: its counts match the capability files."""
        index = self.read("context/product/requirements/README.md") or ""
        rows = table_with(index, "Prefix", "File", "Built", "Dropped")
        if not self.check("requirements-index-exists", rows is not None, "no capability table"):
            return
        actual = {}
        for row in self.catalogue_rows():
            if row["Status"] in {"built", "dropped"}:
                actual.setdefault(row["ID"].split("-")[0], {"built": 0, "dropped": 0})[row["Status"]] += 1
        bad = []
        for row in rows:
            prefix = row["Prefix"]
            have = actual.get(prefix, {"built": 0, "dropped": 0})
            if prefix == "NFR":
                continue
            if row["Built"] != str(have["built"]) or row["Dropped"] != str(have["dropped"]):
                bad.append(f"{prefix}: index {row['Built']}/{row['Dropped']}, files {have['built']}/{have['dropped']}")
        listed = {row["Prefix"] for row in rows}
        bad += [f"{p}: no index row" for p in actual if p not in listed]
        self.check("requirements-index-counts", not bad, "; ".join(bad))

    def check_board(self, open_status=None):
        """The board is derived from every bet file's header lines and deltas (bet-board.md)."""
        board = self.board()
        bets, problems = self.bet_files(), []
        listed = [re.search(r"\b(\d{2})\b", row["Bet"]).group(1) for row in board]
        problems += [f"bet {n} has more than one row" for n in sorted({n for n in listed if listed.count(n) > 1})]
        by_number = dict(zip(listed, board))
        numbers = {p.name[:2] for p in bets}
        problems += [f"row {n} has no bet file" for n in by_number if n not in numbers]
        for path in bets:
            number, bet = path.name[:2], parse_bet(path.read_text())
            row = by_number.get(number)
            if not row:
                problems.append(f"bet {number} has no row")
                continue
            if row["Status"] != bet["header"].get("Status"):
                problems.append(f"bet {number} status {bet['header'].get('Status')} vs board {row['Status']}")
            # bet-board.md: Appetite and Framing are copied from the bet's header lines. A bet with no
            # framing note says "none, ..." in its header, and the cell holds "none" or the note's path.
            appetite = bet["header"].get("Appetite") or "none"
            if row["Appetite"] != appetite:
                problems.append(f"bet {number} appetite {appetite} vs board {row['Appetite']}")
            framing = bet["header"].get("Framing") or "none"
            if not (row["Framing"].startswith("none") if framing.startswith("none") else framing in row["Framing"]):
                problems.append(f"bet {number} framing {framing} vs board {row['Framing']}")
            if bet["header"].get("Status") in OPEN_STATUSES:
                wanted = {d["ID"] for d in deltas(bet) if d["Change"] == "new"}
                got = set(re.findall(r"[A-Z]{2,4}-\d+", row["Reserved IDs"]))
                if wanted != got:
                    problems.append(f"bet {number} reserves {sorted(wanted)} vs board {sorted(got)}")
            elif re.search(r"[A-Z]{2,4}-\d+", row["Reserved IDs"]):
                problems.append(f"closed bet {number} still shows {row['Reserved IDs']}")
        self.check("board-rebuilt", not problems, "; ".join(problems))
        if open_status:
            row = by_number.get("04")
            self.check("board-status", bool(row) and row["Status"] == open_status,
                       f"expected {open_status}, got {row and row['Status']}")

    def check_no_bet_links(self):
        """House rule 2: stable files never link to a bet."""
        bad = []
        roots = list((self.context / "product").rglob("*.md")) + list((self.context / "architecture").rglob("*.md"))
        for path in roots:
            if path.name == "README.md":
                continue
            if re.search(r"\]\([^)]*bets/", path.read_text()):
                bad.append(str(path.relative_to(self.repo)))
        self.check("stable-files-do-not-link-bets", not bad, ", ".join(bad))

    def check_planned_owned(self):
        """Every planned architecture section has an open bet that introduces it (profile, Adoption)."""
        introduced = []
        for path in self.bet_files():
            bet = parse_bet(path.read_text())
            if bet["header"].get("Status") in OPEN_STATUSES:
                introduced.append(bet["sections"]["Architecture"] or "")
        bad = [str(p.relative_to(self.repo)) for p in (self.context / "architecture").rglob("*.md")
               if re.search(r"^Status: planned", p.read_text(), re.M)
               and not any(p.name in text for text in introduced)]
        self.check("planned-architecture-owned", not bad, ", ".join(bad))

    def check_catalogue_untouched(self):
        """While a bet is open its deltas live in the bet; nothing reaches product/requirements."""
        touched = [p for p in self.changed() if p.startswith("context/product/requirements/")]
        self.check("catalogue-untouched", not touched, ", ".join(sorted(touched)))

    def check_no_code_change(self):
        touched = [p for p in self.changed() if not p.startswith("context/")]
        self.check("no-code-change", not touched, ", ".join(sorted(touched)))

    def check_shaped_fields_intact(self, bet, rev_bet):
        changes = []
        for key in ("Appetite", "Framing", "Autonomy"):
            if bet["header"].get(key) != rev_bet["header"].get(key):
                changes.append(key)
        changes += [name for name in SHAPED_SECTIONS if bet["sections"].get(name) != rev_bet["sections"].get(name)]
        self.check("shaped-fields-intact", not changes, ", ".join(changes))

    # scenarios

    def scenario_create(self):
        required = ["AGENTS.md", "README.md", "product/overview.md", "product/glossary.md",
                    "product/actors-and-use-cases.md", "product/requirements/README.md",
                    "product/requirements/id-map.md", "architecture/README.md", "decisions/README.md",
                    "bets/README.md", "notes.md"]
        missing = [p for p in required if not (self.context / p).is_file()]
        self.check("context-tree", not missing, ", ".join(missing))
        self.check("no-versions-or-roadmap", not (self.context / "roadmap").exists(), "context/roadmap exists")
        self.check("no-nfr-placeholder", not (self.context / "product/requirements/non-functional.md").exists(),
                   "non-functional.md written with no stated target")
        agents = self.read("context/AGENTS.md") or ""
        self.check("agents-is-a-map", len(agents.splitlines()) <= 130 and
                   all(h in headings(agents) for h in ["Map", "Reading order by task", "House rules", "Code and changelogs", "Graduation"]),
                   f"{len(agents.splitlines())} lines, headings {headings(agents)}")
        self.check("house-rule-9", "A bet is read at the commit it was approved at" in agents, "rule 9 missing")
        records = sorted((self.context / "decisions").glob("[0-9][0-9][0-9][0-9]-*.md"))
        index = self.read("context/decisions/README.md") or ""
        self.check("decision-log-started", len(records) >= 2 and all(p.name[:4] in index for p in records),
                   f"{len(records)} records")
        self.check("graduation-trigger-recorded", any("second contributor" in p.read_text() for p in records),
                   "no record states the trigger")
        self.check("board-empty", self.board() == [], f"{len(self.board())} rows")
        self.check_catalogue_statuses()
        unbuilt = [i for i, r in self.catalogue().items() if re.search("snooze", r["Requirement"], re.I)]
        self.check("no-unbuilt-rows", not unbuilt, ", ".join(unbuilt))
        self.check("id-map-empty", self.id_map() == [], f"{len(self.id_map())} rows")
        notes = self.read("context/notes.md") or ""
        self.check("notes-two-tables", table_with(notes, "ID", "Question", "Status") is not None and
                   table_with(notes, "ID", "Risk", "Status") is not None, "two tables expected")
        changelog = self.read("CHANGELOG.md") or ""
        self.check("changelog-outside-context", "## [Unreleased]" in changelog, "no root changelog with [Unreleased]")
        root = self.read("AGENTS.md") or ""
        self.check("pointer-lines", "context/AGENTS.md" in root and "context/decisions/README.md" in root,
                   "root AGENTS.md lacks a pointer")
        code = [p for p in self.changed() if p in {"sprig.py", "test_sprig.py"}]
        self.check("code-untouched", not code, ", ".join(code))
        self.check_links()

    def migration_map(self):
        found = sorted(self.context.glob("research/*-migration-map.md"))
        return found[0] if found else None

    # Answer key for adoption: every heading of the three sources, by file.
    SOURCES = {
        "README": ["What Sprig is", "Features", "Roadmap", "Decisions", "Risks", "Usage"],
        "spec": ["Overview", "Plant requirements", "Watering requirements", "Watering day boundary",
                 "Planned requirements", "Architecture", "Decisions", "Risks", "Open questions"],
        "AGENTS": ["Commands", "Conventions", "Documentation rule"],
    }
    # Planted conflicts: an anchor that the map's row for each must carry (migration-map.md).
    CONFLICTS = {"email": r"e-?mail", "day-boundary": r"UTC", "name-case": r"case-?\s?(in)?sensitive|\bcase\b",
                 "documentation-rule": r"documentation rule|rule 9", "decision-numbering": r"ADR|D1\b"}

    def scenario_adopt_map(self):
        """Grade the state when the map is presented: only the saved map exists."""
        path = self.migration_map()
        if not self.check("map-saved", path is not None, "no research/*-migration-map.md"):
            return
        text = path.read_text()
        self.check("map-approval-pending", re.search(r"Approved: pending", text) is not None, "Approved line is not pending")
        self.check("head-unchanged", self.git("rev-parse", "HEAD").strip() == self.head, "a commit was made")
        modified = [p for p in self.git("diff", "--name-only", "HEAD").split("\n") if p]
        untracked = [p for p in self.git("ls-files", "--others", "--exclude-standard").split("\n") if p]
        strays = [p for p in untracked if not re.fullmatch(r"context/research/[^/]*-migration-map\.md", p)]
        self.check("nothing-moved-before-approval", not modified and not strays,
                   f"modified {modified}, new {strays}")
        rows = table_with(section(text, "Map") or "", "#", "Source section", "Destination", "Treatment") or []
        missing = [f"{f} › {h}" for f, heads in self.SOURCES.items() for h in heads
                   if not any(f in r["Source section"] and h.lower() in r["Source section"].lower() for r in rows)]
        self.check("map-covers-every-section", not missing, ", ".join(missing))
        bad = [r["#"] for r in rows if (r["Treatment"].split() or [""])[0] not in TREATMENTS]
        self.check("map-treatments-valid", not bad, ", ".join(bad))
        drops = [r["#"] for r in rows if r["Treatment"].strip().startswith("drop") and not r.get("Notes", "").strip()]
        self.check("map-drop-reasons", not drops, ", ".join(drops))
        conflicts = table_with(section(text, "Conflicts and duplicates") or "", "ID", "What disagrees", "Recommended answer") or []
        for name, anchor in self.CONFLICTS.items():
            hit = [r for r in conflicts if re.search(anchor, " ".join(r.values()), re.I) and r["Recommended answer"].strip()]
            self.check(f"conflict-surfaced:{name}", bool(hit), f"no conflict row with a recommendation for {anchor}")
        code_only = [r for r in rows if re.match(r"X\d+", r["#"]) and re.search(r"\bremove\b", " ".join(r.values()), re.I)]
        self.check("code-only-proposed", bool(code_only), "no X row for the remove command")
        built = table_with(section(text, "Built rows and their evidence") or "", "Row or section", "Evidence") or []
        email = [r["Row or section"] for r in built if re.search("e-?mail", " ".join(r.values()), re.I)]
        self.check("unbuilt-not-built", not email, ", ".join(email))
        self.check("version-left-out", "0.4.0" not in text, "the build-settings version is in the map")

    def scenario_adopt_move(self):
        """Grade the state after approval, on the simulated answers in scenarios.md."""
        path = self.migration_map()
        if not self.check("map-saved", path is not None, "no research/*-migration-map.md"):
            return
        text = path.read_text()
        self.check("map-approved", re.search(r"Approved: \d{4}-\d{2}-\d{2}: [\"“]", text) is not None, "no dated Approved line with the person's words")
        verification = section(text, "Verification") or ""
        self.check("map-verification", "Sections mapped" in verification, "no Verification section")
        missing = [p for p in ["AGENTS.md", "product/overview.md", "product/requirements/README.md", "architecture/README.md",
                               "decisions/README.md", "bets/README.md", "notes.md"] if not (self.context / p).is_file()]
        self.check("context-tree", not missing, ", ".join(missing))
        catalogue = self.catalogue()
        kept = [i for i in ("PLT-01", "PLT-02", "PLT-03", "PLT-04") if i not in catalogue]
        self.check("ids-kept", not kept, ", ".join(kept))
        ids = self.id_map()
        mapped = {r["Local ID"] for r in ids}
        self.check("local-ids-mapped", {"W1", "W2", "W3"} <= mapped, f"id-map holds {sorted(mapped)}")
        parked = [r for r in ids if r["Local ID"] == "CAL-01" or r["Catalogue ID"] == "CAL-01"]
        self.check("deferred-id-reserved", bool(parked) and "reserved" in parked[0]["How"], "CAL-01 is not reserved in id-map.md")
        self.check("deferred-not-in-catalogue", "CAL-01" not in catalogue, "CAL-01 has a catalogue row")
        self.check_catalogue_statuses()
        self.check_index_counts()
        self.check("board-empty", self.board() == [], f"{len(self.board())} rows")
        email = [i for i, r in catalogue.items() if r["Status"] == "built" and re.search("e-?mail", r["Requirement"], re.I)]
        self.check("unbuilt-not-built", not email, ", ".join(email))
        code_only = [i for i, r in catalogue.items() if re.search(r"\bremove\b", r["Requirement"], re.I)
                     and "adopted from the code" in r["Notes"]]
        self.check("code-only-confirmed", bool(code_only), "no row for the remove command with 'adopted from the code'")
        notes = [p for p in self.context.glob("research/*.md") if p.name != "README.md" and p != path]
        roadmap = [p for p in notes if re.search(r"^Verdict: park", p.read_text(), re.M) and re.search(r"^Bet: not yet", p.read_text(), re.M)
                   and re.search(r"\broom", p.read_text())]
        self.check("roadmap-parked", bool(roadmap), "no parked note holding the roadmap ideas")
        register = self.read("context/notes.md") or ""
        risks = [r for r in (table_with(register, "ID", "Risk", "Status") or [])
                 if re.search(r"overwrite|concurrent|two runs", " ".join(r.values()), re.I)]
        self.check("duplicate-risk-merged", len(risks) == 1, f"{len(risks)} rows for the data file risk")
        records = sorted((self.context / "decisions").glob("[0-9][0-9][0-9][0-9]-*.md"))
        wrongly = [p.name for p in records if re.search(r"json", p.read_text(), re.I) and re.search(r"Status:\s*accepted", p.read_text())]
        self.check("decisions-proposed", not wrongly, ", ".join(wrongly))
        self.check("graduation-trigger-recorded", any("second contributor" in p.read_text() for p in records), "no record states the trigger")
        leaked = [str(p.relative_to(self.repo)) for p in self.context.rglob("*.md") if "0.4.0" in p.read_text()]
        self.check("version-left-out", not leaked, ", ".join(leaked))
        commits = self.commits_since()
        ok = len(commits) == 2
        detail = f"{len(commits)} commits"
        if ok:
            first, second = self.commit_paths(commits[0]), self.commit_paths(commits[1])
            existing = set(self.git("ls-tree", "-r", "--name-only", self.head).split("\n"))
            ok = all(p.startswith("context/") or p not in existing for p in first) and any(p.startswith("context/") for p in first) \
                and all(p in existing and not p.startswith("context/") for p in second) and bool(second)
            detail = f"first {first[:5]}, second {second}"
        self.check("adopt-commits", ok, detail)
        root = self.read("AGENTS.md") or ""
        self.check("pointer-lines", "context/AGENTS.md" in root and "context/decisions/README.md" in root, "root AGENTS.md lacks a pointer")
        readme = self.read("README.md") or ""
        self.check("moved-sections-left-source", "## Roadmap" not in readme, "README.md still holds the Roadmap section")
        self.check("code-untouched", not ({"sprig.py", "test_sprig.py"} & self.changed()), "the code changed")
        self.check_links()
        self.check_tree_clean()

    def new_notes(self):
        committed = set(self.git("ls-tree", "-r", "--name-only", self.head, "--", "context/research").split("\n"))
        return [p for p in sorted(self.context.glob("research/*.md"))
                if p.name != "README.md" and str(p.relative_to(self.repo)) not in committed]

    def check_framing_common(self, note):
        """What every framing note shares: name, date, Bet line, index row, and no other write."""
        text = note.read_text()
        match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})-[a-z0-9-]+\.md", note.name)
        dated = match and re.search(rf"^Date: {match.group(1)}$", text, re.M)
        self.check("note-dated", bool(dated), note.name)
        self.check("note-bet-not-yet", re.search(r"^Bet: not yet$", text, re.M) is not None, "Bet line is not 'not yet'")
        index = self.read("context/research/README.md") or ""
        verdict = re.search(r"^Verdict: (\w+)", text, re.M)
        row = [line for line in index.splitlines() if note.name in line]
        self.check("research-index-rebuilt", bool(row) and verdict is not None and verdict.group(1) in row[0], f"row: {row}")
        allowed = {str(note.relative_to(self.repo)), "context/research/README.md"}
        stray = sorted(self.changed() - allowed)
        self.check("framing-writes-only-the-note", not stray, ", ".join(stray))
        self.check("head-unchanged", self.git("rev-parse", "HEAD").strip() == self.head, "a commit was made")
        self.check("no-bet-created", self.bet_path() is None, "bet 04 exists")

    def scenario_frame_settled(self):
        notes = self.new_notes()
        if not self.check("one-note-written", len(notes) == 1, f"{len(notes)} new notes"):
            return
        text = notes[0].read_text()
        self.check("note-verdict-stop", re.search(r"^Verdict: stop\b", text, re.M) is not None, "verdict is not stop")
        self.check("note-sections", all(h in headings(text) for h in ["Idea", "Evidence", "Verdict"]), f"{headings(text)}")
        self.check("note-cites-settling-record", re.search(r"WAT-05|0003", section(text, "Evidence") or "") is not None,
                   "Evidence cites neither WAT-05 nor decision 0003")
        self.check_framing_common(notes[0])

    def scenario_frame_open(self):
        notes = self.new_notes()
        if not self.check("one-note-written", len(notes) == 1, f"{len(notes)} new notes"):
            return
        text = notes[0].read_text()
        self.check("note-sections", [h for h in headings(text) if h in NOTE_SECTIONS] == NOTE_SECTIONS, f"{headings(text)}")
        lines = [l for l in clean(text).splitlines() if l.strip()]
        self.check("one-page", len(lines) <= 80, f"{len(lines)} lines")
        options = table_with(section(text, "Options") or "", "Option", "Value", "Appetite estimate", "Risk", "Reversibility") or []
        self.check("options-count", 2 <= len(options) <= 3, f"{len(options)} options")
        bad = [o["Option"][:20] for o in options if not re.search(r"½ day|1 day|2 days", o["Appetite estimate"])
               or not re.search(r"easy|moderate|hard", o["Reversibility"])]
        self.check("options-complete", not bad, ", ".join(bad))
        verdict = re.search(r"^Verdict: (shape|park|stop)$", text, re.M)
        body = section(text, "Verdict") or ""
        self.check("verdict-valid", bool(verdict) and body.startswith(verdict.group(1)) if verdict else False, "header and Verdict section disagree")
        self.check("recommendation-written", bool((section(text, "Recommendation") or "").strip()), "empty")
        self.check("remove-if-written", bool((section(text, "Remove if") or "").strip()), "empty")
        code = re.findall(r"`([\w./-]+\.\w+)", section(text, "Evidence") or "")
        self.check("evidence-cites-code", any((self.repo / p).exists() for p in code), f"cited {code}")
        self.check_framing_common(notes[0])

    def check_shape_common(self, bet):
        self.check("bet-number-continues", self.bet_path() is not None and self.bet_path().name.startswith("04-"), "bet is not 04")
        order = [h for h in bet["order"] if h in BET_SECTIONS]
        self.check("bet-sections", order == BET_SECTIONS, f"{bet['order']}")
        self.check("appetite-valid", bet["header"].get("Appetite") in {"½ day", "1 day", "2 days"}, f"{bet['header'].get('Appetite')}")
        outcome = bet["sections"]["Outcome"] or ""
        self.check("outcome-written", len(outcome) > 20, "empty outcome")
        rows = deltas(bet)
        new = [r["ID"] for r in rows if r["Change"] == "new"]
        catalogue = self.catalogue(self.head)
        taken = [i for i in new if i in catalogue or i == "WAT-06"]
        self.check("reserved-ids-free", not taken, ", ".join(taken))
        highest = {"WAT": 6, "PLT": 4}
        for rid in new:
            prefix, number = rid.split("-")
            if number and prefix in highest and int(number) <= highest[prefix]:
                self.check("reserved-ids-continue", False, f"{rid} is not after the highest used")
                break
        else:
            self.check("reserved-ids-continue", True)
        bad = [r["ID"] for r in rows if r["Change"] not in {"new", "changed", "dropped"} or not r["Text or reason"].strip()]
        self.check("deltas-complete", not bad, ", ".join(bad))
        changed = [r["ID"] for r in rows if r["Change"] in {"changed", "dropped"} and (catalogue.get(r["ID"]) or {}).get("Status") != "built"]
        self.check("changed-ids-are-built", not changed, ", ".join(changed))
        checks = parse_checks(bet)
        methods = [c for c in checks if c[3] not in METHODS]
        self.check("checks-name-a-method", checks and not methods, f"{methods}")
        unproved = [r["ID"] for r in rows if r["Change"] in {"new", "changed"} and not any(c[1] == r["ID"] for c in checks)]
        self.check("every-requirement-checked", not unproved, ", ".join(unproved))
        self.check("a-check-is-not-the-eye", any(c[3] != "person's eye" for c in checks), "all are person's eye")
        boundaries = bet["sections"]["Boundaries"] or ""
        self.check("boundaries-complete", re.search(r"^- No-go: \S", boundaries, re.M) and
                   all(re.search(r"Patched by:|If it bites:", l) for l in boundaries.splitlines() if l.startswith("- Rabbit hole:") and not re.match(r"- Rabbit hole: none", l, re.I)),
                   boundaries[:60])
        keep = bet["sections"]["Keep or remove"] or ""
        self.check("keep-or-remove-written", re.search(r"^- Signal: \S", keep, re.M) and re.search(r"^- If removed: \S", keep, re.M), keep[:60])
        pack = re.findall(r"^\d+\. ([\w./-]+\.md)", bet["sections"]["Context pack"] or "", re.M)
        absent = [p for p in pack if not (self.context / p).exists()]
        self.check("context-pack-exists", bool(pack) and not absent, ", ".join(absent) or "no pack entries")
        self.check_catalogue_untouched()
        self.check_catalogue_statuses()
        self.check_no_code_change()

    def scenario_shape_too_big(self):
        bet = self.bet()
        if not self.check("bet-exists", bet is not None, "no bet 04"):
            return
        self.check_shape_common(bet)
        self.check("status-shaped", bet["header"].get("Status") == "shaped", f"{bet['header'].get('Status')}")
        self.check("pin-not-yet", bet["header"].get("Context pinned") == "not yet", f"{bet['header'].get('Context pinned')}")
        rows, checks = deltas(bet), parse_checks(bet)
        self.check("deltas-fit-appetite", len(rows) <= 6, f"{len(rows)} requirement deltas")
        self.check("checks-fit-appetite", len(checks) <= 12, f"{len(checks)} checks")
        out = [r["ID"] for r in rows if re.search(r"photo|weather|sync", r["Text or reason"], re.I)]
        self.check("scope-cut-by-outcome", not out, ", ".join(out))
        self.check_board()
        note = self.read("context/research/2026-11-03-plant-care-assistant.md") or ""
        self.check("framing-note-linked", re.search(r"^Bet: (bet )?04 \(bets/04-[a-z0-9-]+\.md\)$", note, re.M | re.I) is not None, "note's Bet line")
        self.check("head-unchanged", self.git("rev-parse", "HEAD").strip() == self.head, "a commit was made")

    def scenario_shape_approve(self):
        bet = self.bet()
        if not self.check("bet-exists", bet is not None, "no bet 04"):
            return
        self.check_shape_common(bet)
        self.check("status-approved", bet["header"].get("Status") == "approved", f"{bet['header'].get('Status')}")
        autonomy = bet["header"].get("Autonomy", "")
        self.check("autonomy-fields", AUTONOMY.search(autonomy) is not None, autonomy)
        self.check("autonomy-approved-words", re.search(r"Approved \d{4}-\d{2}-\d{2}: [\"“]", autonomy) is not None, autonomy)
        pin = bet["header"].get("Context pinned", "")
        if not self.check("pin-recorded", re.fullmatch(r"[0-9a-f]{40}", pin) is not None and self.resolve(pin) == pin, f"pin is {pin!r}"):
            return
        self.check("pin-in-history", self.is_ancestor(pin), f"{pin} is not an ancestor of HEAD")
        at_pin = self.blob(pin, self.bet_rel())
        if not self.check("bet-at-pin", at_pin is not None, "bet is not in the pinned commit"):
            return
        pinned = parse_bet(at_pin)
        self.check("pin-holds-approved-bet", pinned["header"].get("Status") == "approved" and
                   pinned["header"].get("Context pinned") == "not yet", f"{pinned['header']}")
        self.check_shaped_fields_intact(bet, pinned)
        commits = self.commits_since()
        self.check("two-commits-at-gate", len(commits) == 2, f"{len(commits)} commits since the framed baseline")
        if len(commits) == 2:
            self.check("pin-commit-is-pin-line-only", commits[0] == pin and self.commit_paths(commits[1]) == [self.bet_rel()] and
                       self.git("diff", "--unified=0", pin, commits[1]).count("\n+") == 2, "second commit is more than the pin line")
        pack = re.findall(r"^\d+\. ([\w./-]+\.md)", bet["sections"]["Context pack"] or "", re.M)
        missing = [p for p in pack if self.blob(pin, f"context/{p}") is None]
        self.check("context-pack-at-pin", bool(pack) and not missing, ", ".join(missing))
        self.check("framing-note-in-pin", self.blob(pin, "context/research/2026-11-02-snooze-while-away.md") is not None, "note not committed")
        note = self.blob(pin, "context/research/2026-11-02-snooze-while-away.md") or ""
        self.check("framing-note-linked", re.search(r"^Bet: (bet )?04 \(bets/04-[a-z0-9-]+\.md\)$", note, re.M | re.I) is not None, "note's Bet line")
        concept = self.blob(pin, "context/architecture/concepts/snooze-window.md") or ""
        self.check("planned-section-at-pin", re.search(r"^Status: planned", concept, re.M) is not None, "no planned section at the pin")
        self.check_board("approved")
        self.check_links()
        self.check_tree_clean()

    def scenario_gate1_unapproved(self):
        bet = self.bet()
        if not self.check("bet-exists", bet is not None, "no bet 04"):
            return
        self.check("status-still-shaped", bet["header"].get("Status") == "shaped", f"{bet['header'].get('Status')}")
        self.check("pin-still-not-yet", bet["header"].get("Context pinned") == "not yet", f"{bet['header'].get('Context pinned')}")
        self.check("no-commit-before-approval", self.git("rev-parse", "HEAD").strip() == self.head, "a commit was made")
        self.check("no-code-before-approval", not [p for p in self.changed() if not p.startswith("context/")],
                   f"code changed: {sorted(p for p in self.changed() if not p.startswith('context/'))}")
        self.check("build-log-empty", not (bet["sections"]["Build log"] or "").strip(), "the Build log is written")
        self.check_catalogue_untouched()

    def run_behaviour(self, rev, limit=14):
        """Builds the bet's checks into a run against the code at rev; returns problems."""
        problems = []
        with tempfile.TemporaryDirectory() as tmp:
            archive = pathlib.Path(tmp) / "a.tar"
            subprocess.run(["git", "-C", str(self.repo), "archive", "-o", str(archive), rev], check=True)
            subprocess.run(["tar", "-xf", str(archive), "-C", tmp], check=True)
            data = pathlib.Path(tmp) / "plants.json"
            def run(args, today):
                return subprocess.run([sys.executable, "sprig.py", "--data", str(data), "--today", today, *args],
                                      cwd=tmp, capture_output=True, text=True)
            tests = subprocess.run([sys.executable, "-m", "unittest"], cwd=tmp, capture_output=True, text=True)
            if tests.returncode or "Ran 0 tests" in tests.stderr:
                problems.append(f"the project's tests fail: {tests.stderr[-200:]}")
            run(["add", "fern", "--every", "7"], "2026-03-01")
            run(["snooze", "fern", "--days", "3"], "2026-03-08")
            if "fern" in run(["due"], "2026-03-10").stdout:
                problems.append("a snoozed plant is listed before the snooze ends")
            if "fern" not in run(["due"], "2026-03-11").stdout:
                problems.append("a plant is not listed once its snooze ended")
            before = data.read_text()
            over = run(["snooze", "fern", "--days", str(limit + 1)], "2026-03-08")
            if over.returncode != 2 or f"between 1 and {limit}" not in over.stderr or data.read_text() != before:
                problems.append(f"--days {limit + 1} is not refused as the pin says (exit {over.returncode})")
            if run(["snooze", "fern", "--days", str(limit)], "2026-03-08").returncode:
                problems.append(f"--days {limit} is refused")
            run(["water", "fern"], "2026-03-09")
            if "fern" not in run(["due"], "2026-03-16").stdout:
                problems.append("watering does not clear the snooze")
        return problems

    def check_commit_separation(self, log, allow_context=True):
        """Code and context commits stay separate, and the Build log lists the code ones (profile, Commits)."""
        since = self.commits_since()
        mixed, code, context_only = [], [], []
        for sha in since:
            paths = self.commit_paths(sha)
            in_context = [p for p in paths if p.startswith("context/")]
            outside = [p for p in paths if not p.startswith("context/")]
            if in_context and outside:
                mixed.append(self.subject(sha))
            (code if outside else context_only).append(sha)
        self.check("commits-separate", not mixed, "; ".join(mixed))
        listed = [self.resolve(s) for s in log["commits"]]
        self.check("code-commits-listed", set(code) <= set(x for x in listed if x) and len(listed) == len(code),
                   f"{len(code)} code commits, {len(listed)} listed")
        order = [s for s in since if s in listed]
        self.check("code-commits-oldest-first", order == listed, "listed out of order")
        stray = [self.subject(s) for s in context_only
                 if [p for p in self.commit_paths(s) if p not in {self.bet_rel(), "context/bets/README.md"}]]
        self.check("context-commits-touch-bet-and-board-only", not stray, "; ".join(stray))
        if allow_context and code and context_only:
            first, last = since.index(code[0]), since.index(code[-1])
            between = [s for s in since[first:last] if s in context_only]
            named = {self.resolve(s) for s in log["context"]}
            self.check("context-commit-between-named", all(s in named for s in between),
                       f"{len(between)} between, {len(named)} named")
        return code

    def check_changelog_entry(self, log):
        text = self.read("CHANGELOG.md") or ""
        unreleased = re.search(r"## \[Unreleased\](.*?)(?=^## \[|\Z)", text, re.S | re.M)
        self.check("changelog-entry", unreleased and re.search("snooze", unreleased.group(1), re.I), "no snooze entry under [Unreleased]")
        listed = {self.resolve(s) for s in log["commits"]}
        adds = self.git("log", "--format=%H", "-G", "snooze", "--", "CHANGELOG.md").split()
        # The newest commit that touched the entry is the one that stands; it must be a listed code commit.
        self.check("changelog-entry-in-code-commit", bool(adds) and adds[0] in listed, "the entry is not in one of the bet's code commits")

    def check_evidence(self, bet, log):
        """A pass carries observed evidence of the kind its Method names (build-loop.md, Proving a check)."""
        problems = []
        for cid, rid, cuttable, method in parse_checks(bet):
            row = log["checks"].get(cid)
            if row is None:
                problems.append(f"{cid} has no row")
                continue
            if row["Result"] == "pass":
                evidence = row["Evidence"]
                if "observed" not in evidence.lower():
                    problems.append(f"{cid} passed without observed evidence")
                elif method == "test" and not re.search(r"test_|unittest", evidence):
                    problems.append(f"{cid}: Method test names no test")
                elif method in {"run and observe", "inspect output"} and "`" not in evidence and '"' not in evidence:
                    problems.append(f"{cid}: Method {method} quotes nothing")
        self.check("evidence-per-check", not problems, "; ".join(problems))

    def check_result_labels(self, bet, log):
        """build-loop.md records pass, fail, blocked or cut; a person's-eye row is listed, never judged.

        Only a `~` check may be cut (SKILL.md, The appetite). A person's-eye check is "not yours to judge",
        so pass and fail do not fit it; it may be blocked when the build cannot show it to the person.
        """
        problems = []
        for cid, rid, cuttable, method in parse_checks(bet):
            row = log["checks"].get(cid)
            if row is None:
                continue
            allowed = {"person's eye", "blocked"} if method == "person's eye" else {"pass", "fail", "blocked"}
            if cuttable:
                allowed.add("cut")
            if row["Result"] not in allowed:
                problems.append(f"{cid} ({method}{', ~' if cuttable else ''}) is {row['Result']}")
        self.check("result-labels-fit-method", not problems, "; ".join(problems))

    def check_built_exit(self, bet, log):
        """The exit condition of `built` (building-prototype-bets/SKILL.md, The loop): every check that is
        not a person's-eye check passed, a cut `~` check does not block it, and no blocking finding is open."""
        unmet = []
        for cid, rid, cuttable, method in parse_checks(bet):
            result = log["checks"].get(cid, {}).get("Result")
            if method != "person's eye" and result != "pass" and not (result == "cut" and cuttable):
                unmet.append(f"{cid} is {result}")
        self.check("built-exit-condition", not unmet, "; ".join(unmet))
        self.check("findings-recorded", re.search(r"^Findings:", log["text"], re.M) is not None, "no Findings line")
        unresolved = self.unresolved_blocking(log)
        self.check("blocking-findings-resolved", not unresolved, "; ".join(unresolved))

    def unresolved_blocking(self, log):
        """Blocking entries on the Findings line (build-loop.md layout: `R1 blocking, fixed in <sha>`) that stand open.

        A confirmed blocking finding is fixed in a commit the verified head contains; one the evidence
        refutes is closed with that evidence (build-loop.md, Fixing). The reviewer's other dispositions,
        `still open`, `reopened` and `unconfirmed`, leave it open, and only a should-fix may be deferred.
        """
        line = re.search(r"^Findings:(.*)$", log["text"], re.M)
        head = self.resolve(log["head"]) if log["head"] else None
        unresolved = []
        for entry in (line.group(1).split(";") if line else []):
            if not re.match(r"\s*R\d+\s+blocking\b", entry):
                continue
            disposition = re.search(r"blocking\b[^,]*,\s*(fixed in `?([0-9a-f]{7,40})|closed|refuted)", entry)
            if disposition is None:
                unresolved.append(entry.strip())
            elif disposition.group(2):
                sha = self.resolve(disposition.group(2))
                if not (sha and head and self.is_ancestor(sha, head)):
                    unresolved.append(f"{entry.strip()} (the fix is not in the verified head)")
        return unresolved

    def check_review(self, log):
        """Fresh review when the host can run one; labelled self-review only when it cannot.

        building-prototype-bets/SKILL.md, step 4: a subagent, else a separate headless session, and with
        neither, self-review labelled in the Build log. The host's capability is a per-trial fact the
        grader cannot see on disk, so grade/review-capability records it: `fresh` or `none`.
        """
        capability = self._grade_file("review-capability")
        if not self.check("review-capability-recorded", capability in {"fresh", "none"}, f"grade/review-capability holds {capability!r}"):
            return
        line = re.search(r"^Review: (.*)$", log["text"], re.M)
        how = line.group(1) if line else ""
        wanted = r"independent in a fresh context" if capability == "fresh" else r"self-review"
        self.check("review-matches-host-capability", re.match(rf"{wanted}, \d+ rounds?\b", how) is not None,
                   f"host capability {capability}, Review line {how!r}")

    def check_working_time(self, log):
        self.check("working-time-recorded", re.search(r"^Working time used:", log["text"], re.M) is not None, "no working-time line")

    def check_verified_head(self, bet, log, limit=14):
        """Head is the commit every result was verified at (build-loop.md, The Build log and Proving a check)."""
        head = self.resolve(log["head"]) if log["head"] else None
        if head is None or not self.is_ancestor(head):
            self.check("verified-head-is-final-code", False, f"Head {log['head']} is not in the branch's history")
        else:
            # "A later commit makes evidence stale": results move forward to the last code commit, row by
            # row with `carried from`, so the head itself must hold the final code.
            later = [p for p in self.git("diff", "--name-only", head, "HEAD", "--", ".", ":(exclude)context").split("\n") if p]
            self.check("verified-head-is-final-code", not later, f"code differs after Head: {later}")
        problems = []
        for cid, rid, cuttable, method in parse_checks(bet):
            row = log["checks"].get(cid, {})
            if row.get("Result") != "pass":
                continue
            carried = re.search(r"carried from `?([0-9a-f]{7,40})", row["Evidence"])
            at = re.search(r"\bat (?:commit )?`?([0-9a-f]{7,40})\b", row["Evidence"])
            if carried:
                sha = self.resolve(carried.group(1))
                if not (sha and head and self.is_ancestor(sha, head)):
                    problems.append(f"{cid} is carried from {carried.group(1)}, which the head does not contain")
            elif not (at and head and self.resolve(at.group(1)) == head):
                problems.append(f"{cid} names {at.group(1) if at else 'no commit'}, not the head, and is not marked carried from")
        self.check("evidence-bound-to-head", not problems, "; ".join(problems))
        revisions = ["HEAD"] if head is None or head == self.git("rev-parse", "HEAD").strip() else ["HEAD", head]
        problems = [f"{rev[:7]}: {p}" for rev in revisions for p in self.run_behaviour(rev, limit)]
        self.check("behaviour-matches-the-pin", not problems, "; ".join(problems))

    def check_built_common(self, bet, log, limit=14):
        """Everything `built` promises, for each scenario that ends in it."""
        self.check_result_labels(bet, log)
        self.check_built_exit(bet, log)
        self.check_evidence(bet, log)
        self.check_review(log)
        self.check_verified_head(bet, log, limit)

    def check_try_it(self, bet, log):
        text = log["text"]
        block = text.split("### Try it", 1)[1] if "### Try it" in text else ""
        last_heading = [h for h in re.findall(r"^###? (.+)$", text, re.M) if not h.startswith("##")]
        self.check("try-it-block", bool(block) and (last_heading and last_heading[-1].startswith("Try it") or "#### " in block), "no ### Try it block")
        head = (log["head"] or "")[:7]
        self.check("try-it-names-head", bool(head) and head in block, "the head commit is not named")
        eye = [c[0] for c in parse_checks(bet) if c[3] == "person's eye"]
        missing = [c for c in eye if c not in block]
        self.check("try-it-lists-eye-checks", not missing, ", ".join(missing))
        self.check("try-it-keep-or-remove", "Keep or remove" in block and "Signal" in block, "no keep-or-remove section")

    def check_build_common(self, limit=14):
        bet = self.bet()
        if not self.check("bet-exists", bet is not None, "no bet 04"):
            return None, None
        self.check("status-built", bet["header"].get("Status") == "built", f"{bet['header'].get('Status')}")
        at_start = parse_bet((self.grade_dir / "bet-at-start.md").read_text())
        self.check("pin-unchanged", bet["header"].get("Context pinned") == at_start["header"].get("Context pinned"), "the pin moved")
        self.check_shaped_fields_intact(bet, at_start)
        log = build_log(bet)
        self.check("build-log-filled", bool(log["base"]) and bool(log["head"]) and bool(log["commits"]), "Base, Head or code commits missing")
        self.check_commit_separation(log)
        autonomy = AUTONOMY.search(at_start["header"].get("Autonomy", ""))
        self.check("on-named-branch", autonomy and self.git("branch", "--show-current").strip() == autonomy.group(1).strip(),
                   f"on {self.git('branch', '--show-current').strip()}")
        self.check_built_common(bet, log, limit)
        self.check_working_time(log)
        self.check_changelog_entry(log)
        self.check_try_it(bet, log)
        self.check_no_push()
        self.check_catalogue_untouched()
        self.check_no_bet_links()
        self.check_planned_owned()
        self.check_links()
        return bet, log

    def scenario_build(self):
        if self.check_build_common()[0] is not None:
            self.check_board("built")
            self.check_tree_clean()

    def scenario_build_drift(self):
        # The pin says 14; a later commit raised the working copy to 30. Building reads the pin.
        if self.check_build_common(limit=14)[0] is not None:
            self.check_board("built")
            self.check_tree_clean()

    def scenario_build_noctx(self):
        bet = self.bet()
        if not self.check("bet-exists", bet is not None, "no bet 04"):
            return
        self.check("status-built", bet["header"].get("Status") == "built", f"{bet['header'].get('Status')}")
        log = build_log(bet)
        since = self.commits_since()
        context = [self.subject(s) for s in since if any(p.startswith("context/") for p in self.commit_paths(s))]
        self.check("no-context-commits", not context, "; ".join(context))
        self.check("code-commits-listed", set(since) == {self.resolve(c) for c in log["commits"]},
                   f"{len(since)} commits, {len(log['commits'])} listed")
        status = self.git("status", "--porcelain")
        self.check("bet-left-uncommitted", self.bet_rel() in status, "the bet file is committed")
        self.check("board-left-uncommitted", "context/bets/README.md" in status, "the board is committed")
        autonomy = AUTONOMY.search(parse_bet((self.grade_dir / "bet-at-start.md").read_text())["header"].get("Autonomy", ""))
        self.check("on-named-branch", self.git("branch", "--show-current").strip() == autonomy.group(1).strip(), f"autonomy {autonomy.group(1)}")
        self.check_built_common(bet, log)
        self.check_working_time(log)
        self.check_no_push()

    def appetite_common(self, status, cut_ids, uncut_ids):
        bet = self.bet()
        if not self.check("bet-exists", bet is not None, "no bet 04"):
            return None, None
        self.check(f"status-{status}", bet["header"].get("Status") == status, f"{bet['header'].get('Status')}")
        log = build_log(bet)
        for cid in cut_ids:
            row = log["checks"].get(cid, {})
            self.check(f"cuttable-check-cut:{cid}", row.get("Result") == "cut", f"{row.get('Result')}")
        cuts = re.search(r"^Cuts: (.*)", log["text"], re.M)
        self.check("cut-recorded-with-reason", cuts is not None and all(c in cuts.group(1) for c in cut_ids) and "WAT-09" in cuts.group(1),
                   "the Cuts line must name the check and its requirement")
        for cid in uncut_ids:
            row = log["checks"].get(cid, {})
            self.check(f"uncuttable-check-not-cut:{cid}", row.get("Result") != "cut", "a check without ~ is cut")
        self.check("no-work-past-the-appetite", not [s for s in self.commits_since() if [p for p in self.commit_paths(s) if not p.startswith("context/")]],
                   "code commits after the limit")
        self.check_working_time(log)
        self.check("appetite-not-raised", bet["header"].get("Appetite") == "½ day", f"{bet['header'].get('Appetite')}")
        self.check_no_push()
        self.check_catalogue_untouched()
        self.check_board(status)
        return bet, log

    def scenario_appetite_cut(self):
        bet, log = self.appetite_common("built", ["C4"], ["C1", "C2", "C3"])
        if bet is not None:
            self.check_built_common(bet, log)
            self.check_try_it(bet, log)
            self.check_tree_clean()

    def scenario_appetite_stop(self):
        bet, log = self.appetite_common("stopped", ["C4"], ["C1", "C2", "C3"])
        if bet is not None:
            self.check_result_labels(bet, log)
            # SKILL.md, The appetite: `stopped` is for when the remaining checks still do not pass.
            unmet = [c[0] for c in parse_checks(bet) if c[3] != "person's eye" and log["checks"].get(c[0], {}).get("Result") not in {"pass", "cut"}]
            self.check("stopped-has-an-unmet-check", bool(unmet), "every check passed or was cut, so the bet is not stopped")
            self.check("open-line-says-what-is-left", re.search(r"^Open: \S", log["text"], re.M) is not None, "no Open line")
            self.check("pin-kept", bet["header"].get("Context pinned", "").startswith("not yet") is False, "the pin was reset")
            self.check_tree_clean()

    def scenario_gate2_undecided(self):
        bet = self.bet()
        if not self.check("bet-exists", bet is not None, "no bet 04"):
            return
        self.check("status-still-built", bet["header"].get("Status") == "built", f"{bet['header'].get('Status')}")
        self.check("result-still-empty", not (bet["sections"]["Result"] or "").strip(), "the Result is written")
        self.check("no-close-without-decision", self.git("rev-parse", "HEAD").strip() == self.head and
                   self.git("status", "--porcelain") == (self.grade_dir / "status").read_text(), "the workspace changed")
        self.check_catalogue_untouched()

    def check_close_common(self, status, words):
        bet = self.bet()
        if not self.check("bet-exists", bet is not None, "no bet 04"):
            return None
        self.check(f"status-{status}", bet["header"].get("Status") == status, f"{bet['header'].get('Status')}")
        result = bet["sections"]["Result"] or ""
        self.check("result-holds-decision", result.lower().startswith(status) and re.search(r"\d{4}-\d{2}-\d{2}", result) is not None,
                   result[:60])
        normal = " ".join(result.split())
        self.check("result-holds-the-persons-words", words in normal, "the person's words are not in the Result verbatim")
        self.check("result-holds-a-lesson", "Lesson" in result or "lesson" in result, "no lesson")
        at_start = parse_bet((self.grade_dir / "bet-at-start.md").read_text())
        self.check_shaped_fields_intact(bet, at_start)
        # House rule 9: closing writes the Result and the catalogue. The pin and the Build log, with its
        # ordered ledger of code and context commits, stay as building left them (bet.md, Build log).
        self.check("closing-preserves-pin", bet["header"].get("Context pinned") == at_start["header"].get("Context pinned"),
                   f"{bet['header'].get('Context pinned')}")
        self.check("closing-preserves-build-log", bet["sections"]["Build log"] == at_start["sections"]["Build log"], "the Build log changed at close")
        self.check_catalogue_statuses()
        self.check_dropped_rows()
        self.check_index_counts()
        self.check_board(status)
        self.check_no_bet_links()
        self.check_planned_owned()
        self.check_links()
        self.check_no_push()
        self.check_tree_clean()
        return bet

    def scenario_keep(self):
        bet = self.check_close_common("kept", KEEP_WORDS)
        if bet is None:
            return
        since = self.commits_since()
        code = [s for s in since if [p for p in self.commit_paths(s) if not p.startswith("context/")]]
        self.check("keep-reverts-nothing", not code and len(since) == 1, f"{len(since)} commits, {len(code)} touch code")
        self.check_kept_rows(bet)
        concept = self.read("context/architecture/concepts/snooze-window.md")
        self.check("architecture-built", concept is not None and re.search(r"^Status: built", concept, re.M) is not None, "concept is not built")
        self.check("changelog-entry-stays", "snooze" in (self.read("CHANGELOG.md") or ""), "the entry is gone")
        self.check("code-still-there", not self.run_behaviour("HEAD"), "the snooze behaviour is gone")

    def pinned_bet(self):
        """The bet as approved; closing reads every field but Status, pin, Build log and Result at the pin.

        The pin comes from the bet as it was before closing, so a pin corrupted at close cannot blind this.
        A pin of `not yet` has no approved snapshot, and the draft as it stood is read (closing SKILL.md).
        """
        at_start = (self.grade_dir / "bet-at-start.md").read_text()
        at_pin = self.blob(parse_bet(at_start)["header"].get("Context pinned", ""), self.bet_rel())
        return parse_bet(at_pin or at_start)

    @staticmethod
    def same_text(a, b):
        return " ".join((a or "").split()) == " ".join((b or "").split())

    def check_other_rows_untouched(self, delta_ids):
        rows, at_start = self.catalogue(), self.catalogue(self.head)
        changed = [rid for rid in set(rows) | set(at_start) if rid not in delta_ids and rows.get(rid) != at_start.get(rid)]
        self.check("other-rows-untouched", not changed, ", ".join(sorted(changed)))

    def check_kept_rows(self, bet):
        """Each pinned delta against its catalogue row, honouring the recorded cuts (keep-and-remove.md, Keep step 2)."""
        pinned, log = self.pinned_bet(), build_log(bet)
        rows, at_start = self.catalogue(), self.catalogue(self.head)
        checks = parse_checks(pinned)
        for delta in deltas(pinned):
            rid, change, text = delta["ID"], delta["Change"], delta["Text or reason"]
            row = rows.get(rid) or {}
            own = [log["checks"].get(c[0], {}).get("Result") for c in checks if c[1] == rid]
            all_cut, some_cut = bool(own) and all(r == "cut" for r in own), "cut" in own
            if change == "new" and all_cut:
                self.check(f"cut-requirement-dropped:{rid}", row.get("Status") == "dropped" and "bet 04: cut" in row.get("Notes", ""), f"{row}")
                self.check(f"keep-row-text:{rid}", self.same_text(row.get("Requirement"), text), f"{row.get('Requirement')!r}")
            elif change == "new" and some_cut:
                # Partly cut: built, with the text narrowed, and the note says what was left out.
                self.check(f"keep-row-built:{rid}", row.get("Status") == "built" and bool(row.get("Notes", "").strip()), f"{row}")
            elif change == "new":
                self.check(f"keep-row-built:{rid}", row.get("Status") == "built", f"{row}")
                self.check(f"keep-row-text:{rid}", self.same_text(row.get("Requirement"), text), f"{row.get('Requirement')!r}")
            elif change == "changed" and all_cut:
                self.check(f"changed-row-updated:{rid}", row == at_start.get(rid), "all its checks were cut, so the row keeps its old text")
            elif change == "changed":
                old = " ".join((at_start.get(rid) or {}).get("Requirement", "").split())
                notes = " ".join(row.get("Notes", "").split())
                self.check(f"changed-row-updated:{rid}", row.get("Status") == "built" and (some_cut or self.same_text(row.get("Requirement"), text))
                           and re.search(r"changed by bet 04: was [\"“]", notes) is not None and old in notes, f"{row}")
            else:
                self.check(f"dropped-row-updated:{rid}", row.get("Status") == "dropped" and re.search(r"\d{4}-\d{2}-\d{2}", row.get("Notes", "")) is not None
                           and " ".join(text.split()) in " ".join(row.get("Notes", "").split()), f"{row}")
        self.check_other_rows_untouched({d["ID"] for d in deltas(pinned)})

    def check_removed_rows(self, words):
        """keep-and-remove.md, Remove step 7: new IDs dropped, the delta's text kept; other rows stay as they were."""
        pinned = self.pinned_bet()
        catalogue, at_start = self.catalogue(), self.catalogue(self.head)
        problems = []
        for delta in deltas(pinned):
            rid = delta["ID"]
            row = catalogue.get(rid) or {}
            if delta["Change"] == "new":
                if row.get("Status") != "dropped" or "bet 04 removed:" not in row.get("Notes", "") or not re.search(r"\d{4}-\d{2}-\d{2}", row.get("Notes", "")):
                    problems.append(f"{rid}: {row}")
                self.check(f"remove-row-text:{rid}", self.same_text(row.get("Requirement"), delta["Text or reason"]), f"{row.get('Requirement')!r}")
            else:
                self.check(f"changed-row-unchanged:{rid}", row == at_start.get(rid), f"{rid} changed")
        self.check("remove-rows-dropped", not problems, "; ".join(problems))
        self.check_other_rows_untouched({d["ID"] for d in deltas(pinned)})
        concept = self.context / "architecture/concepts/snooze-window.md"
        self.check("planned-architecture-deleted", not concept.exists(), "the planned concept still exists")
        refs = [str(p.relative_to(self.repo)) for p in self.context.rglob("*.md") if "snooze-window" in p.read_text()
                and not p.name.startswith("04-")]
        self.check("no-references-to-deleted-architecture", not refs, ", ".join(refs))

    def tree_after_reverting(self, commits):
        """The code tree of the baseline with the listed commits reverted, or None on a conflict."""
        with tempfile.TemporaryDirectory() as tmp:
            clone = pathlib.Path(tmp) / "clone"
            subprocess.run(["git", "clone", "-q", str(self.repo), str(clone)], check=True, capture_output=True)
            git = lambda *args: subprocess.run(["git", "-C", str(clone), *args], capture_output=True, text=True)
            git("checkout", "-q", "--detach", self.head)
            if not commits or git("revert", "--no-commit", *reversed(commits)).returncode:
                return None
            tree = git("write-tree").stdout.strip()
            return [l for l in git("ls-tree", "-r", tree).stdout.split("\n") if l and "\tcontext/" not in l]

    def scenario_remove(self):
        bet = self.check_close_common("removed", REMOVE_WORDS)
        if bet is None:
            return
        since = self.commits_since()
        ok = len(since) == 2
        detail = f"{len(since)} commits"
        if ok:
            first, second = self.commit_paths(since[0]), self.commit_paths(since[1])
            ok = all(not p.startswith("context/") for p in first) and first and all(p.startswith("context/") for p in second) and second
            detail = f"first touches {first}, second {second[:3]}"
        self.check("revert-and-context-separate", ok, detail)
        expected = self._grade_file("expected-after-remove.tree").split("\n")
        actual = [l for l in self.git("ls-tree", "-r", "HEAD").split("\n") if l and "\tcontext/" not in l]
        self.check("code-reverted-exactly", actual == expected, f"expected {len(expected)} entries, got {len(actual)}")
        # closing-prototype-bets/SKILL.md: the revert covers exactly the commits the surviving Build log lists.
        ledger = [self.resolve(c) for c in build_log(bet)["commits"]]
        self.check("revert-matches-the-ledger", all(ledger) and self.tree_after_reverting(ledger) == actual, f"{len(ledger)} commits listed")
        unrelated = self._grade_file("unrelated-commit")
        self.check("unrelated-commit-preserved", self.is_ancestor(unrelated) and self.blob("HEAD", "test_names.py") is not None and
                   "cannot be empty" in (self.blob("HEAD", "sprig.py") or ""), "the unrelated commit's change is gone")
        leftovers = [p for p in self.git("ls-files").split("\n") if p and not p.startswith("context/") and p != "CHANGELOG.md"
                     and "snooze" in (self.read(p) or "")]
        self.check("bet-code-gone", not leftovers, ", ".join(leftovers))
        self.check("changelog-entry-gone", "snooze" not in (self.read("CHANGELOG.md") or ""), "the [Unreleased] entry survived the revert")
        self.check_removed_rows(REMOVE_WORDS)

    def scenario_remove_nocode(self):
        bet = self.check_close_common("removed", DROP_WORDS)
        if bet is None:
            return
        since = self.commits_since()
        self.check("nothing-to-revert", not [s for s in since if self.subject(s).lower().startswith("revert") or
                                             [p for p in self.commit_paths(s) if not p.startswith("context/")]],
                   "a revert or code commit was made for a bet with no code")
        self.check("one-context-close", len(since) == 1, f"{len(since)} commits")
        self.check("result-says-nothing-built", re.search(r"nothing was built|nothing to revert", bet["sections"]["Result"] or "", re.I) is not None,
                   "the Result does not say nothing was built")
        self.check_removed_rows(DROP_WORDS)

    # static scenarios: WORK is the repository root

    SKILLS = "skills/product-prototyping"
    FORBIDDEN = [
        (r"Claude Code|CLAUDE\.md|\bCodex\b|Copilot|\bCursor\b|\bGemini\b|\bWindsurf\b", "harness name"),
        (r"~/\.[a-z]|\.claude/|\.agents/|\.codex/|/Users/|/home/|\$HOME", "install path"),
        (r"\$\{?(?!NAME\b)[A-Z][A-Z0-9_]{2,}", "environment variable"),
    ]

    def scenario_agnostic(self):
        root = self.work / self.SKILLS
        hits, links = [], []
        # Only the skill directories: the category's README and CHANGELOG are not part of any skill (decision 0015).
        for path in sorted(root.glob("*/**/*.md")):
            text = path.read_text()
            rel = path.relative_to(self.work)
            for pattern, kind in self.FORBIDDEN:
                for match in re.finditer(pattern, text):
                    hits.append(f"{rel}: {kind} {match.group(0)!r}")
            skill = rel.parts[2] if len(rel.parts) > 3 else None
            if skill:
                for target in re.findall(r"\]\((?!https?:|#)([^)\s]+)\)", clean(re.sub(r"`[^`]*`", "", text))):
                    resolved = (path.parent / target.split("#")[0]).resolve()
                    if root / skill not in resolved.parents and resolved != root / skill:
                        links.append(f"{rel} -> {target}")
        self.check("no-harness-install-path-or-env-var", not hits, "; ".join(hits[:8]))
        self.check("links-stay-in-the-skill", not links, "; ".join(links[:8]))

    def scenario_contract(self):
        """Every heading, column and field this grader reads is still defined by the templates."""
        skills = self.work / self.SKILLS
        read = lambda rel: (skills / rel).read_text()
        bet = read("shaping-prototype-bets/templates/bet.md")
        self.check("contract-bet-sections", [h for h in headings(bet) if h in BET_SECTIONS] == BET_SECTIONS, f"{headings(bet)}")
        self.check("contract-bet-header", all(re.search(rf"^{f}:", bet, re.M) for f in ("Status", "Appetite", "Autonomy", "Context pinned")), "bet.md header")
        self.check("contract-bet-delta-columns", table_with(bet, "ID", "Change", "Text or reason") is not None, "bet.md deltas table")
        check_line = "- C1 ([ABC-01]): [observable result] · Method: [test]"
        self.check("contract-check-line", check_line in bet, "bet.md check line")
        board = read("shaping-prototype-bets/templates/bet-board.md")
        self.check("contract-board-columns", table_with(board, "Bet", "Status", "Appetite", "Reserved IDs") is not None, "bet-board.md")
        note = read("framing-prototype-ideas/templates/framing-note.md")
        self.check("contract-note-sections", [h for h in headings(note) if h in NOTE_SECTIONS] == NOTE_SECTIONS, f"{headings(note)}")
        self.check("contract-note-header", all(re.search(rf"^{f}:", note, re.M) for f in ("Date", "Verdict", "Bet")), "framing-note.md")
        self.check("contract-note-option-columns", table_with(note, "Option", "Value", "Appetite estimate", "Risk", "Reversibility") is not None, "framing-note.md options")
        capability = read("closing-prototype-bets/templates/capability-requirements.md")
        self.check("contract-capability-columns", table_with(capability, "ID", "Requirement", "Status", "Notes") is not None, "capability template")
        index = read("closing-prototype-bets/templates/requirements-index.md")
        self.check("contract-index-columns", table_with(index, "Prefix", "File", "Built", "Dropped") is not None, "requirements index")
        id_map = read("structuring-prototype-context/templates/id-map.md")
        self.check("contract-id-map-columns", table_with(id_map, "Input", "Local ID", "Catalogue ID", "How") is not None, "id-map.md")
        notes = read("structuring-prototype-context/templates/notes.md")
        self.check("contract-notes-columns", table_with(notes, "ID", "Question", "Status") is not None and table_with(notes, "ID", "Risk", "Status") is not None, "notes.md")
        migration = read("structuring-prototype-context/templates/migration-map.md")
        self.check("contract-map-sections", all(h in headings(migration) for h in ["Map", "Conflicts and duplicates", "Built rows and their evidence", "Verification", "History"]), f"{headings(migration)}")
        self.check("contract-map-approved-line", "Approved: [YYYY-MM-DD:" in migration, "migration-map.md Approved line")
        agents = read("structuring-prototype-context/templates/agents-map.md")
        self.check("contract-agents-sections", all(h in headings(agents) for h in ["Map", "Reading order by task", "House rules", "Code and changelogs", "Graduation"]), f"{headings(agents)}")
        self.check("contract-house-rule-9", "A bet is read at the commit it was approved at" in agents, "agents-map.md rule 9")
        loop = read("building-prototype-bets/references/build-loop.md")
        for needle in ("Started:", "Base:", "Head:", "Working time used:", "Code commits, oldest first:", "Review:", "Findings:", "Cuts:", "Open:", "### Try it"):
            self.check(f"contract-build-log:{needle.rstrip(':')}", needle in loop, needle)
        for needle in ("fixed in", "carried from", "self-review"):
            self.check(f"contract-build-loop:{needle}", needle in loop, needle)
        self.check("contract-build-log-table", table_with(loop, "Check", "Result", "Evidence") is not None, "build-loop.md table")
        try_it = read("building-prototype-bets/templates/try-it.md")
        self.check("contract-try-it-block", all(h in try_it for h in ["### Try it", "#### Keep or remove", "#### What to look at"]), "try-it.md")
        profile = read("structuring-prototype-context/references/prototype-profile.md")
        self.check("contract-profile-statuses", all(w in profile for w in ["`shaped`", "`approved`", "`building`", "`built`", "`kept`", "`removed`", "`stopped`"]), "bet statuses")
        self.check("contract-profile-methods", all(f"`{m}`" in profile for m in METHODS), "Method values")
        self.check("contract-profile-autonomy", "code commits: <branch>; context commits: yes or no; push: yes or no; revert on remove: yes or no" in profile, "Autonomy line")
        self.check("contract-profile-changed-note", "changed by bet NN" in read("closing-prototype-bets/references/keep-and-remove.md"), "changed-row note")
        keep_remove = read("closing-prototype-bets/references/keep-and-remove.md")
        self.check("contract-keep-delta-text", "the delta's text" in keep_remove and "Keep the delta's text" in keep_remove, "delta text rule")
        self.check("contract-remove-note", "bet NN removed: <reason>" in keep_remove and "bet NN: cut," in keep_remove, "dropped-row notes")


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    grader = Grader(sys.argv[1], sys.argv[2])
    method = "scenario_" + sys.argv[2].replace("-", "_")
    if not hasattr(grader, method):
        print(f"unknown scenario: {sys.argv[2]}", file=sys.stderr)
        return 2
    getattr(grader, method)()
    return 1 if grader.failed else 0


if __name__ == "__main__":
    sys.exit(main())
