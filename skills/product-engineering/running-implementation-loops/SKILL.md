---
name: running-implementation-loops
description: "Coordinate agreed requirements through technical research, architecture agreement, implementation plans, test and review repair loops, and an open pull request. Use to start or resume a complete engineering initiative; individual specifications, reviews, tests, or PR requests belong to their focused capability."
license: MIT
---

# Running implementation loops

Own delivery from a coherent problem to a technically ready pull request awaiting human review. Completion requires observed acceptance evidence, resolved actionable defects, and required checks on the current revision. A convincing summary or successful agent response is not that evidence.

## Establish the baseline

Read applicable project instructions and inspect the task branch, worktree, existing decisions, source, tests, CI, and supplied requirements. Preserve unrelated changes. Adopt an existing task branch; create an appropriate one when necessary and authorized. Never infer the target branch solely from a conventional name.

Accept a product/design handoff or equivalent requirements. Preserve requirement IDs, selected visual intent, approvals, and known prototype simulations. Product-design readiness permits engineering planning; it does not settle architecture or authorize production behavior inferred from a mockup.

Inspect available tools, skills, agent capabilities, models, reasoning controls, and authorization. Read [routing and delegation](references/routing-and-delegation.md) before choosing execution roles. Discover capabilities from what the host actually exposes; never invent custom agent names or claim a model selection that was not applied.

Use the project's artifact locations. Otherwise use `docs/product-engineering/<initiative>/`. Read [workflow and evidence](references/workflow-and-evidence.md) for artifact responsibilities, phase gates, and resumption. For small work, use the [compact initiative template](templates/compact-initiative.md). Artifact paths describe target-project outputs, not skill installation paths.

## Choose the next outcome

| Needed outcome | Specialist, when available | Required input |
|---|---|---|
| Technical context and agreed architecture | `preparing-engineering-specs` | Requirements or handoff, repository, existing decisions |
| Executable packages and dependencies | `planning-implementation` | Technical baseline, acceptance criteria, context |
| Tests and verification obligations, then evidence | `verifying-implementation` | Requirements, risks, interfaces; later, running implementation |
| Bounded code and test changes | `implementing-work-packages` | Ready plan, relevant context, ownership, verification obligations |
| Independent review and fix verification | `reviewing-code-changes` | Scope, baseline and candidate revisions, requirements, tests |
| Durable factual progress | `recording-worklogs` | Supplied events, identifiers, evidence paths, checkpoint |
| Coherent commits and open PR | `preparing-pull-requests` | Verified aggregate change, review records, repository conventions |

Invoke an available specialist through the supported mechanism or read its instructions. Installing this skill alone does not imply other skills are present. If one is missing, say so and perform its essential outcome using [workflow and evidence](references/workflow-and-evidence.md), or hand over the [task packet](templates/task-packet.md) when the capability itself is unavailable. Never mark work complete merely because it was delegated.

## Agree, then execute

Before implementation, prepare a technical proposition covering consequential architecture choices, alternatives, tradeoffs, and relevant uncertainty. Obtain user agreement on these choices; reuse explicit agreement already present. A routine change within an agreed architecture can reference that baseline without another approval ceremony.

Plan tests with the implementation, before coding. Specify meaningful behavior and failure cases, test layers, real versus simulated boundaries, and exact evidence obligations. Readiness requires executable plans for the work being dispatched; later dependent packages may remain provisional.

Execute autonomously within the agreed baseline and authorization. Ask only about unresolved consequential choices, scope changes, or actions that require permission. Investigate discoverable facts first. Explicit authorization carries forward; a skill does not grant new permissions or override repository rules.

Use subagents when available and authorized, matching demonstrated capabilities to bounded work. Each call gets the [task packet](templates/task-packet.md), adapted to the task. Choose tier and effort separately. Parallel work needs settled contracts and disjoint ownership or supported isolation; the orchestrator owns integration and shared-artifact coordination.

## Close the feedback loop

For each package: implement and run targeted checks; review code and tests independently where possible; reproduce or substantiate findings; repair confirmed defects; verify repairs; rerun affected checks. Triage begins every review but never replaces substantive review. Route high-risk work to a strong available model even when the diff is small.

Fix confirmed, actionable in-scope defects at every severity. Optional enhancements are not defects. An unresolvable finding needs a named blocker or explicit scope decision, not silent deferral or relabeling. A user-approved scope change updates the baseline and affected plans before execution continues.

After integration, examine the combined diff and rerun the relevant acceptance and regression checks. Individually passing packages do not establish that their combined behavior works. Record evidence against the revision and environment actually examined; later edits invalidate affected conclusions.

Treat unavailable checks as missing evidence, flaky results as unresolved reliability concerns, and unsupported claims as unverified. Do not weaken a test or redefine acceptance to make the loop terminate.

## Persist and recover

Maintain one worklog writer, normally a lowest-capable-tier subagent. Supply factual events after decisions, completed tasks, checks, findings, fixes, integration, and blockers. The recorder must not infer decisions or completion. Verify both events and checkpoint persistence; a `Done` response alone is insufficient. Recover an interrupted checkpoint without overwriting newer state. If delegation fails, establish sole writer ownership and complete the facts directly.

Flush events before session handoff and major phase transitions. Keep a short checkpoint with current revision, artifacts, active work, unresolved findings, authorization already given, and next action. Retain chronology instead of replacing it with a summary. Resume by reconciling that checkpoint against the actual worktree and evidence.

Change the approach when a repair fails. After two unsuccessful attempts at the same underlying failure without new evidence, escalate diagnosis or revise the plan instead of dispatching another equivalent retry. Respect explicit budgets. If no justified next approach remains, preserve a resumable blocker and continue independent useful work; do not claim completion.

## Deliver

Verify the aggregate result, coherent commit history, PR target, and required CI on the latest PR revision. Present a concise title and description explaining behavior, validation, material limitations, and where the user should focus review. Commit, push, and open the PR only within established authorization; prepare everything reviewable before asking for any missing permission.

The endpoint excludes merge, release, and deployment unless separately requested. Distinguish technically ready for human review from repository mergeability: required human approvals may still be pending. Without execution or hosting access, return the concrete artifacts and remaining action, accurately labeled incomplete.

When evaluating or modifying this workflow, read [evaluation scenarios](references/evaluation-scenarios.md) and record trials with the [evaluation report](templates/evaluation-report.md). Maintained external guidance and its limits are in [sources](references/sources.md); neither models nor provider-specific effort names are embedded in the workflow.
