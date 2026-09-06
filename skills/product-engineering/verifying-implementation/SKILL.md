---
name: verifying-implementation
description: "Design and execute requirement-based unit, integration, E2E, and relevant nonfunctional checks, assess test quality, and record revision-specific verification evidence. Use during technical planning, after implementation, or when repairs and integration invalidate earlier results."
license: MIT
---

# Verifying implementation

Establish what the software actually does and whether the evidence covers the agreed outcome. Test count, coverage percentage, agent confidence, and a green badge cannot substitute for meaningful assertions.

## Establish the verification task

Read applicable instructions, requirements and acceptance criteria, agreed architecture, plan, relevant source/tests, CI configuration, and current revision. Accept equivalent artifacts without other skills installed. Identify whether this task is designing checks before coding, implementing tests, evaluating existing tests, or executing checks on a candidate.

Adopt the project's tooling and evidence conventions. Otherwise write `verification.md` beside the package plan, or a verification section for small work. Aggregate verification belongs at initiative level and references package evidence.

Read [test design and evidence](references/test-design-and-evidence.md) before designing or evaluating tests. Use the [verification template](templates/verification.md). Keep the test design distinct from actual execution results.

## Design from behavior and risk

Map acceptance criteria and important failure modes to observable checks. Use unit tests for meaningful logic and invariants, integration tests for real component boundaries, and a small set of E2E journeys for critical application outcomes. Do not require every layer for every change or invent fixed ratios and coverage thresholds.

Preserve suitable existing frameworks. Prefer Playwright when introducing browser E2E. Test the running application's behavior rather than an offline prototype or static markup when claiming production implementation evidence. State real versus mocked dependencies and what each check cannot prove.

Include relevant boundary, denial, failure, recovery, concurrency, and compatibility cases. For user-facing work, verify agreed visual intent, responsive behavior, keyboard/focus behavior, and accessibility expectations where applicable. For migrations, performance, security, operations, or AI features, choose checks that correspond to the actual risk rather than adding a generic checklist.

Prepare fixtures, services, data isolation, commands, and pass criteria before dispatching test work. If a required interface or environment is missing, identify the prerequisite. Do not invent numerical targets or replace a required real service with an undisclosed mock.

## Challenge the tests

Ask what plausible wrong implementation would still pass. Inspect assertion strength, coverage of the relevant contract, fixture realism, isolation, determinism, and resilience to internal refactoring. A test can be technically correct yet irrelevant to the requirement.

For regressions, demonstrate the check fails for the original defect where feasible. Targeted mutation or fault injection is useful for consequential behavior; execute it in an isolated copy and restore the candidate before final checks. Do not equate compilation failure from an invalid mutant with detecting the intended defect.

Never approve mechanical snapshot updates or weaker expectations solely because the candidate changed. A retry-success outcome still exposes flakiness; investigate it and preserve the original failure.

## Execute and interpret

Run the planned checks and appropriate project-required checks. Record candidate revision or worktree snapshot, environment, exact command/method, actual result, and evidence location. A snapshot covers relevant staged/unstaged modifications, untracked code/tests, and deletions; identify index/worktree divergence. An ordinary unstaged diff is insufficient. Inspect exit status and assertion outcomes. Separate passed, failed, not run, blocked, and flaky results.

Review failures with the implementer, verify repairs, and rerun affected checks. After integration, exercise combined behavior and relevant regression boundaries. Reuse fresh evidence where valid; do not rerun every expensive suite after a purely editorial update. Code, test, dependency, or configuration changes require impact assessment and refresh of affected evidence.

When delegating, provide requirements, risks, settled interfaces, baseline, relevant code/test pointers, real/mock boundaries, ownership, expected result path, and escalation conditions. Match available capabilities; use mid-tier moderate effort for bounded tests and strong models for high-risk or difficult analysis. Record unavailable controls. Self-execution remains possible, with independence limitations disclosed.

## Report the judgment

Return artifact paths, requirement coverage, observed failures, missing evidence, and the next corrective action. A mandatory check that cannot run prevents a verified-complete claim. An optional enhancement is different from a missing acceptance obligation.

State the limits of the method: browser automation is not a user study, an accessibility scanner is not complete conformance evidence, and deterministic API tests do not prove an AI feature's probabilistic quality. Do not claim execution without tools; return a verification design labeled unexecuted when needed.
