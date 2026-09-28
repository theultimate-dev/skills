---
name: defining-verification
description: "Agrees with the user how the agent will prove its own work before implementation starts (stage 3 of the product-engineering loop, gate G3 Verification). Discovers the project's test, lint, typecheck, build and CI commands, how to install, seed and start the app, and which browser-driving and other verification tools the host exposes; writes or confirms docs/product-engineering/verification-profile.md; drafts one observable check per acceptance criterion in the Verification section of spec.md; proposes a Plan 0 for missing verification harness; and records what the agent may self-certify, what needs a human eye, and which environments are allowed. Use after the approach is agreed, when a project has no verification profile yet, or when the user asks 'how will you verify this', 'set up verification', 'define acceptance checks', or 'verification profile'. Before implementation; running checks on a candidate is verifying-implementation."
license: MIT
---

# Defining verification

Agree, before any code is written, how the agent will prove its own work. After G4 the agent works alone, so this contract is what separates "looks done" from "works": every acceptance criterion gets a check the agent can run against the running product and read, with a pass condition anyone watching could observe. Without it, the user becomes the verification loop.

This is stage 3 of the product-engineering loop and ends at gate G3 Verification. It reads `spec.md` (acceptance criteria from G1, Approach from G2). An agreed spec's status line starts with `Status: agreed`, as in `Status: agreed (G1, 2026-09-25: "Agreed")` or, on a bugfix, `Status: agreed (G1 skipped: repro reproduced at a1b2c3d)`. On a track that batches the gates into one message, it may still say `draft`, because that message confirms every gate at once. Any other `draft` means G1 is open: run `specifying-work-items` first, or, when it is not installed, confirm the acceptance criteria with the user in one message and set the status line with their words. This skill writes two things:

- `docs/product-engineering/verification-profile.md`: per project, written once, reused by every later work item. In a monorepo, it repeats Commands, Run the app and Verification tools under `## App: <path>` for each app.
- The `## Verification` section of `docs/product-engineering/<work-item-slug>/spec.md`: the verification contract for this work item.

When there is no `spec.md`, run `specifying-work-items` first when it is installed. Otherwise draft numbered acceptance criteria (`AC1`, `AC2`, …) from the issue or the user's message, confirm them with the user in one message, and create `spec.md` with `Status: agreed (G1, YYYY-MM-DD: "<user's words>")`, `Track:`, `Source:`, the Acceptance criteria section and the Verification section.

## Procedure

### 1. Discover what exists

Ground every fact in the repository or in a command you ran. Never ask the user what the repository can answer.

| Find | Where to look | Record |
|---|---|---|
| Install, build, lint, typecheck, test commands | Package manifests and their scripts, Makefile, justfile, Taskfile, CONTRIBUTING, README | Exact command, what it covers, how long it takes |
| CI | `.github/workflows/`, `.gitlab-ci.yml`, other CI configuration | What runs on pull requests (merge requests), which checks are required, whether a push to the base branch deploys or releases |
| Starting the app | Compose files, Procfile, dev scripts, README | Start command, URL, readiness signal, how to stop it |
| Data | Migrations, seed scripts, fixtures, factories | Migrate, seed and reset commands |
| Accounts and configuration | `.env.example`, config loaders, test setup | Environment variable names, never values |
| Existing tests | Test directories, e2e configuration such as `playwright.config.*` | Layers covered, how to run a single test |
| Tools on this host | This session's tool list, CLIs on `PATH` | Each verification capability and the tool that provides it |

In a monorepo, discover these for each app the work item touches, and read the nested AGENTS.md or CLAUDE.md of each package it touches.

Then confirm by running. Never switch the user's checkout, and never write to data you did not create:

1. Run the checks that write no data once at the base SHA (the tip of `origin/<base>`): lint, typecheck, build, and unit tests that need no database. Run them in a separate worktree outside the repository (`git worktree add --detach <path> <base-sha>`, dependencies installed there), and remove it afterwards. Record the baseline: what passes, what fails, how long it takes. A check that already fails on the base is reported later as a baseline failure, never silently dropped.
2. Run migrate, seed, reset, the start command, or any suite that writes data only against services you started yourself, such as your own compose project (`docker compose -p <unique-name> up -d`), or after the user confirms in one question that the local configuration points only at local services. You cannot read `.env`, so you cannot see where a variable such as `DATABASE_URL` points.
3. Under that condition, start the app once and probe each verification tool against it, for example open the readiness URL with the browser-driving tool and read one heading. A tool counts as available only after a successful probe. Stop everything you started when the probes are done.
4. Never open `.env` files or secret stores. Read variable names from `.env.example` and configuration code.

Read [driving the app](references/driving-the-app.md) for the capability list, the dated tool table, and how to pick among several tools.

### 2. Write or confirm the profile

- **No profile yet:** write `docs/product-engineering/verification-profile.md` from the [profile template](templates/verification-profile.md). Mark each command you could not confirm as `unconfirmed`. Never invent a command.
- **Profile exists:** confirm it. Re-probe the tools. Re-check the commands when manifests, CI, compose or env-example files changed since the commit the profile records (`git log --oneline <recorded-sha>..HEAD -- <those paths>`). Update what changed and the confirmation line.

A new or changed profile lands in the repository with the work item's first PR slice: `implementing-plans` commits it there, with `spec.md` and the other planning files.

With a confirmed profile, G3 on this work item shrinks to the AC-to-check mapping plus any change to environments or human-eye items.

### 3. Draft the contract, one row per AC

Write the rows into the `## Verification` section of `spec.md` using the [contract template](templates/verification-contract.md):

`| AC | Check | Layer | Tool | Steps | Pass condition |`

- Every AC gets at least one row. An AC may have several, for example an `api` row for the denial case and an `e2e` row for the journey.
- Every AC a user can observe gets a row that exercises the running product: layer `e2e`, `api` or `cli`. A unit test alone never passes such an AC.
- Add an automated-test row when the behavior must stay protected in CI: regressions, permissions, money, data integrity. The agent still drives the product at stage 6.
- **Layer:** pick from the layer table in [layers](references/layers.md): the lowest layer that proves the AC, plus the running product for anything user-facing.
- **Tool:** capability first, then the tool the profile confirmed, for example "browser (Playwright MCP)". Write "user (human eye)" for rows the user certifies.
- **Steps:** numbered and concrete. Accounts by environment variable name. A unique value generated at run time, such as a title with a timestamp, so the observation proves this run and not a stale fixture.
- **Pass condition:** what someone watching would see, including the persisted side effect. "After reload, the list shows the title entered in step 2 exactly once." Never "works", "correct" or "as expected".
- A row whose tool or environment the profile has not confirmed is a gap for step 4, not a promise. At stage 6, a `blocked` row that is not an agreed human-eye row stops its slice before the PR opens, and the loop escalates: "the verification contract cannot run".

List the automated checks that must pass on the candidate (lint, typecheck, test suites) under the table.

An AC that cannot be observed ("the code is clean", "the flow is intuitive") cannot get a row. Propose an observable rewording, or a human-eye row, and have the user confirm it at G3.

### 4. Find harness gaps and propose Plan 0

| Gap | Effect if left | Proposal |
|---|---|---|
| No e2e setup | UI criteria are observed by driving only and never rerun in CI | Add the project's e2e runner with one smoke test of the main journey |
| No seed data | Every run builds data by hand, and runs differ | A seed script with known records |
| No test account, or no second account | Sign-in or permission criteria are `blocked` | Seeded accounts whose credentials come from environment variables |
| No single verify entry point | Every session rediscovers the commands | One `verify` script that runs lint, typecheck, tests and e2e in order |
| The app cannot start locally | Every row above `unit` is `blocked` | Make local start work: compose file, env example, documented steps |
| No browser-driving tool on the host | UI criteria are `blocked` or human eye | The user adds one to the host; code cannot close this gap |

Propose the code gaps as "Plan 0: verification harness" for the roadmap. `planning-implementation` schedules it first; without that skill, tell the user Plan 0 comes before the first plan. Plan 0 is an ordinary plan: it is implemented, verified and reviewed, and its CI or build changes make its PR `human` category. When the user declines a gap, agree at G3 what replaces its rows: a human-eye row, or an AC reworded to something the agent can observe. The contract says so. Never leave a row without a runnable check: it would stop every slice that carries it.

### 5. Agree who certifies what, and where

**Self-certify versus human eye.** Start from the spec's Done and review line, then propose this split and adjust it with the user. Never ask again what that line already answers:

| The agent self-certifies | A human eye certifies |
|---|---|
| Functional behavior, persistence, validation and error handling, permissions, API and CLI contracts, keyboard reachability, no console or network errors, layout intact at the agreed viewports | Visual taste and polish, copy tone, brand fit, whether a flow feels right, anything the spec states as a judgment |

A row agreed as needing a human eye is reported `blocked (human eye)` at stage 6 with a screenshot for the user. It puts its PR in the `human` review category, and the loop continues. Any other `blocked` row stops the slice before its PR opens and escalates as "the verification contract cannot run" (G3).

**Environments.** Local and ephemeral (a preview deployment, a disposable container) only. Production is never allowed, not even read-only. Name the production hosts, databases and accounts in the profile so the agent recognizes and refuses them. A shared staging environment is allowed only when the user names it; record their words.

**Destructive limits.** Agree the defaults or the user's tighter version:

- Data: reset only databases the agent created or seeded locally.
- Side effects: no real email, SMS, payments or webhooks; use a local mail catcher or the provider's test mode.
- Load: no load or stress tests against shared infrastructure.

Label every mock or sandbox in the contract with what it excludes.

### 6. Offer the "How to verify" pointer

Offer to add this to the project's AGENTS.md or CLAUDE.md, so later sessions reuse the profile:

```markdown
## How to verify
Before verifying any change, read `docs/product-engineering/verification-profile.md`: commands, how to start and seed the app, test accounts by env-var name, verification tools, and allowed environments. Never verify against production.
```

Add it only when the user says yes. It is an instruction-file change, so it goes in Plan 0 or its own PR slice, never in a feature slice, and that PR is `human` category. Record the answer under Harness gaps in the contract, so `planning-implementation` schedules it.

### 7. Get explicit agreement: G3

Present in one message: the contract table, the automated checks, the human-eye rows, environments and limits, mocks, and the Plan 0 proposal. Ask one question, through the host's structured-question tool when it has one: agree, change something, or discuss.

- Only an explicit yes is agreement. Record the date and the user's words on the `G3:` line of the Verification section.
- A reply that changes the contract is not yet agreement. Apply the changes and confirm again.
- When the user already delegated verification choices in their own words, quote them on the `G3:` line and present the contract as information.

## Tracks

| Track | G3 shape |
|---|---|
| Quick fix | No G3. The check goes in the PR body. When no profile exists, find the start command first, then ask only which environment is allowed, and the start command only when none was found |
| Bugfix | The repro becomes the first row. It must fail on the base for the reported reason before any fix; its pass condition is the expected behavior |
| Small change | The contract rows are part of the single G1 to G4 message |
| Feature | The full procedure |
| New app | There is no harness to discover, so design it: test runner, e2e tool, seed approach, the `verify` entry point, CI. Plan 1, the walking skeleton, builds it. Write the profile from the design and mark unbuilt parts `planned` |
| Refactor | Rows assert behavior preservation. Characterization tests for each invariant in the spec, and before-and-after journeys captured on the base SHA before the first edit. Pass condition: no observable difference |
| Spike | No G3. The spike is never merged; its findings record what was run and observed |

## Rules

- A layer without a tool stays unverified. Never substitute reading code for observing the product.
- Environment variable names only. A secret value never enters the profile, the spec, or a report.
- Production is never an allowed environment.
- This skill defines checks and confirms the harness runs. Writing product code and tests belongs to implementation, including Plan 0.
- Authorization to act comes from the user. Record their words; this skill grants nothing.

## Hand back

Return:

- The profile path, and whether it was created, updated or confirmed.
- The Verification section's location, with its rows counted by layer.
- The human-eye rows, the allowed environments, and the limits.
- The Plan 0 items, or "none".
- G3 status: agreed, with the user's words, or pending, with the open question.

## References

| Read | When |
|---|---|
| [driving the app](references/driving-the-app.md) | Discovering verification tools, filling the Tool column, choosing among several tools |
| [layers](references/layers.md) | Filling the Layer column, writing pass conditions, planning durable, regression and refactor checks |
| [profile template](templates/verification-profile.md) | Writing or confirming the project's verification profile |
| [contract template](templates/verification-contract.md) | Writing the Verification section of `spec.md` |
