# Bet [NN]: [the outcome, in a few words]

Status: shaped
Version: [V1] · Milestone: [1.2 Name] · Appetite: [M | L] · Depends on: [Bet NN, Bet NN | none]
Code repository: [name or URL of the repository that builds it] · Context pinned: not yet

<!-- Keep every heading below, in this order. Implementation loops read bets by these fields.
Status: shaped | ready | in delivery | built | done | dropped. Only this line carries the bet's status; the bet board copies it.
Appetite: M is one plan with several phases, L is two or three plans. Plan 0 (a verification harness) does not count; a walking skeleton does.
Depends on: bets by number; Bet 03 is the file roadmap/v*/bets/03-*.md.
Context pinned: the full commit SHA of this repository at handoff, written by shaping-bets.
Implementation loops read the bet's own fields at the pin: every header line except Status and Context pinned, and every section except Handoff and Outcome log. They read Status, Context pinned, Handoff and Outcome log at the latest commit. Delete this comment. -->

## Outcome

<!-- One observable result a person can demo on its own, in two to four sentences: who can now do what, and what they see. No implementation steps. -->

## Requirements

<!-- The catalogue IDs this bet delivers. The text stays in product/requirements; never copy it here.
Covered: "all", or "part: [which part]" when another bet delivers the rest. -->

| ID | Covered | Notes |
|---|---|---|
| [ABC-01] | all | |

## Acceptance criteria

<!-- One observable outcome per line, with concrete values, naming the requirement it proves. Given/When/Then when order matters.
Every requirement has at least one criterion. A leading ~ marks a criterion that may be cut under appetite pressure. -->

- AC1 ([ABC-01]): 
- ~ AC2 ([ABC-01]): 

## Boundaries

<!-- No-go: what this bet will not do, even though a reasonable reader might expect it.
Rabbit hole: a known risk that could eat the appetite, with how the shaping patched it, or what to do if it bites.
~ Cuttable: scope that may be dropped first if the appetite runs short. -->

- No-go: 
- Rabbit hole: [risk]. Patched by: [constraint or chosen path] | If it bites: [stop and reshape, or the fallback]
- ~ Cuttable: 

## Architecture

<!-- Paths are relative to this repository. A consumed contract must be accepted before the bet is ready. -->

- Touches: [containers or components, with their architecture files]
- Consumes: [architecture/contracts/name.md, version X.Y, accepted | none]
- Produces or changes: [contract and what this bet fixes about it; details it leaves open are settled by the implementation loop and written back at close | none]
- Relies on: [decisions/NNNN-title.md, … | none]

## Risks and open questions

<!-- Register IDs from roadmap/risks.md and roadmap/open-questions.md that bear on this bet, one line each on why. -->

- 

## Context pack

<!-- The files an implementing agent reads, in order, each with why. Short: usually five to ten entries. -->

1. [path]: [why]

## Handoff

<!-- Written by shaping-bets when the bet becomes ready. Leave empty until then. -->

## Outcome log

<!-- Written by reconciling-product-context when the bet closes. Leave empty until then. -->
