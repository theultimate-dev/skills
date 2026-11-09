# Migration map: README, docs/spec.md and AGENTS.md into Sprig prototype context

Date: 2026-11-08 · Mode: adopt · Approved: pending

## Sources

| Source | Sections | Notes |
|---|---|---|
| README.md | 6 | what it is, features, roadmap |
| docs/spec.md | 9 | requirements, plans, architecture |
| AGENTS.md | 3 | commands and the documentation rule |

## Map

| # | Source section | Destination | Treatment | Notes |
|---|---|---|---|---|
| S1 | README.md › What Sprig is | `product/overview.md` | move | |
| S2 | README.md › Features | `product/requirements/plants.md`, `product/requirements/watering.md` | convert | Four rows built; the email reminder is not in the code: see OQ-01 |
| S3 | README.md › Roadmap | `research/2026-11-08-sprig-ideas.md` | convert | One parked note, verdict park |
| S4 | README.md › Decisions | `decisions/` | convert | Records, proposed; numbering conflict OQ-05 |
| S5 | README.md › Risks | `notes.md` | merge | Same risk as S13; one row kept |
| S6 | README.md › Usage | none | drop | Stays in README.md: how to run it |
| S7 | docs/spec.md › Overview | `product/overview.md` | merge | Same content as S1 |
| S8 | docs/spec.md › Plant requirements | `product/requirements/plants.md` | move | PLT-02 waits on OQ-03 |
| S9 | docs/spec.md › Watering requirements | `product/requirements/watering.md` | convert | W1 to W3 become WAT rows, mapped in id-map |
| S10 | docs/spec.md › Watering day boundary | `decisions/` | convert | See OQ-02 |
| S11 | docs/spec.md › Planned requirements | `research/2026-11-08-sprig-ideas.md` | convert | CAL-01 reserved in id-map, not a row |
| S12 | docs/spec.md › Architecture | `architecture/context.md` | move | Built: the code |
| S13 | docs/spec.md › Decisions | `decisions/` | merge | See OQ-05 |
| S14 | docs/spec.md › Risks | `notes.md` | merge | Same risk as S5 |
| S15 | docs/spec.md › Open questions | `notes.md` | move | OQ-06 |
| S16 | AGENTS.md › Commands | none | drop | Stays with the code in AGENTS.md |
| S17 | AGENTS.md › Conventions | none | drop | Stays with the code in AGENTS.md |
| S18 | AGENTS.md › Documentation rule | none | drop | Stays until OQ-04 is answered |
| X1 | code-only: `remove NAME` deletes a plant | `product/requirements/plants.md` | derive | No source states it; proposed, adopted from the code once confirmed |

## Built rows and their evidence

| Row or section | Source row | Evidence | Vouched by |
|---|---|---|---|
| PLT-01 | S8 | `sprig.py` add | code |
| PLT-03 | S8 | `sprig.py` list | code |
| WAT-01 | S9 | `sprig.py` water | code |

## Decision records

| Record | Title | Status | Options and consequences from |
|---|---|---|---|
| 0004 | Data is one JSON file | proposed | S4, S13 |

## Conflicts and duplicates

| ID | What disagrees | Where | Recommended answer | Decision |
|---|---|---|---|---|
| OQ-01 | README lists email reminders as done; the code has none | S2 | Treat as unbuilt and park it | open |
| OQ-02 | The README says a watering day follows the local date; the spec says midnight UTC | S4, S10 | Local dates: the code uses them | open |
| OQ-03 | The spec says names are case-sensitive; the code is case-insensitive | S8 | Follow the code | open |
| OQ-04 | The AGENTS.md documentation rule contradicts profile rule 9 | S18 | A new record superseding the rule | open |
| OQ-05 | Decisions are numbered D1 to D3 in the README and ADR-1, ADR-2 in the spec | S4, S13 | One log | open |

## Gaps

- no glossary terms in the sources: `structuring-prototype-context`

## History

- 2026-11-08: presented.

## Verification

- Sections mapped: pending
