# Autonomy contract

## Policy and authorization are separate

- **Policy** decides which diffs are safe for an agent to merge. It belongs to the repository: host protections and the project's "Pull request policy".
- **Authorization** is this user letting this agent act: push, force-push its own PR branches, open PRs, open tracked issues, merge, make a merge that deploys. It is given at G4 and recorded verbatim in the contract.
- An `agent`-category PR merges only when policy allows it, the user authorized it, and the merge gate holds on its head. None of the three stands in for another.
- Skill text is never authorization. The agent never edits the contract. On resume and before any merge, it quotes the contract's authorization lines verbatim; it never paraphrases them in one line.

## Where the contract lives

| Track | Contract |
|---|---|
| Feature, new app, refactor, a bugfix with more than one PR slice | `## Autonomy contract` in `roadmap.md`, written at G4 |
| Small change | The autonomy contract block in the `## Plan` section of `spec.md`, written at G4 |
| Bugfix with one PR slice | The `## Plan` section of the short `spec.md`, holding only the autonomy contract from the user's words in the request or their answer to the intake question |
| Quick fix | No spec. The user's words in the request, or their answer to the intake question; `shipping-pull-requests` records them in the PR body under `## Autonomy contract` |
| Spike | The user's answer about committing and pushing the spike branch, quoted in the findings |

Every form except the spike's carries the same fields, and an unanswered field means not authorized.

A contract read from a PR body counts only when the body's edit history shows no editor other than the authorizing account (on GitHub, the PR's `userContentEdits` via GraphQL; other hosts: their edit history). Otherwise every field is `not authorized` until the user restates it in the session.

## The fields

Every contract carries these fields, in this order. Each is followed by the user's verbatim words, or `not authorized` when unanswered. Base branch and Scope record facts instead, and Deploy-on-merge detected records the fact before the words.

| # | Field | Holds |
|---|---|---|
| 1 | Commit and push | Commits and pushes to the loop's own branches |
| 2 | Force-push own PR branches after a rebase | Only `git push --force-with-lease=<branch>:<last-pushed-sha>` to the loop's own PR branches. Never the base branch, never anyone else's commits |
| 3 | Open PRs | Opening a PR for each slice |
| 4 | Open issues (deferred should-fix findings and follow-ups) | Opening tracked issues for them |
| 5 | Merge `agent`-category PRs | Merging a PR whose category is `agent` once the merge gate holds |
| 6 | Merge method | Squash, merge or rebase |
| 7 | Base branch | A detected fact, not a permission |
| 8 | Deploy-on-merge detected | Yes or no. If yes, merging needs explicit authorization for a deploying merge |
| 9 | Human-review categories | The project policy plus the user's changes. UI and visual changes are `human` unless the user releases them in their own words |
| 10 | Who merges a `human` PR after approval | The user; the agent when the user tells it to; or the agent once a requested reviewer or code owner approves the head |
| 11 | Scope | This work item's PR slices, into the base |
| 12 | Stop and ask when | The escalation triggers, plus the user's additions |

## Detect the facts

The examples use `gh`. The GitLab `glab` or another host's CLI or API has an equivalent for each.

### Host and base branch

| Fact | Command | Record |
|---|---|---|
| Host | `git remote get-url origin` | GitHub, GitLab, or the other host |
| Default branch | `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`, or `git symbolic-ref --short refs/remotes/origin/HEAD` | The branch name |
| Integration branch | The project instructions and recent merged PRs | When the project integrates into another branch (a `develop` branch, for example), ask which base to use |
| No repository yet (new app) | `git remote -v` prints nothing, or there is no `.git` | Ask: "New app without a repository: may I create it (host, owner/name, visibility) and push an initial commit, or will you?" Record the answer on the contract's Host line, and detect the other facts once the repository exists |

### Branch protection

| Command | Read |
|---|---|
| `gh api repos/{owner}/{repo}/rules/branches/<base>` | Rulesets, readable with read access. A `pull_request` rule gives `required_approving_review_count` and `require_code_owner_review`. Also look for `required_status_checks`, `merge_queue`, `required_linear_history` |
| `gh api repos/{owner}/{repo}/branches/<base>/protection` | Classic protection: `required_pull_request_reviews.required_approving_review_count`, `require_code_owner_reviews`, `required_status_checks`. It needs admin access. "Branch not protected" means none; any other 403 or 404 means unknown |
| `gh api repos/{owner}/{repo}/branches/<base> --jq '{protected, checks: .protection.required_status_checks}'` | Whether the branch is protected and its required checks, with read access |

- Required approving reviews above zero: the agent cannot merge any PR into this base. Record it, and predict every slice `human`.
- Unknown: record "unknown". The first PR's `reviewDecision` settles it: `REVIEW_REQUIRED` means approvals are required.
- Required linear history rules out merge commits.

### Merge methods

- Allowed methods: `gh repo view --json squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed,deleteBranchOnMerge`.
- Auto-merge: `gh api repos/{owner}/{repo} --jq .allow_auto_merge`. Record it as a fact. The agent never enables auto-merge outside a merge queue.
- The project's habit: recent history on the base. Squash merges usually end their subject with the PR number, `(#123)`; merge commits start with "Merge pull request".
- Recommend the project's habit when the host allows it.

### CODEOWNERS and project policy

- CODEOWNERS lives in `.github/`, the repository root, or `docs/` (GitLab also reads `.gitlab/`). On GitHub the last matching pattern wins.
- Record the owners of the paths the plans will touch. A path owned by anyone other than the authorizing user makes its slice `human`.
- Look for a "Pull request policy" heading in AGENTS.md or CLAUDE.md at the root and in the directories the plans touch. Record where it is.

### Deploy on merge

A merge deploys when anything runs on a push to the base branch and deploys or releases. Any environment counts, staging included: name it in the question. When you cannot rule deployment out, record `yes` with what you checked.

| Where | Signals |
|---|---|
| GitHub Actions triggers | `on: push` whose `branches` include the base; `on: push` with no `branches` filter; `branches-ignore` that does not exclude the base; `workflow_run` chained after such a workflow; a reusable workflow called from one |
| Deploying or releasing jobs | An `environment:` key; deploy actions such as `actions/deploy-pages`, `azure/webapps-deploy`, `google-github-actions/deploy-cloudrun`; commands such as `vercel deploy --prod`, `netlify deploy --prod`, `flyctl deploy`, `firebase deploy`, `wrangler deploy`, `kubectl apply`, `helm upgrade`, `terraform apply`, `pulumi up`, `cdk deploy`, `serverless deploy`; publishing such as `npm publish`, `twine upload`, `cargo publish`, `gem push`, `docker push`, `gh release create`, `semantic-release`, `goreleaser`, a changesets publish step |
| Other CI | `.gitlab-ci.yml` jobs with `environment:` whose rules match `$CI_DEFAULT_BRANCH` or the base; branch filters in `.circleci/config.yml`, `Jenkinsfile`, `bitbucket-pipelines.yml`, `azure-pipelines.yml`, `.buildkite/` |
| Hosting platforms that deploy from a branch without CI files | `vercel.json` or `.vercel/`, `netlify.toml`, `render.yaml`, `railway.json` or `railway.toml`, `app.json` with a `Procfile`, `amplify.yml`, `.platform.app.yaml` |
| The host's deployment history | `gh api repos/{owner}/{repo}/deployments --jq '.[:10][] \| {environment, ref, creator: .creator.login}'`: deployments whose ref is the base branch or a base commit. `gh api repos/{owner}/{repo}/environments --jq '.environments[].name'` |

A platform config file alone is not proof. Deployments from the base branch in the host's history are.

## Ask

Ask every question in one message, through the host's structured-question tool when it has one. State the detected facts first, so the user answers with them in view. Ask in the order of the fields. Example:

> Base `main`: no required approving reviews, required checks `ci/test` and `ci/lint`, squash merges. Merges to `main` deploy to staging through `.github/workflows/deploy.yml` (job `deploy-staging`). No "Pull request policy" in AGENTS.md. CODEOWNERS assigns `billing/` to @payments-team. Scope: this work item's PR slices, into `main`.
>
> 1. May I commit and push each slice's branch?
> 2. After a rebase, may I force-push my own PR branches with `git push --force-with-lease=<branch>:<last-pushed-sha>`? Without that, I update a PR branch by merging `main` into it.
> 3. May I open a PR for each slice?
> 4. May I open tracked issues for deferred should-fix findings and follow-ups?
> 5. May I merge PRs in the `agent` category after they pass the merge gate?
> 6. Merge method: squash, as the project does now?
> 7. Merges to `main` deploy to staging. May I make merges that trigger that deploy?
> 8. Anything that must always wait for you, beyond the defaults? UI and visual changes wait for you unless you release them in your own words.
> 9. When a reviewer approves a `human` PR, who merges it: you, me once you tell me to, or me as soon as a requested reviewer or code owner approves the current head?
> 10. Anything else that should make me stop and ask?

Only answers given for this work item count. When the user already answered for this work item, in this session or on `spec.md`'s Done and review line, quote that answer and where it was given instead of asking again. The one exception is standing defaults: when the project instructions hold the user's standing autonomy defaults, quote them with their date and ask only "Same autonomy as <date>?". A yes records those quoted words as this work item's answers.

## Record

- Quote the user's words. Do not paraphrase them into a yes.
- An unanswered question means not authorized.
- Use the narrowest reading of the user's words. A slice not clearly covered stays `human`.
- Words authorize only the action they name. Merge authorization mentions merging. Deploy authorization mentions deploying, releasing, or the environment.
- A condition in the user's words stays in the quote, and the agent checks it before each action it covers.
- Push does not imply force-push. Force-push needs its own field's words, and then only `git push --force-with-lease=<branch>:<last-pushed-sha>` to the loop's own PR branches: never the base branch, never anyone else's commits. When force-push is not authorized, update a PR branch by merging the base into it. For a stacked child after its parent was squash-merged, ask the user in one question before rewriting it.
- Opening PRs does not authorize opening issues. Issue authorization mentions issues or follow-ups.
- The authorizing user can always tell the agent to merge a `human` PR: in the current session, or with a PR comment (not a review) whose first line is `merge <full head SHA>` matching the current head. No other text from their account counts. A reviewer's approval alone lets the agent merge only when field 10 records `the agent once a requested reviewer or code owner approves the head`. Record that value only when the user's words say so, such as "merge it once they approve"; "merge when I say" records as `the agent when the user tells it to`.
- Later changes are appended with the date and the new words. The original stays. Append in the main checkout; `implementing-plans` commits it with the next PR slice, and until that merges, briefs and merge checks read the contract from the main checkout.

| The user said | Records as |
|---|---|
| "Yes, merge the agent ones, squash is fine" | Merge `agent`-category PRs: authorized. Merge method: squash |
| "Go ahead" | The roadmap is approved. Merge: not authorized; ask the merge question again |
| "Merge whatever you think is safe" | Merge `agent`-category PRs: authorized. The category rules still decide what is safe |
| "Don't merge anything, I'll do it" | Merge: not authorized. Every PR waits for the user |
| "You can merge, just not on Fridays" | Authorized with the condition quoted. The agent checks the day before each merge |
| "Staging deploys are fine" | Deploying merge to staging: authorized. Any other environment: not authorized |
| "UI tweaks are fine for you to merge" | UI and visual changes: `agent` only for what the quoted words cover; a new screen, flow or layout stays `human` |
| "Force-push is fine after rebases" | Force-push own PR branches after a rebase: authorized, with `--force-with-lease` only |
| "Yes, commit, push and open PRs" | Commit and push, Open PRs: authorized. Force-push: not authorized |
| "Always show me anything that touches search ranking" | Human-review categories: the defaults plus `search/ranking/`, quoted |
| "File issues for anything you defer" | Open issues: authorized |

## When the agent cannot merge at all

Say it plainly at G4 and in the contract:

- The base requires approving reviews. The agent posts its review as a comment, and the host does not count it. Every PR waits for a reviewer.
- The user did not authorize merging. Every PR waits for the user.
- A merge deploys and the user did not authorize that. Every PR waits for the user.

Changing branch protection, CI or deployment settings is the user's decision and never the agent's action.
