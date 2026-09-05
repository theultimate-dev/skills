---
name: exploring-visual-directions
description: "Develop and compare distinct visual direction briefs for a user-facing application or feature, including composition, typography, spacing, density, color, imagery, and motion. Use when visual identity or UI design is unresolved, before rendering and choosing HTML prototype directions."
license: MIT
---

# Exploring visual directions

Make visual alternatives specific enough to render and compare. Distinctiveness should come from the product's audience, content, and purpose, not an arbitrary collection of fashionable effects.

## Ground the exploration

Read applicable project instructions, including `AGENTS.md` or `CLAUDE.md` when present, requirements, UX flows, real content, existing screens, tokens, fonts, and brand assets. Use supplied materials when repository access is unavailable and identify the gap. Do not require another skill's output format.

Establish whether the user wants to preserve, evolve, or replace the existing visual language. Reuse a prior explicit choice. If it is unresolved, explain the concrete alternatives and ask before treating project styles as mandatory or disposable. Record which constraints remain fixed and which can change.

Respect the project's established technology where it affects feasibility. Do not choose a stack or let a component library's default appearance become the design brief. Missing technology does not prevent exploring composition and typography.

## Develop comparable alternatives

Read [inspiration and critique](references/inspiration-and-critique.md) when gathering references or deciding how alternatives should differ. Use project materials first and targeted public references when useful. Explain the principle adapted from each source. Never invent research, copy another product's identity, or promise global uniqueness.

Default to three direction briefs for unresolved visual design, using the same representative content and user task. Vary meaningful properties such as composition, hierarchy, density, type character, or the way information is explored. A palette swap is not a separate direction. Adapt the count when the user has already narrowed the choice or explicitly requests otherwise.

For each direction, state the premise, audience fit, composition, visual hierarchy, typography, spacing, color roles, imagery, motion if justified, responsive changes, and usability risks. Include a small set of concrete candidate token values rather than only mood adjectives. Read [typography and spacing](references/typography-and-spacing.md) before choosing them.

Use the [direction comparison template](templates/direction-comparison.md). The [annotated directions](references/annotated-directions.md) show how three hypotheses can share content without sharing a layout. They are examples to reason from, not fixed styles to reproduce.

## Prepare the visual decision

Return the briefs and a rendering task for three independent offline HTML sketches. Supply the representative content, scenes, tokens, constraints, and questions each sketch should answer. When available, `building-html-prototypes` can render them; this skill itself remains usable as a standalone brief-writing capability. Do not report unrendered briefs as prototypes.

Recommend a direction provisionally with concrete reasons. Final direction selection should use rendered sketches, including their typography and spacing at narrow and wide sizes. If the user combines elements, specify the resulting composition and tokens instead of handing on an ambiguous “mix A and B.” Record user approval or delegated decisions accurately.

Do not require fresh alternatives when an existing direction is already approved. Revisit only decisions affected by new evidence or requested changes. Without file access, provide complete copyable briefs and say that no files were written.
