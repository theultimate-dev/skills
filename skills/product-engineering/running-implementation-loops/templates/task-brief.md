# Task brief: [stage N, skill: plan NN, phase N: the outcome in one line]

<!-- One brief per agent, for stage 5 (implement), stage 6 (verify), a spike, or a parallel slice. The review stages brief their reviewers with the lens brief from `reviewing-code-changes`; use this brief for a reviewer only when that skill is not installed. The headings match the task brief of `implementing-plans`; this copy adds the Stage section and the per-stage return lines. Paste any text the agent cannot read: a new worktree holds only committed files, and until the work item's first slice merges, the base holds no spec, roadmap or plan. Placeholders are square brackets naming what goes there. -->

## Stage

- Stage and skill: [5 `implementing-plans` | 6 `verifying-implementation` | spike on `implementing-plans` | reviewer, without `reviewing-code-changes`]
- When that skill is not installed: [the stage's essential outcome, in one line]
- Fresh context: [yes: form your own view from the spec, the diff and the evidence below before reading anything else | no]
- Candidate: [branch and head SHA, for verification and review]
- Read only after writing your own result: [the implementer's reasoning, earlier reviews, or none]

Stop when the stage's outcome is reached and return. The coordinator runs the next stage.

A verifier or reviewer owns no files and stays read-only toward the branch and the PR: no edits, commits, pushes, or comments. A verifier checks out the candidate branch, confirms that HEAD equals the candidate SHA, returns to the coordinator when `git status --porcelain` is not empty, and starts the app itself from that checkout. Put scratch scripts and injected faults in a separate worktree, and remove it afterwards.

## Objective

- Outcome: [what exists, or what is known, when this task is done]
- Requirements and acceptance criteria: [R and AC IDs with their text; each AC names its R]
- Verification rows for these ACs: [check, layer, tool, steps, and pass condition, from spec.md]
- Out of scope: [what must not be built or changed]

At stage 5, stop after the targeted checks and return. The coordinator runs verification, review, and the PR.

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

<!-- Copy from the autonomy contract: roadmap.md, the `## Plan` section of spec.md, or the PR body. Use the contract's field names. An agent never gets more than the contract allows, and only `implementing-plans` commits. -->

- Commit and push: [commit: yes, with the project's commit convention and attribution rules / no; push: no, unless the contract's "Commit and push" field covers it and you say so here]
- Force-push own PR branches after a rebase: [no / yes, only `git push --force-with-lease=<branch>:<last-pushed-sha>` to this branch, when the contract's field says so]
- Open PRs, open issues, merge: no; the coordinator does these
- Other: [actions allowed beyond editing owned files, e.g. start the app and reset the local database the seed created]
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

A verifier and a spike return these in place of Status, Commits and ACs:

- Verification (stage 6): the SHA and the counts of `pass`, `fail`, `blocked` and `blocked (human eye)`; the `## Verification` section; each `fail` with its repro; each `blocked (human eye)` row with its screenshot path; each other `blocked` row with its reason, which stops the slice before the PR opens
- Spike: the answer and its evidence: the command and output that support it, the approach it points to, the branch, and the commit of `docs/product-engineering/<slug>/spike.md`
