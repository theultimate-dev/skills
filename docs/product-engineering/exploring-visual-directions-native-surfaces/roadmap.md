# Roadmap: native platform surfaces in product-design, from direction briefs to handoffs

Spec: `spec.md` · Track: feature · Approved at G4: 2026-10-24, the user approved the plan in the plan-mode approval dialog, which carries no typed words

## Autonomy contract

The user's own words, quoted. The agent never edits this section, and quotes its authorization lines verbatim on resume and before any merge. A change is appended under "Changes" with its date and the user's new words, in the main checkout; `implementing-plans` commits it with the next PR slice. An unanswered field means not authorized. Use the narrowest reading of the user's words: a slice not clearly covered stays `human`. Push does not imply force-push.

Detected on 2026-10-24 at f401cae:
- Host: GitHub via `gh`, repository `theultimate-dev/skills`. PRs are opened as `IgorWnek`.
- Base branch protection: required approving reviews none (a PR is required, with 0 approvals); code-owner review not required; required checks `validate`; merge queue no; linear history not required; deletion and non-fast-forward pushes blocked.
- Merge settings: allowed methods merge, squash, rebase; auto-merge not allowed; merged branches deleted by the host: yes. The habit is merge commits (#14–#19).
- CODEOWNERS: none · Pull request policy: AGENTS.md "Conduct" and "Release".
- Deploy on merge: no. `validate.yml` runs on push and PR, and `release.yml` runs on tags or by hand.

Authorization, given at G4 on 2026-10-24. The user chose "Same as 2026-10-24 (Recommended)", which was offered as: "Commit, push and open PRs. No force-push and no issues. Agent PRs merge through the gate with a merge commit; you merge human PRs. Applies to this work item's three PRs into main". It repeats #9's contract of 2026-10-24, which quoted the user's standing default from their CLAUDE.md: "Agents may merge PRs categorized `agent` once the merge gate holds on the head SHA. PRs categorized `human` wait for my review."
- Commit and push: "Same as 2026-10-24 (Recommended)": "Commit, push and open PRs"
- Force-push own PR branches after a rebase: not authorized ("No force-push"; stacked branches update by merging main)
- Open PRs: "Same as 2026-10-24 (Recommended)": "Commit, push and open PRs"
- Open issues (deferred should-fix findings and follow-ups): not authorized ("no issues")
- Merge `agent`-category PRs: "Agent PRs merge through the gate with a merge commit". Every PR is `human` (G1), so this applies to none of them
- Merge method: merge: "with a merge commit"
- Base branch: `main` (a detected fact, not a permission)
- Deploy-on-merge detected: no
- Human-review categories: the project policy and the skill defaults, plus "The PR, and I merge it (Recommended)" (G1, 2026-10-24): the user reviews every PR in this work item. UI and visual changes: `human`
- Who merges a `human` PR after approval: the user: "you merge human PRs"
- Release tags: "Ask me at that point (Recommended)". After the user merges the release PR, the agent creates the annotated tags locally, shows the commit and the versions, and pushes nothing until the user says yes in the session
- Recheck awaiting PRs on a schedule: not authorized ("No, I'll tell you (Recommended)")
- Scope: "Applies to this work item's three PRs into main"
- Stop and ask when: the escalation triggers, the 3-round repair cap in the spec's Verification, and every tag push

## Plans

| Plan | Phases | PR slices | Predicted category | Depends on |
|---|---|---|---|---|
| `plans/01-native-surface-briefs.md` | p1: detection, placements, the platform frame, platform fit, licence-aware type, the renderer's hand-over | whole plan | `human`: the user reviews and merges every PR (G1) | none |
| `plans/02-native-placements-downstream.md` | p1: UX-flow placements, handoff variant, coordinator row | whole plan | `human`: as above | 01: the frame contract, the marker convention, and F-handoff frozen from 01's trials |
| Release (no plan file) | product-design minor and marketplace patch, through `release-process` | one PR | `human`: a release; the user merges it, and the tags wait for the user's yes | 01 and 02 merged |

## Order and parallelism

- Start now: 01.
- In parallel: none. 02 consumes 01's contract, and the release needs both.
- Stacks, one level deep: 02 may stack on 01 while 01 awaits the user's review. The release waits for both to merge.
- Critical path: 01 → 02 → release.
- Shared files: `skills/product-design/CHANGELOG.md` and `evaluations/product-design/README.md` are edited by 01 then 02. The frame contract and the marker convention are owned by 01.
- Planning files: slice 01's first commit carries `spec.md`, this roadmap, both plan files and the updated `verification-profile.md`.
- "How to verify" pointer: not requested (declined on #9, 2026-10-24).

## Decisions

- 2026-10-24: one worktree, `/Users/igor/dev/theultimate-dev/skills-worktrees/exploring-visual-directions-native-surfaces`, holds all three branches, switched in turn. Trials run on staged copies outside any checkout (G3).
- 2026-10-24: both plan files are committed with slice 01, so the verifier's tree is clean. This deviates from "each later plan's first slice commits its own plan file".
- 2026-10-24: the release has no plan file. AGENTS.md lets the release commit touch only the changelogs and the versions, so no plan status can change in it. AC17 maps to the release row.
- 2026-10-24: F-handoff is frozen at slice 02's start from slice 01's passing T1 run 1 and T2 outputs.
- 2026-10-24: `release-process` computes the versions at release time. Expected: product-design 0.3.0 (a new reference) and marketplace 0.3.3 (a patch for the plugin release; the root's evaluation lines are tooling).
- 2026-10-24: the planning folder stays on `main` afterwards. Removing it is the user's choice, as with #9.
