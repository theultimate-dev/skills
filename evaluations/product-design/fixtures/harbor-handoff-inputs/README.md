# Harbor

Harbor is a fictional app that watches the backups of a home server. It lives in the macOS menu bar: its status item opens a panel, and Settings… in the panel opens a settings window. People glance at it several times a day to see whether last night's backup worked, and open it fully only when something failed.

## What the panel shows

- Last backup: Today 03:12 · 41.2 GB · 1 warning, 1 failure
- Next run: Tonight 03:00
- Volumes:
  - Photos: OK
  - Documents: Warning, 3 files skipped
  - Server config: Failed, destination full
- Actions: Back up now, Open logs, Settings…

## What the settings window holds

- Schedule: the daily time, and the days to skip
- Destinations: the backup disks and network shares, each with its free space
- Notifications: failures only, warnings and failures, or every run

## Design state

- Visual language: none yet, nothing to preserve.
- Design files: three direction briefs in `visual-directions.md`, and direction A's sketch, `direction-a.html`, with its notes, `direction-a-notes.md`.
- Public references: none.
- Application code: none yet.

## Decisions so far

- 2026-10-24: the device geometry in `direction-a-notes.md` is the product owner's own figures for the sketch.
- 2026-10-25: the product owner chose direction A, Verdict first, after viewing `direction-a.html` in each placement. Directions B and C are not pursued.
- 2026-10-25: the departures listed in `direction-a-notes.md` are accepted.
