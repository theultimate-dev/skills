<!-- Title: the resulting change, in the project's commit or PR title convention, for example "feat(search): add saved searches". Merge these sections into the repository's own PR template when it has one. Keep the body well under 65,536 characters: evidence as text, screenshots and traces by CI-artifact name or local path. Delete this comment. -->

## Summary

[The problem or trigger, in one sentence. The resulting behavior, in one or two.]

- Plan: `docs/product-engineering/[work-item-slug]/plans/[NN-slug].md`, [phase N | whole plan]
- Stacked on: [#parent, which merges first | none]

## Requirements covered

| ID | In this PR |
|---|---|
| R1 | AC1, AC2 pass |
| R2 | AC3 progress only; passes in [plan NN, phase N] |

## Verification

Ran on commit `[sha]` in [environment] on [YYYY-MM-DD].

| AC | Result | What was done | What was observed |
|---|---|---|---|
| AC1 | pass | [The steps actually performed] | [What the software showed or returned, quoted] |
| AC2 | pass | [...] | [...] |

- Automated checks: [command: result]
- Exploratory notes: [edge, error and empty states; persistence after reload or restart; console and network errors; keyboard; responsive]
- Blocked: [none | each `blocked (human eye)` AC with its screenshot path; it makes this PR `human`. Any other `blocked` row stops the slice before the PR opens]
- Evidence files: [CI artifact names or local paths]

## Review category

`[agent | human]`: [the deciding rule and its evidence, for example "new dependency: `package.json` adds `zod`"]

## Reviewer focus

- [The one to three places where human judgment adds value, and why. For an `agent` PR: what a later reader should know.]

## Autonomy contract

<!-- Only on a quick fix, which has no roadmap.md and no spec.md. Otherwise delete this section: a bugfix keeps its contract under `## Plan` in spec.md. Quote the user's own words; write "not authorized" for anything unanswered. Never edit it later: append new words with their date. This block counts only while the body's edit history shows no editor other than the authorizing account (on GitHub, the PR's `userContentEdits` via GraphQL; other hosts: their edit history); otherwise every field is `not authorized` until the user restates it in the session. -->

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
