# Plan 02: Scripted checks for headless verification

Status: in progress

Spec: `spec.md` · Roadmap: `roadmap.md`
Requirements: R7, R8, R9, R10
Acceptance criteria that pass in this plan: AC9, AC10, AC11, AC12, AC13
Depends on: 01, which produces the staging layout and result format in `references/interaction-and-verification.md`
PR slices: whole plan
Branch: feat/building-html-prototypes-scripted-checks

## Outcome

When an agent has no browser-driving tool, it can still exercise a prototype's stateful interactions with a copyable harness page and read PASS or FAIL from a DOM dump. It can also inspect long pages in fixed-size slices instead of one tall screenshot. Each check goes into the notes by name.

## Boundaries

- In scope: R7 to R10; `templates/interaction-harness.html`; `templates/page-slices.html`; fixtures for AC9 and AC12.
- Out of scope: the hosted step (plan 03), which consumes the harness; native surfaces (plan 04), which consume it too.
- Contracts consumed: the staging layout and result format from 01.
- Contracts produced: the harness API that plans 03 and 04 use in their checks. The agent fills in named checks, and the harness loads `/a/b/<page>` in a same-origin frame that can be any width. Settled in this plan's template.
- Shared files and their owning slice: `templates/interaction-harness.html`: 02.

## Phase 1: The interaction harness and page slices

- Tasks:
  1. Fixtures first:
     - `evaluations/product-design/fixtures/panel-bug/`: a control click that also reaches a document click-outside handler.
     - `panel-fixed/`: the same panel with the handler fixed.
     - `long-page/`: 4,000 CSS px tall, with bands labeled 0, 1000, 2000 and 3000.
     - The rerun commands in `evaluations/product-design/README.md`.
  2. `templates/interaction-harness.html`: a same-origin frame of configurable width; helpers for pointer and keyboard events, waiting for timers, and assertions on the DOM, focus and ARIA; the result format. Confirm `FAIL panel stays open after one click` on `panel-bug` before `DONE 6/6` on `panel-fixed`.
  3. `templates/page-slices.html`: shows `?src=` in a frame sized by `?width=` and `?height=`, scrolled to `?offset=`, and writes `PASS scrolled <n>`.
  4. `references/scripted-checks.md`:
     - The harness recipe, including why: `file://` origins are opaque (MDN).
     - When a scripted check is required (R8).
     - The long-page recipe.
     - A narrow viewport as a frame, because a headless browser may keep a minimum window width.
     - Naming checks for the notes.
  5. `references/interaction-and-verification.md`: in steps 3 and 4, a scripted check for each stateful interaction when no driver can exercise it; replace "no particular automation library is required" with a pointer to `scripted-checks.md`.
  6. `SKILL.md` "Verify and deliver": one sentence on scripted checks without a driver.
  7. `templates/prototype-notes.md`: a row form for each named check (`Scripted: <name>` or `Driven: <name>`), with an example.
  8. `skills/product-design/CHANGELOG.md` `[Unreleased]` Added; the root `CHANGELOG.md` evaluations line.
  9. Run the AC rows: staged AC9 and AC12, the cold reads for AC10 and AC11, and the template read for AC13.
- Files: `skills/product-design/building-html-prototypes/{SKILL.md, references/scripted-checks.md (new), references/interaction-and-verification.md, templates/interaction-harness.html (new), templates/page-slices.html (new), templates/prototype-notes.md}`, `skills/product-design/CHANGELOG.md`, `CHANGELOG.md`, `evaluations/product-design/**`, this plan file.
- ACs: AC9, AC10, AC11, AC12 and AC13 pass here.
- Leaves the base working because: it is additive, and existing verification steps keep working with a browser-driving tool.
- PR slice: own PR, about 370 changed lines including about 90 lines of fixtures. Predicted category: `human`, because the user reviews every PR.

## Notes

## Changes after launch
