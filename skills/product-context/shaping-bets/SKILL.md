---
name: shaping-bets
description: "Shapes a milestone of a product context repository into bets: epic-sized, appetite-bounded work units with an observable outcome, the requirement IDs they cover, acceptance criteria, no-gos, rabbit holes, cuttable scope, the contracts and decisions they rely on, and an ordered context pack. Checks that every requirement of the milestone is covered exactly once, checks readiness, pins the context repository's commit, and hands a ready bet to the implementation loop in the code repository. Use when the user says shape the next milestone, break this into bets, size this, is bet N ready, reshape bet N, hand off bet N, or drop bet N before it is handed off. Not for PR slices (planning-implementation)."
license: MIT
---

# Shaping bets

A bet is a unit of work sized for agentic delivery, closer to an epic than to a task. The term comes from Shape Up: the work is shaped before anyone builds it, the appetite (how much it is worth) is fixed before anyone estimates, the bet is handed over whole, and a circuit breaker stops it instead of letting it grow. This skill cuts a milestone into bets, writes each bet file, checks readiness, and hands ready bets to the implementation loop in the code repository at a pinned commit. It never writes into the code repository.

## Appetite

| Appetite | Means | Use |
|---|---|---|
| M | One plan with several phases, in the implementation loop's terms | One capability, or one flow end to end |
| L | Two or three plans | A capability that crosses containers or needs a new contract; the first bet in an empty code repository |

A plan for a verification harness (Plan 0) does not count against the appetite; a walking skeleton does. Work smaller than M joins a neighbouring bet. Work larger than L splits. Appetite is a ceiling, not a target: never pad a bet to fill it. The implementation loop reads the same scale and stops when the work outgrows it; only the user's words raise an appetite.

## Inputs

- The version brief and the milestone being shaped. When neither exists, run `planning-product-roadmaps` first when it is installed; otherwise ask the user for the milestone and the requirements it targets.
- The requirements whose target Version is that milestone, from `product/requirements/`.
- `architecture/`, especially `contracts/`; `decisions/`; the risk and open-question registers; design handoffs under `design/` for anything with a user interface.
- The bet board of every version, for the next bet number and for bets already in flight.

## Shape a milestone

Read [sizing and appetite](references/sizing-and-appetite.md) before the first step.

1. **List the milestone's requirements** with their IDs. Note those targeted only in part, and the part.
2. **Find the seams.** Cut by outcome, never by layer: each bet delivers something a person can see or do, end to end through the containers it needs. Put the walking skeleton first when the code repository is empty. Keep requirements that share a flow or a contract together; set apart those that wait on design work.
3. **Draft the slate**: for each bet, an outcome-shaped title, the requirement IDs (all or part), the appetite, its dependencies, and the contracts it consumes or produces.
4. **Check coverage.** Every requirement of the milestone is covered exactly once, and partial coverages add up to the whole requirement. A requirement with no bet, or with two, is a defect in the slate.
5. **Size each bet** against the rules in the reference: M or L, about 3 to 12 requirement IDs, at most about 15 acceptance criteria, only `accepted` contracts consumed, at most one contract produced or changed.
6. **Present the slate** in one message: a table of bets in dependency order, the coverage check, and what each bet still needs before it can be ready (a contract, a decision, a design handoff, an answered question). Ask for agreement. An edit request means revise and present again.
7. **Write each agreed bet** from [the bet template](templates/bet.md), as [writing a bet](references/writing-a-bet.md) describes, with `Status: shaped`. Number bets after the highest number used in any version; never reuse a number. Rebuild the version's bet board from [the bet board template](templates/bet-board.md); it is derived from the bet files.

## Check readiness

A bet becomes `ready` only when every row holds. Read [readiness and handoff](references/readiness-and-handoff.md) for how to check each.

| Check | Holds when |
|---|---|
| Requirements | Every ID exists in the catalogue with this milestone as its target and status `planned` |
| Acceptance criteria | Each is observable from outside the code, names its requirement, and every requirement has one |
| Contracts | Every consumed contract lists the version the bet names as `accepted`; a produced or changed contract states what the bet fixes about it |
| Decisions | Every decision the bet relies on is `accepted` |
| Dependencies | Every bet it depends on is `built` or `done`; `Bet 03` is the file `roadmap/v*/bets/03-*.md` |
| Design | A bet that changes a user interface links an agreed design handoff under `design/` |
| Open questions | No open question listed against the bet blocks it |
| Code repository | The Code repository field names a repository that exists, or the bet is the first in a new one and is shaped L |
| Context repository | It has commits, and no path the bet names has an uncommitted change: the bet, the requirement files for its IDs, the contracts, the decisions, the context pack |

A failed check names what fixes it: a contract through `designing-system-architecture`, a decision through `decision-records`, a design handoff through the `product-design` skills, each when it is installed; an open question goes to the user. Without the skill, name the gap and leave the bet `shaped`.

## Hand off

1. Confirm readiness. Commit the bet's final text, then take the context repository's full HEAD commit SHA as the pin.
2. Write the bookkeeping fields: `Status: in delivery`, `Context pinned: <sha>`, and the `## Handoff` section with the date, the code repository, the work-item slug (`NN-slug`) and the kickoff line. Commit them. The implementation loop reads the bet's own fields at the pin: every header line except `Status:` and `Context pinned:`, and every section except Handoff and Outcome log. It reads the bookkeeping fields (Status, Context pinned, Handoff, Outcome log) at the latest commit.
3. Give the user the kickoff line to run in the code repository:

   ```
   Use running-implementation-loops on bet <path in the context repository> in <context repository checkout> at <full sha> as work item <NN-slug>
   ```

   For an agent that sees only the code repository, render the bet with [the kickoff template](templates/kickoff.md) as an issue there, pasted at the pinned commit; creating the issue is the user's action or needs their words.

## Reshape or drop

The implementation loop stops a bet when its appetite or boundaries no longer hold: the plans outgrow the appetite, a no-go would be crossed, a consumed contract or decision must change, the scope grows beyond the bet's requirements, or a rabbit hole survives two attempts. It reports the evidence and the options. Reshaping happens here:

- **Split**: the bet keeps its number and the part that fits; the rest becomes a new bet with the next free number and moves the coverage with it.
- **Change a contract or a decision**: first, through `designing-system-architecture` when it is installed, otherwise as an open question for the user; then update the bet.
- **Add or change a requirement**: first, through `curating-product-requirements` when it is installed; then update the bet.
- **Raise the appetite**: only in the user's words. Edit the bet's `Appetite:` line and add a dated line with the user's words to the Handoff section.

Commit the reshaped bet, take the new pin, write a new Kickoff line in the Handoff section next to the dated entry, and give the user that kickoff line: the same format and work-item slug as the first one, with the new SHA. The loop treats a kickoff for an existing work item with a new SHA as the user's re-pin. Cutting `~` scope needs no reshape: the loop does it at its own G1, in the user's words. An appetite extension the user gives inside the loop is recorded in the work item's `roadmap.md` Decisions in the code repository and leaves the bet file unchanged; `reconciling-product-context` reports it when the bet closes.

Drop a bet here only while it was never handed off (`shaped` or `ready`): set `Status: dropped` with the date, the reason and the user's words in the Handoff section, and rebuild the bet board; its requirements stay `planned` for another bet. A bet `in delivery` is closed as dropped by `reconciling-product-context`, which writes its outcome log.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| A bet per layer: "the API for lists" | One outcome, end to end through the containers it needs |
| Implementation steps in the bet | The outcome, boundaries and criteria; the loop plans the work |
| Requirement text copied into the bet | IDs only; the text stays in the catalogue |
| Criteria nobody can observe: "works reliably" | Concrete values, observable from outside the code |
| Consuming a `proposed` contract | Settle the contract first |
| Padding a bet to fill its appetite | Appetite is a ceiling |
| Extending an appetite because the work grew | Reshape, or ask the user |

## Hand back

Report the bets written or changed with their status, the coverage check, what blocks each bet that is not `ready`, and for a handoff the pin and the kickoff line. Commit in the context repository only when the user asks, except the commits a pin requires: the two handoff commits, and the reshape commits before a re-pin, which the handoff or reshape request authorizes.

## When a sibling skill is missing

Name the missing skill in one line, then produce its essential outcome yourself only when it is small: an index row, a one-line note in a register. A missing contract, decision or design handoff blocks readiness; never invent one to make a bet ready. Without file access, return the slate and the bet files as complete Markdown, say that nothing was written, and do not report a bet as handed off.

## References

| Read | When |
|---|---|
| [sizing and appetite](references/sizing-and-appetite.md) | Finding seams, sizing, splitting and merging, the first bet in an empty code repository, a worked slate |
| [writing a bet](references/writing-a-bet.md) | Writing or reviewing each section of a bet file |
| [readiness and handoff](references/readiness-and-handoff.md) | Checking readiness, pinning, what the loop reads at the pin, the kickoff line, status transitions, resuming after a reshape, dropping |
| [bet template](templates/bet.md) | Writing a bet |
| [bet board template](templates/bet-board.md) | Rebuilding a version's bet board |
| [kickoff template](templates/kickoff.md) | Rendering a bet as an issue for an agent without the context repository |
