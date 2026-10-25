# Plan 02: Native placements in UX flows and handoffs

Status: done

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

- 2026-10-25 02: the branch stacks on 01's head, `d5a628f`, while PR #20 awaits review, as the roadmap allows.
- 2026-10-25 02: F-handoff holds T1 run 1's `visual-directions.md` from `e0ee116`, and T2's sketch, checks and notes from `146d3a3`, copied unchanged. Its README is the `harbor-menu-bar` brief, with the design state brought up to date and a "Decisions so far" section: direction A chosen and its departures accepted, and the device geometry as the owner's own figures. Without that section, no artifact records a selection. T2's `QUESTIONS.md` and `ANSWERS.md` are left out, so a trial's own `QUESTIONS.md` can't mix with them. The notes keep their stale "proposed" and "not viewed" lines and a link outside the folder, and every handoff flagged them.
- 2026-10-25 02: both baselines fail at `f401cae`. B-ux keeps "Narrow-screen behavior" and has no placements, so it fails U1. B4 fails P1: its note that other platforms show their own system font, and its symbol stand-ins, sit under "Behavior and content notes", outside "Selected design". B4 passes P2, so P2 alone is a regression guard. AC15's row still discriminates through P1.
- 2026-10-25 02: one sentence of the readiness reference was added after reading B4's output, before any candidate run: a face that can't be embedded renders through `system-ui`, "so reviewers on other platforms saw their own system font in its place". Without it, the skill didn't ask for P1's other-platform note.
- 2026-10-25 02: calibration ran before each real grade, on mutated copies of T-ux-3 and T4-3 with an unmutated control. The graders failed all five mutations and passed both controls. The handoff grader read "the owner's answer" as the notes' "user's answer" source in calibration, and applied that reading to every handoff, B4 included.
- 2026-10-25 02: all trials pass at `a6c8570`. U1 passes in T-ux 1 to 3, U2 in T-ux-web, and P1 and P2 in T4 1 to 3. Every transcript is clean or prints only text, such as a `sed` expression or a relative glob.

## Changes after launch
