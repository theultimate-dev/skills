---
name: planning-product-roadmaps
description: "Plans a product's versions and milestones in a product context repository: the gates between versions, version briefs with outcome, done-when, scope in and out, milestones as release slices with observable exit criteria, requirement coverage per milestone derived from the catalogue, prerequisites outside the code, and one risk register and one open-question register. Answers what's next and what's the status from the bet files. Use when the user says plan the next version, plan the milestones, what's the product status, what's next for the product, where are we on the milestones, move this to a later version, close this milestone, or log a risk or open question. Not for one work item's PR slices (planning-implementation) or a work item's PR status (running-implementation-loops)."
license: MIT
---

# Planning product roadmaps

Keep the roadmap layer of a product context repository: which versions the product goes through, what each version delivers and how its milestones are sliced, what must be true before the next version starts, and which risks and open questions are live. Answer "what's the status" and "what's next" from the files, never from memory.

This is the product roadmap. A work item's `roadmap.md` of PR slices belongs to `planning-implementation` in the code repository. Bets inside a milestone belong to `shaping-bets`.

## Inputs and when to run

| Request | Do | Writes |
|---|---|---|
| Plan the product's versions, or the next one | Versions and gates, then the version brief | `roadmap/README.md`, `roadmap/vN/README.md` |
| Plan the milestones of a version | Milestones as release slices with exit criteria | The version brief |
| What's the product status, what's next for the product | Read the bet files, the registers and the architecture index, report | Nothing |
| Move a requirement to a later version | Retarget it | The requirement's Version column; the coverage index |
| A milestone's exit criterion holds | Record the exit with the user's words | The version brief |
| A version ships | Record it, check the gate to the next one, open the next folder | `roadmap/README.md`, `roadmap/vN+1/README.md` |
| Log, close or resolve a risk or open question | Update the register | `roadmap/risks.md`, `roadmap/open-questions.md` |

The repository layout, IDs and statuses are fixed by the repository's `AGENTS.md`. When it has none, use the layout in the [layers summary](#layers-this-skill-relies-on) and say so.

## Read before writing

1. `AGENTS.md`, `roadmap/README.md`, the version brief, `roadmap/risks.md`, `roadmap/open-questions.md`.
2. The requirement catalogue under `product/requirements/`: each capability file's Version and Status columns are the source of every coverage figure.
3. Every bet file under `roadmap/vN/bets/`, for its `Status:`, `Milestone:` and `Depends on:` lines. The bet file's `Status:` line is the only authoritative status; the bet board under `bets/README.md` is a derived copy.
4. `decisions/README.md`, so a plan never contradicts an accepted decision, and `architecture/README.md`, to know whether the architecture baseline is accepted.

Never ask what these files answer. Ask the user only for intent: what a version is for, what order matters, which trade-off to take, and whether an exit criterion holds.

## Versions and gates

`roadmap/README.md` lists every version with its status (`planned`, `in progress`, `shipped`), the only place a version's status lives, one line on what it gives the user, and the **gate** to the next version: an observable condition the user can judge, such as "V1 in daily use by five households for a month". A gate is never "V1 is finished".

- Name the current focus: the version and milestone in progress.
- Keep later versions as sections in `roadmap/README.md`. Open a version's folder, `roadmap/vN/`, only when the previous version ships. When the user asks, the first two versions may be planned together, because the second often shapes decisions the first must not block: the second's brief then lives in `roadmap/v2/README.md`, with no `bets/` folder until the first version ships.
- Keep a **Parked** list: ideas that have no requirement ID yet, deliberately not scheduled, each with one line on why. Parked is not a backlog; nothing moves out of it without the user. A requirement already in the catalogue that has no target is `deferred`, set through `curating-product-requirements`, not parked.

## The version brief

`roadmap/vN/README.md`, from the [version brief template](templates/version-brief.md). It carries no version status; that stays in `roadmap/README.md`.

- **Outcome** in two to four sentences, and **Done when**, an observable condition judged by the user.
- **Scope**: an In / Not in table. Each "Not in" row names the version that takes it, or Parked.
- **Milestones** in delivery order, each a release slice the user can use on its own. Each has what the user gets, its exit criterion, and its status (`planned`, `in progress`, `exited`).
- **Coverage index**: milestone to requirement IDs, derived from the catalogue (see below).
- **Prerequisites outside the code**: accounts, legal checks, purchases, people. Each is a checkbox naming the milestone it gates.
- **Bets**: a link to `bets/README.md`, the bet board. The board is written by `shaping-bets` and rewritten by `reconciling-product-context`.

## Milestones as release slices

Slice the version the way a story map slices a backbone: each milestone is a horizontal cut across the product that someone can use end to end.

1. **The walking skeleton first.** The first milestone is the thinnest slice that runs end to end through every major container and the release path, even when it does almost nothing for the user.
2. **Then by learning value and dependency.** Order the rest so that each one is usable on its own and the riskiest assumptions are tested early.
3. **One exit criterion per milestone,** observable and judged by the user: "a full week of meal plans made from the pantry without a spreadsheet". The user records the exit; you write `exited (YYYY-MM-DD: "<user's words>")`. A milestone never exits on merged code alone.

Read [versions and milestones](references/versions-and-milestones.md) for gate and exit-criterion examples, sizing, and a worked example.

## The coverage index is derived

A requirement row's target Version names a milestone, such as `V1.2` for milestone 1.2, or only a version, such as `V1`, while it waits for a milestone. A `deferred` row has no target. The coverage index in the version brief is rebuilt from those columns: never type it by hand. When rebuilding:

- Count the requirements per milestone and in total.
- List the rows targeted at the version only as "not yet in a milestone".
- **Flag every disagreement**: a requirement targeted at a milestone the brief does not have, a milestone with no requirement, a requirement whose prose in the brief promises something no row covers. Report each one; do not resolve it by editing the index.
- A requirement split across versions (`V1.4, V2.3`) appears under both, marked `part`.

## Retargeting a requirement

Moving a requirement to another milestone or version is a roadmap decision. Confirm it with the user, then change its Version column under the catalogue's rules: when `curating-product-requirements` is installed, follow it; otherwise edit only the Version cell. Moving it to no version at all makes it `deferred`, through `curating-product-requirements`. Rebuild the coverage index. When a bet already covers the requirement, name the bet: the bet must be reshaped with `shaping-bets` before it is handed off, and a bet already `in delivery` is the user's call.

## Registers

One risk register and one open-question register per product, in `roadmap/`. Other files cite register IDs and never keep their own lists.

- `roadmap/risks.md`: `RSK-NN`, the risk, why it matters, the mitigation, the versions it affects, the owner (a bet or a person), and `open` or `closed`.
- `roadmap/open-questions.md`: `OQ-NN`, the question, what it blocks, the recommended answer, the owner, and `open` or `resolved` with a link to what answers it.

Merge duplicates, keeping the lowest ID and noting the merged ones. An answer that settles structure, technology, a boundary or a trade-off becomes a decision record: use `decision-records` when it is installed, and link the record from the resolved row. Read [registers](references/registers.md) for the formats and the rules for merging and closing.

## Status and what's next

Answer from the files, in this order: bet files' `Status:` lines, the version brief, the registers, then the requirement statuses. Never answer from memory or from the bet board alone; when the board disagrees with a bet file, the bet file wins and the board needs `reconciling-product-context`.

Report:

1. **In delivery**: each bet, the code repository and work item from its Handoff section.
2. **Built, awaiting reconciliation**.
3. **Ready to hand off**: `ready` bets whose dependencies are `built` or `done`.
4. **Shaped, not ready**: each `shaped` bet with what fails readiness: a `proposed` contract, a dependency not yet built, an open question, a missing design handoff.
5. **Needs shaping**: milestones whose requirements no bet covers yet.
6. **Blocked**: open questions and prerequisites that block a milestone or a bet.
7. **Milestone and version state**: what exited, what is in progress, whether the architecture baseline is accepted, the gate to the next version.
8. **Next**: the one action that unblocks the most, by the rules below.

Next-action rules, first match wins:

1. A `built` bet: close it with `reconciling-product-context`. Unreconciled work makes every later answer wrong.
2. A `ready` bet whose dependencies are `built` or `done`: hand it off with `shaping-bets`.
3. No accepted architecture baseline for the version in focus: run `designing-system-architecture` in baseline mode before any shaping.
4. A `shaped` bet that fails readiness: route it to the fix. A `proposed` contract goes to `designing-system-architecture` in contract mode, an open question to the user, a missing design handoff to the `product-design` skills, a dependency not yet built to that dependency's own next step.
5. A milestone in focus with requirements no bet covers: shape it with `shaping-bets`.
6. An open question that blocks the milestone in focus: ask it, with its recommended answer.
7. Every bet of the milestone in focus is `done` and it has not exited: ask the user whether its exit criterion holds.
8. A version that just shipped: record it, check the gate, and refresh the architecture with `designing-system-architecture` before shaping the next version.
9. Nothing above: plan the next milestone or version.

Read [status and next](references/status-and-next.md) for the report format and dependency checks.

## Agreement

Version scope, milestone order, gates, exits and retargets are the user's decisions. Propose them with a recommendation and its reason; write them once the user agrees in words, and record the date. Silence or "looks good" on a draft that also raised a question is not agreement on that question.

## When a sibling skill is missing

Say in one line which skill is missing, then produce its essential outcome yourself:

| Missing | Essential outcome |
|---|---|
| `curating-product-requirements` | Edit only the Version cell of the retargeted row; never renumber or reword a requirement |
| `shaping-bets` | Report the milestone's uncovered requirements as "needs shaping"; never write bet files |
| `reconciling-product-context` | Report built bets and stale boards; never rewrite another skill's index |
| `decision-records` | Write a short record in the repository's `decisions/` convention: status, date, context, options, decision, consequences; add its index row |
| `designing-system-architecture` | Name the architecture sections a new version touches as an open question |

## Report

Return the files written, the decisions the user made with their words, the coverage disagreements found, the register changes, and the next action. Without file access, return the changed sections as Markdown and say that no file was written.

## Layers this skill relies on

`roadmap/README.md` (versions and their statuses, gates, focus, parked), `roadmap/vN/README.md` (version brief), `roadmap/vN/bets/` (bets and their board), `roadmap/risks.md`, `roadmap/open-questions.md`, `product/requirements/` (the catalogue and its Version column), `architecture/README.md` (whether the baseline is accepted), `decisions/`. Statuses: version `planned | in progress | shipped`, in `roadmap/README.md` only; milestone `planned | in progress | exited`; bet `shaped | ready | in delivery | built | done | dropped`; risk `open | closed`; open question `open | resolved`.

## References

| Read | When |
|---|---|
| [versions and milestones](references/versions-and-milestones.md) | Planning versions and gates, slicing milestones, writing exit criteria, shipping a version, the worked example |
| [registers](references/registers.md) | Logging, merging, closing or resolving risks and open questions |
| [status and next](references/status-and-next.md) | Answering status and what's next, checking dependencies, spotting stale boards |
| [roadmap index template](templates/roadmap-index.md) | Writing `roadmap/README.md` |
| [version brief template](templates/version-brief.md) | Writing `roadmap/vN/README.md` |
| [risks template](templates/risks.md) | Starting `roadmap/risks.md` |
| [open questions template](templates/open-questions.md) | Starting `roadmap/open-questions.md` |
