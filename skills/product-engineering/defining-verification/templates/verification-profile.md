# Verification profile

Confirmed: [YYYY-MM-DD] at commit [short SHA]
Re-check when these paths change: [package manifests, CI configuration, compose files, .env.example]

Names only. A secret value never appears in this file. Mark anything not yet confirmed by a run as `unconfirmed`, and anything designed but not built as `planned`.

In a monorepo, repeat Commands, Run the app and Verification tools under `## App: <path>` for each app.

## Stack

- Languages and frameworks: [e.g. TypeScript, Next.js]
- Package manager: [e.g. pnpm]
- Repository host: [GitHub, GitLab, other], from the git remote

## Commands

| Purpose | Command | Covers | Typical time | Baseline on [short SHA] |
|---|---|---|---|---|
| Install | [pnpm install --frozen-lockfile] | | | |
| Lint | | | | |
| Typecheck | | | | |
| Unit tests | | | | |
| Integration tests | | | | |
| End-to-end tests | | | | |
| Build | | | | |
| Verify entry point | [make verify, or "none: harness gap"] | | | |
| Run a single test | [e.g. pnpm vitest run path -t "name"] | | | |

Baseline values: `pass`, `fail` (quote the first failing test), `unconfirmed`.

## CI

- Workflows: [path: what it runs, on which events]
- Required checks on pull requests: [names, or "unknown: branch rules not readable"]
- Deploys or releases on push to the base branch: [yes: workflow and job, or no]

## Run the app

| Step | Command or value |
|---|---|
| Services | [docker compose up -d db mail] |
| Migrate | |
| Seed | |
| Reset data | |
| Start | [pnpm dev] |
| URL | [http://localhost:3000] |
| Readiness | [GET /health returns 200, or the log line "ready on"] |
| Logs | [stdout of the start command, or a file path] |
| Stop | [stop the start process; docker compose down] |

## Configuration and accounts

| Env var | Purpose | Where the value comes from |
|---|---|---|
| [DATABASE_URL] | [local database] | [.env.example default] |
| [E2E_USER_EMAIL, E2E_USER_PASSWORD] | [first test account] | [seed script; exists only locally] |
| [E2E_USER_B_EMAIL, E2E_USER_B_PASSWORD] | [second account, for permission checks] | |

## Verification tools

| Capability | Tool | Probe | Confirmed |
|---|---|---|---|
| Drive a real browser | [Playwright MCP, isolated] | [opened the readiness URL, read the heading "Tasks"] | [YYYY-MM-DD] |
| Call an HTTP API | [curl] | | |
| Run the app's CLI | | | |
| Inspect persisted state | [psql against the local database] | | |
| Capture outbound side effects | [Mailpit at http://localhost:8025, or none] | | |

Another host or machine may expose different tools. Probe before use. A tool with the same capability may replace one listed here; the report names the tool actually used.

## Environments

| Environment | URL or host | Allowed for verification |
|---|---|---|
| Local | [http://localhost:3000] | yes |
| Ephemeral preview | [URL pattern, or none] | [yes or no] |
| Staging | [URL, or none] | only when a work item's contract names it with the user's words |
| Production | [hosts, database names, accounts] | never, not even read-only |

## Default limits

- Data the agent may reset: [only local databases it created or seeded]
- Outbound side effects: [no real email, SMS, payments or webhooks; use the mail catcher or provider test mode]
- Load: [no load or stress tests against shared infrastructure]

## Harness gaps

- [Gap: Plan 0 in work item X, or declined by the user on YYYY-MM-DD, with the effect on verification]
