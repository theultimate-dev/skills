---
name: planning-implementation
description: "Turn an agreed technical baseline into implementation-roadmap.md and bounded plan.md work packages with interfaces, dependencies, ownership, test obligations, and integration gates. Use before dispatching implementation or when new evidence requires replanning."
license: MIT
---

# Planning implementation

Create executable work packages whose outcomes and verification are clear to another engineer or agent. Accept an agreed specification or equivalent requirements and technical decisions; no coordinator is required.

## Inspect readiness

Read applicable instructions, the technical baseline and its agreement status, relevant code and tests, current branch/worktree, and available execution environments. Reuse established artifact locations. Otherwise use `docs/product-engineering/<initiative>/implementation-roadmap.md` and `work-packages/<id>/plan.md` beneath the initiative root.

Do not fill a consequential architecture gap with an unapproved planning assumption. Identify the decision and prepare a concrete recommendation. Existing explicit agreement counts. Continue planning independent work where useful.

## Define executable packages

Read [decomposition and integration](references/decomposition-and-integration.md). Use the [roadmap](templates/implementation-roadmap.md) and [package plan](templates/plan.md) templates. A single small task can use sections in one document.

Each package identifies its useful outcome, requirement references, implementation approach, required interface changes, affected code, ownership, prerequisites, test cases, execution environment, and completion evidence. Resolve choices required for safe dispatch. Leave routine private implementation details to the implementer rather than specifying every helper.

Prefer increments that produce useful behavior. Infrastructure or migration prerequisites can be separate packages when they unblock that behavior; state why and how their contract is checked. Split work where ownership, dependencies, or useful validation boundaries differ, not to manufacture parallelism.

## Plan verification before coding

For every acceptance criterion, name the observable check and appropriate layer. Unit tests cover logic and invariants; integration tests cover meaningful boundaries and persistence; critical user journeys get E2E checks where applicable. Prefer Playwright when adding browser E2E, while preserving suitable existing tooling. Do not impose a numerical pyramid or new test framework on unrelated work.

State representative success, boundary, failure, and recovery cases that matter to the requirement. Identify actual versus mocked dependencies, fixtures, required services, commands, and how the test would detect the defect. Relevant visual, accessibility, security, performance, migration, and AI evaluation needs belong here, not as surprises at final review.

When available, `verifying-implementation` can develop or challenge this strategy before implementation and execute it afterward. Otherwise include the obligations directly. Make test quality review explicit: behavior assertions, deterministic isolation, realistic boundaries, and resilience to internal refactoring.

## Schedule and hand off

Declare dependency order, which work may run concurrently, shared-file coordination, and an integration owner. Supported isolated workspaces can help; without them, use disjoint ownership or sequence changes. Never assume separate workspaces eliminate interface conflicts.

Dispatch only ready packages. Provide their objective, relevant spec/context and code references, baseline revision, available capabilities, ownership, expected evidence and output path, and escalation conditions. Match an available agent by capability; use a general agent or sequential execution if specialists are absent. Tell workers to preserve others' changes.

Require package review and a combined review/verification after integration. Later edits invalidate affected evidence. New learning updates affected plans and roadmap status; architecture or scope changes return for the affected user decision.

Return plan paths, immediately runnable work, parallelization boundaries, and blockers. A planning request does not authorize implementation or repository publication. Without file access, provide complete copyable artifacts and accurately state the limitation.
