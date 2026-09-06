---
name: implementing-work-packages
description: "Implement a bounded engineering plan with owned code and test changes, targeted verification, repair cycles, and an evidence-based handback. Use when an implementation package is ready or confirmed review findings need fixes within an agreed technical baseline."
license: MIT
---

# Implementing work packages

Deliver the behavior and evidence in a ready plan. Accept an equivalent bounded task without requiring another skill or a specific custom agent.

## Check the assignment

Read project instructions, the plan, relevant requirements and architecture decisions, current code and tests, and branch/worktree state. Confirm ownership, dependencies, acceptance cases, environment, and output locations. Inspect surrounding code needed to understand the affected boundary.

Raise unresolved consequential contract or scope choices before implementing dependent work. Resolve routine details within the agreed baseline. Preserve unrelated edits. Never reset, replace, or stage another worker's changes to make the task easier.

Use the assigned branch/workspace. Coordinate shared files with the integration owner; isolated workspaces do not authorize conflicting contracts. Record the baseline actually used, including relevant uncommitted changes.

## Implement and test

Reproduce a reported defect before changing it where feasible. Inspect baseline failures so new regressions remain distinguishable. Write meaningful tests from the agreed behavior and failure modes, then implement the smallest coherent change. TDD is useful when a failing test can establish the requirement; do not manufacture an artificial red step for a documentation-only or already-covered change.

Run targeted checks and inspect their actual results. Use unit tests for relevant logic, integration tests for real boundaries, and critical E2E journeys for application behavior as specified in the plan. Preserve suitable project tools; use Playwright when browser E2E is needed and no suitable tool exists. Do not replace a planned real integration check with a mock without exposing the evidence gap.

Read [repair and handback](references/repair-and-handback.md) for failed checks, review fixes, and integration. Treat tests as part of the product change: do not weaken assertions, delete meaningful cases, or change accepted behavior to match an accidental result.

## Use capabilities deliberately

When delegation is available and authorized, select relevant engineering or testing capabilities from the advertised agents. Supply a bounded outcome, requirement/plan references, source starting points, owned files, settled contracts, baseline, expected checks, result path, and escalation conditions. Tell workers they are not alone and must preserve others' edits.

Start routine bounded implementation at a capable mid tier and moderate effort. High-risk repairs need a high/top tier; difficult reasoning or uncertain evidence can also justify escalation irrespective of priority. Use only supported runtime controls and record unavailable settings honestly. Without delegation, carry out the assignment sequentially.

Parallel code and test authors need a settled observable contract and disjoint ownership. The implementer may write tests, but an independent review should challenge both code and tests where supported. Implementation self-checks are not independent approval.

## Return evidence

Use the [implementation result](templates/implementation-result.md), normally as a plan section or handback artifact. Return a short status, paths, changed behavior, actual commands/results, candidate revision, and blockers. Link review fixes to finding IDs and request their verification rather than declaring them closed yourself.

Update the plan's factual progress and send events to the designated worklog writer. Do not create competing writers for shared history. The integration owner checks the combined result before acceptance.

Stop only when the package obligations are met or a named blocker prevents further justified work. After two equivalent failed repair attempts without learning, escalate diagnosis or replan. Preserve the work and a concrete next need. A missing environment is unverified work, not a pass.

Committing and publication depend on the user's authorization and repository rules; implementing a package does not imply permission to merge or release. Without execution access, return a proposed patch or instructions accurately labeled unexecuted.
