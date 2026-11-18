---
name: simplifying-system-architecture
description: "Simplifies a system's architecture without breaking what it promises, or shows that nothing should change: writes a dated simplification study at studies/YYYY-MM-DD-slug/README.md (context/architecture/ by default) from templates/simplification.md, with the guarantee each component, hop, store and technology gives, before and after views with the same element ids, a table showing each scenario and constraint still holds, where each removed guarantee now lives, where the complexity moved and what to measure first, then records the person's accept, narrow or decline. Asks of each part what breaks if it is removed or merged, and proposes only changes that keep every guarantee. Use when the user says can this be simpler, this feels too heavy, can we drop the queue, do we need this service, or can we merge these. Not for refactoring code inside one module, a critical look at risks (evaluating-architecture-risks), or comparing new designs (exploring-architecture-options)."
license: MIT
---

# Simplifying system architecture

Answers "can this be simpler?" for a system that feels heavier than its job: many services, stores, hops or technologies, slow changes, a high running cost. The answer is a dated study that tests every part against the guarantees the system must keep, proposes only the removals and merges that keep all of them, and counts where the complexity goes, because complexity that follows from a promise moves rather than disappears. A removed queue may come back as retry logic in every client.

Two answers are uncomfortable and both are often right. The part the person wants to remove may be the one that keeps a promise on the bad day, and then it stays. And the system may already be as simple as its promises allow, and then the study says "nothing should change", with its reasons, and invents no work to justify the run. A study that proposes nothing and shows why is a complete result.

## Where the work lives

[The view conventions](references/view-conventions.md) give the location rule, the folder tree, the view format, statuses, element ids, evidence, the Mermaid subset and quoting, and the link forms. Read them before you write. A simplification study is a study: `studies/YYYY-MM-DD-<slug>/README.md` in the architecture folder, with `Kind: simplification study` in its header line, beside its own views: `<view>-before.md`, a copy of the standing view it compares, and `<view>-after.md`, the proposed design with the same ids.

The study reads the standing views and the decision log and edits neither while the person has not answered, because a standing view records only what is built or agreed. The one shared file it changes before the answer is the index `README.md`, which gains the study's row in its Studies table.

## Situations

| Situation | What to do |
|---|---|
| Standing views exist | All the steps below |
| The person names a removal or merge ("can we drop the queue?") | Restate the question without it (step 2) and test it as proposal `P1`. Still inventory every part at that view's level (step 3): the person's aim, less to run, may be met by a part they did not name |
| No views, or views with little evidence | Work from the code. Draw the current design inside the study as `<view>-before.md`, from the code, with evidence on every row. List what you could not evidence under Assumptions, and name `recovering-built-architecture` in the report |
| A product context repository holds the architecture | Write no standing view there. Write the study in the code repository by the location rule, and hand it over as input to that repository's architecture work |
| An earlier simplification study of the same system | Read it and re-check every claim you rely on against the code, because code moves and a study keeps its date. Write a new study |
| The aim is lower running cost | Add cost as a constraint or a scenario with a measure, taking figures from the deployment configuration or from the person, never estimated |

## Steps

1. **Read first.** Open the repository's `AGENTS.md`, the decision log's index and every record that touches the parts in question, the architecture index, the standing views, and earlier studies. Then read what the product promises (README, help pages, store listings, terms) and the code and configuration of every part: deployment manifests, entry points, process commands, the settings of each store and queue, schema, tests. Note the element ids in use. A part's value usually shows only on a bad day, and only the code and configuration show what it does then.

2. **Run the intake.** Follow [the scenario intake](references/scenario-intake.md): the real question restated without the removal the person named, three to five priority scenarios with all six fields, hard constraints, facts apart from assumptions and proposals, and what is already decided. Here the scenarios are the guarantees to keep: draw them from the product's promises, include at least one failure scenario (a process killed, a provider down, a client offline), and add the reason the system feels heavy as a change or cost scenario when the person gave one. Ask the person only what the repository cannot answer, in one message with a default for each question. Write the intake at the top of the study, under the title and the header line; nothing that judges goes above it.

3. **Inventory every part and the guarantee it gives.** One row for each component, hop, store and technology at the level of the view in question (usually containers), in the study's Inventory table. For each, ask the two questions of [the guarantee test](references/subtraction.md#the-guarantee-test): what breaks if it is removed, and what breaks if it is merged with a neighbour? Name the guarantee it provides here (replay, ordering, durability before the answer, isolation, independent release, a latency bound, delivery despite an outage, a trust boundary, a stable address), with the line of code or configuration that shows it. Judge by what the code does, not by the part's name: a "queue" may be a log that clients replay from, a "gateway" may forward requests unchanged. A guarantee named only from the part's type is not an answer.

4. **Sort each part.** It carries a scenario or constraint (it stays, or goes only with every guarantee re-homed); it carries a guarantee no scenario names (the guarantee is kept: add a row for it, or ask whether anyone relies on it, because dropping a guarantee is the person's decision); or it carries nothing, which is a claim about absence, so write what you checked, including callers outside the repository such as app versions still in the field. [Essential and accidental complexity](references/subtraction.md#essential-and-accidental-complexity) gives the signs.

5. **Propose only what keeps every guarantee.** For each candidate, a removal or a merge with its id (`X1`): the guarantees it touches, where each one lives afterwards (the element and the mechanism), and its cost in operation before and after, to run, to upgrade, to debug and to staff, as [the cost of a technology](references/subtraction.md#the-cost-of-a-technology-in-operation) describes. A part that looks like overhead and carries a guarantee stays, or is replaced only with every guarantee re-homed and that cost counted. Keep each proposal acceptable on its own where you can, and say which depend on each other, so the person can narrow. Test the named proposal `P1` the same way and say plainly whether it survives, is narrowed, or is rejected and which guarantee it would break. When a guarantee could be re-homed in more than one reasonable way, name that choice and hand it on rather than choosing silently.

6. **Re-trace every scenario and constraint** through the design after the proposed changes, element by element, on the scenario's bad day as well as the normal path, and every guarantee no scenario names. One row each in the scenario table: holds or not, the mechanism that carries it after, and the evidence or the assumption it rests on. For each scenario with a time or a count as its measure, and each one that ends in a state the source must see, write a trace ledger through the design after the change, as the intake's "The trace ledger" describes, from the source's first action to what its own device shows; where the same ledger through today's design already misses the measure, say so, because a proposal cannot be said to keep what does not hold today. A row holds only when it holds under the proposal as you would default it, its cutover included, as the intake's "When a scenario counts as met" describes: where a default gives up part of a promise even once, such as one lost summary at cutover, either change the default to the route that keeps it and count that cost, or mark the row as not holding and hand the loss to the person as their decision. A proposal under which any row fails is dropped, or narrowed until every row holds. One that keeps every guarantee but one goes under "Considered and rejected" with the guarantee it would give up: dropping a guarantee is the person's decision.

7. **Count where the complexity went.** For each proposal, look where [complexity hides after a removal](references/subtraction.md#where-complexity-hides-after-a-removal): retry logic in clients, a dual write, a background loop, a shared table, configuration moved into a neighbour, a runbook step, the migration itself. Fill the table with what is gone for good, added for good and one-off, and write the net in one sentence. A proposal whose added work is close to what it removes is not worth a migration: drop it and say why.

8. **Decide the result.** Either the proposals that survived steps 5 to 7, or "nothing should change". When nothing survives, write the result as [when nothing should change](references/subtraction.md#when-nothing-should-change) describes: the answer in one sentence, the mechanism behind each scenario, the parts that look removable and why each stays, what was checked, and what would change the answer. Improvements inside one element go in a separate list as ordinary code work.

9. **Draw the views.** Every view follows [the view template](templates/view.md). Copy each standing view whose elements or arrows the proposals change into the study as `<view>-before.md`, and give each its `<view>-after.md`, because the Accept step updates exactly the views the study compared: change only its title, adding "before" to it, and the targets of its Related links so they resolve from the study's folder; keep its Status line, Verified part and rows, which record what was checked and when. With no standing view, draw it from the code (Situations). When a change is proposed, write `<view>-after.md` with the same ids: unchanged elements stay `built`, changed and new elements and arrows are `proposed` with the `proposed` class and dotted arrows, removed elements are absent, and the view's Status is `proposed`. Link both from the study with a compare link, before view first. When nothing should change, draw no after view.

10. **Write what to measure first.** The riskiest assumption first, then each scenario whose mechanism changed, measured on the new path, then a failure drill for each re-homed guarantee, each with the threshold that settles it both ways, as [what to measure](references/subtraction.md#what-to-measure-before-trusting-the-change) describes. When paper cannot settle a question, propose the smallest spike that would.

11. **Write the study and the index.** Fill [the simplification template](templates/simplification.md) at `studies/YYYY-MM-DD-<slug>/README.md`, with the Outcome `waiting for the answer`, or `nothing should change`. Add the study's row to the index's Studies table and change nothing else there; ids that only this study uses stay out of the element ids table until the person accepts. Check every view and link against the conventions' "Before you finish" list.

12. **Rebuild the page.** When the skill `drawing-architecture-views` is available, rebuild `architecture.html` by its steps before you report, with its build script where a shell is available, and read the page's check lines as it describes. When it is not available, leave `architecture.html` as it is, write the views in Markdown only, say in your report that the page was not rebuilt and is out of date, and name `drawing-architecture-views` as the skill that rebuilds it. Say too that the new views have not been drawn: their Mermaid is unchecked until the page is rebuilt and its check lines are read. Ask the person to have the page rebuilt and to read its `DONE` line before they rely on the pictures.

## Gate: Accept

Show the person the result: each proposed change with what it removes, the guarantees it re-homes and where, the net complexity, and what to measure first; or the reasons nothing should change. Ask them to accept, narrow (accept some changes, decline others) or decline. Silence is not acceptance: until they answer, the Accept section says the study is waiting, and nothing outside the study changes.

When they answer, record it as below and then give a short updated report that opens with the current outcome, and correct any saved report that still says the study is waiting:

1. **Record the answer** in the study's Accept section with the date and their words, which changes are accepted and which declined, and set the Outcome (`accepted on`, `narrowed on`, `declined on` and the date) in the header line and in the index row.
2. **Offer a decision record** for the accepted changes, and write it only when the person says yes: in the decision log the location rule found, in that log's own format, or with the parts Title, Status, Date, Context, Decision, Consequences when it has none. Its Context links the study, and its Consequences name the guarantees re-homed and the measurements to run. When the change reverses an accepted record, the new record supersedes it by link; never edit the old one. Record in the Accept section whether it was written.
3. **Update the standing views as a separate step,** for accepted changes only: new elements and arrows go in as `planned`, with the `planned` class, dotted arrows and the decision record or the person's statement as evidence. A part accepted for removal still runs, so it stays `built`; name its planned removal in the view's prose and link the decision under Related, leaving its rows unchanged so the Verified part still holds. Add new ids to the index's element ids table. The study and its views stay exactly as they were: they are the record of why.
4. **Rebuild the page again** (step 12).

When the answer is "nothing should change" and the person agrees, record that answer the same way; there is nothing to plan. When a part stays because of a guarantee nobody had written down, list it in your report as a choice worth recording, so the next person who asks finds the reason.

## Output

- `studies/YYYY-MM-DD-<slug>/README.md`: the intake; the inventory with the guarantee each part gives and its evidence; the proposed changes, or none; the scenario and constraint table; what is removed and where its guarantee lives; where the complexity moved; what to measure first; the result; the Accept section with the person's answer.
- `<view>-before.md` and, when a change is proposed, `<view>-after.md` in the study folder, with the same ids.
- The index row; after acceptance, the standing views with the accepted changes as `planned`, and a decision record when the person agreed to one.
- `architecture.html` rebuilt, or reported as out of date.

## Done when

- Every removed or merged part has the guarantee it gave and where that guarantee now lives, or the evidence that it carried none.
- Every scenario, constraint and unnamed guarantee has a row that says it holds after the change, with the mechanism and its evidence or assumption.
- The person's answer is recorded in the study with its date, or the study says it is waiting; only accepted changes reached the standing views, as `planned`.
- The index lists the study; the page is rebuilt or reported as out of date.

## Example

The person says: "Larder runs a separate search service and a Redis session cache. Can we cut it down?" The intake restates: "Which of these parts carry a promise, and which can go with less to run?" S1: a member searches a household of 3,000 items and sees results within 300 ms at the 95th percentile (`README.md:12`). S2: a signed-out member's session stops working within a minute. C1: one developer on call. The inventory finds that the session cache carries nothing: every session check is one indexed primary-key read (`api/src/auth/session.ts:18`), and revocation already goes to Postgres first. The search service carries S1: item names are indexed for prefix and typo matches (`search/src/index.ts:8`). X1 removes the cache; nothing moves except one connection setting, and S2 gets simpler because revocation no longer waits for an expiry. Search could move to a trigram index in Postgres, but the re-trace leaves S1 unknown at 3,000 items and typo tolerance would move into hand-written queries, so it stays, with M1: time the trigram query on a copy of the largest household, under 150 ms to reconsider. The person accepts X1. The Accept section records it; the decision record is offered and written; `containers.md` names the cache's planned removal; `containers-before.md` and `containers-after.md` in the study stay as they were.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| Counting boxes as the measure of simple | Count guarantees kept and the work gone, added and one-off |
| Judging a part by its name or its type | The guarantee test from its code and configuration |
| Removing a part because no scenario names its guarantee | Keep the guarantee; ask the person whether anyone relies on it |
| A removal whose guarantee "moves to the client" with no element and mechanism named | Name the new home, re-trace on the bad day, count its cost |
| Adopting the named removal as the question | Restate the problem; test the removal as `P1` |
| Proposing a change to make the run look useful | "Nothing should change", with its reasons |
| Adding a part "for scale", or splitting modules into services | Removals and merges only; a new mechanism only as the new home of a guarantee a removal displaces |
| A running-cost figure estimated from memory | Figures from the configuration or the person, and the other three costs |
| Editing a standing view before the person accepts | The study holds the proposal; standing views change after the answer |
| Changing the study's views after acceptance | They stay as the record; only the standing views and the Accept section change |

## Hand back

Report:

- What was written: the study's path, its views, the index row, and whether the page was rebuilt (its `DONE` line) or is out of date; after the gate, the standing views changed and the decision record.
- The result in a few lines: each proposed change with the guarantee it re-homes and the net complexity, or that nothing should change and the main reasons; what the named proposal came to.
- What is uncertain: assumptions to confirm, callers outside the repository that could not be ruled out, and the measurements to run first.
- The step that fits next. On an existing application the usual order is recover, evaluate, then simplify or explore, then a decision record, then the standing views updated. So after a study with proposals: the person's answer at the Accept gate, then the decision record and the standing views, then the code work that makes the change; `evaluating-architecture-risks` for a critical look at a large after design before building it; `exploring-architecture-options` when a guarantee can be re-homed in more than one way worth comparing; `recovering-built-architecture` when the views lacked evidence. When nothing should change: no next step is needed; name the check that would change the answer.

Commit nothing: the person reviews the study and commits it. Without file access, return the study and its views as Markdown and say that nothing was written and the page was not rebuilt.

## Not for

- Refactoring code inside one module: the same idea at the scale of functions and files is ordinary code work. This skill changes the parts the views show.
- A critical look at what could go wrong: `evaluating-architecture-risks`. A simplification study names risks only where a removal creates them.
- Comparing new designs for an open choice: `exploring-architecture-options`. This skill subtracts from the design that exists.

## References

| Read | When |
|---|---|
| [the scenario intake](references/scenario-intake.md) | Step 2, before any judgement: the question, scenarios, constraints, facts and assumptions, decisions |
| [subtraction](references/subtraction.md) | Steps 3 to 10: essential against accidental, the guarantee test, re-homing, the cost of each technology, where complexity hides, what to measure, published cases, when nothing should change |
| [the simplification template](templates/simplification.md) | Step 11: writing the study, and the Accept section at the gate |
| [the view conventions](references/view-conventions.md) | Before writing: location rule, view format, statuses, ids, evidence, Mermaid subset and quoting, compare links |
| [the view template](templates/view.md) | Step 9: writing the before and after views, and the standing view update at the gate |
