# Readiness and traceability

## Reconcile intent before packaging

Inspect user decisions, requirements, UX, selected design, and actual prototype behavior together. A requirement can be approved while a prototype is still exploratory. A prototype can demonstrate useful behavior that has not yet been agreed. State the difference.

If documents disagree, identify the conflicting statements and the resulting user-visible behavior. Use explicit user decisions and applicable project instructions to resolve what they settle. Ask about an unresolved substantive conflict rather than inventing a universal source-precedence policy.

## Minimum traceability

| Requirement | UX behavior | Prototype evidence | Acceptance criterion | Gap |
|---|---|---|---|---|
| Stable ID or source section | Screen/state/action | Artifact and relevant element or state | Observable result or reference | Missing, simulated, unverified, or none |

Use identifiers only where they help connect artifacts. Avoid a separate registry for every control. Verify referenced files and sections exist in the target project. The prototype evidence column describes demonstrated behavior, not an assertion of automated testing.

## Visual contract

State the chosen direction and any explicit combination. Include typography roles, actual and intended font faces, weights, sizes, line heights, text measure, spacing tokens, layout rhythm, color roles, and responsive changes. Map copied tokens back to project sources when available. Note where a prototype uses a fallback instead of the intended asset.

Treat values as agreed, provisional, or inherited according to the actual decisions. Do not require the implementer to reverse-engineer a screenshot to discover them. Preserve motion and interaction expectations where they affect the experience.

## Readiness boundaries

- **Ready for engineering planning:** essential product behavior and visual intent are agreed, acceptance criteria are usable, and remaining questions are engineering concerns or accepted nonblocking limitations.
- **Ready for prototype evaluation:** the artifact can answer the learning question, but the hypothesis has not yet been validated. State proposed evaluation and missing observations.
- **Needs product/design decisions:** unresolved scope, conflicting behavior, unselected consequential visual choices, or missing content assumptions prevent a coherent plan. List exact decisions and work that can continue independently.

Missing stack choice alone does not imply product/design failure. A design depending on an unavailable device capability or data source may have a feasibility blocker; identify that dependency rather than promising implementation will solve it.

## Delivery slices and verification

Prefer useful increments: browse readable guides; narrow and recover; complete the next agreed journey. Include acceptance checks with each slice. Do not substitute horizontal layers such as “build all components” for user outcomes. Architectural dependencies can remain engineering questions without a fabricated API schema.

Document verification honestly: browser and viewport conditions, actions exercised, static-only checks, and limitations. Do not turn visual approval into evidence about research, accessibility conformance, or production performance.
