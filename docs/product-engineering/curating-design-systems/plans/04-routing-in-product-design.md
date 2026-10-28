# Plan 04: route to curating-design-systems from the coordinator and the three specialists

Status: planned

Spec: `spec.md` · Roadmap: `roadmap.md`
Requirements: R15, R16
Acceptance criteria that pass in this plan: AC17, AC18
Depends on: 03-p2, so the skill is complete before anything routes to it
PR slices: whole plan
Branch: feat/curating-design-systems-04

## Outcome

Discovery routes Converge through graduation, after the direction is selected and before refinement. The skills on either side of graduation, and the handoff, point to the new skill and its foundations.

## Boundaries

- In scope:
  - `guiding-product-discovery`: its `SKILL.md` specialist table, the Converge row of `references/workflow.md`, and a design-home row in `templates/discovery-index.md`;
  - `exploring-visual-directions`: its `SKILL.md` selection paragraph, and the selection fields of `templates/direction-comparison.md`;
  - `building-html-prototypes`: its `SKILL.md`, and the "Shared files" section of `references/design-tree-contract.md`;
  - `preparing-implementation-handoffs`: its `SKILL.md`, and line 30 of `templates/implementation-handoff.md`;
  - the plugin's description in `marketplace.json` and its README row;
  - the changelog.
- Out of scope: any behavior change in those skills beyond naming and routing; the tree check, whose comment already changed in 01-p1.
- Contracts consumed: the skill name, and graduation's position between selection and refinement.
- Shared files and their owning slice: `.claude-plugin/marketplace.json` (description) and `README.md` (row text), here.

## Phase 1: route to the skill

- Tasks:
  1. Failing check first: run the AC17 and AC18 cold reads on main, and record that none of them names `curating-design-systems`.
  2. Make the edits listed under "In scope". Each skill names the new skill in prose, never by a link outside its own directory.
  3. Rerun the cold reads, and run the validator.
  4. Add a changelog entry, and set `Status: done` in this plan file. This is the work item's last slice.
- Files: the files listed under "In scope", plus `skills/product-design/CHANGELOG.md` and this plan file.
- ACs: AC17 and AC18 pass here.
- Leaves the base working because: it adds wording only. No behavior is removed.
- PR slice: own PR · Predicted category: `human`: you review every PR (G1)

## Notes

## Changes after launch
