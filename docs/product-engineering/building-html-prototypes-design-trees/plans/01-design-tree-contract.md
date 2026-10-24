# Plan 01: The design-tree contract

Status: done

Spec: `spec.md` · Roadmap: `roadmap.md`
Requirements: R1, R2, R3, R4, R16
Acceptance criteria that pass in this plan: AC1, AC2, AC3, AC4, AC5, AC19
Depends on: none
PR slices: whole plan
Branch: feat/building-html-prototypes-design-trees

## Outcome

`building-html-prototypes` names two contracts, the one-file artifact and the design tree, and says when each applies. A design tree has explicit rules and a copyable `tree-check.html` that reports every reference that is remote, leaves the tree, or points to a missing file. Nothing in the plugin still claims that every prototype is one file.

## Boundaries

- In scope: R1 to R4 and R16; decision records 0016 and 0017; the "Serve files locally" section (staging layout and result format); fixtures for AC2, AC3 and AC5.
- Out of scope: the hosted render step and the entry page (plan 03); the harness and page slices (plan 02); native surfaces (plan 04); #10 and #11.
- Contracts produced:
  - Staging layout: the tree is copied untouched to `<staging>/a/b/`, the templates sit at `<staging>/`, and `<staging>/` is served from the server root.
  - Result format: one `#results` element, one `PASS <name>` or `FAIL <name>: <detail>` line per check, ending with `DONE <passed>/<total>`.
  - Both are written in `references/interaction-and-verification.md`. The input of `tree-check.html` is the tree root under the server, the entry page, and an optional page list.
- Shared files and their owning slice: as in the roadmap.

## Phase 1: The design-tree contract, tree check and one-file claims

- Tasks:
  1. Fixtures first, in `evaluations/product-design/fixtures/`:
     - `broken-tree/`: a remote `href` to `https://cdn.example.com/x.css`, a root-absolute `src="/img/logo.svg"`, a `url()` outside the tree, and a missing `href`, the last on a page that only the notes list.
     - `clean-tree/`: a root page linking a view in its own folder, plus `shared/tokens.css` and `shared/components.css`.
     - `shared-foundations-project/` and `no-shared-files-project/` for the trials.
     - `evaluations/product-design/README.md` with the rerun commands.
  2. `templates/tree-check.html`. Run it on `broken-tree` and confirm the four `FAIL` lines, which shows the check can fail, then make `clean-tree` end `DONE n/n`.
  3. `references/design-tree-contract.md`: when the contract applies, the page rules from R2 with parent paths described in words, the shared-files list in the notes, and how to run `tree-check.html`.
  4. `references/interaction-and-verification.md`: add "Serve files locally" (staging layout, result format), and point step 1, static portability, at the design-tree check for trees.
  5. `references/offline-artifact-contract.md`: scope it to the one-file artifact, and replace the "different portability contract" paragraph with a pointer to the design tree.
  6. `SKILL.md`:
     - The description names both contracts.
     - "Establish the task": continuity means linking a tree's shared files, or copying tokens into a one-file artifact.
     - "Choose fidelity": sketches stay one file and may keep candidate tokens inline until a direction is chosen.
     - "Verify and deliver": replace the sentence that no artifact may need another file.
  7. `templates/prototype-notes.md`: add a contract line (one file or design tree) and the shared files each page depends on.
  8. R16 outside the skill: `README.md:26`, `skills/product-design/guiding-product-discovery/templates/task-brief.md:21`, the plugin description in `.claude-plugin/marketplace.json:61`. Records 0016 and 0017 and their index rows are already written.
  9. Changelogs:
     - `skills/product-design/CHANGELOG.md` `[Unreleased]`: Added (the design-tree contract and the tree check) and Changed (the one-file wording, the plugin description).
     - Root `CHANGELOG.md` `[Unreleased]`: decisions 0016 and 0017, and `evaluations/product-design/`.
  10. Run the AC rows: the cold reads for AC1 and AC4, trials AC2 and AC3, staged AC5, and AC19.
- Files:
  - In `skills/product-design/building-html-prototypes/`: `SKILL.md`, `references/design-tree-contract.md` (new), `references/offline-artifact-contract.md`, `references/interaction-and-verification.md`, `templates/tree-check.html` (new), `templates/prototype-notes.md`.
  - Elsewhere: `README.md`, `skills/product-design/guiding-product-discovery/templates/task-brief.md`, `.claude-plugin/marketplace.json`, `decisions/0016-*.md`, `decisions/0017-*.md`, `decisions/README.md`, `skills/product-design/CHANGELOG.md`, `CHANGELOG.md`, `evaluations/product-design/**`, and the planning files.
- ACs: AC1, AC2, AC3, AC4, AC5 and AC19 pass here.
- Leaves the base working because: it is additive. The one-file artifact stays the default, and its rules are unchanged.
- PR slice: own PR, about 490 changed lines. That includes about 110 lines of fixtures and the two records approved at G3, but not the planning files approved at the gates. Predicted category: `human`, because the user reviews every PR, and the slice touches `.claude-plugin/marketplace.json` and adds accepted decision records.

## Notes

- `tree-check.html` also fails what the contract forbids and markup can show: a page that is not a full HTML document, a `base` element, a module script, a CSS `@import`, and a reference to a folder rather than a file. Scripts are still read by hand for requests.
- The references name `templates/tree-check.html` and `templates/prototype-notes.md` in backticks instead of linking them, because a link from `references/` to `templates/` needs a parent path, which `scripts/validate.py` bans. `SKILL.md` links the template directly.
- `fixtures/clean-tree/index.html` is the tree's root page and links the view, so plan 03 can use it as the entry page.
- The trial fixtures and `evaluations/product-design/README.md` are committed with the tree check, in one evaluations unit.
- Verification on 778f763 found two gaps, fixed in this slice: `broken-tree`'s out-of-tree `url()` named a missing file, so a check without the in-tree rule still passed AC5 (it now reaches `fixtures/outside-tree/paper.svg`, and the rerun checks each reason); and the check skipped form `action` and `formaction`, which it now reads.
- The quick review at 426d616 found that a folder linked without its trailing slash passed, that a malformed percent escape stopped the check, and that the check did not test the `meta charset` the contract requires. Fixed with `fixtures/edge-tree/` as their regression; the contract now states the `base` ban and the case-sensitivity limit. Accepted records 0016 and 0017 already describe the harness, page slices and hosted check that plans 02 and 03 add; the PR says so.

## Changes after launch
