# Spec: [work item]

Status: draft
Track: [bugfix | small change | feature | new app | refactor]
Source: [issue ID and link, product brief, or handoff path; "user request, YYYY-MM-DD" when there is none]

<!-- Keep every heading below, in this order. Status stays draft until the user explicitly confirms the spec; at G1 write: Status: agreed (G1, YYYY-MM-DD: "<user's words>").
A bugfix whose repro reproduced skips G1: Status: agreed (G1 skipped: repro reproduced at <short-sha>). -->

## Problem

<!-- Who has the problem, what happens today (with code paths), and the outcome that makes this worth doing.
Bugfix: repro steps, expected vs. actual, blast radius.
Refactor: why the structure must change. -->

## Requirements

<!-- One capability or rule per line, from the user's or caller's side, never a component.
Keep upstream IDs exactly; number new ones after the highest upstream ID.
Refactor: each invariant is a requirement. -->

- R1: 

## Acceptance criteria

<!-- One observable outcome per line, with concrete values, naming the R it proves. Given/When/Then when order matters.
Every R has at least one AC. Every decided error or edge behavior has an AC.
Bugfix: AC1 is "following the repro steps gives the expected result". -->

- AC1 (R1): 

## Non-goals

<!-- What a reasonable reader would expect that this work item will not do, including what is deferred. -->

- 

## Constraints

<!-- Facts that bound the solution, each with its source: code (path), the user, or a policy.
A non-functional that bounds the solution but has no check of its own goes here; one the user wants checked is a requirement with an AC.
End with what "done" means to the user and what they will review themselves. -->

- 
- Done and review: 

## Assumptions and open questions

<!-- Assumption: [statement]. Basis: [accepted default | delegated by the user | inferred from code at path | not asked: low impact]. If wrong: [what changes].
Open: [question]. Blocks: [what it blocks]. Owner: [who answers].
A high-impact open question blocks G1 unless the user accepts an assumption in its place. -->

- Assumption: 

## Approach

<!-- Written at G2 by brainstorming-solutions. Leave empty at G1. -->

## Verification

<!-- Written at G3 by defining-verification: one row per AC with the columns AC, Check, Layer, Tool, Steps, Pass condition. Leave empty at G1. -->

## Plan

<!-- Small-change track: the inline plan and its autonomy contract, with every field of the roadmap's contract, written at G4 by planning-implementation.
Bugfix with one PR slice: keep this heading with only the autonomy contract from the intake answer, every field of the roadmap's contract, "not authorized" for each one unanswered.
Delete this heading on every other track. -->
