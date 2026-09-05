# Interaction and verification

## Build the smallest meaningful interaction

Choose native controls first. A button performs an action; a link navigates. Inputs need visible labels. A custom role does not supply keyboard behavior; consult the relevant [WAI-ARIA guidance](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) only for a widget the task actually requires.

Keep focus where the user's task continues. Filtering normally updates the list without moving focus. If an action hides or removes the focused control, move focus to an appropriate remaining control. Announce short dynamic results politely; do not turn the entire result list into a repeatedly read live region.

Simulate asynchronous states only when exploring that future behavior. Do not add spinners to an immediate local filter. Use explicit local sample data, preserve input on errors, and give useful recovery for empty results.

## Verification sequence

1. **Static portability:** inspect HTML, CSS URLs, scripts, and embedded assets for remote or sibling dependencies, imports, requests, form submissions, and external SVG references. Check inline script syntax.
2. **Direct opening:** open the file itself, not a development server. Block/disconnect the network and reload. Check for failed resource requests and script errors with available browser tools. Browser background traffic is distinct from document requests.
3. **Task behavior:** exercise the primary journey and relevant recovery states. Confirm counts, labels, results, return actions, and simulations behave as described.
4. **Input:** complete the task using keyboard alone, with visible focus and appropriate reading order. Check pointer/touch-relevant controls do not require hover. If announcing dynamic results matters, inspect semantics and use assistive technology when available; DOM inspection alone does not verify spoken output.
5. **Layout:** inspect a narrow viewport around 320 CSS pixels and a representative wide viewport. Test long titles, realistic paragraphs, and relevant missing content. Check wrapping, overlap, and unintended horizontal scrolling; genuinely two-dimensional content may need a different approach. See [W3C reflow guidance](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).
6. **Adaptation:** inspect at 200% text/page zoom and relevant reflow conditions. Override line height to 1.5, paragraph spacing to 2em, letter spacing to 0.12em, and word spacing to 0.16em without losing content or behavior. These are override checks, not required authored defaults; see [W3C text-spacing guidance](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html).
7. **Visual and motion review:** check text/control contrast against the project's accessibility target, type hierarchy, measure, grouping, and density. If animation exists, honor reduced-motion preferences and ensure understanding does not depend on animation.

Use available browser tooling; no particular automation library is required. Record exact checks performed and limitations. A file can pass static checks and still render poorly. Do not claim conformance to an accessibility standard based on a prototype checklist.

## Compare and refine

Inspect the same content and primary task in each sketch at the same viewport sizes. Describe observed differences and unresolved questions. After selection, repeat checks affected by revisions rather than rebuilding every alternative.

The delivered notes should distinguish completed checks, failures, and checks not performed. If browser access is unavailable, provide the manual steps above with the specific task actions and sample outcomes for that artifact.
