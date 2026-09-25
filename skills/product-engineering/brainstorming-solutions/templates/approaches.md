# Approaches template

Two parts. The comparison is the G2 message to the user. The Approach section goes into `spec.md` after the user picks. Delete every bracketed placeholder you do not fill.

## The comparison message

```markdown
Approaches for [work item] ([path to spec.md])

Context: [one line: the prior art or constraint that shapes the options. Outside a work item, also the problem and the 2–5 criteria, stated as assumptions]

**A: [short name]**
How it works: [2–4 sentences: where the logic lives, the data flow, what is reused]
Touches: [modules and files]
Reuses: [existing utilities or patterns, with paths]
Best when: [the situation in which this approach wins]

**B: [short name]**
How it works:
Touches:
Reuses:
Best when:

| Approach | Fit with the architecture | Risks | Effort | Reversibility | Meets all ACs |
|---|---|---|---|---|---|
| A | [follows or departs from what, and why] | [top one or two, and what exposes them early] | [S, M, or L] | [easy, moderate, or hard] | [yes, or no: which AC] |
| B | | | | | |

Recommendation: [A], because [reasons tied to the criteria, the constraints, and the code evidence].
I would recommend [B] instead if [condition].

[Spike proposed, when one would settle the pick: the question, the timebox, the observation that answers it, and which answer points to which approach.]

Pick one, combine them, or ask me to dig into one.
```

Scales, identical for every approach:

- Effort: S is one PR slice (the work that becomes one pull request, or merge request), M is one plan with several phases, L is several plans.
- Reversibility: easy means a flag or config change undoes it; moderate means a code change undoes it and no data or contract moves; hard means undoing needs a data migration, a public-contract change, or an external commitment.

## The Approach section in spec.md

```markdown
## Approach

Chosen: [name]. Agreed at G2, [YYYY-MM-DD]: "[the user's words]"

[How it works, in 3–6 sentences: where the logic lives, the data flow, what is reused. Stop at module boundaries and contracts.]

- Touches: [modules and files]
- Reuses: [utilities and patterns, with paths]
- Contracts: [interfaces, data shapes, or events that later work depends on; "none" when nothing crosses a boundary]
- Evidence: [code paths; spike findings with branch and commit; sources with URL, retrieval date, and version]

Rejected alternatives:

- [B]: [one-line reason]
- [C]: [one-line reason]

Consequences:

- [What becomes easier or harder]
- [A risk to watch, and what exposes it early]
- Revisit if: [the condition that would reopen this choice]
- Decision record: [path, or "none: not consequential"]
```

When the user delegated the choice, the agreement line reads: `Chosen: [name]. Chosen by delegation at G2, [YYYY-MM-DD]: "[the user's words]"`. When the request named the approach, it reads: `Chosen: [name]. Named in the request, [YYYY-MM-DD]: "[the user's words]"`, and G2 only checks it against the ACs. When only one approach was sensible, the rejected alternatives list each discarded idea with the constraint or criterion that ruled it out.
