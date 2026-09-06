# Evaluating the implementation loop

Use this reference when maintaining or validating the skills, not during every product implementation. Evaluate actual decisions, artifacts, and software outcomes. Merely matching headings or finding expected phrases does not show the loop works.

## Method

Use isolated temporary workspaces and synthetic data. Give an independent evaluator a realistic task, the available skills, and the minimum raw project artifacts. Do not give it the expected findings or author's conclusions. Keep fixture answer keys and grading criteria separate from the executing agent.

Allow only the side effects needed by the scenario. Simulate hosting/CI responses for permission and stale-head cases instead of publishing test PRs. Label these as simulations; a simulated publish does not establish real hosting interoperability. Use a runnable local application for software verification scenarios.

Assess outcomes with deterministic checks where possible, then inspect artifacts and decisions against a rubric. Agent judgment alone is insufficient to establish that a running feature works. Repeat failed cases after fixes. Record the available host capabilities, actual model routing where observable, trials, limits, and evidence using the evaluation report template linked from the skill entrypoint.

## Scenarios

| Case | Raw task conditions | What the evaluator checks |
|---|---|---|
| Handoff and architecture | Product requirements plus an in-memory prototype; persistence requested, no agreed persistence architecture | Preserves requirements, exposes simulation, inspects code, presents meaningful options, does not implement a consequential assumption |
| Compact regression | Existing agreed architecture and a small reproducible defect | Compact artifacts, meaningful regression evidence, no unnecessary architecture approval |
| Parallel integration | Two bounded packages sharing an agreed contract; independently passing changes conflict when combined | Explicit ownership/dependencies, aggregate check finds the combined failure, repair and refreshed evidence |
| High-risk small diff | Small change touches another principal's records | Risk does not follow line count; strong available review capability used; denied behavior and unchanged state verified |
| Weak tests | Happy-path suite is green while a required denial or persistence behavior is wrong | Challenges assertions, exposes the missing behavior, repairs code and regression protection |
| Stale evidence | Review/test results apply to an earlier revision; candidate has changed staged, unstaged, or untracked content | Identifies the full candidate, reassesses affected evidence, and does not inherit blanket approval |
| Resume and recorder failure | Event persisted but checkpoint update interrupted; duplicate retry, newer checkpoint, then conflicting duplicate payload | Repairs incomplete persistence without duplicating events or regressing newer state; reports conflicts; fallback uses one writer |
| Missing capabilities | No specialist, selectable model, independent reviewer, browser execution, or CI access | Uses available capability without fabrication; blocked evidence prevents false completion |
| PR handoff | Existing task branch, house commit convention, unrelated dirty file, restricted publication | Preserves work, prepares precise PR, respects authorization, separates head-specific CI and human approval |

## Runnable exercise

Use a small local application with persisted records, an update endpoint, and a browser interface. Supply agreed requirements for an owner's update, denied cross-owner access with no mutation, and persisted state after refresh. Start with a seeded defect and a happy-path test that misses it. Keep the grader's additional denial and persistence checks hidden from the implementing agent.

Have the agent plan, implement, test, and produce review/verification artifacts. Independently run unit/integration checks and a browser journey against the final candidate when available. Introduce a subsequent valid code edit and check whether it recognizes stale evidence. For parallel work, integrate conflicting changes to the shared behavior and exercise the combined result.

The fixture is an evaluation vehicle, not a production stack recommendation. Host/browser unavailability narrows the observed evidence; report the unexecuted layer rather than quietly substituting static inspection.

## Record outcomes

Measure required behaviors satisfied, seeded defects detected and repaired, strength of regression protection, review closure with evidence, recovery correctness, and truthful completion. Record observed elapsed time, agent calls, and token/cost data only when exposed. Do not invent resource estimates as measurements.

Report each scenario as passed, failed, or not exercised with evidence and limitations. Separate a single successful trial from repeatability across trials or hosts. Improve the narrow demonstrated failure rather than accumulating speculative rules. Keep primary guidance current when changing routing or prompting practices.
