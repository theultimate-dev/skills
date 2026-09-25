# Test quality

A green suite says the tests passed. It does not say the tests would fail if the behavior broke. This file is about the second question.

## Contents

- The question
- Weak-test patterns
- Fail before, pass after
- Fault injection
- Flaky results
- Model-backed features
- Limits to state
- What never counts

## The question

For each criterion covered by automated tests, ask: what plausible wrong implementation would still pass? Then look at:

- **Assertion strength:** the test checks the value the user would see or the state that must exist, not only "no error" or "truthy".
- **Contract coverage:** the test covers the criterion's condition, including its failure mode, not a neighboring behavior.
- **Fixture realism:** the data resembles production shape: several records, several users, existing data, not one pristine row.
- **Isolation and determinism:** the test sets up its own data, runs in any order, and controls clocks and randomness.
- **Resilience:** a harmless refactor of internals would not break it.
- **Relevance:** a test can be correct and still prove nothing about the requirement.

## Weak-test patterns

| Pattern | Why it proves little | Stronger |
|---|---|---|
| Asserts only the success message | The write can fail behind a success toast | Assert the record after a reload or in the store |
| Mocks the boundary under test | The real query, request or permission check never runs | Use the real component with controlled data; mock only third parties |
| Checks the owner's happy path only | Missing authorization passes | Add the denied read and write as a second principal |
| Asserts call order or private helpers | Breaks on refactor; misses wrong results | Assert public output and effects |
| Snapshot regenerated with the change | The new output is accepted without being read | Review the snapshot diff, or assert the specific values |
| `toBeTruthy`, `not.toThrow`, status only | Wrong values pass | Assert the exact value, message or field |
| Fixed sleeps | Flaky, and hides races | Wait for the condition |
| Depends on another test's data | Passes only in one order | Create the data inside the test |
| Catches the error and passes | The failure path is never asserted | Assert the error and that no state changed |

## Fail before, pass after

A regression test proves itself by failing on the code that had the bug.

1. Create an isolated worktree at the slice's base, outside the working tree, under the run directory for this SHA:
   ```sh
   RUN_DIR="${TMPDIR:-/tmp}/verify-$(git rev-parse --short HEAD)"; mkdir -p "$RUN_DIR"
   git worktree add "$RUN_DIR/base" "$(git merge-base HEAD origin/<base>)"
   ```
2. Copy only the new test into it, and run that one test.
3. It must fail for the reported reason: the assertion shows the wrong value. A missing import, a compile error or absent infrastructure does not count.
4. Run the same test on the candidate SHA. It passes.
5. Remove the worktree: `git worktree remove --force "$RUN_DIR/base"`.

Record both SHAs and the failure message in the report. When the base cannot run, say why, and support the test by another bounded method, such as a unit reproduction of the faulty function.

## Fault injection

Use it for consequential behavior: permissions, money, data loss, persistence, and any criterion that only automated tests cover. Skip it for trivial edits.

1. Create an isolated worktree at the candidate SHA, under the same run directory:
   ```sh
   RUN_DIR="${TMPDIR:-/tmp}/verify-$(git rev-parse --short HEAD)"; mkdir -p "$RUN_DIR"
   git worktree add "$RUN_DIR/fault" <sha>
   ```
2. Inject one plausible fault that still compiles:

   | Behavior | Fault to try |
   |---|---|
   | Ownership or authorization | Remove the owner check, or compare against the wrong id |
   | Persistence | Skip the save call, or save to a field nobody reads |
   | Validation | Drop one rule, or widen a limit by one |
   | Calculation | Return a constant, or swap two operands |
   | Boundaries | Change `<` to `<=` |
   | Error handling | Swallow the error and return success |

3. Run the test that should catch it. It must fail, for the right reason.
4. Remove the worktree. Confirm the main working tree is untouched: `git status` is clean and `git rev-parse HEAD` equals the SHA.

A fault that survives is a test gap. Report the exact fault and the test that missed it, and return it to implementation like a failure. Never commit a mutant, and never inject faults in the working branch.

## Flaky results

- A row that failed and then passed on retry is `fail`, unless the first failure was a quoted tool error. Report both outcomes, with the first failure's message.
- A flaky check in code this slice touches is a test defect: return it to `implementing-plans` like a failure. A flaky check in code the slice does not touch is a follow-up in the report, with both outcomes.
- Look for the cause: shared data, ordering, time, a fixed sleep, an unhandled race.
- Never raise retry counts or timeouts just to make a check pass.
- A failure on the base as well is a baseline failure. Report it as such; it is neither ignored nor blamed on the candidate without evidence.

## Model-backed features

Separate deterministic checks (output format, invariants, refusal of bad input) from quality evaluation. Run the agreed evaluation cases the agreed number of times and report the spread, not the best run. A mocked model response proves the code around the model, never the model's quality. Record the model and settings used in the report.

## Limits to state

Name the limit in the report's mocks and limits subsection when it applies:

- Browser automation is not a user study.
- A clean accessibility scan is not full conformance.
- Deterministic tests do not prove the quality of a model-backed feature.
- A local timing does not predict production performance.
- Seed-sized data does not predict how long a migration or backfill takes in production.

## What never counts

- Reading a test, or a model's opinion of it, instead of running it.
- A compile error from an invalid mutant, presented as the test catching the fault.
- A snapshot or expectation weakened because the candidate changed.
- A coverage percentage presented as proof of adequacy.
