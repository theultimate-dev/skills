# Plan 03: Hosted review

Status: done

Spec: `spec.md` · Roadmap: `roadmap.md`
Requirements: R5, R6
Acceptance criteria that pass in this plan: AC6, AC7, AC8
Depends on: 01 (`tree-check.html`, the `clean-tree` fixture, the staging layout); 02 (`interaction-harness.html`, which AC7 drives)
PR slices: whole plan
Branch: feat/building-html-prototypes-hosted-review

## Outcome

When reviewers will open a prototype through a host, the agent checks it served under a nested prefix as well as from disk, publishes it through an entry page at the tree root, and records the hosted result separately. When it can't open the host itself, it records "not performed" and asks the user to confirm.

## Boundaries

- In scope: R5 and R6; the hosted step; the entry-page section; the notes' hosted row.
- Out of scope: any particular host or its API (spec non-goal); real-host verification, which per R5 is the user's to confirm.
- Contracts consumed: the staging layout and result format (01), `tree-check.html` (01), and the harness API (02).
- Shared files and their owning slice: `references/design-tree-contract.md`, created in 01, gains its entry-page section here.

## Phase 1: The hosted render step and entry page

- Tasks:
  1. Check first: stage `clean-tree` at `/a/b/` and fill the harness with `entry reaches view` and `shared tokens applied`, plus the negative control that stages only the view's folder. Confirm the control shows `FAIL shared tokens applied` before writing the guidance. Add an entry page to `clean-tree` if it doesn't already have one.
  2. `references/interaction-and-verification.md`: a hosted step after "Direct opening". It runs when the artifact will be reviewed through a host: serve the exact file set under `/a/b/`, repeat the render check with `tree-check.html` and the harness, record the result in its own row, and when the host can't be opened, record "not performed" and ask the user.
  3. `references/design-tree-contract.md`: the entry-page pattern. A small page at the tree root links or forwards to the view, and the shared files are published at their tree-relative paths.
  4. `SKILL.md` "Verify and deliver": one sentence on the hosted step.
  5. `templates/prototype-notes.md`: a "Hosted render under a nested prefix" row whose results include "not performed".
  6. `skills/product-design/CHANGELOG.md` `[Unreleased]` Added.
  7. Run the AC rows: the cold reads for AC6 and AC8, and staged AC7.
- Files: `skills/product-design/building-html-prototypes/{SKILL.md, references/interaction-and-verification.md, references/design-tree-contract.md, templates/prototype-notes.md}`, `evaluations/product-design/fixtures/clean-tree/` (entry page, if missing), `evaluations/product-design/README.md`, `skills/product-design/CHANGELOG.md`, this plan file.
- ACs: AC6, AC7 and AC8 pass here.
- Leaves the base working because: it is additive. The `file://` step stays first and unchanged.
- PR slice: own PR, about 80 changed lines. Predicted category: `human`, because the user reviews every PR.

## Notes

- 2026-10-24 03: reconciled with `main` after slices 01 and 02. `clean-tree` already had its entry page, `index.html`, which links to `views/saved-guides/index.html`, so the fixture is unchanged. Only `check` is global in the harness, so AC7's checks live in `evaluations/product-design/checks/hosted-checks.js`, loaded with `?checks=`, and the template stays unfilled.
- 2026-10-24 03: the notes template has two hosted rows instead of one: the local check under `/a/b/`, and the render on the review host, which is "not performed" until the user confirms it. The agent's stand-in and the host's own result stay apart.
- 2026-10-24 03: the hosted step is step 3 of the verification sequence, so the later steps move down one. Nothing in the skill cites a step by number; plan 04's "step 5" (Layout) is now step 6.
- 2026-10-24 03: the root `CHANGELOG.md` gets an entry for the new checks file, which the plan's file list omits.
- 2026-10-24 03: the evaluations README also records the negative control's tree check, which reports the view's four references as outside the tree and ends `DONE 1/5`.

## Changes after launch
