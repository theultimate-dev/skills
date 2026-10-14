---
name: curating-product-requirements
description: "Maintains the product layer of a product context repository: overview, glossary, actors and use cases, and a requirement catalogue with permanent capability-prefixed IDs, priorities, target versions and statuses, plus non-functional requirements with stated targets. Integrates product briefs, product/design handoffs and feedback without duplicates, maps their local IDs to catalogue IDs, and drops or defers rows with a reason, never deletes. Use when the user says add this to the requirement catalogue, fold this brief or handoff into the catalogue, what does PAN-03 mean, drop or defer a requirement, add a use case or an NFR target, clean up the requirements, or update the glossary. Not for shaping a rough idea (shaping-product-briefs), one work item's spec (specifying-work-items), or moving requirements between versions (planning-product-roadmaps)."
license: MIT
---

# Curating product requirements

Keep the product layer of a product context repository true and small: why the product exists, the words it uses, who uses it, and what it must do. The catalogue outlives every version and every bet, so its IDs never change, its rows never disappear, and each fact lives in one place. This skill integrates and maintains; it does not invent the product. A rough idea goes to `shaping-product-briefs` first, and its brief comes back here.

The repository's layout, ID formats and statuses are fixed by its `AGENTS.md` and `product/requirements/README.md`. Read both first and follow them; where they are silent, use the conventions below. When there is no product context repository yet, create or adopt one with `structuring-product-context` when it is installed; otherwise ask the user where the product layer should live.

## What this skill owns

| File | Holds | Changes when |
|---|---|---|
| `product/overview.md` | Vision, who it is for, principles that hold across versions, assumptions and constraints, what the product is not | Rarely, and only with the user's words |
| `product/glossary.md` | The product's terms, one meaning each, and the aliases to avoid | A requirement, use case or architecture file needs a term that is not defined |
| `product/actors-and-use-cases.md` | Actors, and use cases `UC-NN` with their primary actor and target version | A new actor or use case |
| `product/requirements/<capability>.md` | One capability's functional requirements `<CAP>-NN`: statement, priority, target version, status, notes | A requirement is added, clarified, retargeted, built, deferred or dropped |
| `product/requirements/non-functional.md` | `NFR-NN` by area, with targets only where the user stated or accepted them | A quality target is stated, confirmed or changed |
| `product/requirements/id-map.md` | Local IDs from briefs and handoffs mapped to catalogue IDs; append-only | An input with its own IDs is integrated |
| `product/requirements/README.md` | The derived index: capability files, prefixes, counts by status and version | Rebuilt after every change to the catalogue, never edited by hand |
| `product/platforms.md`, `product/business.md` (optional) | What each surface does; ownership, licence, costs and pricing | Only with the user's words |

Version targets are set here only when the user states them while adding a requirement. Moving a requirement to another version belongs to `planning-product-roadmaps`, which also owns the risk and open-question registers. Rationale belongs in a decision record or the overview, never in a requirement row.

## Scale by request

| Request | Do |
|---|---|
| "Add this requirement" with clear text | Check for duplicates and conflicts, assign the ID, write the row, rebuild the index, report. No interview |
| Fold in a brief or a product/design handoff | The full procedure below; one confirmation of the integration summary |
| Integrate feedback or a bug report that implies new behaviour | Classify first: most feedback is a defect against an existing requirement, a question, or a design detail, not a new requirement |
| A rule promoted back from a closed bet | Fold a clarification into the existing row's text with a note; give added behaviour a new ID with status `built` |
| "What does PAN-03 mean?" | Read the row, its notes, the glossary terms it uses, the decisions it cites and the bets that cover it; answer in a few lines. Change nothing |
| Clean up the catalogue | Run the consistency checks in the [catalogue reference](references/requirement-catalogue.md#consistency-checks); propose every change in one summary; write on a yes |
| Update the glossary, actors or overview | Edit the one file; check that the requirements still read correctly with the changed term |
| The first catalogue of a new product | Start from the [templates](#references); one file per capability the user names; leave Version empty until the roadmap exists |

## Procedure

1. **Read the layer before the input.** Read `AGENTS.md`, `product/overview.md`, `product/glossary.md`, `product/requirements/README.md`, `product/requirements/id-map.md`, the capability files the input touches, and `decisions/README.md`. Then read the input in full. Never ask what the catalogue or the decision log already answers.
2. **Classify every incoming item** by the table in [integrating inputs](references/integrating-inputs.md#classify-each-item): functional requirement, non-functional requirement, constraint or assumption, design detail, implementation choice, open question, or a duplicate of something already here. Only the first two become catalogue rows.
3. **Match each requirement against the catalogue.**
   - Same behaviour as an existing row: reuse its ID and record the mapping. Change the existing text only to make it clearer, and only when the meaning stays the same.
   - Overlap: merge into one row or split into rows that do not overlap. Never leave two rows that a single bet would have to deliver together to make sense.
   - Contradiction with a row, the overview's principles or an accepted decision: ask, with a recommended default. Never let the newer input win silently.
   - New behaviour for a `built` requirement: a new row that names the one it extends in Notes. A built row keeps describing what shipped.
4. **Assign IDs.** Use the capability's prefix and the next number after the highest ever used in that file, dropped rows included. A requirement that fits no capability starts a new capability file; propose its name and prefix and get a yes. Never reuse, renumber or recycle an ID.
5. **Draft the rows** in the [row format](references/requirement-catalogue.md#row-format): one capability or rule per row, from the user's or caller's side, observable, free of components and technologies. Priority comes from the input or the user. Version only when the user states it. Status `planned`. Nothing is written yet.
6. **Keep the language consistent.** Every term a new row needs is in the glossary with one meaning; add missing terms, and replace aliases the glossary marks to avoid.
7. **Plan where each non-requirement goes**, without writing it yet. Open questions go to the open-question register, constraints and assumptions to the overview, and design details stay with their design files. Implementation choices go through `designing-system-architecture` when it is installed; a decision record written for one is `proposed` unless the user made the choice. A defect against an existing requirement changes nothing here: name the requirement ID so the defect goes to the code repository's tracker.
8. **Confirm.** Present a summary of at most 10 lines: rows added, rows clarified, rows dropped or deferred, IDs mapped, conflicts and how they were resolved, questions raised, and anything left out with where it will go. Write on an explicit yes. A single row the user dictated needs no confirmation; report it.
9. **Write, map and rebuild.** Write the rows, file each non-requirement item in the home step 7 planned for it, append the ID mappings to `id-map.md` with the date, and rebuild `product/requirements/README.md` from the capability files.

## Rules that keep the catalogue usable

- **IDs are permanent.** A dropped requirement stays in its table with status `dropped`, the date and the reason. A deferred one keeps its row with status `deferred` and no Version.
- **One home per fact.** A row states what, never why. The why is a decision record or a line in the overview, and the row links to it in Notes.
- **No implementation in requirements.** "The pantry list updates on every device within 5 seconds" is a requirement; "sync pushes changes over a WebSocket" is architecture.
- **Targets are never invented.** A non-functional requirement without a number the user stated or accepted gets the target "to confirm" and an open question.
- **No links to the roadmap.** Requirements never link to bets or milestones; the roadmap points at requirements. Version is a target, not a link. A plain-text ID in Notes, such as `OQ-06` or "rule from Bet 05, AC-E2", records provenance and is allowed; a link to a roadmap file never is.
- **Acceptance criteria live in bets.** Do not write criteria into the catalogue. A rule proven in a bet comes back only through promotion.

Read the [catalogue reference](references/requirement-catalogue.md) for good and bad rows, EARS phrasing, priorities, non-functional areas and the consistency checks.

## Ask good questions

Ask only what changes the catalogue: whether two items are the same requirement, which of two contradicting statements holds, a missing priority for a Must candidate, a target for a quality requirement. Ask in rounds of at most four, each with the evidence and a recommended default:

```text
The handoff's R2 ("show items about to expire") overlaps PAN-04 ("warn about items
expiring within a set number of days"), status built in V1.
Recommended: a, because R2 adds a sorted view, not a new warning.
  a) Keep PAN-04 as is; add PAN-07 "List pantry items by expiry date" (recommended)
  b) Map R2 to PAN-04 and drop the sorted view
  c) Map R2 to PAN-04 and ask for a separate design decision on the view
```

When the user says "you decide", take the recommended default and list it in the summary as decided by delegation.

## When a sibling skill is missing

Say in one line which skill is missing, then produce its essential outcome yourself.

| Missing | Essential outcome |
|---|---|
| `shaping-product-briefs` | For a rough idea: audience, problem, intended outcome, in scope and out, in a few lines confirmed by the user, then integrate those as the input |
| `planning-product-roadmaps` | Append open questions to `roadmap/open-questions.md` in its existing format with the next `OQ-NN`; leave Version empty unless the user states it |
| `decision-records` | Write a short record in the repository's `decisions/` format: status (`proposed` unless the user made the choice), date, context, options, decision, consequences; add its index row |
| `designing-system-architecture` | Record the implementation choice as an open question in the register, naming the choice; or, when `decision-records` is available, as a `proposed` decision record |

## Hand back

Report the files changed, the rows added, clarified, deferred and dropped with their IDs, the mappings appended, the terms added to the glossary, the questions raised and where they were filed, and anything the input held that is not in the catalogue, with where it went. Name the next step when there is one: version targets with `planning-product-roadmaps`, or a bet with `shaping-bets`. Without file access, return the changed rows and files as complete Markdown and say that nothing was written.

## References

| Read | When |
|---|---|
| [requirement catalogue](references/requirement-catalogue.md) | Writing or reviewing rows: format, good and bad examples, EARS, priorities, statuses, non-functional areas, changing built requirements, consistency checks |
| [integrating inputs](references/integrating-inputs.md) | Folding in a brief, a handoff, feedback or a promoted rule: classification, the ID map, duplicates and conflicts, a worked example |
| [overview template](templates/overview.md) | Writing `product/overview.md` |
| [glossary template](templates/glossary.md) | Writing `product/glossary.md` |
| [actors and use cases template](templates/actors-and-use-cases.md) | Writing `product/actors-and-use-cases.md` |
| [capability requirements template](templates/capability-requirements.md) | Starting a capability file |
| [non-functional template](templates/non-functional.md) | Starting `product/requirements/non-functional.md` |
| [requirements index template](templates/requirements-index.md) | Rebuilding `product/requirements/README.md` |
