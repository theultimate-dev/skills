# Generating approaches

How to research, produce approaches that genuinely differ, judge them on one scale, and decide what needs the user. Effort is counted in PR slices; a PR slice is the work that becomes one pull request (merge request).

## Contents

- Research discipline
- Use external evidence selectively
- Axes of distinctness
- The strawman check
- Scoring the criteria
- Decisions that need the user
- Example: persistence behind a prototype
- Spikes
- Briefing parallel drafters

## Research discipline

Start where the spec's behavior enters the code. Follow its state, dependencies, and failure handling, and read the tests alongside. Then widen to prior art:

1. Search code, tests, and migrations for the spec's domain words ("cancel", "refund", "export").
2. Find the closest existing feature and read it end to end: routing, validation, persistence, jobs, notifications, tests.
3. List the utilities, services, and components you can reuse, with their paths.
4. Read the git history of the modules you will touch: recent churn, reverted attempts, and the reasons given in commit messages.
5. Read the decision log and AGENTS.md or CLAUDE.md for rules that settle a choice.

Record each finding as a fact with its path. Every approach that departs from prior art states why. Never imply that an experiment ran because an example looked plausible.

## Use external evidence selectively

Research when an unresolved technical question changes feasibility or the plan. Prefer official documentation, source code, standards, or original research. Record the URL, retrieval date, version and applicability, the finding, and its implication. Known solutions are options with trade-offs, not permission to copy their architecture wholesale.

Distinguish a source's claim from your inference and from a tested local observation. Conflicting or inaccessible sources leave uncertainty: say so rather than pick the convenient one. Do not include credentials, irrelevant private code, or whole external documents in delegated context.

A documentation lookup tool (a docs MCP server such as Context7, the vendor's documentation, the package source) answers version-specific API questions more reliably than general web search.

## Axes of distinctness

Two approaches are distinct when they differ on an axis that changes the architecture, the risk, or the cost. Choose the two or three axes where the spec's constraints bite. Skip every axis the codebase or an accepted decision already settles.

| Axis | Typical positions | What it changes |
|---|---|---|
| Where the logic lives | Client, server, database (constraint, trigger, view), edge, background job | Latency, trust, duplication, testability |
| Build, buy, or reuse | Extend an existing module, add a library, use a hosted service, write new code | Dependencies and cost, control, time to the first slice |
| Sync vs. async | Inside the request, a queued job, an event consumer, a scheduled batch | Failure handling, user feedback, ordering, retries |
| Data model | New table, new columns, a JSON field, derived on read, an event log | Migration, query cost, reversibility |
| Rollout | Incremental behind a flag, strangler, parallel run, big-bang | Risk per PR slice, how long two code paths coexist |
| Client vs. server state | Server-rendered, a client store, URL state, local storage | Consistency across devices, offline behavior, complexity |
| Push vs. pull | Webhook, polling, subscription or websocket | Freshness, load, operational burden |
| Consistency | Transactional, eventual with reconciliation | Correctness guarantees, throughput |
| Generality | Specific to this feature, a reusable mechanism | Effort now vs. later; the risk of an abstraction nobody reuses |
| Boundary | Inside an existing module, a new module, a separate service | Ownership, deploy coupling |

## The strawman check

Ask of each approach:

1. In what situation is this the best choice? When no situation is plausible for this project, drop it.
2. Does it meet every AC? When it misses one, name the AC and why. Choosing it would change the spec, which is a G1 question.
3. Is it described at the same depth as the others, with effort and reversibility on the same scale?
4. Does it differ from another approach only by a name or a library brand? Merge the two.

Two approaches that survive beat four that include two strawmen. When only one survives, say so and ask for a one-line confirmation.

## Scoring the criteria

| Criterion | Ask | Write |
|---|---|---|
| Fit | Does it follow the patterns, boundaries, and conventions the code already has? | "Follows [pattern] ([path])" or "Departs from [pattern] because [reason]" |
| Risk | What could go wrong: data loss, a security exposure, a performance cliff, unknown library behavior, a hard migration? | The top one or two, each with what would expose it early |
| Effort | S: one PR slice. M: one plan with several phases. L: several plans | The size and what drives it |
| Reversibility | Easy: a flag or config undoes it. Moderate: a code change undoes it, and no data or contract moves. Hard: undoing needs a data migration, a public-contract change, or an external commitment | The level and the cost of undoing |

When two approaches fit equally well, recommend the more reversible one: it lets the user learn before committing.

## Decisions that need the user

Typical consequential decisions change persistent data ownership, public contracts, deployment or platform commitments, security boundaries, major dependencies, cost structure, or a product trade-off. Show the concrete proposal before asking. Do not substitute repeated approval of routine local details for these decisions.

An existing agreed architecture can settle a choice. Explicit user delegation can settle who decides it. State the actual basis, and never label an assumption agreed. When a change would invalidate an earlier agreement, show what changed and request only the affected decision.

Separate blockers from bounded uncertainty. A missing API contract that two parallel plans depend on blocks both of them. The name of a private helper does not. Record small reversible details as implementation choices within the approach instead of forcing them into G2.

A product trade-off found here, such as an AC that no reasonable approach meets at an acceptable cost, is not a technical choice. Take it back to G1 with the evidence.

| Choice | Decision record |
|---|---|
| A new table this feature owns | Yes: persistent data ownership |
| A new public endpoint or a changed response shape | Yes: public contract |
| A new or major-bumped dependency | Yes: major dependency |
| Moving authorization checks from handlers into middleware | Yes: security boundary |
| A new hosted service, region, or paid tier | Yes: platform commitment and cost |
| Reusing an existing module's function | No |
| A private helper's name or file placement | No |
| A feature flag for the rollout | No, unless the flag system itself is new |

## Example: persistence behind a prototype

The product handoff says saved entries remain available after a reload, while the prototype holds them in memory. Inspect the existing storage and identity model first. If the application already has an agreed authenticated storage service, plan within it: one sensible approach and a one-line confirmation. If no storage exists, present viable persistence and identity options, their data and operational consequences, and a recommendation. The prototype's local array cannot silently become the production storage decision.

Suppose the app has sessions and a relational database with migrations, and the spec says: "AC2 (R1): entries saved on one device appear after signing in on another." The comparison reads:

| Approach | Fit | Risks | Effort | Reversibility | Meets all ACs |
|---|---|---|---|---|---|
| A: A table in the existing database, behind the current session auth | Follows the `users` table and its migrations | The schema is hard to change once entries exist; exposed early by checking it against every AC before the first migration | M | Hard: data ownership | Yes |
| B: A hosted document store | A new dependency and credentials | Vendor coupling and a new bill | M | Hard: external commitment | Yes |
| C: Browser local storage | No server change | Entries are lost when site data is cleared | S | Easy | No: fails AC2 |

C appears only because the prototype implies it, and it is marked as failing AC2. Choosing it would change the spec, so it is a G1 question, not a G2 option.

Recommendation: A, because the app already has sessions and migrations, and B adds a vendor for data the existing database holds without strain. B wins only when the data outgrows the relational model, which nothing in the spec suggests. A fixes persistent data ownership, so it gets a decision record.

## Spikes

Run a spike when a feasibility question separates the approaches and neither the code nor a primary source answers it. Examples: whether a library handles the file sizes in the spec, whether the payment provider's test mode supports partial refunds, whether a query stays fast at the stated volume.

| Part | What to state |
|---|---|
| Question | One question, answerable with yes, no, or a number |
| Timebox | In hours, agreed with the user |
| Commit and push | Asked in the same question as the timebox: may the agent commit and push the spike branch? Without a yes, nothing is committed or pushed, and the finding cites files and commands instead of a commit |
| Environments | Local services and provider test modes, or the environments the verification profile allows. Never production, real email, payments, or webhooks |
| Exit | The observation that answers the question |
| Mapping | Which answer points to which approach |
| Branch | Follow the project's naming; otherwise `spike/<work-item-slug>-<topic>`. Never merged, never opened as a PR for merge |
| Finding | The answer, with the command and output that support it, the branch, and the commit. A standalone spike writes it to `docs/product-engineering/<slug>/spike.md` on the spike branch |

A standalone spike needs no spec: its question comes from the request. After the finding, stop and offer a work item whose G2 uses it.

Spike code is throwaway. Anything worth keeping is rebuilt under the chosen approach, with its tests, during implementation.

## Briefing parallel drafters

Give each drafter the same brief with a different position held fixed:

```text
Spec: [path to spec.md]. Research notes: [facts with paths].
Draft one technical approach that meets every acceptance criterion, holding this fixed: [axis position, e.g. "all logic stays on the server"].
Return, in this order: a short name; how it works in 2–4 sentences; the files and modules touched; fit with the existing architecture; the top risks; effort (S, M, L); reversibility (easy, moderate, hard); the situation in which it is the best choice.
Do not edit files.
```

When the drafts come back, merge duplicates, run the strawman check, and put the survivors in one table. Drafters that converge on the same design are evidence that there is one sensible approach.
