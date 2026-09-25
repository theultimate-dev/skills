# Interview guide

How to find what the user must decide, ask it well, and know when to stop. The question bank is a menu, not a script: ask only what the code cannot answer and whose answer would change the spec.

## Contents

- Inspect a useful boundary
- Upstream handoffs and prototypes
- Rank the unknowns
- Anatomy of a question
- Running the rounds
- Question bank by topic
- Question bank by track
- From answers to requirements and criteria
- When to stop
- Assumptions and open questions

## Inspect a useful boundary

Start at the changed behavior's entry point and follow its state, dependencies, and failure handling. Read the tests alongside the code. Capture source paths and symbols, the current revision, important constraints, and commands that reproduce the current behavior. Skip a repository-wide inventory when a bounded path answers the question.

Check whether the intended behavior fits the existing interfaces, persistence and migrations, authentication and authorization, deployment topology, observability, and UI conventions. Each mismatch becomes a constraint to record or a question to ask.

Never ask the user for these; read them:

- the stack, frameworks, versions, and test setup
- the current behavior, states, and data model
- similar features and how they behave, which are the best source of recommended defaults
- conventions in AGENTS.md or CLAUDE.md, and accepted decisions in the decision log
- who calls an interface, from the code and its tests
- when a bug started, from the git history

A fact the code shows is not a decision the user made. "The export caps at 10,000 rows" is a fact. Whether the new report keeps the cap is a question.

## Upstream handoffs and prototypes

For a `product-design` handoff, inspect both the intended behavior and the prototype's limitations. A static success screen does not establish persistence, identity, idempotency, accessibility, or real third-party integration. Convert only agreed production behavior into requirements, and surface missing consequential behavior as questions.

| Handoff content | Treatment in the spec |
|---|---|
| Requirement and criterion IDs | Keep them exactly. Number new ones after the highest upstream ID |
| Accepted behavior | Import it as agreed. Do not re-ask it |
| Suggested delivery slices | Note them under Constraints as input for G4. Slicing is decided there |
| Product or design blockers | Return them to `product-design`. Do not decide them here |
| Engineering questions | Add them to the unknowns and rank them |
| Simulated or omitted prototype behavior | Ask when it is consequential, for example when the prototype keeps data in memory and nothing says whether it must survive a reload |

A product brief from `shaping-product-briefs` is handled the same way: its IDs, scope, and exclusions carry over, and its open questions join the unknowns.

## Rank the unknowns

Score each unknown with these questions, in order. The first yes sets its impact. A PR slice is the work that becomes one pull request (merge request).

| Question | If yes |
|---|---|
| Does the answer change what gets built, who can do it, or what an AC asserts? | High |
| Would a wrong guess cost a PR slice or more to undo, or touch data, money, auth, or a public contract? | High |
| Does the answer change an edge or error behavior, or effort within one slice? | Medium |
| Is it a reversible detail the user catches at first sight: copy, placement, a default value? | Low |

Then decide who can answer it:

| Who answers | Treatment |
|---|---|
| The code, the history, or a document in the repository | Read it. Record the fact with its path |
| The user | Ask it in the round for its theme |
| Someone else (legal, a partner, another team) | Record it as an open question with an owner and what it blocks |
| Nobody until something is tried | Record it as an open question; `brainstorming-solutions` can settle it with a spike at G2 |

Within a round, put first the question whose answer may remove other questions. "Whole order only, or single items?" removes every question about partial refunds.

## Anatomy of a question

1. **Context:** one line of what the code or the input already says, with the path.
2. **The decision:** one decision, stated neutrally.
3. **The recommended default and its reason:** prior art in the repository, a project convention, the smallest scope that meets the outcome, or the more reversible choice.
4. **Options:** 2–4 that differ in outcome, each short enough to scan. Mark the recommended one.

With the host's structured-question tool (for example AskUserQuestion in Claude Code), send one round per call: up to 4 questions, 2–4 options each, a short header per question, the recommended option listed first with "(recommended)" in its label. When the tool adds a free-text answer itself (AskUserQuestion does), do not spend an option on "Other"; otherwise use the numbered list below.

A round holds up to 4 questions under one theme the user can hold in mind, such as the cancellation rule. A theme may span several topics of the question bank.

Without such a tool, send the round as a numbered list and say how to answer:

```text
Round 2 of about 3: failures. Reply like "1b, 2 ok"; "ok" takes the recommendation.

1. The payment provider times out during the refund. What does the customer see?
   Recommended: a, the same as the staff flow in src/admin/orders/cancel.ts.
   a) Nothing changes; an error asks them to try again (recommended)
   b) The order cancels and the refund is queued for a retry
```

## Running the rounds

- Announce the theme and the estimated number of rounds left, so the user can budget attention.
- Wait for the answers before the next round. Never send two rounds at once.
- Take free-text answers literally. An answer that adds a condition ("yes, but only after they confirm their email") is a new requirement, not a nuance to drop.
- When an answer contradicts an earlier answer or the code, resolve it in the next round before anything else.
- "You decide" is delegation. Record the recommended default as an assumption with the basis "delegated by the user" and list it in the G1 summary.
- "I don't know" on a high-impact question becomes an open question with an owner. Offer the recommended default as a provisional assumption the user can accept.

## Question bank by topic

Each line is the decision behind the question. Phrase it with context, a default, and options, as above.

**Why and outcome**
- Which problem matters most, when the request names several? This decides the non-goals.
- What outcome tells the user it worked? Ask only when it changes scope.

**Actors and permissions**
- Who can perform the action: signed-in users, guests, admins, API clients, scheduled jobs?
- Can one actor act on another's data: team members, admins acting on behalf of users?
- What happens when a permission is revoked mid-flow?

**Scope and non-goals**
- What is the smallest version that reaches the outcome? Offer it as the default.
- What is explicitly out, and what is deferred to a later work item?
- Which surfaces are in: web, mobile, API, email, CLI?

**Behavior**
- The main path: trigger, what the user sees, what changes elsewhere (lists, counts, notifications, other users).
- State transitions: from which states the action is allowed, and which state results.
- Defaults when the user supplies nothing.

**Errors and edge cases**
- Invalid input: reject, repair, or accept with a flag?
- Empty, one, many, and very large inputs.
- Concurrent change: two users, or the state changes while the user is deciding.
- A downstream call fails: roll back, retry, or leave a flagged state?
- Repeated actions: a double submit, a retry after a timeout.
- Expired sessions and stale links.

**Data**
- Where the data comes from and who owns it.
- Existing data: migrate it, backfill it, or leave it untouched?
- Retention and deletion, and whether personal data is involved.
- Volume and growth that bound the approach.

**Non-functionals** (only the ones this item touches)
- Performance: a number only when the user states or accepts one; otherwise "no slower than today on [dataset]".
- Security and privacy: who must never see what.
- Accessibility: the project's standard; keyboard and screen-reader paths for new UI.
- Compatibility: browsers, API versions, older clients, rollback.
- Observability: what must be logged or measured to know it works in production.

**Constraints**
- A deadline, a release train, or a freeze.
- Dependencies the user wants or forbids.
- Policies outside the repository: legal, compliance, partner contracts.

**Done and review**
- What will the user check themselves before calling this done?
- Which parts does the user want to review before merge? A good default names anything touching money, auth, personal data, or migrations, plus visible UI and copy.
- Does the user want to see each PR, or only the finished work item?

Record the answers on the spec's Done and review line. G3 and G4 start from that line and do not ask again.

## Question bank by track

**Bugfix**
- Repro: exact steps, environment, account or data, frequency (always, sometimes, once).
- Expected vs. actual, in the user's words.
- Blast radius: who else is affected, since which release or commit, and whether data is now wrong.
- When data is wrong: is repairing it in scope, or only preventing new damage?

Reproduce the bug yourself when that is cheap and safe: locally, never against production. Skip the interview and G1 only when it reproduces: restate the steps and the expected result as the short spec, with `Status: agreed (G1 skipped: repro reproduced at <short-sha>)`. A report that does not reproduce is a high-impact unknown: ask for the missing condition. When reproducing is not cheap or safe, the short spec stays `Status: draft` until the user confirms it.

**Small change**
- One round, two at most: the behavior, the one or two edge cases that matter, and what is out.

**Feature**
- Every topic above, in two to four rounds.

**New app**
- Product interview, labeled as such, only when `guiding-product-discovery` is not installed or the user declines it: who it is for, the one job it must do first, the first usable slice, what it replaces today (a spreadsheet, another tool), and what is excluded.
- Engineering interview: where it must run (hosting, devices, offline), who signs in and how, what data it holds and how sensitive it is, integrations, a cost ceiling, who maintains it, and any language or platform the user imposes.
- The stack is chosen at G2 and the verification harness at G3. Ask here only about environments and accounts the user already has.

**Refactor or migration**
- What must not change: public API, behavior, data, performance envelope, URLs, CLI flags, file formats.
- What the new structure must make possible. This is the one requirement that is not an invariant.
- What may change: internal names, module boundaries, private interfaces.
- How it lands: small mechanical PRs, and how long old and new code may coexist.

Each invariant becomes an AC, for example: `AC1 (R1): every request in the characterization suite returns the same status and body before and after the change.`

## From answers to requirements and criteria

- A requirement states one capability or rule from the user's or caller's side: `R2: A customer can cancel an order while it is pending.` Never a component: `R2: Add a CancelButton.`
- An acceptance criterion is one observable outcome that proves a requirement, with concrete values: "with 3 items", not "with some items". It names its R.
- Cover the main path and every error or edge behavior the user decided.
- A non-functional the user wants checked becomes a requirement with a measurable AC. One that only bounds the solution goes under Constraints.

| Weak | Why it fails | Testable |
|---|---|---|
| Cancelling works reliably | No observable outcome | Given a pending order, when the customer confirms cancellation, the order page shows "Cancelled" and the full amount is refunded |
| The list is fast | No number, no condition | With 5,000 orders, the first page of the list renders within 1 s on the staging dataset (target accepted by the user) |
| Errors are handled gracefully | Which error, what happens | When the refund call fails, the order stays pending and the customer sees "We couldn't cancel your order. Try again in a minute." |
| Uses the new OrderService | Implementation, not behavior | Drop it. The approach is decided at G2 |

## When to stop

Stop when all of these hold:

- Every R has at least one AC, and every AC names its R.
- Every AC is observable from outside the code and has one pass condition.
- No high-impact unknown is open, unless the user accepted an assumption in its place.
- The non-goals name what a reasonable reader would otherwise expect.
- The user's review expectations are recorded under Constraints.

Stop earlier when the user asks to proceed. Record the rest as assumptions and flag the high-impact ones in the summary.

When the user declines to answer ("just build it", "no more questions"), stop asking. Record every open unknown as an assumption with its recommended default and the basis "delegated by the user", and send the G1 summary once. A "go ahead" to that summary is agreement.

Round budget: bugfix 0–1, small change 1–2, feature 2–4, new app 3–5 across both interviews. Needing more signals a work item that should be split. Propose the split as the next question.

## Assumptions and open questions

Write each on one line:

```text
- Assumption: no cancellation reason is collected. Basis: not asked: low impact. If wrong: one optional field and a feed change.
- Open: how long cancelled orders are retained. Blocks: nothing before implementation. Owner: the shop-operations lead.
```

The basis is one of: accepted default, delegated by the user, inferred from code (with the path), or not asked: low impact. An assumption the user never saw is not agreed. The G1 summary lists every high- and medium-impact assumption; low-impact ones stay visible in the spec the user confirms.
