<!--
Fill every [bracket]. Evidence is text: quote what was seen. Reference screenshots and traces by local path or CI artifact name; never embed them.
Keep this section under about 10,000 characters so the PR body stays far below GitHub's 65,536-character limit.
Delete subsections that do not apply. Never delete a failed or blocked row.
Results: pass, fail, blocked, or blocked (human eye). A row that failed and then passed on retry is fail, unless the first failure was a quoted tool error.
Redact tokens, keys, cookies and connection strings from quoted logs and output.
With no PR, save this as verification.md in the work-item folder, with "# Verification: [work item]" as the first line.
-->
## Verification

Commit: `[full 40-character SHA]` on `[branch]`
Environment: [local, docker compose] · Profile confirmed [YYYY-MM-DD] · Tools: [Playwright MCP (isolated), curl, psql]
Contract: [full, or rows for this slice: AC1, AC2] · [agreed at G3, or checks derived by the agent, not agreed at G3]
Verified by: [a fresh-context verifier, or the implementing agent]
Summary: [N] pass · [N] fail · [N] blocked · [N] blocked (human eye)

| AC | Result | What was done | What was observed |
|---|---|---|---|
| [AC1 (R1)] | pass | [Signed in as `E2E_USER_EMAIL`, added a task titled "verify-1727262000", reloaded; queried `tasks` by that title] | [After reload the list showed "verify-1727262000" once; one matching row in `tasks`; no console errors; no failed requests] |
| [AC2 (R2)] | fail | [As `E2E_USER_B_EMAIL`, requested `GET /api/tasks/42`, a task owned by user A] | [Expected 404; got 200 with the body `{"title":"verify-1727262000"}`] |
| [AC3 (R3)] | blocked (human eye) | [Screenshots of the empty list at 375 px and 1280 px wide] | [Needs the human eye for visual tone: `[path or artifact]`] |

### Automated checks

| Command | Result | Summary |
|---|---|---|
| `[pnpm lint]` | pass | [0 problems] |
| `[pnpm test]` | pass | [142 passed, 0 failed, 0 skipped; new: `tasks.api.test.ts › denies other users`] |
| `[pnpm exec playwright test]` | fail | [1 failed: `create task persists`; trace `[artifact]`; not a baseline failure] |

### Exploratory notes

Timebox: [15 minutes]. Covered: [web UI states, input, access, 375 px, keyboard]. Not covered: [slow network].

- [Empty title, submit: "Title is required" next to the field; no request sent.]
- [Follow-up, outside scope, also on the base: the settings page logs a 404 for `favicon.svg`.]

### Test strength

- [Fault: removed the owner check in `src/tasks/get.ts` in an isolated worktree. `denies other users` failed with "expected 404, received 200". Worktree removed.]
- [Regression: `[test name]` failed on base `[short SHA]` with "[message]", and passes on this commit.]

### Flaky

- [None, or `[test name]` failed once with "[message]", then passed on retry. In code this slice touches: `fail`, a test defect returned to `implementing-plans`. Outside it: a follow-up.]

### Mocks and limits

- [Payment provider in test mode: excludes real card-network responses and payouts.]
- [Browser automation is not a user study; the flow's feel is left to the human eye.]
- [Migration run on seed-sized data: [N] rows before and after, [duration]. It does not predict production time.] or [None]

### Carried forward

- [Rows AC4, AC5 from `[short SHA]`: the later diff touched only `[paths]`.] or [None]

### Blocked and not verified

- [AC3 `blocked (human eye)`: needs the human eye for visual tone. Screenshots: `[path or artifact]`. The PR is `human`.]
- [AC4 `blocked`: why the check could not run. The slice stops before its PR opens: the verification contract cannot run (G3).] or [None]

Evidence files: [local directory or CI artifact names]. Not committed.
