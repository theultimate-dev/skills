# Review methods

How to take a critical look at an architecture: trace the priority scenarios, look for what they miss, and write findings a reader can check. The method is a lightweight review in the spirit of the SEI's Architecture Tradeoff Analysis Method (scenarios, risks, sensitivity and trade-off points), Simon Brown's risk-storming, Gary Klein's premortem, failure mode and effects analysis, and the trust-boundary step of threat modelling. It is one agent's review, not a formal evaluation with stakeholders: call it a risk review, and treat every lens below as a prompt for evidence, not as testimony.

The examples use Larder, a fictional household pantry app: a web client `web`, a mobile client `mobile`, an API `api`, one Postgres database `db`, and a mail provider `mail`.

## Contents

1. [The stance](#the-stance)
2. [Trace each scenario](#trace-each-scenario)
3. [Single points of failure](#single-points-of-failure)
4. [Failure modes per dependency](#failure-modes-per-dependency)
5. [Trust boundaries and sensitive data](#trust-boundaries-and-sensitive-data)
6. [Premortem](#premortem)
7. [Writing a risk so it is checkable](#writing-a-risk-so-it-is-checkable)
8. [Ranking by likelihood and impact](#ranking-by-likelihood-and-impact)
9. [Trade-off points and sensitivity points](#trade-off-points-and-sensitivity-points)
10. [Next checks](#next-checks)
11. [When nothing needs to change](#when-nothing-needs-to-change)
12. [The annotated view and the failure sequence](#the-annotated-view-and-the-failure-sequence)
13. [Saying the uncomfortable thing](#saying-the-uncomfortable-thing)

## The stance

A review that agrees with everything has told the person nothing. For each claim the design makes (this is idempotent, this survives a restart, only this element writes that store), look for the strongest counterexample: the input, timing or failure that would break it. Keep a claim only when the evidence survives the attempt.

Three habits keep the review honest:

- **The code outranks the view.** A view is a claim about the code. On every path you trace, open the files the view cites and the files it should cite. When they disagree, the code is what runs; record the disagreement.
- **Evidence or label.** Every statement in the study is a fact with evidence, an assumption with what would confirm it, or a hypothesis marked as one. A plausible story is not a finding until it has a path through the elements and a piece of evidence.
- **Bounded claims.** "S2 is met within the reviewed scope (the API restart path; the database failover was not examined)" is a claim a reader can trust. "The system is resilient" is not.

## Trace each scenario

Tracing walks one scenario through the architecture, element by element, asking at each step whether the design still meets the measure and what shows it.

1. **Pick the views the scenario crosses.** Usually containers for responsibility, a runtime view for order, deployment for what runs where. Note the element ids in the scenario's "part affected" field and check they exist in the views.
2. **Write the path.** List the elements in the order the stimulus reaches them, with each hop: `mobile → api → db → api → mobile`. Include the paths taken on failure and retry, not only the happy path.
3. **At each element, ask four questions and write the answers:**
   - What does this element do with the stimulus? Read the code that handles it, not only the view's Responsibility cell.
   - Which mechanism provides the response here? A transaction, a timeout, a retry, an idempotency key, an ordering rule, a cache, a retention limit, a queue's acknowledgement.
   - What is the evidence? A path and line for the mechanism. A runtime value (latency, volume, failure rate) is an assumption unless someone measured it.
   - Does the measure still hold after this element? Spend the budget: a 2 s measure shared by four hops leaves each hop a part of it. For a correctness measure (nothing lost, nothing doubled), ask what happens if the element stops between any two of its steps.
4. **Note sensitivity points.** A setting whose small change moves the outcome sharply: a timeout, a batch size, a retention period, an instance count, a pool size. Write each with its evidence; they are where the next incident starts.
5. **Give the verdict.** One of three words, with the reasoning in a sentence or two and the evidence:

| Verdict | When | The study says |
|---|---|---|
| `met` | Every element on the path has evidence that it does its part, and the measure holds in the stated environment | Which mechanisms carry it, and the limits of what was checked |
| `at risk` | There is a credible path, with evidence, on which the measure fails | The path, the cause, and the risk ids it produced |
| `unknown` | The evidence that would decide it is missing: a runtime number, a configuration you cannot see, behaviour only a test would show | What is missing and the next action that would settle it |

Pick one word per scenario. "Met, but at risk at scale" is two scenarios: split it, or give `at risk` and say under which growth. A verdict of `met` reached without opening the code is `unknown`.

A trace can be written as a short table under the scenario:

```
| Step | Element | What it does | Mechanism | Evidence | Measure after this step |
|---|---|---|---|---|---|
| 1 | mobile | Sends 200 changes in one request | Batch with change ids | `mobile/src/sync/push.ts:30` | 0 lost so far; 300 ms spent (assumed, A2) |
| 2 | api | Writes the batch in one transaction | Unique key on change id | `api/src/sync/write.ts:18` | A repeat is skipped, not doubled |
```

## Single points of failure

A single point of failure is anything whose loss stops a scenario with nothing taking over. Look beyond processes:

- **Elements with one instance:** read the deployment configuration for instance counts; a container drawn once may run once.
- **Shared places:** two elements on one host, one disk, one database, one region, one account with the provider. They fail together even when the views draw them apart.
- **Hidden singletons:** one consumer that must run alone to keep order, one scheduled job, one lock, one certificate, one API key, one DNS name, one person who can deploy or restore.

For each candidate, write which scenarios stop, what the user sees, how the failure is noticed, and how long recovery takes (automatic restart in seconds, or a human restoring from a backup in hours). A single point of failure with a fast automatic recovery and no data at stake is often acceptable; say so instead of listing it as a risk. One that holds data no one has restored is not.

## Failure modes per dependency

For every dependency on the paths you traced (a store, a queue, another service, an external API, a client calling the API), ask what happens in each of these modes. A table per dependency keeps it short:

| Mode | Ask | Larder example |
|---|---|---|
| Slow | Is there a timeout, and is it shorter than the caller's? What waits, what piles up, what retries amplify the load? | `api` calls `mail` with no timeout: each slow call holds a request worker, and the API stops answering pantry reads |
| Down | Does the caller fail fast, queue, fall back, or lose the work? What does the user see? What happens on recovery? | `db` down: the API returns 503 and the mobile client keeps its local changes; nothing lost |
| Wrong answer | Is the answer validated? What spreads if it is wrong: a bad record stored, shown, sent on? | `mail` accepts a message and drops it: nobody notices, because only acceptance is checked |
| Duplicate | Is the receiving operation idempotent? What is the key, and how long is it kept? | A retried sync batch: the change id makes the second write a no-op |
| Out of order | Does the result depend on order? Who sets the order, and what happens when two writers race? | Two members edit one item: the later arrival wins, not the later edit |

Also ask, where it applies: full (disk, memory, a quota), stale (a cache or a replica behind), and partial success (step one done, step two not, and how repair happens). Watch for fixes that make failures worse: retries without backoff that multiply load, fallbacks that are never exercised, timeouts longer than the caller's.

Write only the modes that produce a finding or that a scenario depends on; for the rest, one line saying they were checked is enough.

## Trust boundaries and sensitive data

This pass finds architectural exposure. It is not a security assessment; when the findings call for one, the study says so.

1. **List the sensitive data** the subject touches: credentials and session tokens, secrets and API keys, personal data (names, email addresses, locations, anything about a household's life), payment data, the content users trust you with.
2. **Mark the trust boundaries:** where control changes hands. The user's device, your network, a managed service's network, a third party. A data-flow view with each boundary as a subgraph shows this; the view conventions give its form.
3. **Follow each kind of sensitive data across each boundary** and ask:
   - Who is authenticated at this crossing, and where is that enforced? A private network is a location, not an authorization: a store that anyone inside the network can read without credentials is reachable by every compromised neighbour.
   - Is the data encrypted in transit and at rest where it lands?
   - Does it reach a third party, and does the product's promise allow that (privacy text, region, consent)?
   - Where else does it land: logs, error reports, analytics, backups, emails?
   - Where do secrets live, and who can read them?
4. **Write each finding** as a risk with the element ids on both sides of the crossing.

## Premortem

Scenarios test what someone thought of; a premortem looks for what nobody did. Imagine it is a year from now and the system, or the change under review, has failed badly. Write three to five short stories of why, each from a different lens:

- the member who lost data or saw someone else's;
- the person on call at three in the morning, with one runbook and no help;
- the next developer making an ordinary change;
- someone who wants data they should not have;
- a dependency provider changing a limit, a price or an API;
- growth: ten times the users, the data or the clients.

Each story must be a concrete path through element ids with a trigger, a mechanism and a consequence: "Six months on, the household count has tripled; the nightly export in `api` now holds a long transaction on `db` past breakfast, and morning syncs time out." Then check each against the evidence. Keep the stories the evidence supports as risks; keep the plausible ones you could not confirm as assumptions with a check; drop the ones the code rules out, and say in one line that you checked them. These stories are one reviewer's lenses, not the views of those people: label them as such.

## Writing a risk so it is checkable

A risk the reader cannot check is an opinion. Write each one with:

| Part | What it holds |
|---|---|
| Id | `R1`, `R2`, in rank order once ranked |
| Elements | The element ids it sits on, which exist in the views; an arrow is written `api → mail` |
| Cause | The condition and the mechanism: what has to be true, and what then happens inside the element |
| Consequence | Which scenario or promise breaks, and what the user or operator sees |
| Evidence | Paths and lines that show the cause, or `assumed` with what would confirm it |
| Likelihood and impact | A band each, with its basis |
| Next check | The observation that confirms or clears it, with a threshold |

Weak: "The API might not scale."
Checkable: "R2 on `api`, `db`. Cause: the pantry list query reads every item of the household with no limit (`api/src/pantry/list.ts:14`). Consequence: S1's 300 ms bound fails above about 5,000 items. Likelihood possible (the largest household has 3,140 items, F2), impact major. Next check: time the query on a copy with 10,000 items; cleared when under 100 ms."

A risk that sits on no element is not yet a finding. Trace it until it lands on one, or record it as an assumption.

## Ranking by likelihood and impact

Use bands, each with its basis:

| Likelihood | Basis |
|---|---|
| Likely | It happens in normal operation, or has happened, or the evidence shows it will at the stated growth |
| Possible | It needs a plausible condition: a failure, a peak, a race |
| Unlikely | It needs several conditions together, or a rare external event |

| Impact | Basis |
|---|---|
| Severe | A product promise breaks for many users, or data is lost or exposed |
| Major | A scenario's measure fails, or a group of users loses a function for hours |
| Minor | Degraded but recoverable, few users, no data at stake |

Rank severe before major before minor within the same likelihood, and likely before possible before unlikely within the same impact. Then move irreversible harm (lost data, exposed data, a broken legal promise) ahead of reversible harm of the same bands, because a rare loss that cannot be undone may deserve action that a frequent annoyance does not. Do not multiply bands into scores: the product of two guesses is a third guess with false precision.

Write an uncertainty note where the band rests on an assumption, so a reader knows which rank a measurement could move. The top risks are the ones worth acting on now, usually three to five. A quadrant chart can show the ranking at a glance; put its points at the band centres, not at invented decimals, and keep the labels to an id and two words, as the view conventions describe.

## Trade-off points and sensitivity points

A **trade-off point** is a mechanism or setting that serves one scenario and hurts another. Find them by looking for an element that appears in two traces with opposite needs: a longer cache lifetime makes pantry pages fast (S1) and shows another member's edit late (S3); a longer session keeps members signed in (S2) and widens the window for a stolen token (S4). Write each as one sentence naming both scenario ids, the mechanism, and its evidence. Name it; do not resolve it, because choosing which scenario wins is the person's decision, and an options study is the place to compare the ways out.

A **sensitivity point** is a setting whose small change moves one scenario sharply, without a second scenario pulling the other way. List them with the trace they came from; they are often the cheapest next check.

## Next checks

Every top risk ends with the cheapest observation that would confirm or clear it, with the threshold that settles it:

- **Read more code or configuration**: when the evidence is one file away.
- **Query production data or metrics**: counts, sizes, latencies, error rates, lag.
- **Measure on a copy**: a load test or a timing of one query, on realistic data.
- **Drill**: restore a backup, kill a process, fail over, in a safe environment.
- **Inject a failure**: slow down or cut off one dependency in a test environment and watch the scenario.
- **Ask a person**: for what only they know, such as a contract term or an incident nobody wrote down.

Write where the check runs, so nobody runs a destructive drill in production by reading the study, and what result settles it either way: "Restore last night's backup into a scratch database; cleared when the restore completes in under an hour and row counts match."

## When nothing needs to change

Sometimes the honest finding is that the architecture is fine for the question asked. Say so when:

- every priority scenario is `met` with evidence, and the passes found nothing above minor; or
- the risks found sit inside one element and are fixed in its code or configuration (a timeout, an index, a limit), or are operational (a drill, an alert, a runbook); or
- the problem the person described is not caused by the architecture at all: a slow query, a missing index, a process gap.

Write it as one plain sentence in the study, with the reasons tied to the scenarios, and name the non-architecture change each finding needs. Do not add findings to make the review look thorough; "no material finding within the reviewed scope" is a result, as long as the study says what the scope was. When the person proposed an architecture change, say what it would cost to add (a store to run, a failure mode, a boundary) for no gain on the traced scenarios.

## The annotated view and the failure sequence

Both are view files inside the study folder, written in the view format with the view template.

**The annotated view.** Copy the standing view on which the top risks sit, usually containers or deployment, to `<view>-risks.md` in the study folder. Keep every id, node, arrow and class line. Then mark the risks:

- On an element at risk, replace the label's second line with its risk ids and two or three words: `api["<b>API</b><br/>R2 R3: unbounded list"]`.
- On an arrow at risk, start its label with the risk id: `-->|"R1: no timeout"|`.
- Add no new kind of node and no `style` or new `classDef` lines; the risk ids in the labels, and the table below the diagram, carry the annotation.

The view sentence says it shows where this review's risks sit: "This view helps the team answer where the risks of this review sit about Larder's containers as built." The view keeps `Status: built` when its elements are built, without the Verified part unless you checked the whole view against the code just now. The Elements table keeps the evidence and names the risks in the Responsibility cell. In the study, link it and add a compare link with the standing view first, so a reader sees the plain and the annotated view side by side; the compare link form is in the view conventions.

When no standing view covers the elements the risks sit on, draw the annotated view from the code you read, with evidence on each row or `assumed`, and say so in the study.

**The failure sequence.** For the top risk where order matters (a crash between two steps, a race, a retry storm, a timeout chain), draw a `sequenceDiagram` that starts on the normal path, shows the failure at the step where it happens, and continues to what the user or operator sees and how the system recovers, or does not. Use the element ids as participants, notes for timings and conditions, and an `alt` block for the paths that diverge. Name it after the standing runtime view it varies, then the failure, such as `runtime-sync-api-restart.md`, or `runtime-<topic>-<failure>.md` when there is no standing runtime view.

When order adds nothing to any top risk, because each is a capacity limit, a missing check or a data exposure that holds in every order, write one sentence in the study saying so and why, instead of drawing a sequence nobody needs.

## Saying the uncomfortable thing

The person asked for a critical look; softening the findings withholds what they asked for. When the evidence shows that their proposal adds risk, that a decision on record no longer holds, that a promise in the product's own copy is not kept today, or that the problem is not architectural, write it plainly, as the first sentence of the finding, with the evidence beside it. Keep the tone factual and the claim bounded, and leave the decision with them.
