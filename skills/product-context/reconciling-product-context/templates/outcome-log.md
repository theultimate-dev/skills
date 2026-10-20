<!-- Paste this under the bet's "## Outcome log" heading and fill every [bracket]. Evidence names a pull request and a short SHA, never a claim without a source. Code-repository files are named by repository and path, never by a local checkout path. Delete sections that do not apply and this comment. -->

Closed: [YYYY-MM-DD] · Result: [built | partial | stopped | dropped] · Status set: [done | built | dropped | unchanged]
Work item: [code repository name]: `docs/product-engineering/[slug]/` · Pins: `[short sha]` [at handoff | pinned by the loop at intake | pasted, not checked against the pin][, `[short sha]` re-pinned [YYYY-MM-DD]: "[user's words]"]
Appetite: [M | L] ([N] plans) · Used: [N] plans, [N] pull requests[ · Raised in the bet [YYYY-MM-DD]: "[user's words]"][ · Extended in the loop [YYYY-MM-DD]: "[user's words]"]
Not checked: [sources that could not be read, and why | none]

### Shipped

| Pull request | Slice | Merged | Criteria observed |
|---|---|---|---|
| #[NN], [pull request URL] | [01-p1] | [YYYY-MM-DD] at `[short sha]` | [AC1, AC2] |

### Acceptance criteria

| Criterion | Result | Evidence |
|---|---|---|
| AC1 ([ABC-01]) | pass | [#NN] at `[short sha]` |
| ~ AC2 ([ABC-02]) | cut | `spec.md`: cut ([YYYY-MM-DD]: "[user's words]") |
| AC-E1 ([ABC-01]) | pass | [#NN] at `[short sha]` · [promoted into ABC-01 | not promoted: implementation detail] |
| AC3 ([ABC-03]) | not observed | [no pass on a merged head; what would close it] |

### Requirements

| ID | Status now | Note |
|---|---|---|
| [ABC-01] | built | |
| [ABC-02] | planned | [part cut in this bet: what is left] |

### Architecture and contracts

- `[architecture/path.md#section]`: planned → built
- `[architecture/contracts/name.md]`: version [X.Y] → [X.Y+1 | X+1.0], [what was settled], from `[repository]: decisions/NNNN-title.md`
- Divergence: [what was built differs from the architecture, how it was resolved, the user's words | none]

### Decisions in the code repository

- `[repository]: decisions/NNNN-title.md`: [implementation, internal | moved the architecture: linked from `[architecture path]`[, adopted by `decisions/NNNN-title.md`]]

### Cut, partial and deferred

- [What was not delivered, why, with the user's words, and where it went: a later bet, a planned requirement, dropped]

### Failed approaches worth remembering

- [What was tried and abandoned, why, and where it is recorded: [plan Notes | decision record | pull request]]

### Follow-ups

- [Issues opened by the loop, registers changed (RSK-NN closed, OQ-NN resolved), questions for the next bet]
