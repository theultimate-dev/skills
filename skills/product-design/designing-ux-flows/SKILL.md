---
name: designing-ux-flows
description: "Translate product requirements into UX flows, information hierarchy, screen responsibilities, interaction rules, content needs, and relevant interface states. Use when a user journey or feature behavior needs to be worked out before visual design or implementation."
license: MIT
---

# Designing UX flows

Make the intended experience concrete enough to walk through, including how people recover when something goes wrong. Work at the behavior level; leave component libraries and backend architecture to project decisions.

## Establish inputs

Read applicable project instructions, existing requirements, current screens, navigation, and interaction conventions. Include `AGENTS.md` or `CLAUDE.md` when present. A supplied brief or direct user request can be enough; do not require a particular upstream skill or document format.

Identify the primary actor, trigger, desired result, scope, and known constraints. Respect established stack limitations when relevant. If a missing requirement would materially change the journey, surface that question with a proposed answer before treating the flow as settled.

## Model the experience

Read [flows and states](references/flows-and-states.md). Define the primary journey first, then only the branches needed to evaluate it. Specify entry and exit points, available actions, feedback, relevant state transitions, and recovery. Map screens or sections to responsibilities so navigation and hierarchy follow the task.

Include representative content, control labels, validation messages, and long-content cases where they influence design. State what information must be available; do not invent data or API contracts. For an existing product, preserve familiar navigation unless redesign is in scope.

Consider keyboard and touch operation, visible focus, reading order, and narrow layouts while defining behavior. For dynamic controls, describe where focus goes and what feedback is announced. Avoid adding a modal, hover-only control, or multi-step flow unless it helps the task.

Use a small flow diagram only when branches or transitions are clearer visually. A sentence is enough for a one-step action. Use the [UX specification template](templates/ux-specification.md), scaled to the task. Read the [worked recovery journey](references/worked-journey.md) for an example of interaction precision without architecture decisions.

## Review and hand onward

Walk through a concrete task from entry to result and recovery. Check every visible action has an intended outcome and every required piece of information has a source or an explicit assumption. Link back to requirement IDs where available.

Return the UX specification, unresolved behavior choices, and the scenes/content that visual sketches must share. If the flow reveals a scope change, identify the affected requirement and ask for that decision rather than hiding the change in a screen design. Treat provisional behavior as provisional.

When file access is unavailable, return the complete specification as Markdown and explain that nothing was written. This skill works independently and does not authorize building the application.
