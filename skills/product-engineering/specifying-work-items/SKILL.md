---
name: specifying-work-items
description: "Interviews the user to turn an issue, product brief, or product-design handoff into an agreed spec.md with numbered requirements (R1…), observable acceptance criteria (AC1…), non-goals, constraints, and assumptions. Grounds itself in the code first so it never asks what the repository can answer, ranks the unknowns by impact, asks in short rounds where every question carries a recommended default and options, and ends with the user's explicit confirmation. Stage 1 of the product-engineering loop, gate G1. Use when the user says spec this out, interview me, what do you need to know, or write requirements. Not for shaping a rough product idea (shaping-product-briefs)."
license: MIT
---

# Specifying work items

Stage 1 of the product-engineering loop and gate G1. Turn a request into `spec.md`: read the code first, then interview the user about what the code cannot tell you. The repository answers questions of fact. The user answers questions of intent, priority, and trade-off. Ask the user only the second kind. G1 is the user's explicit confirmation of the written spec.

The spec lives at `docs/product-engineering/<work-item-slug>/spec.md` unless the project already keeps specs elsewhere. Leave its Approach and Verification sections empty: `brainstorming-solutions` writes Approach at G2 and `defining-verification` writes Verification at G3. When those skills are not installed, hand over the agreed spec and say that G2 and G3 are still open.

## Scale by track

| Track | Establish | Interview |
|---|---|---|
| Quick fix | Nothing; the intent goes in the pull request (merge request) body | This skill does not run |
| Bugfix | Repro steps, expected vs. actual, blast radius: who else is affected, since when, whether any data is now wrong | Reproduce it first when that is cheap and safe: locally, never against production. Skip G1 only when it reproduces: write the short spec with `Status: agreed (G1 skipped: repro reproduced at <short-sha>)` and show it in the next gate's message. A report that does not reproduce is a high-impact unknown: ask for the missing condition. When reproducing is not cheap or safe, keep `Status: draft` and let the next gate's message confirm the short spec. Ask about scope only when the blast radius includes damaged data, because repair is a scope decision. The repro becomes AC1 and the G3 check |
| Small change | The behavior change, the one or two edge cases that matter, what is out | One round, two at most. `running-implementation-loops` batches G1–G4 into one message; then write the spec and leave the confirmation to that message |
| Feature | Every topic in the table below | Rounds until the stop rule holds |
| New app | The product first, then the engineering constraints | Route unresolved product or UX questions to `guiding-product-discovery` when it is installed, and resume from its handoff. Otherwise run a short interview labeled "Product interview" before the engineering one. The stack is chosen at G2, not here |
| Refactor or migration | The invariants that must hold (behavior, public contracts, data, performance envelope) and what the new structure must make possible | Short. Each invariant becomes a requirement with its own AC |
| Spike | Nothing here | This skill does not run: a standalone spike needs no spec, and `brainstorming-solutions` takes the question from the request. A feasibility question inside a work item goes under Assumptions and open questions, and G2 settles it with a spike |

## Procedure

1. **Read the inputs.** Fetch an issue by its ID with an issue-tracker tool (`gh issue view`, the GitLab equivalent, a Linear or Jira MCP server). When no tool reaches it, ask the user to paste it. Read a product brief or a `product-design` handoff in full. Keep upstream IDs exactly: a handoff's `R3` stays `R3`. Import accepted upstream behavior as agreed and never re-ask it. Send a handoff's product or design blockers back to `product-design`; its engineering questions join your unknowns. An existing `spec.md` means resume: read it and ask only what is still open. Existing approval or delegation carries forward.
2. **Ground yourself in the code.** Read the project instructions (AGENTS.md, CLAUDE.md, and the nested ones in each package the change touches) and the decision log. Follow the changed behavior from its entry point through state, dependencies, failure handling, and tests. Find the closest existing feature: it supplies most of your recommended defaults. Never ask what the repository can answer: the stack, current behavior, states, data model, conventions, similar features. When the code answers part of a question, state the finding with its path and ask only for the decision. With no codebase, ground yourself in the inputs and in every system the app must integrate with.
3. **List the unknowns and rank them.** Write each unknown as one line and rank it by how much its answer changes behavior, scope, or effort.

   | Impact | The answer changes | Treatment |
   |---|---|---|
   | High | What gets built, who can do it, what an AC asserts, or effort by a PR slice or more; or it touches data, money, auth, or a public contract | Ask first. Never assume it silently |
   | Medium | An edge or error behavior, or effort within one slice | Ask in the round for its theme when there is room; otherwise assume it and flag it in the summary |
   | Low | A reversible detail the user catches at first sight: copy, placement, a default value | Do not ask. Record it as an assumption |

4. **Interview one theme at a time.** A round holds at most 4 questions under one theme the user can hold in mind, such as the cancellation rule; a theme may span several topics. Order the themes by their highest-impact unknown, so the first round carries the most consequential questions. Each question gives one line of context from the code, a recommended default with its reason, and 2–4 options. Use the host's structured-question tool when it has one. Otherwise send a numbered list the user can answer as `1b, 2 ok, 3a`. After each round, record the answers, re-rank, and drop every question the answers already settled. Save the draft `spec.md` after each round when the interview runs longer than two rounds.
5. **Stop when the criteria are testable.** Stop when every AC is observable and testable, every R has at least one AC, and no high-impact unknown is open unless the user accepted an assumption in its place. Stop earlier when the user says to proceed. Every remaining unknown becomes an assumption with its default and what changes if it is wrong. When the user declines to answer ("just build it", "no more questions"), stop: record every open unknown as an assumption with its recommended default and the basis "delegated by the user", and send the G1 summary once. A "go ahead" to that summary is agreement.
6. **Write `spec.md`** from the [spec template](templates/spec.md), with its exact headings in their order. Leave Approach and Verification empty. Keep the Plan heading only on the small-change track, where `planning-implementation` fills it at G4, and on a bugfix with one PR slice, where it holds only the autonomy contract from the intake answer. Delete it on every other track.
7. **Confirm: G1.** Present a summary of at most 10 lines: the problem and the agreed behavior in two sentences, the requirement and AC counts, the non-goals, the assumptions the user must check, and what they will review themselves. Ask whether the spec is agreed as written. On an explicit yes, set `Status: agreed (G1, YYYY-MM-DD: "<user's words>")`. Silence, a change of subject, or "looks interesting" is not agreement. When the user edits, apply the edits and confirm only what changed.

## What the interview covers

Ask about a topic only when the code does not answer it and the answer changes something. The [interview guide](references/interview-guide.md) holds a question bank for each topic and track.

| Topic | Establish |
|---|---|
| Why | The problem, who has it, and the outcome that makes this worth doing |
| Actors | Who performs each action, with which permissions: guests, members, admins, other systems |
| Scope and non-goals | What is in, what is explicitly out, what is deferred |
| Behavior | The main path as the user observes it: trigger, visible result, what changes elsewhere |
| Errors and edge cases | Invalid input; empty, one, and very many; concurrent change; partial failure of a downstream call; repeated submits |
| Data | Where it comes from, who owns it, existing data to migrate, retention, personal data, volume |
| Non-functionals | Only those this item touches: performance, security and privacy, accessibility, compatibility, observability. A number enters the spec only when the user states or accepts it |
| Constraints | Deadlines, platforms, compatibility, dependencies, and policies the code does not show |
| Done and review | What "done" means to the user and what they want to review themselves, such as UI, copy, migrations, or anything touching money or auth. Record the answer on the Done and review line under Constraints; G3 starts its human-eye split from it and G4 its review categories, so neither asks again |

## Ask good questions

A bad question hands the design work to the user:

```text
How should we handle errors during the import?
```

A good question carries context, a recommendation with its reason, and options that differ in outcome:

```text
Some rows in an uploaded CSV can be invalid. What should the import do with them?
Recommended: b, because the contacts import already works this way (src/import/contacts.ts).
  a) Reject the whole file and list every error
  b) Import the valid rows and offer a download of the rejected rows with reasons (recommended)
  c) Import everything and flag the invalid rows for editing
```

| Anti-pattern | Example | Instead |
|---|---|---|
| Asking a discoverable fact | "Which database do you use?" | Read the config and the models |
| Questionnaire dump | Fifteen questions in one message | Rounds of at most 4 under one theme, highest impact first |
| Leading question | "We should add retries to make it robust, right?" | Neutral options, with the recommendation and its reason stated separately |
| Re-asking what is approved | Asking again about behavior the handoff marked agreed | Import it; ask only when the code contradicts it |
| No default | "Any thoughts on permissions?" | A recommended default and 2–4 options |
| Choosing the approach at G1 | "Redis or Postgres for this?" | Ask for the behavior that drives the choice ("must drafts survive a restart?"); the approach is G2 |
| Inventing targets | Writing "p95 under 200 ms" that nobody said | Ask, or record it as an assumption |

When the user answers "you decide", record the recommended default as an assumption with the basis "delegated by the user" and list it in the G1 summary.

## Write testable acceptance criteria

An AC is one outcome someone can observe from outside the code: the UI, an API response, CLI output, a sent message, or state read back through the product. It uses concrete values, names the R it proves, and has one pass condition. Use Given/When/Then when order matters.

- Weak: `AC2 (R1): Cancelling works reliably.`
- Testable: `AC2 (R1): Given a pending order, when the customer confirms cancellation, the order page shows "Cancelled" and the admin order list shows the order as cancelled.`

Every error or edge behavior the user decided gets an AC. A decided behavior without an AC is a gap that G3 cannot check.

## Reopen the spec

Return here when a later stage finds a contradiction, a missing behavior, or scope growth. Change only the affected requirements and criteria, set `Status: draft`, show the change, and confirm it. Never shrink scope silently to make an approach fit, and never downgrade the track without saying so.

## Hand back

Report the spec path, its status, the counts of requirements and criteria, the assumptions the user accepted, each open question with what it blocks, and the next stage: G2 with `brainstorming-solutions`, or G3 when the track skips G2. A request to specify is not a request to implement: change no product code at this stage. Without file access, return the spec as Markdown and say that no file was written.

## References

| Read | When |
|---|---|
| [interview guide](references/interview-guide.md) | Inspecting the code, handling handoffs and prototypes, ranking unknowns, writing questions, the question bank by topic and track, turning answers into criteria, deciding when to stop |
| [worked interview](references/worked-interview.md) | Calibrating grounding, round size, defaults, the G1 summary, and the spec that results |
| [spec template](templates/spec.md) | Writing `spec.md` |
