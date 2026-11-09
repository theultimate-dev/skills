# Bet 01: The due list

Status: kept
Appetite: 1 day · Framing: none, shaped without a framing note
Autonomy: code commits: main; context commits: yes; push: no; revert on remove: yes. Approved 2026-10-03: "go ahead"
Context pinned: @@C1@@

## Outcome

The plant keeper runs `due` and sees which plants need water today.

## Requirement deltas

| ID | Change | Text or reason |
|---|---|---|
| WAT-02 | new | `due` lists every plant whose next watering date is today or earlier |

## Acceptance checks

- C1 (WAT-02): A fern added on 2026-03-01 every 7 days is listed on 2026-03-08 and not on 2026-03-07. · Method: test

## Boundaries

- No-go: reminders of any kind.
- Rabbit hole: none.

## Keep or remove

- Signal: the due list is what gets opened each morning.
- If removed: the code commits are reverted.

## Architecture

- Touches: none
- Introduces: none
- Relies on: none

## Context pack

1. product/overview.md: what Sprig is

## Build log

Started: 2026-10-03 09:00 · Finished: 2026-10-03 11:00 · Base: @@C1@@ · Head: @@C1@@ · Branch: main
Code commits, oldest first: none recorded; the due list predates the loop.

## Result

Kept, 2026-10-04: "Keep it." Lesson: a list is enough.
