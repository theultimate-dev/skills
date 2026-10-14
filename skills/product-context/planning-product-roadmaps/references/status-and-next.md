# Status and what's next

How to answer "what's the product status" and "what's next for the product" from the repository, and what to recommend.

## Sources, in order of authority

1. **Bet files.** Each bet's `Status:` line (`shaped`, `ready`, `in delivery`, `built`, `done`, `dropped`) is the only authoritative status of that bet. Read `Milestone:`, `Depends on:` and the `## Handoff` section too.
2. **The version brief.** Milestone statuses, exits, prerequisites, the coverage index.
3. **The registers.** Open questions and risks, with what they block.
4. **The requirement catalogue.** Status and Version columns.
5. **`roadmap/README.md`.** Versions and their statuses, gates, the current focus.
6. **`architecture/README.md`.** Whether the architecture baseline is accepted, and which contracts are `proposed`.

The bet board (`roadmap/vN/bets/README.md`) is a derived copy of the bet files. Use it to find the bets, never to read their status. When it disagrees with a bet file, the bet file wins; list the disagreement in the report and recommend `reconciling-product-context`, which rewrites the board.

Live pull request state lives on the code host and never in the context repository. A bet `in delivery` says only where it was handed; when the user wants to know how far it got, point them to the implementation loop's status in the code repository named in the Handoff section.

## Checks

- **Dependencies.** A bet's dependency is met when the bet it depends on is `built` or `done`. A dependency that is neither blocks readiness, so the bet stays `shaped` and is listed under Shaped, not ready, naming the dependency.
- **Readiness.** For every `shaped` bet, name what fails readiness: a consumed contract version still `proposed`, a dependency not yet built, an open question listed against it, a missing design handoff.
- **Baseline.** The version in focus has an accepted architecture baseline when `architecture/README.md` shows its containers and the decisions that precede code; otherwise no milestone of it should be shaped yet.
- **Coverage.** A requirement of the milestone in focus that no bet's Requirements table lists, fully or as the remaining part, needs shaping.
- **Stale states.**
  - `built` bets older than a few days are unreconciled work: every later answer about requirements and architecture is wrong until they are closed.
  - A milestone whose bets are all `done` but which has not exited is waiting on the user's judgement of its exit criterion.
  - A requirement still `planned` in an exited milestone is a gap.
- **Blockers.** An open question whose Blocks field names the milestone in focus or one of its bets; a prerequisite outside the code whose checkbox is open and which gates the milestone in focus.

## Report

```text
Roadmap status, [date]. Focus: [version], milestone [N.N Name] ([status])

In delivery
- Bet 04 Use-soon list → larder, work item 04-use-soon-list (handed off 2026-11-10)

Built, awaiting reconciliation
- Bet 03 Expiry dates: close it with reconciling-product-context

Ready to hand off
- Bet 05 Pantry search (depends on Bet 03: built, not yet done; may start)

Shaped, not ready
- Bet 06 Meal plan sync: consumes sync-protocol 1.1, still proposed → designing-system-architecture, contract mode

Needs shaping
- 1.2 Meal plans: MEA-01 to MEA-04 and PAN-06 are covered by no bet

Blocked
- OQ-07 Must meal plans work offline? Blocks Bet 06. Recommended: no in V1
- Prerequisite: privacy notice reviewed (gates 1.2)

Milestones and versions
- 1.0 Skeleton exited 2026-11-02; 1.1 Pantry in progress; 1.2 planned
- Gate to V2: in daily use by five households for a month (not yet)

Board disagreements
- bets/README.md shows Bet 03 as in delivery; the bet file says built

Next: close Bet 03 with reconciling-product-context.
```

Leave out empty sections. Keep each line to one bet, milestone or item.

## What's next

First match wins. Name one action; mention the second only when it can run in parallel. These are the same rules, in the same order, as the skill's own list.

1. **A `built` bet** → close it with `reconciling-product-context`.
2. **A `ready` bet whose dependencies are `built` or `done`** → hand it off with `shaping-bets`.
3. **No accepted architecture baseline for the version in focus** → run `designing-system-architecture` in baseline mode before any shaping.
4. **A `shaped` bet that fails readiness** → route it to the fix: a `proposed` contract to `designing-system-architecture` in contract mode, an open question to the user, a missing design handoff to the `product-design` skills, a dependency not yet built to that dependency's own next step.
5. **The milestone in focus has requirements no bet covers** → shape it with `shaping-bets`.
6. **An open question blocks the milestone in focus** → ask it, with its recommended answer.
7. **All bets of the milestone are `done` and it has not exited** → ask the user whether its exit criterion holds.
8. **The version just shipped** → record it, check the gate, and refresh the architecture with `designing-system-architecture` before shaping the next version.
9. **Nothing above** → plan the next milestone or version.

When a sibling skill named here is not installed, name the action anyway, and follow the skill's missing-sibling table: it says which essential outcome to produce yourself and which to leave as a report.
