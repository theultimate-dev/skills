---
name: preparing-pull-requests
description: "Prepare coherent commits and a concise pull request from verified engineering work, then publish within authorization and check CI against the current PR revision. Use when an implementation initiative is ready for reviewer handoff or an existing PR needs repair and updated evidence."
license: MIT
---

# Preparing pull requests

Deliver a technically ready PR that the user can review efficiently. Keep technical readiness, remote publication, required human approval, and mergeability distinct.

## Inspect the candidate

Read project instructions, contributing guidance, recent commit history, changelog policy, PR template, branch/worktree state, remotes, intended base, diff, verification results, and review history. Accept equivalent evidence without requiring any other skill.

Preserve the existing appropriate task branch and unrelated changes. If a task branch is absent, follow the project's naming convention and create one when authorized. Resolve ambiguous remote/base choices through repository context before asking. Do not reset dirty work or assume the default branch is the correct target.

Confirm all agreed acceptance obligations have current evidence and confirmed actionable in-scope defects are resolved. Review the aggregate change, including tests, configuration, migrations, and generated files when relevant. If evidence is stale or a required check is unavailable, repair or disclose the blocker; do not present the PR as technically ready.

Read [publication and CI](references/publication-and-ci.md) for commits, authorization, and remote-state checks. Use the [PR body](templates/pull-request.md), adapting the repository's template and the change's size.

## Prepare coherent history

Follow project commit conventions; use Conventional Commits only when no convention exists. Group changes into coherent, reviewable commits that tell the implementation story. Avoid clerical worklog commits for every event or a history of incidental trial-and-error edits.

Stage only intended owned changes after inspecting them. Preserve unrelated user commits and edits. Do not rewrite existing or published history merely to make it prettier; follow explicit authorization and repository rules for any requested history change.

Include changelog or documentation updates required by the project. Do not invent a version bump or release step. Honor attribution rules; do not add AI/tool attribution unless explicitly requested.

## Publish within established authorization

A skill invocation cannot override repository permissions. Check whether the current request or prior explicit authorization covers commits, branch push, and PR creation. Reuse that authorization; do not ask again merely because a phase changed. If authorization is missing, finish local preparation and show the exact reviewable scope and PR text before requesting it.

Use an available connector or CLI; do not require a particular host or hosting provider. Create a PR against the intended base, or update the existing PR for this branch when appropriate. Avoid duplicates. A full-loop request ending in a PR can authorize publication when project rules permit; a request merely to draft PR text does not.

Use structured text arguments or a body file for multiline descriptions. Describe the concrete problem and resulting behavior, actual validation, material limitations, and reviewer focus. Keep a simple change to a few sentences; use the repository template when required.

## Inspect CI and hand off

Confirm the remote branch and PR head match the intended candidate. Inspect required checks for that head, not an older green run. Investigate failures, repair within scope, update affected evidence, and rerun necessary checks. Preserve failed and flaky outcomes honestly.

Pending, unavailable, cancelled, or failed required checks cannot establish technical readiness. If CI or remote access blocks completion, leave an accurate resumable status. An early draft PR may be useful within authorization, but it remains incomplete until the technical gate passes.

Return the PR link, brief resulting behavior, verification summary, reviewer focus, and any outstanding human approval. Check merge conflicts and branch rules without merging. A protected branch awaiting human review can be technically ready while not yet mergeable.

Do not merge, tag, release, or deploy under this default workflow. Without publication capability, provide prepared commits if authorized, exact PR title/body, and the missing action; never claim an open PR exists when it does not.
