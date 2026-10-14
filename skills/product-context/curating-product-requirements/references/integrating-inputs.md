# Integrating inputs

How a brief, a product/design handoff, feedback or a promoted rule becomes part of the catalogue without duplicates, lost decisions or broken IDs.

## Inputs and what they bring

| Input | Usually from | Brings | Watch for |
|---|---|---|---|
| Product brief | `shaping-product-briefs` | Audience, outcome, scope, prioritized requirements with local IDs `R1…`, acceptance examples | Local IDs; acceptance examples are not catalogue content, they inform the bets |
| Product/design handoff | `preparing-implementation-handoffs`, or `guiding-product-discovery` | Agreed behaviour with local IDs, traceability to flows and prototypes, suggested delivery slices | Design details and slices that look like requirements; slices go to `shaping-bets`, details stay in `design/` |
| Feedback or a bug report | Users, reviews, support | Observed problems and wishes | Most of it is a defect against an existing requirement or a question, not a new requirement |
| A rule promoted from a closed bet | `reconciling-product-context` | A durable rule or an engineering criterion (`AC-En`) worth keeping, with the bet and criterion it came from | Promotion clarifies what shipped; it never introduces planned work |
| An adopted document | `structuring-product-context`, during adoption | Existing requirement tables, sometimes with IDs already | Keep an existing ID when it is unique and fits the catalogue's scheme; give any other a catalogue ID and record the pair in `id-map.md` |

Accepted upstream decisions carry forward. A requirement the user already agreed in a brief or handoff is integrated as agreed; ask only where it conflicts with the catalogue or a decision.

## Classify each item

| The item | Becomes |
|---|---|
| A capability someone uses, observable from outside | A functional requirement in its capability file |
| A quality of the whole product or a part, with or without a number | A non-functional requirement; target "to confirm" without a stated number |
| A limit the product must live within: platform, law, budget, policy | A constraint in `product/overview.md` |
| A belief the plan depends on | An assumption in `product/overview.md`, with what changes if it is wrong |
| A visual or interaction detail | Stays in `design/<initiative>/`; the bet that builds it lists that file in its context pack |
| How to build it | A decision record or an architecture note, through `designing-system-architecture` when it is installed; a record is `proposed` unless the user made the choice |
| A defect against an existing requirement | No catalogue change; report the requirement ID so the defect goes to the code repository's tracker |
| Something nobody has decided | An open question in the register |
| A suggested delivery slice | Input for `shaping-bets`; not a requirement |
| Already in the catalogue | A mapping to the existing ID |

## The ID map

Inputs with their own IDs keep them in their own files. The catalogue records the mapping once, in `product/requirements/id-map.md`. The file is append-only: a row is never edited, a correction is a new row.

```markdown
# Requirement ID map

Local IDs from briefs and handoffs, mapped to catalogue IDs. Append-only.

| Date | Input | Local ID | Catalogue ID | How |
|---|---|---|---|---|
| 2026-11-02 | design/expiry-view/handoff.md | R1 | PAN-07 | new |
| 2026-11-02 | design/expiry-view/handoff.md | R2 | PAN-04 | same behaviour |
| 2026-11-02 | design/expiry-view/handoff.md | R3 | PAN-08, PAN-09 | split |
| 2026-11-02 | design/expiry-view/handoff.md | R4 | none | design detail, stays in the handoff |
```

`How` is one of: `new`, `same behaviour`, `clarifies`, `split`, `merged`, or `none` with where the item went instead. A bet that uses design files reads this map to translate their local IDs.

## Duplicates and conflicts

Look for duplicates by behaviour, not by words: search the capability files for the nouns and verbs of the item, and the glossary for its terms and their aliases.

| Finding | Recommended default |
|---|---|
| Same behaviour, different words | Map to the existing ID; keep the clearer wording if the meaning is identical |
| Same behaviour, broader | A new row for the extra part, noted "extends …"; never widen a `built` row |
| Partly overlapping | Split so each row stands alone; ask when the split is not obvious |
| Contradicts a `planned` row | Ask which holds; the losing row is edited or dropped with the reason |
| Contradicts a `built` row | A new row that changes the behaviour; the built row stays until the new one ships |
| Contradicts an accepted decision | Ask; changing the decision is a new record that supersedes it, never an edit |
| Contradicts a principle in the overview | Ask; the principle wins by default |

## Worked example

Larder's catalogue has PAN-01 to PAN-06; PAN-04, "Warn the household about items expiring within a number of days they choose", is `built` in V1. A handoff for an expiry view arrives with four local requirements:

- R1 "Show pantry items sorted by expiry date"
- R2 "Warn before items expire"
- R3 "Let a member mark an item as used up or thrown away, and keep a waste count per month"
- R4 "Expired items show a red badge"

1. **Read**: the pantry file, the glossary ("item", "pantry", "household", "member"; "product" marked to avoid), the ID map, decision 0004 ("household data stays within the household").
2. **Classify**: R1, R2 and R3 are functional; R4 is a design detail.
3. **Match**: R2 is PAN-04's behaviour. R1 is new. R3 holds two capabilities.
4. **Ask** one question, because R3's waste count could be read as analytics leaving the household, which decision 0004 forbids:

   ```text
   R3's waste count per month: is it shown only inside the household?
   Recommended: a, because decision 0004 keeps household data within the household.
     a) Shown to the household only (recommended)
     b) Also reported to Larder in aggregate; this needs a new decision superseding 0004
   ```

5. **Write** after the user answers "a":

   | ID | Requirement | Priority | Version | Status | Notes |
   |---|---|---|---|---|---|
   | PAN-07 | List pantry items by expiry date | Should | | planned | |
   | PAN-08 | Mark a pantry item as used up or thrown away | Should | | planned | |
   | PAN-09 | Show the household how many items it threw away each month | Could | | planned | Visible to the household only, decision 0004 |

6. **Map**: R1 → PAN-07 new; R2 → PAN-04 same behaviour; R3 → PAN-08, PAN-09 split; R4 → none, design detail.
7. **Report**: three rows added with no Version, because the user stated none; the version targets are next, with `planning-product-roadmaps`.

## Promoted rules

`reconciling-product-context` sends rules from a closed bet that are worth keeping, such as `AC-E2 (SHO-02): adding an item already on the list increases its quantity instead of adding a second line`.

- When the rule clarifies what the requirement already meant, fold it into the text and note "rule from Bet 05, AC-E2" in plain text, never as a link.
- When it adds behaviour the requirement did not cover, add a row with status `built`, the version that shipped it, and the same note.
- When it is a design or engineering detail with no product meaning, leave it out and say so; it lives in the code repository.
