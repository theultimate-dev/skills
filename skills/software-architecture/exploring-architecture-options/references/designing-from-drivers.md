# Designing from drivers

How to turn an intake into two or three options worth comparing, compare them honestly, and recommend one in a way the person can check. The drivers are the intake's priority scenarios and hard constraints: every option exists because it meets them in a different way, and every judgement in the study points back to them by id.

The examples use Larder, a fictional household pantry app: a web client, a mobile client, an API and one Postgres database.

## Contents

1. [Drivers before options](#drivers-before-options)
2. [The axis the choice turns on](#the-axis-the-choice-turns-on)
3. [Options that differ in kind](#options-that-differ-in-kind)
4. [The smallest change](#the-smallest-change)
5. [One level, one base, shared ids](#one-level-one-base-shared-ids)
6. [Tracing the scenarios through each option](#tracing-the-scenarios-through-each-option)
7. [Writing a matrix cell](#writing-a-matrix-cell)
8. [Recommending, and what would reverse it](#recommending-and-what-would-reverse-it)
9. [Prior art](#prior-art)
10. [When a spike settles more than a comparison](#when-a-spike-settles-more-than-a-comparison)
11. [A new system with no code](#a-new-system-with-no-code)
12. [Before you write the study](#before-you-write-the-study)

## Drivers before options

Start from the scenarios, not from a list of patterns. For each priority scenario, ask which mechanism could give its response at its measure, and write the candidates down before you group them into options:

| Scenario | Candidate mechanisms |
|---|---|
| S1: three typed letters show the first matching items within 300 ms, in a household of 3,000 items | An index inside the existing database; a search engine we run beside the API; a managed search service |
| S2: an item added on a phone is found by the next search | Query the database directly, which is always current; update the index on every write; feed the index from a change log with a lag |
| C1: one developer runs production | Nothing new to run; a managed service; one more process on the same platform |
| C2: personal data stays in the EU | Anything we run in the current region; a managed service only with an EU region |

Then group mechanisms that work together into options. A pattern name ("event-driven", "CQRS", "microservices") is a label you may add afterwards, never the reason an option exists.

Why: an option chosen from a catalogue arrives with its own justification and gets defended, while an option built from mechanisms is tied to a measure a reader can check. It also keeps the first idea from anchoring the rest: listing mechanisms for every scenario before judging any of them is what makes the second and third options real.

Read the mechanisms the system already has before inventing new ones. A retry loop, a log, a cursor, a scheduled job or a health check that exists today is often the cheapest way to meet a new scenario, and it is where the smallest change usually starts.

## The axis the choice turns on

A system-level choice usually turns on one axis. Find it, then place the options at different points on it. The common axes:

| Axis | Positions |
|---|---|
| Where a responsibility lives | Inside an existing element; in a new element we run; in a service someone else runs |
| How a change travels | The caller asks and waits; the reader polls; the writer pushes on an open connection; events go through a log or a queue |
| Who holds the authoritative data | One store; several stores, one writer each; copies on devices that merge |
| What deploys and fails together | One deployable; several deployables sharing a store; separate services with their own stores |
| Build, run or buy | Code we own on infrastructure we run; code we own on a managed platform; a managed service |
| How we get there | Change in place; build alongside and switch over; replace |

Pick the axis whose positions change which scenarios hold or what someone must run. When two axes move together (a search engine we run is both a new place for a responsibility and a second copy of the data), treat them as one.

## Options that differ in kind

Two options differ in kind when at least one priority scenario or constraint gets a different answer for a different reason, or when what someone must run, watch, pay for and restore differs. Three message brokers that give the same delivery guarantee are one option; the brand is a detail of that option, chosen after the pick. An index inside the existing database, a search engine we run and a managed search service are three options, because each meets the search scenario by a different mechanism and leaves a different thing to run.

Give each option the situation it wins in, in one sentence about this system: "B is the best choice when households grow past what one database index can serve, or when typo tolerance becomes a promise." When you cannot write that sentence, the option is a strawman: drop it. When an option breaks a hard constraint, drop it too, whatever it does for the scenarios. List both under "Considered and dropped" with the reason, so the reader sees they were weighed.

Three is a maximum, not a target. Two real options are better than two and a filler. When only one option survives the constraints, say so plainly, keep the smallest change as the comparison when it is viable, and let the matrix show why the others fell.

## The smallest change

Option A is always the least change to the current system that could meet the priority scenarios: a setting or a limit, a mechanism the system already has stretched to a new use, a change inside one element, or an operational step with no change to the architecture at all.

It is always there for three reasons. It often wins: every new element is one more thing to deploy, watch, upgrade, secure and restore for as long as the system lives, and a long-lived system pays that every year. It prices the others: the matrix shows exactly what the bigger options buy beyond it, cell by cell. And it is the easiest to undo, so when the evidence is thin it is usually the safest step.

Write it in its honest best form, with its winning situation, never as the option set up to lose. When it cannot meet a scenario, its cell says so and why: that sentence is the evidence that a bigger option is needed.

When even the smallest change is more than the scenarios need, because the system already meets them, say so: either the question is not architectural (the work is inside one element, which `brainstorming-solutions` handles where installed) or the scenarios missed what the person is worried about, and you should say which.

## One level, one base, shared ids

Draw every option at the same level, so the reader compares like with like: usually containers; the context when the options differ in which outside systems are involved; deployment when they differ in where things run and what fails together. Pick the level where the options differ, and keep all of them there.

Start each option's view from the same base: the standing view at that level, or, when there is none, a current-state view you draw in the study with evidence. Copy the base, then change it. The view conventions give the file names: the base view's name, then the option, such as `containers-db-index.md`, `containers-search-engine.md`, `containers-managed-search.md`.

Ids follow one rule: the same element has the same id everywhere, and a different element has a different id.

- Elements the option leaves alone keep their id and their `built` status.
- A new element gets a new id. When two options add the same element, it has the same id in both.
- When two options add elements with a similar role but a different nature (a search engine we run, `search`, against a managed search service, `search_saas`), they get different ids, because a matrix cell that names `search` must mean one thing.
- A removed element disappears from that option's picture; say so in the prose under the diagram, because a picture cannot show what is missing.
- Look up the index's element ids table before choosing a new id, and never reuse an id the system once had.

In each option's view, the new and changed elements are `proposed` in the Elements table, carry the `proposed` class, and their arrows are dotted. The view's Status line is `Status: proposed`. Evidence for a proposed element is the study's own README, a prior-art source, or `assumed`.

Keep every option's view to the same scope: the elements the choice touches and their direct neighbours, within the 15-element cap. A view that shows more of one option than another makes it look heavier than it is.

Link each option from the study with a compare link, the base first. From a study the link target reaches the page two folders up, and the source paths after `#compare=` stay relative to the architecture folder: the base view, then `studies/<date>-<slug>/<option view>.md`.

## Tracing the scenarios through each option

Trace every priority scenario through every option, in the same order, element by element:

1. Where the stimulus enters, by element id.
2. Each element it crosses: what that element does with it and which mechanism gives the response (an index, a poll interval, an open connection, a transaction, an ordering rule, a retry, a retention limit).
3. Where the measure is spent (time, a count, places a change must touch) and where it could fail.
4. What differs from the trace through the current system, and from the other options.

Cite a path for every built element on the path, and an assumption id or a prior-art source for every proposed one. Keep the working notes short; put a trace in the study only where it decides the matrix, as a few lines under the option.

Three traces are easy to forget:

- **The new element failing.** Every element an option adds brings its own failure scenario: what happens to S1 when the search engine or the managed service is down, and to S2 while the index is rebuilt? Trace it, at least in one sentence per option.
- **Getting there.** How existing data, clients and devices move to the option: a migration, two versions of a client in the field, a cut-over. An option that is sound once built and dangerous to reach is not sound.
- **The decision on record.** When a decision record explains a mechanism a scenario depends on (why sessions live in the database, why one process applies changes in order), trace that the option keeps what the record relies on, or label the option as reopening it. Read the record's Consequences too: a record that names its own fallback or the condition for revisiting it tells you which options it already accepts.

## Writing a matrix cell

Rows are the priority scenarios and the hard constraints, then two more: what the option adds to run and change, and how hard it is to undo. Columns are the options, the smallest change first. Each cell is one sentence with three parts: whether the measure holds, by which mechanism, and on what evidence.

| Instead of | Write |
|---|---|
| ✓, 4/5, "good", "high" | "Holds: a trigram index serves three-letter matches from the database, 40 ms on a copy with 3,000 items (F5)." |
| "Better than A" | "Holds only while the index lags writes by under a second; a phone that adds and then searches at once may miss the new item (A3)." |
| "Scales well" | "At risk past about 100,000 items per household, where the index outgrows the database's memory on the current plan (A2)." |
| "Complex" | "Adds one process to deploy, watch and restore, and a second copy of item names to keep in step with the database." |

For the constraint rows, the sentence says how the option stays inside the constraint. An option that breaks one is not in the matrix; it is under "Considered and dropped".

For the undo row, use one scale across options: easy (a setting or a flag undoes it), moderate (a code change undoes it, no data or contract moves), hard (undoing needs a data migration, a public-contract change, or an external commitment such as a vendor contract).

No scores, ticks, stars, weights or totals. A score hides its reason, so nobody can check it against the code; a number invites precision the evidence does not have; and a weighted total lets a broken constraint or a failed failure scenario be averaged away by good marks elsewhere. A sentence can be wrong in a way someone can see, which is what makes it useful.

When changing one assumption would change which option the matrix favours, write it under the matrix: "Close call: A2 decides between A and B." Then propose a spike or ask the person, instead of presenting the winner as clear.

## Recommending, and what would reverse it

Write the recommendation in this order: the option; the scenario and constraint rows that decide it; what it costs to run and to undo; why each other option loses, in one clause each. Prefer, among options that meet the priority scenarios inside the constraints, the one with less to run and an easier undo, and say so when that is the reason.

Then list what would reverse it: two to four conditions, each observable, each with a threshold, each tied to an id.

- "If the largest household passes 50,000 items (A2), A misses S1 and B wins."
- "If typo tolerance becomes a promise to members, A cannot meet it, and B or C is needed."
- "If the managed service has no EU region (A5), C breaks C2 and is out; if the spike shows its EU region adds more than 150 ms (A6), C misses S1."

"If requirements change" is not a reversal condition: name the requirement and the value. A reversal condition tells the person which assumption to confirm first, and tells a later reader when the decision is due for review.

Say the uncomfortable answer when it is the true one:

- The smallest change wins, though the person asked about the bigger design.
- The best option reopens a decision on record: recommend it, name the record and what changed, and leave reopening it to the person.
- No option can be recommended from the evidence: a spike or a measurement comes first.
- No option changes an element, a store, a boundary or a deployable: the choice is not architectural, and the study says so.

## Prior art

Look in this order, and stop when you know enough to trace the options:

1. **The repository.** The closest mechanism the system already has, end to end: its code, its limits, its tests. The decision records and earlier studies on the subject. This is where the smallest change comes from.
2. **Dated official documentation** for the versions in use, where the harness can search the web: the guarantees, limits and failure behaviour of the mechanism or service an option relies on.
3. **A first-party account** of a team running the same mechanism in production: what it cost them and what went wrong.

Record each outside source in the study with its address, the date you read it, the version it describes, the claim you use, and what transfers to this system and what does not (scale, team size, consistency needs, region). The popularity of an approach is not evidence that it fits; a claim from a source is a fact about the source until the trace shows it holds here.

Where the harness cannot search the web, say so in the study's prior-art section in one sentence, mark every claim about an outside service or library as an assumption with what would confirm it, and list the missing research under what was not checked.

## When a spike settles more than a comparison

A spike is a short, disposable test that observes one thing a comparison can only guess. Propose one when all of these hold:

- the recommendation turns on one assumption (a close call in the matrix, or a reversal condition you cannot rule out);
- being wrong would be costly or hard to undo: a store, a vendor, a data migration;
- a test of hours to two days, in a safe environment, could observe it;
- documentation does not already answer it.

Write it in the study's Spike section as a card:

```
- Question: <the one assumption, by id>
- Decides between: <option ids>
- Setup: <what is built, with which versions, against what load or data>
- Observe: <the measurement>
- Threshold: <value> or better: <option>; worse: <option>
- Timebox: <hours or days>
- Where it runs: <a local copy, a test environment; never production unless the person says so>
- Thrown away afterwards: <what is not kept>
```

Propose it; run it only when the person asks. When it has run, add its result to the Spike section with the date and the raw observation, and update the recommendation with one line saying what the spike changed. A spike is not the place to build the option: its code is thrown away, and the option is built after the pick.

A test that cannot represent the scenario (a toy load, a different version, a local network for a mobile scenario) does not settle it; say what it does not represent.

## A new system with no code

With no code, the brief and the person are the evidence.

- **Location.** Apply the location rule: with no `AGENTS.md` pointer, write under `context/architecture/` and propose the pointer line.
- **Intake.** Derive the scenarios from the brief's promises ("works offline", "shared by the household", a response time, a region). Facts cite the brief's path or `stated by`. Almost every runtime number is an assumption; say who or what would confirm it.
- **The smallest change** becomes the fewest moving parts: the fewest deployables, stores and technologies, on a platform's managed features, that could meet the scenarios. A bought service counts as fewer parts to run but not as free: when leaving it later means rewriting the clients or migrating data, the undo row says so, and the recommendation weighs it.
- **Part affected.** When the options differ in their backend elements, write the shared ids in the scenario table and add one line above it naming each option's own elements, so every trace still lands on element ids.
- **Options** on a new system usually differ on the axes that are cheap to choose now and expensive to change later: who holds the authoritative data (the server, or each device with merging), how many deployables, and what is bought against what is run.
- **Views.** There is no standing view and no base to compare against. Draw each option at the same level with fresh ids shared across options, `Status: proposed`. A context view first only when the options differ in outside systems. Compare links put two options side by side: both source paths are inside the study.
- **After the pick.** No standing view changes yet: the next steps are a critical look at the chosen option, then the standing views drawn as `planned`.

## Before you write the study

- Every option is built from mechanisms that meet named scenarios, and each has its winning situation.
- The options differ in kind; option A is the smallest change; dropped options are listed with the reason.
- Every option's view is at the same level and scope, starts from the same base, and uses one id per element.
- Every scenario is traced through every option, including the new element failing and the way there.
- Every matrix cell is a sentence with a mechanism and an evidence or assumption id; no scores.
- The recommendation cites rows; the reversal conditions are observable, with thresholds and ids.
- Prior art is recorded with dates and limits, or the study says the harness could not search.
- What was not checked is listed.
