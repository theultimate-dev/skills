---
name: verifying-implementation
description: "Verifies a committed candidate for real, without the user (stage 6 of the product-engineering loop). Checks out the handed-over branch, confirms HEAD is the handed-over commit SHA and never commits, starts the app itself from that checkout with docs/product-engineering/verification-profile.md, runs the automated checks, drives the running product through every acceptance criterion in the Verification section of spec.md with the agreed tool (a browser-driving tool, an HTTP client, a CLI, a database query), checks persistence, console and network errors, runs a timeboxed exploratory pass, challenges test strength with fault injection, and writes a Verification report for the pull request body, or verification.md when there is no PR. Use after implementing a PR slice, after a repair, or when the user asks 'verify it works', 'test this in the browser', 'check the acceptance criteria', 'QA this change', or 'does it actually work'."
license: MIT
---

# Verifying implementation

Prove that the candidate works by running it and watching it. Tests are part of the evidence. The rest is the agent driving the running product through every acceptance criterion with the agreed tool and recording what it saw. A criterion passes only when its pass condition was observed on a known commit.

This is stage 6 of the product-engineering loop. It runs without the user, once for every slice of work that becomes one pull request (merge request), called a PR slice. It reads:

- `docs/product-engineering/verification-profile.md`: how to install, seed, start and probe the app.
- The `## Verification` section of `docs/product-engineering/<work-item-slug>/spec.md`: the contract agreed at G3, one row per acceptance criterion.
- The plan in `plans/NN-slug.md`: which criteria this slice delivers.

It writes a `## Verification` report for the PR body, or `verification.md` in the work-item folder when there is no PR.

Run this stage in a fresh context when the host has parallel agents or subagents: give the verifier the contract, the profile, the branch and the SHA, not the implementer's reasoning. When the implementer verifies its own work, the report says so.

## Missing inputs

| Missing | Do this |
|---|---|
| The contract (quick-fix track, or no G3 happened) | Derive one row per criterion, or per stated intent, in the contract's columns. The report's Contract line says "checks derived by the agent, not agreed at G3" |
| The profile | Discover the start command first, from the project's scripts, README, compose file and CI configuration. Then ask the user one question: which environment is allowed, plus the start command only when discovery found none. `defining-verification` writes a full profile when installed. Never run a start command against an unknown environment |
| The plan | Verify every row in the contract |
| The agreed tool, on this host | Use another tool with the same capability and name it in the report. With no tool for the capability, the row is `blocked` |

## Procedure

### 1. Check out the candidate and confirm the SHA

The verifier never commits. Only `implementing-plans` commits code and planning files.

1. Run `git status --porcelain`. Ignore only this work item's own `verification.md` and `review.md`, which `implementing-plans` commits with its next commit. When it shows any other change, stop and return the list to `implementing-plans`; without that skill, show the list to the user. Never commit, stash or discard them: an uncommitted tree ties the evidence to nothing.
2. Check out the branch you were given, and confirm `git rev-parse HEAD` equals the SHA you were given. When they differ, stop and return both SHAs. When the user asked directly and named no branch or SHA, verify the current `HEAD`: record its full SHA and the branch name.
3. Every result in the report belongs to that SHA. When any commit lands after a check ran (a repair, a review fix, a rebase), that check is stale. Rerun every check whose code path, dependencies, configuration or data the new diff touches (`git diff --stat <old-sha>..<new-sha>`). A rebase onto a moved base reruns everything. Carry forward only checks the diff cannot affect, and mark each one "carried from" with the old short SHA.

### 2. Prepare the environment and start the app

1. Check each environment variable the profile names with `test -n "${VAR-}"`, and never print its value. For each URL variable, print only its host and compare it with the allowed and refused environments in the profile and the contract. Refuse any production host, database or account, even read-only. An unset variable or an unknown host makes the rows that need it `blocked`.
2. Run install, start services, migrate and seed as the profile says, on a local database you created or reset for this run. A slice with a migration or backfill also follows its row in the table below, so the migration meets existing rows.
3. Start the app yourself from this checkout, in the background, with output redirected to a log file. Record the PID of every process you start. Never verify against a server, preview or container you did not start in this run, unless it reports this exact commit.
4. Poll the profile's readiness signal with a timeout; never sleep for a fixed time and hope. On timeout, the rows that need the app are `blocked`: quote the last log lines, redacted.
5. Probe each tool you will use once against the readiness URL.

| Project | Start and readiness |
|---|---|
| No server: a library, CLI, mobile or desktop app | Build from this checkout. Ready means the library imports in a scratch script, the CLI binary prints its `--version`, or an emulator or simulator runs this build and shows its first screen. With no native UI driver on the host, the native UI rows are `blocked` |
| Monorepo | Start every app and service the slice's rows touch, each from this checkout, and poll each readiness signal |
| A migration or backfill | Seed at the base SHA from a worktree, then migrate from this checkout. Record the row counts before and after, and the duration. Seed-sized data does not predict production time: say so under Mocks and limits |

A port held by a process you did not start stays untouched. Use another port when the app supports it; otherwise the rows are `blocked`.

### 3. Run the automated checks

Run every command under the contract's Automated checks on the SHA, and read the actual result:

- The exit code and the summary: passed, failed, skipped.
- A suite that ran zero tests, or skipped the tests this slice added, is `blocked`, not `pass`.
- A failure is "fails on the base too" only when a run on the slice's base failed with the same message: the base run `implementing-plans` reported, or your own run in a worktree at `git merge-base HEAD origin/<base>`. The profile's baseline can be stale; never rely on it alone. Report a base failure; never drop it.
- The tests the plan promised exist and ran. Name them.

### 4. Drive the product for every criterion

For each contract row of this slice, follow its Steps with its Tool:

1. Generate the unique value the steps call for, such as a title with a timestamp.
2. Act as the user would: by role, label and visible text.
3. Observe the pass condition. Quote the exact text, status, count or row you saw.
4. Observe the side effects: the state after reload or restart, the database row or the file, console errors, failed network requests, errors in the server log.
5. Record the result:
   - `pass`: the pass condition was observed, and no unexpected console error, failed request or server error appeared during the journey.
   - `fail`: something else was observed. Quote expected and observed. A row that failed and then passed on retry is `fail`, unless the first failure was a quoted tool error.
   - `blocked (human eye)`: the row was agreed at G3 as needing a human eye. Report it with a screenshot for the user. The PR is `human`, and the loop continues.
   - `blocked`: the check could not run. Name why. The slice stops before its PR opens (step 9).

Check every constraint in `spec.md` that is observable at runtime the same way, for example "no new third-party requests". Rerun the `e2e` rows of criteria from earlier slices when this slice touches their code path. Read [driving the app](references/driving-the-app.md) for readiness, locators, waiting, console and network capture, a second user, persistence and cleanup.

### 5. Exploratory pass

Timebox it: about 10 minutes for a small change, 20 to 30 for a feature slice. Work through the [exploratory charter](references/exploratory-charter.md) for each surface the slice touches: empty, error and loading states; invalid input; a second user denied access; refresh and back; a narrow viewport; keyboard only; slow or failed network where the tool can simulate it.

- A defect inside the slice's scope fails the criterion it breaks.
- A pre-existing defect outside scope becomes a follow-up in the report. Do not fix it here.
- Record what was covered and what the timebox left out.

### 6. Challenge the tests

For consequential behavior (permissions, money, data loss, persistence, and any criterion covered only by automated tests) ask: would a plausible wrong implementation still pass?

1. Inject that fault in an isolated git worktree at the SHA, never in the working branch.
2. Run the check that should catch it. It must fail for the right reason, not with a compile error.
3. Remove the worktree. Confirm `HEAD` still equals the SHA and the tree is clean.

A fault that survives is a test gap. Return it to implementation like a failure. Skip this step for trivial edits. Read [test quality](references/test-quality.md) for the faults to try and the weak-test patterns.

### 7. Clean up

- Stop every process and container you started, by PID or by the compose project you started. Leave everything else running.
- Close the browser sessions, remove the worktrees, delete the scratch scripts.
- Confirm `git status` is clean and `HEAD` equals the recorded SHA.

### 8. Write the report

Fill the [verification report](templates/verification-report.md): the SHA, one row per contract row (`| AC | Result | What was done | What was observed |`), the automated checks, exploratory notes, test strength, flaky checks, mocks and limits, carried-forward rows, and everything blocked.

- Evidence is text: quoted screen text, status codes, counts, rows. Screenshots and traces are referenced by local path or CI artifact name, never embedded.
- Redact tokens, keys, cookies and connection strings from quoted logs and output.
- Keep the section under about 10,000 characters, so the whole PR body stays far below GitHub's 65,536-character limit. Quote only the relevant log lines.
- The report is complete when every contract row for this slice has a result with what was done and what was observed, and the SHA is the one under review. Complete does not mean passing.

Where it goes:

- No PR yet: hand the section to `shipping-pull-requests`, or to the user, for the PR body.
- A PR is open: replace its `## Verification` section and keep the rest of the body. Inside the loop, return the section to the coordinator, which makes this edit; a verifier dispatched by a coordinator stays read-only toward the PR. Detect the host from the git remote. With GitHub, read the body with `gh pr view <number> --json body` and write it back with `gh pr edit <number> --body-file <file>`; the GitLab or other host equivalent applies.
- No PR will be opened: write `docs/product-engineering/<work-item-slug>/verification.md`.

### 9. On a failure or a block

Return the failure to `implementing-plans` with a precise repro: the SHA, the AC and row, the exact steps, expected versus observed (quoted), the evidence path, and the relevant console or log lines, redacted. Report what the evidence shows, not a guessed cause. A flaky check in code this slice touches is a test defect: return it the same way. Without that skill, fix it yourself starting from the same repro, or hand the repro to the user.

After the repair, rerun the failed row and every check the repair diff affects, on the new SHA. Apply the two-attempt rule: after two failed attempts at the same failure with no new evidence, change the approach or escalate.

Any `blocked` row other than `blocked (human eye)` stops the slice before its PR opens, for example when the app will not start, a required tool is missing, or the only allowed environment is down. Escalate with the blocked rows: the verification contract cannot run (G3). That is an escalation trigger, not a pass.

## Honesty rules

- Never mark a row `pass` from reading code, a diff or a test file.
- Never claim a browser run, click or screenshot that did not happen. Name the tool that did it.
- Label every mock, stub and sandbox, and what it excludes.
- Never commit. Verify only the SHA you were handed, on an app you started from it or one that reports that exact commit.
- `blocked` and `blocked (human eye)` are not `pass`. A slice with a `blocked` row is not verified and does not reach a PR.
- A row that failed and then passed on retry is `fail`, unless the first failure was a quoted tool error. Report both outcomes.
- Never print or quote a secret's value.
- A suite that ran zero tests is `blocked`.
- Evidence from another SHA counts only when marked as carried forward.
- Never touch production, not even to read.
- Stop the servers you started.

## Tracks

| Track | What changes |
|---|---|
| Quick fix | Derive the check from the intent. A user-facing change is still driven in the running product. The report goes in the PR body |
| Bugfix | Confirm the repro row fails on the base SHA for the reported reason, then passes on the candidate. Record both SHAs |
| Small change, feature | The procedure as written, once per PR slice |
| Refactor | Rerun the characterization tests and before-and-after journeys captured on the base. Any observable difference fails, unless `spec.md` lists it |
| New app | Run the `verify` entry point from a clean clone, and drive the walking skeleton's journey end to end |
| Spike | No report. Record what was run and observed in the findings; a spike is never marked verified |

## Hand back

Return:

- The SHA, and counts of `pass`, `fail`, `blocked` and `blocked (human eye)`. When step 1 stopped the run: the uncommitted files, or both SHAs.
- Where the report went: handed over, PR body updated, or `verification.md`.
- Each `fail`, with its repro.
- Each `blocked (human eye)` row, with its screenshot path. It puts the PR in the `human` review category, and the loop continues.
- Each other `blocked` row, with its reason. The slice stops before its PR opens and escalates: the verification contract cannot run (G3).
- Flaky checks, test gaps, and out-of-scope follow-ups.

## References

| Read | When |
|---|---|
| [driving the app](references/driving-the-app.md) | Starting the app, picking and operating a tool, second-user sessions, persistence, cleanup |
| [exploratory charter](references/exploratory-charter.md) | The exploratory pass, by surface: web UI, API, CLI, background job |
| [test quality](references/test-quality.md) | Challenging tests, fault injection, fail-before and pass-after, flaky results |
| [verification report](templates/verification-report.md) | Writing the report for the PR body or `verification.md` |
