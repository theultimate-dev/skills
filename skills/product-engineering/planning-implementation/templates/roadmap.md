# Roadmap: [work item]

Spec: `spec.md` · Track: [feature | new app | refactor | bugfix] · Approved at G4: [YYYY-MM-DD]

<!-- Structural, written once at G4. Live PR state (open, awaiting a human, merged) is read from the host and never written here. Delete this comment. -->

## Autonomy contract

The user's own words, quoted. The agent never edits this section, and quotes its authorization lines verbatim on resume and before any merge. A change is appended under "Changes" with its date and the user's new words, in the main checkout; `implementing-plans` commits it with the next PR slice. An unanswered field means not authorized. Use the narrowest reading of the user's words: a slice not clearly covered stays `human`. Push does not imply force-push.

Detected on [YYYY-MM-DD]:
- Host: [GitHub via `gh` | GitLab via `glab` | other], repository [owner/repo] [new app only: created by the user | created by the agent: "[user's words]"]
- Base branch protection: required approving reviews [N | none | unknown]; code-owner review [required | not required]; required checks [names | none]; merge queue [yes | no]; linear history [required | not required]
- Merge settings: allowed methods [squash, merge, rebase]; auto-merge [allowed | not allowed]; merged branches deleted by the host [yes | no]
- CODEOWNERS: [path and owners of the planned paths | none] · Pull request policy: [file and heading | none]
- Deploy on merge: [yes | no]. Evidence: [workflow file and job, platform, deployment history, or what was checked]

Authorization:
- Commit and push: "[user's words]" | not authorized
- Force-push own PR branches after a rebase: "[user's words]" | not authorized
- Open PRs: "[user's words]" | not authorized
- Open issues (deferred should-fix findings and follow-ups): "[user's words]" | not authorized
- Merge `agent`-category PRs: "[user's words]" | not authorized | impossible: the base requires approving reviews
- Merge method: [squash | merge | rebase]: "[user's words]" | not authorized
- Base branch: [name] (a detected fact, not a permission)
- Deploy-on-merge detected: [yes | no]. Merges that deploy to [environment]: "[user's words]" | not authorized
- Human-review categories: the project policy and the skill defaults, plus "[user's changes]". UI and visual changes: [`human` | `agent` only for what these words cover: "[user's words]"]
- Who merges a `human` PR after approval: [the user | the agent when the user tells it to: "[user's words]"]
- Scope: this work item's PR slices, into [base]
- Stop and ask when: the escalation triggers, plus "[user's additions]"

Changes:
- [YYYY-MM-DD] "[user's new words]": [what it changes]

## Plans

| Plan | Phases | PR slices | Predicted category | Depends on |
|---|---|---|---|---|
| `plans/01-[slug].md` | p1 [name]; p2 [name] | per phase | p1 `human`: [reason]; p2 `agent` | none |
| `plans/02-[slug].md` | p1 [name] | whole plan | `agent` | 01-p2: [the contract it consumes] |

## Order and parallelism

- Start now: [slices with no unmet dependency]
- In parallel, each in its own worktree: [slices with disjoint files and no contract between them]
- Stacks, one level deep: [child slice on parent slice while the parent awaits a human]
- Critical path: [01-p1, 01-p2, 02-p1]
- `human` slices and when they open: [01-p1 first, so its review runs while 01-p2 is built]
- Shared files and their owning slice: [lockfile: 01-p2; schema: 01-p1]
- Planning files: `implementing-plans` commits `spec.md`, `roadmap.md`, a new or changed `verification-profile.md`, the plan file and any decision record written at G2 with [first slice]; each later plan's first slice commits its own plan file
- "How to verify" pointer in AGENTS.md or CLAUDE.md: [in Plan 0 | its own `human` PR slice: [slice] | not requested]

## Decisions

- [YYYY-MM-DD] [A planning choice and why. Example: the saved-searches panel ships behind `savedSearches`, off by default, so the UI review is one small flip PR at the end.]
- [YYYY-MM-DD] [After launch: what changed, why, and the user's words when a gate was reopened.]
