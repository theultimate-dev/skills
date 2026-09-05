# Typography and spacing

## Choose for reading and action

Begin with the audience's tasks, content density, languages, device conditions, and existing product identity. Long-form reading, scanning a collection, and manipulating dense records place different demands on type. Do not prescribe a font pairing independent of those conditions.

Specify roles before font names: body reading, display headings, compact UI labels, and numeric or code content where needed. One well-chosen family may cover several roles. For each chosen face, explain its purpose and check required weights, italic treatment, distinguishing characters, and language coverage. Avoid synthesized weights when the intended face matters.

Show candidate typography with actual headings, labels, long titles, and paragraphs. Discuss substantial font and hierarchy choices with the user through rendered alternatives; routine refinements within the selected direction need not each become a new approval step.

## Make the rhythm concrete

Document a small token vocabulary: font families, body size, heading sizes, weights, line heights, readable measure, spacing steps, content width, and layout gaps. Use CSS custom properties in the sketches. Name roles clearly so the handoff can map them to the target project's conventions later.

Useful starting hypotheses, not universal rules:

- A reading-focused body might start at 1rem to 1.125rem with a line height around 1.5 to 1.7 and a measure around 60 to 70 characters.
- A compact index may use less inter-item space while retaining comfortable label sizing, readable summaries, and distinct interactive targets.
- A restrained spacing scale such as 0.25rem, 0.5rem, 0.75rem, 1rem, 1.5rem, 2rem, and 3rem can simplify rhythm; choose values to express relationships, not to satisfy a mathematical pattern.

Related elements should look related through proximity. Separate major sections more than labels from their values. Check optical balance with real content instead of insisting every gap be mechanically identical. [W3C design guidance](https://www.w3.org/WAI/tips/designing/) explains how headings and spacing communicate grouping.

Use responsive type and spacing deliberately. Large headings must wrap without crushing nearby actions. Set a sensible maximum text measure, allow long words or identifiers to wrap where appropriate, and inspect both sparse and dense content. Preserve hierarchy when columns collapse.

## Offline font fidelity

The rendering brief must distinguish the intended face from what the prototype can actually render. If an appropriate font file and redistribution permission are available, embed it in the HTML with a data URL and retain required notices. Do not assume a desktop-installed or subscription font may be redistributed.

If embedding is unavailable, choose an explicit system fallback, record the intended face and limitation, and inspect the fallback layout. Do not use only `local()` and call the artifact typographically portable: it can resolve differently on another machine. The [MDN font-face reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@font-face) documents font sources and descriptors.

## Review type and spacing together

Assess the first visual hierarchy, sustained reading, scanability, line wrapping, controls, and narrow layouts. Check zoom and user spacing overrides for clipped or overlapping content. The [W3C text-spacing criterion](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html) concerns tolerating overrides; its values are not mandatory authored typography defaults.

Record decisions in context: “Use the tighter list gap to keep title and summary together while preserving the larger gap between guides” is more useful than “make it cleaner.” Keep font limitations and still-provisional choices visible in the companion notes and handoff.
