# The build loop

How `building-prototype-bets` runs a bet in detail: where working notes go, how work is handed between agents through files, how a check is proved, how the independent reviewer is run, and what the Build log holds. The bet's fields, statuses and commit rules are in the prototype profile, `references/prototype-profile.md` in this skill.

## Contents

- The working folder
- Briefs and hand-offs
- Proving a check
- Observed and inferred
- The independent reviewer
- Fixing
- Cuts and the clock
- Context commits
- Recording the code commits
- The Build log
- Resuming

## The working folder

Working notes are untracked, so a remove reverts code and nothing else, and drafts never reach the history. Take the folder from the project's instructions. Confirm it is ignored with `git check-ignore -q <folder>`. When none is, use a temporary folder outside the repository, such as one made with `mktemp -d`, and record its absolute path in the Build log so a resumed session finds it. Ask the person only when neither an ignored folder nor a temporary one is usable, and do not edit the ignore file without their agreement. Quill, for example, would use `.work/bet-03/`.

| File | Holds |
|---|---|
| `LOG.md` | One timestamped line per event, newest last: start, step planned, check run, commit, review round, cut, wait for the person, stop. Each line says what happened and where (a file, a commit SHA) |
| `bet-at-pin.md` | The bet as `git show` printed it at the pinned commit. Briefs and the reviewer read this copy |
| `steps/NN-brief.md` and `steps/NN-return.md` | A delegated step's brief and what the worker returned |
| `evidence/` | Command output and observations, one file per check and commit, named `C2-<short sha>.txt` |
| `review/round-N-brief.md` and `review/round-N-findings.md` | The reviewer's brief and the findings file it wrote |

`LOG.md` is the clock and the memory: appetite is measured from its timestamps, and a session that ends can be resumed from it. Record a wait for the person as `wait start` and `wait end`, so the appetite does not charge for it.

## Briefs and hand-offs

Hand work between agents through files, never through the conversation. A worker or reviewer starts with an empty context, so the file has to carry everything it needs, and the file stays as a record of what it was asked.

A step brief holds: the goal in one sentence; the parts of the bet it serves (outcome, the checks it targets, the boundaries that apply), copied from `bet-at-pin.md`; the files it may change and the files it must leave alone; the commands to run and the result that counts as done; what to return (changed files, commands run with their results, anything it could not do). Name one owner for each shared file (a lockfile, a schema, a fixture). When the harness has subagents and the steps touch disjoint files, run them in parallel; otherwise run them in turn. Workers edit and run targeted checks; the builder integrates one finished step at a time, runs the checks again on the combined result, and commits that step before integrating the next, because isolated green is not combined green and steps batched into one commit cannot be tied to their evidence or reverted apart. Write the briefs with `improving-prompts` when it is installed.

## Proving a check

Each check names its Method; the proof is the method's own, run on the commit you made. This section holds the proof rules; `SKILL.md` only points here. Record each check as `pass`, `fail`, `blocked` or `cut`.

- **Baseline first.** Before the first change, run the targeted tests, the build and the linters once. A failure that was already there is reported as such and never counted as a regression or hidden.
- **Tie evidence to a commit.** Every result in the Build log belongs to a commit. A later commit makes evidence stale for any check whose code path, dependencies or data the new diff touches (`git diff --stat <old>..<new>`). Run those checks again; carry forward only what the diff cannot affect, and mark it `carried from <short sha>`.
- **`test`.** Name the test, run it, and read the summary: passed, failed, skipped. A run that selected zero tests, or skipped the tests you added, is `blocked`, not `pass`. For a behaviour that matters (data loss, persistence, anything the person would lose work to), ask whether a plausible wrong implementation would still pass; break the behaviour in a scratch copy, confirm the test fails for the right reason, and discard the copy.
- **`build`.** Run the project's build from a clean state when it is cheap; quote the exit status and the lines that matter.
- **`run and observe`.** Start the app yourself from this checkout, in the background, with output to a log file, and record the process ID of everything you start. Poll the readiness signal with a timeout instead of sleeping. Use a local database or file you created for the run; never production data or accounts. Act as the person would, observe the pass condition, and quote the exact text, count or state. Check the server log and the console for errors during the flow. When the check is about persistence, reload or restart and look again. Stop what you started, and leave what you did not start running.
- **`inspect output`.** Produce the output (a file, a report, a response) and quote the lines or fields the check names.
- **`person's eye`.** It is the person's judgement, and it does not gate `built`. Make it possible: start command, seed data and anything they must click are in the Try it block. A screenshot or an output file may be attached, but it is not a pass.
- **Secrets.** Test for a variable with `test -n "${NAME-}"` and never print its value. Redact tokens and connection strings from anything you quote.
- **Mocks.** Label every mock, stub and fixture, and say what it leaves out.

A check that cannot run is `blocked` with the reason. It does not count as a pass and does not become one by a different check standing in for it.

## Observed and inferred

Mark every line of evidence as one or the other. Observed means you ran it or drove it and saw the result. Inferred means you read the code or a test and concluded the result. Only observed evidence passes a check. An inferred line may support a finding or explain a result, and the Build log says which it is, so the person and the reviewer know how much of the build was seen working.

## The independent reviewer

The reviewer's job is to compare the result with the bet's intent, which the builder is worst placed to do. A cut that the bet at its pin marks `~` is a decision the bet allowed, so the reviewer checks that the cut was allowed and does not report the missing implementation or evidence behind it. It works in a fresh context, preferably on a different model from the builder's, and from files only. Use a subagent when the harness has them, or a separate headless agent session; with neither, review yourself against `bet-at-pin.md` after rereading it and label the round self-review in the Build log.

**Input**, all in the brief (`templates/review-brief.md` in this skill): `bet-at-pin.md`; the Context pack paths at the pin; the diff range, as `git diff <base>..<head> -- . ':(exclude)context'`, which holds the code and the app's changelog and leaves the context folder out, so a context commit between the code commits cannot show the reviewer the Build log; the cuts made so far, each with its check, requirement and reason; the evidence directory; the repository path; the round number. After a repair, the brief also carries the person's request, and the diff still runs from the base. Hold back the builder's reasoning, `LOG.md` and earlier reviews until the reviewer has written its own findings; they anchor it to the builder's framing.

**Output**: one findings file, `review/round-N-findings.md`. Each finding has an ID (`R1`, `R2`, … stable across rounds), a severity (`blocking`, `should-fix`, `nit`), a status (`confirmed` or `unconfirmed`), the file and line at the head, a one-sentence summary, the trigger, the impact, the evidence, the basis (the check, the outcome sentence or the no-go it touches) and a direction. The reviewer starts with a matrix, one line per check: where it is implemented, what exercises it, the result recorded. It answers `no findings` only with a line saying what it examined.

**Rounds.**

1. Round 1 is a fresh session on the head after the iteration's checks pass.
2. After the fixes, the follow-up pass runs in the same reviewer session when the harness lets you continue it. The reviewer rechecks each earlier finding at the new head, reporting `closed`, `still open` or `reopened` with evidence, and reviews the delta. When the session cannot be continued, send the same brief with the findings to recheck.
3. A later pass is a fresh session, given all earlier findings with their status, so a long conversation does not wear its judgement down.
4. A blocking finding still open after round 3 goes to the person with both positions.

The reviewer reads and runs checks; it never edits the code or the bet, commits or pushes. Fixes go through the builder. A reviewer asked to find problems tends to report some, so an empty review is a valid answer.

## Fixing

Confirm each finding before touching code: read the cited lines and run a check or the trigger. A finding the evidence refutes is closed with that evidence written beside it; one nothing settles stays `unconfirmed` and is recorded as a question. For a confirmed finding, add a check that fails without the fix, make the smallest change, commit with the finding ID (a trailer such as `Refs: R2`), and name the checks the fix may have made stale. Never delete a meaningful test, weaken an assertion or reword a check to pass a finding.

Two failed attempts at the same failure with no new evidence mean change the approach: a new hypothesis, a smaller reproduction, a stronger model. A third attempt the same way is a stop.

## Cuts and the clock

The clock runs from the first `Started` line of the Build log, read through `LOG.md`, and it covers the bet's whole life: after a reshape, a stop or a repair, the working time already used stays used, and the approved appetite is the total ceiling. The Build log records the working time used at every stop and finish, so a lost working folder does not lose it. An appetite the person raises is a new total in their words, written in the Build log as a dated line with those words; it is never time added on top. A cut is a decision recorded at the moment it is made, with the reason, so the person at Gate 2 sees what was traded for the time. Cut `~ Cuttable` scope and the `~` checks that prove it before any other `~` check, in the order the Boundaries list them. Name the requirement beside each cut. On keep, a new requirement whose every check is cut is written `dropped` with `bet NN: cut, <reason>`, a changed one keeps its old text, and one whose checks are partly cut is narrowed to what was built.

## Context commits

The bet file and the board change together whenever building changes the bet's Status, at the start, a stop, a finish and a repair. The board is rebuilt from the bet files' header lines and Requirement deltas, in the layout it already has. Before any context commit, run `git diff --cached --name-only`: when anything is staged outside the bet file and the board, stop and tell the person, because those changes are not yours. Stage the two paths by name, read `git diff --cached` to see that it holds only the status, Build log and board changes, and then commit. When the autonomy line says `context commits: no`, leave the changes uncommitted and say so.

## Recording the code commits

Commit each step when its targeted checks pass and before you plan the next, so the code commits accumulate as the work does. Before the first code commit of a bet, run `git rev-parse HEAD` and record it as the base. A continuation or a repair keeps that base, so the review diff still holds every code commit the bet owns. After each code commit, append its short SHA and subject to `LOG.md`. At the end, the Build log lists every code commit by SHA, oldest first, never a range, and a continuation appends to the earlier list instead of replacing it. A context commit that sits between them is named as such, so that closing reverts exactly the code. Commits that touched only `context/` are never listed as code commits.

## The Build log

`Head` is the commit that every result below was verified at; closing compares it with the branch head. The Build log in the bet file is short, so the bet stays readable in one sitting, and it ends with the Try it block, the one note that must outlive the working folder; long output stays in the working folder, which may not survive. Write it in this layout:

```
## Build log

Started: YYYY-MM-DD HH:MM · Finished: YYYY-MM-DD HH:MM · Base: <sha> · Head: <sha> · Branch: <name>
Approved YYYY-MM-DD at <sha>: <autonomy line as approved>      one line per approval, oldest first
Appetite raised YYYY-MM-DD to <total>: "<the person's words>"   only when the person raised it
Working time used: <hours and minutes>, waits excluded, as of YYYY-MM-DD HH:MM
Working folder: <absolute path>, when it is not the project's ignored folder
Repair requested YYYY-MM-DD: "<the person's words>"             one line per repair
Code commits, oldest first: <sha> <subject>, one per line; a context commit between them as `context: <sha> <subject>`
Review: <how it ran: independent in a fresh context | self-review>, <N> rounds

| Check | Result | Evidence |
|---|---|---|
| C1 (STK-03) | pass | observed: `npm test streaks`, 14 passed, 0 skipped, at <short sha> |
| ~ C2 (STK-03) | cut | out of appetite at 1 day; the requirement keeps C1 |
| C3 (STK-04) | person's eye | listed in the Try it block |

Findings: R1 blocking, fixed in <sha>; R2 should-fix, deferred (reason); R3 nit, left
Cuts: <what, and why>
Decisions taken: <choices inside the bet that closing should record, with the reason>
Open: <what is left, for a stopped bet>

### Try it
<the block from templates/try-it.md, written at the end state>
```

## Resuming

A session that ends mid-bet leaves the Build log, `LOG.md` and the commits. Read Status and the Build log from the latest bet file, `LOG.md`, and `git log <base>..HEAD`. Where they disagree the commits are the truth: continue from the first step the commits do not show as done. If the working folder is gone, rebuild what you can from the Build log and the history, take the working time from the Build log's last working-time line, mark the time since as unknown in the Build log, and tell the person, so the appetite is judged by them and not guessed.

A bet that comes back `approved` with a Build log, or `built` with a repair request, continues the same way: its base, ledger and working time used carry on, and only the pin or the request is new.
