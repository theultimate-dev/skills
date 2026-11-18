---
name: exploring-architecture-options
description: "Explores the options for a system-level architecture choice and writes an options study in the architecture folder (context/architecture/ by default): studies/YYYY-MM-DD-slug/README.md from templates/options.md, with the shared intake, what the code and decision log already settle, two or three options that differ in kind, each a proposed view at one level with shared element ids, one of them the smallest change, a matrix against scenarios and constraints with a sentence per cell and no score, a recommendation, what would reverse it, and what was not checked. Derives the options from the priority scenarios, traces the same scenarios through each, and records the person's pick with its date. Use when the user says what are our options, should this be one service or several, which store should we use, events or direct calls, we are starting this from nothing, or compare architectures for X. Not for choosing how to build one work item (brainstorming-solutions), or a prototype idea (framing-prototype-ideas)."
license: MIT
---

# Exploring architecture options

An options study answers "what are our options?" for a choice about the system as a whole: a new system, a boundary between applications, a store, synchronous calls or events, one deployable or several. It lays two or three real alternatives side by side, traces the same scenarios through each, recommends one, and leaves the choice to the person. The result is one dated study beside the standing views. It changes no standing view, and it ends at a gate: the person picks.

A comparison is only worth reading when it could have come out another way. So the options come from the scenarios and constraints, not from a catalogue of patterns; one of them is always the smallest change that could work; and the recommendation says what would make it wrong. Say what the evidence says, including when it is uncomfortable: the smallest change may win over the design the person hoped for, a decision on record may already settle the question, two options may be too close to call without a short test, or the choice may not be architectural at all.

## Where the work lives

[The view conventions](references/view-conventions.md) give the location rule, the folder tree, the view format, statuses, element ids, evidence, the Mermaid subset and quoting, and the link forms, including the compare link. Read them before you write. An options study is a study: `studies/YYYY-MM-DD-<slug>/README.md` in the architecture folder, with `Kind: options study` in its header line, and one `proposed` view per option beside it, named after the standing view it varies, then the option: `containers-search-engine.md`.

The study reads the standing views and the decision log and edits neither, because a standing view shows what is built or agreed, and an option is neither until the person picks it. The one shared file it changes is the index `README.md`, which gains the study's row in its Studies table. Ids that only the options use stay out of the index's element ids table until a pick turns them into planned elements.

## Situations

| Situation | What to do |
|---|---|
| An existing system with standing views | All the steps below. Each option is drawn as a variant of the standing view at the level where the options differ |
| An existing system with no views, or views with little evidence | Read the code the choice crosses and draw the current state you need inside the study as `<view>-current.md`, with evidence, as the base the options vary. List what you could not evidence under what was not checked, and name `recovering-built-architecture` in the report |
| A new system with no code | Work from the brief and the person's answers: facts cite the brief's path or `stated by`. The smallest change is the fewest deployables, stores and technologies that could meet the scenarios. There is no standing view, so each option's view stands alone and compare links put two options side by side |
| The decision log already settles the question | Say so at step 3, link the record, and stop with a short study whose Outcome is `settled by <record>`. Reopen nothing on your own; when the evidence says the record's context has changed, say what changed and leave reopening it to the person |
| Only one option survives the hard constraints | Say so, keep the smallest change as the comparison when it is viable, and never invent an option to fill the table |
| A prototype context (`context/AGENTS.md`) | Follow its map: its `architecture/` is the architecture folder, the study goes in `architecture/studies/`, and its index lists the study as its rules allow |
| The architecture lives in a separate product context repository | Write no standing view there and make no change to it: write the study in the code repository's architecture folder by the location rule, and hand it over as input to `designing-system-architecture`, which owns that repository's views and decisions |

## Steps

1. **Read first.** Open the repository's `AGENTS.md` (or `CLAUDE.md`), the decision log's index and every record that touches the choice, the architecture index, the standing views the choice crosses, and earlier studies of the same subject. Then read the code and configuration the choice crosses: entry points, the modules on the path, deployment files, schema, and the constants that set limits. Note the element ids in use.
2. **Run the intake.** Follow [the scenario intake](references/scenario-intake.md): the real question restated without the solution the person named, three to five priority scenarios with all six fields and a measure, hard constraints, facts apart from assumptions and proposals, and what is already decided. Include the scenario the new need creates, and at least one failure scenario. Ask the person only what the repository and the brief cannot answer, in one message, each question with the default you will use; with no answer, carry on with the defaults as assumptions. Write the intake at the top of the study, under the title and the header line, before any option.
3. **Check what is already settled.** List what the decision log, the standing views and the code already fix for this choice: an accepted record, a mechanism a promise depends on, a limit a scenario relies on. Every option works inside them. An option that would reopen a decision is labelled as doing so, names the record, and shows why the record's context no longer holds; when a record names its own fallback or revisit condition, check whether it now applies. Leave reopening to the person, because a decision record is theirs. When the index, a standing view or an earlier study disagrees with the code or the decision log, say so in the study and in your report, with both paths, and leave the file as it is.
4. **Research prior art.** Look first at the repository: the closest mechanism it already has, which is often the base of the smallest change. Where the harness can search the web, read dated official documentation for the versions in use and a first-party account of the same mechanism in production, and record each source with its address, the date read, the version, and what transfers to this system and what does not. Where it cannot search, say so in the study, and treat claims about outside services as assumptions. [Prior art](references/designing-from-drivers.md#prior-art) gives the procedure.
5. **Sketch two or three options that differ in kind.** Derive them from the scenarios and constraints as [designing from drivers](references/designing-from-drivers.md) describes: find the axis on which the choice turns, and vary the mechanism along it, not the brand or the detail. Option A is always the smallest change that could work. Drop an option that breaks a hard constraint, and any option for which you cannot name the situation it wins in; list both under "Considered and dropped" with the reason.
6. **Draw each option as a `proposed` view.** One view per option, all at the same level (the level where they differ, usually containers), from [the view template](templates/view.md). Start each from the same base view; an element that appears in several options keeps its id in all of them, and a new element gets a new id, the same one wherever it is the same element. Mark new and changed elements `proposed` with the `proposed` class and dotted arrows; unchanged built elements keep `built`. Link each from the study with a compare link against the base view.
7. **Trace the same scenarios through each option.** Follow each scenario through each option's view, element by element, as [tracing an option](references/designing-from-drivers.md#tracing-the-scenarios-through-each-option) describes: which mechanism carries it, what changes from today, whether the measure holds, and on what evidence or assumption. Write a trace ledger for each scenario with a time or a count as its measure, one per option where the options differ, as the intake's "The trace ledger" describes, and keep the ledgers in the study's Traces section. Trace to the response as the scenario's source observes it, the screen or the caller included, and compare the mechanism's own numbers with the measure, as the intake's "When a scenario counts as met" describes: an option whose trace stops one element short, or whose timing exceeds the measure, is at risk in that row and names the mechanism it still lacks.
8. **Write the matrix.** One row per priority scenario and per hard constraint, then one row for what each option adds to run and change and one for how hard it is to undo; one column per option. Each cell is one sentence that says whether the measure holds, by which mechanism, citing a fact or an assumption id. No scores, ticks, stars or weights: [writing a cell](references/designing-from-drivers.md#writing-a-matrix-cell) says why and how.
9. **Recommend one, and say what would reverse it.** Recommend the option that meets the priority scenarios inside the constraints with the least to run and the easiest undo, with reasons that cite the matrix. The recommendation has to hold under the defaults the intake carries: when an option holds only inside a condition, such as up to 200 devices, and the intake's default lies outside it, recommend it conditionally with the measurement that decides, or recommend the option that holds under the default. Then list what would reverse the recommendation: observable conditions, each tied to an assumption or a scenario, with the threshold at which you would recommend another option. When one uncertain assumption decides between two options and a short test could settle it, propose a spike instead of guessing, as [spikes](references/designing-from-drivers.md#when-a-spike-settles-more-than-a-comparison) describes.
10. **Write the study and the index.** Fill [the options template](templates/options.md) at `studies/YYYY-MM-DD-<slug>/README.md`, with the Outcome `waiting for the pick` and the Pick section reading `Waiting`. State what was not checked: measures nobody has taken, prior art you could not search, costs not priced, code not read. Add the study's row to the Studies table of the architecture index, and change nothing else in it (create the index as the conventions describe when there is none). Check every view and link against the conventions' "Before you finish" list.
11. **Try to break the study.** Before you report, run the falsification pass that [the intake](references/scenario-intake.md#the-falsification-pass) describes: an independent agent where the harness can start one, otherwise your own second read from the last ledger row backwards, attacking every step said to succeed, every sum, every default, every measure of zero, every end state and every threshold. Change the study for what breaks, and fill its "Falsification pass" section with who did it, what broke, and what could not be checked without running the system.
12. **Rebuild the page.** When the skill `drawing-architecture-views` is available, rebuild `architecture.html` by its steps before you report, where a shell is available with its build script, and read the page's check lines as it describes. When it is not available, leave `architecture.html` as it is, write the views in Markdown only, say in your report that the page was not rebuilt and is out of date, and name `drawing-architecture-views` as the skill that rebuilds it. Say too that the new views have not been drawn: their Mermaid is unchecked until the page is rebuilt and its check lines are read. Ask the person to have the page rebuilt and to read its `DONE` line before they rely on the pictures.
13. **Ask for the pick.** Send the report (see Hand back) and ask the person to choose, through the harness's question tool where it has one, with the options as choices and the recommended one first. Then follow the gate.

## Gate: Pick

The person chooses in their own words. Until they do, the study says the choice is waiting.

- **A pick** ("go with B", "B", "take your recommendation"): write it in the Pick section with the date and their words quoted, set the Outcome to `picked option B on YYYY-MM-DD`, and update the index row to match. "You choose" is a pick by delegation: record the recommended option as picked, with their words. A pick that differs from the recommendation is recorded the same way, without arguing it again: leave the recommendation as written on its date, and add one line naming the reversal conditions or open assumptions the picked option must now settle first. After recording any pick, give a short updated report that opens with the current outcome, and correct any saved report that still describes the choice as waiting.
- **A combination** ("B, but keep A's database index as the fallback"): restate the combination in one paragraph, check it against the scenarios and constraints in the matrix, and ask the person to confirm it. Record it once they do.
- **No answer, or an answer that is not a choice** (a question, "looks good", "let me think", silence): it is not a pick. Answer any question with evidence, leave the Pick section at `Waiting`, with the date you asked, and say in your report that the choice is waiting. Never record a pick the person did not make.
- **After a pick**, offer a decision record in one line. When the person accepts, write it in the repository's decision log by that log's own conventions (numbering, template, index row; with a decision-records skill when one is installed), with the options as the alternatives considered and a link to the study; with no decision log, offer to start one at the location rule's `context/decisions/`. Then offer to update the standing views with the picked option's new and changed elements as `planned`, as a separate step that leaves the study's files unchanged. On a new system, the next steps are a critical look at the chosen option (`evaluating-architecture-risks`) and then the standing views drawn as `planned` (`drawing-architecture-views`). In a product context repository, both belong to `designing-system-architecture`: hand the pick over with the study.

## Output

- `studies/YYYY-MM-DD-<slug>/README.md`: the intake; what is already settled; the prior art or the statement that the harness could not search; each option with its view and compare link; the options considered and dropped; the matrix; the recommendation and what would reverse it; a spike when one is proposed; what was not checked; the Pick section; the next skill.
- One `proposed` view per option in the study folder, all at one level with shared ids, and a `<view>-current.md` only when no standing view gave the base.
- The index row, and `architecture.html` rebuilt or reported as out of date.
- After a pick: the Pick section and the Outcome updated, and the decision record and standing-view update when the person accepted them.

## Done when

- The intake, two or three options that differ in kind (or the stated reason there is only one), one of them the smallest change, and a matrix row for every priority scenario and constraint with a sentence in every cell.
- The recommendation cites the matrix and names what would reverse it; what was not checked is listed.
- The pick is recorded with its date and the person's words, or the study states that the choice is waiting.
- No standing view and no decision record changed without the person's yes; the index lists the study; the page is rebuilt or reported as out of date.

## Example

The person says: "Deploys of the pantry code keep interrupting sync. Should we split sync into its own microservice?" Larder's folder has `containers.md` with `web`, `mobile`, `api` and `db`; the decision log has no record on deployables. The intake restates the question without the named solution: "Which failures and changes in one part of the API reach sync today, and what must sync keep while the rest of the API changes?" S1, a change scenario: a pantry change is deployed while 50 phones are syncing; measure, no sync request fails and none is applied twice. S2, a failure scenario: a pantry endpoint leaks memory until its process restarts; measure, sync keeps answering within 2 s. C1: one developer runs production. The trace shows each deploy restarts every API instance at once (a fact, with the deployment file's path), and that the mobile client already retries a failed sync idempotently. The axis is how far sync is isolated from the rest. A, the smallest change: a rolling deploy with a health check and connection draining, nothing new to run. B: the same code started as a second deployable, `api_sync`, sharing `db`. C: a sync service with its own store, `sync_db`, fed by events from `api`. The matrix: A meets S1 by draining and the client's retry, and leaves S2 at risk because both still share one process; B meets S1 and S2 with one more service to deploy and watch; C meets both and adds a store, an event contract and a second place household data lives, which C1 weighs against. Recommendation: A now, reversed if the memory leak in S2 recurs after it is fixed, where B wins; C only if sync needs a schema of its own. The Pick section reads `Waiting`. Two days later the person writes "go with B": the Pick section records it with the date and their words, the Outcome becomes `picked option B on 2026-11-20`, a decision record is offered, and so is updating `containers.md` with `api_sync` as `planned`.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| Options picked from a pattern catalogue, then justified | Derive each from the scenarios: which mechanism meets which measure |
| Three brands of the same mechanism | One option per mechanism; brands are a detail of the picked option |
| No small option, or a smallest change written as a strawman | Option A is the least that could work, with the situation it wins in |
| Options drawn at different levels, or one element with two ids | Same level, same base, same id for the same element |
| Scores, stars, weights or a total | One sentence per cell, citing a fact or an assumption |
| The person's named solution adopted as the question | Restate the problem; the named solution is one proposal among the options |
| Quietly ignoring a decision record | List it as settled, or label the option that would reopen it |
| "Looks good" recorded as a pick | Only an explicit choice is a pick; otherwise the choice is waiting |
| Editing a standing view to show the recommended option | The options live in the study; standing views change only after a pick and the person's yes |
| A confident recommendation on a guess that a short test could settle | Propose a spike with its question, threshold and timebox |

## Hand back

Report:

- What was written: the study's path, each option's view, the index row, and whether the page was rebuilt (its `DONE` line) or is out of date and which skill rebuilds it.
- The options in one line each, the recommendation, and what would reverse it.
- What is uncertain: assumptions the person should confirm, prior art not searched, measures nobody has taken, and the spike when one is proposed.
- The pick: the question to the person, or the pick as recorded, with the offers that follow it.
- The skill that fits next: `evaluating-architecture-risks` for a critical look at the picked option, which is the usual next step on a new system; a decision record after the pick; `drawing-architecture-views` to draw the standing views as `planned`; `recovering-built-architecture` when the views lacked evidence; `designing-system-architecture` when the architecture lives in a product context repository. On an existing application the usual order is: recover, evaluate, then explore or simplify, then a decision record, then the standing views updated; on a new system: explore, evaluate the chosen option, then draw the standing views as `planned`.

Commit nothing: the person reviews the study and commits it. Without file access, return the study and its views as Markdown and say that nothing was written and the page was not rebuilt.

## Not for

- Choosing how to build one work item inside the existing structure, such as which library, which module or which data shape: `brainstorming-solutions`. A choice that changes an element, a store, a boundary or a deployable belongs here.
- Deciding whether a prototype idea is worth trying: `framing-prototype-ideas`.
- A critical look at one design (`evaluating-architecture-risks`) or removing parts (`simplifying-system-architecture`): this skill compares alternatives and hands the picked one on.

## References

| Read | When |
|---|---|
| [the scenario intake](references/scenario-intake.md) | Step 2, before any option: the question, scenarios, constraints, facts and assumptions, decisions |
| [designing from drivers](references/designing-from-drivers.md) | Steps 4 to 9: deriving options, the smallest change, one level and shared ids, tracing, matrix cells, reversal conditions, prior art, spikes, a new system |
| [the options template](templates/options.md) | Step 10, and at the gate: writing the study and the Pick section |
| [the view conventions](references/view-conventions.md) | Before writing: location rule, view format, statuses, ids, evidence, Mermaid subset and quoting, compare links |
| [the view template](templates/view.md) | Step 6: writing each option's view |
