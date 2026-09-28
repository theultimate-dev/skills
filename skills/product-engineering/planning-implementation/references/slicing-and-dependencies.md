# Slicing and dependencies

## Bound work by a checkable outcome

A plan fits one coherent implementation and review context. "Build the backend" hides its contracts. One plan per function creates coordination overhead with no review benefit. Use the smallest useful outcome with an explicit evidence boundary: the ACs it makes pass.

| Unit | Signals |
|---|---|
| Plan | A capability the user would recognize, or a prerequisite that unblocks one. It owns its own Rs and ACs. It fits in one line of release notes |
| Phase | One PR's worth of change. It leaves the base branch building, tested and releasable. It is usually one of: a contract (types, schema, API stub), the core behavior with its tests, the UI on top, the flag flip |

Prefer vertical slices. A thin end-to-end path that makes one AC observable beats a horizontal layer that makes nothing observable. Cut a horizontal slice only to isolate a `human` concern (a migration, a new dependency, a CI change) or a contract that other slices consume.

## What must be settled before a slice starts

- The ACs it makes pass, and what it excludes.
- The agreed approach, and every interface the slice changes.
- Its starting point: a fresh branch from the base, or a stacked parent. Its owned files and its dependencies.
- The Verification rows it must satisfy, their real and mocked boundaries, and the environment they need.
- The escalation triggers.

The first slice can be ready while later ones stay provisional. A roadmap row is not permission to start every slice. Before starting a dependent slice, confirm on the host, not from the roadmap, that its producer actually merged, or that its PR is open, `human`, and not itself stacked.

## Choosing the PR slice

| Signal | Slice |
|---|---|
| The whole plan is one concern, under about 400 changed lines, one category | The whole plan |
| One phase touches a `human` area and the rest does not | Per phase. The `human` phase ships alone and early |
| The plan exceeds one sitting | Per phase |
| A phase cannot leave the base working on its own | Re-cut the phases with a flag or expand-and-contract. Never fuse them into one large PR |
| Generated code or lockfile churn dominates the diff | Generate in its own slice, or leave generated files out of the size estimate |
| Two slices would edit the same shared file | Give the file to one slice and make the other depend on it |

Around 400 changed lines is where review quality drops. It is a signal to split, not a quota.

### Feature flags

- Put incomplete user-facing work behind a flag that is off by default. The code merges, users see nothing, and the base stays releasable.
- Verification runs with the flag on in the verification environment.
- Turning the flag on, or removing it, is its own small slice at the end. With the UI default, that slice is `human`, and it is where the human judges the visual result: its PR body points to the screenshots and the verification steps.
- Use the project's flag system. Without one, read a config value or environment variable in one place. Adding a flag library is a new dependency, so that slice is `human`.

### Expand and contract

Schema and API changes that would break callers ship in steps. Each step leaves the base working and deployable.

1. Expand: add the new column, field or endpoint, additive only. `human`: a migration.
2. Write both, read the old. `agent`.
3. Backfill the new from the old. `human`: a backfill.
4. Switch reads to the new, behind a flag when users can see the change. `agent`.
5. Contract: remove the old column or endpoint once every caller has moved. `human`: a migration or a breaking change.

## Dependencies and contracts

Declare every producer and consumer. Agents must not discover conflicting assumptions at integration time.

An existing save API, for example, can let a persistence repair and a keyboard-feedback change proceed in parallel once the response and error semantics are settled. If both slices change the response shape, settle that shape in the first slice and make the second depend on it.

Keep shared schemas, dependency manifests, lockfiles, migrations, generated artifacts and common fixtures under one owning slice. Every other slice consumes them.

## Parallelism and worktrees

- Two slices run in parallel only when their files are disjoint and neither consumes the other's contract.
- Give each parallel slice its own worktree: `git worktree add <path outside the repository> -b <branch> origin/<base>`. Use the host's own isolation feature when it has one.
- Each worker edits only its owned files and preserves everyone else's changes.
- Isolated worktrees prevent file collisions, not semantic conflicts. After each merge, dependent branches update from the new base and rerun their affected checks: by merging the base into them, or by a rebase when the contract authorizes force-push.
- Without parallel agents or worktrees, run the slices in dependency order. The plan stays the same.

## Tests are designed with the plan

- Every AC already has a Verification row. Map it to the phase that makes it pass, and do not duplicate the same trivial assertion at every layer.
- A regression plan names the failing behavior and writes the failing check before the fix.
- Ask what plausible wrong implementation would still pass the planned checks. Ownership isolation, for example, needs a second user and a denied operation, not only a happy-path save.
- When tests and code are written by different agents, settle the observable contract and the fixture boundaries first. Test authors work from the requirements and the public behavior; they do not mirror implementation internals.

## Integration

Merges land on the base branch one slice at a time, so integration is continuous. After each merge, dependents update from the new base, as above, and rerun their affected checks. The slice that completes a journey spanning several plans verifies the whole journey. Resolve a conflict by the intent of both sides, never by whichever version merges cleanly.

## Replanning

Replan only when new evidence changes a contract, reveals hidden coupling, or invalidates a dependency, and only through the "After launch" table in the skill. Record why, update the affected plan files, and revisit only the user agreements that actually changed. Do not broaden scope to clean up unrelated code found while planning: note it as a follow-up for the user.

## Worked examples

### Feature: saved searches in a web app

Spec: R1 save a search, R2 list and rerun saved searches, R3 delete one; AC1 to AC5. Approach: a `saved_searches` table, REST endpoints, a panel on the search page.

| Plan | Phases | PR slices | Predicted category | Depends on |
|---|---|---|---|---|
| `plans/01-storage-and-api.md` | p1 migration adding `saved_searches`; p2 repository, endpoints, tests | per phase | p1 `human`: migration; p2 `human`: authorization (owner checks on every endpoint) | none |
| `plans/02-saved-searches-panel.md` | p1 panel behind `savedSearches`, off by default; p2 flag on | per phase | p1 `agent`: nothing user-visible; p2 `human`: UI | 01-p2 (the endpoint contract) |

- AC1 to AC3 at the API level pass in 01-p2. The UI journeys AC4 and AC5 pass in 02-p1, verified with the flag on. 02-p2 re-runs them with the flag's default on.
- 01-p1 opens first: small, `human`, and its review runs while 01-p2 is built. 01-p2 stacks on 01-p1 while it awaits review.
- Critical path: 01-p1, 01-p2, 02-p1, 02-p2. Three of the four slices are `human`: the migration, the owner checks, and the UI switch. Each is small, and each review runs while the next slice is built.

### Refactor: split a 2,000-line module

- Plan 01, phase 1: characterization tests pinning the current behavior, and captured before/after journeys. `agent`: tests only, nothing weakened.
- Phases 2 to 5: move one responsibility each, with the characterization tests unchanged and passing. `agent` while the invariants hold and no public boundary moves.
- A phase that must move a public export is `human`: it is a breaking contract change. Isolate it as its own phase.

### New app

- Plan 1, walking skeleton: the smallest runnable app, CI that builds, lints and tests it, the verify entry point from the verification profile, and the decision log started with the stack decision. `human`: new dependencies and CI configuration.
- Plans 2 onward: one capability each, vertical slices, `agent` wherever the defaults allow.
