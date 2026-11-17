# Simplification study: [subject]

Date: [YYYY-MM-DD] · Kind: simplification study · Outcome: [waiting for the answer | nothing should change | accepted on YYYY-MM-DD | narrowed on YYYY-MM-DD | declined on YYYY-MM-DD]

<!-- Save as studies/[YYYY-MM-DD]-[slug]/README.md in the architecture folder; the slug names the subject in two to four words.
Keep the title and the header line first: the index row is copied from them. Update the Outcome when the person answers, and the index row with it.
The Intake comes directly under the header line: put no summary or finding above it; the answer goes in "Result". Ids: S scenarios, C constraints, F facts, A assumptions, P proposals (what the person named), G guarantees, X proposed changes, M measurements. Element ids are the ids of the views.
Links to standing views and to the page start with two parent-folder steps, because the study sits two folders below the architecture folder; the source paths after "#compare=" stay relative to the architecture folder.
When nothing should change: keep the Inventory, the before view, the scenario table and the Result; write "none" under Proposed changes, What is removed, Where the complexity moved and What to measure first, and draw no after view.
Write "none" under a heading that has nothing, with what was checked. Delete this comment and every unused placeholder. -->

## Intake

Asked by [person] on [YYYY-MM-DD]: "[their words]"

**The real question.** [One or two sentences, without the removal or merge the person named.]

**Priority scenarios.** These are the guarantees the result must keep.

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

- P1: [the removal or merge the person named, or none]. Source: [the person's words].

**Already decided.**

- [link to a decision record, an accepted study or a standing view]: [what it settles here, or "the decision log is empty"].

## Scope

Views read: [links to the standing views and earlier studies read]. Code and configuration read at commit [short commit]: [the folders and files the inventory and the traces crossed]. Earlier simplification studies of this system: [which of their findings still hold, or none].

## Inventory: what each part guarantees

One row per component, hop, store and technology at the level of [the view], judged by what its code and configuration do, not by its name.

| Element | Part | Kind | Guarantee it gives | Carries | If removed | If merged with a neighbour | Evidence | Finding |
|---|---|---|---|---|---|---|---|---|
| [id, or id → id for a hop] | [name] | [component \| hop \| store \| technology] | G1: [what it guarantees here, in a few words, or "none found"] | [S and C ids, or "no scenario names it"] | [what breaks, on the normal path and on the bad day] | [neighbour id: what the separation gives today] | [`path:line`; for "none found", what was checked] | [stays \| candidate \| ask the person] |

Guarantees no scenario names: [G ids, each kept unless the person says nobody relies on it, or none].

## Proposed changes

| Id | Change | Elements | Guarantees it touches | Where each guarantee lives after | Lasting cost removed | Lasting cost added | One-off cost |
|---|---|---|---|---|---|---|---|
| X1 | [remove \| merge] [what] | [ids] | [G ids, or none] | [element and mechanism, or "not needed: carries none"] | [to run, upgrade, debug, staff] | [the same four, or none] | [migration, running both, drain, rollback] |

Considered and rejected: [each removal or merge tested and dropped, with the guarantee it would break, or none]. The named proposal P1: [kept as X id, narrowed, or rejected because it breaks G id for S id].

## Views

- Before: [a relative link to `[view]-before.md` in this folder], a copy of the standing view as it was on [YYYY-MM-DD], or drawn from the code when no standing view existed.
- After: [a relative link to `[view]-after.md` in this folder], with the same element ids; changed and new elements and arrows are `proposed`, removed ones are absent.
- [A compare link whose target is the page two folders up, then `#compare=studies/[YYYY-MM-DD]-[slug]/[view]-before.md,studies/[YYYY-MM-DD]-[slug]/[view]-after.md`, with the before view first.]

## Scenarios and constraints after the change

Every scenario and constraint of the intake, and every guarantee no scenario names, re-traced through the after view.

| Id | Holds after? | Why: the mechanism that carries it after the change | Evidence or assumption |
|---|---|---|---|
| S1 | [yes \| yes, if M id confirms it \| no] | [element by element, the mechanism that gives the response and meets the measure] | [`path:line`, A id] |
| C1 | [yes \| no] | [why] | [evidence] |
| G[n] | [yes \| no] | [where the guarantee lives now] | [evidence] |

## What is removed and where its guarantee lives

| Removed or merged | The guarantee it gave | Where that guarantee lives now | Evidence or the change that puts it there |
|---|---|---|---|
| [id] | [G id and words, or "none: carried nothing, checked [what]"] | [element and mechanism, or "not needed"] | [`path:line`, X id] |

## Where the complexity moved

| Item | Gone for good | Added for good | One-off |
|---|---|---|---|
| [technology, deployable, hop, store, mechanism, runbook step, configuration] | [what no longer has to be run, upgraded, debugged or known] | [what now has to be, and where: a client, a table, a script, a person] | [migration, running both, drain] |

Net: [one or two sentences: fewer technologies or deployables to run, and what that cost in added mechanism; or that the added work is close to what is removed and the change is not worth a migration].

## What to measure first

| Id | Measurement | Settled when | Where it runs |
|---|---|---|---|
| M1 | [the riskiest assumption first, then each scenario whose mechanism changed, then a failure drill for each re-homed guarantee] | [the threshold, both ways] | [production read-only, a copy, a test environment, a person] |

## Result

[One plain sentence: the changes proposed (X ids) and what they remove, or "Nothing should change: [reasons tied to the scenarios]".]

[When nothing should change: the parts that look removable and why each stays; what would change the answer; improvements inside one element, kept apart as ordinary code work.]

## Accept

The person accepts, narrows or declines. Until they answer, this section says "Waiting for the answer since [YYYY-MM-DD]", and nothing outside this study changes.

- Answer on [YYYY-MM-DD], from [person]: "[their words]"
- Accepted: [X ids, or none]. Declined: [X ids, or none].
- Decision record: [offered on YYYY-MM-DD; written at a relative link | declined by the person | not offered, nothing accepted].
- Standing views updated: [each standing view changed, with the accepted elements and arrows shown as `planned` | none]. This study and its views stay as they were on [the study's date].

## Next

[The skill or step that fits next and why: a decision record for the accepted changes, then the code work that makes them; evaluating-architecture-risks for a critical look at the after design before building it; exploring-architecture-options when a guarantee can be re-homed in more than one way worth comparing; recovering-built-architecture when the views lacked evidence; drawing-architecture-views to rebuild the page when it was not rebuilt. Or, when nothing should change: no next step, or the next check that would change the answer.]
