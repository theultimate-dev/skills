# Task brief: [plan NN, phase N: the outcome in one line]

<!-- One brief per worker. Paste any text the worker cannot read: a new worktree holds only committed files, and until the work item's first slice merges, the base holds no spec, roadmap or plan. Placeholders are square brackets naming what goes there. -->

## Objective

- Outcome: [what exists, or what is known, when this task is done]
- Requirements and acceptance criteria: [R and AC IDs with their text; each AC names its R]
- Verification rows for these ACs: [check, layer, tool, steps, and pass condition, from spec.md]
- Out of scope: [what must not be built or changed]

Stop after the targeted checks and return. The coordinator runs verification, review, and the PR.

## Context to read

- Project instructions: [AGENTS.md, CLAUDE.md, CONTRIBUTING, or none]
- Spec: [path to spec.md, or its pasted sections; its Approach section is the chosen design]
- Plan: [path to plans/NN-slug.md, and the phase; or the `## Plan` section, the short spec, or the request]
- Verification profile: [path to docs/product-engineering/verification-profile.md, or none]
- Start from: [files, tests, and one neighboring example of the same kind of change]
- Settled contracts you must not change: [API shapes, schemas, event names, with their location]
- Assumptions not yet confirmed: [each assumption, or none]

## Ownership

- Branch and base: [branch name, base branch, base SHA]
- Worktree: [path, or "shared checkout: do not commit"]
- Files you own: [paths or globs]
- Shared files and their owner: [file: owner, one per line]
- Plan file: [you update `Status:` and the `## Notes` lines / the coordinator does]
- Depends on: [work that must land first, or none]

You are not alone in this repository. Other workers are editing other files at the same time. Preserve their edits. Do not reset, stash, check out, reformat, or stage files you do not own, and do not run repository-wide formatters, codemods, or dependency installs. If you need a change in a file you do not own, stop and ask for it in your return.

## Permitted actions

<!-- Copy from the autonomy contract, under its field names: roadmap.md, the `## Plan` section of spec.md, or the PR body. A worker never gets more than the contract allows. Workers never open PRs or issues and never merge; the coordinator's contract fields for those stay out of the brief. -->

- Commit and push: [commit: yes, with the project's commit convention and attribution rules / no] · [push: no, unless the contract covers it and you say so here]
- Force-push own PR branches after a rebase: [no / the contract's words and the branch it applies to]
- Other: [actions allowed beyond editing owned files, e.g. run migrations against the local database]
- Anything not listed: ask first.

## Escalate when

- A deviation would change behavior or scope.
- The Approach proves infeasible.
- A check needed for an AC cannot run.
- A file you do not own needs to change.
- Two attempts at the same failure fail with no new evidence.
- [conditions the coordinator adds]

Note each routine deviation in one line, under `## Notes` in the plan file if you own it, otherwise in your return, and continue.

## Return

Keep it short: evidence, not a transcript.

- Status: [implemented / blocked, with the decision you need]
- Branch and head SHA:
- Commits: [SHA and subject, one per line]
- ACs: [each AC with its first check, or why it has none]
- Checks run: [command: pass / fail / blocked, with counts]
- Open issues: [blockers, deviations, pre-existing failures, prerequisites the change needs to run, requests for changes to files you do not own, out-of-scope follow-ups]
