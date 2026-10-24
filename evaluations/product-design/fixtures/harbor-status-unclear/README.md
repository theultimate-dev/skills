# Harbor

Harbor is a fictional app that watches the backups of a home server. Harbor needs a view that shows the backup status at a glance. People check it several times a day to see whether last night's backup worked, and look closer only when something failed.

## What the view shows

- Last backup: Today 03:12 · 41.2 GB · 1 warning, 1 failure
- Next run: Tonight 03:00
- Volumes:
  - Photos: OK
  - Documents: Warning, 3 files skipped
  - Server config: Failed, destination full
- Actions: Back up now, Open logs, Settings

## What the settings hold

- Schedule: the daily time, and the days to skip
- Destinations: the backup disks and network shares, each with its free space
- Notifications: failures only, warnings and failures, or every run

## Design state

- Visual language: none yet, nothing to preserve.
- Design files: none.
- Public references: none.
- Application code: none yet.
