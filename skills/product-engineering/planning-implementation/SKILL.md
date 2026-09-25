---
name: planning-implementation
description: "Plans the implementation of an agreed spec.md at stage 4 of the product-engineering loop and runs gate G4, whose approval launches autonomous work. Decomposes the work item into plans and phases, chooses PR slices that each stay green and releasable, sets dependencies and parallel work, predicts each slice's human or agent review category, maps acceptance criteria to phases, and drafts the autonomy contract after detecting the default branch, branch protection and deploy-on-merge and asking the user whether the agent may merge. Writes roadmap.md and plans/NN-slug.md, or an inline Plan section in spec.md for a small change. Use when an agreed spec.md needs PR slices: break this spec into PRs, plan the PR slices, write this work item's roadmap. Not for product roadmaps."
license: MIT
---

# Planning implementation

Turn an agreed `spec.md` into the plan the autonomous loop runs on, and get the user's approval to launch it. The plan names the plans, their phases, and the slices that each become one pull request (merge request), called PR slices. The output is `roadmap.md` and one `plans/NN-slug.md` per plan, in `docs/product-engineering/<work-item-slug>/`. The user's approval of the roadmap is gate G4. This skill plans. It does not implement, commit, push or merge.

## Check the inputs

1. Read `spec.md`. Its status line must start with `Status: agreed`, as in `Status: agreed (G1, 2026-09-25: "Agreed")` or, on a bugfix, `Status: agreed (G1 skipped: repro reproduced at a1b2c3d)`, and its Approach and Verification sections must be filled, which means G1 to G3 are done. On a track that batches the gates into one message, the spec may still say `draft`: that message confirms every gate at once. When a section is missing, run the skill for that gate first: `specifying-work-items` (G1), `brainstorming-solutions` (G2), `defining-verification` (G3). When that skill is not installed, get the missing agreement from the user in one message.
2. Read `docs/product-engineering/verification-profile.md`, the project instructions (AGENTS.md, CLAUDE.md, including any "Pull request policy" section), CODEOWNERS, the CI configuration, recent history, and the code the Approach touches.
3. Confirm the track. A small change gets the inline plan below. A feature, new app or refactor gets a roadmap, and so does a bugfix that needs more than one PR slice. When a small change needs more than one PR slice, it is a feature: say so and plan it as one. Never downgrade a track silently.
4. Never fill a consequential gap with a planning assumption. A missing behavior decision goes back to G1, a missing approach decision to G2.

Spikes are not planned here. They run on a timeboxed branch that is never merged. A quick fix and a bugfix with one PR slice are not planned here either. Their autonomy contract comes from the user's words in the request or their answer to the intake question. A bugfix records it in the `## Plan` section of its short `spec.md`, which holds only that contract. A quick fix has no spec: its contract lives in the PR body under `## Autonomy contract`, and it counts only while the body's edit history shows no editor other than the authorizing account.

## 1. Decompose into plans and phases

- A **plan** is a coherent deliverable: a capability the user would recognize, or a prerequisite that unblocks one. It owns a set of requirements and ACs.
- A **phase** is a reviewable increment inside a plan that leaves the base branch working: it builds, its tests pass, and users see nothing half-finished.
- Number plans in delivery order: `plans/01-saved-searches.md`. Most plans have one to four phases. Split a plan that needs more than five phases.

| Situation | What comes first |
|---|---|
| `defining-verification` recorded harness gaps | Plan 0, `plans/00-verification-harness.md`, closes them. Every later AC depends on it |
| New app | Plan 1 is a walking skeleton: the smallest runnable app, CI that builds, lints and tests it, and the verify entry point. It also carries the decision log with the stack decision. Predict it `human` |
| Refactor or migration | The first phase captures characterization tests and before/after journeys before any edit. Later phases are small mechanical steps |

## 2. Choose the PR slice for each plan

A PR slice is the whole plan or one phase of it. Every slice passes four tests:

| Test | Passes when |
|---|---|
| One sitting | A reviewer reads the diff in one sitting: under about 400 changed lines, not counting lockfiles, snapshots and generated code |
| One concern | The slice does one thing, and its title needs no "and" |
| Independently verifiable | Its ACs, or its stated enabling purpose, can be observed on its own head |
| Green and releasable | Merging it and stopping there leaves the product working |

Slice per phase when the whole plan fails "one sitting" or "one concern", or when one phase is `human` and the others are not. Otherwise slice per plan. Put incomplete user-facing work behind a feature flag that is off by default; turning the flag on or removing it is its own later slice. Read [slicing and dependencies](references/slicing-and-dependencies.md) for the signals, expand-and-contract, and worked examples.

## 3. Set dependencies, order and parallelism

1. Record every dependency: which slice produces a contract (an API shape, a schema, an event) that another slice consumes. Settle a shared contract before either side starts.
2. Give each shared file one owning slice: schemas, migrations, lockfiles, generated code, shared fixtures, route tables.
3. Mark slices parallel only when their files are disjoint and neither consumes the other's contract. Parallel slices run in isolated worktrees (git worktree, or the host's isolation feature) with parallel agents or subagents, when the host has them. Without them, run the slices one after another.
4. Name the critical path: the longest chain of dependent slices.
5. A dependent slice may stack on a parent slice that awaits human review, one level deep. A deeper chain waits.

## 4. Predict the review category

Predict `human` or `agent` for every slice from the files and behavior it will touch. `shipping-pull-requests` recomputes the category from the actual diff, and the category can only escalate.

Precedence, strongest first: host protections (branch rules, CODEOWNERS), the "Pull request policy" section of the project instructions, the autonomy contract (it tightens freely and loosens only in the user's own words), then these defaults. A slice is `human` when it touches:

- authentication or authorization, crypto, secrets, payments, personal data;
- schema changes, migrations, backfills;
- breaking public API or contract changes;
- new or major-bumped dependencies;
- CI/CD, infrastructure, build or permission configuration;
- policy or instruction files (AGENTS.md, CLAUDE.md, CODEOWNERS);
- user-visible UI or visual changes, a default the user can flip in the autonomy contract.

Conditions that appear during the loop always make a PR `human`:

- deleted tests or weakened assertions;
- an AC that was not observed;
- a waived blocking finding;
- a scope change;
- a self-review verdict;
- blocking findings that survive 3 full review rounds;
- an AC agreed as needing a human eye, reported `blocked (human eye)` with a screenshot.

Predict `human` now for a slice whose ACs include a human-eye row. Everything else inside the approved scope is `agent`. When the base branch requires approving reviews, every slice is `human`, because the agent cannot approve its own PR.

Schedule `human` slices early, keep them small, and decouple them: a migration alone, a dependency added alone, a UI change behind a flag. A slice waiting for a reviewer then stays off the critical path.

## 5. Map acceptance criteria to phases

For every Verification row in `spec.md`, name the one phase whose PR makes that AC pass. Earlier phases that move it forward list it as "progress only". An AC with no phase is a planning gap: add a phase, or return to G1 when the AC itself is wrong. A phase with no AC states its enabling purpose: a harness, a contract, an invariant held. An AC behind a flag passes with the flag on in the verification environment.

## 6. Draft the autonomy contract

Detect the facts, then ask. Read [autonomy contract](references/autonomy-contract.md) for the commands, the deploy signals and examples of recorded answers.

1. Detect the host from the git remote, the default branch, branch protection (required approving reviews, code-owner review, required checks, merge queue), the allowed merge methods, and whether a merge deploys. A merge deploys when CI runs a job on a push to the base branch that deploys or releases, or a hosting platform deploys from that branch. When you cannot rule deployment out, record `yes`. A new app without a repository has no remote yet: ask the repository question below, and detect the rest once the repository exists.
2. Ask in one message, through the host's structured-question tool when it has one, about every field that is not detected. Never assume an answer. The contract has these fields, in this order:

   | Field | Ask, or record |
   |---|---|
   | Commit and push | May the agent commit and push? |
   | Force-push own PR branches after a rebase | May the agent force-push its own PR branches after a rebase, only as `git push --force-with-lease=<branch>:<last-pushed-sha>`? Push does not imply force-push. Without it, the agent updates a PR branch by merging the base into it |
   | Open PRs | May the agent open PRs? |
   | Open issues (deferred should-fix findings and follow-ups) | May the agent open tracked issues for them? |
   | Merge `agent`-category PRs | May the agent merge them? Only words that mention merging count: "go ahead" approves the roadmap, not merging |
   | Merge method | Which method? Recommend the project's habit |
   | Base branch | Not asked: a detected fact, not a permission. Ask which base only when the project integrates into another branch |
   | Deploy-on-merge detected | Record yes or no. When yes, ask: may the agent make a merge that deploys to the named environment? |
   | Human-review categories | Which changes must always wait for the user, beyond the project policy? UI and visual changes stay `human` unless the user releases them in their own words |
   | Who merges a `human` PR after approval | The user, or the agent when the user tells it to? |
   | Scope | Not asked: this work item's PR slices, into the base |
   | Stop and ask when | When else should the agent stop and ask, beyond the escalation triggers? |

   A new app without a repository adds one question: "New app without a repository: may I create it (host, owner/name, visibility) and push an initial commit, or will you?"
3. Record each answer verbatim, in quotes, with the date. An unanswered field is `not authorized`. Use the narrowest reading of the user's words: a slice not clearly covered stays `human`. When the user already answered for this work item, in this session or on `spec.md`'s Done and review line, quote that answer and where it was given instead of asking again. Only an answer given for this work item counts. When the project instructions hold the user's standing autonomy defaults, quote them and ask only "Same autonomy as <date>?".
4. When branch protection requires approving reviews, say plainly that the agent cannot merge any PR into that base and that every PR will wait for a reviewer. Changing that rule is the user's decision, never the agent's action.

## 7. Present the roadmap (G4)

1. Write `roadmap.md` from the [roadmap template](templates/roadmap.md) and one file per plan from the [plan template](templates/plan.md), each plan with `Status: planned` and one `Branch:` line per PR slice. Plan files hold no PR links: live PR state is read from the host by branch name.
2. Present in one message: the plans table, each PR slice with its predicted category and reason, the order, what runs in parallel, the critical path, and the autonomy contract with the detected facts and the questions from step 6. When the roadmap has `human` slices and the host can schedule tasks, offer to recheck the PRs awaiting review on a schedule and resume the loop when they merge.
3. G4 is the user's explicit approval of that roadmap. An edit request is not approval: revise and present again. Approval of an earlier gate is not G4.
4. On approval, record the answers in the contract and launch the first slices. `running-implementation-loops` drives the loop when it is installed; otherwise take each slice through `implementing-plans`, `verifying-implementation`, `reviewing-code-changes` and `shipping-pull-requests` in that order.

The planning files land with the PR slices, so no two open PRs write the same file. `implementing-plans` commits them: the work item's first slice commits `spec.md`, `roadmap.md` when there is one, a new or changed `docs/product-engineering/verification-profile.md`, the plan file when there is one, and any decision record written at G2; each later plan's first slice commits its own plan file; a plan's final slice sets `Status: done` in its plan file within the same PR. Nothing is committed after a PR opens only to record it. `roadmap.md` stays structural: live PR state is read from the host by branch name, never written into files. When the user accepted the AGENTS.md or CLAUDE.md "How to verify" pointer at G3, schedule it in Plan 0 or its own PR slice: it is an instruction-file change, so `human`.

## Small-change track

No `roadmap.md` and no plan files. Write the plan into the `## Plan` section of `spec.md` and present it with G1 to G4 in one message. The autonomy contract is a block of that message with every field of the roadmap's contract, recorded in the same section. Ask its questions as in section 6:

```
## Plan
PR slice: one PR · Predicted category: agent | human: [reason] · Branch: [type]/[work-item-slug]
Tasks:
1. [Failing check first, when one can exist]
2. [Change]
Files: [paths]
ACs: AC1, AC2 (all pass in this PR)
Notes:
- [YYYY-MM-DD] [a routine deviation, in one line]

Autonomy contract ([date]; the user's words, quoted; "not authorized" when unanswered):
- Commit and push: "[words]" | not authorized
- Force-push own PR branches after a rebase: "[words]" | not authorized
- Open PRs: "[words]" | not authorized
- Open issues (deferred should-fix findings and follow-ups): "[words]" | not authorized
- Merge `agent`-category PRs: "[words]" | not authorized
- Merge method: [squash | merge | rebase]: "[words]" | not authorized
- Base branch: [branch] (a detected fact, not a permission)
- Deploy-on-merge detected: [yes | no]. Merges that deploy to [environment]: "[words]" | not authorized
- Human-review categories: the project policy and the skill defaults, plus "[words]". UI and visual changes: [`human` | `agent` only for what these words cover: "[words]"]
- Who merges a `human` PR after approval: [the user | the agent when the user tells it to: "[words]"]
- Scope: this work item's PR slices, into [base]
- Stop and ask when: the escalation triggers, plus "[words]"
```

## After launch

The roadmap is fixed at G4. A plan changes after launch only this way:

| What happened | Do |
|---|---|
| A spec contradiction or scope growth | Stop and return to G1 for the affected part |
| The chosen approach proves infeasible | Stop and return to G2 |
| The verification contract cannot run | Stop and return to G3 |
| An action goes beyond the autonomy contract | Stop and ask the user |
| Blocking findings survive 3 full review rounds | The PR becomes `human`; the plan itself stays |
| Phases split or merge, files or tasks differ, while ACs, categories and dependencies stay the same | Update the plan file in the current PR and add a dated line to its "Changes after launch" section saying why |

After the user resolves an escalation, update the affected plan files and add a dated entry to the roadmap's Decisions section quoting the user. Never rewrite the autonomy contract: append the user's new words with the date. Append in the main checkout, and `implementing-plans` commits it with the next PR slice; until that merges, briefs and merge checks read the contract from the main checkout.

## Report

Return the files written, the slices that can start now, what runs in parallel, the slices predicted `human` and why, and the recorded contract, including every action that is not authorized.

## References

| Read | When |
|---|---|
| [slicing and dependencies](references/slicing-and-dependencies.md) | Sizing plans and phases, choosing PR slices, flags and expand-and-contract, contracts and shared files, worktrees, worked examples |
| [autonomy contract](references/autonomy-contract.md) | Detecting the default branch, branch protection, merge methods and deploy-on-merge; asking the questions; recording answers |
| [roadmap template](templates/roadmap.md) | Writing `roadmap.md` at G4 |
| [plan template](templates/plan.md) | Writing each `plans/NN-slug.md` |
