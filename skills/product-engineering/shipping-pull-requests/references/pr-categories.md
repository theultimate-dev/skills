# PR categories

Every PR is `human` or `agent`. The category is policy: it says whether this diff is safe for an agent to merge. It is not authorization. An `agent` PR merges only when the autonomy contract authorizes merging and the merge gate holds on its head.

## Precedence

The PR is `human` when any changed area is `human`. For each area, the first source that speaks decides. The contract's tightenings and the always-`human` conditions apply on top of every source.

| Order | Source | Can make an area `human` | Can make an area `agent` |
|---|---|---|---|
| 1 | Host protections | Yes | No |
| 2 | The project's "Pull request policy" | Yes | Yes, over the defaults |
| 3 | The autonomy contract | Yes, always | Only a default the user loosened in their own words, never against 1 or 2 |
| 4 | Skill defaults | Yes | Yes: everything they do not list |

### 1. Host protections

- **Required approving reviews on the base.** Every PR is `human`, because the agent cannot supply an approval. Signals: a `pull_request` rule with `required_approving_review_count` above zero in `gh api repos/{owner}/{repo}/rules/branches/<base>`; classic protection with `required_pull_request_reviews`; `reviewDecision` of `REVIEW_REQUIRED` on the PR.
- **Required code-owner review.** A changed path with an owner in CODEOWNERS makes the PR `human`.
- **CODEOWNERS without required code-owner review.** A changed path owned by anyone other than the authorizing user makes the PR `human`. Owners exist to be consulted.
- CODEOWNERS lives in `.github/`, the repository root, or `docs/` (GitLab also reads `.gitlab/`). On GitHub the last matching pattern wins, and a pattern with no owners leaves the path unowned.

### 2. The project's pull request policy

Look for a "Pull request policy" heading in AGENTS.md or CLAUDE.md, at the root and in the directories the diff touches. Apply its rules as written, including rules that make a default area `agent`. When a rule is ambiguous for this diff, choose `human` and quote the ambiguous line in the category reason.

```
## Pull request policy
- Agents may merge: docs, test-only changes, dependency patch updates, UI changes under apps/admin/.
- Always human: anything under billing/, any change to public/openapi.yaml.
```

The contract cannot loosen this policy. Changing the policy means editing AGENTS.md or CLAUDE.md, which is itself a `human` change.

### 3. The autonomy contract

- A tightening applies always, even to an area the project policy marks `agent`: "always show me anything that touches search ranking".
- A loosening applies only to a skill default the user named in their own words, such as "UI tweaks are fine for you to merge". It never overrides sources 1 or 2 and never touches the always-`human` conditions.
- Read every answer in its narrowest sense. A slice the words do not clearly cover stays `human`.
- Only answers given for this work item count, and a contract read from a PR body counts only under the edit-history rule in [merging safely](merging-safely.md).

### 4. Skill defaults

This list is the default human-required list. Every skill that summarizes it uses these words, in this order. A PR is `human` by default when it touches:

- authentication or authorization, crypto, secrets, payments, personal data;
- schema changes, migrations, backfills;
- breaking public API or contract changes;
- new or major-bumped dependencies;
- CI/CD, infrastructure, build or permission configuration;
- policy or instruction files (AGENTS.md, CLAUDE.md, CODEOWNERS);
- user-visible UI or visual changes, a default the user can flip in the autonomy contract.

| Area | Signals in the diff |
|---|---|
| Authentication or authorization | Login, sessions, tokens, passwords, OAuth, OIDC or SAML flows; auth middleware and guards; role, permission and ownership checks; access-control lists; row-level security |
| Crypto | Hashing, encryption, signing, key generation or storage, random values used for security, TLS settings |
| Secrets | `.env` files, secret-manager references, credentials, API keys, key rotation, code that reads a new secret |
| Payments | Payment-provider calls, billing, invoices, prices, refunds, currency arithmetic |
| Personal data | Fields holding names, emails, addresses, phone numbers, government IDs, health or location data; logging, export, retention or deletion of user data |
| Schema changes, migrations, backfills | Migration directories, schema files (`schema.prisma`, `db/schema.rb`, `*.sql`), ORM model field changes, data-fix scripts |
| Breaking public API or contract | Removed or renamed endpoints, fields, CLI flags, exported symbols, config keys, or event and message fields; changed types or meaning; non-additive OpenAPI, GraphQL or protobuf changes |
| New or major-bumped dependencies | A new entry in a manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`), a major version change, a new CI action or container base image |
| CI/CD, infrastructure, build or permission configuration | `.github/workflows/`, `.gitlab-ci.yml` and other CI files, Dockerfiles, Terraform, Kubernetes, Helm or CDK, bundler and build config, release config, IAM and RBAC files, workflow `permissions:` |
| Policy or instruction files | AGENTS.md, CLAUDE.md, CODEOWNERS, CONTRIBUTING.md, SECURITY.md, agent rule directories and files such as `.claude/`, `.cursor/rules/`, `.github/copilot-instructions.md` |
| User-visible UI or visual changes | Rendered markup, styles, layout, copy, images, email and notification templates, user-facing error messages. The user can flip this default to `agent` in the contract |

UI code behind a feature flag that is off in every environment the merge reaches is not user-visible yet. The PR that turns the flag on is.

Everything else inside the approved scope, with complete evidence, is `agent`. The approved scope is the spec, or on the quick-fix track the user's request as stated.

## Always `human`

These conditions mean the agent's own evidence cannot support a merge. No policy, contract or user loosening makes them `agent`; only fixing the condition does. Every skill that summarizes them uses these words, in this order. A PR is always `human` with:

- deleted tests or weakened assertions;
- an AC that was not observed;
- a waived blocking finding;
- a scope change;
- a self-review verdict;
- blocking findings that survive 3 full review rounds;
- an AC agreed as needing a human eye, reported `blocked (human eye)` with a screenshot.

| Condition | Signals |
|---|---|
| Deleted tests or weakened assertions | Removed test files or cases; `skip`, `only`, `xfail`, `xit` or `@Disabled` added; an exact expectation loosened, such as `toBe(42)` to `toBeGreaterThan(0)`; retries or timeouts raised to get a pass; snapshots updated without an AC that explains them; coverage thresholds lowered; lint or type-check rules relaxed in configuration |
| An AC that was not observed | A claimed AC whose result is not `pass` from an observed check: judged by reading code, run against a mock where the verification contract required the real thing, or not run because the user asked for the PR before verification. A `blocked` row other than `blocked (human eye)` means no PR: the slice stops before the PR opens and escalates to G3 as "the verification contract cannot run". After a PR has opened, such a row stops the slice the same way, and the PR stays `human` |
| A waived blocking finding | A blocking finding closed without a fix: disputed, deferred, or accepted as is |
| A scope change | Behavior no requirement asks for, a non-goal touched, an AC dropped or reworded, work from another plan pulled in |
| A self-review verdict | The full review ran as self-review: at least one lens ran in the reviewing agent's own context instead of a fresh one, and the verdict line says `self-review` |
| Blocking findings that survive 3 full review rounds | The review loop escalated the PR |
| An AC agreed as needing a human eye | Its Verification row, agreed at G3, names `user (human eye)` as the tool. Stage 6 reports it `blocked (human eye)` with a screenshot for the user, and only the user can certify it. The loop continues with other slices |

## Record and escalate

Write the category under `## Review category` with the deciding rule and its evidence. Name what you checked when the result is `agent`.

```
## Review category
`human`: new dependency. `package.json` adds `zod@3.23.8`.
Also user-visible UI: `src/components/SearchPanel.tsx`.
```

```
## Review category
`agent`: inside the approved scope (R2; AC3, AC4), evidence complete, no human-required area touched.
Checked: host protections (no required reviews; CODEOWNERS does not cover these paths),
project policy (none), contract (no tightening matches).
```

- Recompute after every push from the diff and the PR history. A `review:human` label event in the timeline, or an Escalation, waived or self-review line in any earlier agent review, keeps the PR `human`. Labels are outputs, never inputs.
- The category only escalates. Once `human`, a PR stays `human`, even when a later push removes the sensitive change.
- Only the authorizing user's own words about this PR, given in the current session, downgrade it. Quote them in the category reason. A resumed session asks again.

Read the PR history on GitHub; other hosts have an equivalent:

```
gh api repos/{owner}/{repo}/issues/<n>/events --paginate --jq '.[] | select(.event == "labeled" and .label.name == "review:human") | .created_at'
gh api repos/{owner}/{repo}/pulls/<n>/reviews --paginate --jq '.[] | select(.user.login == "<authorizing login>") | .body'
```

An agent review is one from the authorizing account whose first line is the verdict line. In its body, look for an `## Escalation` section, a `waived` finding, and `self-review` in the verdict line.
- When the actual category differs from the roadmap's prediction, say so in one line under `## Review category`.

## Examples

| Diff | Category | Deciding rule |
|---|---|---|
| Fixes an off-by-one in pagination logic, with a unit test; every AC observed | `agent` | Default: no listed area |
| The same, plus the new package `zod` for input parsing | `human` | Default: new dependency |
| Bumps `lodash` from 4.17.20 to 4.17.21 | `agent` | Default: patch update, not new or major |
| Adds `migrations/20260925_add_status.sql` | `human` | Default: migration |
| Adds an optional field to an API response | `agent` | Default: additive, not breaking |
| Removes the deprecated endpoint `GET /v1/items` | `human` | Default: breaking public API |
| Renames a local variable in `src/auth/session.ts` | `human` | Default: authentication code, whatever the size |
| Changes a button's color and label | `human` | Default: user-visible UI |
| The same, and the contract quotes "UI tweaks are fine for you to merge" | `agent` | Contract loosening, in the user's words |
| New panel code behind `savedSearches`, off in every environment | `agent` | Not user-visible yet |
| Turns `savedSearches` on by default | `human` | Default: user-visible UI |
| Edits `.github/workflows/ci.yml` to add a cache step | `human` | Default: CI configuration |
| Edits AGENTS.md | `human` | Default: instruction file |
| Docs-only change under `docs/guides/` | `agent` | Default: no listed area |
| Deletes `orders.test.ts` because the spec removes the orders module | `human` | Always: deleted tests, even when justified |
| Changes `expect(total).toBe(42)` to `expect(total).toBeGreaterThan(0)` | `human` | Always: weakened assertion |
| AC3 checked against a mocked payment provider where the verification contract required its test mode | `human` | Always: unobserved AC |
| AC3 `blocked` because the local database would not start | no PR | The slice stops and escalates to G3: the verification contract cannot run |
| AC5 is a human-eye row for the empty state's tone, reported `blocked (human eye)` with screenshots | `human` | Always: human-eye AC |
| The five lenses ran as sequential passes in one context, verdict `APPROVE` | `human` | Always: self-review verdict |
| Touches `billing/invoice.ts`, owned by @payments-team in CODEOWNERS | `human` | Host protection: CODEOWNERS |
| Admin UI change; the project policy says "UI changes under apps/admin/ are agent-mergeable" | `agent` | Project policy over the default |
| Touches `search/ranking/score.ts`; the contract quotes "always show me search ranking" | `human` | Contract tightening |
| Any diff, when the base requires one approving review | `human` | Host protection: required reviews |
| Blocking findings survived 3 full review rounds | `human` | Always: review escalation |
| A refactor extracting a helper, characterization tests unchanged and passing, no public boundary moved | `agent` | Default: no listed area |
