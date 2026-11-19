# Options study: [subject]

Date: [YYYY-MM-DD] · Kind: options study · Outcome: [waiting for the pick | picked option B on YYYY-MM-DD | settled by decision NNNN]

<!-- Save as studies/[YYYY-MM-DD]-[slug]/README.md in the architecture folder; the slug names the choice in two to four words.
Keep the title and the header line first: the index row is copied from them. Update the Outcome when the person picks, and the index row with it.
The Intake comes directly under the header line: put no option, recommendation or summary above it. Ids: S scenarios, C constraints, F facts, A assumptions, P proposals; options are A, B, C, with A the smallest change. Element ids are the ids of the views.
Each option has one view in this folder, named after the base view it varies, then the option: [view]-[option-slug].md, Status: proposed. All option views are at the same level and start from the same base.
Links to standing views and to the page start with two parent-folder steps, because the study sits two folders below the architecture folder; the source paths after "#compare=" stay relative to the architecture folder.
Write "none" under a heading that has nothing, with what was checked. Delete this comment and every unused placeholder. -->

## Intake

Asked by [person] on [YYYY-MM-DD]: "[their words]"

**The real question.** [One or two sentences, without the solution the person named.]

**Priority scenarios.**

| Id | Source | Stimulus | Environment | Part affected | Response | Measure |
|---|---|---|---|---|---|---|
| S1 | [who or what] | [what happens] | [conditions] | [element ids] | [what the system does] | [number or observable condition] |

Considered, not traced: [scenarios left out, one phrase each, or none].

**Hard constraints.**

- C1: [constraint]. Evidence: [path, stated by, or decision record link].

**Facts.**

- F1: [fact]. Evidence: [`path:line` or stated by].

**Assumptions.**

- A1: [assumption]. Confirmed by: [observation or person].

**Proposals.**

- P1: [the solution the person named, or none]. Source: [the person's words, a document]. It is weighed as one of the options below, or under "Considered and dropped".

**Already decided.**

- [link to a decision record, an accepted study or a standing view]: [what it settles here, or "the decision log is empty"].

## Scope

Views read: [links to the standing views and earlier studies read, or "none: the base is drawn in this study as [view]-current.md"]. Code read at commit [short commit]: [the folders and files the traces crossed, or "no code: the brief at [path]"].

## What is already settled

| Settled by | What it fixes | How the options treat it |
|---|---|---|
| [decision record link, standing view, `path:line`] | [the mechanism, store, limit or boundary it fixes, and the scenario that relies on it] | [every option keeps it \| option C reopens it, because (what changed)] |

[When the record names its own fallback or revisit condition, one sentence: whether it applies now, with evidence.]

## Prior art

- In this repository: [the closest existing mechanism, end to end, with `path`; what it already gives; its limits].
- [Source title]: [address], read [YYYY-MM-DD], version [x]. Claim used: [what it says]. Transfers: [what holds here]. Does not transfer: [scale, team, consistency, region].

[Or: The harness could not search the web; every claim about an outside service or library below is an assumption, and the research is listed under what was not checked.]

## Options

The choice turns on [the axis: where a responsibility lives, how a change travels, who holds the authoritative data, what deploys and fails together, build, run or buy, how we get there].

### A: [name], the smallest change

[Two to four sentences: how it meets the scenarios, by which mechanism, and what changes from today.]

- Changes: [element ids added, changed or removed; or "no element changes: a setting in `path`"].
- Wins when: [the situation in which this is the best choice].
- View: [a relative link to `[view]-[option-slug].md` in this folder]. [A compare link whose target is the page two folders up, then `#compare=[base view].md,studies/[YYYY-MM-DD]-[slug]/[view]-[option-slug].md`, base first.]

### B: [name]

[Same parts as A.]

### C: [name]

[Same parts as A, or delete this section when two options are all the evidence supports.]

### Considered and dropped

- [Option]: [the hard constraint it breaks, or "no situation in which it wins: (reason)"].

## Traces

One ledger per priority scenario whose measure is a time or a count, per option where the options differ; a ledger shared by several options is written once and says so. Every wait has its own row.

### S1 through A

| Step | Element | What happens | Wait or cost, normal | Wait or cost, bad day | Evidence |
|---|---|---|---|---|---|
| 1 | [id: where the source acts] | [what happens] | [number] | [number] | [`path:line` or A id] |
| [n] | [id: where the source observes the response] | [what it shows] | [number] | [number] | [evidence] |
| Sum | | | [sum] against [measure] | [sum] against [measure] | |

## Matrix

One sentence per cell: whether the measure holds, by which mechanism, and on what fact or assumption. A cell for a scenario with a ledger states its sums and takes its verdict from them. No scores.

| Scenario or constraint | A: [name] | B: [name] | C: [name] |
|---|---|---|---|
| S1: [short name] | [sentence (F or A id)] | [sentence] | [sentence] |
| C1: [short name] | [how it stays inside the constraint] | [sentence] | [sentence] |
| To run and change | [what it adds to deploy, watch, upgrade and restore, or "nothing new"] | [sentence] | [sentence] |
| To undo | [easy \| moderate \| hard]: [what undoing takes] | [sentence] | [sentence] |

[Close call: [assumption id] decides between [options]. Or delete this line.]

## Recommendation

[Option], because [the scenario and constraint rows that decide it]. It costs [what it adds to run, and how hard it is to undo]. [Each other option loses because ..., one clause each.]

## What would reverse it

- If [observable condition, with a threshold] ([assumption or scenario id]), [which option wins instead, and why].

## Spike

[Delete this section when no spike is proposed.]

- Question: [the one assumption, by id]
- Decides between: [option ids]
- Setup: [what is built, with which versions, against what load or data]
- Observe: [the measurement]
- Threshold: [value] or better: [option]; worse: [option]
- Timebox: [hours or days]
- Where it runs: [a local copy, a test environment]
- Thrown away afterwards: [what is not kept]
- Result: [not run | YYYY-MM-DD: the raw observation, and what it changed in the recommendation]

## Falsification pass

By: [an independent agent with a fresh context | the author's second read, from the last ledger row backwards]

| Attacked | Result | What changed in this study |
|---|---|---|
| [a verdict, a sum, a default, a measure of zero, an end state or a threshold, by its id or row] | [broke: `path:line`, what follows \| not falsified] | [the verdict or default as it now reads \| nothing] |

Could not be checked without running the system: [list, or "nothing"].

## What was not checked

- [Measures nobody has taken, prior art not searched, costs not priced, code paths not read, migrations not traced, and what would check each.]

## Pick

Waiting: asked [person] on [YYYY-MM-DD]; no choice yet.

<!-- When the person picks, replace the line above with:
Picked: option [B] on [YYYY-MM-DD]. [Person]'s words: "[their words]".
For a combination, add one paragraph restating it, and "Confirmed on [YYYY-MM-DD]: "[their words]"".
For "you choose", write: Picked by delegation: option [B], the recommendation, on [YYYY-MM-DD]. [Person]'s words: "[their words]".
Then add:
Decision record: [offered on YYYY-MM-DD | written as (link to the record) | declined on YYYY-MM-DD].
Standing views: [offered: (views) with the picked option's elements as planned | updated as planned on YYYY-MM-DD | declined | not here: handed to designing-system-architecture].
Leave the rest of the study as it was on its date. -->

## Next

[The skill that fits next and why: while waiting, the person's pick; after a pick, evaluating-architecture-risks for a critical look at the picked option, a decision record, and drawing-architecture-views to draw the standing views as planned; designing-system-architecture when the architecture lives in a product context repository; recovering-built-architecture when the views lacked evidence.]
