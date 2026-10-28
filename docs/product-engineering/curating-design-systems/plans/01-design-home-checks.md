# Plan 01: keep a design home's rules and check it

Status: in progress

Spec: `spec.md` · Roadmap: `roadmap.md`
Requirements: R7, R13, R14
Acceptance criteria that pass in this plan: AC13, AC14, AC16
Depends on: none
PR slices: per phase

## Outcome

`curating-design-systems` exists in product-design. It states the design home's four layout rules, and it checks a home with three browser-only templates: the mirrored tree check, the token check, and the render check. The validator keeps the tree check's copy identical to its source.

## Boundaries

- In scope:
  - the skill's directory, with `SKILL.md`, a layout-rules reference and the three check templates;
  - the validator's mirror rule and its AGENTS.md line;
  - decision records 0018 and 0019;
  - packaging in `marketplace.json`, `README.md` and both changelogs;
  - the AC13, AC14 and AC16 fixtures and their rerun commands.
- Out of scope:
  - setup and adoption (plan 02);
  - graduation (plan 03);
  - routing from other skills (plan 04);
  - any change to `building-html-prototypes` beyond the one comment line in its tree check.
- Contracts produced:
  - **Mirror rule:** a list of source and copy paths in `scripts/validate.py`, with an error for a pair that differs or is missing.
  - **Check inputs:** `entry=` and `pages=`, the same as the tree check's.
  - **Result lines:**
    - token check: `token defined once: <name>` and `token resolves: <page> <name>`;
    - render check: `renders as before: <page>`.
  - **Render baseline:** `#snapshot` JSON, saved as `render-baseline.json` at the staging root. Compare mode takes `baseline=` and `moved=<old>:<new>,…`.
- Shared files and their owning slice: `scripts/validate.py`, `AGENTS.md` and both copies of `tree-check.html`: p1. The new `SKILL.md`: p1 creates it, and p2 and p3 add their check's paragraph.

## Phase 1: the skill, its layout rules and the mirrored tree check

- Tasks:
  1. Failing check first: add the mirror rule to `scripts/validate.py`, with the pair `building-html-prototypes/templates/tree-check.html` → `curating-design-systems/templates/tree-check.html`. Run the validator and observe the missing-copy error.
  2. In the source's line-18 comment, change "every page the notes list that no link reaches" to wording that names no skill's notes. Then copy the file byte for byte.
  3. Write `SKILL.md`:
     - the frontmatter;
     - the purpose of a design home;
     - the four rules, with depth in `references/layout-rules.md`;
     - how to stage the home and run the tree check after every change;
     - no placeholders for later capabilities: the skill describes only what it does so far.
  4. Write decision records 0018 and 0019 with `decision-records`, and index them in `decisions/README.md`.
  5. Add the AGENTS.md "Skill format" line on mirrored files.
  6. Packaging:
     - add the skill's path to product-design's `skills` in `marketplace.json`;
     - add it to the README categories table;
     - add a product-design `[Unreleased]` entry;
     - add a root `[Unreleased]` entry for the validator rule and the two records.
  7. Add the AC16 fault steps to `evaluations/product-design/README.md`.
  8. Commit the planning files: `spec.md`, `roadmap.md`, all four plan files and `verification-profile.md`.
- Files:
  - `scripts/validate.py`, `AGENTS.md`;
  - `skills/product-design/curating-design-systems/{SKILL.md,references/layout-rules.md,templates/tree-check.html}`;
  - `skills/product-design/building-html-prototypes/templates/tree-check.html`;
  - `decisions/0018-curate-a-design-home-in-product-design.md`, `decisions/0019-mirror-shared-templates-across-skills.md`, `decisions/README.md`;
  - `.claude-plugin/marketplace.json`, `README.md`, `CHANGELOG.md`, `skills/product-design/CHANGELOG.md`;
  - `evaluations/product-design/README.md`;
  - `docs/product-engineering/curating-design-systems/**`, `docs/product-engineering/verification-profile.md`.
- ACs: AC16 (both rows) passes here. AC7 and AC15: progress only.
- Leaves the base working because: it is additive. The new skill is coherent on its own (rules and the tree check), and the source tree check changes one comment line only.
- PR slice: own PR · Predicted category: `human`: you review every PR (G1); it also changes an instruction file (AGENTS.md) and repository tooling (the validator)
- Branch: feat/curating-design-systems-01-p1

## Phase 2: token check

- Tasks:
  1. Failing check first: add fixtures F-dupes and F-clean, with their expected lines in the evaluations README. Staging them shows no `token-check.html` yet.
  2. Write `templates/token-check.html`, following the Approach section's design for this check.
     - Read every stylesheet and `style` element each page links, and parse it with `new CSSStyleSheet().replaceSync()`.
     - Key each definition by its file, selector and condition chain.
     - Read `var()` uses from `cssText`, since shorthands hide them from iteration, as the G2 probe showed.
     - A `var()` with a fallback is never reported.
  3. Add the token check to `SKILL.md`'s check step, and add a changelog entry.
  4. Fault injection: add a fourth duplicate to a scratch copy of F-clean, and observe a `FAIL` naming it.
- Files: `skills/product-design/curating-design-systems/{templates/token-check.html,SKILL.md}`, `evaluations/product-design/fixtures/{token-dupes,token-clean}/**`, `evaluations/product-design/README.md`, `skills/product-design/CHANGELOG.md`.
- ACs: AC13 passes here.
- Leaves the base working because: it is additive.
- PR slice: own PR · Predicted category: `human`: you review every PR (G1)
- Branch: feat/curating-design-systems-01-p2

## Phase 3: render check

- Tasks:
  1. Failing check first: add fixtures F-before and F-after, with their expected lines in the evaluations README.
  2. Write `templates/render-check.html`.
     - It loads each page in a same-origin frame of a fixed width (a `width=` parameter with a documented default).
     - It walks the page's elements by path and records a fixed list of computed properties.
     - Baseline mode writes the snapshot into `#snapshot`. Compare mode reads `baseline=` and maps pages through `moved=`, then reports the first differences for each page: the element, the property, and the values before and after.
  3. Add the render step to `SKILL.md`: take the baseline before any change touches a page, compare afterwards, and record each difference as intended, citing the user's choice, or as broken. Also say what the check can't see: changes that only pixels show.
  4. Run the controls: compare F-before with its own baseline, then rename one view folder and compare with `moved=`.
- Files: `skills/product-design/curating-design-systems/{templates/render-check.html,SKILL.md}`, `evaluations/product-design/fixtures/{render-before,render-after}/**`, `evaluations/product-design/README.md`, `skills/product-design/CHANGELOG.md`.
- ACs: AC14 passes here.
- Leaves the base working because: it is additive.
- PR slice: own PR · Predicted category: `human`: you review every PR (G1)
- Branch: feat/curating-design-systems-01-p3

## Notes

- 2026-10-26 01-p1: what the tree check cannot see sits in `references/layout-rules.md`, linked from `SKILL.md`, which keeps `SKILL.md` at 53 lines.
- 2026-10-26 01-p1: deleting the copy also breaks `SKILL.md`'s link to it, so the AC16 fault step 2 reports two errors. The evaluations README records both lines.

## Changes after launch
