# Tracks

How to place a work item on a track, what each track runs, and one worked request per track. Every name, path and number in the examples is invented.

## Contents

- Choosing between neighbors
- Quick fix
- Bugfix
- Small change
- Feature
- New app
- Refactor
- Spike
- Upgrading mid-track
- The autonomy contract on tracks without G4

## Choosing between neighbors

Classify from the request and a short look at the code it names. A two-minute read often moves a quick fix to a bugfix.

| Undecided between | Choose the first when | Choose the second when |
|---|---|---|
| Quick fix, bugfix | The location and the change are known, and nobody must decide behavior | The cause is unknown, or the fix needs a repro to prove it |
| Quick fix, small change | No user or caller sees new behavior. A copy, label or link change the request fully specifies is not new behavior | Users or callers get new behavior |
| Bugfix, feature | Restoring the intended behavior fits one PR | The fix needs new behavior or several PR slices. Wrong data alone stays a bugfix: ask whether repair is in scope; an in-scope backfill is its own `human` slice and goes to G4 |
| Small change, feature | One PR, one or two ACs, and one obvious approach | Several ACs, a consequential choice (data ownership, a public contract, a security boundary, a major dependency, cost), or more than one PR slice |
| Refactor, feature | No behavior a user or caller would notice changes | Any such behavior changes |
| Feature, new app | A codebase exists to extend | There is no codebase |
| Spike, G2 research | Only running code can answer the feasibility question | The code or a primary source answers it |

When two tracks stay plausible, take the larger one. Its extra gate costs one question; a missed gate costs rework.

## Quick fix

- **Signals:** a known location, no behavior decision, at most one AC. The request says what to change.
- **Gates:** none. Ask the authorization question at intake. When no `verification-profile.md` exists, find the start command first, then ask which environment is allowed, and how to start the app only when no start command was found.
- **Artifacts:** no `spec.md` and no roadmap. The intent, the check and the autonomy contract go in the PR body, where the contract counts only under the edit-history rule at the end of this file.
- **Branch:** the project's naming; the default is `<type>/<work-item-slug>`.
- **Path:** 0 → 5 → 6 → 8 → 9 → 10. No quick review: the full review on the PR covers it, with the lenses scaled to the diff.

**Example.** "Fix the broken link to the API reference in `docs/guides/export.md`."

1. **Stage 0.** The link points to `docs/api/export.md`, which was renamed to `docs/reference/export-api.md`. Quick fix. `.github/workflows/docs.yml` publishes the docs site on every push to `main`, so a merge deploys. The request says nothing about merging, so ask: "May I commit, push and open a PR, and squash-merge it if it qualifies for `agent` review? UI and copy changes wait for your review by default; may I merge those too? May I open issues for follow-ups I defer? A merge to `main` publishes the docs site. May a merge deploy it?" The user answers: "Yes to all, docs deploys are fine."
2. **Stage 5.** `implementing-plans` fixes the link on `docs/export-guide-link` and commits.
3. **Stage 6.** `verifying-implementation` derives the check from the intent and says so on its Contract line. It builds the docs site and follows the link in the built page: the target heading "Export API" is present. The docs link checker passes on the SHA.
4. **Stage 8.** `shipping-pull-requests` opens the PR with the intent, the report, and the `## Autonomy contract` block quoting the user. Category: `agent`, a docs-only change under `docs/guides/`.
5. **Stage 9.** A docs-only PR gets the `intent` and `conventions` lenses. Verdict `APPROVE`.
6. **Stage 10.** The gate holds and the deploy is authorized in the user's words: squash-merge pinned to the head, then watch the docs deploy and report its result.

## Bugfix

- **Signals:** observed wrong behavior.
- **Gates:** G1 is skipped when the report gives repro steps and the expected result, and the repro reproduces on the base; the short spec says `Status: agreed (G1 skipped: repro reproduced at <short-sha>)`. A repro that does not reproduce is a high-impact unknown: ask for the missing condition. When stored data is now wrong, ask whether repairing it is in scope; an in-scope backfill is its own `human` slice and goes to G4. G2 runs only when the fix options differ in behavior, risk or reach, such as patching one endpoint versus fixing a helper three endpoints share; otherwise the fix is one line under Approach. The repro is AC1 and the first G3 row, and it must fail on the base for the reported reason. Present what the bugfix needs in one message, with the authorization question.
- **Artifacts:** a short `spec.md` (Problem with the repro, expected versus actual and blast radius; R1; AC1; the Approach line; the Verification rows; a `## Plan` heading holding only the autonomy contract from the intake answer). No roadmap. A fix that needs more than one PR slice goes to G4 for a roadmap.
- **Branch:** default `fix/<work-item-slug>`.
- **Path:** 0 → short spec → 5 with the failing check first → 6 → 7 → 8 → 9 → 10.

**Example.** "`GET /api/products?page=2` repeats the last product of page 1. Steps: seed 25 products, request pages 1 and 2 with the default page size of 20."

1. **Stage 0.** The handler in `src/api/products/list.ts` computes the offset as `(page - 1) * size - 1`. The repro reproduces on the base at `b71e0d4`: 24 distinct products. Bugfix, one sensible fix, no damaged data.
2. **One message.** The short spec at `docs/product-engineering/products-pagination-overlap/spec.md`, with `Status: agreed (G1 skipped: repro reproduced at b71e0d4)` and AC1 (R1): "Following the repro, pages 1 and 2 return 25 distinct products, 20 on page 1 and 5 on page 2." Approach: "Compute the offset as `(page - 1) * size`." The G3 rows: an `api` row driven with curl and an `integration` test. The authorization question. The user answers: "Fine. Commit, push, open the PR, and merge it if it's agent." The spec's `## Plan` section records that answer as the autonomy contract; the unanswered fields, such as opening issues, read `not authorized`.
3. **Stage 5.** On `fix/products-pagination-overlap`, `implementing-plans` writes the test first. It fails on the base with 24 distinct products, the reported reason. Then the one-line fix, and the test passes. The commit also carries `spec.md`.
4. **Stage 6.** The repro row fails on the base SHA and passes on the candidate SHA; the report records both.
5. **Stages 7 to 10.** No quick-review findings. Category `agent`: the fix restores the documented behavior and touches no listed area. Full review: all five lenses run, none finds anything, and the verdict is `APPROVE`. The gate holds and the PR merges.

## Small change

- **Signals:** new behavior, one PR, no consequential choice.
- **Gates:** G1 to G4 in one message. `specifying-work-items` runs one interview round, two at most, and leaves the confirmation to that message.
- **Artifacts:** `spec.md` with its `## Plan` section: one PR slice, the predicted category, the branch, the tasks, and the autonomy contract with every field of the roadmap's. No roadmap and no plan files.
- **Branch:** the `Branch:` field of the `## Plan` section, default `<type>/<work-item-slug>`.
- **Path:** 0 → 1 to 4 in one message → 5 → 6 → 7 → 8 → 9 → 10.

**Example.** "Add a Copy link button to the share dialog."

1. **Stage 0.** The dialog lives in `web/share/ShareDialog.tsx`, and `useClipboard` in `web/lib/clipboard.ts` already copies text elsewhere. One behavior, one PR, an obvious approach. Small change.
2. **Interview.** One round: should the button also close the dialog? The user: "No, keep it open."
3. **One message.** R1 and two ACs: AC1 (R1) "Clicking Copy link puts the share URL on the clipboard and shows 'Link copied' for 2 seconds"; AC2 (R1) "The button is reachable with Tab and activates with Enter". Approach: reuse `useClipboard`. Verification: two `e2e` rows through a browser-driving tool. Plan: one PR, predicted `human` because it is user-visible UI, branch `feat/share-copy-link`. The autonomy questions. The user answers: "Agreed. Commit, push and open the PR. I'll review UI myself."
4. **Stages 5 to 9.** Built, driven in the browser, quick-reviewed, and opened as `review:human`. The full review verdict is `APPROVE`.
5. **Stage 10.** `human` path: reviewers requested, a handoff comment posted. The finish report lists the PR under "Awaiting you", because it is user-visible UI.

## Feature

- **Signals:** several ACs, a consequential choice, or more than one PR slice.
- **Gates:** G1 to G4, one at a time, each through its skill.
- **Artifacts:** `spec.md`, a decision record when G2 fixes something consequential, `roadmap.md` with the autonomy contract, and `plans/NN-slug.md`.
- **Branch:** the plan file's `Branch:` line for each PR slice, default `<type>/<work-item-slug>-<NN>[-p<phase>]`.
- **Path:** 0 → 1 → 2 → 3 → 4, then 5 to 10 for each PR slice in the roadmap's order.

**Example.** "Build saved searches with email alerts."

1. **G1.** Three interview rounds settle who can save searches, the limit per user, how often alerts go out, and that the user reviews the email's look. Twelve ACs.
2. **G2.** Two approaches for alerts: a daily job that reruns each saved search, or matching new products against saved searches as they are published. The user picks the daily job. The new `saved_searches` table fixes persistent data ownership, so it gets a decision record.
3. **G3.** The profile exists, so G3 confirms the AC-to-check mapping. The profile has no mail catcher, so G3 proposes Plan 0: add one to the compose file. The email's look is a human-eye row.
4. **G4.** The roadmap:

   | Plan | Phases | PR slices | Predicted category | Depends on |
   |---|---|---|---|---|
   | `plans/00-verification-harness.md` | p1 mail catcher in the compose file | whole plan | `human`: infrastructure | none |
   | `plans/01-storage-and-api.md` | p1 migration adding `saved_searches`; p2 repository, endpoints, tests | per phase | p1 `human`: migration; p2 `human`: authorization (owner checks on every endpoint) | none |
   | `plans/02-saved-searches-panel.md` | p1 panel behind `savedSearches`, off by default; p2 flag on | per phase | p1 `agent`: off in every environment; p2 `human`: UI | 01-p2 |
   | `plans/03-email-alerts.md` | p1 alert job and email template | whole plan | `human`: user-visible email | 00, 01-p2 |

   No merge to `main` deploys. Stacking is expected, so G4 asks about force-pushing too. The user approves: "Approved. Commit, push and open the PRs, force-push your own branches after a rebase, and merge the agent ones yourself, squash." The contract records it.
5. **First pass.** 00 and 01-p1 open first, both `human`, and wait. 01-p2 stacks on 01-p1, runs stages 5 to 9, and opens as `human`. 02-p1 and 03-p1 depend on 01-p2, which is itself stacked, so they would sit two levels deep: they pause. Nothing independent is left, so the loop ends with a finish report: 00, 01-p1 and 01-p2 await you, 01-p2 behind 01-p1.
6. **Resume.** The user merges 00 and 01-p1 and says "resume the work on saved searches". The host shows both merged. 01-p1 was squash-merged, so 01-p2 is rebased onto `main`, force-pushed with a lease as the contract allows, and retargeted; CI and verification rerun on its new head, and it gets a delta review. It waits for the user again, now based on `main`, so 02-p1 and 03-p1 may stack on it one level deep.
7. **Parallel.** 02-p1 (`web/search/`) and 03-p1 (`jobs/alerts/`, `templates/email/`) touch disjoint files and consume the same settled contract, so they run in parallel worktrees, each stacked on 01-p2. Once the user merges 01-p2, both are rebased onto `main` and retargeted, and 02-p1 merges through the gate. 03-p1 then updates from the new base, reruns its affected checks, gets a delta review, and waits as `human`. 02-p2, the flag flip, opens as `human`.
8. **Finish report.** Merged: 00, 01-p1 and 01-p2 by you, and 02-p1 through the gate. Awaiting you: 03-p1 (user-visible email; screenshots of the email in the report), 02-p2 (turns the panel on for users).

## New app

- **Signals:** no codebase.
- **Gates:** G1 to G4. When the product or UX is unresolved, recommend `guiding-product-discovery` from the `product-design` plugin first and resume from its handoff; without it, `specifying-work-items` runs a short interview labeled "Product interview". G2 chooses the stack, hosting and data store, and starts the decision log with the stack decision; it lands in the walking-skeleton PR. G3 designs the verification harness, and the profile marks unbuilt parts `planned`.
- **Artifacts:** as for a feature. Plan 1 is a walking skeleton: the smallest runnable app, CI that builds, lints and tests it, and the verify entry point. It is `human`: new dependencies and CI configuration.
- **Repository:** a new repository has no base branch to open a PR against. Ask: "New app without a repository: may I create it (host, owner/name, visibility) and push an initial commit, or will you?" The walking skeleton then lands as the first PR.
- **Path:** product-design when product or UX is unresolved → 1 → 2 → 3 → 4 → 5 to 10 for the skeleton, then for each capability plan.

**Example.** "Build an internal tool to track equipment loans; we have no code yet."

1. **Stage 0.** No repository and no product brief. Ask the repository question; the user answers: "Create it on our GitHub org as equipment-loans, private." The flows (who borrows, who approves, what happens when an item is late) are open, so recommend `guiding-product-discovery`. The user answers the product questions there, and its handoff comes back with R and AC IDs.
2. **G1.** The engineering interview: company single sign-on, about 400 items, hosting on the company's existing cloud account, personal data limited to names and work emails.
3. **G2.** Three stacks compared; the user picks a server-rendered web app with a relational database on the existing cloud account. The stack decision starts the decision log; it lands in the walking-skeleton PR.
4. **G3.** The harness is designed: a test runner, a browser-driving tool for `e2e`, a seed script, a `verify` script, and CI on pull requests.
5. **G4.** Plan 1, the walking skeleton, `human`. Plan 2, the item catalog. Plan 3, borrowing and returns. Plan 4, overdue reminders.
6. **Loop.** Plan 1's PR waits for the user. Plans 2 onward need its code and CI, so plan 2 stacks on it one level deep and the rest wait. After the user merges plan 1, the loop continues. Slices that touch sign-in or the name and email fields stay `human`; the rest are `agent` wherever the defaults allow.

## Refactor

- **Signals:** no intended behavior change.
- **Gates:** G1 lists the invariants: behavior, public contracts, data, the performance envelope. Each invariant is a requirement with its own AC. G2 runs only when the target structure is consequential; otherwise the target is one paragraph under Approach. G3 plans characterization tests and before/after journeys, captured on the base SHA before the first edit. Their pass condition is no observable difference.
- **Artifacts:** as for a feature. The first phase captures the characterization tests and journeys.
- **Category:** `agent` while the invariants hold, no public boundary moves, and no default human area is touched; the PR that adds a dependency is `human` and stands alone. A phase that moves a public export is `human` and stands alone too. A changed characterization test is a weakened assertion, which makes the PR `human`.
- **Path:** 0 → 1 → (2) → 3 → 4 → 5 to 10 for each small mechanical PR.

**Example.** "Split the 2,000-line `orders/service.ts` into modules without changing behavior."

1. **G1.** Invariants: the exports of `orders/service.ts`, every `/api/orders` response, the stored order format. Three Rs, three ACs.
2. **G2.** Skipped: the target is one paragraph, "one module per responsibility: pricing, fulfilment, notifications; `orders/service.ts` re-exports them".
3. **G3 and G4.** Plan 01: p1 characterization tests and captured journeys; p2 to p4 move one responsibility each. All predicted `agent`.
4. **Loop.** Each phase is its own PR, verified by rerunning the characterization suite and the journeys against what was captured on the base. Each merges through the gate. When p3 turns out to need a renamed public export, that breaks the first invariant: stop and return to G1. When the user accepts the rename, it becomes its own `human` phase, because it is a breaking contract change.

## Spike

- **Signals:** feasibility is unknown, and neither the code nor a primary source settles it.
- **Gates:** the question, the timebox and the exit observation are agreed with the user. A standalone spike needs no spec: take the question from the request. In the same question as the timebox, ask whether you may commit and push the spike branch. No G3, no G4, no verification report, no review, no PR for merge.
- **Limits:** run only against local services and provider test modes, or the environments the verification profile allows. Never production, real email, payments or webhooks.
- **Artifacts:** the findings in `docs/product-engineering/<slug>/spike.md` on the spike branch: the question, the answer, the command and output that support it, the branch and the commit, the approach it points to, and the user's authorization answer. Inside a work item they also go into the comparison and the Approach section's evidence at G2.
- **Branch:** default `spike/<work-item-slug>-<topic>`. Never merged, so `spike.md` never reaches the base.
- **Path:** `brainstorming-solutions` scopes the spike; `implementing-plans` builds it on the spike track and writes `spike.md`. Inside a work item, G2 uses the findings. A standalone spike stops there and offers a work item whose G2 uses them.

**Example.** "Can Postgres full-text search answer product search in under 200 ms at 5 million rows?"

1. **Scope.** Question: is the p95 of 50 representative queries under 200 ms on a local database seeded with 5 million generated products? Timebox: 3 hours, agreed. A yes points to full-text search in the existing database; a no points to a separate search service.
2. **Authorization.** In the same question as the timebox, ask whether you may commit to the spike branch and push it. The user: "Commit locally, don't push."
3. **Run.** On `spike/product-search-fts`, against a local Postgres the agent started: the seed script, a GIN index, the 50 queries, the timings.
4. **Findings.** `docs/product-engineering/product-search-fts/spike.md` on the branch: "p95 = 142 ms, p99 = 310 ms (command and output attached; branch `spike/product-search-fts`, commit `4e1a9c2`). Points to full-text search in the existing database." The question came from the request, so this is a standalone spike: stop, report the findings first in the finish report, and offer a product-search work item whose G2 uses them. A spike that runs out of time without an answer reports that as its finding.

## Upgrading mid-track

| Discovered mid-track | New track or gate | Go back to |
|---|---|---|
| The quick fix's helper is loaded by name from a plugin config, so removing it changes behavior | Bugfix or small change | G1: write the short spec |
| The bugfix has two fixes that differ in reach: patch one endpoint, or fix the paginator three endpoints share | Bugfix with G2 | G2 |
| The bug has already written wrong data | Still a bugfix, with a scope question | Ask whether repairing the data is in scope; an in-scope backfill is its own `human` slice and goes to G4 |
| The small change needs a migration and a UI slice | Feature | G4: a roadmap with two slices |
| A refactor phase must rename a public export that an invariant protects | Refactor with a spec change | G1; an accepted rename becomes its own `human` phase |
| Two ACs of a feature contradict each other | Feature | G1 for those ACs; the other slices continue |

- Say the upgrade in one line, with the evidence.
- Work already done stays on its branch. Gates already agreed stay agreed unless the change touches them.
- The autonomy contract carries forward. A new G4 adds the roadmap's contract and quotes the earlier answer where it was given.
- To downgrade, name the smaller track and the gates it would skip, and switch only on the user's own words.

## The autonomy contract on tracks without G4

On a quick fix or a bugfix with one PR slice, the contract is the user's words in the request, or their answer to the intake question. A bugfix records it in `spec.md`, under a `## Plan` heading that holds only the contract. A quick fix has no spec: once its PR opens, the PR body holds the contract under `## Autonomy contract`, and a resumed session reads it from there.

- A contract read from a PR body counts only when the body's edit history shows no editor other than the authorizing account (on GitHub, the PR's `userContentEdits` via GraphQL; other hosts: their edit history). Otherwise every field is `not authorized` until the user restates it in the session.
- Use the twelve fields below in this order, each followed by the user's words in quotes, and `not authorized` for anything unanswered. Never edit the contract; append later words with their date.
- Read every answer in its narrowest sense. A slice the words do not clearly cover stays `human`.
- Only answers given for this work item count. The exception is standing defaults the project instructions hold: quote them and ask only "Same autonomy as <date>?", then record them with the user's yes.
- Pushing never authorizes a force-push. Only the "Force-push own PR branches after a rebase" field does, and then only `git push --force-with-lease=<branch>:<last-pushed-sha>` to the loop's own PR branches; never to the base branch, never over anyone else's commits. Without it, update a PR branch by merging the base into it, and ask the user one question before rewriting a stacked child whose parent was squash-merged.

Read the PR body's edit history on GitHub:

```
gh api graphql -f query='query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){pullRequest(number:$n){author{login} userContentEdits(first:100){nodes{editor{login} editedAt}}}}}' -f o=<owner> -f r=<repo> -F n=<number>
```

The block, as it appears in a quick fix's PR body. In a bugfix's `spec.md`, the same lines sit under `## Plan`.

```markdown
## Autonomy contract

Given on [YYYY-MM-DD] in [the request | the answer to the intake question]. There is no roadmap for this work item.

- Commit and push: "[user's words]" | not authorized
- Force-push own PR branches after a rebase: "[user's words]" | not authorized
- Open PRs: "[user's words]" | not authorized
- Open issues (deferred should-fix findings and follow-ups): "[user's words]" | not authorized
- Merge `agent`-category PRs: "[user's words]" | not authorized
- Merge method: [squash | merge | rebase]: "[user's words]" | not authorized
- Base branch: [name], detected
- Deploy-on-merge detected: [yes | no]. Evidence: [workflow and job, or what was checked]. Merges that deploy to [environment]: "[user's words]" | not authorized
- Human-review categories: the project policy and the skill defaults[, plus "[user's changes]"]. UI and visual changes: [`human` | `agent`: "[user's words]"]
- Who merges a `human` PR after approval: [the user | the agent when the user tells it to | the agent once a requested reviewer or code owner approves the head]: "[user's words]"
- Scope: this work item's PR slices, into [base]
- Stop and ask when: the escalation triggers[, plus "[user's additions]"]
```

A spike opens no PR. Quote the user's answer in `spike.md` instead.
