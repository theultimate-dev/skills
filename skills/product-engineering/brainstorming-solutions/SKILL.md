---
name: brainstorming-solutions
description: "Researches the codebase for prior art, reusable utilities, and constraints, generates two to four genuinely distinct technical approaches to an agreed spec.md, compares them in a table of architecture fit, risk, effort, and reversibility with a clear recommendation, and writes the approach the user picks, the rejected alternatives, and the consequences into the Approach section of spec.md, plus a decision record when the choice is consequential. Stage 2 of the product-engineering loop, gate G2. Use when the user says brainstorm approaches, what are our options, how should we build this, compare approaches, or when a spec is agreed and the technical direction is still open."
license: MIT
---

# Brainstorming solutions

Stage 2 of the product-engineering loop and gate G2. Research the codebase, lay out two to four genuinely different ways to build the agreed spec, recommend one, and let the user pick or combine. The user's pick is G2. Then write the Approach section of `spec.md`.

This skill covers technical approaches only. Product and UX ideation belongs to the `product-design` plugin.

## Inputs and when to run

Start from `spec.md` whose status line starts with `Status: agreed`, as in `Status: agreed (G1, 2026-09-25: "Agreed")` or `Status: agreed (G1 skipped: repro reproduced at a1b2c3d)`. On a track that batches the gates into one message, it may still say `draft`. Inside a work item without an agreed spec, run `specifying-work-items` first. When it is not installed, draft the problem and the acceptance criteria from the request and the code, and ask the user to confirm them in one message before comparing approaches.

Two requests skip G1:

- **Options outside a work item**, such as "what are our options for search?": write no `spec.md`. Derive the problem and 2–5 criteria from the request and the code, and state them as assumptions in the comparison's Context line. After the pick, offer a decision record.
- **A standalone spike** needs no spec: take the question from the request, and follow "Settle feasibility with a spike".

An approach the request names ("move to date-fns") is recorded as `Chosen:` with the user's words. G2 only checks it against the ACs and writes the decision record (step 6).

An approach answers the spec and never changes it. When an approach would drop or weaken an acceptance criterion, that is a scope change: take it back to G1 with the evidence.

| Track | G2 |
|---|---|
| Quick fix | Does not run |
| Bugfix | Only when the fix options differ in behavior, risk, or reach, such as patching the symptom vs. fixing a shared cause. Otherwise write the fix in one line under Approach |
| Small change | Short, and batched with G1–G4 in one message. With one sensible approach, ask for a one-line confirmation |
| Feature | Runs in full |
| New app | Runs on the stack, hosting, and data store. Always record the stack decision, starting a decision log if none exists; the record lands in the walking-skeleton PR |
| Refactor or migration | Only when the target structure is consequential. Otherwise describe the target in one paragraph under Approach |
| Spike | Feeds G2. A standalone spike needs no spec; see "Settle feasibility with a spike" |

## Procedure

1. **Research the codebase.** Read the spec, the project instructions (AGENTS.md, CLAUDE.md), and the decision log; an accepted decision can settle a choice outright. Search for prior art: the closest feature that solves a similar problem, how it is laid out end to end, and the utilities it uses. List the reusable pieces with their paths. Note the constraints that bite: runtime and framework versions, the data model, deployment, conventions, the performance envelope. Consult dated primary sources (official documentation, source code, standards) only when a technical question changes feasibility, and record the URL, retrieval date, version, and finding. Keep apart what the code shows, what a source claims, and what you infer.
2. **Generate 2–4 genuinely distinct approaches.** Pick the axes where the spec's constraints bite, such as where the logic lives, build vs. buy vs. reuse, sync vs. async, the data model, incremental vs. big-bang, client vs. server. Each approach differs from every other on at least one of them. For each, write how it works in 2–4 sentences, the files and modules touched, its fit with the existing architecture, its risks, its effort, and its reversibility. Every approach meets every AC, or says which it misses. Run the strawman check: name the situation in which each approach is the best choice, and drop any approach for which you cannot.
3. **Compare and recommend.** Put the approaches in one table from the [approaches template](templates/approaches.md). Recommend one, with reasons tied to the spec's criteria and constraints and to the evidence from step 1, never to taste. Name the condition under which you would recommend another.
4. **Discuss and pick: G2.** Send the approaches, the table, and the recommendation in one message. Then ask the user to pick one or combine them, through the host's structured-question tool when it has one, with the approaches as options and the recommended one first. Answer follow-up questions with evidence from the code. When the user combines approaches, check that the combination is coherent, restate it in one paragraph, and confirm it. An explicit pick is G2; silence is not. When the user says "you choose", record the recommendation as chosen by delegation.
5. **Write the Approach section** of `spec.md` in the format from the template: the chosen approach and how it works, what it touches and reuses, the contracts later work depends on, the evidence, the rejected alternatives with a one-line reason each, the consequences, and the G2 agreement line with the date and the user's words. Stop at module boundaries and contracts. File-level steps belong to `planning-implementation` at G4.
6. **Record a consequential choice.** A choice is consequential when it fixes persistent data ownership, a public contract, a security boundary, a major dependency, a deployment or platform commitment, or cost. Record it in the project's decision log. When the `decision-records` skill is installed, use it. Otherwise write a short record in the project's existing convention (such as `docs/adr/` or `decisions/`): status, date, context, options, decision, consequences. When the project has no decision log, keep the decision in the Approach section and offer in one line to start a log; on a new app, start it. Link the record from the Approach section. The record lands in the repository with the work item's first PR slice: `implementing-plans` commits it with `spec.md`.

Effort and reversibility use one scale across all approaches. A PR slice is the work that becomes one pull request (merge request).

| Effort | Meaning | Reversibility | Meaning |
|---|---|---|---|
| S | One PR slice | Easy | A flag or a config change undoes it |
| M | One plan with several phases | Moderate | A code change undoes it; no data or contract moves |
| L | Several plans | Hard | Undoing needs a data migration, a public-contract change, or an external commitment |

## When one approach is sensible

Say so. Explain why the alternatives fail: a named constraint, an AC they cannot meet, or a pattern the codebase already standardizes. Ask for a one-line confirmation. Never invent alternatives to fill a table.

For a spec in which customers cancel their own orders, and the staff cancellation already refunds and restocks:

```text
One sensible approach: move the refund-and-restock steps out of the staff cancellation
(src/admin/orders/cancel.ts) into a shared function that the admin and the storefront both call.
Processing cancellations in a background job would break AC9, which requires the customer
to see a failed refund immediately. Reply "yes" to go ahead, or tell me what to reconsider.
```

## Settle feasibility with a spike

When a feasibility question decides between approaches and neither the code nor a primary source settles it, propose a spike: a timeboxed throwaway branch that is never merged. State the question, the timebox, the observation that answers it, and which answer points to which approach. In the same question as the timebox, ask whether you may commit and push the spike branch; without a yes, commit and push nothing. Run it once the user agrees to the timebox, only against local services and provider test modes, or the environments the verification profile allows. Never touch production, real email, payments, or webhooks. Record the finding, with the branch and commit it came from, in the comparison and in the Approach section's evidence. A spike that runs out of time without an answer is also a finding: report it and pick with that risk named.

A standalone spike follows the same rules. Write its findings to `docs/product-engineering/<slug>/spike.md` on the spike branch, which is never merged. Then stop and offer a work item whose G2 uses them.

## Draft in parallel for diversity

When the host has parallel agents or subagents, draft approaches independently so that no approach anchors the others. Give each drafter the spec, the research notes, and a different axis position to hold fixed, such as "all logic on the server", "reuse the existing job queue", or "no new dependencies". Then merge duplicates, run the strawman check, and compare. Without parallel agents, write every approach's "how it works" before judging any of them.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| A strawman that makes the favorite look good | Drop every approach whose winning situation you cannot name |
| Options that differ only by library brand | Merge them, and vary an axis that changes the architecture |
| A recommendation by taste: "cleaner", "more modern" | Tie each reason to an AC, a constraint, or code evidence |
| Ignoring what the repository already does | Start from prior art and justify every departure from it |
| Re-arguing an accepted decision | Cite the record. Reopen it only with new evidence, as its own question |
| A scope cut hidden inside an approach | Show which criteria each approach meets; a dropped AC goes back to G1 |
| Designing down to files and functions | Stop at module boundaries and contracts |

## Reopen the approach

When implementation shows that the chosen approach is infeasible, that is an escalation trigger. Return here with the new evidence, show what changed, and ask only the affected decision. Update the Approach section, and supersede the decision record rather than editing it.

## Hand back

Report the chosen approach in one sentence, where the Approach section was written, the decision record path (committed by the first PR slice with `spec.md`) or "none: not consequential", any spike findings, and the next stage: G3 with `defining-verification`. A standalone spike reports its findings instead: the answer, its evidence, the branch and commit, and the approach it points to; then it offers a work item. Options outside a work item report the comparison, the pick, and the decision record offer, with no next stage. A request to brainstorm is not a request to implement: change no product code at this stage, and keep spike code on its unmerged branch. Without file access, return the Approach section as Markdown and say that no file was written.

## References

| Read | When |
|---|---|
| [generating approaches](references/generating-approaches.md) | Researching prior art and sources, choosing axes of distinctness, running the strawman check, scoring the criteria, deciding which choices need the user and a record, scoping a spike, briefing parallel drafters |
| [approaches template](templates/approaches.md) | Presenting the comparison and writing the Approach section |
