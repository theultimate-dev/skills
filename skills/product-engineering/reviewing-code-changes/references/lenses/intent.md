# Intent lens

Judge whether the change solves the problem the spec describes. Every acceptance criterion in scope is implemented and actually exercised, the logic holds at its edges, the tests would fail on a plausible wrong implementation, and nothing outside the scope changed. Quick mode runs this lens alone.

## Read first

1. The spec: Problem, Requirements (`R1`, `R2`, …), Acceptance criteria (`AC1`, `AC2`, …, each naming its R), Non-goals, Constraints, Approach, and the Verification section's agreed check for each AC.
2. The plan file, for the ACs and the phase this PR slice covers. A slice can cover some ACs only; the others are out of scope for this review.
3. The verification report: the SHA it ran on, and one row per AC with the result, what was done and what was observed.
4. Outside the loop there is no spec. Take the stated intent from the linked issue, the problem the PR description states, and the commit messages. Write the intent you reviewed against in one or two sentences at the top of your output.

## Check

1. **Every AC in scope.** Build a matrix with one row per AC in this slice: where it is implemented (file and line), which test or verification check exercises it, and the result the report records. An AC with no implementation, or with no observed check that still holds for this head (see check 5), is a finding.
   - On a bugfix, the reproduction's test fails on the base SHA and passes at the head. Run it on both when the report does not show both.
   - On a refactor, the spec lists invariants instead of new behavior. Check each invariant, and check that the characterization tests are unchanged.
2. **Correctness on the paths the diff touches.** Walk the changed code with concrete inputs, in the categories the code actually touches:
   - boundaries: off-by-one, inclusive or exclusive ranges, the first and last page, zero, the maximum;
   - absence: null, undefined, an empty string or collection, a missing optional field;
   - error paths: a dependency fails or times out, partial writes are rolled back or completed, the user sees a correct message;
   - state and ordering: idempotent retries, double submission, concurrent updates to the same record, multi-step writes that must be atomic;
   - time and text: time zones, daylight saving, locale, Unicode, rounding of money.
3. **Tests assert the intended behavior.**
   - Each test checks the AC's observable outcome, not an implementation detail.
   - Name a plausible wrong implementation and ask whether the test fails on it: a handler that returns the error but writes first, a filter that returns everything, a sort tested with one item.
   - A test that asserts a mock returned what it was told to return proves nothing.
   - Mocks stop at the boundary the plan allows. The boundary under test is real.
   - Deleted tests, skipped or focused tests (`.skip`, `.only`), loosened expected values, and snapshots updated to accept wrong output are always findings. They also make the PR `human`.
   - When test strength decides a finding, break the behavior in a scratch copy (remove the check, return a constant), run the test, confirm it fails for the right reason, and discard the copy.
4. **Scope.** Flag changes outside the plan slice: behavior the spec does not ask for, refactors of untouched code, anything the Non-goals exclude. Flag missing pieces: stubs, TODOs standing in for required behavior, a requirement the slice claims but does not deliver. A behavior change beyond the spec is scope growth, and the user decides it.
5. **The verification report matches the code.** It ran on this head, or on an earlier SHA whose diff to this head does not touch the verified behavior. Each observation is consistent with the code: a message the report says it saw is the message the code renders. No blocked check is counted as a pass. Mocked checks are labeled.
6. **User-facing text.** Documentation, changelog entries, error messages and UI copy match the new behavior.
7. **Fix rechecks.** In a delta round or a quick-mode recheck, read each fix, rerun the trigger of the finding it claims to close, and check the neighboring behavior the fix could break.

## Quick mode

You are the only reviewer before the PR opens. Stay with this lens. Also report any confirmed defect you notice outside it, labeled with the lens it belongs to (`architecture`, `security`, `conventions` or `efficiency`), but do not hunt for them: the full review on the PR covers those lenses.

## Leave to other lenses (full mode)

- Security consequences, including a missing ownership check: security. Report one here as well only when it breaks an AC.
- Structure and reuse: architecture.
- Style and idioms: conventions.
- Cost: efficiency. An AC's own performance pass condition stays here.

## Evidence bar

- Tie each finding to an R or AC ID, or to the stated intent outside the loop.
- Give the concrete input or sequence, the result the spec expects, and what the code does instead.
- Reproduce when the tests or the app can run: run the targeted test, add a scratch test, or drive the app locally as the verification profile describes. Use only local or disposable environments.
- For a weak test, name the wrong implementation that would still pass it.
- A missing check is a different finding from wrong code. Say which one it is: code that does the wrong thing, a check that was never run, or a check that could not run (blocked).

## Severity

| Severity | Intent examples |
|---|---|
| `blocking` | An in-scope AC not implemented, or broken. A confirmed defect on an AC path: a wrong result, a crash, data loss, a lost write. A test that asserts the wrong behavior. An in-scope AC with no observed check that still holds for this head. A claim in the verification report that the code contradicts. A behavior change outside the spec. |
| `should-fix` | A confirmed defect on an edge path outside the ACs. A changed branch with no test where the project tests such branches. A weak test that a named wrong implementation passes. An unrelated refactor mixed into the PR. |
| `nit` | A test name, a clearer assertion message, a tighter fixture. |

A confirmed defect in changed code is never a nit.

## Output

Start with the AC matrix, one line per AC in scope: `AC<n>: <file:line> | <test or check> | <report result>`. Then return one block per finding, most severe first:

```text
lens: intent
file: <path>
line: <line at the head SHA>
severity: blocking | should-fix | nit
status: confirmed | unconfirmed
summary: <one sentence: what is wrong>
trigger: <the input or sequence; what the spec expects versus what the code does>
impact: <who is hurt, and how badly>
evidence: <quoted code, a command and its output, or the reproduction>
basis: <the R or AC ID, or the stated intent>
direction: <a suggested fix, without an unrelated refactor>
```

After the blocks, add one line: `Checked: <paths, inputs and tests you examined>`.

When the diff changes no behavior, tests or user-facing text, answer only `intent: nothing in scope (<reason>)`. When you checked and found nothing, give the AC matrix and then `intent: no findings. Checked: <paths, inputs and tests you examined>`.
