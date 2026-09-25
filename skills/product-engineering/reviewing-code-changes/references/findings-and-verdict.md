# Findings and verdict

The orchestrating reviewer turns the lens output into one review. Work through the sections in order: collect, deduplicate, substantiate, rate, check the category, decide, post. Later rounds add dispositions and the delta rules.

## Contents

- Collect the lens output
- A useful finding
- Deduplicate
- Substantiate
- Severity
- Category check
- Verdict
- Post the review
- Dispositions preserve history
- Delta reviews
- Round limit
- Scaling and models
- Example: one ownership check across three rounds

## Collect the lens output

Each lens returns finding blocks, `nothing in scope` with a reason, or `no findings` with a `Checked:` line.

- When a lens's output is missing, malformed or about another lens, rerun it once with the same brief. When the rerun fails too, run that lens yourself and label it self-review in the review. The verdict line then says self-review too.
- A `no findings` answer without a `Checked:` line is not coverage. Ask the reviewer what it checked, or rerun it.
- Keep the findings a lens raised outside its scope. Deduplication assigns each one to the lens that owns it.

## A useful finding

| Field | Content |
|---|---|
| ID | `F1`, `F2`, … in full mode; `Q1`, `Q2`, … in quick mode. Stable across rounds and never reused. |
| Lens | The lens whose fix it is, plus any other lens that raised it. |
| Location | File and line at the reviewed SHA. List every location when one cause shows up in several places. |
| Severity | `blocking`, `should-fix` or `nit` |
| Status | `confirmed` or `unconfirmed` |
| Summary | One sentence on what is wrong. |
| Trigger | The input, state or sequence that exposes it; expected versus actual. |
| Impact | Who or what is hurt, and how badly. |
| Evidence | The reproduction, a command and its output, or the quoted code with the reasoning. |
| Basis | The R or AC ID, the project rule, the decision record, or the idiom's source. |
| Direction | A suggested fix that does not force an unrelated refactor. |

- Static evidence can confirm a defect that the environment cannot execute. Say that it was confirmed by reading, not by running.
- A suspicion without a concrete trigger is not a confirmed finding, however plausible it sounds.
- A missing check and wrong code are different findings with different routes:

| The finding is | It goes to |
|---|---|
| Code that does the wrong thing | `implementing-plans`, for a fix |
| A check that was never run | `verifying-implementation`, to run it at the head |
| A check that cannot run (blocked) | escalation: the verification contract cannot run, and the PR becomes `human`. The direction says so instead of proposing a code fix. |

## Deduplicate

1. Group findings with the same root cause, even when the lenses describe different symptoms.
2. Keep one finding per root cause, owned by the lens whose fix it is. A missing ownership check is a security finding even when intent found it through an AC.
3. Keep the strongest evidence, every location, and the highest severity the evidence supports.
4. When two findings pull opposite ways, settle it with evidence and post one finding with the resolution. For example, efficiency asks for a cache, and security shows the cache would serve one user's data to another.

## Substantiate

Substantiate every finding before it reaches the review:

1. Read the code at the reviewed SHA: the flagged lines, their callers, and anything upstream that might already guard them.
2. Run a targeted check: the test that should fail, a scratch test, a query count, a request against a local run started from the verification profile.
3. Reproduce the trigger when it is cheap. Use only local or disposable environments.

On a PR the loop did not open, run nothing from its head (install, build, tests, audit, the app) until the user agrees. Substantiate by reading, and label the finding "confirmed by reading".

| Outcome | Action |
|---|---|
| The evidence confirms it | Keep it as `confirmed`. |
| The evidence refutes it | Drop it, and list it under "Dropped after checking" with the counter-evidence, so a later round does not raise it again without new evidence. |
| Nothing settles it | Keep it as `unconfirmed`, phrased as a question that names what would settle it. An unconfirmed `blocking` finding keeps the verdict at REQUEST CHANGES; other unconfirmed findings do not affect it. |

- A fresh context makes a reviewer independent, not right. Substantiate its findings like any other.
- Evidence settles disagreement, not votes. Four lenses that saw nothing do not outweigh one reproduction. Two lenses sharing an unproven suspicion leave it unconfirmed.
- Counter-evidence is a line of code or a check result. "The implementation intends X" is not counter-evidence.
- When this context wrote or coordinated the code, it drops or downgrades a lens's blocking finding only on a check result; otherwise it reruns that lens fresh with the counter-evidence.
- A trigger that is hard to reproduce is a reason to investigate further, never a reason to lower the severity.

## Severity

| Severity | Means | Examples | What happens |
|---|---|---|---|
| `blocking` | The PR must not merge with it open. | An AC unimplemented or broken; an exploitable vulnerability; data loss or corruption; a crash on a supported path; a test that asserts the wrong behavior; an in-scope AC with no observed check. | Fixed in this PR. Only the user can waive it, in their own words, and a waived blocking finding makes the PR `human`. |
| `should-fix` | A confirmed problem that breaks no AC but has a real cost. | A defect on an edge path; a broken written project rule; a material inefficiency at the expected scale; a duplicate of an existing utility; a weak test that a named wrong implementation passes. | Fixed in this PR, or deferred to a tracked issue with a reason. |
| `nit` | An improvement with no defect behind it. | A clearer name within the rules; a tighter idiom; a better assertion message. | Optional. Never affects the verdict. |

- A confirmed defect in changed code is never a nit.
- Severity follows consequence, not the size of the diff or the effort of the fix. A one-line missing ownership check is blocking. A 400-line mechanical rename may carry only nits.
- A defect in code the diff does not touch becomes a follow-up issue. It does not affect the verdict unless the change makes it reachable or worse.
- An unconfirmed finding carries the severity it would have if confirmed, so the reader knows what is at stake. An unconfirmed `blocking` finding blocks APPROVE; other unconfirmed findings do not count toward the verdict.
- When the project defines its own review severities, map them onto these three and state the mapping once in the review.

## Category check

After synthesis, compare what the diff and the review show with the PR's category label. These areas make a PR `human` by default:

- authentication or authorization, crypto, secrets, payments, personal data;
- schema changes, migrations, backfills;
- breaking public API or contract changes;
- new or major-bumped dependencies;
- CI/CD, infrastructure, build or permission configuration;
- policy or instruction files (AGENTS.md, CLAUDE.md, CODEOWNERS);
- user-visible UI or visual changes, a default the user can flip in the autonomy contract.

These conditions always make it `human`:

- deleted tests or weakened assertions;
- an AC that was not observed;
- a waived blocking finding;
- a scope change;
- a self-review verdict;
- blocking findings that survive 3 full review rounds;
- an AC agreed as needing a human eye, reported `blocked (human eye)` with a screenshot.

The project's pull request policy and the autonomy contract can add areas to the defaults or release one, and neither releases an always-`human` condition. When the PR carries `review:agent` and the review shows one of these areas, say so in the review and hand the PR to `shipping-pull-requests` to relabel it `review:human`. When that skill is not installed, relabel it yourself. A category only escalates; a review never lowers it.

## Verdict

- `APPROVE` only when no confirmed `blocking` or `should-fix` finding and no unconfirmed `blocking` finding is open. A should-fix deferred to an issue with a link counts as not open. Settle an unconfirmed blocking finding with a check before the next round.
- `REQUEST CHANGES` otherwise.
- The verdict names the head SHA it was given on. Any later push voids it.
- A review that ran one lens at the user's request gives findings and no verdict.
- A review run as sequential passes in one context still gives a verdict, labeled self-review in the verdict line. In full mode, a self-review verdict makes the PR `human`.
- `APPROVE` is the skill's verdict, not permission to merge. The rest of the merge gate (required CI green on this SHA, a complete verification report, merge authorization in the autonomy contract) belongs to `shipping-pull-requests`.

## Post the review

Post the review as a comment review pinned to the reviewed SHA, with the verdict line first:

```text
gh api repos/{owner}/{repo}/pulls/<n>/reviews -f event=COMMENT -f commit_id=<reviewed-sha> -F body=@<review-file>
```

On GitLab, post a merge-request note whose verdict line names the reviewed SHA (`glab mr note <n> --message "$(cat <review-file>)"`). Other hosts have an equivalent. `gh pr review --comment` does not pin the review to the SHA you reviewed, so do not use it.

The merge gate counts only the latest review posted by the authorizing account whose first line is the verdict line, whose `commit_id` equals the current head, and whose verdict line names that same SHA. Any other review does not count.

- Never use the host's approve or request-changes state. Hosts refuse an approval from the PR's author, and GitHub also refuses a change request from the author. The agent acts with the user's credentials, so on the agent's own PR the author is the user. On someone else's PR, an approval from the agent would count toward branch protection as the user's own approval, which only the user may give.
- Put the verdict line first, then the findings grouped by severity. Keep the body under the host's comment limit (65,536 characters on GitHub) by writing nits one line each.
- Inline line comments are optional. On GitHub, one call to the reviews API posts the body and the inline comments together, pinned to the reviewed SHA: `gh api repos/{owner}/{repo}/pulls/<n>/reviews --input <review.json>`, with `commit_id` set to the head SHA, `event` set to `COMMENT`, the body, and a `comments` array of `path`, `line` and `body`. Keep every finding in the body as well, so the review reads on its own.
- Post on PRs the loop opened. On anyone else's PR, show the review to the user first and post only when they ask; a posted review speaks in the user's name.
- With no PR, append the round to `review.md` in the work-item folder under a `## Round N` heading and never rewrite an earlier round. Outside the loop, with no work-item folder, give the review in the conversation.

## Dispositions preserve history

| Status | Means |
|---|---|
| `open` | Confirmed and not fixed. |
| `unconfirmed` | A question. Blocks APPROVE only when its severity is `blocking`. |
| `fixed` | A fix commit exists; waiting for the recheck. |
| `closed` | The recheck passed at a named SHA. |
| `deferred` | A should-fix or nit moved to a tracked issue, with the link and the reason. |
| `rejected` | Refuted by counter-evidence, which is recorded. |
| `waived` | A blocking finding the user waived; quote their words. The PR becomes `human`. |

- IDs stay stable across rounds. A duplicate points to the canonical ID.
- Never delete a finding or rewrite its original evidence. Add the new status with the SHA and the reason.
- Close a finding only after a recheck: read the fix, rerun the trigger that exposed it, and check the neighboring behavior the fix could break. The implementer saying "fixed" is not a recheck.
- Reopen a closed finding on new evidence, or when a later push touches the fixed lines.
- A rejected finding returns only with new evidence.
- Defer only what falls outside this PR slice's scope; fix the rest here. A deferral needs the issue link, and without one the finding stays open. Open the issue with the host CLI (`gh issue create`) when the autonomy contract's Open issues field authorizes it. Opening PRs does not authorize opening issues. Otherwise ask the user, and keep the finding open until the issue exists.
- Say who rechecked a finding. A recheck in the implementer's own context is labeled self-review.
- Never lower the bar because the loop is taking long.

## Delta reviews

A delta review covers the changes since the reviewed head. Choose its lenses from what the delta touches:

| The delta | Rerun |
|---|---|
| Fixes confined to the lines of earlier findings | `intent`, plus each fixed finding's owning lens |
| New files or modules, public interfaces, a moved boundary | `architecture` |
| Input handling, auth, queries, file or network access, dependencies, CI or configuration | `security` |
| New or rewritten code beyond the fixed lines | `conventions` |
| Loops, queries, data volume, rendering or bundle | `efficiency` |
| A rewrite of the approach, or a delta larger than the reviewed diff | all five, as a fresh full review |

- `intent` runs in every delta review. It checks that each fix closes its finding and changes nothing else.
- Changes that came from the base branch, through a merge or a rebase onto a newer base, are not re-reviewed. Conflict resolutions are.
- Give each rerun lens the delta, the full diff for context, and the open findings to recheck, listed after its own review task.
- A lens that is not rerun keeps its earlier result, and the review says which round that result is from.

## Round limit

A round is one full-mode review of one head SHA, first or delta. When a blocking finding is still open after round 3, stop the fix loop and post the round with an Escalation section:

1. the finding, with its ID and evidence;
2. what each fix attempt changed, by SHA;
3. the reviewer's position and the implementer's, one or two sentences each;
4. the options the user has: fix differently, change the spec, or waive.

The review recommends human review, and the PR becomes `human`. Surviving three rounds is an escalation trigger, and escalating a category needs no approval.

## Scaling and models

- A docs-only PR (Markdown, documentation pages, code comments; no code, configuration or dependency change) gets the `intent` and `conventions` lenses only.
- When the PR head is the SHA of quick mode's clean pass (`intent: no findings at <sha>`), or differs from it only under `docs/product-engineering/`, reuse that intent result, labeled `from quick mode at <sha>`, and launch the other four. A quick-mode result that ran as self-review stays self-review.
- Every other PR gets all five lenses, however small. A one-line change can remove an ownership check, and a lens with nothing in scope costs one line.
- Use the strongest model the host offers for the `architecture`, `security` and `intent` lenses, which carry the most reasoning. The host's default model serves `conventions` and `efficiency`.
- A diff too large for one reviewer to read in full is a slicing problem. Say so in the review and recommend splitting the PR. When it cannot be split, split each lens by directory and merge the results during synthesis.

## Example: one ownership check across three rounds

**Round 1, full, at `a1b2c3d`.** The security lens finds that `PATCH /orders/:id` loads the order by ID and updates it without checking its owner. The evidence is a second-principal request against a local run: user B sends `PATCH /orders/<A's order ID>`, gets 200, and A's order changes. The intent lens reports the same defect through AC4, "only the owner can edit an order". Synthesis keeps one finding, F1, owned by security and `blocking`. The verdict is REQUEST CHANGES.

**Round 2, delta, at `e4f5a6b`.** The fix adds the ownership predicate and a test that B's request returns 404. Security and intent rerun. Security reads the handler: the predicate sits in the query that loads the order, before any write, and rerunning B's request returns 404 with A's order unchanged. F1 is closed at `e4f5a6b`. Intent notices that the new test asserts only the status code: a handler that writes first and rejects afterwards would pass it. That is F2, `should-fix`: assert that A's order is unchanged after B's request. The verdict is REQUEST CHANGES.

**Round 3, delta, at `c7d8e9f`.** The test now reads A's order after B's request. Intent removes the predicate in a scratch copy, sees the test fail for the right reason, and discards the copy. F2 is closed. The verdict is APPROVE at `c7d8e9f`.

**A later PR slice** adds `POST /orders/bulk-update`. Its security lens repeats the second-principal request against the new path. F1's test passing does not show that every path to an order checks ownership.
