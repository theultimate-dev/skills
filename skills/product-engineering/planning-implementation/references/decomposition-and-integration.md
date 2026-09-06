# Decomposition and integration

## Bound work by a checkable outcome

A package should fit a coherent implementation and review context. A vague “build the backend” package hides contracts; a separate package for every function creates coordination overhead. Use the smallest useful outcome with an explicit evidence boundary.

An existing save API, for example, may allow persistence repair and keyboard-feedback work to proceed independently once response/error semantics are settled. If both packages change the same response shape, agree that contract first and assign one owner. Declare producer/consumer dependencies; do not let agents discover conflicting assumptions at integration time.

## What must be settled before dispatch

- Required behavior, exclusions, and acceptance examples.
- Applicable agreed architecture and relevant public/interface changes.
- Starting code and tests, permitted ownership, dependencies, integration owner.
- Verification method, important cases, real/mocked boundaries, environment prerequisites.
- Expected evidence and artifact paths; conditions for escalating uncertainty.

The first package can be ready while later packages remain provisional. A roadmap is not permission to dispatch every row. Mark each prerequisite explicitly and inspect its actual completion evidence.

## Tests are designed with the package

Map each relevant requirement to a check. Avoid writing one test at every layer for the same trivial assertion. Use fast tests for exhaustive logic cases and integration/E2E for the boundary confidence those tests cannot supply.

Regression plans should name the failing behavior and seek a failing check before the fix. Acceptance plans should ask what plausible wrong implementation might pass the proposed tests. If ownership isolation matters, a happy-path save test is inadequate; include a second principal and a denied operation.

When tests and implementation are delegated separately, agree the observable contract and fixture boundaries first. Test authors use requirements and public behavior, then inspect implementation to assess coverage and feasibility. Do not require agents to guess an unfinished interface or make tests mirror implementation internals.

## Integrate deliberately

Keep shared schemas, dependency files, migrations, generated artifacts, and common fixtures under coordinated ownership. Workspaces may be isolated, but package outputs must target compatible baselines. Preserve unrelated work and inspect conflicts semantically instead of accepting whichever version merges cleanly.

At integration, check combined user journeys, changed interfaces, migration ordering, configuration, and shared state where relevant. Run affected regression checks and the required project-wide checks. The aggregate review evaluates omissions and interactions across packages, not only their individual findings.

Replan if new evidence changes a contract, reveals hidden coupling, or invalidates a dependency. Record why, update affected packages, and revisit only user agreements actually changed. Do not broaden scope to clean up unrelated code discovered during planning.
