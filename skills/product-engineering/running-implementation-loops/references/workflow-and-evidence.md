# Workflow and evidence

## Artifacts and authority

Adopt existing artifacts in place. The default root is `docs/product-engineering/<initiative>/` in the target project. Do not create competing sources of truth just to obtain these filenames.

| Artifact | Owns |
|---|---|
| `spec.md` | Problem, scope, requirement references, acceptance, constraints, agreed technical direction |
| `context.md` or existing `research.md` | Inspected code and tests, observed baseline, sources, options, uncertainties |
| `implementation-roadmap.md` | Packages, dependencies, integration order, status, next action |
| `work-packages/<id>/plan.md` | Bounded outcome, contracts, approach, ownership, tests, completion criteria |
| `work-packages/<id>/review.md` | Review rounds, revisions, findings, dispositions, verification of fixes |
| `work-packages/<id>/verification.md` | Requirement-to-check mapping, execution results, environment, evidence gaps |
| `worklog.md` | Current session checkpoint and chronological factual events |

Store aggregate review and verification in clearly labeled initiative-level sections or `review.md` and `verification.md` for larger work. Reference package records; inspect cross-package behavior rather than copying their success claims.

For one small change, sections in one document carry this contract. For multiple packages, separate plans and histories prevent ambiguous ownership. Keep requirement text authoritative in one place; assign local IDs to new requirements when needed. Worklogs reference decisions and evidence, and cannot approve requirements or replace verification records.

Track concise durable Markdown unless project policy says otherwise. Keep bulky logs, traces, screenshots, and generated data in the project's evidence store or CI artifacts. Record their locations and retention limitations; never commit secrets. Broken or expired evidence references must be repaired or treated as unavailable.

## Entry and phase gates

| Phase | Evidence required to advance |
|---|---|
| Intake | Coherent intended behavior, constraints, known upstream gaps, relevant branch/worktree state |
| Technical baseline | Inspected code and tests; consequential options resolved with the user; acceptance criteria usable |
| Package readiness | Bounded outcome, settled required interfaces, available dependencies, ownership, verification obligations |
| Package verification | Planned behavior and regression checks executed or explicitly blocked; results tied to candidate revision |
| Package review | Triage plus substantive review of code and tests; confirmed actionable defects repaired and verified |
| Integration | Combined diff examined and combined behavior checked; affected stale evidence refreshed |
| PR delivery | Authorized coherent commits and PR; required CI evaluated for the current head; truthful remaining human-review status |

Record statuses such as proposed, ready, active, blocked, verified, and reviewed as useful to the project. Name the evidence for a transition; a status checkbox cannot establish it. A package may be blocked while an independent package continues. Neither unavailable tools nor an agent's confidence waive a gate.

## Essential specialist outcomes when operating alone

**Technical preparation:** distinguish intended behavior from prototype simulations. Inspect architecture and baseline checks before proposing changes. Research uncertain or evolving technical claims from primary sources. Present consequential options with recommendation and tradeoffs; preserve the resulting user agreement. Resolve routine engineering details autonomously within that agreement.

**Planning:** sequence useful increments and explicit prerequisites. Set ownership and integration points. For each required outcome, specify its observable acceptance check and the lowest suitable test layer. Include real boundary integration checks and critical E2E journeys when relevant. Existing tests and tools constrain the plan; absent environments become explicit prerequisites.

**Implementation:** inspect the bounded plan and affected dependencies, reproduce the baseline where feasible, implement and test, then return changed artifacts, actual check results, and gaps. Coordinate shared files and do not erase other work. Do not edit acceptance criteria to match an accidental implementation.

**Verification:** inspect assertion quality, isolation, representative inputs, and mock boundaries. Unit tests cover logic; integration tests exercise meaningful boundaries; browser E2E exercises the actual application for critical journeys. Preserve suitable existing frameworks. Prefer Playwright when adding browser E2E. For regressions, seek a demonstrated failing case before the fix. Never count a mocked component check as a real integration result or rerun away a flake.

**Review:** first triage consequence, uncertainty, complexity, and affected boundaries. Then review the actual diff and surrounding code, tests, acceptance coverage, and relevant operational concerns. Follow project priorities, otherwise P0 critical, P1 high, P2 medium, P3 low; enhancements are separate. Findings include trigger, impact, location, evidence, revision, status, and fix verification. Fix all confirmed actionable in-scope defects. Reconcile disagreements using evidence, escalating uncertainty instead of majority voting. Review the combined change after integration.

**Logging:** supply uniquely identified facts and checkpoint changes with an expected predecessor to a single writer. Append history, update a short checkpoint, and verify both. Duplicate retries must not duplicate entries; repair an interrupted checkpoint only from its expected prior state, preserving later checkpoints. Record claimed results as claims until evidence is inspected. Preserve authorization and pending decisions across sessions.

**PR preparation:** inspect recent history and instructions for commit conventions; use Conventional Commits only when absent. Group coherent changes and stage only owned content. Respect authorization for commits, push, and PR creation. Prepare a concise problem/result description, validation and reviewer focus. Verify the remote target and head, CI results and required approvals separately. Do not merge or publish a release under an implementation request.

## Evidence freshness and recovery

Each check or review records the relevant commit or worktree snapshot, execution time, command or method, environment, outcome, and evidence location. A commit identifier alone is insufficient if uncommitted changes were tested. Identify all relevant candidate content: tracked modifications whether staged or unstaged, new untracked implementation/tests, and deletions. Use a content manifest with hashes or a complete snapshot; an ordinary unstaged diff omits staged and untracked content. Record index/worktree divergence so a later commit cannot silently substitute different bytes for the tested candidate. State what a check proves and what its mocks exclude.

An edit invalidates evidence for the affected behavior and dependencies. Review fixes, rerun impacted checks, and run the project's required final checks against the integrated candidate. Final CI must match the current PR head. Editorial changes to logs need not force a browser rerun, but do not use this exception for code, configuration, dependencies, or test edits.

On resume, inspect branch, head, dirty files, active assignments, latest checkpoint, open findings, and changed contracts. Reconcile differences before dispatch. Revalidate affected evidence and avoid rerunning completed unrelated research. If interruption left a write uncertain, inspect the destination before retrying.

For a blocked repair, record the failure, attempted approaches, new evidence, and exact next need. Two equivalent unsuccessful attempts without learning trigger stronger diagnosis or replanning. A budget limit narrows work or produces a checkpoint; it never changes failing work to complete.
