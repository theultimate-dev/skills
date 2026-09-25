# Review-recall trial

Measures what `reviewing-code-changes` finds. In full mode it measures recall for each lens and counts false positives (scenario 7 of the [scenario catalog](../evaluation-scenarios.md)). In quick mode it checks that an unimplemented acceptance criterion is caught before the PR opens (scenario 6).

[`seeded.patch`](seeded.patch) turns a copy of the [fixture](../fixture/) into one small-change PR slice, "Records overview": a spec with six acceptance criteria, three new endpoints, and five tests that pass. It plants exactly one defect per lens: security, efficiency, conventions, architecture and intent. [`answer-key.md`](answer-key.md) lists them with their locations, expected severities and observed evidence, and gives the scoring rules.

Keep this directory away from the reviewing agent. It sees only the patched repository and the PR description below.

## Set up

Run this for every trial, so each one starts from a fresh copy:

```bash
EVAL=/absolute/path/to/skills/evaluations/product-engineering
WORK=$(mktemp -d)
cp -R "$EVAL/fixture" "$WORK/repo" && cd "$WORK/repo" && rm -rf __pycache__
git init -q -b main && echo '__pycache__/' >> .git/info/exclude
git add -A && git commit -qm "chore: fixture baseline"
git switch -qc feat/records-overview
patch -p1 -i "$EVAL/review-recall/seeded.patch"
git add -A && git commit -qm "feat: added records overview"
python3 -m unittest discover -p 'test_*.py'    # 5 tests pass
git rev-parse HEAD                              # the head SHA for the PR description
```

Set `user.name` and `user.email` first when the machine has no git identity. Start the reviewing agent with `$WORK/repo` as its working directory and the skills installed. There is no remote, so the full review is written to `review.md` in the work-item folder instead of being posted. The loop did not write this code, and `reviewing-code-changes` runs nothing from the head of a PR the loop did not open until the user agrees. Both prompts below give that agreement for local runs, so a finding can be confirmed by running a check as well as by reading.

## Run

Full mode:

```text
Use reviewing-code-changes in full mode on the branch feat/records-overview
against main. There is no pull request and no remote: treat the text below as
the PR description. You may run the tests and start the app locally in this
workspace, with temporary data. Write the review to review.md in the work-item
folder and change no other file.

<the PR description below, with <HEAD_SHA> replaced>
```

Quick mode:

```text
Use reviewing-code-changes in quick mode on the branch feat/records-overview
against main, before its pull request opens. Its verification report is the
Verification section below. You may run the tests and start the app locally in
this workspace, with temporary data. Return the findings and stop; do not fix
them.

<the PR description below, with <HEAD_SHA> replaced>
```

## PR description to supply

The description is deliberately flawed in the way a hurried implementer's would be: it claims AC1 to AC6, reports five rows, and categorizes the PR as `agent`.

````markdown
## Summary

Adds a records overview. `GET /records` lists the caller's records with the time each was last saved, `GET /records/1/attachments/<name>` serves a record's attached files to its owner, and `GET /records/export` exports the caller's records. Covers R1 to R3 (AC1 to AC6) of `docs/product-engineering/records-overview/spec.md`.

## Verification

Commit: `<HEAD_SHA>` on `feat/records-overview`
Environment: local · Tools: curl, unittest
Contract: AC1 to AC6, agreed at G3
Verified by: the implementing agent
Summary: 5 pass · 0 fail · 0 blocked · 0 blocked (human eye)

| AC | Result | What was done | What was observed |
|---|---|---|---|
| AC1 (R1) | pass | `GET /records` as alice, then as bob, on a fresh data file | alice: `[{"id": "1", "title": "First note", "updated_at": null}]`; bob: `[]` |
| AC2 (R1) | pass | `PUT /records/1` as alice with the title "verify-0925", then `GET /records` | Record 1 shows "verify-0925" and an `updated_at` later than the save request |
| AC3 (R2) | pass | Wrote `attachments/1/notes.txt`, then `GET /records/1/attachments/notes.txt` as alice | 200 and the body `attached notes` |
| AC4 (R2) | pass | The same request as bob | 403 and `{"error": "Record unavailable"}` |
| AC5 (R3) | pass | `GET /records/export` as alice | 200 and an object whose only key is `1` |

### Automated checks

| Command | Result | Summary |
|---|---|---|
| `python3 -m unittest discover -p 'test_*.py' -v` | pass | 5 passed, 0 failed |

## Review category

`agent`: read-only endpoints inside the approved scope; no listed area.
````

## Score

Score each trial against [`answer-key.md`](answer-key.md) and record it in the [evaluation report](../evaluation-report.md). Run at least three full-mode trials, because reviews vary between runs, and report recall per lens across them rather than one run's result.

- **Full mode passes a trial** when the verdict is `REQUEST CHANGES`, in a verdict line that opens the round and names the full head SHA, P1 and P5 are confirmed as `blocking`, the review flags that the PR belongs in the `human` category, and no false positive is reported. Recall for P2 to P4 is reported, not thresholded.
- **Quick mode passes a trial** when P5 is a confirmed `blocking` finding with an AC matrix behind it, no verdict is given, nothing is posted, and no code changes. Other planted defects are optional in quick mode; when reported, they should carry their own lens label.
