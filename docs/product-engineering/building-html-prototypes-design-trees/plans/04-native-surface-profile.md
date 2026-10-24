# Plan 04: The native-surface profile

Status: planned

Spec: `spec.md` · Roadmap: `roadmap.md`
Requirements: R11, R12, R13, R14, R15
Acceptance criteria that pass in this plan: AC14, AC15, AC16, AC17, AC18
Depends on: 02 (`interaction-harness.html` in a 320 px frame, which AC16 uses); 01 (the staging layout)
PR slices: whole plan
Branch: feat/building-html-prototypes-native-surfaces

## Outcome

A prototype of a native surface (a menu-bar panel, desktop window, phone widget or watch face) is drawn at a stated scale and checked at device scale factors 1 and 2. Its geometry comes from sourced tokens. Each scene scrolls inside its own container while the page around it reflows at 320 px. System type and symbols are recorded as fidelity limits, and the platform's settings are switched from a control outside the scenes.

## Boundaries

- In scope: R11 to R15; `references/native-surface-profile.md`; the fixture for AC16.
- Out of scope: the native-surface variant of `exploring-visual-directions` (#10); tables of device geometry (spec non-goal).
- Contracts consumed: the harness API (02) and the staging layout (01).
- Contracts produced: the profile that #10's platform frame hands over to.
- Shared files and their owning slice: as in the roadmap.

## Phase 1: The native-surface profile

- Tasks:
  1. Check first: `evaluations/product-design/fixtures/native-scene/`, a page with an 800 CSS px scene. Fill the harness to load it in a 320 px frame. Confirm the check shows `FAIL` on a variant where the scene widens the page, then `PASS no page scroll at 320` and `PASS scene scrolls in its container` on the profile's pattern.
  2. `references/native-surface-profile.md`:
     - Scale mapping (1 CSS px = 1 pt as the example), and checks at device scale factors 1 and 2.
     - Geometry tokens with sources: display size in points, system bar heights, safe areas, hardware cut-outs.
     - Reflow: the page around the scenes reflows at 320 px, and each scene scrolls in its own container. Cite WCAG 2.2 SC 1.4.10's two-dimensional layout exception.
     - Type and symbols: `system-ui` and drawn stand-ins, recorded as fidelity limits.
     - Settings: a control in the page around the scenes, never inside one, that starts from `prefers-color-scheme`, `prefers-contrast`, `prefers-reduced-transparency` and `prefers-reduced-motion`, and forces each setting where its media feature is unavailable. Cite MDN for `prefers-reduced-transparency` being experimental.
  3. `references/interaction-and-verification.md` step 5: fixed-scale scenes follow the profile in place of the 320 px check.
  4. `references/offline-artifact-contract.md` "Fonts and imagery": point to the profile for platform system fonts.
  5. `SKILL.md`: one sentence routing native surfaces to the profile.
  6. `templates/prototype-notes.md`: the scale mapping, a geometry-sources list, and type and symbol fidelity limits.
  7. `skills/product-design/CHANGELOG.md` `[Unreleased]` Added; the root `CHANGELOG.md` evaluations line.
  8. Run the AC rows: the cold reads for AC14, AC15, AC17 and AC18, and staged AC16.
- Files: `skills/product-design/building-html-prototypes/{SKILL.md, references/native-surface-profile.md (new), references/interaction-and-verification.md, references/offline-artifact-contract.md, templates/prototype-notes.md}`, `evaluations/product-design/**`, `skills/product-design/CHANGELOG.md`, `CHANGELOG.md`, this plan file.
- ACs: AC14, AC15, AC16, AC17 and AC18 pass here.
- Leaves the base working because: it is additive, and responsive pages keep the 320 px check.
- PR slice: own PR, about 160 changed lines. Predicted category: `human`, because the user reviews every PR.

## Notes

## Changes after launch
