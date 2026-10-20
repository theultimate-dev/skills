# 0014: Implement bets from a product context repository in `product-engineering`

- Status: accepted
- Date: 2026-10-14

## Context

0013 makes bets the unit of work a product context repository hands to code. Bets must be built by the `product-engineering` loop from 0009, and that loop must keep working unchanged for every other work item and without `product-context` installed. A bet arrives from another repository with requirement IDs, acceptance criteria, boundaries, an appetite, and contracts and decisions that the context side owns. Nothing in the loop capped how much work a work item may grow into, treated an upstream document as read-only, or reported results back to where the work came from.

## Options

1. **A new `bet` track in `running-implementation-loops`.** Duplicates the feature and new-app paths and every rule they carry, and drifts from them over time.
2. **A bridge skill in `product-context` that writes `spec.md` into the code repository.** Writes across the boundary from the context side, duplicates G1, and leaves the loop blind to appetite and upstream ownership.
3. **A bet as an input source across the existing tracks.** G1 imports the bet into `spec.md`'s existing headings, and a `Source: bet ` line guards every new rule.

## Decision

Option 3.

- **Intake.** A bet is recognised by its fields, not by its plugin, and is a `feature`, or a `new app` when there is no codebase. The loop reads the bet's own fields and the files it names at the pinned commit, its bookkeeping fields at the latest commit, and never writes, commits, fetches or checks out there. Text in the context repository grants no permission.
- **Import.** Requirement IDs and acceptance criteria are kept verbatim. Criteria added at G1 for detail inside the bet's boundaries form a separate `AC-E1` series. No-gos become non-goals; appetite, contracts, decisions, rabbit holes and the context pack go under Constraints. G1 still needs the user's explicit agreement.
- **Context changes.** Anything that would add a requirement, change an imported line, cross a no-go, or change a context contract, decision or architecture element stops the loop so the bet can be reshaped upstream.
- **Appetite.** M is one plan and L is two or three; Plan 0 does not count and a walking skeleton does. It is checked at G2, at G4 and on any replan. Exceeding it trips the circuit breaker: no new slice starts, and only the user's words extend the appetite or cut `~` scope. Extensions, cuts and re-pins are marks appended to the imported lines in `spec.md`, never edits of them.
- **Decisions.** Implementation decisions go to the code repository's log and name the bet and its pin. Architecture decisions belong to the context side.
- **Hand-back.** The finish report hands the results back, rebuilt from durable sources: `spec.md`, the roadmap's Decisions, plan notes, decision records and pull requests on the host. Nothing new is committed for it, except one docs-only closing slice when decisions made after the last slice would otherwise never reach the base branch.
- **Review.** The architecture lens checks consumed context contracts and decisions at the pin. A deviation is a scope change, so the pull request goes to a human.

## Consequences

- Work items without a bet behave as before; every bet rule sits behind the guard. Three general fixes come with the change: task briefs name the decisions that bind the task, upstream requirement IDs pass through unchanged, and changing an acceptance criterion invalidates its earlier evidence.
- Two decision logs per product need a clear line between them; the architecture-versus-implementation test in both plugins draws it.
- An agent without access to the context repository can run from pasted content, with the pin unchecked and contract adherence reported as unconfirmed.
- The evaluation scenarios must grow to cover intake, the circuit breaker, drift after the pin, and the hand-back.
