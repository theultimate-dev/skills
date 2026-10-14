# Sizing and appetite

How to cut a milestone into bets that an implementation loop can build within a fixed appetite, and what to do when a bet is the wrong size.

## Appetite, not estimate

An estimate asks how long the work will take. An appetite says how much the outcome is worth, and the shaping makes the work fit it. A bet's appetite is set before anyone plans it, and it is a ceiling: when the work outgrows it, the loop stops and the bet is reshaped, rather than extended.

The scale is the implementation loop's own effort scale, so both sides measure the same thing:

| Appetite | Plans in the loop | Typical PR slices | Typical shape |
|---|---|---|---|
| M | One plan with several phases | 2 to 5 | One capability, or one flow end to end through the containers it needs |
| L | Two or three plans | 5 to 12 | A capability that crosses containers, needs a new contract, or starts an empty code repository |

A verification harness plan (Plan 0) does not count; it builds the means to check every later bet. A walking skeleton does count: it is the first bet's real work.

## Find the seams

Cut by outcome. Each bet ends in something a person can see or do, and it goes end to end through whatever containers that takes. A cut by layer, "the database for lists" then "the API for lists", produces bets that cannot be demonstrated or verified on their own.

| Seam | Cut here when |
|---|---|
| A user-visible flow | The flow works from start to finish without the rest of the milestone |
| A capability boundary | Requirements share a prefix and a data shape, and other capabilities only read it |
| A contract | Two parts meet at one interface: the bet that produces it comes first, the bets that consume it follow |
| A design dependency | Requirements with a user interface wait on a design handoff; the rest can go first |
| Risk | One unknown dominates: give it a small bet of its own, early, so the rest is not hostage to it |

Order the slate so the first bet is a thin path through every container the milestone touches, the walking skeleton, when the code repository is empty or the milestone adds a container. Later bets thicken it.

## Size signals

| Signal | Too big: split | Too small: merge |
|---|---|---|
| Requirement IDs | More than about 12 | One or two that make no outcome on their own |
| Acceptance criteria | More than about 15; the interview would not fit one sitting | Fewer than three |
| Contracts | Produces or changes two or more | — |
| Containers | Changes the inside of three or more containers at once | — |
| Outcome sentence | Needs "and" to say what the user gets | Describes a step, not a result |
| Plans | Clearly more than three | Clearly one PR slice |

Split along a seam, keeping the bet that holds the walking path or the produced contract first. Merge a too-small bet into the neighbour that shares its flow or its data.

## The first bet in an empty code repository

Shape it as L. The implementation loop treats a bet with no codebase as a new app: its first plan is a walking skeleton with continuous integration and a verification entry point, and that plan counts against the appetite. Keep the rest of the bet thin: a single path from the outermost container to the innermost, observed end to end.

## Worked slate

Larder, milestone 1.1 Pantry. The milestone targets PAN-01 to PAN-04, PAN-06, PAN-07, SYN-01 (part: pantry items), NFR-02 and NFR-03; PAN-05 was dropped. The code repository already holds the walking skeleton from milestone 1.0.

| Bet | Outcome | Requirements | Appetite | Depends on | Contracts |
|---|---|---|---|---|---|
| 04 Pantry items | A household member adds, edits and removes pantry items in the web app, and they survive a reload | PAN-01, PAN-02, PAN-03, NFR-03 | M | 03 | Consumes `sync-protocol` 1.0 |
| 05 Expiry tracking | Items show their expiry, and items expiring within three days are listed first | PAN-04, PAN-07 | M | 04 | none |
| 06 Pantry sync | Changes on one device appear on another signed into the same household | PAN-06, SYN-01 (part: pantry items), NFR-02 | L | 04 | Changes `sync-protocol` to 1.1: pantry item operations |

Coverage: PAN-01 to PAN-04, PAN-06 and PAN-07 once each; SYN-01's pantry part once, its meal-plan part left to milestone 1.2; NFR-02 and NFR-03 once. Before bet 06 can be ready, `sync-protocol` 1.1 must be accepted, through `designing-system-architecture` when it is installed.
