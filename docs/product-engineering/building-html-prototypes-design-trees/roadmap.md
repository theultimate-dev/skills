# Roadmap: building-html-prototypes beyond the one-file sketch

Spec: `spec.md` · Track: feature · Approved at G4: 2026-10-24, "Approved"

## Autonomy contract

The user's own words, quoted. The agent never edits this section, and quotes its authorization lines verbatim on resume and before any merge. A change is appended under "Changes" with its date and the user's new words, in the main checkout; `implementing-plans` commits it with the next PR slice. An unanswered field means not authorized. Use the narrowest reading of the user's words: a slice not clearly covered stays `human`. Push does not imply force-push.

Detected on 2026-10-24:
- Host: GitHub via `gh`, repository `theultimate-dev/skills`. PRs are opened as `IgorWnek`, the user's own account, and GitHub does not let an author approve their own PR.
- Base branch protection (`gh api repos/theultimate-dev/skills/rules/branches/main`): required approving reviews: none (a pull request is required, with 0 approvals); code-owner review: not required; required checks: `validate`; merge queue: no; linear history: not required; deletion and non-fast-forward pushes are blocked.
- Merge settings: allowed methods: merge, squash, rebase; auto-merge: not allowed; merged branches deleted by the host: yes. The project's habit is merge commits (`git log --merges origin/main`: #14, #8, #7, #6).
- CODEOWNERS: none. Pull request policy: AGENTS.md "Conduct": "Never commit, push, tag, open a pull request, or publish without explicit confirmation in the current conversation". AGENTS.md "Release": "`main` takes changes only through pull requests".
- Deploy on merge: no. Evidence: `.github/workflows/validate.yml` only validates on push and pull request, and `.github/workflows/release.yml` runs only on tags or by hand.

Authorization, given at G4 on 2026-10-24. The user chose "Standing default (Recommended)", which was offered as: "Commit, push, open PRs; merge agent-category PRs through the merge gate with a merge commit; human PRs wait for you. No force-push (stacked branches update by merging main). No issues opened." That option quoted the user's standing default from their CLAUDE.md: "Agents may merge PRs categorized `agent` once the merge gate holds on the head SHA. PRs categorized `human` wait for my review."
- Commit and push: "Standing default (Recommended)": commit and push
- Force-push own PR branches after a rebase: not authorized ("No force-push (stacked branches update by merging main)")
- Open PRs: "Standing default (Recommended)": open PRs
- Open issues (deferred should-fix findings and follow-ups): not authorized ("No issues opened")
- Merge `agent`-category PRs: "Standing default (Recommended)": through the merge gate on the head SHA. Every slice is predicted `human`, so this applies only to a slice that turns out `agent`, which the human-review categories below rule out
- Merge method: merge: "with a merge commit"
- Base branch: `main` (a detected fact, not a permission)
- Deploy-on-merge detected: no
- Human-review categories: the project policy and the skill defaults, plus "All three" (G1, 2026-10-23: the user reviews every PR of this work item). UI and visual changes: `human`
- Who merges a `human` PR after approval: the user: "I merge it (Recommended)"
- Scope: this work item's PR slices, into `main`
- Stop and ask when: the escalation triggers

Changes:

## Plans

| Plan | Phases | PR slices | Predicted category | Depends on |
|---|---|---|---|---|
| `plans/01-design-tree-contract.md` | p1 the design-tree contract, tree check and one-file claims | whole plan | `human`: the user reviews every PR; also touches `.claude-plugin/marketplace.json` and accepted decision records | none |
| `plans/02-scripted-checks.md` | p1 the interaction harness and page slices | whole plan | `human`: the user reviews every PR | 01: the staging layout and result format in `references/interaction-and-verification.md` |
| `plans/03-hosted-review.md` | p1 the hosted render step and entry page | whole plan | `human`: the user reviews every PR | 01: `tree-check.html` and the `clean-tree` fixture; 02: `interaction-harness.html` for AC7 |
| `plans/04-native-surface-profile.md` | p1 the native-surface profile | whole plan | `human`: the user reviews every PR | 02: `interaction-harness.html` for AC16 |

## Order and parallelism

- Start now: 01.
- In parallel: none. Every slice changes `SKILL.md`, `references/interaction-and-verification.md`, `templates/prototype-notes.md`, both changelogs and `evaluations/product-design/README.md`.
- Stacks, one level deep: 02 may stack on 01 while 01 awaits review. 03 and 04 wait until 02 merges.
- Critical path: 01 → 02 → 03 → 04.
- `human` slices and when they open: all four, in order. Each review runs while the next slice is built, as far as the one-level stacking rule allows.
- Shared files and their owning slice:
  - The staging layout and result format: 01, in `references/interaction-and-verification.md`.
  - `templates/interaction-harness.html`: 02.
  - `templates/tree-check.html` and the `clean-tree` fixture: 01.
  - `references/design-tree-contract.md`: 01 creates it; 03 adds the entry-page section.
  - Every other shared file is edited by each slice in order.
- Planning files: `implementing-plans` commits `spec.md`, `roadmap.md`, `verification-profile.md`, `plans/01-design-tree-contract.md` and decision records 0016 and 0017 with slice 01. Each later plan's first slice commits its own plan file.
- "How to verify" pointer in AGENTS.md: not requested (declined at G3, 2026-10-24).

## Decisions

- 2026-10-24: Intake planned three slices (A = parts 1 and 2, B = part 3, C = part 4). G4 splits A in two:
  - A as one PR fails two of the slicing tests. Its title needs an "and" (design trees and hosted review), and at about 490 changed lines, plus the planning files, it doesn't fit one sitting.
  - The hosted check's AC7 drives `interaction-harness.html`, which B creates, so hosted review lands after B. The order becomes tree contract, scripted checks, hosted review, native surfaces.
- 2026-10-24: The staging layout and result format live in a "Serve files locally" section of `references/interaction-and-verification.md`, written in 01, because `tree-check.html` needs them before the hosted step exists. The Approach had placed them in the hosted step. The contract is unchanged; only its first home moves.
- 2026-10-24: Slice 01 reuses the planning branch `feat/building-html-prototypes-design-trees` in the existing worktree, where the planning files and records already sit uncommitted. Later slices take descriptive branch names after the repository's `<type>/<skill>-<change>` pattern.
- 2026-10-24: The planning files are committed with slice 01 under `docs/product-engineering/` ("1", G4). No skill in the loop deletes them: each plan's last slice sets `Status: done`. Removing this work item's folder after 04 merges is the user's choice, as its own docs PR. `verification-profile.md` stays for later work items.
- 2026-10-24: Releasing product-design is a non-goal (spec). After the last slice merges, `release-process` cuts product-design 0.2.0, a minor bump for new references and templates, together with a marketplace release.
