# Bet 04: Snooze a plant while away

Status: shaped
Appetite: 1 day · Framing: research/2026-11-02-snooze-while-away.md
Autonomy: code commits: main; context commits: yes; push: no; revert on remove: yes
Context pinned: not yet

## Outcome

The plant keeper runs `snooze NAME --days N` before going away, and the plant stays off the due list until those days have passed, or until it is watered. An out-of-range snooze is refused with a plain message.

## Requirement deltas

| ID | Change | Text or reason |
|---|---|---|
| WAT-07 | new | `snooze NAME --days N` hides a plant from `due` for N days from today |
| WAT-08 | new | A snooze is between 1 and 14 days; anything else is refused with status 2 |
| WAT-09 | new | `list` shows `snoozed until YYYY-MM-DD` for a snoozed plant |
| WAT-02 | changed | `due` lists every plant whose next watering date is today or earlier, except a plant that is snoozed |

## Acceptance checks

- C1 (WAT-07): A fern due on 2026-03-08 and snoozed that day with `--days 3` is absent from `due` on 2026-03-10 and listed on 2026-03-11. · Method: test
- C2 (WAT-08): `snooze fern --days 15` exits with status 2, prints `snooze: days must be between 1 and 14`, and leaves the data file unchanged; `--days 14` succeeds. · Method: run and observe
- C3 (WAT-02): A fern snoozed on 2026-03-08 for 14 days and watered on 2026-03-09 is listed by `due` on 2026-03-16: watering clears the snooze. · Method: test
- ~ C4 (WAT-09): `list` shows `snoozed until 2026-03-11` for the fern of C1. · Method: inspect output
- C5 (WAT-07): The snooze reads as one obvious step before a trip. · Method: person's eye

## Boundaries

- No-go: a snooze for every plant at once; one plant at a time.
- Rabbit hole: dates across a month end. Patched by: `--today` and calendar dates only; no time zones.
- ~ Cuttable: the `snoozed until` text in `list`.

## Keep or remove

- Signal: after the next trip the plant keeper snoozed the plants they meant to, and the due list stayed quiet until they were home.
- If removed: the code commits are reverted, WAT-07, WAT-08 and WAT-09 are recorded as dropped, the planned snooze window concept is deleted, and WAT-02 stays as it was.

## Architecture

- Touches: the one file `sprig.py` (architecture/context.md)
- Introduces: architecture/concepts/snooze-window.md (Status: planned)
- Relies on: decisions/0003-sprig-stays-offline.md

## Context pack

1. product/overview.md: what Sprig is
2. product/glossary.md: due, interval, plant
3. product/requirements/watering.md: WAT-02, the row this bet changes
4. architecture/context.md: one file, local dates
5. architecture/concepts/snooze-window.md: the planned rule for when a snooze ends
6. decisions/0003-sprig-stays-offline.md: why nothing here may reach the network

## Build log

## Result
