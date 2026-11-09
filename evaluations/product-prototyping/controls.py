#!/usr/bin/env python3
"""Runs every positive and negative control of the product-prototyping grader.

Usage: controls.py [name-filter]

A positive control is a good end state, built by fixture.sh or by a good-end function below, on
which the grader must exit 0. A negative control is that end state with one named fault planted,
on which the grader must print `FAIL <check>` for the check that names the fault. Each control runs
in its own copy of a fixture under a temporary directory, which is removed afterwards.
Ends with `controls: N/N` and exits non-zero when any control did not behave.
"""

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
FIXTURES = HERE / "fixtures"
PYTHON = sys.executable
sys.path.insert(0, str(HERE))
import grade  # noqa: E402

BET = "context/bets/04-snooze-while-away.md"
BOARD = "context/bets/README.md"
WATERING = "context/product/requirements/watering.md"
INDEX = "context/product/requirements/README.md"
CONCEPT = "context/architecture/concepts/snooze-window.md"
ENV = dict(GIT_AUTHOR_NAME="Control", GIT_AUTHOR_EMAIL="c@example.com",
           GIT_COMMITTER_NAME="Control", GIT_COMMITTER_EMAIL="c@example.com",
           GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null", PATH="/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin")


class Workspace:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.repo = self.path / "sprig"

    def git(self, *args):
        run = subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True, text=True, env=ENV)
        if run.returncode:
            raise RuntimeError(f"git {args}: {run.stderr}")
        return run.stdout.strip()

    def path_of(self, rel):
        return self.repo / rel

    def read(self, rel):
        return self.path_of(rel).read_text()

    def write(self, rel, text):
        target = self.path_of(rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def sub(self, rel, pattern, repl, count=1, flags=re.M):
        text = self.read(rel)
        new, made = re.subn(pattern, repl, text, count=count, flags=flags)
        assert made, f"{pattern!r} not found in {rel}"
        self.write(rel, new)

    def append(self, rel, text):
        self.write(rel, self.read(rel).rstrip("\n") + "\n" + text)

    def commit(self, subject, *paths):
        if paths:
            self.git("add", *paths)
        else:
            self.git("add", "-A")
        self.git("commit", "-q", "-m", subject)
        return self.git("rev-parse", "HEAD")

    def grade_file(self, name):
        return (self.path / "grade" / name).read_text().strip()


def set_status(w, status):
    w.sub(BET, r"^Status: .*$", f"Status: {status}")
    w.sub(BOARD, r"^(\| \[04 .*?\]\(.*?\) \|) [a-z]+ \|", rf"\1 {status} |")


def clear_reserved(w):
    w.sub(BOARD, r"^(\| \[04 .*?\| [^|]* \|) WAT-07, WAT-08, WAT-09 \|", r"\1 none |")


def rebuild_counts(w, watering_built, watering_dropped):
    w.sub(INDEX, r"^\| Watering \| WAT \| (.*?) \| \d+ \| \d+ \|$", rf"| Watering | WAT | \1 | {watering_built} | {watering_dropped} |")


def write_result(w, text):
    w.sub(BET, r"^## Result\n*", f"## Result\n\n{text}\n")


# Good ends: what a correct trial leaves on disk


def good_frame_settled(w):
    w.write("context/research/2026-11-08-email-me.md", f"""# Framing: Email reminders again

Date: 2026-11-08
Verdict: stop
Bet: not yet

## Idea

> Sprig should email me when a plant is due.

## Evidence

- Context: `WAT-05` was dropped because a reminder needs a mail server and an account; decision 0003 keeps Sprig offline. The reason still holds.

## Verdict

stop: WAT-05 and decision 0003 settle it.
""")
    w.append("context/research/README.md", "| [2026-11-08-email-me.md](2026-11-08-email-me.md) | Email reminders again | stop |\n")


def good_frame_open(w):
    w.write("context/research/2026-11-08-rooms.md", """# Framing: Group plants by room

Date: 2026-11-08
Verdict: shape
Bet: not yet

## Idea

> Group plants by room so I can water one room at a time.

## Problem

The plant keeper walks from room to room and has to scan the whole due list in each one.

## Evidence

- Code: `sprig.py`: plants carry only an interval and a last date.
- Context: WAT-02 lists every due plant.

## Options

| Option | Value | Appetite estimate | Risk | Reversibility |
|---|---|---|---|---|
| A: A room label per plant | The due list groups by room | 1 day | The label goes stale | easy |
| B: A separate list per room | Fewer plants to scan | 2 days | Two lists to keep | moderate |

## Recommendation

A, because the problem is scanning and a label is enough. B would win if rooms were kept apart.

## Remove if

- The rooms are not used after a week.

## Verdict

shape: option A.
""")
    w.append("context/research/README.md", "| [2026-11-08-rooms.md](2026-11-08-rooms.md) | Group plants by room | shape |\n")


FERTILISING_BET = """# Bet 04: A fertilising date for each plant

Status: shaped
Appetite: 1 day · Framing: research/2026-11-03-plant-care-assistant.md
Autonomy: code commits: main; context commits: yes; push: no; revert on remove: yes
Context pinned: not yet

## Outcome

The plant keeper records when a plant was fertilised and `fertilise-due` lists the ones whose next date has passed.

## Requirement deltas

| ID | Change | Text or reason |
|---|---|---|
| FRT-01 | new | `fertilise NAME` records today as the last fertilising |
| FRT-02 | new | `fertilise-due` lists every plant whose next fertilising date is today or earlier |

## Acceptance checks

- C1 (FRT-01): `fertilise fern` writes today's date to the data file. · Method: test
- C2 (FRT-02): A fern fertilised on 2026-03-01 every 30 days is listed on 2026-03-31 and not on 2026-03-30. · Method: test

## Boundaries

- No-go: photos, weather and sync; none of them fit this bet.
- Rabbit hole: none.

## Keep or remove

- Signal: a date is recorded within the month.
- If removed: the code commits are reverted and FRT-01 and FRT-02 are recorded as dropped.

## Architecture

- Touches: the one file `sprig.py` (architecture/context.md)
- Introduces: none
- Relies on: none

## Context pack

1. product/overview.md: what Sprig is

## Build log

## Result
"""


def good_shape_too_big(w):
    w.write("context/bets/04-a-fertilising-date.md", FERTILISING_BET)
    w.sub("context/research/2026-11-03-plant-care-assistant.md", r"^Bet: not yet$", "Bet: 04 (bets/04-a-fertilising-date.md)")
    w.append(BOARD, "| [04 A fertilising date for each plant](04-a-fertilising-date.md) | shaped | 1 day | FRT-01, FRT-02 | research/2026-11-03-plant-care-assistant.md |\n")


def good_appetite_cut(w):
    log = w.read(BET)
    w.sub(BET, r"^\| ~ C4 \(WAT-09\) \| blocked \| not started \|$", "| ~ C4 (WAT-09) | cut | out of appetite at ½ day: the `snoozed until` text in `list`; WAT-09 has no other check |")
    w.sub(BET, r"^(Findings: .*)$", r"\1\nCuts: ~ C4 (WAT-09), the `snoozed until` text in `list`, cut at the limit of the appetite")
    head = re.search(r"Head: ([0-9a-f]{40})", log).group(1)
    try_it = (FIXTURES / "bet04/build-log.md").read_text().split("### Try it", 1)[1].replace("@@HEAD@@", head).replace("@@BRANCH@@", "main")
    w.sub(BET, r"^## Result", f"### Try it{try_it}\n## Result".replace("\\", r"\\"))
    set_status(w, "built")
    w.commit("docs(context): finish bet 04", BET, BOARD)


def good_appetite_stop(w):
    w.sub(BET, r"^\| ~ C4 \(WAT-09\) \| blocked \| not started \|$", "| ~ C4 (WAT-09) | cut | out of appetite at ½ day: the `snoozed until` text in `list` was cut first |")
    w.sub(BET, r"^(Findings: .*)$", r"\1\nCuts: ~ C4 (WAT-09), the `snoozed until` text in `list`\nOpen: C2 (WAT-08), the limit on the days, is not built; nothing left to cut")
    set_status(w, "stopped")
    w.commit("docs(context): stop bet 04", BET, BOARD)


def good_keep(w):
    write_result(w, f'Kept, 2026-11-08: "{grade.KEEP_WORDS}" Lesson: one command before a trip is all a snooze has to be.')
    set_status(w, "kept")
    clear_reserved(w)
    w.append(WATERING, '| WAT-07 | `snooze NAME --days N` hides a plant from `due` for N days from today | built | bet 04 |\n')
    w.append(WATERING, "| WAT-08 | A snooze is between 1 and 14 days; anything else is refused with status 2 | built | bet 04 |\n")
    w.append(WATERING, "| WAT-09 | `list` shows `snoozed until YYYY-MM-DD` for a snoozed plant | dropped | 2026-11-08, bet 04: cut, out of the appetite |\n")
    w.sub(WATERING, r"^\| WAT-02 \| .*$",
          '| WAT-02 | `due` lists every plant whose next watering date is today or earlier, except a plant that is snoozed | built | changed by bet 04: was "`due` lists every plant whose next watering date is today or earlier" |')
    w.sub(CONCEPT, r"^Status: planned$", "Status: built")
    rebuild_counts(w, 6, 2)
    w.commit("docs(context): keep bet 04")


def good_remove(w, also_revert_unrelated=False):
    commits = w.grade_file("bet-code-commits").split()
    reverts = ([w.grade_file("unrelated-commit")] if also_revert_unrelated else []) + list(reversed(commits))
    w.git("revert", "--no-commit", *reverts)
    w.commit("revert: remove the snooze (bet 04)")
    close_removed(w, grade.REMOVE_WORDS, f'Removed, 2026-11-08: "{grade.REMOVE_WORDS}" Lesson: nobody snoozes after the first day.')


def close_removed(w, words, result):
    write_result(w, result)
    set_status(w, "removed")
    clear_reserved(w)
    for rid, text in [("WAT-07", "`snooze NAME --days N` hides a plant from `due` for N days from today"),
                      ("WAT-08", "A snooze is between 1 and 14 days; anything else is refused with status 2"),
                      ("WAT-09", "`list` shows `snoozed until YYYY-MM-DD` for a snoozed plant")]:
        w.append(WATERING, f"| {rid} | {text} | dropped | 2026-11-08, bet 04 removed: {words.split('. ')[-1].rstrip('.').lower()} |\n")
    w.path_of(CONCEPT).unlink()
    rebuild_counts(w, 4, 4)
    w.commit("docs(context): remove bet 04")


def good_remove_nocode(w):
    close_removed(w, grade.DROP_WORDS, f'Removed, 2026-11-08: "{grade.DROP_WORDS}" Nothing was built. Lesson: the idea did not survive a second look.')


def good_create(w):
    shutil.copytree(FIXTURES / "context", w.repo / "context")
    for name in ("01-the-due-list.md", "02-email-reminders.md", "03-a-watering-chart.md"):
        w.path_of(f"context/bets/{name}").unlink()
    for note in w.path_of("context/research").glob("2026-*"):
        note.unlink()
    w.write(BOARD, "# Bets\n\nNo bets yet.\n\n| Bet | Status | Appetite | Reserved IDs | Framing |\n|---|---|---|---|---|\n")
    w.write("context/research/README.md", "# Research\n\nDated evidence and framing notes.\n\n| File | What it answers | Status |\n|---|---|---|\n")
    w.sub(WATERING, r"^\| WAT-05 .*\n", "")
    rebuild_counts(w, 4, 0)
    w.write("context/product/requirements/id-map.md", "# Requirement ID map\n\n| Date | Input | Local ID | Catalogue ID | How |\n|---|---|---|---|---|\n")
    shutil.copy(FIXTURES / "app/CHANGELOG.md", w.repo / "CHANGELOG.md")
    w.append("AGENTS.md", "\nContext map: `context/AGENTS.md`. Decisions index: `context/decisions/README.md`.\n")


def good_adopt_map(w):
    w.write("context/research/2026-11-08-migration-map.md", (FIXTURES / "controls/migration-map.md").read_text())


def good_adopt_move(w):
    good_create(w)
    w.write("context/research/2026-11-08-migration-map.md", (FIXTURES / "controls/migration-map.md").read_text())
    w.sub("context/research/2026-11-08-migration-map.md", r"Approved: pending", 'Approved: 2026-11-08: "Approved. Take every recommended answer and confirm X1."')
    w.sub("context/research/2026-11-08-migration-map.md", r"Sections mapped: pending", "Sections mapped: 18 of 18")
    w.write("context/product/requirements/plants.md", """# Plants (PLT)

Registering and listing plants.

| ID | Requirement | Status | Notes |
|---|---|---|---|
| PLT-01 | `add NAME --every DAYS` registers a plant with its interval | built | |
| PLT-02 | Plant names are unique, ignoring case | built | the spec said case-sensitive; the code is not |
| PLT-03 | `list` shows every plant with its interval and next watering date | built | |
| PLT-04 | Adding a plant stores today as its first watering | built | |
| PLT-05 | `remove NAME` deletes a plant | built | adopted from the code |
""")
    w.write(WATERING, """# Watering (WAT)

| ID | Requirement | Status | Notes |
|---|---|---|---|
| WAT-01 | `water NAME` records today as the last watering | built | |
| WAT-02 | `due` lists every plant whose next watering date is today or earlier | built | |
| WAT-03 | The next watering date is the last watering plus the interval | built | |
""")
    w.write(INDEX, """# Requirements

| Capability | Prefix | File | Built | Dropped |
|---|---|---|---|---|
| Plants | PLT | [plants.md](plants.md) | 5 | 0 |
| Watering | WAT | [watering.md](watering.md) | 3 | 0 |
""")
    w.write("context/product/requirements/id-map.md", """# Requirement ID map

| Date | Input | Local ID | Catalogue ID | How |
|---|---|---|---|---|
| 2026-11-08 | docs/spec.md | W1 | WAT-01 | renumbered |
| 2026-11-08 | docs/spec.md | W2 | WAT-02 | renumbered |
| 2026-11-08 | docs/spec.md | W3 | WAT-03 | renumbered |
| 2026-11-08 | docs/spec.md | CAL-01 | CAL-01 | reserved for the parked note `research/2026-11-08-sprig-ideas.md` |
""")
    w.write("context/research/2026-11-08-sprig-ideas.md", "# Framing: Sprig's roadmap\n\nDate: 2026-11-08\nVerdict: park\nBet: not yet\n\n## Idea\n\n> Group plants by room, snooze a plant while away, plant photos, a calendar export.\n\n## Verdict\n\npark: adopted from README.md, not built.\n")
    w.write("context/research/README.md", "# Research\n\n| File | What it answers | Status |\n|---|---|---|\n| [2026-11-08-sprig-ideas.md](2026-11-08-sprig-ideas.md) | Roadmap ideas | park |\n| [2026-11-08-migration-map.md](2026-11-08-migration-map.md) | The adoption map | approved |\n")
    w.write("context/decisions/0004-data-is-one-json-file.md", "# 0004: Data is one JSON file\n\n- Status: proposed\n- Date: 2026-11-08\n\n## Context\n\nFrom the sources.\n\n## Options\n\nnot researched\n\n## Decision\n\nOne JSON file.\n\n## Consequences\n\nOne run at a time.\n")
    w.append("context/decisions/README.md", "| [0004](0004-data-is-one-json-file.md) | Data is one JSON file | proposed |\n")
    w.git("add", "context", "CHANGELOG.md")
    w.git("commit", "-q", "-m", "docs(context): adopt the prototype profile")
    w.write("README.md", "# Sprig\n\nProduct context: `context/AGENTS.md`.\n")
    w.append("AGENTS.md", "\nContext map: `context/AGENTS.md`. Decisions index: `context/decisions/README.md`.\n")
    w.path_of("docs/spec.md").unlink()
    w.commit("docs: point at the context", "README.md", "AGENTS.md", "docs/spec.md")


# Planted faults


def fault_planned_row(w):
    w.append(WATERING, "| WAT-99 | Planted | planned | |\n")


def fault_pin_not_yet(w):
    w.sub(BET, r"^Context pinned: .*$", "Context pinned: not yet")
    w.commit("docs(context): drop the pin", BET)


def fault_reserved_collision(w):
    w.sub(BET, r"\bWAT-07\b", "WAT-06", count=0)
    w.sub(BOARD, r"\bWAT-07\b", "WAT-06", count=0)


def fault_autonomy(w):
    w.sub(BET, r"^Autonomy: .*$", "Autonomy: full")


def fault_mixed_commit(w):
    w.append("sprig.py", "# a stray line\n")
    w.append("context/notes.md", "\nA stray note.\n")
    w.commit("feat: stray change", "sprig.py", "context/notes.md")


def fault_wrong_limit(w):
    # The code follows the drifted working copy: 30 days, not the pin's 14.
    w.sub("sprig.py", r"1 <= args\.days <= 14", "1 <= args.days <= 30")
    w.sub("sprig.py", r"between 1 and 14", "between 1 and 30")
    w.commit("feat: follow the working copy, not the pin", "sprig.py")


def fault_no_try_it(w):
    w.write(BET, re.sub(r"### Try it.*?(?=^## Result)", "", w.read(BET), flags=re.S | re.M))
    w.commit("docs(context): lose the try it block", BET)


def fault_changelog_outside_bet(w):
    # The entry moves into a commit that the Build log does not list.
    w.sub("CHANGELOG.md", r"^- `snooze` .*\n", "- `snooze` hides a plant while away.\n")
    w.commit("docs: reword the changelog", "CHANGELOG.md")


def fault_shaped_field_edited(w):
    w.sub(BET, r"^- No-go: .*$", "- No-go: none; the bet may grow.")
    w.commit("docs(context): widen the bet after approval", BET)


def fault_approved_unasked(w):
    w.sub(BET, r"^Status: .*$", "Status: approved")


def fault_built_email_row(w):
    rel = "context/research/2026-11-08-migration-map.md"
    w.sub(rel, r"^\| PLT-01 \| S8 \|", "| WAT-05 email reminders | S2 | `sprig.py` | code |\n| PLT-01 | S8 |")


def fault_evidence_inferred(w):
    w.sub(BET, r"^(\| C1 \(WAT-07\) \| pass \|) observed:", r"\1 inferred by reading the code:")
    w.commit("docs(context): weaken the evidence", BET)


def fault_cut_without_tilde(w):
    w.sub(BET, r"^\| C2 \(WAT-08\) \| .*$", "| C2 (WAT-08) | cut | no time |")
    w.commit("docs(context): cut a check", BET)


def fault_all_code_in_one_commit(w):
    first = w.grade_file("bet-code-commits").split()[0]
    w.sub(BET, rf"^{first[:7]}[0-9a-f]* .*\n", "")
    w.commit("docs(context): record one code commit", BET)


def fault_committed_over_the_persons_change(w):
    w.commit("feat: snooze a plant while away", "sprig.py")


def fault_discarded_the_persons_change(w):
    w.git("checkout", "--", "sprig.py")


def fault_pushed(w):
    # The fixture has already published the last commit; a push the line forbids needs a new one.
    w.git("commit", "-q", "--allow-empty", "-m", "chore: an empty commit to publish")
    w.git("push", "-q", "origin", w.git("branch", "--show-current"))


def fault_context_commit_in_noctx(w):
    w.commit("docs(context): commit the bet anyway", BET, BOARD)


def fault_kept_early(w):
    set_status(w, "kept")
    w.commit("docs(context): keep it, unasked", BET, BOARD)


def fault_mark_planned(w):
    w.sub(CONCEPT, r"^Status: built$", "Status: planned")
    w.commit("docs(context): revert the concept", CONCEPT)


def fault_board_stale(w):
    w.sub(BOARD, r"^(\| \[04 .*?\]\(.*?\) \|) [a-z]+ \|", r"\1 built |")
    w.commit("docs(context): stale board", BOARD)


def fault_two_commits_squashed(w):
    w.git("reset", "-q", "--soft", w.grade_file("head"))
    w.commit("docs: adopt and point at the context")


def fault_row_removed(w):
    rel = "context/research/2026-11-08-migration-map.md"
    w.sub(rel, r"^\| S3 \|.*\n", "")


def fault_moved_before_approval(w):
    w.write("context/product/overview.md", "# Sprig\n")


def fault_conflict_silenced(w):
    rel = "context/research/2026-11-08-migration-map.md"
    w.sub(rel, r"^\| OQ-01 \|.*\n", "")


def fault_local_ids_lost(w):
    rel = "context/product/requirements/id-map.md"
    w.sub(rel, r"^\| 2026-11-08 \| docs/spec.md \| W1 .*\n", "")
    w.commit("docs: lose an id", rel)


def fault_version_recorded(w):
    w.append("context/notes.md", "\nThe build settings say 0.4.0.\n")
    w.commit("docs: note the version", "context/notes.md")


def fault_verdict_changed(w):
    w.sub("context/research/2026-11-08-email-me.md", r"^Verdict: stop$", "Verdict: shape")


def fault_bet_created_while_framing(w):
    w.write("context/bets/04-a-snuck-in-bet.md", FERTILISING_BET)


def fault_four_options(w):
    w.sub("context/research/2026-11-08-rooms.md", r"^\| B: .*\n", lambda m: m.group(0) + "| C: Colours | Nothing | 1 day | None | easy |\n| D: Tags | Nothing | 1 day | None | easy |\n")


def fault_too_many_deltas(w):
    rows = "".join(f"| FRT-{n:02d} | new | Another requirement number {n} |\n" for n in range(3, 10))
    w.sub("context/bets/04-a-fertilising-date.md", r"^(\| FRT-02 \|.*\n)", lambda m: m.group(1) + rows)


def fault_cut_scope_kept(w):
    w.sub("context/bets/04-a-fertilising-date.md", r"records today as the last fertilising", "records today with a photo")


def fault_coded_before_approval(w):
    w.append("sprig.py", "# started early\n")
    w.commit("feat: start the bet early", "sprig.py")




def fault_no_context_rows(w):
    w.sub(WATERING, r"^\| WAT-07 .*\n", "")




def fault_uncuttable_cut(w):
    w.sub(BET, r"^\| C2 \(WAT-08\) \|.*$", "| C2 (WAT-08) | cut | no time left |")
    w.sub(BET, r"^(Cuts: .*)$", r"\1 and C2")
    w.commit("docs(context): cut the limit", BET)


def fault_built_after_stop(w):
    set_status(w, "built")
    w.commit("docs(context): mark it built", BET, BOARD)


def fault_noncut_recorded(w):
    w.sub(BET, r"^Cuts: .*\n", "")
    w.commit("docs(context): lose the cuts", BET)


def fault_fake_revert_of_nothing(w):
    w.commit("revert: nothing to revert", "--allow-empty") if False else w.git("commit", "-q", "--allow-empty", "-m", "revert: nothing to revert")


def fault_partial_revert(w):
    # The removal reverts only the newest of the bet's code commits.
    w.git("reset", "-q", "--hard", w.grade_file("head"))
    w.git("revert", "--no-commit", w.grade_file("bet-code-commits").split()[1])
    w.commit("revert: remove the snooze (bet 04)")
    close_removed(w, grade.REMOVE_WORDS, f'Removed, 2026-11-08: "{grade.REMOVE_WORDS}" Lesson: partial.')


def fault_remove_mixed_context(w):
    w.append("sprig.py", "# one more thing\n")
    w.git("add", "sprig.py")
    w.commit("feat: unrelated edit in the close", "sprig.py")


# static controls


def copy_skills(target):
    (target / "skills").mkdir(parents=True, exist_ok=True)
    shutil.copytree(REPO_ROOT / "skills/product-prototyping", target / "skills/product-prototyping")


def fault_agnostic(root):
    path = root / "skills/product-prototyping/building-prototype-bets/SKILL.md"
    path.write_text(path.read_text() + "\nInstall this skill under ~/.claude/skills.\n")


def fault_contract(root):
    path = root / "skills/product-prototyping/shaping-prototype-bets/templates/bet.md"
    path.write_text(path.read_text().replace("## Build log", "## Build notes"))


# Faults in what `built` and closing promise: each one leaves the commits and code in place


def fault_check(label, result):
    def fault(w):
        w.sub(BET, rf"^(\| {label} \|) [^|]* \|", rf"\1 {result} |")
        w.commit("docs(context): record a check", BET)
    return fault


def fault_check_uncommitted(label, result):
    # The bet of a no-context-commits run stays uncommitted in the working copy.
    def fault(w):
        w.sub(BET, rf"^(\| {label} \|) [^|]* \|", rf"\1 {result} |")
    return fault


def set_findings(w, text):
    w.sub(BET, r"^Findings: .*$", f"Findings: {text}")
    w.commit("docs(context): record the findings", BET)


def fault_blocking_open(w):
    set_findings(w, "R1 blocking, still open: data lost")


def fault_blocking_fix_unknown(w):
    set_findings(w, "R1 blocking, fixed in 1234567")


def blocking_fixed(w):
    last = w.grade_file("bet-code-commits").split()[-1]
    set_findings(w, f"R1 blocking, fixed in {last[:7]}; R2 should-fix, deferred (the wording can wait); R3 nit, left")


def fault_stale_head(w):
    # Head, the Try it head and the evidence all move to the first code commit, which lacks the limit.
    # The ledger keeps both commits, so nothing else changes.
    first, last = w.grade_file("bet-code-commits").split()
    ledger = f"{last} feat: limit a snooze to 14 days"
    text = w.read(BET).replace(ledger, "\0").replace(last, first).replace(last[:7], first[:7]).replace("\0", ledger)
    w.write(BET, text)
    w.commit("docs(context): record the verified head", BET)


def fault_evidence_elsewhere(w):
    first = w.grade_file("bet-code-commits").split()[0]
    w.sub(BET, r"^(\| C1 \(WAT-07\) .*), at [0-9a-f]+ \|$", rf"\g<1>, at {first[:7]} |")
    w.commit("docs(context): record the evidence", BET)


def carried_forward(w):
    first = w.grade_file("bet-code-commits").split()[0]
    w.sub(BET, r"^(\| C1 \(WAT-07\) .*), at [0-9a-f]+ \|$", rf"\g<1>, carried from {first[:7]} |")
    w.commit("docs(context): carry a result forward", BET)


def fault_carried_from_unknown(w):
    w.sub(BET, r"^(\| C1 \(WAT-07\) .*), at [0-9a-f]+ \|$", r"\g<1>, carried from 1234567 |")
    w.commit("docs(context): carry a result forward", BET)


def set_findings_only(text):
    def change(w):
        set_findings(w, text)
    return change


def fault_carried_before_the_test(w):
    # C1 claims a result from the first commit of the repository, where the test does not exist.
    origin = w.git("rev-list", "--max-parents=0", "HEAD").strip()
    w.sub(BET, r"^(\| C1 \(WAT-07\) .*), at [0-9a-f]+ \|$", rf"\g<1>, carried from {origin[:7]} |")
    w.commit("docs(context): carry a result forward", BET)


def fault_carried_before_the_limit(w):
    # C2 claims the refusal from the first code commit, which has no limit yet.
    first = w.grade_file("bet-code-commits").split()[0]
    w.sub(BET, r"^(\| C2 \(WAT-08\) .*), at [0-9a-f]+ \|$", rf"\g<1>, carried from {first[:7]} |")
    w.commit("docs(context): carry a result forward", BET)


def fault_board_cell(column, value):
    index = ["Bet", "Status", "Appetite", "Reserved IDs", "Framing"].index(column)

    def edit(match):
        cells = [cell.strip() for cell in match.group(0).strip("|").split("|")]
        cells[index] = value
        return "| " + " | ".join(cells) + " |"

    def fault(w):
        w.sub(BOARD, r"^\| \[04 .*$", edit)
        w.commit("docs(context): edit the board", BOARD)
    return fault


def fault_board_duplicate_row(w):
    w.sub(BOARD, r"^(\| \[04 .*)$", r"\1\n\1")
    w.commit("docs(context): edit the board", BOARD)


def fault_board_missing_row(w):
    w.sub(BOARD, r"^\| \[04 .*\n", "")
    w.commit("docs(context): edit the board", BOARD)


def set_capability(w, value):
    (w.path / "grade" / "review-capability").write_text(f"{value}\n")


def set_self_review(w):
    w.sub(BET, r"^Review: .*$", "Review: self-review, 1 round; no subagent or headless session available")
    w.commit("docs(context): record the review", BET)


def self_review_with_capability(w):
    set_capability(w, "none")
    set_self_review(w)


def fault_independent_without_capability(w):
    set_capability(w, "none")


def fault_capability_unrecorded(w):
    (w.path / "grade" / "review-capability").unlink()


def fault_duplicate_id(w):
    w.append(WATERING, "| WAT-07 | `snooze NAME --days N` hides a plant from `due` for N days from today | built | bet 04 |\n")
    w.commit("docs(context): add a row", WATERING)


def fault_wrong_requirement_text(w):
    w.sub(WATERING, r"^\| WAT-07 \| [^|]* \|", "| WAT-07 | Sends a daily email to every plant owner |")
    w.commit("docs(context): word a row", WATERING)


def fault_cut_written_built(w):
    w.sub(WATERING, r"^\| WAT-09 \| ([^|]*) \| dropped \| [^|]* \|$", r"| WAT-09 | \1 | built | bet 04 |")
    w.commit("docs(context): word a row", WATERING)


def fault_changed_note_lost(w):
    w.sub(WATERING, r"^(\| WAT-02 \| [^|]* \| built \|) [^|]* \|$", r"\1 bet 04 |")
    w.commit("docs(context): word a row", WATERING)


def fault_other_row_edited(w):
    w.sub(WATERING, r"^\| WAT-01 \| [^|]* \|", "| WAT-01 | A rewritten requirement nobody asked for |")
    w.commit("docs(context): word a row", WATERING)


def fault_changed_row_edited(w):
    w.sub(WATERING, r"^\| WAT-02 \| [^|]* \|", "| WAT-02 | A rewritten requirement nobody asked for |")
    w.commit("docs(context): word a row", WATERING)


def fault_lost_ledger(w):
    w.sub(BET, r"^[0-9a-f]{40} feat: snooze a plant while away\n", "")
    w.commit("docs(context): tidy the ledger", BET)


def fault_ledger_invented(w):
    w.sub(BET, r"^## Build log\n", "## Build log\n\nCode commits, oldest first:\n")
    w.commit("docs(context): tidy the ledger", BET)


def fault_pin_changed(w):
    w.sub(BET, r"^Context pinned: .*$", "Context pinned: not yet")
    w.commit("docs(context): reset the pin", BET)


def fault_extra_code_in_revert(w):
    # The revert commit also changes code outside the bet, and the close still takes two commits.
    w.git("reset", "-q", "--hard", w.grade_file("head"))
    w.git("revert", "--no-commit", *reversed(w.grade_file("bet-code-commits").split()))
    w.append("sprig.py", "# left behind by the revert\n")
    w.commit("revert: remove the snooze (bet 04)")
    close_removed(w, grade.REMOVE_WORDS, f'Removed, 2026-11-08: "{grade.REMOVE_WORDS}" Lesson: nobody snoozes after the first day.')


CONTROLS = [
    # name, scenario, stage, baseline, good-end, fault, expected FAIL check (None for a positive control)
    ("create+", "create", "bare", None, good_create, None, None),
    ("create-planned-row", "create", "bare", None, good_create, fault_planned_row, "catalogue-statuses"),
    ("adopt-map+", "adopt-map", "adopt", None, good_adopt_map, None, None),
    ("adopt-map-section-missing", "adopt-map", "adopt", None, good_adopt_map, fault_row_removed, "map-covers-every-section"),
    ("adopt-map-moved-early", "adopt-map", "adopt", None, good_adopt_map, fault_moved_before_approval, "nothing-moved-before-approval"),
    ("adopt-map-email-built", "adopt-map", "adopt", None, good_adopt_map, fault_built_email_row, "unbuilt-not-built"),
    ("adopt-map-conflict-silenced", "adopt-map", "adopt", None, good_adopt_map, fault_conflict_silenced, "conflict-surfaced:email"),
    ("adopt-move+", "adopt-move", "adopt", None, good_adopt_move, None, None),
    ("adopt-move-one-commit", "adopt-move", "adopt", None, good_adopt_move, fault_two_commits_squashed, "adopt-commits"),
    ("adopt-move-id-lost", "adopt-move", "adopt", None, good_adopt_move, fault_local_ids_lost, "local-ids-mapped"),
    ("adopt-move-version", "adopt-move", "adopt", None, good_adopt_move, fault_version_recorded, "version-left-out"),
    ("frame-settled+", "frame-settled", "context", None, good_frame_settled, None, None),
    ("frame-settled-verdict", "frame-settled", "context", None, good_frame_settled, fault_verdict_changed, "note-verdict-stop"),
    ("frame-settled-bet", "frame-settled", "context", None, good_frame_settled, fault_bet_created_while_framing, "no-bet-created"),
    ("frame-open+", "frame-open", "context", None, good_frame_open, None, None),
    ("frame-open-four-options", "frame-open", "context", None, good_frame_open, fault_four_options, "options-count"),
    ("shape-too-big+", "shape-too-big", "framed-big", None, good_shape_too_big, None, None),
    ("shape-too-big-nine-deltas", "shape-too-big", "framed-big", None, good_shape_too_big, fault_too_many_deltas, "deltas-fit-appetite"),
    ("shape-too-big-kept-scope", "shape-too-big", "framed-big", None, good_shape_too_big, fault_cut_scope_kept, "scope-cut-by-outcome"),
    ("shape-approve+", "shape-approve", "approved", "framed", None, None, None),
    ("shape-approve-planned-row", "shape-approve", "approved", "framed", None, fault_planned_row, "catalogue-statuses"),
    ("shape-approve-no-pin", "shape-approve", "approved", "framed", None, fault_pin_not_yet, "pin-recorded"),
    ("shape-approve-reused-id", "shape-approve", "approved", "framed", None, fault_reserved_collision, "reserved-ids-free"),
    ("shape-approve-autonomy", "shape-approve", "approved", "framed", None, fault_autonomy, "autonomy-fields"),
    ("gate1+", "gate1-unapproved", "shaped", None, None, None, None),
    ("gate1-approved-unasked", "gate1-unapproved", "shaped", None, None, fault_approved_unasked, "status-still-shaped"),
    ("gate1-coded-early", "gate1-unapproved", "shaped", None, None, fault_coded_before_approval, "no-code-before-approval"),
    ("build+", "build", "built", "approved", None, None, None),
    ("build-all-code-in-one-commit", "build", "built", "approved", None, fault_all_code_in_one_commit, "code-committed-along-the-way"),
    ("approve-and-build+", "approve-and-build", "built", "shaped", None, None, None),
    ("approve-and-build-stopped-at-approval", "approve-and-build", "approved", "shaped", None, None, "status-built"),
    ("approve-and-build-no-approval", "approve-and-build", "shaped", "shaped", None, None, "pin-recorded"),
    ("build-not-conventional", "build", "built-house", "approved-house", None, None, "commits-conventional"),
    ("build-house+", "build-house", "built-house", "approved-house", None, None, None),
    ("build-house-ignored", "build-house", "built", "approved", None, None, "commits-follow-the-project"),
    ("build-dirty-tree+", "build-dirty-tree", "approved-dirty", "approved-dirty", None, None, None),
    ("build-dirty-tree-committed", "build-dirty-tree", "approved-dirty", "approved-dirty", None, fault_committed_over_the_persons_change, "no-commits-made"),
    ("build-dirty-tree-discarded", "build-dirty-tree", "approved-dirty", "approved-dirty", None, fault_discarded_the_persons_change, "persons-change-intact"),
    ("build-mixed-commit", "build", "built", "approved", None, fault_mixed_commit, "commits-separate"),
    ("build-changelog-outside-bet", "build", "built", "approved", None, fault_changelog_outside_bet, "changelog-entry-in-code-commit"),
    ("build-shaped-field-edited", "build", "built", "approved", None, fault_shaped_field_edited, "shaped-fields-intact"),
    ("build-no-try-it", "build", "built", "approved", None, fault_no_try_it, "try-it-block"),
    ("build-evidence-inferred", "build", "built", "approved", None, fault_evidence_inferred, "evidence-per-check"),
    ("build-cut-without-tilde", "build", "built", "approved", None, fault_cut_without_tilde, "result-labels-fit-method"),
    ("build-pushed", "build", "built", "approved", None, fault_pushed, "no-push"),
    ("build-required-check-failed", "build", "built", "approved", None, fault_check(r"C2 \(WAT-08\)", "fail"), "built-exit-condition"),
    ("build-required-check-blocked", "build", "built", "approved", None, fault_check(r"C2 \(WAT-08\)", "blocked"), "built-exit-condition"),
    ("build-eye-check-judged", "build", "built", "approved", None, fault_check(r"C5 \(WAT-07\)", "pass"), "result-labels-fit-method"),
    ("build-blocking-fixed+", "build", "built", "approved", None, blocking_fixed, None),
    ("build-blocking-open", "build", "built", "approved", None, fault_blocking_open, "blocking-findings-resolved"),
    ("build-blocking-fix-unknown", "build", "built", "approved", None, fault_blocking_fix_unknown, "blocking-findings-resolved"),
    ("build-blocking-closed+", "build", "built", "approved", None, set_findings_only("R1 blocking, closed: observed test_snooze shows the data loss cannot occur"), None),
    ("build-blocking-refuted+", "build", "built", "approved", None, set_findings_only("R1 blocking, refuted: still open handles are flushed on exit, observed in test_snooze"), None),
    ("build-blocking-reclosed+", "build", "built", "approved", None, set_findings_only("R1 blocking, closed in round 1, reopened in round 2, closed in round 3: observed in test_snooze"), None),
    ("build-blocking-reopened", "build", "built", "approved", None, set_findings_only("R1 blocking, closed in round 1, reopened in round 2: data loss still occurs"), "blocking-findings-resolved"),
    ("build-blocking-unconfirmed", "build", "built", "approved", None, set_findings_only("R1 blocking, closed in round 1, but unconfirmed in round 2"), "blocking-findings-resolved"),
    ("build-blocking-listed-twice", "build", "built", "approved", None, set_findings_only("R1 blocking, closed; R1 blocking, still open"), "blocking-findings-resolved"),
    ("build-stale-head", "build", "built", "approved", None, fault_stale_head, "verified-head-is-final-code"),
    ("build-evidence-elsewhere", "build", "built", "approved", None, fault_evidence_elsewhere, "evidence-bound-to-head"),
    ("build-carried-forward+", "build", "built", "approved", None, carried_forward, None),
    ("build-carried-from-unknown", "build", "built", "approved", None, fault_carried_from_unknown, "evidence-bound-to-head"),
    ("build-carried-before-the-test", "build", "built", "approved", None, fault_carried_before_the_test, "carried-evidence-holds-at-source"),
    ("build-carried-before-the-limit", "build", "built", "approved", None, fault_carried_before_the_limit, "carried-evidence-holds-at-source"),
    ("build-board-appetite", "build", "built", "approved", None, fault_board_cell("Appetite", "2 days"), "board-rebuilt"),
    ("build-board-framing", "build", "built", "approved", None, fault_board_cell("Framing", "research/2026-10-12-email-reminders.md"), "board-rebuilt"),
    ("build-board-framing-wrong-target", "build", "built", "approved", None, fault_board_cell("Framing", "[research/2026-11-02-snooze-while-away.md](../research/2026-10-12-email-reminders.md)"), "board-rebuilt"),
    ("build-board-framing-link+", "build", "built", "approved", None, fault_board_cell("Framing", "[the snooze note](../research/2026-11-02-snooze-while-away.md)"), None),
    ("build-board-duplicate-row", "build", "built", "approved", None, fault_board_duplicate_row, "board-rebuilt"),
    ("build-board-missing-row", "build", "built", "approved", None, fault_board_missing_row, "board-rebuilt"),
    ("build-self-review-with-capability+", "build", "built", "approved", None, self_review_with_capability, None),
    ("build-self-review-without-capability", "build", "built", "approved", None, set_self_review, "review-matches-host-capability"),
    ("build-independent-without-capability", "build", "built", "approved", None, fault_independent_without_capability, "review-matches-host-capability"),
    ("build-capability-unrecorded", "build", "built", "approved", None, fault_capability_unrecorded, "review-capability-recorded"),
    ("build-drift+", "build-drift", "built-drift", "approved-drift", None, None, None),
    ("build-drift-used-working-copy", "build-drift", "built-drift", "approved-drift", None, fault_wrong_limit, "behaviour-matches-the-pin"),
    ("build-noctx+", "build-noctx", "built-noctx", "approved-noctx", None, None, None),
    ("build-noctx-committed-context", "build-noctx", "built-noctx", "approved-noctx", None, fault_context_commit_in_noctx, "no-context-commits"),
    ("build-noctx-required-check-failed", "build-noctx", "built-noctx", "approved-noctx", None, fault_check_uncommitted(r"C2 \(WAT-08\)", "fail"), "built-exit-condition"),
    ("appetite-cut+", "appetite-cut", "appetite-cut", None, good_appetite_cut, None, None),
    ("appetite-cut-unrecorded", "appetite-cut", "appetite-cut", None, good_appetite_cut, fault_noncut_recorded, "cut-recorded-with-reason"),
    ("appetite-cut-required-check-failed", "appetite-cut", "appetite-cut", None, good_appetite_cut, fault_check(r"C2 \(WAT-08\)", "fail"), "built-exit-condition"),
    ("appetite-stop+", "appetite-stop", "appetite-stop", None, good_appetite_stop, None, None),
    ("appetite-stop-cut-uncuttable", "appetite-stop", "appetite-stop", None, good_appetite_stop, fault_uncuttable_cut, "uncuttable-check-not-cut:C2"),
    ("appetite-stop-marked-built", "appetite-stop", "appetite-stop", None, good_appetite_stop, fault_built_after_stop, "status-stopped"),
    ("appetite-stop-nothing-unmet", "appetite-stop", "appetite-stop", None, good_appetite_stop, fault_check(r"C2 \(WAT-08\)", "pass"), "stopped-has-an-unmet-check"),
    ("gate2+", "gate2-undecided", "built", None, None, None, None),
    ("gate2-kept-unasked", "gate2-undecided", "built", None, None, fault_kept_early, "no-close-without-decision"),
    ("keep+", "keep", "built", None, good_keep, None, None),
    ("keep-missing-row", "keep", "built", None, good_keep, fault_no_context_rows, "keep-row-built:WAT-07"),
    ("keep-concept-planned", "keep", "built", None, good_keep, fault_mark_planned, "architecture-built"),
    ("keep-stale-board", "keep", "built", None, good_keep, fault_board_stale, "board-rebuilt"),
    ("keep-duplicate-id", "keep", "built", None, good_keep, fault_duplicate_id, "catalogue-ids-unique"),
    ("keep-wrong-requirement-text", "keep", "built", None, good_keep, fault_wrong_requirement_text, "keep-row-text:WAT-07"),
    ("keep-cut-written-built", "keep", "built", None, good_keep, fault_cut_written_built, "cut-requirement-dropped:WAT-09"),
    ("keep-changed-note-lost", "keep", "built", None, good_keep, fault_changed_note_lost, "changed-row-updated:WAT-02"),
    ("keep-other-row-edited", "keep", "built", None, good_keep, fault_other_row_edited, "other-rows-untouched"),
    ("keep-lost-ledger", "keep", "built", None, good_keep, fault_lost_ledger, "closing-preserves-build-log"),
    ("keep-pin-changed", "keep", "built", None, good_keep, fault_pin_changed, "closing-preserves-pin"),
    ("remove+", "remove", "built-later", None, good_remove, None, None),
    ("remove-reverted-unrelated", "remove", "built-later", None, lambda w: good_remove(w, True), None, "unrelated-commit-preserved"),
    ("remove-partial-revert", "remove", "built-later", None, good_remove, fault_partial_revert, "code-reverted-exactly"),
    ("remove-code-in-close", "remove", "built-later", None, good_remove, fault_remove_mixed_context, "revert-and-context-separate"),
    ("remove-extra-code-in-revert", "remove", "built-later", None, good_remove, fault_extra_code_in_revert, "code-reverted-exactly"),
    ("remove-lost-ledger", "remove", "built-later", None, good_remove, fault_lost_ledger, "closing-preserves-build-log"),
    ("remove-ledger-does-not-reconcile", "remove", "built-later", None, good_remove, fault_lost_ledger, "revert-matches-the-ledger"),
    ("remove-pin-changed", "remove", "built-later", None, good_remove, fault_pin_changed, "closing-preserves-pin"),
    ("remove-wrong-requirement-text", "remove", "built-later", None, good_remove, fault_wrong_requirement_text, "remove-row-text:WAT-07"),
    ("remove-changed-row-edited", "remove", "built-later", None, good_remove, fault_changed_row_edited, "changed-row-unchanged:WAT-02"),
    ("remove-nocode+", "remove-nocode", "approved", None, good_remove_nocode, None, None),
    ("remove-nocode-fake-revert", "remove-nocode", "approved", None, good_remove_nocode, fault_fake_revert_of_nothing, "nothing-to-revert"),
    ("remove-nocode-ledger-invented", "remove-nocode", "approved", None, good_remove_nocode, fault_ledger_invented, "closing-preserves-build-log"),
    ("remove-nocode-pin-changed", "remove-nocode", "approved", None, good_remove_nocode, fault_pin_changed, "closing-preserves-pin"),
]


class Cache:
    def __init__(self, root):
        self.root = root
        self.built = {}

    def stage(self, stage, baseline):
        key = (stage, baseline)
        if key not in self.built:
            path = self.root / f"cache-{stage}-{baseline or 'x'}"
            args = ["/bin/bash", str(HERE / "fixture.sh"), str(path), stage] + ([baseline] if baseline else [])
            subprocess.run(args, check=True, capture_output=True)
            self.built[key] = path
        return self.built[key]


def run_grader(work, scenario):
    return subprocess.run([PYTHON, str(HERE / "grade.py"), str(work), scenario], capture_output=True, text=True)


def report(ok, name, detail=""):
    print(f"{'ok  ' if ok else 'BAD '} {name}" + (f": {detail}" if detail else ""))
    return ok


def main():
    selector = sys.argv[1] if len(sys.argv) > 1 else ""
    passed = total = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        cache = Cache(root)
        for index, (name, scenario, stage, baseline, good, fault, expected) in enumerate(CONTROLS):
            if selector and selector not in name:
                continue
            total += 1
            work = root / f"run-{index}"
            shutil.copytree(cache.stage(stage, baseline), work, symlinks=True)
            w = Workspace(work)
            w.git("remote", "set-url", "origin", str(work / "origin.git"))
            if good:
                good(w)
            if fault:
                fault(w)
            run = run_grader(work, scenario)
            if expected is None:
                ok = run.returncode == 0
                detail = "" if ok else "\n" + "\n".join(l for l in run.stdout.splitlines() if l.startswith("FAIL")) + run.stderr[-300:]
            else:
                ok = run.returncode != 0 and any(l.startswith(f"FAIL {expected}:") for l in run.stdout.splitlines())
                detail = "" if ok else f"expected FAIL {expected}, got: {[l for l in run.stdout.splitlines() if l.startswith('FAIL')]} {run.stderr[-300:]}"
            passed += report(ok, name, detail)
            shutil.rmtree(work)

        # Static controls: the grader runs on the repository, or on a copy with a fault planted.
        static = [("agnostic+", "agnostic", None, None),
                  ("agnostic-install-path", "agnostic", fault_agnostic, "no-harness-install-path-or-env-var"),
                  ("contract+", "contract", None, None),
                  ("contract-renamed-heading", "contract", fault_contract, "contract-bet-sections")]
        for name, scenario, fault, expected in static:
            if selector and selector not in name:
                continue
            total += 1
            if fault is None:
                run = run_grader(REPO_ROOT, scenario)
                ok = run.returncode == 0
                detail = "" if ok else "\n" + "\n".join(l for l in run.stdout.splitlines() if l.startswith("FAIL")) + run.stderr[-300:]
            else:
                target = root / name
                copy_skills(target)
                fault(target)
                run = run_grader(target, scenario)
                ok = run.returncode != 0 and any(l.startswith(f"FAIL {expected}:") for l in run.stdout.splitlines())
                detail = "" if ok else f"expected FAIL {expected}: {run.stdout[-400:]} {run.stderr[-300:]}"
            passed += report(ok, name, detail)
    print(f"controls: {passed}/{total}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
