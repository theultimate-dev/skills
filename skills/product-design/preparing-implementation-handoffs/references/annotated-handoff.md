# Annotated handoff: saved-guide filtering

Fictional example. Approval and verification statements illustrate the information a real handoff should contain; they are not results from a real project.

## Outcome and status

Readers can narrow an existing saved collection by topic and recover from no matches. In this example, the user agreed the behavior and requested preserving the current visual language. Sign-in, saving/removing guides, taxonomy changes, and recommendations are excluded.

The handoff is ready for engineering planning once source artifacts and their agreement are confirmed. Missing production search architecture is an engineering question; the prototype need not implement a backend.

## Traceability example

| Requirement | UX and prototype behavior | Acceptance | Gap |
|---|---|---|---|
| R1: filter by topic | Topic select updates local guides and count | Writing displays two matching guides; focus remains on select | Production data retrieval undecided |
| R2: clear filter | Clear action selects All topics and restores list | Three guides return; focus lands on remaining select | No persistence across reloads |
| R3: recover from no matches | Making displays zero results and recovery message | Clear filter is reachable and restores all guides | Spoken status needs assistive-technology verification |

In a real handoff, each row links to the current requirement, UX section, and delivered HTML. Do not link to an unrelated example merely because its controls look similar.

## Visual contract example

Preserve the project's approved text and surface colors, 1rem UI body size, and spacing steps of 0.5rem, 1rem, and 1.5rem. Place the visible topic label above its select. Keep titles and summaries grouped, with greater separation between guides. At narrow widths, place the filter before the list and allow labels and titles to wrap.

If the prototype uses a system fallback instead of the intended font, identify both and the missing asset. Point to actual copied token sources where they exist, rather than asserting these illustrative values came from a real repository.

## Suggested slices

1. Preserve readable collection content and existing navigation while preparing the topic control in the established design.
2. Deliver filtering, result feedback, and empty-state recovery together, with checks for matching, no matches, and clearing.

Engineering decides how topics and results reach the interface and whether URL or session persistence belongs in a later requirement. The handoff does not infer either from a local demonstration.

## Verification reporting example

Useful: “Static inspection found no external assets. Browser interaction and assistive-technology checks are pending.” Unhelpful: “Accessible and production-ready.” If browser checks were performed, record environment, actions, outcomes, and remaining limits instead of copying a checklist as passed.
