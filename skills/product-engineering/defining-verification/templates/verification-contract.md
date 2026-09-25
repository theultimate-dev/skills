## Verification

Profile: `docs/product-engineering/verification-profile.md`, confirmed [YYYY-MM-DD]
G3: [agreed YYYY-MM-DD, "the user's own words"] or [pending: the open question]

| AC | Check | Layer | Tool | Steps | Pass condition |
|---|---|---|---|---|---|
| [AC1 (R1)] | [A created task persists] | [e2e] | [browser (Playwright MCP)] | [1. Sign in as `E2E_USER_EMAIL`. 2. Add a task titled `verify-{timestamp}`. 3. Reload.] | [After reload, the list shows that title exactly once; no console error; no failed request] |
| [AC1 (R1)] | [New automated test: create, then reload] | [e2e] | [Playwright test runner] | [Runs in CI and locally] | [The test passes, and fails when the save call is removed] |
| [AC2 (R2)] | [Another user cannot read a task] | [api] | [HTTP (curl)] | [1. As user A, create a task and note its id. 2. As `E2E_USER_B_EMAIL`, request `GET /api/tasks/{id}`.] | [Status 404; the body contains no title] |
| [AC3 (R3)] | [The empty state reads well] | [visual] | [user (human eye)] | [Screenshots of the empty list at 375 px and 1280 px wide] | [The user confirms tone and layout] |

### Automated checks

Every command runs on the candidate SHA and must pass. Baseline failures from the profile are listed, not ignored; a failure counts as pre-existing only when a run on the slice's base fails with the same message.

- [pnpm lint]
- [pnpm typecheck]
- [pnpm test]
- [pnpm exec playwright test]

### Who certifies

- The agent self-certifies: [AC1, AC2: functional behavior, persistence, permissions]
- Human eye: [AC3: visual tone of the empty state]. These rows are reported `blocked (human eye)` with a screenshot until the user looks. They put the PR in the `human` review category, and the loop continues. Any other `blocked` row stops the slice before its PR opens.

### Environments and limits

- Allowed: [local through docker compose; ephemeral preview]
- Never: production ([hosts named in the profile]), not even read-only
- Data: [reset only the local database the seed created]
- Side effects: [no real email; use the local mail catcher]

### Mocks and what they exclude

- [Payment provider in test mode: excludes real card-network responses and payouts] or [none]

### Harness gaps

- [No second test account: Plan 0 seeds user B] or [none]
- "How to verify" pointer in AGENTS.md or CLAUDE.md: [accepted YYYY-MM-DD: in Plan 0 | accepted YYYY-MM-DD: its own `human` PR slice | declined | already present]
