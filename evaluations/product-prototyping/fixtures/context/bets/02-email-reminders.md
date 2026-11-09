# Bet 02: Email reminders

Status: removed
Appetite: 1 day · Framing: research/2026-10-12-email-reminders.md
Autonomy: code commits: main; context commits: yes; push: no; revert on remove: yes. Approved 2026-10-15: "go ahead"
Context pinned: @@C1@@

## Outcome

The plant keeper gets an email when a plant is due.

## Requirement deltas

| ID | Change | Text or reason |
|---|---|---|
| WAT-05 | new | Sprig emails a reminder when a plant is due |

## Acceptance checks

- C1 (WAT-05): A due plant produces one email to the configured address. · Method: inspect output

## Boundaries

- No-go: a hosted service.
- Rabbit hole: none.

## Keep or remove

- Signal: the email is opened rather than ignored.
- If removed: the code commits are reverted and WAT-05 is recorded as dropped.

## Architecture

- Touches: none
- Introduces: none
- Relies on: none

## Context pack

1. product/overview.md: what Sprig is

## Build log

Started: 2026-10-16 09:00 · Finished: 2026-10-16 15:00 · Base: @@C1@@ · Head: @@C1@@ · Branch: main
Code commits, oldest first: none recorded; the code was reverted before this context was adopted.

## Result

Removed, 2026-10-20: "Remove it. I am not setting up a mail account for a plant." Lesson: a reminder needs a server; decision 0003 stands.
