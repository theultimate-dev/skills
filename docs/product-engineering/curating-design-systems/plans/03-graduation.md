# Plan 03: graduate a chosen direction into the design home

Status: planned

Spec: `spec.md` · Roadmap: `roadmap.md`
Requirements: R8, R9, R10, R11, R12
Acceptance criteria that pass in this plan: AC8, AC9, AC10, AC11, AC12, AC15
Depends on: 02, for the home layout and the README template's "graduated directions" section; 01-p2, for the token check
PR slices: per phase

## Outcome

After you select or combine a direction, the skill moves its tokens into the foundations by role, with their appearance variants. It turns repeated parts into shared components, and puts the view's own surfaces in the view's stylesheet. It records each direction's reason in the comparison and checks the tree. It stops and asks when an appearance is missing, or when a role conflicts with the foundations.

## Boundaries

- In scope:
  - the graduation section of `SKILL.md` and a graduation reference;
  - fixtures F-grad, F-light (derived) and F-conflict;
  - the T-grad, T-light and T-conflict task texts.
- Out of scope: refining pages (`building-html-prototypes`); exporting tokens to code (spec non-goal); routing (plan 04).
- Contracts consumed: the home layout and README sections (plan 02); the check inputs and result lines (plan 01).
- Contracts produced:
  - **Token roles** in five groups: colour, type, space, radius and motion.
  - **Appearance variants:** the same names in the same file, under an appearance condition.
  - **Geometry tokens** go in their platform's folder, with their sources.
  - **The comparison's reasons:** chosen, combined in part (naming which parts), or not chosen.
- Shared files and their owning slice: the skill's `SKILL.md` and `references/graduating-a-direction.md` are created in p1 and extended in p2.

## Phase 1: graduate a direction

- Tasks:
  1. Failing check first: add F-grad and the T-grad task text. Run T-grad once against the plan-02 skill, and record that the foundations stay empty.
  2. `SKILL.md` gains the graduation steps:
     - **Source:** the chosen sketches, plus the comparison's selection and combination, or a refined one-file prototype. Set up a home first when there is none.
     - **Tokens:** move them by role into the foundations, with every defined appearance variant under its condition.
     - **Geometry:** a platform frame's geometry tokens go to their platform's folder, with their sources.
     - **Components:** a repeated part becomes a shared component.
     - **Surfaces:** the view's own surfaces go to its stylesheet.
     - **Explorations** stay untouched, and each direction's reason goes in the comparison. With no comparison, a short record beside the sketches.
     - **README:** list the graduated direction, linked to its record.
     - **Checks:** the three checks, with the render baseline taken first.
  3. Write `references/graduating-a-direction.md`, with role naming, appearance conditions that can be forced by a root attribute, and a worked example.
  4. Run T-grad ×3 and the AC15 cold read.
  5. Add a changelog entry and widen the skill's `description`.
- Files: `skills/product-design/curating-design-systems/{SKILL.md,references/graduating-a-direction.md,templates/design-home-readme.md}`, `evaluations/product-design/fixtures/harbor-home-graduate/**`, `evaluations/product-design/README.md`, `skills/product-design/CHANGELOG.md`.
- ACs: AC8, AC9, AC10 and AC15 pass here.
- Leaves the base working because: it is additive to the skill.
- PR slice: own PR · Predicted category: `human`: you review every PR (G1)
- Branch: feat/curating-design-systems-03-p1

## Phase 2: stop for a missing appearance or a conflicting role

- Tasks:
  1. Failing check first: add F-conflict, the documented staged edit that derives F-light from F-grad, and the two task texts. Run both against the 03-p1 skill and record what it does.
  2. **Missing appearance:** when a platform the home serves has an appearance the direction lacks, ask whether to draft it for review or record it as an open question, and write no value before the answer.
  3. **Conflicting role:** list each conflicting role with both values and the pages that link it, and offer three choices: change it everywhere, keep the existing value, or add a new role. Change no foundation file before the answer, and never let a view override a foundation role.
  4. Run T-light and T-conflict.
  5. Add a changelog entry.
- Files: `skills/product-design/curating-design-systems/{SKILL.md,references/graduating-a-direction.md}`, `evaluations/product-design/fixtures/harbor-home-conflict/**`, `evaluations/product-design/README.md`, `skills/product-design/CHANGELOG.md`.
- ACs: AC11 and AC12 pass here.
- Leaves the base working because: it is additive to the skill.
- PR slice: own PR · Predicted category: `human`: you review every PR (G1)
- Branch: feat/curating-design-systems-03-p2

## Notes

## Changes after launch
