---
name: building-prototype-bets
description: "Builds an approved prototype bet in a loop until intent and result match: reads the bet at the commit it was approved at, plans, implements and commits each step as it finishes within the autonomy line, verifies every acceptance check by its named method with quoted evidence, has an independent reviewer in a fresh context compare the result with the bet's intent, fixes, and repeats. Starts as soon as the bet is approved and runs without the person until the result is ready to try, stopping only for what only they can decide. Cuts cuttable scope or stops when the appetite runs out. Adds the changelog entry, fills the bet's Build log and prepares what the person needs to try the result. Use when the user says build bet N, start the bet, continue the bet, repair the built bet, or the bet is approved. Not for a product's planned delivery loop (running-implementation-loops)."
license: MIT
---

# Building prototype bets

Build one approved bet inside its appetite, then hand it to the person to try. The bet says what must be true when you finish: an outcome, acceptance checks that each name how they are proved, boundaries, and an autonomy line. You build until every check that does not need the person's eye passes on the code you committed, and an independent reviewer who has not seen your reasoning agrees that the result matches the bet's intent. The person then tries the build and decides at Gate 2, which belongs to `closing-prototype-bets`. This skill has no gate of its own: Gate 1 already approved the bet, and the autonomy line is the permission you work under.

Read [the prototype profile](references/prototype-profile.md) first for the bet's fields, statuses, the read-at-pin rule and the commit rules. Read [the build loop](references/build-loop.md) before the first step for the working folder, briefs, evidence, the reviewer and the Build log layout.

## Work on your own from approval to hand-back

The person's approval at Gate 1 is their one go-ahead for the whole build, and their direct request for the commits the autonomy line names. Carry the build through to the hand-back in one run, so the person's next touch is trying the result.

- **Decide whatever stays inside the bet and another commit can undo:** names, file layout, the order of steps, how to use what the project already has, how to fix a failure your own change caused. Take the option that best serves the Outcome and write it with its reason under Decisions taken in the Build log, where the person sees it at Gate 2.
- **Keep the record in `LOG.md`,** so the person can look in whenever they like and nothing waits for them.
- **Bring the person only what "Stop and ask" lists.** Everything else has its answer in the bet, the context or the code.

## Where to start

Find the bet's `Status:` line in the latest bet file and act on it.

| Status | Do |
|---|---|
| `approved`, Build log empty | Start: preconditions, then the loop |
| `approved`, Build log not empty | Continuation of a reshaped or extended bet: preconditions, then the loop, keeping the original base, the code commit ledger and the working time already used. Only the pin is new |
| `building` | Resume: read the Build log and the working folder's `LOG.md`, check them against `git log`, continue from the first step not done |
| `shaped` | Not approved yet. Hand it to `shaping-prototype-bets` for Gate 1 |
| `stopped` | The appetite ran out. Build only after the person states a new total in their own words, or the bet is reshaped and approved again; otherwise `closing-prototype-bets` can close it as `removed` |
| `built`, the person asks for an in-scope change | Repair, below |
| `built`, no such request | Nothing to build. Hand it to the person to try, then to `closing-prototype-bets` |
| `kept`, `removed` | Closed. A new idea is a new bet |

## Preconditions

1. **A pin.** `Context pinned:`, read from the working copy, holds a full SHA that exists in the history (`git cat-file -e <sha>`). `not yet` means Gate 1 has not passed: stop.
2. **Read the bet at its pin**, so later edits cannot change what was approved: `git show <sha>:context/bets/NN-slug.md`. Read the shaped fields from that copy and Status, Context pinned, the Build log and the Result from the working copy, reporting any uncommitted state (`git status --short -- context/bets/NN-slug.md`). Then read the Context pack in order, each file at the same pin. When the shaped fields differ between the pin and the working copy, build from the pin and tell the person what differs.
3. **The autonomy line.** Quote it as recorded. Four things come from it: the branch your code commits go on, whether you commit context, whether you push, and whether closing may revert your commits. Anything it does not say you do not do. When it names no branch for code commits, ask before the first one, because every check's evidence is tied to a commit. A continuation works under the autonomy line of its latest approval.
4. **A clean tree.** Run `git status --porcelain`. Changes you did not make stay untouched, and evidence has to come from commits alone, so work in a separate worktree of the named branch when git allows it. When the branch is checked out here, a worktree cannot hold it and only the person can say what happens to their changes: stop and ask before the clock starts.
5. **The working folder.** Working notes go in an untracked folder that the project ignores (`git check-ignore -q <folder>`). Take the name from the project's instructions; when none is ignored, use a temporary folder outside the repository and record its absolute path in the Build log. Ask the person only when neither works, and write nowhere tracked until they answer.
6. **The way to prove things.** Find the commands for tests, build and run in the project's instructions, scripts and CI configuration. Run the targeted checks once before you change anything, so failures that were already there stay distinguishable from yours. When a `run and observe` check has no way to start the app or no tool to drive it, say so now: that check is blocked, and blocked is not a pass.
7. **Start the clock, or keep it.** Run `git rev-parse HEAD` for the base, then set `Status: building` and rebuild the board in the same context change (see "Context commits" in [the build loop](references/build-loop.md)). Make sure the Build log has an approval line for the current pin. A start also records the start time and the base commit and opens `LOG.md`. A continuation keeps the original start, base and commit ledger, and adds the approval line for the new pin: the time already used stays used, and the remaining appetite is the approved total minus it. The appetite counts from the first start.

## The loop

Repeat until the exit condition holds. An iteration is a coherent increment and holds one or more committed steps; a half-day bet may need only two iterations.

1. **Plan the next step.** Pick the smallest increment that moves one or more checks toward passing, riskiest first: a named rabbit hole is worth hitting early, while there is still appetite to patch it. Write the step into `LOG.md` with the checks it targets.
2. **Implement the step, then commit it.** When the harness has subagents, delegate bounded steps with a brief written to a file, drafted with `improving-prompts` when it is installed, and give each worker disjoint files. Otherwise implement inline. Match the project's conventions and look for an existing utility before writing a helper. When a check's method is `test`, write the test first and watch it fail for the right reason. As soon as the step's targeted checks pass, commit it, before you plan the next one, on the branch the autonomy line names, in the project's commit convention, and add its SHA to `LOG.md`. One logical change is one commit, so the history grows as the work does: every result ties to a commit, a resumed session continues from the last one, and a bad step is undone without losing the rest. Keep code and context in separate commits. Stage by path, so uncommitted context changes never enter a code commit. Commit context only when the line says `context commits: yes`, and push only when it says `push: yes`.
3. **Prove each check by its Method**, on the commit you made, as [the build loop](references/build-loop.md) lays out under "Proving a check", and quote what you saw. Record each check as `pass`, `fail`, `blocked` or `cut`, and say which evidence was observed and which only inferred: reading code never makes a check pass. A later commit makes earlier evidence stale for any check the new diff can touch: run it again. A `person's eye` check is not yours to judge; make sure the build lets the person see it and list it for the Try it block.
4. **Review independently** once the iteration's checks have passed, not after every commit. Fill [the review brief](templates/review-brief.md) with the bet at its pin, the diff range, the cuts made so far with their reasons, and the evidence, and run a reviewer in a fresh context with no sight of your reasoning, preferably on a different model. The reviewer writes a findings file; each finding is rated `blocking`, `should-fix` or `nit`. Without subagents, start a separate headless agent session if the harness offers one; with neither, review it yourself against the pinned bet and label the result self-review in the Build log.
5. **Fix.** Confirm each finding by reading the code and running a check, then fix every confirmed `blocking` and `should-fix` finding, or defer a `should-fix` with a reason in the Build log. A `nit` is optional. Refer to the finding's ID in the commit and add a check that fails without the fix. Dispute a finding only with counterevidence, and never weaken a check to get past it. The reviewer's follow-up pass runs in the same session; a later pass runs fresh. When a blocking finding survives the third review round, stop and bring it to the person.

Exit when every check that is not a person's-eye check has passed on the current head, every code change is committed, and the latest review round holds no open `blocking` finding. A cut check does not block the exit, but it is recorded, and the reviewer is told about it.

## The appetite

Appetite is a ceiling for working time over the bet's whole life, never a target and never time added on top by a reshape: a raised appetite is a new total in the person's words, written in the Build log with those words. Take the time used from the Build log's last working-time line plus the timestamps in `LOG.md` since, without the stretches the log records as waiting for the person: those do not count. At half the appetite, compare the work left with the time left; when it cannot fit, cut early, because a late cut saves nothing.

At the limit:

1. Cut the checks marked `~` and the scope named under `~ Cuttable`, in the bet's order, and write each cut with its reason in the Build log. A check without `~` is never cut, however short the time. Name the requirement beside the cut: when every check of a new requirement is cut, closing writes it as `dropped` with `bet NN: cut, <reason>` if the person keeps the bet (a changed one keeps its old text), and when only some are cut, closing narrows its text to what was built.
2. When the remaining checks still do not pass, set `Status: stopped`, rebuild the board, record the working time used and write what is left. Do not carry on past the appetite, and do not extend it yourself: only the person's own words raise it.

## Stop and ask

Once the preconditions hold, stop only when one of these does, because each needs something the bet, the context and the code cannot give you:

- the only way to the Outcome crosses a No-go, or a named rabbit hole survives two attempts that changed the approach between them;
- an accepted decision or a contract the bet relies on has to change: the person decides, and `shaping-prototype-bets` records it;
- a check cannot be observed as written, or two checks contradict each other;
- the build needs what only the person has: a credential, an account, a paid service, or a fact about the product that the context and the code do not settle;
- the next action cannot be undone by a revert, such as deleting data someone relies on or reaching a production system or real users;
- the bet cannot finish without an action beyond the autonomy line. An action it can finish without, such as a push the line does not allow, stays undone and goes in the hand-back;
- something outside the bet breaks, blocks a check, and would need a change the bet does not name. When it blocks nothing, record it under Open and carry on;
- a blocking finding is still open after the third review round.

Commit what already passes, finish any work the answer cannot change, and log `wait start`. Then bring the person the evidence, what you tried and the one decision you need, through the harness's structured-question tool when it has one. When the answer comes, log `wait end` and carry on without being told to.

The status stays `building` in these cases; only an exhausted appetite makes it `stopped`. When the person decides to change a decision or a contract, `shaping-prototype-bets` supersedes or versions it and runs readiness and Gate 1 again; the bet then comes back `approved` with its Build log, and you continue it.

## The changelog

Add the bet's entry under `[Unreleased]` in the app's `CHANGELOG.md`, in a code commit that belongs to the bet, so that reverting the bet takes the entry with it. Write it for users, from the Outcome and not from the commit subjects, under `Added`, `Changed` or `Removed` as the requirement deltas call for. Use `release-process` for the entry when it is installed. When the app has no changelog, create a minimal Keep a Changelog file in the same commit and mention it in the report. Cut a version only when the person asks.

## Finish

When the exit condition holds:

1. Fill the Build log in the bet file, as [the build loop](references/build-loop.md) lays it out: every code commit by SHA, oldest first, with any context commit between them named; the head that every result below was verified at; the working time used; each check's result and evidence; cuts with reasons; review findings and fixes; and decisions you took that closing should record. Set `Status: built` and rebuild the board in the same change. Edit no other part of the bet.
2. Write the Try it block at the end of the Build log, from [the try-it template](templates/try-it.md), at the end state: how to start the build, each `person's eye` check as a step with what to look for, and the keep-or-remove signal. It lives in the bet file, so it survives the working folder. Point the person to it in the report.
3. Commit the bet file and the board as one context commit when the autonomy line says `context commits: yes`; when it says `no`, leave the change uncommitted and say so.

## Repair after trying

The person tried a `built` bet and asks for a change inside its outcome and checks. A change outside them is a new bet, not a repair; ask which they mean when it is unclear.

1. Quote the request in the person's words as a dated line in the Build log, set `Status: building`, and rebuild the board in the same change. The pin, the base, the code commit ledger and the working time used all stay; the repair is built within what remains of the appetite. When nothing remains, only a new total in the person's words continues it.
2. Run the loop with the request as the target: write the failing check first, fix, prove again every check the repair's diff can touch, and brief the reviewer with the request and the full diff from the base.
3. Finish as usual, with the Try it block refreshed for the new head. The bet is `built` again and goes back to Gate 2 in `closing-prototype-bets`.

## Hand back

Report, in this order:

- the bet, its status, and the head commit with the list of code commits;
- each check with `pass`, `fail`, `blocked` or `cut` and one line of evidence;
- the review: how it ran, the rounds, the findings by severity and what became of each;
- the time against the appetite, and any cuts;
- what is left for the person's eye, and the Try it block in the Build log;
- what you did not do because the autonomy line does not cover it.

Next: the person tries the build, then says keep or remove to `closing-prototype-bets`. A `stopped` bet goes to `shaping-prototype-bets` to reshape, or to `closing-prototype-bets` to close as removed.

## When a sibling skill is missing

Name the missing skill in one line, then produce its outcome yourself.

| Missing | Do |
|---|---|
| `improving-prompts` | Write each brief by hand with the goal, the relevant parts of the bet, the files the worker owns, the commands, what done means and the format to return |
| `release-process` | Write the entry by hand in Keep a Changelog form under `[Unreleased]` |
| `closing-prototype-bets` | Gate 2 stays with the person: give them the Build log, whose Try it block says what to do, change nothing beyond `built`, and do not close the bet |
| `shaping-prototype-bets` | A stopped or contradicted bet goes back to the person with the evidence and the options: cut, extend in their words, reshape by hand, or remove |

Without file or shell access, return the plan and the patch as text labelled unexecuted, and report no check as passed.

## References

| Read | When |
|---|---|
| [prototype profile](references/prototype-profile.md) | Before the first step: the bet's fields, statuses, read-at-pin rule, changelog and commit rules |
| [build loop](references/build-loop.md) | Setting up the working folder, writing briefs, proving a check, running the reviewer, committing context, keeping the Build log, resuming |
| [review brief](templates/review-brief.md) | Briefing the independent reviewer |
| [try-it block](templates/try-it.md) | Writing the Try it block of the Build log, what the person does at Gate 2 |
