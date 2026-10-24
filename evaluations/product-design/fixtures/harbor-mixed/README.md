# Harbor

Harbor is a fictional app that watches the backups of a home server. This work covers two surfaces:

1. Harbor's macOS menu-bar panel: its status item opens the panel. People glance at it several times a day to see whether last night's backup worked.
2. Harbor's web account page, opened in a browser on phones and desktops, where people manage their plan and devices.

## What the panel shows

- Last backup: Today 03:12 · 41.2 GB · 1 warning, 1 failure
- Next run: Tonight 03:00
- Volumes:
  - Photos: OK
  - Documents: Warning, 3 files skipped
  - Server config: Failed, destination full
- Actions: Back up now, Open logs, Settings…

## What the account page holds

- Plan: Home, 2 TB, renews on 1 March
- Storage used: 1.3 TB of 2 TB
- Devices: the home servers linked to the account, each with its last check-in
- Billing email, and a link to download invoices

## Design state

- Visual language: none yet, nothing to preserve.
- Design files: none.
- Public references: none.
- Application code: none yet.
