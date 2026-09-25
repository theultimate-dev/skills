# Stacked PRs

A stack is a child PR whose base is its parent's branch instead of the base branch. It lets dependent work continue while the parent waits for a human. The examples use `gh`; `glab mr update <iid> --target-branch <base>` retargets on GitLab.

## When to stack

| Situation | Do |
|---|---|
| The child needs the parent's code, and the parent awaits a human | Stack the child on the parent's branch |
| The parent is `agent` and its gate is about to pass | Wait for the merge, then branch from the base |
| The child does not need the parent's code | Branch from the base. No stack |
| The parent is itself stacked, so the child would be depth 2 | Pause this chain and work on independent plans |

Depth stays at 1 because every level multiplies the rebase, CI and re-verification work, a change requested on the root cascades through every child, and reviewers lose track of what they are approving.

## Create a child

```
git fetch origin
git switch -c <child> origin/<parent-branch>
# implement, verify and quick-review the child
git push -u origin <child>
gh pr create --base <parent-branch> --head <child> --title "<title>" --body-file <file>
```

- The body says "Stacked on #<parent>. That PR merges first." The diff then shows only the child's own changes.
- Compute the category on the child's own diff, and again after it is retargeted.
- Many workflows run only for PRs into the default branch (`pull_request: branches: [main]`), so the child's checks may not run yet. Verification still runs locally on the child's head. Required CI must be green after the retarget in any case.
- The child can get its full review while it waits. The update after the parent merges changes its head, so a delta review follows. It is small when the update changed nothing but the base.

## Never merge a child into its parent's branch

The base branch's protections, required checks and human review apply to the base branch. Code merged into the parent's branch reaches the base through the parent's merge, without the child's own gate. It also puts code into a PR the human is reviewing, or has already approved, without them seeing it. The child waits until the parent has merged and the child has been retargeted.

## After the parent merges

1. Record the parent's final head before anything is cleaned up: `gh pr view <parent> --json headRefOid --jq .headRefOid`. When that commit is not in your local repository, fetch it: `git fetch origin pull/<parent>/head`. GitHub keeps PR heads after the branch is deleted.
2. Rebase and retarget. This works for squash, rebase and merge-commit merges, and it needs the contract's "Force-push own PR branches after a rebase" field:

   ```
   git fetch origin
   OLD=$(git merge-base <child> <parent-head-sha>)
   git rebase --onto origin/<base> "$OLD" <child>
   git push --force-with-lease=<child>:<last-pushed-child-sha> origin <child>
   gh pr edit <child-pr> --base <base>
   ```

   Pushing never authorizes this force-push. Only that field does, and then only `git push --force-with-lease=<branch>:<last-pushed-sha>` to the loop's own PR branches; never to the base branch, never over anyone else's commits. Without the field:

   | The parent was merged with | Do |
   |---|---|
   | A merge commit | Merge the base into the child (`git merge origin/<base>`), push normally, and retarget |
   | A squash, or a rebase, which rewrites the parent's commits the same way | Ask the user one question before rewriting: "#<parent> was squash-merged. May I rebase #<child> onto <base> and force-push it with a lease?" Until they answer, the child waits |

3. Resolve any conflict by the intent of both sides. A resolution is a code change.
4. The push starts CI on the new head. Rerun verification for the child's ACs, recompute the category, get a delta review, then run the merge gate.
5. Delete the parent's branch, per repository policy, only after the child is retargeted.

Why `--onto` with the merge-base: a squash or rebase merge writes the parent's changes to the base as new commits. A plain rebase would replay the parent's old commits again and conflict with them. The merge-base names exactly the parent commit the child was built on, so only the child's own commits move.

When the host deletes merged branches on its own, GitHub retargets open children to the merged PR's base. Update them anyway, as above: after a squash merge, the parent's old commits still appear in the child's diff. Other hosts may close the child instead. If that happens, open a new PR from the updated branch and link the closed one.

## When the parent gets "changes requested"

1. Before changing the parent, record where each child branched: `OLD=$(git merge-base <child> origin/<parent-branch>)`.
2. Fix the parent through `implementing-plans`, with new commits on top of what the reviewer saw. Push, re-verify, get a delta review, and request the review again.
3. Run `git fetch origin`, then update each child from the new parent tip. With the force-push field, rebase it (`git rebase --onto origin/<parent-branch> "$OLD" <child>`) and push with a lease. Without it, merge the parent's branch into it (`git merge origin/<parent-branch>`) and push normally.
4. Rerun CI where it runs, rerun the child's verification, and get a delta review.

## When the parent is closed without merging

The child contains the parent's commits, so it cannot simply be retargeted. Stop the chain and ask the user: drop the child, or rebuild it on the base without the parent's changes. Rebuilding is a planning change and goes through the plan's "Changes after launch".

## Edge cases

| Case | Do |
|---|---|
| The child needs a change in the parent's code | Make it in the parent when it belongs to the parent's concern, and tell the reviewer what changed. Otherwise make it in the child |
| The parent must be updated from a moved base | Merge the base into the parent, then update the children as above. Rebase the parent instead only with the force-push field: record `OLD` for each child first, and tell the parent's reviewer why the history changed |
| A human approved the parent, then the parent changed | The host may dismiss the approval. Request the review again and say what changed |
| Two children on one parent | Allowed: both are depth 1. Update each after the parent merges |
| The child's branch after the retarget | Keep its name. The plan file's `Branch:` line finds the PR on the host; no file changes |

## History

- Rewrite only your own branches, and never to hide repairs.
- Pushing never authorizes a force-push. Only the contract's "Force-push own PR branches after a rebase" field does, and then only `git push --force-with-lease=<branch>:<last-pushed-sha>` to the loop's own PR branches; never to the base branch, never over anyone else's commits. Without it, update a PR branch by merging the base into it, and ask the user one question before rewriting a stacked child whose parent was squash-merged.
- When the lease fails, someone else pushed: fetch and inspect their commits instead of overwriting them.
- Do not rewrite published history to make it prettier. A reviewer who has seen a branch reads new commits more easily than rewritten ones.
