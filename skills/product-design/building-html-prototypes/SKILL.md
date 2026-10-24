---
name: building-html-prototypes
description: "Build responsive UI sketches and interactive prototypes as offline HTML: by default one self-contained file with embedded CSS, assets, and minimal JavaScript, or a design tree of pages that link the project's shared tokens and component styles by relative path. Use to compare design directions or refine an agreed application or feature experience before production implementation."
license: MIT
---

# Building HTML prototypes

Produce artifacts that the user can open directly, compare, and pass to another person without an application runtime. The prototype demonstrates design intent and selected behavior; it is not production implementation.

## Establish the task

Read applicable project instructions, including `AGENTS.md` or `CLAUDE.md` when present, supplied requirements, UX flows, direction briefs, existing styles, and assets. Do not require any other skill or a particular input format. Establish the representative task, content, fidelity, and behavior to demonstrate.

Respect an existing preserve/evolve/replace decision. If it is absent and the prototype touches an existing visual language, ask which relationship the user wants before inheriting or discarding styles. When continuity is intended, a design tree links the project's shared design files, and a one-file artifact copies the relevant token values or minimal CSS. Never make a prototype depend on the application's stylesheet, build, or component runtime.

## Choose the portability contract

- **Design tree:** when the project already keeps shared design files, such as `tokens.css` or `components.css`, or the user asks for them. Every page is a full HTML document that links the shared files by relative path and opens offline while the tree stays together. Read the [design-tree contract](references/design-tree-contract.md).
- **One-file artifact:** otherwise. It is also the default for direction sketches, even when the project keeps shared design files; a sketch may keep its candidate tokens inline until the user chooses a direction. Read the [offline artifact contract](references/offline-artifact-contract.md).

Read the chosen contract before creating any HTML, and name it in the notes. The project's production stack remains context, not a dependency of the prototype.

## Choose fidelity

- **Direction sketches:** normally one HTML file for each of three supplied visual directions, using comparable content and tasks. Show enough responsive layout, typography, and spacing to make the design decision. Add only interactions needed for comparison. Do not deepen a preferred direction before the user chooses unless explicitly delegated.
- **Refined prototype:** develop the selected or explicitly combined direction, representative flows, relevant states, responsive rules, and coherent tokens. In a design tree, the pages link the shared files rather than copying their rules. If the combination is ambiguous, resolve the conflicting choices rather than averaging the styles silently.
- **Bounded feature or experiment:** build only what answers the user's question; an approved direction does not require three new alternatives.

If asked to build immediately from a rough idea, state a provisional direction and assumptions proportionate to the request. Surface missing decisions that would materially change the result. Do not claim the user approved choices you proposed.

## Build for inspection

Use the [neutral HTML starter](templates/prototype.html) for document structure and adaptation points, not as a prescribed visual style. Replace its sample content, tune tokens, and change composition to fit the brief. The [completed collection example](templates/collection-example.html) demonstrates local filtering and recovery; its [annotation](references/example-notes.md) explains the choices and limitations.

Use meaningful representative content, semantic HTML, visible labels and focus, keyboard-operable controls, and a reading order that survives narrow layouts. Keep the actual app UI free of developer notes, test switches, and approval panels. Put assumptions, simulated behavior, asset provenance, and review questions in the [prototype notes](templates/prototype-notes.md).

Check typography in context: font roles and actual rendered fallbacks, hierarchy, line height, measure, content wrapping, spacing rhythm, and control density. Preserve the selected direction's character while making necessary usability refinements. Flag substantial departures for user review.

## Verify and deliver

Read [interaction and verification guidance](references/interaction-and-verification.md). For a design tree, run the [design-tree check](templates/tree-check.html) first. Open each artifact directly through `file://` when a browser is available, verify it without network access, inspect narrow and wide layouts, and exercise the primary task and recovery with keyboard as well as pointer input. Check relevant zoom, text-spacing overrides, reduced motion, and content pressure.

Fix failures and record what was actually checked. Static inspection alone does not prove rendering or accessibility. If browser or filesystem access is unavailable, deliver copyable HTML and exact manual checks, clearly marked unverified; do not claim screenshots or successful interaction tests.

Return each HTML artifact and companion notes, identify what differs between sketches, and recommend the next decision or refinement. Keep sketches independently usable; a comparison document may link to them. A one-file artifact needs no other file to render or complete its demonstrated task. A design-tree page needs only files inside its tree, and its notes list the shared files it links.
