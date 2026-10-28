# Plan 02: set up or adopt a design home

Status: planned

Spec: `spec.md` · Roadmap: `roadmap.md`
Requirements: R1, R2, R3, R4, R5, R6
Acceptance criteria that pass in this plan: AC1, AC2, AC3, AC4, AC5, AC6, AC7
Depends on: 01-p3, which provides the render check and its `moved=` parameter for adoption
PR slices: whole plan
Branch: feat/curating-design-systems-02

## Outcome

The skill inspects a project, proposes a design-home layout with its reasons, and creates it once you agree. It adopts an existing design folder by a mapping you approve. It writes the home's README, and records the layout's reasons in the project's decision log when there is one.

## Boundaries

- In scope:
  - the setup and adoption sections of `SKILL.md`;
  - a setup-and-adoption reference;
  - the README template for the home;
  - the root `index.html` that links every view;
  - fixtures F-new and F-adopt, and the T-setup, T-adopt and T-readme task texts with their fixed answers.
- Out of scope: graduation (plan 03); routing (plan 04); `product-context`'s design layer (spec non-goal).
- Contracts consumed: the check inputs, result lines and render baseline from plan 01.
- Contracts produced:
  - **Home layout:** the default from the spec's Assumptions, plus the root `index.html`.
  - **README template sections:** layout, the four rules, adding a platform, adding a view, graduated directions, and open questions including token export.
- Shared files and their owning slice: the skill's `SKILL.md`, the changelog and the evaluations README, each extended here.

## Phase 1: set up or adopt a design home

- Tasks:
  1. Failing check first: add F-new and F-adopt and the trial task texts to the evaluations README. Then run one T-setup phase 1 against the plan-01 skill and record that it doesn't propose a layout.
  2. `SKILL.md` gains the setup and adoption steps:
     - inspect: design folders, token and theme files, the code's apps, instructions, and the decision log;
     - propose: the layout, where the home sits, the recommendation and its reasons, the project's rules on where files live, and any conflict, which it asks about;
     - create the home only on your explicit yes.

     Adoption gains its own steps:
     - map every existing file to its place;
     - take the render baseline before any move;
     - move files and rewrite their relative paths only once you agree;
     - run the three checks, using `moved=` for the render check;
     - read the code's theme files as a source of values, and never move, edit or link them.
  3. Write `references/setting-up-and-adopting.md`, covering:
     - naming platforms after the code's apps, or after the brief's surfaces when there is no code;
     - when a platform has a platform stylesheet;
     - where the home sits;
     - examples that describe parent paths in prose.
  4. Write `templates/design-home-readme.md` with the six sections. "Adding a view" says which stylesheets a view links, and climbs to them in words.
  5. The layout's reasons: a record in the project's decision log (through `decision-records` when installed), linked from the README, or the README itself when there is no log.
  6. Run T-setup ×3, T-adopt and T-readme, and the AC2, AC6 and AC7 cold reads, as the spec's Verification section describes.
  7. Add a changelog entry and widen the skill's `description`.
- Files: `skills/product-design/curating-design-systems/{SKILL.md,references/setting-up-and-adopting.md,templates/design-home-readme.md}`, `evaluations/product-design/fixtures/{harbor-home-new,harbor-home-adopt}/**`, `evaluations/product-design/README.md`, `skills/product-design/CHANGELOG.md`.
- ACs: AC1, AC2, AC3, AC4, AC5, AC6 and AC7 pass here. AC15: progress only.
- Leaves the base working because: it is additive to the skill.
- PR slice: own PR · Predicted category: `human`: you review every PR (G1)

## Notes

## Changes after launch
