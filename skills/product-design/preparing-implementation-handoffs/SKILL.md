---
name: preparing-implementation-handoffs
description: "Consolidate requirements, UX flows, selected visual decisions, HTML prototypes, acceptance criteria, and suggested delivery slices into a product/design handoff. Use when discovery artifacts need to become a coherent brief for engineering planning, without inventing architecture or API contracts."
license: MIT
---

# Preparing implementation handoffs

Give the next engineer or agent enough agreed product behavior and visual intent to begin engineering planning. Readiness here is product/design readiness, not a claim that architecture, production code, or deployment is complete.

## Inspect and reconcile

Read applicable project instructions, including `AGENTS.md` or `CLAUDE.md` when present, current requirements, flows, selected directions, prototypes, feedback, and existing decisions. Adopt the project's artifact conventions. This skill accepts equivalent source material and works without the coordinator or other specialists.

Identify the current intended artifacts and compare their contents. Do not assume the newest file is approved or that a polished prototype is authoritative about behavior. Read [readiness and traceability](references/readiness-and-traceability.md) before resolving inconsistencies.

Preserve established stack, tokens, component conventions, and visual continuity decisions as constraints. When technology is missing, identify the engineering decision and its implications; do not silently select a stack or invent data/API contracts to make the handoff look complete.

## Prepare the handoff

Use the [handoff template](templates/implementation-handoff.md), adapting it to existing documents. Keep one authoritative requirement statement and reference it from flows, prototype screens/states, and acceptance criteria. Small tasks may use sections in a single document.

Include the agreed outcome and exclusions, behavior, content and state requirements, selected composition, typography and spacing tokens, actual font/fallback limitations, responsive rules, and accessibility expectations. Distinguish observed prototype behavior from intended production behavior, and identify simulations and omissions.

Suggest delivery slices that each produce a useful user outcome and include relevant acceptance checks. Sequence by dependencies and learning value without inventing file-level implementation tasks or architectural decisions. Read the [annotated handoff](references/annotated-handoff.md) for an example.

## Review readiness

Flag contradictions, unapproved consequential choices, missing acceptance criteria, broken artifact references, and unresolved behavior that blocks the next step. Resolve editorial inconsistencies within agreed intent. For substantive conflicts, present concrete options and their impact; do not silently pick a convenient source.

State what was inspected or tested, what failed, and what was not verified. A prototype checklist is not a production accessibility audit or user study. For a proof of concept, distinguish readiness to evaluate the hypothesis from evidence that the hypothesis is supported.

Present a readiness judgment: ready for engineering planning, ready only for prototype evaluation, or needs named product/design decisions. Reuse prior approvals or explicit delegation. If final product/design acceptance remains pending, say so; do not introduce a new approval when it is already established.

Return artifact links, material limitations, and the next engineering questions. This skill does not authorize implementation or release. Without filesystem access, provide complete copyable Markdown and state that no file was created.
