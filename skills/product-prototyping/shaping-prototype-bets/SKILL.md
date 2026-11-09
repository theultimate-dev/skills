---
name: shaping-prototype-bets
description: "Shapes one prototype bet from a framed idea: an observable outcome, an appetite of half a day to two days, requirement deltas with reserved permanent IDs, acceptance checks that each name how they are verified, no-gos, rabbit holes, cuttable scope, a keep-or-remove signal, a context pack, and an autonomy line. Checks readiness, gets the person's approval at Gate 1, records the commit the bet was approved at, and starts the build. Also reshapes a stopped bet, or a bet paused for a contract or decision change. Use when the user says shape this, turn this into a bet, size this, is the bet ready, approve bet N, or reshape bet N. Not for planned versions and milestones (shaping-bets)."
license: MIT
---

# Shaping prototype bets

A prototype bet is one try, sized before anyone builds it: an outcome a person can judge, an appetite that is a ceiling (half a day, one day or two), and a plain question at the end, keep it or remove it. This skill turns a framed idea into that bet, checks that it is ready, and gets the person's approval at Gate 1, the first of the category's two gates. It writes the bet file, the board and any planned architecture the bet introduces. It never writes code and never builds.

The profile in [the prototype profile](references/prototype-profile.md) defines the bet's statuses, the IDs, the read rules and where each fact lives. Read it before the first step; this skill uses its names character for character.

## Modes

| The person says | Do |
|---|---|
| Shape this, turn this into a bet, size this | Shape: steps 1 to 7 |
| Is bet N ready | Check readiness only; report, change nothing |
| Approve bet N, go ahead | Check readiness now, then Gate 1 |
| Reshape bet N | [Reshape a stopped or paused bet](#reshape-a-stopped-or-paused-bet) |

## Inputs

- A framing note under `research/` whose Verdict is `shape`, from `framing-prototype-ideas`. It carries the problem, the options, the recommended one and the Remove if line that becomes the Keep or remove signal.
- When the person arrives with an idea and no framing note, say so in one line, recommend `framing-prototype-ideas` first, and continue only on their word. Then write `Framing: none, shaped without a framing note` and ask the questions a note would have answered: the problem, two options and what would make the try worth removing.
- Reading order for shaping, from the profile: the framing note, the requirement files the bet touches, `architecture/contracts/`, `decisions/README.md`, `bets/README.md`, `notes.md`.

## Shape a bet

Read [sizing and readiness](references/sizing-and-readiness.md) before step 3 and [writing a prototype bet](references/writing-a-prototype-bet.md) before step 4.

1. **Read the inputs.** Confirm the framing verdict is `shape`; a `park` or `stop` verdict is the person's call to reopen, not yours. Read the board for bets already open and the next bet number: one past the highest ever used, removed bets included.
2. **Reserve IDs.** For each new requirement, take the next free number in its capability, counting built and dropped rows, reservations on the board, those of removed bets and those recorded in `product/requirements/id-map.md`. A new capability needs a prefix of two to four letters that no file uses. Existing IDs for changed and dropped rows must exist in the catalogue as `built`. A bet that builds a requirement parked at adoption claims its reserved ID instead: the `new` delta keeps that ID and shaping appends a line naming the bet to `id-map.md`; unrelated scope never reuses it. The bet's own reservations stay its own when the bet is checked or reshaped again.
3. **Size the bet.** Pick the appetite from the outcome, never from a wish. An idea that does not fit two days is cut to its thinnest end-to-end outcome or split; the rest waits for its own bet.
4. **Write the bet** from [the bet template](templates/bet.md) with `Status: shaped`, `Autonomy` proposed and `Context pinned: not yet`. Leave Build log and Result empty. Write the Outcome first, then the checks, then the rest; the checks are where a vague idea shows.
5. **Write what the bet introduces.** A contract or concept that other files must reference is written now as `Status: planned`, at its path under `architecture/`, and listed under Introduces. Nothing else reaches `architecture/` until closing. These files, the bet, the board, the `notes.md` rows and the framing note with its research index stay uncommitted until Gate 1, and count as present for readiness. Add a question you could not answer to `notes.md` as an `OQ-` row and cite its ID in the bet.
6. **Check readiness** against the table below. Fix what you can; name the owner of the rest.
7. **Rebuild the board** from [the bet board template](templates/bet-board.md): it is derived from the bet files' header lines and Requirement deltas, so the new bet appears with its reserved IDs.
8. **Link the framing note.** Write the bet's number in the note's `Bet:` line as `Bet: NN (bets/NN-slug.md)`, and update that note's row in `research/README.md`, the derived research index. The note, which `framing-prototype-ideas` leaves uncommitted, is committed whole with the bet at Gate 1. Skip this step when the bet has no framing note.

## Check readiness

| Check | Holds when |
|---|---|
| Requirement deltas | Every reserved ID is free, or is a parked requirement's ID that the bet claims; every changed or dropped ID is a `built` row; every `dropped` delta has a reason |
| Acceptance checks | Every new or changed requirement has a check; each check is observable from outside the code, with concrete values, naming its requirement and one Method; at least one check is not a person's-eye check |
| Person's-eye checks | Listed, each with what the person will look at, so Gate 2 can ask for it |
| Appetite | The checks fit the appetite; cuttable checks and scope carry `~` |
| Boundaries | At least one no-go; every rabbit hole is patched or says what to do if it bites |
| Keep or remove | The signal is something the person can judge after trying the bet; the removal leaves behind only what is listed |
| Architecture | Every consumed contract is `accepted` at the version named; every decision relied on is `accepted`; introduced sections are `planned` |
| Open questions | No open question blocks the bet |
| Context pack | A sufficient pack, in order, each entry with why it earns its place; five to ten is a guide. Every file is committed or a pending shaping artifact that the Gate 1 commit will include |
| Context repository | No path the bet names has an uncommitted change, apart from the pending shaping artifacts: the bet, the board, the planned sections, `notes.md` rows, the framing note and its research index |

[Sizing and readiness](references/sizing-and-readiness.md) says how to check each row. A failed row names what fixes it: a decision through `decision-records`, a design through the `product-design` skills, each when installed; an open question goes to the person. Never make a bet ready by weakening a check or dropping a boundary. A failing row leaves the bet `shaped` with its blockers named; it is not offered for approval.

## Gate 1: the person approves the bet

Offer approval only on a readiness check made now, on the bet as it stands, that passes every row; when anything it reads has changed since the last check, check again before presenting and again before recording an approval. When a row fails, report the blockers and stop with the bet `shaped`. Otherwise present the bet in one message: the outcome, the appetite, the requirement deltas with their reserved IDs, the checks with their methods and which are the person's eye, the boundaries, the keep-or-remove signal, what the bet introduces, the readiness result, and a recommended Autonomy line. Recommend `code commits: <the branch the person works on>; context commits: yes; push: no; revert on remove: yes`, because a removed bet is undone by a revert on that branch, while a bet branch would need a merge to keep, which this loop does not have. The person may change any part of it.

Say in the same message that approval starts the build at once and that it runs without them until there is something to try, stopping only for what only they can decide, so this yes is the last input the build needs. Run `git status --porcelain` and name any change that is not this bet's, because an unrelated change on the branch would stop the build before it starts, and settle it here. When the person chooses `context commits: no`, tell them the build then waits until they commit and pin the bet themselves.

Only explicit approval counts, given after readiness passes: the person says to approve or go ahead. Silence, a question, praise or "looks good, but" does not. A request for changes means revise and present again.

On approval:

1. Set `Status: approved`. Replace Autonomy with the approved line and the person's words, as in [writing a prototype bet](references/writing-a-prototype-bet.md). Rebuild the board.
2. When the approved line says `context commits: yes`, commit the bet, the board, the planned sections, any `notes.md` row, and the whole framing note with the research index in one context commit, with the commit convention the profile's Commits section sets. Before staging, check the index for changes outside those paths and stop on any; after staging, check that the staged diff holds exactly those paths ([sizing and readiness](references/sizing-and-readiness.md) gives the commands). Keep context commits apart from code commits.
3. Check that every Context pack path exists in that commit, then take its full SHA and write it as `Context pinned`. Commit that line alone, with the same index checks: a commit cannot contain its own SHA, and building reads Status, Context pinned, the Build log and the Result from the working copy and everything else at the pin.
4. Start the build. Go straight on to `building-prototype-bets` on this bet in the same session, because the approval was the go-ahead for it. When the person asked to hold it, as in "approve it, but wait", stop here with the bet `approved` and pinned.

When the approved line says `context commits: no`, stop with the bet `approved` and `Context pinned: not yet`; `building-prototype-bets` needs a pin and will say so.

## Reshape a stopped or paused bet

Two things send a started bet here: `building-prototype-bets` sets `stopped` when the appetite runs out with checks left, and it hands a bet back, still `building`, when a contract or an accepted decision it relies on has to change. Read the Build log first: what passed, what was cut, the code commits, the base commit, the working time consumed, where work stopped and why. Keep the actual reason; a paused bet is not an exhausted one.

Offer the person the options and recommend one:

- **Cut to what is left.** Drop or mark `~` the checks and scope that cannot fit, and narrow the Outcome to match.
- **Split.** The bet keeps its number and the part that fits; the rest becomes a new bet with the next free number. Only scope with no implementation moves, with its requirement deltas. Started scope and its commits stay in the original bet, because every code commit belongs to exactly one bet; an implemented part that should move is reverted first.
- **Change the contract or decision.** The person decides. Supersede an accepted decision through `decision-records` (a new record, never an edit), and give a changed contract a new version; these are the changes to files the bet relies on that the open-bet rule allows, with the person's agreement. Then update Architecture and the Context pack.
- **Raise the appetite.** Only in the person's words, as a new total for the whole bet, never time on top of what was spent. Edit the Appetite line.
- **Close as removed.** Hand it to `closing-prototype-bets`.

To reshape:

1. Keep the Build log's history: the code commits, the base commit and the consumed working time. When the bet carries a pin, first append the approval that is about to be replaced as a dated line, `Approved YYYY-MM-DD at <sha>: <the approved Autonomy line>`, so closing can still act under it while the bet is `shaped` again. Once Gate 1 passes again, the new pin's Autonomy line is the authority and the archived line is history.
2. Patch what caused the stop as a rabbit hole in Boundaries, set `Status: shaped` and `Context pinned: not yet`, replace Autonomy with a proposed line, and append one dated line: `Reshaped YYYY-MM-DD: <what changed and why work stopped>; <time consumed> of <appetite> used`, with the person's words when they changed the appetite. Rebuild the board.
3. Check what is left of the appetite. When none is left and the person has not given a new total, do not restart the clock: ask for a new total in their words, or offer to close the bet as removed.
4. Run readiness and Gate 1 again. The new pin replaces the old one, and building continues from the kept commits, ledger and time.

A bet that is `shaped`, `approved` or `stopped` and that the person no longer wants goes to `closing-prototype-bets`. Whether removal reverts anything is decided by the Build log's list of code commits, never by Status: a reshaped bet keeps its commits and its recorded approvals.

## Hand back

Report: the bet written or changed with its path and status, the reserved IDs, the readiness result and what blocks the bet when it is not ready, the planned sections written, the pin when there is one. After an approval that reached a pin, keep this report to a few lines and carry on into the build. Otherwise name the next step: `building-prototype-bets` on bet N, once it is `approved` and pinned. Commit, push and revert only as the person agreed in the current request or the bet's Autonomy line allows.

## When a sibling skill is missing

Name the missing skill in one line, then do only its small essential outcome yourself.

- `framing-prototype-ideas` missing: shape from the person's idea and ask the framing questions in Inputs.
- `decision-records` missing: a relied-on decision that is not `accepted` blocks readiness; name it, never invent one.
- `building-prototype-bets` missing: stop with the bet `approved` and pinned, and tell the person the build has not started.
- `structuring-prototype-context` missing and no `context/` folder: there is nothing to pin the bet to; say so and recommend it.
- No file access: return the bet and the board as complete Markdown, say that nothing was written, and do not report a bet as approved or pinned.

## References

| Read | When |
|---|---|
| [prototype profile](references/prototype-profile.md) | Before the first step: statuses, IDs, read rules, where facts live |
| [writing a prototype bet](references/writing-a-prototype-bet.md) | Step 4, and when reviewing a bet: each section, weak against better, with the Autonomy line |
| [sizing and readiness](references/sizing-and-readiness.md) | Steps 2, 3 and 6, reshaping and Gate 1: appetite, splitting, reserving IDs, how to check each readiness row, pinning |
| [bet template](templates/bet.md) | Writing a bet |
| [bet board template](templates/bet-board.md) | Rebuilding `bets/README.md` |
