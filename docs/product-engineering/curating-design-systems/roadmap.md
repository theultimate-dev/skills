# Roadmap: curating-design-systems, a design home and the graduation of a chosen direction

Spec: `spec.md` · Track: feature · Approved at G4: 2026-10-25, "Approve the roadmap". The user asked to stop after G4 and wait for their go-ahead before 01-p1 starts.

## Autonomy contract

The user's own words, quoted. The agent never edits this section, and quotes its authorization lines verbatim on resume and before any merge. A change is appended under "Changes" with its date and the user's new words, in the main checkout; `implementing-plans` commits it with the next PR slice. An unanswered field means not authorized. Use the narrowest reading of the user's words: a slice not clearly covered stays `human`. Push does not imply force-push.

Detected on 2026-10-25 at fc87115:
- Host: GitHub via `gh`, repository `theultimate-dev/skills`.
- Base branch protection on `main`:
  - a pull request is required, with 0 approving reviews, and `require_extra_approval_for_unattributed_changes` is set;
  - code-owner review is not required;
  - the required check is `validate`;
  - no merge queue, and linear history is not required;
  - deletion and non-fast-forward pushes are blocked.
- Merge settings: merge, squash and rebase are all allowed. Auto-merge is not allowed. The host deletes merged branches. The habit is merge commits (#17–#22).
- CODEOWNERS: none. Pull request policy: AGENTS.md "Conduct" and "Release".
- Deploy on merge: no. `validate.yml` runs on every push and pull request; `release.yml` runs on tags or by hand.

Authorization, given at G4 on 2026-10-25.

The user chose "Same as 2026-10-24 (Recommended)", which was offered as: "Commit, push and open PRs. No force-push: stacked branches update by merging main. Agent PRs would merge through the gate with a merge commit, but every PR here is human, and you merge human PRs. Applies to this work item's seven PRs into main."

That repeats #10's contract of 2026-10-24, which quoted the user's standing default from their CLAUDE.md: "Agents may merge PRs categorized `agent` once the merge gate holds on the head SHA. PRs categorized `human` wait for my review."

- Commit and push: "Same as 2026-10-24 (Recommended)": "Commit, push and open PRs"
- Force-push own PR branches after a rebase: not authorized ("No force-push: stacked branches update by merging main")
- Open PRs: "Same as 2026-10-24 (Recommended)": "Commit, push and open PRs"
- Open issues (deferred should-fix findings and follow-ups): "Only the product-context one (Recommended)". This covers one issue, the product-context follow-up named in the spec's non-goals. No other issues: deferred findings go back to the user.
- Merge `agent`-category PRs: "Agent PRs would merge through the gate with a merge commit". Every PR is `human` (G1), so this applies to none of them.
- Merge method: merge: "with a merge commit"
- Base branch: `main` (a detected fact, not a permission)
- Deploy-on-merge detected: no
- Human-review categories: the project policy and the skill defaults, plus "Every PR (Recommended)" (G1, 2026-10-25): you review every PR in this work item. UI and visual changes: `human`
- Who merges a `human` PR after approval: the user: "you merge human PRs"
- Recheck awaiting PRs on a schedule: not authorized ("No, I'll tell you (Recommended)")
- Release: not in scope (spec non-goal). Cut only when the user asks.
- Scope: "Applies to this work item's seven PRs into main"
- Stop and ask when: the escalation triggers, and before starting 01-p1 (the user's instruction for this session: "Once I approve G4, stop instead of starting the first PR slice, and wait for my go-ahead.")

Changes:

## Plans

| Plan | Phases | PR slices | Predicted category | Depends on |
|---|---|---|---|---|
| `plans/01-design-home-checks.md` | p1: the skill with its layout rules and the mirrored tree check; p2: token check; p3: render check | per phase | all `human`: you review every PR (G1). p1 also changes AGENTS.md and the validator | none |
| `plans/02-setup-and-adoption.md` | p1: set up or adopt a design home | whole plan | `human`: as above | 01-p3: the render check's `moved=` for adoption |
| `plans/03-graduation.md` | p1: graduate a direction; p2: stop for a missing appearance or a conflicting role | per phase | `human`: as above | 02: the home layout and README template; 01-p2: the token check |
| `plans/04-routing-in-product-design.md` | p1: the coordinator and three specialists route to the skill | whole plan | `human`: as above | 03-p2: the complete skill to route to |

## Order and parallelism

- Start now: 01-p1.
- In parallel: none. Every slice edits the new skill's `SKILL.md`, `skills/product-design/CHANGELOG.md` or `evaluations/product-design/README.md`, so the slices run one after another.
- Stacks, one level deep: a slice may stack on its parent while the parent awaits your review. Its own child then waits for the parent to merge.
- Critical path: 01-p1 → 01-p2 → 01-p3 → 02 → 03-p1 → 03-p2 → 04.
- `human` slices: all seven, opened as early as the chain allows, so your reviews overlap with the next slice's build.
- Shared files and their owners:
  - The new skill's `SKILL.md`: created by 01-p1 and extended by each later slice of plans 01–03.
  - The changelogs and `evaluations/product-design/README.md`: each slice adds its own entry or section.
  - `.claude-plugin/marketplace.json`: 01-p1 adds the skill path; 04 updates the plugin description.
  - `scripts/validate.py` and `AGENTS.md`: 01-p1.
  - `building-html-prototypes/templates/tree-check.html` and its copy: 01-p1.
- Planning files: 01-p1's first commit carries `spec.md`, this roadmap, all four plan files and the updated `verification-profile.md`, as #10 did, so the verifier's tree is clean. The decision records 0018 and 0019 land in 01-p1 too.
- "How to verify" pointer: not requested (declined for #9 on 2026-10-24).

## Decisions

- 2026-10-25: one worktree holds every branch, switched in turn: `/Users/igor/dev/theultimate-dev/skills-worktrees/curating-design-systems`. Trials run on staged copies outside any checkout (G3).
- 2026-10-25: the skill grows in four coherent steps, each a working skill when it merges:
  - plan 01: keep a design home's rules and check it;
  - plan 02: set up or adopt a home;
  - plan 03: graduate a direction into it;
  - plan 04: the neighboring skills route to it.

  Its `description` is widened in each step.
- 2026-10-25: the token and render checks are separate slices (01-p2, 01-p3), each about 250 lines of template JavaScript plus fixtures, to keep each PR readable in one sitting. The mirrored tree check is a byte-identical copy that the validator compares, so its 254 lines need no line-by-line review.
- 2026-10-25: graduation is split in two (03-p1, 03-p2): the main path, then the two points where it stops to ask. F-light is derived from F-grad by a documented staged edit, not copied, to keep 03-p2 small.
- 2026-10-25: no release slice, because the spec lists cutting a release as a non-goal. Once 04 merges, `release-process` can cut product-design 0.4.0 (a minor bump for a new skill) and marketplace 0.3.4, when you ask for it.
- 2026-10-25: the product-context follow-up issue (spec non-goal) is opened when the slices launch, if the contract allows opening issues. Otherwise its text goes in the finish report.
- 2026-10-26: at launch, opened the product-context follow-up as #23. It is linked to #13, whose "Layout" point covers the product-design side.
