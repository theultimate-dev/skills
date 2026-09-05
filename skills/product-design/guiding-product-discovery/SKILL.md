---
name: guiding-product-discovery
description: "Guide a rough product, application, feature, or proof-of-concept idea through requirements, UX flows, visual directions, offline HTML prototypes, and a product/design handoff. Use to coordinate discovery across phases or resume unfinished design work; individual artifact requests belong to the relevant specialist."
license: MIT
---

# Guiding product discovery

Help the user make consequential product and design choices while agents develop concrete proposals between decisions. Finish with a product/design handoff, not production implementation or a silently selected architecture.

## Start from the project

Read applicable project instructions, including `AGENTS.md` or `CLAUDE.md` when present, and inspect existing briefs, source, design assets, tokens, and decisions. In a chat without repository access, use supplied materials and identify what could not be inspected. Do not ask the user to repeat discoverable information.

Capture the intended audience, problem, desired outcome, boundaries, and unresolved questions. An established stack constrains feasibility; a missing stack does not block discovery. Raise a stack decision only when it changes a proposal's feasibility or the handoff. Never replace project technology by preference.

For an existing product, establish whether this initiative preserves, evolves, or replaces its visual language. Infer this from explicit instructions already given; otherwise ask with concrete implications. Carry the choice forward, including any approved exceptions.

Read [workflow and milestones](references/workflow.md) to choose the next useful phase. Adopt existing artifact locations. Otherwise use `docs/product-design/<initiative>/` in the target project and the [discovery index](templates/discovery-index.md). The path is an output convention, not an installation requirement.

## Coordinate by outcome

| Needed outcome | Specialist, when available | Required input |
|---|---|---|
| Agreed problem, scope, requirements | `shaping-product-briefs` | Idea, known audience, constraints, evidence |
| Journeys, information hierarchy, screen behavior | `designing-ux-flows` | Brief or equivalent requirements |
| Three comparable visual direction briefs | `exploring-visual-directions` | Audience, content, flows, visual continuity choice |
| Three offline sketches, then a refined selected prototype | `building-html-prototypes` | Direction briefs or selected direction and flows |
| Product/design handoff and suggested slices | `preparing-implementation-handoffs` | Current requirements, flows, chosen design, prototype and review findings |

Use the host's supported skill invocation mechanism, or read an available skill and carry out its instructions. This workflow does not require subagents, concurrent execution, or a particular tool. Do not invent skill paths or assume that installing this skill installed the specialists.

If a specialist is unavailable, name the missing capability and provide the [portable task brief](templates/task-brief.md), including enough context to continue elsewhere. Continue independent discovery work; do not label an unperformed specialist step complete.

## Keep the user in the decisions

Default to three milestones: agree product scope; select or combine a direction after reviewing three HTML sketches; review the refined prototype and readiness for handoff. Prepare a recommendation and concrete alternatives before asking. Existing approval counts: do not ask again unless new information materially changes the choice. A request for only one artifact does not authorize the whole workflow.

Between milestones, resolve routine details autonomously within the agreed scope. Ask when an unresolved choice materially changes outcomes, effort, or the experience. Record which decisions are the user's, which are provisional recommendations, and what remains unknown. Never treat silence or a finished-looking prototype as approval.

Three sketches are the default for unresolved visual direction, not a ritual for every change. Skip exploration already settled by the user. Merge documents for small work and omit irrelevant states or diagrams. Read the [worked examples](references/worked-examples.md) when calibrating effort for a new application, small feature, or proof of concept.

## Resume and revise

Keep the index small: current artifacts, approved choices, assumptions, unresolved questions, and next action. Give each requirement a stable local identifier when needed for traceability. Other artifacts reference the requirement instead of copying its text everywhere.

When a prototype reveals a problem, revise affected requirements or flows first, then update the direction, prototype, and handoff as needed. Mark a prior approval as needing review only where the change invalidates it. Retain rejected directions and the reasons they were rejected when useful for future decisions.

## Finish

Return links to current artifacts, the key decisions, any remaining blockers, and the next engineering questions. Product/design readiness means sufficient agreed behavior and visual intent to begin engineering planning; it does not assert architectural readiness, production accessibility conformance, or research validation.

Without file-writing capability, provide complete copyable artifacts and filenames and state that no files were written. Never claim visual or interaction verification unless it was performed.
