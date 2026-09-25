<!-- The posted review body, and the local review.md when there is no PR. Keep the verdict line first, and name the full 40-character head SHA in it: the merge gate matches that SHA against the review's pinned `commit_id`. Delete empty sections, unused alternatives and this comment. In review.md, put each round under a "## Round N" heading, append new rounds, and never rewrite an earlier one. -->

**Verdict: [APPROVE | REQUEST CHANGES]** at `[full head SHA]` · round [N][, delta from `[reviewed SHA]`][ · self-review]

[PR #n, or branch vs. base] for [work item], reviewed against [path to spec.md and plan NN, covering ACs …] [or: the stated intent in the linked issue and the PR description, since there is no spec].

[Self-review: [all lenses | the named lenses] ran as sequential passes in the reviewing agent's own context, not as independent reviewers. A self-review verdict makes this PR `human`.]

Category: `[review:agent | review:human]`[; the diff touches [area], so this PR moves to `review:human`]

| Lens | Ran as | Result |
|---|---|---|
| architecture | [parallel agent / headless CLI run / self-review / not rerun, result from round N / intent only: from quick mode at `[sha]`] | [nothing in scope / no findings / F1, F3] |
| security | | |
| conventions | | |
| efficiency | | |
| intent | | |

## Blocking

### F1 · [lens] · `[path:line]` · [confirmed | unconfirmed]

- **Summary:** [one sentence]
- **Trigger:** [input, state or sequence; expected versus actual]
- **Impact:** [who or what is hurt, and how badly]
- **Evidence:** [reproduction, command and output, or quoted code]
- **Basis:** [R or AC ID, rule, decision record, or idiom source]
- **Direction:** [suggested fix]
- **Status:** open since round [N]

## Should-fix

### F2 · [lens] · `[path:line]` · [confirmed | unconfirmed]

[Same fields as above.]

## Nits

Optional; they do not affect the verdict.

- F3 · [lens] · `[path:line]`: [what to change, in one line]

## Unconfirmed questions

An unconfirmed blocking question keeps the verdict at REQUEST CHANGES until a check settles it; the others do not affect the verdict.

- F4 · [lens] · `[path:line]`: [the question, its severity if confirmed, and what would settle it]

## Deferred

| Finding | Issue | Reason |
|---|---|---|
| F5 | [issue link] | [why it falls outside this PR slice] |

## Rechecked this round

| Finding | Status | Evidence at `[head SHA]` |
|---|---|---|
| F1 | [closed / still open / reopened] | [what was read and run] |

## Dropped after checking

- [lens] · `[path:line]`: [the suspicion], dropped because [the counter-evidence]

## Escalation

[Only after round 3 with a blocking finding still open.]

- **Finding:** [ID, summary, evidence]
- **Fix attempts:** [SHA: what it changed, for each attempt]
- **Positions:** [the reviewer's, and the implementer's]
- **Options:** [fix differently / change the spec / waive, which makes the PR `human`]
- **Recommendation:** human review; this PR moves to `review:human`.

---

This is a comment review. The verdict is the reviewing agent's and is not a host approval.
