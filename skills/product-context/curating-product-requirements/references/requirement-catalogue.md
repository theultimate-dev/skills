# The requirement catalogue

How to write and keep the rows in `product/requirements/`. The examples use Larder, a fictional household pantry and meal-planning app; its capabilities are pantry (`PAN`), meal plans (`MEA`), shopping list (`SHO`) and sync (`SYN`).

## Row format

Each capability file holds one table:

| ID | Requirement | Priority | Version | Status | Notes |
|---|---|---|---|---|---|
| PAN-03 | Remove an item from the pantry | Must | V1.1 | built | |
| PAN-07 | List pantry items by expiry date | Should | V1.1 | planned | Extends PAN-04 |
| PAN-05 | Import a pantry from a spreadsheet | Could | | dropped | 2026-11-02: dropped, decision 0006 |

- **ID**: the capability prefix and a two-digit number, the next after the highest ever used in the file.
- **Requirement**: one capability or rule, from the user's or caller's side, in the present tense.
- **Priority**: `Must`, `Should` or `Could` for the version it targets. "Won't" is not a priority: such a row is `deferred` or `dropped`.
- **Version**: the target, in the roadmap's labels: a version (`V1`) before a milestone is chosen, then the milestone (`V1.2`). Empty until someone with authority states it, and empty on a `deferred` row, which has no target. Retargeting is a roadmap change, made through `planning-product-roadmaps`.
- **Status**: `planned`, `built`, `deferred` or `dropped`. `built` is set when a bet that covers the requirement closes; a partially delivered requirement stays `planned` with a note on the part that shipped.
- **Notes**: short facts only: "extends PAN-04", "part built in V1.1: single device", "dropped 2026-11-02: reason", a decision number. Register and bet IDs, such as `OQ-06` or "rule from Bet 07, AC-E2", appear as plain text for provenance, never as links. No rationale paragraphs.

## Writing a good requirement

| Weak | Why | Better |
|---|---|---|
| The app should handle expiry well | Not observable | Warn the household about items expiring within a number of days they choose |
| Sync uses a change feed over WebSockets | Implementation, not behaviour | An item changed on one device appears on the household's other devices |
| Scan barcodes and edit quantities and share the list | Three capabilities in one row | Three rows, one capability each |
| Fast search | Quality without a target | A non-functional row: "NFR-04 Pantry search returns results as the user types", target to confirm |
| As a parent I want meal plans so that dinner is easy | A story, not a capability; the rationale belongs elsewhere | Plan meals for a week from the recipes the household saved |

EARS patterns help when behaviour depends on an event, a state or an unwanted situation. Use them when they make a row clearer, not for every row:

| Pattern | Shape | Example |
|---|---|---|
| Event-driven | When [trigger], the [system] shall [response] | When a pantry item reaches its expiry date, Larder shall notify every member of the household |
| State-driven | While [state], the [system] shall [response] | While a device is offline, Larder shall keep the shopping list editable |
| Unwanted behaviour | If [condition], then the [system] shall [response] | If two members change the same item at once, then Larder shall keep both changes visible until one is chosen |
| Optional feature | Where [feature is enabled], the [system] shall [response] | Where barcode scanning is enabled, Larder shall fill in the item's name and size |

## Functional, non-functional, or neither

| It is | Example | Goes to |
|---|---|---|
| A functional requirement | Share a shopping list with the household | A capability file |
| A non-functional requirement | The web app works with a screen reader | `non-functional.md` |
| A constraint | Runs on the two most recent versions of each major browser | `product/overview.md`, Assumptions and constraints |
| An assumption | Households have at most eight members | `product/overview.md`, Assumptions and constraints, with what changes if it is wrong |
| A design detail | The expiry badge is amber three days before the date | The design files of its initiative |
| An implementation choice | Store the pantry in a relational database | A decision record or `architecture/`, through `designing-system-architecture` when it is installed; `proposed` unless the user made the choice |
| A question | Should a guest see the pantry? | The open-question register |

## Non-functional requirements

`non-functional.md` uses one table:

| ID | Area | Requirement | Target | Version | Status | Notes |
|---|---|---|---|---|---|---|
| NFR-02 | Performance | A change made on one device appears on the others quickly | p95 under 5 s on a normal connection | V1.1 | built | |
| NFR-04 | Performance | Pantry search returns results as the user types | to confirm | V1.2 | planned | OQ-06 |

- Common areas: reliability, performance, capacity, footprint, security, privacy, accessibility, compatibility, maintainability, observability, operability, cost.
- A target is a number or an observable condition the user stated or accepted. Anything else is "to confirm", with an open question that asks for it; its ID goes in Notes as plain text, never a link.
- A product-wide principle that every requirement obeys, such as "no feature depends on being online", belongs in the overview's principles; non-functional rows make such principles checkable.

## Priorities, versions and statuses

- Priority is relative to the target version. Re-prioritising is a curation change; moving versions is a roadmap change.
- A requirement may span versions: give the version that delivers the first part, and note the split, such as "part in V1: one household; rest in V2: several households". The bets that cover it say which part they deliver.
- Only the close of a bet sets `built`. Do not set it from a pull request, a demo or a promise.
- `deferred` keeps a requirement wanted but unplanned: clear its Version. `dropped` ends it: keep the row, add the date and the reason.

## Changing what exists

| Change | Do |
|---|---|
| Clearer wording, same meaning | Edit the text. No note needed unless a bet already quoted the old text, then note the date |
| Narrower or broader meaning on a `planned` row | Edit the text and note the date and the source of the change. Bets in delivery keep the meaning they were pinned to; say so in the summary |
| Different behaviour on a `built` row | A new row that names the one it changes in Notes. The built row keeps describing what shipped, until the new row is built and the old one is dropped with "replaced by" |
| Split | Keep the original ID for the part closest to its old meaning; give the rest new IDs; note the split on each |
| Merge | Keep one ID; drop the other with "merged into" |
| Promoted rule from a closed bet | Fold a clarification of the existing meaning into the text, noting the bet and criterion it came from as plain text; give added behaviour a new row with status `built` |

## Consistency checks

Run these when asked to clean up, and on any change that touches more than a few rows:

1. **Duplicates and overlaps**: two rows a single bet could not deliver one without the other, or that say the same thing in different words.
2. **Compound rows**: rows with "and" joining two capabilities.
3. **Implementation leaks**: component names, technologies, storage or protocols in requirement text.
4. **Untraced use cases**: a use case no requirement serves, or a capability no use case needs.
5. **Undefined terms**: words in requirements that the glossary lacks, or aliases it marks to avoid.
6. **Targets**: non-functional rows without a target or an open question.
7. **ID hygiene**: gaps are fine; reused numbers, duplicate IDs and rows without a status are not.
8. **Rationale in rows**: why-sentences in Requirement or Notes that belong in a decision record or the overview.
9. **Versions**: a version label the roadmap does not know. Report it to `planning-product-roadmaps`; do not fix it here.

Report findings as a numbered list with the row IDs, the fix you recommend, and which fixes need the user's decision.
