# Adopting into the profile

How to move existing documents into a prototype context without losing anything, without keeping anything twice, and without deciding anything the person has not decided. The inventory, map and verification work as in a full product context. What differs is where things land: a prototype has no versions, no milestones and no plan rows, so the targets below replace the full profile's.

## Inventory

Read every source in full before mapping any of it. Number its sections by heading path, going below a heading when the content under it changes kind:

```
S1   README.md › What Quill is
S2   README.md › Features                       (list of 6, five marked done)
S3   README.md › Roadmap                        (list of 4 ideas)
S4   docs/streaks.md › Rules                    (table of 7 rules)
S5   docs/streaks.md › Why the streak resets at local midnight
S6   AGENTS.md › Build and test commands
S7   AGENTS.md › Conventions
```

Record tables with their row counts and ID ranges; verification compares them later. Include the code in the inventory by reference: a claim that something is built is checked against it (see Built or planned).

## Built or planned

This is the question the profile adds. For every section that states behaviour, decide which of these it is before choosing a destination.

| The source says | Evidence | Lands as |
|---|---|---|
| Behaviour that exists and works | The code, a test, or the person's word | A `built` row in the capability file |
| Behaviour that was planned, started or half-working | The code shows it is missing or partial | A framing note with verdict `park`, or an open question; never a requirement row |
| Behaviour that existed and was removed | The source or the history says so | A `dropped` row with the date and the reason, when the source gives them; otherwise an open question |
| A rule the code enforces | The code | A `built` row, or an architecture concept when it is a cross-cutting rule |

A requirement row means the code does it. Check each claim of "done" against the code (a path, a test, a quick run), and note in the map which evidence was used. When the code and the source disagree, the disagreement is a conflict (below); the row waits for the person's answer. Rows keep the source's wording where it is observable and are rewritten only to remove hedges such as "should" or "will".

## Classify

| Kind | Typical content | Destination |
|---|---|---|
| Product intent | Summary, principles, the problem | `product/overview.md` |
| Assumptions and constraints | Platform floor, what the product never does | `product/overview.md` |
| Vocabulary | Terms the sources define or use with a specific meaning | `product/glossary.md`, with the treatment derive |
| Actors and use cases | Who uses it, what for | `product/actors-and-use-cases.md` |
| Built behaviour | Feature lists marked done, rule tables, user stories the code satisfies | `product/requirements/<capability>.md`, status `built` |
| Qualities | Performance, privacy, footprint targets | `product/requirements/non-functional.md`; a target nobody stated is "to confirm" with an open question |
| Architecture view | Context and container diagrams, components, deployment | `architecture/<view>.md`, `Status: built` only when the code has it, with the evidence named in the map; unbuilt architecture goes to a parked note (see Unbuilt plans) |
| Cross-cutting rule, interface | Error handling, a protocol or schema several parts share | `architecture/concepts/<rule>.md`, `architecture/contracts/<name>.md` |
| External dependency | Libraries, services, platforms | `architecture/ecosystem.md` |
| Decision or rationale | "We chose X because", comparison tables, ADR lists | `decisions/NNNN-<title>.md` |
| Unbuilt plan | Roadmap items, wishlists, TODO lists about the product | A framing note in `research/`, verdict `park`; or an open question |
| Risk, open question | Risk tables, unchecked questions | `notes.md` |
| Evidence | Market scans, benchmarks, source lists | `research/YYYY-MM-DD-<topic>.md`, or next to the claim it supports |
| Build and test instructions, conventions | Commands, code style, agent instructions | Stay with the code: the root `AGENTS.md` or the app README (see Beside the context) |
| Framing | Q&A addressed to a reader, bylines, "where I push back" | Its content to the kinds above; the framing itself is dropped |

A source that speaks of versions or milestones does not get version folders. What shipped is built behaviour; what did not ship is an unbuilt plan; the history of what shipped when belongs in the app's changelog, which changes only through a Beside the context row.

## Unbuilt plans

An unbuilt plan is an idea, and ideas are framed before they are bets. Write each as a short research note, `research/YYYY-MM-DD-<slug>.md`, with the header lines of a framing note, `Date: YYYY-MM-DD`, `Verdict: park` and `Bet: not yet`, then its sections: Idea (the source's words, quoted), Problem, Evidence, Options, Recommendation, Remove if, Verdict. Fill what the source holds and write "not researched" in the rest. The verdict is `park`, with the reason "adopted from `<source>`, not built". Unbuilt architecture is parked the same way, unless a retained open bet introduces it; only then does it stay as a `Status: planned` section. `framing-prototype-ideas` picks a parked note up later and does the research the note lacks.

When a plan is really a question ("do we want reminders at all?"), an open question in `notes.md` with a recommended answer is smaller than a note. Group tiny items of one theme into one note.

## Treatments

| Treatment | Meaning |
|---|---|
| Move | The section goes whole to one destination, text unchanged apart from links |
| Split | Parts go to several destinations; name each |
| Merge | The section duplicates another; keep one home and note which wins |
| Convert | The content changes form: a decision table into records, a feature list into requirement rows, a wishlist into framing notes |
| Derive | A new file built from the sources' content, such as the glossary |
| Drop | Nothing moves; state the reason |

## Existing files

When the target already holds a context folder, for example a full-profile skeleton with `roadmap/`, treat its files as sources and give each one a row under "Existing files" in the migration map: what it becomes, with a treatment.

| Found | Becomes |
|---|---|
| `roadmap/` version folders and briefs | Dropped, with the reason "no versions in the prototype profile"; shipped scope is already in the catalogue as `built`; unshipped scope becomes parked notes |
| Bets from earlier versions | Kept in `bets/` with their numbers, closed ones as `kept` or `removed`. A planned one becomes a parked note and keeps its numbered bet file: the header lines (framing: the parked note) and Status `removed`, with the Result "parked at adoption: not tried, see `<note>`". Bet numbers are never reused, and the board and the next number read these files |
| `roadmap/risks.md`, `roadmap/open-questions.md` | Merged into the two tables of `notes.md`, IDs unchanged |
| Version, `Since:` and milestone columns or lines | Removed; requirement status becomes `built` or `dropped`; architecture is classified against the code, `built` with evidence, or parked unless a retained open bet introduces it |
| `planned` or `deferred` requirement rows | Moved out of the catalogue into a parked note; the ID stays reserved (IDs are permanent), and `id-map.md` records it as reserved with the note it went to, including a prefix that has no capability file. The allocation rule for new IDs reads the catalogue, the board and `id-map.md`. When a later bet builds that same requirement, shaping appends a line to `id-map.md` naming the claiming bet, and the bet's `new` delta keeps the reserved ID; the reservation is then the bet's own. Unrelated scope never reuses the number |

Nothing in an existing skeleton is removed before the person approves the map.

## Beside the context

Documents outside `context/`, such as an app README, the root `AGENTS.md` or a docs folder, belong to the code. Adopting changes them only through "Beside the context" rows, each applied with the person's agreement:

- A README whose content moved into the context keeps a short pointer instead of the moved text.
- The root `AGENTS.md` gains the two pointer lines (the context map and the decisions index) and loses nothing else.
- A docs file whose content moved entirely is removed only when the person says so; until then it is listed.

A row the person does not agree to stays as it is, and the destination in `context/` holds the content anyway: the duplicate is reported as a fact kept in two places for the person to resolve.

## Conflicts and duplicates

| Signal | Example | Handling |
|---|---|---|
| The same fact twice | A rule in the README and in `docs/streaks.md` | Merge into one home; the other source row maps to merge |
| The source says done, the code says no | README lists a weekly recap that is not in the code | An open question with the evidence; no row until answered |
| The code does it, no source says so | A grace period in the code that no document mentions | A `built` row proposed in the map, flagged "from the code", for the person to confirm |
| Contradictory statements | Reset at local midnight in one place, UTC in another | An open question with the recommended answer, citing the code |
| Two numbering schemes | Decision numbers in two files | One log; list both numberings in the map |

Recommend an answer for each, with its reason. Do not resolve a conflict silently, and do not keep both versions.

## Links

- Links between sources become relative links to the new homes.
- Links from the code repository to moved documents are Beside the context rows.
- Links to external sources stay, next to the claim they support.

## Verify

Walk the inventory after moving:

- Every row maps to at least one destination that holds its content, or to a stated drop reason.
- Every ID table has the same row count and ID range as its source, or is mapped in `id-map.md`.
- Every `built` row has its evidence named in the map.
- No requirement row describes something unbuilt.
- Every `built` architecture section has evidence, and every `planned` section has a retained open bet that introduces it.
- Every legacy bet has a numbered bet file, and every reserved ID is in `id-map.md`.
- Every row under Existing files and Beside the context is applied, or listed as left, with the reason.
- Every relative link resolves, and no fact appears in two files except in derived indexes.

Save the map with the result as `research/YYYY-MM-DD-migration-map.md`.

## Worked example

Quill's code repository holds a `README.md` (what it is, a feature list, a roadmap), `docs/streaks.md` (the streak rules and why), and a root `AGENTS.md` with build commands. The person asks to adopt them. An excerpt of the map:

| # | Source section | Destination | Treatment | Notes |
|---|---|---|---|---|
| S1 | README › What Quill is | `product/overview.md` | move | |
| S2 | README › Features (5 done, 1 started) | `product/requirements/streaks.md` | convert | STK-01 to STK-05 `built`, evidence `src/streak.ts` and its tests; the sixth, the weekly recap, is not in the code: see S3 and OQ-01 |
| S3 | README › Roadmap (4 ideas) | `research/2026-11-06-quill-ideas.md` | convert | One parked note: weekly recap, reminders, export, themes; verdict `park` |
| S4 | docs/streaks.md › Rules (7) | `product/requirements/streaks.md`, `architecture/concepts/day-boundary.md` | split | Four rules are rows STK-06 to STK-09; the three that govern how days are cut go to the concept |
| S5 | docs/streaks.md › Why the streak resets at local midnight | `decisions/0002-reset-at-local-midnight.md` | convert | `proposed`: the sources state it, the person has not confirmed it |
| S6 | AGENTS.md › Build and test commands | none | drop | Stays with the code; not context |

Beside the context:

| File | Change | Why | Agreed |
|---|---|---|---|
| `README.md` | Replace Features and Roadmap with a pointer to `context/` | Their content moved | pending |
| `AGENTS.md` | Add the two pointer lines | Agents find the context | pending |

Conflicts raised: OQ-01 (the README lists the weekly recap as done; the code has no such feature; recommended: park it). Gaps reported: no glossary, no non-functional targets, no changelog; `release-process` writes one, or the changelog template does when that skill is missing.
