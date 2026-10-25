# Plan 02: Native placements in UX flows and handoffs

Status: planned

Spec: `spec.md` · Roadmap: `roadmap.md`
Requirements: R12, R13, R14
Acceptance criteria that pass in this plan: AC14, AC15, AC16
Depends on: 01. It consumes the platform frame contract and the template markers. F-handoff is frozen from 01's passing T1 run 1 and T2 outputs
PR slices: whole plan
Branch: feat/product-design-native-placements

## Outcome

For a native surface, a UX specification describes placements in place of narrow-screen behavior. The implementation handoff carries forward:

- the placements and scale;
- the platform frame;
- the system type and symbol limits.

The coordinator's Converge row names placements. Responsive pages keep their narrow-screen behavior and responsive rules.

## Boundaries

- In scope: R12 to R14.
  - `designing-ux-flows`: `SKILL.md`, `references/flows-and-states.md` and `templates/ux-specification.md`.
  - `preparing-implementation-handoffs`: `SKILL.md`, `references/readiness-and-traceability.md` and `templates/implementation-handoff.md`.
  - `guiding-product-discovery/references/workflow.md`.
  - The F-handoff fixture and its trials.
- Out of scope: `exploring-visual-directions` and `building-html-prototypes` (01), the release, and the spec's non-goals.
- Contracts consumed: the platform frame and the marker convention from 01.
- Shared files and their owning slice: `skills/product-design/CHANGELOG.md` and `evaluations/product-design/README.md`, 01 then 02.

## Phase 1: Placements downstream

- Tasks:
  1. Failing check first.
     - Freeze F-handoff under `evaluations/product-design/fixtures/harbor-handoff-inputs/` from 01's T1 run 1 and T2 outputs.
     - Extend the evaluations README with T-ux, T-ux-web and T4.
     - Run baselines B-ux and B4 on f401cae. Each must fail its native criteria.
  2. `designing-ux-flows`:
     - `SKILL.md`: placements for a native surface, next to narrow layouts.
     - `references/flows-and-states.md`: the responsive paragraph gains its native counterpart.
     - `templates/ux-specification.md`: "Narrow-screen behavior (responsive page)" and "Placements (native surface)".
     - A changelog entry.
  3. `preparing-implementation-handoffs`:
     - `SKILL.md`: placements and scale, the platform frame, and the type and symbol limits, in place of responsive rules for a native surface.
     - `references/readiness-and-traceability.md`: the same, for the readiness check.
     - `templates/implementation-handoff.md`: the marked lines.
     - A changelog entry.
  4. `guiding-product-discovery/references/workflow.md`: the Converge row reads "responsive behavior or, for a native surface, placements". A changelog entry.
  5. Run the trials and the AC rows, then set this plan's `Status: done` before the PR opens.
- Files:
  - `skills/product-design/{designing-ux-flows, preparing-implementation-handoffs}/**`
  - `skills/product-design/guiding-product-discovery/references/workflow.md`
  - `evaluations/product-design/**`
  - `skills/product-design/CHANGELOG.md`
  - this plan file
- ACs: AC14, AC15 and AC16 pass here.
- Leaves the base working because: it's additive, and responsive lines only gain markers.
- PR slice: own PR, about 250 changed lines. Predicted category: `human`, because the user reviews every PR.

## Notes

## Changes after launch
