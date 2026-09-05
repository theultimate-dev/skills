# Worked examples

These fictional examples illustrate judgment; they are not product requirements or research findings.

## New application: Fieldnotes

Request: “I want somewhere for readers to find my practical field guides. I have no designs.”

Inspection finds only a short description and no chosen stack. The coordinator asks about the primary audience and whether the first useful outcome is finding a guide or publishing one. The user chooses reader discovery; authoring tools and accounts are excluded.

The brief proposes browsing and filtering a small guide collection. UX defines a collection, an individual guide, no matches, and a way to clear filters. The direction skill proposes an editorial reading room, a compact field index, and an illustrated trail map. The prototype skill renders the same three sample guides and discovery task in each sketch, using inline assets and system fonts with documented limitations.

The user chooses the reading room with the index's compact filter placement. That combination is recorded explicitly. The refined prototype demonstrates filtering, a guide view, empty results, and return navigation. A proposed remote search service remains an engineering question, not an implied requirement.

The handoff connects requirements to screens and acceptance criteria. Suggested slices begin with browsing readable content, then filtering and recovery. Stack selection remains open because none of the agreed interactions required a framework choice. The next engineering task receives that fact.

## Existing feature: filter a saved collection

Request: “Add filtering to saved guides. Keep our current design.”

Inspection finds approved project typography, spacing tokens, and the collection page. The coordinator reuses them and a single discovery document. The brief defines filtering by topic and an empty state. UX specifies immediate local filtering, result count, and clearing the filter without losing focus.

No three-direction exploration is needed: visual continuity is already decided. One offline HTML prototype copies the relevant token values and uses invented guide titles. It does not import the application's stylesheet or load its component runtime. A font that cannot be embedded uses a documented fallback.

If the user later requests a completely different information layout, visual exploration reopens while the approved filtering behavior stays agreed. Only affected decisions need review.

## Proof of concept: can readers distinguish categories?

The question is whether three unfamiliar topic names help readers find a guide. The artifact contains one collection and enough realistic sample titles to compare categories. There is no reason to design sign-in, an editor, or a production data model.

Record the hypothesis, a small task-based evaluation proposal, and what observations would favor revising the labels. Agent inspection may find confusing wording, but it cannot establish that readers understand the taxonomy. Handoff can say “prototype ready for evaluation” while the broader product remains unvalidated.

## Recovery cases

- **Specialist absent:** package the current scope, representative content, constraints, and offline requirement into a task brief. Mark sketches pending, not complete. Continue resolving content questions.
- **No browser:** deliver HTML and a manual verification checklist, marked unverified. Do not manufacture screenshots or claim keyboard checks passed.
- **Session resumes:** inspect the index and artifact contents, carry forward the user's selected direction, and work on the unresolved states instead of producing three new alternatives.
- **Conflicting instructions:** explain the concrete conflict and its impact. Follow applicable instruction precedence; do not silently discard established project constraints.
