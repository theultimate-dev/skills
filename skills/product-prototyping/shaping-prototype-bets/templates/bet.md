# Bet [NN]: [the outcome, in a few words]

Status: shaped
Appetite: [½ day | 1 day | 2 days] · Framing: [research/YYYY-MM-DD-slug.md]
Autonomy: [proposed at shaping; replaced at Gate 1 by the approved line with the person's words]
Context pinned: not yet

<!-- Keep every heading below, in this order. Building and closing read bets by these fields. Delete this comment.
Status: shaped | approved | building | built | kept | removed | stopped. Only this line carries the bet's status; the board copies it.
Appetite: ½ day, 1 day or 2 days of working time, one total ceiling across the bet's whole life, reshapes included. Waits for the person, recorded in the working log, do not count. A raised appetite is a new total in the person's words, never additional time on top. When the work does not fit 2 days, cut scope or split the bet.
Framing: the research note whose verdict is shape.
Autonomy: what the builder may do without asking, in four fields: `code commits: <branch>; context commits: yes | no; push: yes | no; revert on remove: yes | no`. Recommended at Gate 1: the branch the person works on, yes, no, yes, because a removed bet is undone by a revert on that branch. A reshape replaces an approved line with a proposal; the replaced approval stays in the Build log as a dated line.
Context pinned: the full commit SHA the bet was approved at, written when the person approves it at Gate 1.
Read rules: read the shaped fields at Context pinned: every header line except Status and Context pinned, and every section except Build log and Result. Read Status, Context pinned, Build log and Result from the working copy, reporting any uncommitted state. -->

## Outcome

<!-- One observable result a person can try on its own, in two to four sentences: who can now do what, and what they see. No implementation steps. -->

## Requirement deltas

<!-- The requirement rows this bet adds, changes or drops, held here until the bet closes. The catalogue in product/requirements holds only built and dropped rows.
ID: a reserved ID for a new row (the next free number in the capability, not used by any other open bet), or an existing ID for a changed or dropped row.
Change: new | changed | dropped.
Text or reason: the full text of a new row, the new text of a changed row, or the reason a row is dropped. -->

| ID | Change | Text or reason |
|---|---|---|
| [ABC-01] | new | |

## Acceptance checks

<!-- One observable result per line, with concrete values, naming the requirement it proves. Every new or changed requirement has at least one check.
Method: how the builder proves it. test | build | run and observe | inspect output | person's eye. A person's-eye check is listed for the person to judge at Gate 2 and is not a condition for built.
A leading ~ marks a check that may be cut under appetite pressure. -->

- C1 ([ABC-01]): [observable result] · Method: [test]
- ~ C2 ([ABC-01]): [observable result] · Method: [run and observe]

## Boundaries

<!-- No-go: what this bet will not do, even though a reasonable reader might expect it.
Rabbit hole: a known risk that could eat the appetite, with how the shaping patched it, or what to do if it bites.
~ Cuttable: scope that may be dropped first if the appetite runs short. -->

- No-go: 
- Rabbit hole: [risk]. Patched by: [constraint or chosen path] | If it bites: [stop and reshape, or the fallback]
- ~ Cuttable: 

## Keep or remove

<!-- The signal the person will judge at Gate 2 after trying the bet, and what removing it would leave behind: code reverted, requirement rows dropped, planned architecture deleted, anything that stays, such as a note or a decision. -->

- Signal: 
- If removed: 

## Architecture

<!-- Paths are relative to the context folder. A relied-on contract must be accepted before the bet is approved. -->

- Touches: [containers, components or files of the code, with their architecture files | none]
- Introduces: [sections or contracts written at shaping as Status: planned, with their paths | none]
- Relies on: [decisions/NNNN-title.md, architecture/contracts/name.md version X.Y accepted, … | none]

## Context pack

<!-- The files an implementing agent reads, in order, each with why. Short: five to ten entries is a guideline; each entry earns its place. -->

1. [path]: [why]

## Build log

<!-- Written by building-prototype-bets. Leave empty until building starts: the base commit and the consumed working time; every code commit by SHA, oldest first, with any context commit between them named (each code commit belongs to exactly one bet); each check's result and evidence; cuts with reasons; review findings and their fixes; and the Try it block.
Dated lines of the bet's history, kept across reshapes: `Approved YYYY-MM-DD at <sha>: <autonomy line>`, appended by shaping when a reshape replaces an approval, and `Reshaped YYYY-MM-DD: <what changed>`. A reshape keeps the code commits, the base commit and the consumed time. Which commits removal reverts is decided by this list of code commits, never by Status. -->

## Result

<!-- Written by closing-prototype-bets when the person decides at Gate 2. Leave empty until then: kept or removed, the date and the person's words, the lesson. A legacy bet parked at adoption reads "parked at adoption: not tried, see <note>". -->
