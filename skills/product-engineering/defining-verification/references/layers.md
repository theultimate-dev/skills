# Layers, pass conditions and durable checks

## Contents

- Verification target
- The layer table
- Choosing the layer
- Writing pass conditions
- Durable tests
- Regressions: fail before, pass after
- Refactors: characterization and before-and-after journeys
- Mocks and sandboxes

## Verification target

Every row names a check the agent can run and read: a test suite, a build, a request whose response it reads, a journey whose screen it reads, a script that diffs output against a fixture. Without one, "looks done" is the only signal, and the user ends up doing the verification. The evidence the row produces is what the agent quotes in the report: the command and its output, the text on screen, the row in the database.

## The layer table

Use these names in the Layer column.

| Layer | Proves | Use for | False confidence to avoid |
|---|---|---|---|
| `unit` | Logic in isolation | Validation, calculations, state transitions, invariants | Asserting private call order; reimplementing the function inside the assertion |
| `integration` | Real components work together | Persistence, queries, boundaries inside the app, a library's public API | Mocking away the boundary under test |
| `api` | The running service honors its contract | Status, payload, errors, access for two principals | Checking the status only, not the body or the persisted effect |
| `e2e` | A user completes the journey in the running app | Every user-facing criterion; critical journeys | A success message on screen while the write failed |
| `cli` | The command behaves for its user | Output, exit codes, files written, errors on stderr | Checking exit code 0 only |
| `job` | Background work happens once and correctly | Queued or scheduled work, retries, idempotency | Calling the handler directly and never enqueueing |
| `migration` | Existing data and existing callers survive | Schema changes, backfills, compatibility | Testing only a fresh, empty database |
| `visual` | Layout and appearance match the agreed intent | Responsive layout, agreed design; taste goes to the human eye | Accepting regenerated snapshots without looking |
| `accessibility` | Keyboard and assistive-technology basics hold | Forms, dialogs, navigation: roles, names, focus order | A clean scanner run presented as full conformance |
| `performance` | A measured workload meets an agreed number | Only when the spec states a number | An invented target; one timing sample |
| `ai-eval` | Model-backed behavior is good enough | Representative cases, deterministic invariants, repeated trials | A mocked model response presented as quality evidence |

## Choosing the layer

1. Start from what must be proven, not from the test tooling that exists.
2. Take the lowest layer that proves it. Logic proven by a `unit` row does not need an `e2e` row to prove it again.
3. A criterion a user can observe also gets one row through the running product: `e2e`, `api` or `cli`. Unit tests alone never pass it.
4. Add a second row for the failure mode that matters most: the denied user, the invalid input, the lost connection.
5. An existing test counts when it exercises the current behavior. Cite it by path and name.
6. No coverage percentage proves adequacy. Coverage reports only locate omissions.
7. A `performance` row needs a number the user agreed. Without one, leave performance out rather than invent a target.

## Writing pass conditions

A pass condition states what someone watching would see, specifically enough that a wrong implementation would not satisfy it.

| Weak | Observable |
|---|---|
| Creating a task works | After reload, the list shows the title entered in step 2 exactly once, and no console error appeared |
| Shows an error for an empty title | Submitting an empty title shows "Title is required" next to the field, and no request to create a task is sent |
| Other users cannot access it | As user B, `GET /api/tasks/<id of A's task>` returns 404 and the body contains no title |
| Export works | The command exits 0, and `out.csv` has a header plus one line per seeded record |
| Sends a confirmation | The mail catcher holds one message to the seeded address, with the order number in the subject |
| Fast enough | The p95 of 50 local requests is under 300 ms (only when the user agreed this number) |

Rules:

- Name the persisted side effect: after reload, after restart, in the database, in the file.
- Use a value generated at run time, such as a title with a timestamp, so the observation proves this run.
- For an error path, state both the feedback and the state that must not change.
- Never write "works", "correct", "as expected", "properly" or "looks good".

## Durable tests

Rows that become automated tests follow these rules.

- Start from the actor, the trigger, the input, the observable result and the failure modes.
- Assert public behavior, not internal structure. Prefer inputs that tell a correct implementation from a plausible shortcut.
- Ownership: test two principals, and the denied read and write, not only the owner's happy path.
- Persistence: assert a later read, or a restart where the spec requires it, not the create response.
- Error paths: assert the feedback and that no unwanted state change happened.
- Control clocks, randomness, fixtures and cleanup. Each test runs on its own, in any order.
- Keep third-party boundaries controlled and labeled. A real integration obligation gets a separate sandbox or contract check.
- Browser tests locate elements by role, label or visible text, use assertions that wait for a condition, isolate session and data per test, avoid fixed sleeps and selectors tied to incidental markup, and keep traces for failures. These follow the [Playwright best practices](https://playwright.dev/docs/best-practices), reviewed 2026-09-25.
- Never exercise a live destructive operation to validate a test.

## Regressions: fail before, pass after

For a bugfix, the repro is the first row, and it becomes a failing check before the fix.

1. Write the check against the reported behavior.
2. Run it on the base SHA. It must fail for the reported reason: the assertion fails with the wrong value. A missing import, a compile error or absent infrastructure does not count.
3. Record the base SHA and the failure message.
4. After the fix, the same check passes on the candidate SHA.

When the base cannot run, record why, and support the row by another bounded method, such as a unit reproduction of the faulty function.

## Refactors: characterization and before-and-after journeys

A refactor promises no behavior change, so the checks capture behavior before the first edit.

1. List the invariants from the spec: outputs, error messages, API responses, stored formats, performance numbers if any.
2. On the base SHA, write characterization tests that pin the current outputs, including odd behavior. Odd behavior is pinned, not fixed.
3. Drive the main journeys on the base SHA and record what was observed as text: screens, responses, exit codes, files.
4. Pass condition for every row: the same observation on the candidate SHA. Any difference fails, unless the spec lists it as intended.

## Mocks and sandboxes

Label every mock, stub or sandbox in the contract with what it excludes: "payment provider in test mode: excludes real card-network responses and payouts". A mocked response is evidence about the code around it, never about the thing it replaced. For model-backed features, separate deterministic checks (format, invariants, refusal of bad input) from quality evaluation, and run repeated trials where outputs vary.
