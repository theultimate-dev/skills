# Adopting documents

How to move existing product documents into the layers without losing anything, without keeping anything twice, and without deciding anything the user has not decided.

## Inventory

Read every source in full before mapping any of it. Then number its sections by heading path:

```
S1   larder-prd.md › Summary
S2   larder-prd.md › Summary › Answers to the founders' questions
S3   larder-prd.md › Assumptions
S12  larder-prd.md › Requirements › Pantry           (table PAN-01 … PAN-06)
S13  larder-prd.md › Requirements › Meal plans       (table MEA-01 … MEA-07)
S21  larder-v1.md › Milestones › 1.1 Pantry
```

Go below a heading when the content under it changes kind: a requirement table inside a chapter on scope is its own row; a paragraph of rationale under a decision table is its own row. Record tables with their row counts and ID ranges; verification compares them later.

## Classify

| Kind | Typical content | Destination |
|---|---|---|
| Product intent | Vision, summary, principles, tagline, the problem | `product/overview.md` |
| Assumptions and constraints | Platform floor, operating model, what the product never does | `product/overview.md` |
| Vocabulary | Terms the sources define or use with a specific meaning | `product/glossary.md`, with the treatment derive |
| Actors and use cases | Who uses it, what for | `product/actors-and-use-cases.md` |
| Requirements | ID tables, user stories, "the system shall" lists | `product/requirements/<capability>.md` |
| Non-functional requirements | Targets for performance, reliability, security, footprint | `product/requirements/non-functional.md` |
| Surfaces and business | Per-platform capability maps; licensing, pricing, ownership, costs | `product/platforms.md`, `product/business.md` |
| Architecture view | Context and container diagrams, component lists, deployment, packaging | `architecture/<view>.md` |
| Runtime scenario | Flows, sequences, state machines | `architecture/runtime/<topic>.md` |
| Cross-cutting rule | Security boundaries, error handling, consistency rules | `architecture/concepts/<rule>.md` |
| Interface | Protocols, APIs, schemas several parts share | `architecture/contracts/<name>.md` |
| External dependency | Libraries, services, platforms the product builds on | `architecture/ecosystem.md` |
| Decision or rationale | "We chose X because", comparison tables, ADR lists | `decisions/NNNN-<title>.md` |
| Plan | Versions, milestones, phases, timelines, done-when | `roadmap/README.md`, `roadmap/vN/README.md` |
| Risk, open question | Risk tables, unchecked questions, TODO lists about the product | `roadmap/risks.md`, `roadmap/open-questions.md` |
| Prerequisite outside the code | Accounts, legal checks, purchases, enrolments | The version brief's prerequisites |
| Evidence | Market scans, name checks, benchmarks, source lists | `research/YYYY-MM-DD-<topic>.md`, or next to the claim it supports |
| Framing | Q&A addressed to a reader, bylines, "where I push back" | Its content to its kinds above; the framing itself is dropped |

A section about one version goes to the same layer as any other section of its kind, tagged with the version. Architecture for V2 goes into `architecture/` with `Since: V2 · Status: planned`; it does not get a V2 architecture file.

## Treatments

| Treatment | Meaning |
|---|---|
| Move | The section goes whole to one destination, text unchanged apart from links |
| Split | Parts go to several destinations; name each |
| Merge | The section duplicates another; keep one home and note which wins |
| Convert | The content changes form, such as a decision table becoming decision records or a checklist becoming register rows |
| Derive | A new file built from the sources' content, such as the glossary from the domain model |
| Drop | Nothing moves; state the reason, such as "framing", "superseded by S14", or "byline: git keeps authorship" |

## Conflicts and duplicates

Look for these across every pair of sources:

| Signal | Example | Handling |
|---|---|---|
| The same fact twice | The same risk in the PRD and in the V1 plan | Merge into one register row |
| Two numbering schemes | Ten "key decisions" in the PRD, six numbered ADRs in the V1 plan, overlapping | One log; list both numberings in the map; the user confirms the order |
| A promise without a requirement | A milestone promises reminders that no requirement covers | An open question: add a requirement, or move the promise |
| Counts that disagree | "V1 delivers 40 requirements" while the tables say 38 | An open question, with both counts and the rows that differ |
| Contradictory statements | Retention 30 days in one place, 90 in another | An open question, with the recommended answer |

Recommend an answer for each, with its reason. Do not resolve a conflict silently, and do not keep both versions.

## Links

- Links between sources, including links to hosted copies of them, become relative links to the new homes.
- Links to external sources stay, next to the claim they support.
- Anchors into a long source document become links to the new file, plus an anchor when the destination is still long.

## Verify

Walk the inventory after moving:

- Every row maps to at least one destination file that holds its content, or to a stated drop reason.
- Every ID table has the same row count and ID range as its source.
- Every relative link resolves.
- No fact appears in two files, except in derived indexes.
- Every decision record carries a status that matches what the user decided.

Save the map with the result as `research/YYYY-MM-DD-migration-map.md`.

## Worked example

Three sources: `larder-prd.md` (the whole product, 40 sections), `larder-v1.md` and `larder-v2.md` (one per version). An excerpt of the map:

| # | Source section | Destination | Treatment | Notes |
|---|---|---|---|---|
| S1 | PRD › Summary | `product/overview.md` | move | |
| S2 | PRD › Answers to the founders' questions | `decisions/0002`–`0004`, `product/overview.md` | merge | The three answers are key decisions 1 to 3 of S9; Q&A framing dropped |
| S9 | PRD › Key decisions (10) | `decisions/0002`–`0011` | convert | V1 plan's ADR list overlaps: see OQ-01 |
| S12 | PRD › Requirements › Pantry | `product/requirements/pantry.md` | move | PAN-01–06, 6 rows |
| S18 | PRD › Domain model | `architecture/domain-model.md`, `product/glossary.md` | split, derive | Glossary terms derived from the entities |
| S27 | PRD › Risks | `roadmap/risks.md` | convert | Merged with the rows of S48 (V1 risks) and S63 (V2 risks) |
| S33 | PRD › Sources | split by citing section | split | Each source moves next to the claim it supports |
| S34 | PRD › Byline | none | drop | Git keeps authorship |
| S45 | V1 › Architecture on one server | `architecture/deployment.md` | move | Tagged `Since: V1` |
| S58 | V2 › Pairing a household | `architecture/runtime/pairing.md` | move | Tagged `Since: V2 · Status: planned` |

Conflicts raised: OQ-01 (two decision numberings), OQ-02 (milestone 1.1 promises reminders; no requirement). Gaps reported: no glossary, no contracts for the sync protocol, no acceptance criteria.
