# 0006: Package product discovery as independent skills with an optional coordinator

- Status: accepted
- Date: 2026-09-05

## Context

The repository needs reusable guidance for a solo builder working with agents on rough ideas, features, applications, and proofs of concept. Product scope and design direction should remain user decisions while agents prepare concrete alternatives. The first set ends at a product/design handoff and must work across project stacks and agent hosts.

## Options

1. **One comprehensive skill.** Simple discovery, but individual artifact requests load a broad workflow and make phase boundaries harder to maintain.
2. **Five independent specialists with a documented sequence.** Focused invocation and individual installation, but no dedicated capability for resuming and coordinating an initiative.
3. **Five independent specialists plus an optional coordinator.** Focused capabilities with a separate discovery entry point; requires clear routing and specialist responsibilities.

## Decision

Option 3, installed together as the `product-design` category. Specialists shape product briefs, design UX flows, explore visual directions, build offline HTML prototypes, and prepare implementation handoffs. The coordinator manages context, progress, and milestones without requiring subagents or a specific host.

Skills are stack-neutral and inspect project instructions and existing assets. Product scope, direction selection after normally three contrasting sketches, and product/design readiness are default milestones; existing approval and explicit delegation carry forward. Existing visual language may be preserved, evolved, or replaced according to the user's choice.

Each prototype is independently usable as one offline HTML file with embedded CSS, necessary JavaScript, and required assets. Implementation, architecture planning, and deployment are outside this first set. Each skill is self-contained and accepts equivalent artifacts without another skill installed.

## Consequences

- Users can install one category or invoke one specialist for bounded work.
- Discovery scales to uncertainty and resumes from current artifacts instead of repeating completed phases.
- Font and asset availability can limit offline fidelity; prototypes must disclose fallbacks.
- The coordinator must handle unavailable specialists explicitly; examples must not become universal product or stack requirements.
- Future engineering-delivery skills can consume the handoff without expanding these skills' scope.
