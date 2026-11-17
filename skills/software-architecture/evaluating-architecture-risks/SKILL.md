---
name: evaluating-architecture-risks
description: "Takes a critical look at a system's architecture, a design or a proposal and writes a dated risk review in the architecture folder (context/architecture/ by default): a study at studies/YYYY-MM-DD-slug/README.md from templates/risk-review.md that opens with the shared intake, gives each priority scenario a verdict of met, at risk or unknown, ranks risks by likelihood and impact, pins each to an element id with cause, evidence and a next check, names trade-off points, and adds an annotated view and a failure sequence. Traces each measurable scenario through the views element by element, then looks for what the scenarios miss: single points of failure, dependencies slow or down, sensitive data crossing trust boundaries, and a premortem. Use when the user says take a critical look, review the architecture, what could go wrong, poke holes in this design, or check the risks before we change X. Not for reviewing a code change (reviewing-code-changes), or a full security assessment (a security specialist)."
license: MIT
---

# Evaluating architecture risks

A risk review answers "take a critical look" with evidence. Its value lies in what the person did not already know, so its job is to try to break the design's claims, not to confirm them: each priority scenario is traced through the system until the evidence shows that it holds, shows how it fails, or shows that nobody can tell yet. The result is one dated study beside the standing views. It changes no standing view and has no gate: the findings are shown and the person decides what to do with them.

Say what the evidence says, including when it is uncomfortable: the person's proposal may be the riskiest part, a decision on record may no longer hold, or the problem may not be an architecture problem at all. "This problem does not need an architecture change" is a finding like any other, and often the most useful one.

## Where the work lives

[The view conventions](references/view-conventions.md) give the location rule, the folder tree, the view format, element ids, evidence, the Mermaid subset and quoting, and the link forms. Read them before you write. A risk review is a study: `studies/YYYY-MM-DD-<slug>/README.md` in the architecture folder, with `Kind: risk review` in its header line and its own view files beside it, named after the standing view they vary.

The review reads the standing views and the decision log and edits neither, because a standing view records what is built or agreed, and a review is neither. When the review shows a standing view is wrong, it says so in the study and in the report and leaves the fix to a separate step. The one shared file it changes is the index `README.md`, which gains the study's row in its Studies table and nothing else: ids that only this study uses stay out of the index's element ids table, which lists the ids of standing views, until the person accepts the study's outcome.

## Situations

| Situation | What to do |
|---|---|
| Standing views exist | All the steps below |
| A proposal: a study's `proposed` view, a document, or the person's words | Trace the scenarios through the current system and through the proposal. Reuse the ids the proposal shares with the current views. A proposal given only in words is drawn as a `proposed` view inside this study before it is traced |
| No views, or views with little evidence | Nobody needs to recover the architecture first: work on the views that exist, read the code the scenarios cross, and draw only what the trace needs, inside this study. List every element and relationship you could not evidence under "What this review assumed", and name `recovering-built-architecture` as the next skill |
| An earlier review of the same subject | Read it, and re-check against the code every claim of it you rely on, because code moves and a study keeps its date. Say which of its findings still hold, which changed and which were wrong. Write a new study; the old one stays unchanged |
| "Before we change X" | Add a change scenario whose stimulus is X, so the review says whether the system is ready for it |

## Steps

1. **Read first.** Open the repository's `AGENTS.md`, the decision log's index and the records it lists that touch the subject, the architecture index, every standing view the subject crosses, and the studies on the same subject. Then read the code and configuration the subject crosses: entry points, the modules on the path, deployment files, schema. Note the element ids in use. A view is a claim; a review that trusts the picture without opening the code reviews the picture, not the system.
2. **Run the intake.** Follow [the scenario intake](references/scenario-intake.md): the real question restated without the solution the person named, three to five priority scenarios with all six fields and a measure, hard constraints, facts apart from assumptions and proposals, and what is already decided. Ask the person only what the repository cannot answer, in one message, each question with the default you will use. Write the intake at the top of the study, directly under the title and the header line, so every judgement below can be checked against it. Nothing that judges goes above it: the headline finding belongs in "Does this need an architecture change?" and in your report.
3. **Trace each scenario.** Follow the scenario through the views, element by element, as [scenario tracing](references/review-methods.md#trace-each-scenario) describes: at each element, what it does with the stimulus, which mechanism gives the response (a timeout, a retry, a transaction, an ordering rule, a retention limit), the evidence for it, and whether the measure still holds. Check the view against the code at each element on the path. Give each scenario one verdict, `met`, `at risk` or `unknown`, with its reasoning; an `unknown` names the next action that would settle it.
4. **Look for what the scenarios miss.** Scenarios only test what someone thought of. Make four passes, each described in [the review methods](references/review-methods.md):
   - **Single points of failure:** for each element and each place it runs, if it stops, which scenarios fail, and for how long?
   - **Dependencies:** for each dependency on the paths you traced, what happens when it is slow, down, gives a wrong answer, delivers twice or delivers out of order.
   - **Trust boundaries:** where sensitive data goes, which boundaries it crosses, and what checks each crossing.
   - **Premortem:** "It is a year from now and this failed. Why?" Write three to five short failure stories, each a concrete path through element ids, and keep those the evidence supports.
5. **Write each risk so it can be checked.** Each risk gets an id (`R1`), the element ids it sits on, a cause (the condition and the mechanism), the consequence (which scenario or promise breaks), its evidence, and a next check: an observation with a threshold that confirms or clears it. A risk you cannot pin to an element is a worry, not yet a finding: trace it until it lands on one, or list it under what was assumed.
6. **Rank by likelihood and impact.** Use bands (likely, possible, unlikely; severe, major, minor) with the basis for each, not computed numbers, because invented precision hides how little is known. Rank irreversible harm, such as lost data or exposed data, above reversible harm of the same band. The top risks are the ones worth acting on now, usually three to five; each of them has a next check.
7. **Name the trade-off points.** Where one mechanism serves one scenario and hurts another, or one parameter moves two scenarios in opposite directions, write it as a trade-off point with both scenario ids. Name it; leave resolving it to an options study.
8. **Decide what kind of change each finding needs.** For each top risk, say whether it needs an architecture change (an element, a relationship, a store or a boundary changes), a change inside one element (code, configuration, a limit), an operational change (monitoring, a drill, a runbook), or nothing beyond accepting it. When none needs an architecture change, the study says so in one plain sentence with its reasons.
9. **Draw two views in the study.** Every view follows [the view template](templates/view.md); [annotating](references/review-methods.md#the-annotated-view-and-the-failure-sequence) gives the details.
   - **One annotated view:** a copy of the standing view where the top risks sit (often containers or deployment), saved as `<view>-risks.md`, with the same ids, each element or arrow at risk carrying its risk ids in its label. Link it from the study with a compare link against the standing view.
   - **A failure sequence** for the top risk where order matters: a `sequenceDiagram` from the normal path into the failure and on to what the user sees, saved as `runtime-<topic>-<failure>.md`. When order adds nothing to any top risk, write one sentence in the study saying why instead.
10. **Write the study and the index.** Fill [the risk review template](templates/risk-review.md) at `studies/YYYY-MM-DD-<slug>/README.md`, with an Outcome of a few words such as `findings shown` or `no architecture change needed`. Add the study's row to the Studies table of the architecture index, and change nothing else in it (create the index as the conventions describe when there is none). Check every view and link against the conventions' "Before you finish" list.
11. **Rebuild the page.** When the skill `drawing-architecture-views` is available, rebuild `architecture.html` by its steps before you report, where a shell is available with its build script, and read the page's check lines as it describes. When it is not available, leave `architecture.html` as it is, write the views in Markdown only, say in your report that the page was not rebuilt and is out of date, and name `drawing-architecture-views` as the skill that rebuilds it.

## Output

- `studies/YYYY-MM-DD-<slug>/README.md`: the intake; a verdict per scenario (met, at risk, unknown) with reasoning and evidence; the four passes; risks ranked by likelihood and impact, each pinned to element ids with cause, evidence and consequence; trade-off points; the next check for each top risk; what kind of change each finding needs; what the review assumed; standing views that disagree with the code.
- `<view>-risks.md` in the study folder: the annotated view.
- `runtime-<topic>-<failure>.md` in the study folder, or the sentence saying why order adds nothing.
- The index row, and `architecture.html` rebuilt or reported as out of date.

## Done when

- Every priority scenario has a verdict with reasoning that cites evidence, or is `unknown` with the next action that would settle it.
- Each of the four passes appears in the study, with its findings or with "nothing found" and what was checked.
- Every risk names an element id that exists in the views, a cause, evidence, and its likelihood and impact bands; every top risk has a next check.
- No standing view and no decision record changed; the index lists the study; the page is rebuilt or reported as out of date.

## Example

The person says: "Logins feel slow. Should we put a Redis cache in front of Postgres for sessions?" Reading Larder's folder finds `containers.md` with `web`, `mobile`, `api` and `db`, and no decision on sessions. The intake restates the question without the cache: "Signing in and loading the first screen take too long for members; where does the time go, and what bound must hold?" S1: a member signs in on the web over a home connection at normal load, and the pantry shows within 1.5 s at the 95th percentile (A1, an assumed bound for the person to confirm). The trace follows `web`, `api`, `db`: the session check is one indexed read (`api/src/auth/sessions.ts:22`), but the sign-in handler hashes the password with a work factor tuned for a larger machine (`api/src/auth/hash.ts:9`), which by itself exceeds the budget on the API's instance size. Verdict: S1 at risk; R1 sits on `api`, cause the work factor, next check: time one sign-in on the production instance size, settled when it is under 300 ms. A cache would add a store, a stale-revocation failure mode and one more place for session tokens, and would not touch the slow step. The premortem adds R2: `db` is one instance with backups nobody has restored; next check, a restore drill. Trade-off point T1: a lower work factor helps S1 and weakens password storage. Outcome: `no architecture change needed`; R1 is a configuration change within the security guidance, R2 an operational one. The study draws `containers-risks.md` with `api` and `db` annotated, and says order adds nothing because the slow step is one computation.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| Judging before the intake is written | Intake first, at the top of the study; every verdict cites a scenario |
| "Looks fine" for a scenario because the view shows the arrow | Open the code on the path; `met` needs evidence for each element |
| A risk list of generic worries: "might not scale", "security" | A cause, an element id, evidence, a consequence and a check |
| Scores multiplied into a precise rank | Bands with their basis; irreversible harm first |
| Adopting the person's named solution as the question | Restate the problem; test the named solution as one proposal |
| Inventing findings to look thorough | "No material finding within the reviewed scope" is valid; say what was covered |
| Editing a standing view the review showed to be wrong | Record it under the views that disagree with the code and name the next skill |
| Copying an earlier study's findings | Re-check each against the code and cite it |
| Recommending a redesign in the review | Name the change kind; hand the open choice to an options study |

## Hand back

Report:

- What was written: the study's path, its views, the index row, and whether the page was rebuilt (its `DONE` line) or is out of date.
- The verdict per scenario in one line each, the top risks with their next checks, and whether any finding needs an architecture change.
- What is uncertain: assumptions the person should confirm, `unknown` verdicts, elements without evidence, standing views that disagree with the code.
- The skill that fits next: `exploring-architecture-options` when a top risk needs an architecture change with more than one way to make it, or a trade-off point needs a choice; `simplifying-system-architecture` when the review found mechanisms that carry no scenario; `recovering-built-architecture` when the views lacked evidence or disagreed with the code; a decision record when the person accepts a finding that changes what was decided. When nothing needs an architecture change, say so and name the next check to run instead. The usual order on an existing application is: recover, evaluate, then simplify or explore, then a decision record, then the standing views updated; on a new system: explore, evaluate the chosen option, then draw the standing views as `planned`.

Commit nothing: the person reviews the study and commits it. Without file access, return the study and its views as Markdown and say that nothing was written and the page was not rebuilt.

## Not for

- Reviewing a code change or a pull request: `reviewing-code-changes` reads a diff. This skill reviews the system's shape, before or apart from any diff.
- A full security assessment: the trust-boundary pass finds architectural exposure (where sensitive data goes and what guards each crossing). A threat model, a penetration test or a compliance audit needs a security specialist; say so in the study when the findings call for one.
- Choosing between designs (`exploring-architecture-options`) or removing mechanisms (`simplifying-system-architecture`): the review names the risk and the change kind and hands the choice on.

## References

| Read | When |
|---|---|
| [the scenario intake](references/scenario-intake.md) | Step 2, before any judgement: the question, scenarios, constraints, facts and assumptions, decisions |
| [the review methods](references/review-methods.md) | Steps 3 to 9: tracing, the four passes, writing and ranking risks, trade-off points, next checks, when nothing needs to change, the two views |
| [the risk review template](templates/risk-review.md) | Step 10: writing the study |
| [the view conventions](references/view-conventions.md) | Before writing: location rule, view format, ids, evidence, Mermaid subset and quoting, compare links |
| [the view template](templates/view.md) | Step 9: writing the annotated view and the failure sequence |
