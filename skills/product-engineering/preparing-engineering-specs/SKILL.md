---
name: preparing-engineering-specs
description: "Prepare spec.md and technical context from product requirements, design handoffs, and existing code, including architecture options and agreement on consequential decisions. Use before implementation planning when behavior, feasibility, or technical direction needs grounding."
license: MIT
---

# Preparing engineering specs

Produce a technical baseline the user and implementation agents can rely on. Accept equivalent requirements without any other skill installed. An agreed product handoff is an input to architecture discussion, not proof architectural decisions are settled.

## Ground the problem

Read project instructions, supplied requirements and decisions, relevant source, tests, configuration, dependency manifests, and CI. Adopt existing artifact conventions; otherwise write `spec.md` and `context.md` under `docs/product-engineering/<initiative>/`. Reuse an existing `research.md` rather than duplicate it. Small changes can combine sections.

Preserve upstream requirement IDs, accepted behavior, design tokens, and visual continuity choices. Separate production expectations from prototype simulations, omissions, and observations. For non-UI work, accept the problem statement and existing contracts directly; do not manufacture design artifacts.

Inspect the actual code path and relevant dependencies. Record what currently works, what fails, and which baseline checks were actually run. Report inability to inspect or execute accurately. Avoid asking the user for facts available in the repository.

Read [research and architecture agreement](references/research-and-agreement.md) when gathering external evidence or proposing consequential changes. Use primary sources for uncertain or evolving technical claims. Separate observations, assumptions, recommendations, and approved decisions.

## Prepare the proposition

Use the [spec template](templates/spec.md) and [context template](templates/context.md). Define the problem, intended outcome, boundaries, acceptance criteria, inherited constraints, and relevant nonfunctional requirements. Reference an authoritative requirement instead of rewriting it throughout the documents.

Describe the technical approach at the depth needed to settle consequential choices: component responsibilities, data flow, interfaces, persistence, trust boundaries, deployment constraints, and failure/recovery behavior where relevant. Define contracts that upcoming work depends on; do not invent an exhaustive schema before there is a concrete need.

Present serious architecture alternatives with implications for future evolution, operations, migration, cost, and complexity where they matter. Recommend an option from evidence. Preserve established stack and conventions unless the problem justifies a change.

Consequential choices need user agreement before autonomous implementation. Reuse explicit agreement or delegation already present; a routine change within the existing agreed architecture needs no fresh ceremony. Do not record silence, a recommendation, or a polished document as approval. Investigate independent questions while a decision is pending.

## Hand to planning

State whether the baseline is ready for implementation planning, needs a named decision, or needs a bounded feasibility experiment. Capture experiment questions and exit criteria; observations must follow execution, not be invented in the proposal.

Record accepted decisions using the project's established decision log where appropriate. If `decision-records` is available, it can maintain that log; this skill must still supply the decision and rationale without it.

Return artifact paths, agreed direction, remaining uncertainty, and constraints for planning. If architecture changes later, identify affected requirements, contracts, plans, and approvals before resuming dependent work. No production implementation is authorized by a request for specifications alone. Without file access, return copyable Markdown and say nothing was written.
