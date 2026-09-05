# Requirements and uncertainty

## Classify statements before formalizing them

| Statement | Kind | Treatment |
|---|---|---|
| “Readers need a useful guide for their current task.” | Desired outcome | Ask which audience and task, then define the smallest useful result |
| “Let readers filter the collection by topic.” | Candidate functional requirement | Specify trigger, visible result, and relevant edge cases |
| “Use the project's existing type and spacing tokens.” | Constraint | Carry into design and prototype instructions |
| “A magazine layout will make guides feel more credible.” | Design hypothesis | Compare it with alternatives; do not present credibility as established |
| “Use a particular search library.” | Implementation suggestion | Keep separate unless already an explicit project decision |

Write behavior from the user's perspective. Useful requirement: “Selecting a topic shows matching guides and the count; clearing it restores the full collection.” Weak requirement: “Filtering should be intuitive and modern.” Overspecified requirement: “Implement a particular component and cache library” when neither is an established constraint.

## Acceptance criteria

Use concrete examples or Given/When/Then when sequence matters. Include the happy path and failures that affect the intended outcome. Do not enumerate imaginary network errors for an offline static interaction.

For filtering:

- With six guides and two tagged Writing, selecting Writing displays those two and a count of two.
- With no matching guides, the collection explains the empty result and provides a clear recovery action.
- Clearing the topic restores all six, and keyboard users can continue from the control they operated.

These are behavior criteria, not a mandate to use any particular data model or component library.

## Evidence and priorities

Label user statements, inspected implementation, observed research, and assumptions separately. An agent's heuristic review is a recommendation, not observed user behavior. Avoid fabricated personas with unsupported demographic detail.

Use the project's priority scheme. Otherwise use “required for this outcome,” “useful later,” and “excluded.” For each required item, ask whether removing it prevents the stated outcome. Do not call every attractive addition essential.

Give uncertain requirements a provisional status. Explain what would change if an assumption is false and whether it blocks the next task. Missing stack details often do not block visual discovery; unsupported device capabilities or unavailable source data may.

## Scale by the question

A small feature may need one paragraph, a few requirements, and acceptance examples. A whole application benefits from separate journeys and explicit boundaries. A proof of concept should specify the hypothesis, the demonstration or evaluation, and the observation that would support, reject, or leave the hypothesis unresolved. Do not invent an arbitrary success percentage without a reason and user agreement.
