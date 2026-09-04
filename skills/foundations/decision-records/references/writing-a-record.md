# Writing a record

## When a decision deserves a record

Ask: would a competent newcomer, or an agent working here next month, plausibly undo or re-argue this without knowing the reason? If yes, record it. Typical yes: a dependency or platform choice, a data model or API shape, a process rule (branching, releasing, review), a deliberate rejection ("we will not add a message queue"), a security or privacy trade-off. Typical no: formatting, a variable name, a config value nobody debated.

Record decisions, not plans or tasks. "Migrate to Postgres by Q3" is a plan. "Use Postgres for the event store" is a decision, with the migration among its consequences.

## The four sections

**Context.** The forces at play, stated neutrally: constraints, requirements, what is known, what hurts today. No arguing yet. Two to five sentences is usually enough. Write it so the reader could have made the decision from it.

**Options.** Every option seriously considered, numbered, the chosen one included. One or two lines each: what it is, and why it won or lost. A record with one option is a note, not a decision; if there was truly no alternative, say why in Context and keep Options to two lines.

**Decision.** What was chosen, in the first sentence. Then the rules that follow: names, paths, formats, limits. Concrete enough that two people would implement it the same way.

**Consequences.** What becomes easier, what becomes harder, what must now be done, what to revisit and when. Include the costs. A record with only upsides is not believable.

## Shape

- File `NNNN-kebab-title.md`, next free number, four digits. Never reuse a number, even for a withdrawn proposal; mark that one deprecated instead.
- Title as the decision itself: "Use Postgres for the event store", "Ship releases from tags on main". Not "Database", not "Release process".
- Head lines: `- Status: accepted`, `- Date: YYYY-MM-DD` (the date the status was set). Add `- Supersedes: NNNN` or `- Superseded by: NNNN` only when they apply. `- Deciders:` is optional and useful when more than one person decided.
- One page; two at most. Longer means the Context is arguing or the Options are essays.
- Plain sentences. No marketing, no hedging. The reader is technical and busy.

## Status lifecycle

- `proposed`: written, not yet agreed. Edit freely.
- `accepted`: in force. The decision text is frozen from here on. Fix typos and dead links, nothing else.
- `deprecated`: no longer applies and nothing replaces it (the feature was removed, the constraint disappeared). Add a dated line under the head saying why.
- `superseded`: replaced by a newer record. The old record gets `- Superseded by: NNNN` and the new status; the new one gets `- Supersedes: MMMM` and, in its Context, one sentence on what changed since.

Every status change is mirrored in the index row.

## Superseding versus amending

If the decision changes, supersede. If only the Consequences turned out different (a cost was larger than expected) and that changes what people should do, supersede as well. If it changes nothing about what people should do, a short dated "Outcome" note appended under Consequences is acceptable. Never rewrite Context or Options to make the old decision look better or worse than it was.

## Common mistakes

- Recording after the fact with options reverse-engineered to favour the outcome. Write the options as they were seen at the time.
- One record per meeting instead of one per decision.
- Consequences that restate the decision. A consequence is something that will now happen or must now be done.
- Linking to chat threads or tickets as the only explanation. Summarise in the record; links go stale.
- Numbering by date or category. Sequential numbers only; the index carries the rest.
