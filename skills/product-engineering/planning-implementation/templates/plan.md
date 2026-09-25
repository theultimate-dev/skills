# Plan [NN]: [deliverable]

Status: planned

<!-- Status is planned, in progress or done. The plan's first slice sets in progress, and the PR that completes this plan's last slice sets done in that same PR. Plan files hold no PR links: live PR state is read from the host by branch name, never written here. Delete this comment. -->

Spec: `spec.md` · Roadmap: `roadmap.md`
Requirements: [R1, R3]
Acceptance criteria that pass in this plan: [AC1, AC2, AC4]
Depends on: [plan and slice, and the contract it consumes | none]
PR slices: [whole plan | per phase]
Branch: [type]/[work-item-slug]-[NN] [when the whole plan is one PR slice; per phase, each phase carries its own Branch: line instead]

## Outcome

[What exists once this plan has merged, in one or two sentences a user would recognize.]

## Boundaries

- In scope: [behavior and files]
- Out of scope: [non-goals from the spec, and work owned by other plans]
- Contracts produced or consumed: [API shape, schema or event, and where it is settled]
- Shared files and their owning slice: [path: slice]

## Phase 1: [name]

- Tasks:
  1. [Failing check first, when one can exist]
  2. [Change]
  3. [Change]
- Files: [paths or globs created or changed]
- ACs: [AC1 passes here; AC2 progress only | none: enabling purpose]
- Leaves the base working because: [additive only | behind flag `[name]`, off by default | other reason]
- PR slice: [own PR | shared with phase 2] · Predicted category: [`agent` | `human`: reason]
- Branch: [type]/[work-item-slug]-[NN]-p1 [per-phase slices only]

## Phase 2: [name]

[The same fields as phase 1.]

## Notes

- [YYYY-MM-DD] [slice]: [A routine deviation in one line: another file in the same module, a renamed helper, a reordered step, an extra test. `implementing-plans` writes these.]

## Changes after launch

- [YYYY-MM-DD] [What changed in this plan and why. A change to scope, approach or verification goes back to its gate first.]
