# Registers

A product keeps one risk register and one open-question register, both in `roadmap/`. Every other file cites register IDs instead of keeping its own list: a version brief lists the IDs that bear on it, a bet lists the IDs that bear on the bet. That keeps each risk and question in one place, where its status can be trusted.

## Risks: `roadmap/risks.md`

| Field | Write |
|---|---|
| ID | `RSK-NN`, the next number ever used; never reused |
| Risk | What could go wrong, in one sentence |
| Why it matters | The consequence for users or the product, not a severity score |
| Mitigation | What reduces it, and where that lives: a requirement, a decision, a bet, a test |
| Versions | The versions it affects: `V1`, `V1–V2` |
| Owner | The bet that mitigates it (`Bet 03`), or a person |
| Status | `open` or `closed`, with the date and why when closed |

Example:

| ID | Risk | Why it matters | Mitigation | Versions | Owner | Status |
|---|---|---|---|---|---|---|
| RSK-02 | Two devices edit the same list offline and one edit is lost | A household stops trusting the list | Last-writer-wins per item with an edit log (decision 0006); conflict test in CI | V1–V2 | Bet 02 | open |
| RSK-05 | The sync service's free hosting tier sleeps after inactivity | First sync of the day is slow | Keep-alive ping; revisit with paid tier | V1 | owner of the product | closed (2026-11-20: paid tier from 1.1) |

Close a risk only when its mitigation is in place and observed, or when the thing it guards no longer exists. Never delete a closed row.

## Open questions: `roadmap/open-questions.md`

| Field | Write |
|---|---|
| ID | `OQ-NN`, the next number ever used; never reused |
| Question | One question, answerable by the user or by a check |
| Blocks | What cannot proceed until it is answered: a milestone, a bet, a decision, a prerequisite |
| Recommended answer | Your recommendation and its reason, so the user can answer with one word |
| Owner | Who answers: the user, a named person, or a spike |
| Status | `open`, or `resolved (YYYY-MM-DD)` with a link to the file or decision that holds the answer |

Example:

| ID | Question | Blocks | Recommended answer | Owner | Status |
|---|---|---|---|---|---|
| OQ-03 | Does a list belong to a person or to a household? | V1 data model, contract `sync-protocol` | To a household from V1, so V2 needs no migration | the user | resolved (2026-10-30): `decisions/0005-lists-belong-to-households.md` |
| OQ-07 | Must meal plans work offline? | Bet 05 | No in V1; the pantry list is enough offline | the user | open |

## Rules

- **One question per row.** A row that asks two things gets split.
- **Ask from the register.** When a question blocks the milestone in focus, ask it with its recommended answer. Record the user's words in the resolved row.
- **Resolve into the right home.** The answer is written where it belongs (a requirement, an architecture section, a version brief), and the register links to it. An answer that settles structure, technology, a boundary or a trade-off becomes a decision record: use `decision-records` when it is installed, otherwise write a short record in the repository's `decisions/` convention and add its index row. Link the record from the resolved row.
- **Merge duplicates.** When two rows ask the same question or describe the same risk, keep the lower ID, move anything the other adds into it, and set the other to `closed` or `resolved` with "merged into RSK-NN" or "merged into OQ-NN". Never renumber.
- **Imported documents.** When `structuring-product-context` adopts documents that each kept their own risks and questions, the same item often appears in several of them. Merge them here once, and list the source sections in the row's notes.
- **Who writes.** Any skill may add a row; this skill owns the format, merges duplicates, and closes or resolves rows with the user.
- **Never a backlog.** A register holds risks and questions, not tasks or ideas. Ideas go to the Parked list in `roadmap/README.md`; work goes to bets.
