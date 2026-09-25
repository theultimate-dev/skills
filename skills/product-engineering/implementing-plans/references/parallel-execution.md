# Parallel execution

How to split implementation across parallel agents or subagents without losing edits or shipping a combination nobody checked.

## Contents

- When to run in parallel
- Two shapes
- Prepare each brief
- Worktrees
- Ownership and shared files
- Tell workers they are not alone
- Integrate
- Without parallel agents

## When to run in parallel

Run workers in parallel only when every condition holds.

| Condition | How to check it |
|---|---|
| The host has parallel agents or subagents | Its tools offer them |
| The units own disjoint files | Compare the files each plan names, and search for shared imports the plans do not mention |
| The contracts between them are settled | API shapes, schemas, event names, and shared fixtures are written in the spec or the plan, not left to be decided |
| No unit depends on another's unmerged output | The `Depends on` column and `## Order and parallelism` in `roadmap.md` |
| Each unit has its own targeted checks | Its Verification rows map to tests the worker can run alone |

When any condition fails, build the units one after another in the roadmap's order. Parallel work on an unsettled contract produces two implementations that each pass their own checks and do not fit together.

## Two shapes

| Shape | Branches | Where integration happens |
|---|---|---|
| Parallel plans | One branch and one PR per slice, each from the base | On the base: after one merges, the other branch updates from the new base and is checked again |
| One slice split across workers | One branch per worker, merged into the slice branch | On the slice branch, before the handoff to verification |

Split one slice only when its parts are large and the contract between them is settled, for example an API endpoint and its client once the response shape is fixed. One agent finishes a small slice faster than two agents plus an integration.

## Prepare each brief

Fill the task brief (`templates/task-brief.md` in this skill) for each worker. It is a contract, not a transcript of the conversation.

- Paste the text of the Rs and ACs the worker owns, or give a path it can read. A new worktree holds only committed files, and the planning files reach the base only when the work item's first slice merges. A worker dispatched before then gets the spec, the roadmap and its plan pasted into its brief.
- Name the settled contracts it must not change, with their location.
- Separate agreed intent (the spec and its Approach) from observations (what the code does today) and from assumptions nobody has confirmed.
- Give starting points: files, tests, a neighboring example. Let the worker read any dependency it needs.
- Copy the permitted actions from the autonomy contract. A worker never gets more than the contract allows.
- Leave out secrets, credentials, and unrelated private material. Name test accounts by environment-variable name.
- Ask for a short return with evidence: status, branch, commits, checks with results, open issues. Not a reasoning transcript.

## Worktrees

Give each worker its own worktree when the host supports it: `git worktree add <path> -b <branch> <base>` per worker, or the host's option to run a subagent in an isolated worktree. Put the worktree outside the tracked tree, or in a path the project already ignores, so it never shows up as untracked files.

A worktree needs its own dependency install and build output. Run the project's setup command in each worktree before its first check.

Without isolated worktrees, parallel workers share one checkout and one git index. Then workers edit only their own files and do not commit. You commit each worker's files by path after it returns, because two agents committing in one checkout race on the index.

Remove a worktree once its branch is integrated, with `git worktree remove <path>`.

## Ownership and shared files

Every file a unit changes has exactly one owner, listed in the brief. Shared files have one owner for the whole run, named in every brief.

| Shared file | Why it needs one owner |
|---|---|
| Schemas and interface definitions | Two edits produce a contract neither side tested |
| Lockfiles and dependency manifests | Parallel installs produce lockfiles that merge as text and break at install |
| Migrations | Parallel workers pick the same sequence number or conflicting orders |
| Shared fixtures and seed data | One worker's change breaks the other's assertions |
| Generated code | Regenerate it once, from the integrated sources |
| The plan file | A worker building a whole plan owns its plan file; in a split slice, you own it |

A worker that needs a change in a file it does not own stops and returns the request: the file, the change, and why. The owner makes the change. Only the coordinator edits `roadmap.md`, and only to append.

## Tell workers they are not alone

Put this paragraph in every brief:

> You are not alone in this repository. Other workers are editing other files at the same time. Preserve their edits. Do not reset, stash, check out, reformat, or stage files you do not own, and do not run repository-wide formatters, codemods, or dependency installs. If you need a change in a file you do not own, stop and ask for it in your return.

## Integrate

You own the integration.

1. Inspect each return. A missing, malformed, or unevidenced return is a failed handoff, not completed work.
2. Read each worker's diff. Check that it stayed inside its files and its contracts.
3. Merge the worker branches into the slice branch in dependency order. Resolve each conflict by what the code means, not by which side merges cleanly: a merge that is clean as text can still break a contract.
4. Run the combined checks: the targeted checks of every unit, the project-wide build and typecheck, and the tests of every shared module.
5. Check what only the combination can break: the producer's and consumer's expectations of an API, migration order, shared fixtures and state, and the user journey that crosses the units.
6. Hand the integrated head SHA to verification. Evidence from a worker's branch holds for that branch only.

For parallel plans with separate PRs, integration happens on the base. After one PR merges, the other's green result is for the old base. The same holds for a stacked child after its parent changes or merges. Update the branch:

- By default, merge the new base, or the changed parent branch, into it. This never rewrites pushed history.
- Rebase only when the project rebases and the contract's `Force-push own PR branches after a rebase` field authorizes it. Push does not imply force-push. The only allowed form is `git push --force-with-lease=<branch>:<last-pushed-sha>`, to the loop's own PR branches: never the base branch, never anyone else's commits.
- A stacked child whose parent was squash-merged still carries the parent's original commits. Ask the user one question before rewriting it.

Then rerun its targeted checks and hand it to verification again.

## Without parallel agents

Build the units one after another in the roadmap's order. Keep the same ownership rules, so each slice's commits stay separable into their own PR.
