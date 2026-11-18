# Scenario intake

The intake is the first part of every study that judges an architecture: a risk review, an options study or a simplification study. It fixes, in writing and before any judgement, what the study is for and what "good" means, so the judgement can be checked against something other than taste. Every verdict, option and removal in the study refers back to it by id.

The examples use Larder, a fictional household pantry app: a web client, a mobile client, an API and one Postgres database.

## Contents

1. [What the intake holds](#what-the-intake-holds)
2. [Read before you ask](#read-before-you-ask)
3. [The real question](#the-real-question)
4. [Priority scenarios](#priority-scenarios)
5. [Hard constraints](#hard-constraints)
6. [Facts, assumptions and proposals](#facts-assumptions-and-proposals)
7. [What is already decided](#what-is-already-decided)
8. [Asking the person](#asking-the-person)
9. [The intake block](#the-intake-block)
10. [A filled example](#a-filled-example)
11. [Before you move on](#before-you-move-on)

## What the intake holds

Five parts, in this order, at the top of the study under `## Intake`:

1. **The real question**, restated without the solution the person named.
2. **Three to five priority scenarios**, each with six fields: source, stimulus, environment, the part affected, response, measure.
3. **Hard constraints**, which no score or preference can trade away.
4. **Facts, assumptions and proposals**, kept apart. A fact has evidence. An assumption names what would confirm it.
5. **What is already decided**, read from the decision log and the standing views.

Keep it short: a page at most. Its job is to make the rest of the study checkable, not to be complete.

## Read before you ask

Read in this order, and take from the repository everything it can answer, because a question the repository answers costs the person time and tells them you did not look:

1. The repository's `AGENTS.md` (or `CLAUDE.md`), for where the architecture folder and the decision log are.
2. The decision log's index, and every record that touches the subject.
3. The architecture index and the standing views the subject crosses, and earlier studies on the same subject.
4. What the product promises its users: the README, the app's own copy, store listings, terms, help pages, an SLA. These are the source of most scenarios.
5. The code and configuration the subject crosses: entry points, deployment files, schema, the constants that set limits (timeouts, retention, batch sizes, instance counts), and the tests' names, which often state an intended behaviour.

## The real question

Restate what the person needs to know or decide, in one or two sentences, without the solution they named. Quote their words above it with the date, so a reader sees both.

A named solution is a clue to the problem, not the problem. "Should we add a cache?" usually means "this is too slow for someone"; "should we split the API?" may mean "deploys of one part keep breaking another" or "one part needs to scale alone". Restating lets the study test the named solution as one proposal among others, and leaves room for the answer that no architecture change is needed.

Test the restatement: a different solution could answer it, and the person would agree it is what they want to know. When the request names an upcoming change ("before we add X"), the question includes whether the system is ready for that change.

| Person's words | Restated |
|---|---|
| "Should we put Redis in front of Postgres?" | "Pantry pages are slow for large households. Where does the time go, and what bound must hold?" |
| "Take a critical look at the digests before we add SMS reminders" | "Will reminders keep reaching members when a second delivery channel is added, and what breaks first?" |
| "Can we drop the job runner?" | "Which guarantees does the job runner give, and can each be kept with less to run?" |

## Priority scenarios

### The six fields

A quality-attribute scenario turns a vague quality into something a design can be traced against. Each has six fields:

| Field | What it says | Larder example |
|---|---|---|
| Source | Who or what causes the stimulus | A household member on a phone |
| Stimulus | What happens | Syncs after a day offline with 200 changed items |
| Environment | The conditions it happens in | A mobile connection, normal load |
| Part affected | The elements the scenario crosses, by element id | `mobile`, `api`, `db` |
| Response | What the system does | Applies every change once and returns the household's current state |
| Measure | How to tell whether the response is good enough, as a number or an observable condition | Under 2 s end to end, and 0 changes lost |

### When a scenario counts as met

A scenario is met only at its response, as its source observes it, within its measure. Follow it to the last element of the part affected, which is usually where a person sees the result or a caller gets its answer: a change that reached a device's local store is not yet a change the member sees on the screen. Compare the mechanism's own numbers with the measure in the same unit: a retry that waits five minutes cannot meet a measure of one minute. Where the trace stops one element short, or the numbers do not meet, the verdict is at risk or does not hold, with the missing mechanism named, never met with a caveat. The same test applies to every default a proposal carries, a cutover included: a default that gives up part of a promise even once does not keep that scenario.

### The trace ledger

A verdict written from memory of a trace tends to skip the waits. So for every scenario whose measure is a time or a count, write the trace as a ledger before you write its verdict, one row per step, in order:

| Step | Element | What happens | Wait or cost, normal | Wait or cost, bad day | Evidence |
|---|---|---|---|---|---|
| 1 | `mobile` | The member ticks an item; the change is written to the local store and the outbox | 0 s | 0 s | `mobile/src/screens/List.tsx:22` |
| 2 | `mobile` | The outbox is sent on the next sync timer | up to 30 s | up to 5 min after a failed attempt (backoff cap) | `mobile/src/sync/engine.ts:12`, `:40` |
| 3 | `api` | Accepts and applies the change | 0.1 s (A2) | 0.1 s | `api/src/sync/routes.ts:22` |
| 4 | `mobile` (the other phone) | Pulls on its own timer and re-reads the list on screen | up to 30 s | up to 30 s | `mobile/src/sync/engine.ts:12` |
| Sum | | | up to 60 s | up to 5.5 min | |

- Start at the first thing the source does, the tap or the request, not at the first server element: a change that waits in a client's outbox has not started its journey.
- End at the element where the source observes the response, and say what that element shows. For an end state, the last row says what the source's own device ends up with, including what it does with its own changes when they come back to it.
- Put every timer, poll interval, batch window, retry delay and backoff cap on its own row, with its number and the line it comes from. A wait that is not on the ledger is not counted, and a number you assumed carries its assumption id.
- Sum both columns and set the sums beside the measure. The verdict follows from the numbers: met when both sums are inside the measure; at risk when only the bad-day sum is outside, or a decisive row rests on an assumption; not met when the normal sum is outside. A proposed change earns a better verdict only through the rows it changes.

Keep each ledger in the study, under the scenario or the option it belongs to. A ledger that is the same for several options is written once and named as shared.

"Fast" is not a scenario; "a household of 5 syncs 200 items on a mobile connection in under 2 seconds" is. "Reliable" is not a scenario; "the API restarts during a sync and no accepted change is lost or applied twice" is. A measure is something a check could observe: a duration at a percentile, a count of lost or duplicated items, a time to recover, a number of places a change must touch.

### Kinds of scenario

Cover the kinds the question touches, not all of them:

- **Runtime:** normal use under normal or peak load (latency, throughput, freshness).
- **Failure:** something breaks (a process dies, a dependency is slow or down, a disk is lost) and the system must still keep a promise.
- **Growth:** the load, the data or the number of clients grows to a stated size.
- **Change:** someone changes the system (adds a client, a field, an integration) and the measure is how many elements must change, or how long it takes.
- **Security:** someone who should not see or change data tries to, and the measure is what they can reach.

### Deriving scenarios from the product's promises

When nobody hands you scenarios, derive them; this is the usual case.

1. **List the promises.** Collect what the product tells its users and what the team has committed to: "works offline", "no change is lost", "everyone sees the same list", "your data stays in the EU", an uptime figure, a response time in a contract. Quote each with its path.
2. **List the limits the code already sets.** Retention periods, timeouts, batch sizes, instance counts, rate limits, cron schedules. Each is an implicit promise or an implicit risk: a 30-day retention limit means something happens on day 31.
3. **Turn each promise into a stimulus and an environment that would test it.** Push it to its edge: "works offline" becomes "after the longest time offline the product promises"; "no change is lost" becomes "while the process holding the change is killed".
4. **Write the measure from the promise's own words.** "No change is lost" gives "0 accepted changes lost". When the promise has no number, propose one, mark it as an assumption (`A1`) and say who would confirm it. A proposed number makes the scenario traceable; leaving it vague makes every verdict unfalsifiable.
5. **Add the change the person is about to make**, when there is one, as a change or growth scenario.

### Picking three to five

Tracing costs real effort per scenario, and a study with twelve scenarios traces none of them well. Keep the three to five that:

- the real question is about;
- the architecture decides, rather than one line of code inside one element;
- would be costly or irreversible to get wrong: lost data, exposed data, a promise broken for every user;
- pull against each other, because that is where trade-offs show;
- include at least one failure scenario, and, when a change is coming, one scenario in which it happens.

Order them by priority (`S1` first). List the ones you considered and left out on one line, `Considered, not traced:`, so the reader knows they were not forgotten.

## Hard constraints

A hard constraint is a limit the study cannot trade away: a law or regulation, a contract, a budget ceiling, the size of the team that runs the system, a platform the product must run on, a decision the person says is fixed. Give each an id (`C1`) and its evidence.

A preference is not a constraint: "we like Postgres" is a preference unless a decision record or the person makes it fixed. Keep the list short and real, because every constraint removes options. An option or a removal that breaks a hard constraint is out, however well it does on the scenarios; no score or weighting brings it back.

## Facts, assumptions and proposals

Keep three lists apart, each item with an id, because a study that mixes them presents guesses as findings:

- **Facts (`F1`)** have evidence: a repository path, optionally with a line, or `stated by <person>, <YYYY-MM-DD>`, the same evidence forms the view conventions use. "The API retries a failed write three times (`api/src/db/retry.ts:12`)."
- **Assumptions (`A1`)** are what the study takes as true without evidence, each with what would confirm or refute it: "Households have under 2,000 items; a count per household from the production database would confirm it." A runtime fact the code cannot show (traffic, data volume, real latencies, how often a dependency fails) is an assumption until someone measures it.
- **Proposals (`P1`)** are designs not yet built or agreed: the solution the person named, a study's `proposed` view, a design document. A proposal is judged, never used as evidence.

A view's claim is a fact only when its Evidence cell holds; an element marked `assumed` in a view is an assumption here.

## What is already decided

List the decisions that bound the study, each linked: accepted decision records, accepted outcomes of earlier studies, and `planned` elements in the standing views, which someone already agreed to. Respect them: the study works inside them and does not reopen one silently.

When the evidence says a decision no longer holds (its context changed, its assumption failed), say so in the study, name the record and what changed, and leave reopening it to the person, because a decision record is theirs. When the decision log is empty or missing, say so in one line.

## Asking the person

Ask only what the repository cannot answer: a measure only they can set, which promise matters most, a constraint that lives in a contract, the size of a planned change. Ask in one message, with every question numbered and a proposed default for each, so they can answer "yes to all" in one line.

When the answer would not change which scenarios you trace or how, do not ask: use the default and record it as an assumption. When no answer comes, carry on with the defaults, mark each as an assumption with who would confirm it, and say so in the report.

## The intake block

Write it at the top of the study, under the title and the header line, before any verdict, option or removal:

```
## Intake

Asked by <person> on <YYYY-MM-DD>: "<their words>"

**The real question.** <One or two sentences, without the named solution.>

**Priority scenarios.**

| Id | Source | Stimulus | Environment | Part affected | Response | Measure |
|---|---|---|---|---|---|---|
| S1 | <who or what> | <what happens> | <conditions> | <element ids> | <what the system does> | <number or observable condition> |

Considered, not traced: <scenarios left out, one phrase each, or none>.

**Hard constraints.**

- C1: <constraint>. Evidence: <path, stated by, or decision record link>.

**Facts.**

- F1: <fact>. Evidence: <path:line or stated by>.

**Assumptions.**

- A1: <assumption>. Confirmed by: <the observation or the person that would settle it>.

**Proposals.**

- P1: <the named solution or design under study>. Source: <the person's words, a study view, a document>.

**Already decided.**

- <link to a decision record, an accepted study or a standing view>: <what it settles for this study>.
```

Write "none" under a heading that has nothing, rather than dropping the heading, so a reader can tell "none" from "not checked".

## A filled example

```
## Intake

Asked by Dana on 2026-11-12: "Search is slow for big households. Should we add Meilisearch?"

**The real question.** Members of large households wait too long for pantry search results. Where does the time go, and what response time must search keep as households grow?

**Priority scenarios.**

| Id | Source | Stimulus | Environment | Part affected | Response | Measure |
|---|---|---|---|---|---|---|
| S1 | Member on the web | Types three letters of an item name | Household of 3,000 items, normal load | `web`, `api`, `db` | Shows matching items | First results under 300 ms at the 95th percentile |
| S2 | Member on a phone | Adds an item, then searches for it | Mobile connection | `mobile`, `api`, `db` | The new item is found | Found on the first search after the add |
| S3 | Developer | Adds a searchable field to items | One developer, normal week | `api`, `db` | Field is searchable in both clients | One migration and one query change, no new process to run |

Considered, not traced: search across households (not offered), typo tolerance (not promised).

**Hard constraints.**

- C1: One developer runs production. Evidence: stated by Dana, 2026-11-12.
- C2: Personal data stays in the EU. Evidence: `docs/privacy.md:14`.

**Facts.**

- F1: Search runs `ILIKE '%term%'` over item names with no index that serves it. Evidence: `api/src/pantry/search.ts:21`, `api/migrations/002_items.sql`.
- F2: The largest household has 3,140 items. Evidence: stated by Dana, 2026-11-12.

**Assumptions.**

- A1: The 300 ms bound in S1 is what members expect. Confirmed by: Dana.
- A2: Item counts grow under 20 percent a year. Confirmed by: monthly counts from the production database.

**Proposals.**

- P1: A Meilisearch index fed by the API on every item change. Source: Dana's words above.

**Already decided.**

- None: the decision log has no record on search or on adding stores.
```

## Before you move on

- The question is restated without the named solution, and the person's words are quoted with the date.
- Three to five scenarios, ordered by priority, each with all six fields and a measure a check could observe.
- At least one failure scenario, and a scenario for the coming change when there is one.
- Every constraint is hard and has evidence; every fact has evidence; every assumption says what would confirm it; every proposal is labelled as one.
- The decision log and the standing views were read, and what they settle is listed.
- At most one message of questions went to the person, and nothing in it was answerable from the repository.
