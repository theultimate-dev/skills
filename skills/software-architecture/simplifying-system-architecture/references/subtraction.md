# Subtraction

How to tell which parts of a system can go, which must stay, and what a removal really costs. Every judgement in a simplification study rests on this file: the guarantee test for each part, the line between essential and accidental complexity, the cost of each technology in operation, where complexity hides after a removal, what published simplifications teach, and how to write the answer when the answer is that nothing should change.

The examples use Larder, a fictional household pantry app: a web client, a mobile client, an API and one Postgres database, with whatever extra parts each example needs.

## Contents

1. [Fewer boxes is not the goal](#fewer-boxes-is-not-the-goal)
2. [Essential and accidental complexity](#essential-and-accidental-complexity)
3. [The guarantee test](#the-guarantee-test)
4. [Guarantees and where they hide](#guarantees-and-where-they-hide)
5. [Re-homing a guarantee](#re-homing-a-guarantee)
6. [The cost of a technology in operation](#the-cost-of-a-technology-in-operation)
7. [Where complexity hides after a removal](#where-complexity-hides-after-a-removal)
8. [What to measure before trusting the change](#what-to-measure-before-trusting-the-change)
9. [Published cases and what does not transfer](#published-cases-and-what-does-not-transfer)
10. [When nothing should change](#when-nothing-should-change)

## Fewer boxes is not the goal

A simpler system is one that is cheaper to run, change, debug and staff while it keeps every promise it makes. A diagram with fewer boxes can be harder on all four: a removed queue whose job moved into retry code in three clients has fewer boxes and more complexity. So the study never counts boxes. It counts guarantees kept, and work moved, added and removed.

Two errors are equally real, and the study guards against both:

- **Removing a part that carries a guarantee.** The part looks like overhead because its value only shows on a bad day: when a process dies, a provider is down, a phone comes back after a week. The diagram shows the box; only the code and configuration show what it does on that day.
- **Keeping a part that carries nothing,** or proposing work to look useful. A part that forwards requests unchanged, a cache in front of an indexed read, a store nothing reads: each costs something every week. And when nothing in the system is removable, inventing a change to justify the study costs the person a migration for nothing.

## Essential and accidental complexity

Brooks separated the difficulty that belongs to the problem (essential) from the difficulty we add while solving it (accidental). In a system's architecture:

- **Essential** complexity follows from a scenario or a hard constraint: the product promises that a reminder still goes out when the push provider has a bad hour, so something must hold the reminder and retry; it promises search results within 300 ms for a household of 3,000 items, so something must index item names; personal data must stay in the EU, so every store that holds it must run there. It can move, but it cannot disappear from a drawing without a promise breaking.
- **Accidental** complexity follows from history, fashion, a team that no longer exists, a speculative need, or a mechanism that duplicates another. It can go.

Tell them apart from evidence, never from names or from how the part looks:

| Sign | Points to | Check |
|---|---|---|
| A product promise, a contract, a decision record or a test names the behaviour the part provides | Essential | Quote the promise and the line of code that keeps it |
| The part's configuration is tuned for a guarantee: fsync on every write, acknowledgement after commit, a retention period, a consumer group, a retry schedule, a dead-letter, `FOR UPDATE SKIP LOCKED` | Essential, most likely | Trace which scenario that setting serves |
| The part forwards, copies or renames without changing anything a caller relies on | Accidental, most likely | List every header, check, limit or transformation it adds, and every caller it has |
| Two mechanisms provide the same guarantee (two retry layers, two caches, two places that validate the same input) | One of them accidental | Find which one the scenarios actually depend on |
| A part serves a need that is hypothetical: "in case we need to scale", "for a future partner API" | Accidental now | YAGNI test below |
| Nobody can say what the part is for, and the code shows no guarantee | Unknown, not accidental | Ask, and look for consumers outside the repository |

**The YAGNI test** (Fowler) sorts a part that serves a future need into three: needed now; needed later and slow to add then (a data migration, a public contract, a store that must hold history from day one); hypothetical. Only the hypothetical one is accidental today, and only after you check that adding it later stays feasible. A ten-year horizon is not by itself a reason for several services, a plugin system or multi-region writes today.

**Names mislead.** A "queue" may be a durable log that devices replay from; a "cache" may be the only copy of some data; a "gateway" may do nothing; a "worker" may be the only thing that keeps writes in order. Judge each part by what its code and configuration do, and say in the inventory when its name suggests otherwise.

## The guarantee test

For each component, hop, store and technology on the inventory, ask two questions and answer them from the code and configuration:

1. **If it were removed, what would break?** Walk each scenario and constraint through the system without the part. What happens on the normal path, and what happens on the bad day each scenario describes? Name the scenario or constraint that fails and the line of code or configuration that shows why.
2. **If it were merged with a neighbour, what would break?** Merging two deployables into one, two stores into one, or a hop into the element on either side. What does the separation give today: independent release, isolation from the neighbour's failure or load, a different trust boundary, independent scaling, a different technology the neighbour cannot provide?

Write the answer as a guarantee with its evidence, in a few words: "holds each reminder until the push provider accepts it (`notifier/src/queue.ts:21`)", "keeps item search under 300 ms by indexing names (`search/src/index.ts:8`)". A guarantee named only from the part's type ("queues give decoupling") is not an answer: it must be what this part does here. State it as what a caller or a promise can rely on (a bound, a count, a behaviour on the bad day), not as the mechanism that gives it today ("the answer does not wait for the apply", "a second process"). Then a new mechanism that still meets the same bound is a re-homing, checked by a measurement, and not a guarantee given up.

Each part ends with one of three findings:

| Finding | Meaning | What follows |
|---|---|---|
| Carries `S2`, `C1` | A scenario or constraint depends on a guarantee this part gives | It stays, or it goes only with every such guarantee re-homed and the cost counted |
| Carries a guarantee no scenario names | It gives something real (ordering, an audit trail, a public URL old clients use) that the intake did not list | Treat the guarantee as kept. Add it to the scenario table as a row of its own, or ask the person whether anyone relies on it. Dropping a guarantee is the person's decision, never the study's |
| Carries nothing | You checked for each kind of guarantee below and found none, and nothing outside the repository calls it | A removal candidate. Write what you checked, because "carries nothing" is a claim about absence and needs its evidence too |

**Look outside the repository before you call a part unused.** Old mobile app versions stay in the field for months and keep calling the URLs they shipped with. A dashboard, a partner, a support script or a scheduled export may read a store or call a host. The repository cannot show all of these; where a removal depends on there being no other caller, write that as an assumption with the observation that would confirm it (access logs by caller over a week, the store's connection list, the app versions still in use).

## Guarantees and where they hide

| Guarantee | What it means | Where the evidence usually sits |
|---|---|---|
| Durability of accepted work | Once the system says yes, the work survives a crash | The order of "write" and "answer" in the handler; fsync, replication or append-only settings; a transaction committed before the response |
| Replay and catch-up | A client or consumer can read what happened after a point it last saw, in order, including what was deleted | Retention settings, cursor or offset parameters, "read after id" queries, a log table kept for N days, a fallback when a cursor is older than the history kept, a feature that shows a returning user what changed |
| Ordering | Changes are applied in the order they were accepted | A single consumer, a partition key, a sequence column, an "apply in order" loop |
| Idempotency, an effect applied once | A retried or redelivered request changes state once | A table of applied ids, `ON CONFLICT DO NOTHING`, an idempotency key header |
| Delivery despite a downstream outage | Work reaches a provider that was down for a while | An outbox table, a retry schedule with backoff, a maximum attempt count, a dead-letter |
| A latency bound | The caller's answer does not wait for slow work | Work handed to another process or a table before the answer; timeouts on outbound calls |
| Failure isolation | One part failing or overloading does not take another down | Separate processes, pools, instance counts, circuit breakers, bulkhead limits |
| Independent release | One part ships without shipping or retesting another | Separate build and deploy entries, versioned contracts between them |
| Independent scaling | One part scales without the others | Separate instance counts, autoscaling rules |
| A trust boundary | Secrets or personal data stay on one side | Which process holds which credential; network rules; which part sees which data |
| A stable address | Clients that cannot be updated keep working | Public hostnames, DNS, URLs compiled into shipped apps |
| Compatibility | Old and new clients or schemas work side by side | Version prefixes, adapters, translation layers |
| Back-pressure | A burst is absorbed instead of failing callers | Queue length limits, `noeviction` policies, rate limits |
| Auditability | Someone can tell later who changed what | Append-only tables, change logs kept past their technical need |

Read the tests' names too: they often state a guarantee nobody wrote down, such as "applies a redelivered change once".

## Re-homing a guarantee

A part that carries a guarantee can still go when another element takes over the guarantee and the result is cheaper overall. Re-homing is a design change, so treat it like one:

1. Name the new home for each part of the guarantee, not only for its headline. Replay, for instance, is a cursor, an order, a retention period, deletes kept as tombstones so a reader learns what was removed, an idempotency key, and the fallback for a cursor older than the history; a design that re-homes four of these breaks the fifth. Name the element and the mechanism for each. "Item search moves from the Meilisearch service to a trigram index on `items.name` in Postgres, queried by the API."
2. Write what the new mechanism needs that the old one gave for free: an extension to enable, an index to build without blocking writes, typo tolerance written as a query, a period where both answer.
3. Re-trace every scenario the guarantee served through the new home, on its bad day: does the new home hold under the same failure?
4. Count its cost with the next two sections, in the same terms as the part it replaces.
5. Show it in the after view as `proposed`, with the same ids for every element that stays.

When a candidate keeps every guarantee but one, it is not a proposal: list it under "Considered and rejected" with the guarantee it would give up and the scenario that depends on it. Whether that guarantee is still needed is the person's decision; when they drop it, the study is re-run against the new scenarios.

When the guarantee can be re-homed in more than one reasonable way and the choice between them is the real question, the study names the choice and hands it on as an options question rather than choosing silently.

## The cost of a technology in operation

Every technology the system runs costs in four ways, and most of the cost comes after it is chosen:

| Cost | What to count | Larder example |
|---|---|---|
| To run | Instances, plans and disks in the deployment configuration; backups and their restore drills; alerts and dashboards; secrets to rotate; local development setup; CI services | A Meilisearch service on its own plan with its own disk, its own health check, its own API key, its own container in the local stack |
| To upgrade | Major versions per year; security patches; client library upgrades in every caller; data migrations an upgrade forces | A Meilisearch major version needs a dump and a reload of the index; Postgres has its own upgrade path beside it |
| To debug | Failure modes someone must know; logs and traces that must be correlated across it; tools needed to inspect it | An index out of step with the database after a failed update, a rebuild that slows writes: each needs its own knowledge at 3 a.m. |
| To staff | People who understand it well enough to be on call; time for a new engineer to learn it | One developer on call must know Node, Postgres and Meilisearch, not only Node and Postgres |

McKinley's "Choose Boring Technology" frames this as a small budget of technologies whose failure modes a team can afford to learn: each new one spends part of it, and a well-understood one costs less than its feature list suggests. Two consequences for the study:

- **A technology earns its place by removing more complexity than it adds.** Postgres, already run, can often take a job a second store does (a queue table, a log, a lock) at little added cost; a second store adds all four costs above.
- **Fees are rarely the largest cost.** When the person raises running cost, take the figures from the deployment configuration (plans, instance counts, disk sizes) or from the person, and say which; never estimate a bill you cannot see. Then add the other three costs, which usually decide.

Count costs for the before and the after in the same terms, so the comparison is honest. A number of technologies, deployables or hops is a fair proxy; a "complexity score" is not, because it hides what was counted.

## Where complexity hides after a removal

Complexity that follows from a guarantee moves; it does not vanish. After each proposed removal or merge, look for it in these places and count what you find in the study's "Where the complexity moved" table:

| Removed or merged | Where the complexity tends to go |
|---|---|
| A queue or stream | Retry and backoff logic in every producer; a dual write while both run; a polling loop; a log table with its own retention job; lost ordering, now enforced by locks |
| A separate service, merged into another | A shared deployable with a larger blast radius; a shared database table that couples two modules; one release train for both; a background loop inside a web process that now competes for its resources |
| A cache | Slower reads and a larger database instance; or nothing, when the read was cheap |
| A gateway or proxy | Configuration in the API: CORS, request ids, rate limits, TLS; DNS changes; client configuration for every client version, including the ones in app stores |
| A second store | A data migration; constraints the old store enforced, now in application code; a larger backup |
| A framework layer or abstraction | Code that was generated or shared, now written in each place that needed it |
| Any of them | The transition itself: a migration, a period running both, a drain, a rollback path. Count it as a one-off cost beside the lasting one |

Also look in places no diagram shows: runbooks a person must follow, deployment scripts that grow conditions, monitoring that must now watch a new failure, and knowledge one person holds. If the complexity moved into one of these, it still counts.

Write the net result plainly: what is gone for good, what is added for good, what is a one-off. A removal whose added work is close to what it removes is not worth a migration; say so.

## What to measure before trusting the change

A simplification rests on assumptions the code cannot settle: real traffic, real latencies, who else calls a host, how long devices stay offline. Before the change is trusted, name the few measurements that would show it is safe, each with the threshold that settles it both ways:

- **The riskiest assumption first.** The one that, if wrong, breaks a scenario: "no caller other than the two first-party clients reads the search service: its access logs by caller for 7 days show none".
- **Each scenario whose mechanism changed,** measured on the new path: the latency bound at the 95th percentile with the work now in the database, the time a returning client needs to catch up through the new mechanism, the write load on the database with the removed store's writes added.
- **A failure drill where a guarantee was re-homed:** kill the process mid-write, take the provider down, restore the store from backup, and check the scenario's measure.

When a comparison on paper cannot settle the question, propose a spike: the smallest experiment that would, with how long it takes and what result would change the recommendation.

## Published cases and what does not transfer

Simplification stories travel well and transfer badly. Use them for their method, never as proof that a removal is safe here.

- **Segment, "Goodbye Microservices" (Alexandra Noonan, 2018).** Segment's delivery pipeline had grown to one queue and one service per destination, with shared libraries that each service pinned at a different version; upgrades and operations became the bottleneck. The team moved to one service and a stronger test suite, and the write-up names what that cost, including the loss of isolation between destinations. What transfers: find the operational or change bottleneck, change the mechanism responsible, and name the guarantee given up. What does not: their scale, their number of destinations, their team; it is evidence about one pipeline, not about microservices. <https://www.twilio.com/en-us/blog/developers/best-practices/goodbye-microservices>
- **Shopify's modular monolith (Kirsten Westeinde, 2019; Philip Müller, 2020).** Shopify kept one codebase and one deployable and invested in enforced module boundaries and ownership, reaching them step by step rather than at once. What transfers: modularity and the number of deployables are separate decisions, so a merge can keep a boundary as a module boundary. What does not: the tooling and team size behind their enforcement. <https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity>, <https://shopify.engineering/shopify-monolith>
- **"No Silver Bullet" (Fred Brooks, 1986)** for essential and accidental difficulty; **"Yagni" (Martin Fowler)** for speculative capability; **"Choose Boring Technology" (Dan McKinley, 2015)** for the cost of each technology in operation. <https://martinfowler.com/bliki/Yagni.html>, <https://mcfunley.com/choose-boring-technology>
- **Stories retold without their source,** such as a famous cost saving from merging services, carry their headline number without its context. Cite a case only from a first-party write-up you could read, and never carry its numbers into a study as if they applied here.

In a study, a published case is at most one sentence under the proposal it resembles, with what transfers and what does not. The evidence for a removal is always this system's code, configuration and measurements.

## When nothing should change

"Nothing should change" is a full result, and on a system that is already as simple as its promises allow it is the right one. It is useful only when it is written so the next person who asks the same question can check it instead of repeating the study. Write it with:

1. **The answer in one sentence,** at the top of the study's Result: "Nothing should change: every part carries a guarantee a scenario or constraint depends on, and no merge keeps them all for less."
2. **Each scenario and constraint with the mechanism that carries it,** in the scenario table, so the reasons are tied to promises rather than to taste.
3. **The parts that look removable and why each stays:** the guarantee, the scenario it serves, the evidence. These are the answers people will want next time; a part that looks like overhead is the most important row of the study.
4. **What was checked:** the parts inventoried, the files and configuration read, at which commit.
5. **What would change the answer:** the condition under which a part would become removable or a merge worthwhile, such as "if reminders stop being promised during a push provider outage, the reminder table and its retry loop could go" or "if a second team takes over the web client, a separate deployable starts to pay".
6. **Improvements inside one element,** if the inventory found any, listed as ordinary code work and kept apart from the architecture answer, so they do not look like reasons to change the architecture.

No proposal, no after view, no decision record to write, and no work invented to make the run look productive. The before view and the inventory are the record.
