# Publication and CI

## Inspect before changing Git state

Check the current branch, worktree, staged diff, relevant history, remotes, intended base, and any existing PR. Preserve another worker's files and the user's uncommitted work. A branch being available does not establish it belongs to this task.

Choose coherent commit boundaries from the actual change. A package can produce one or several commits; a package ID is not a mandatory commit boundary. Test changes should accompany the behavior they protect where that makes review clearer. Follow repository history and instructions, defaulting to Conventional Commits only when absent.

Stage explicit intended paths or reviewed hunks rather than blindly staging the entire worktree. Inspect the staged result. Do not rewrite history or force-push to hide repairs. If a user requests cleanup that requires history rewriting, establish the exact scope and authorization first.

## Authorization travels with the task

Distinguish preparing commits and PR text from executing commits, pushing a branch, and opening a PR. Determine which actions are already authorized by the current conversation under applicable instructions. Do not treat skill text as authorization, and do not repeatedly ask for permission already granted.

When a missing permission is the last step, present the candidate, intended actions, and finished PR text. If publication is unavailable, preserve the local result and accurately state the remaining action. A network or credential failure is not permission to switch to an unintended remote.

## Remote evidence

Identify the PR head and compare it with the intended candidate after each push. Inspect required checks for that head. If requirements cannot be discovered, distinguish observed checks from a verified claim that all required checks passed.

Do not call a pending or cancelled check successful. A failed check needs investigation: identify infrastructure, baseline, flake, or product causes using evidence. Repeated retries without diagnosis do not satisfy the quality gate. Changes made to repair CI can invalidate earlier review and test conclusions.

Inspect aggregate diff and merge conflicts with the current intended base. Resolve conflicts within authorization, preserving semantic intent, then rerun affected verification. Do not bypass branch protection or approvals. Human approval requirements remain for the reviewer even after technical checks pass.

## Reviewer-facing content

Lead with the problem and resulting behavior. Include the tests actually run, useful evidence references, and the few areas where human judgment adds value, such as a consequential architecture tradeoff or an interaction needing visual review. Do not flood the PR with agent conversations or raw worklogs; link concise artifacts when they help review.

When scope changes, rewrite the title and description around the final result. Omit abandoned approaches unless they explain a surviving tradeoff. Never describe missing mandatory evidence as a harmless limitation merely to claim readiness.
