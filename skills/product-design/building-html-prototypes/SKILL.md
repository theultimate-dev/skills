---
name: building-html-prototypes
description: "Build responsive UI sketches and interactive prototypes as independent offline HTML files with embedded CSS, assets, and minimal JavaScript. Use to compare design directions or refine an agreed application or feature experience before production implementation."
license: MIT
---

# Building HTML prototypes

Produce artifacts that the user can open directly, compare, and pass to another person without an application runtime. The prototype demonstrates design intent and selected behavior; it is not production implementation.

## Establish the task

Read applicable project instructions, including `AGENTS.md` or `CLAUDE.md` when present, supplied requirements, UX flows, direction briefs, existing styles, and assets. Do not require any other skill or a particular input format. Establish the representative task, content, fidelity, and behavior to demonstrate.

Respect an existing preserve/evolve/replace decision. If it is absent and the prototype touches an existing visual language, ask which relationship the user wants before inheriting or discarding styles. Copy the relevant token values or minimal CSS into the artifact when continuity is intended; never make the file depend on the application's stylesheet or component runtime.

Read the [offline artifact contract](references/offline-artifact-contract.md) before creating any HTML. The project's production stack remains context, not a dependency of the artifact.

## Choose fidelity

- **Direction sketches:** normally one HTML file for each of three supplied visual directions, using comparable content and tasks. Show enough responsive layout, typography, and spacing to make the design decision. Add only interactions needed for comparison. Do not deepen a preferred direction before the user chooses unless explicitly delegated.
- **Refined prototype:** develop the selected or explicitly combined direction, representative flows, relevant states, responsive rules, and coherent tokens. If the combination is ambiguous, resolve the conflicting choices rather than averaging the styles silently.
- **Bounded feature or experiment:** build only what answers the user's question; an approved direction does not require three new alternatives.

If asked to build immediately from a rough idea, state a provisional direction and assumptions proportionate to the request. Surface missing decisions that would materially change the result. Do not claim the user approved choices you proposed.

## Build for inspection

Use the [neutral HTML starter](templates/prototype.html) for document structure and adaptation points, not as a prescribed visual style. Replace its sample content, tune tokens, and change composition to fit the brief. The [completed collection example](templates/collection-example.html) demonstrates local filtering and recovery; its [annotation](references/example-notes.md) explains the choices and limitations.

Use meaningful representative content, semantic HTML, visible labels and focus, keyboard-operable controls, and a reading order that survives narrow layouts. Keep the actual app UI free of developer notes, test switches, and approval panels. Put assumptions, simulated behavior, asset provenance, and review questions in the [prototype notes](templates/prototype-notes.md).

Check typography in context: font roles and actual rendered fallbacks, hierarchy, line height, measure, content wrapping, spacing rhythm, and control density. Preserve the selected direction's character while making necessary usability refinements. Flag substantial departures for user review.

## Verify and deliver

Read [interaction and verification guidance](references/interaction-and-verification.md). Open each artifact directly through `file://` when a browser is available, verify it without network access, inspect narrow and wide layouts, and exercise the primary task and recovery with keyboard as well as pointer input. Check relevant zoom, text-spacing overrides, reduced motion, and content pressure.

Fix failures and record what was actually checked. Static inspection alone does not prove rendering or accessibility. If browser or filesystem access is unavailable, deliver copyable HTML and exact manual checks, clearly marked unverified; do not claim screenshots or successful interaction tests.

Return each HTML artifact and companion notes, identify what differs between sketches, and recommend the next decision or refinement. Keep sketches independently usable; a comparison document may link to them, but no HTML artifact may need another file to render or complete its demonstrated task.
