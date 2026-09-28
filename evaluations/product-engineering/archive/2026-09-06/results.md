# 2026-09-06: trials of the eight-skill set

> Kept for history only. These trials exercised the superseded eight-skill loop of [decision 0007](../../../../decisions/0007-product-engineering-loop.md), which [decision 0009](../../../../decisions/0009-product-engineering-front-loaded-loop.md) replaced with the current nine skills. Several behaviors below, such as recording worklogs, checkpoints and candidate snapshots, no longer exist in the skills. Nothing here is evidence about the current loop; see [results.md](../../results.md) for that.

Date: 2026-09-06. Initial product-engineering implementation, followed by repairs from independent review. These are bounded trials, not a cross-host reliability benchmark.

Final format validation: `python3 scripts/validate.py` reported **0 errors, 0 warnings**; `git diff --check` passed and evaluation Markdown links resolved. The recorded candidate patch reconstructs the exact app/test hashes in its manifest. The 31-file skill corpus fingerprint of the eight-skill set was `eaaf1d741606b00f29ce180ca9054ca6c6565b41f7148e195ef193f05de70a97` (SHA-256 over sorted skill-relative paths plus each file's SHA-256, separated by a colon and terminated by a newline).

## Environment and method

Three independent subagent evaluators produced artifacts in isolated temporary directories. The main agent inspected outputs, independently ran the application grader and integration suite, and exercised the running application through Chrome. Python 3.13.2 on macOS; synthetic local JSON data and simulated principals. HTTP checks used real loopback servers after sandbox binding restrictions were resolved through approval.

Evaluators used inherited models. Actual model-tier switching, effort enforcement, token/cost measurements, concurrent implementation agents, remote CI, and PR publication were not exercised. Review and execution independence are recorded separately. No repository commits or external publication occurred.

## Outcomes

| Trial | Observed result | Judgment and limit |
|---|---|---|
| Product handoff to architecture | Produced spec/context preserving requirements and approved layout; proposed persistence/identity options and left consequential choices unapproved | Passed artifact trial; supplied prototype state was simulated, not executed |
| Compact regression and weak tests | Original saved-record happy-path test passed; independent grader found three authorization failures, including an HTTP update that changed another owner's record | Demonstrated that green initial tests missed required behavior |
| Bounded implementation and repair | Implementing evaluator added denial, unchanged-state, reopen/restart, and HTTP checks; repaired ownership before mutation and browser identity state | Eight authored tests passed; browser acceptance remained explicitly pending |
| Independent backend acceptance | Separate grader ran six checks against the repaired candidate, including actual HTTP and persisted state | All six passed; grader was withheld from implementer |
| Independent code/test review | Reviewer inspected candidate before author conclusions and identified no further actionable defects against R1–R3 | Static independent review passed; does not establish browser execution |
| Browser baseline and candidate | Baseline browser allowed Bob's update and displayed Saved. Repaired browser loaded Alice's record. Subsequent save/state operations timed out and browser control became unavailable | Partial: repaired save/reload, identity switching, denial feedback, and stale-response behavior were not fully verified; F002 remains awaiting runtime verification |
| Integrated packages | Original two isolated package checks passed; added aggregate checks exposed three errors from validating before trimming | Repair passed all five checks; main agent independently reran them. Pure-function integration fixture, not concurrent-agent execution |
| Stale PR evidence and restricted publication | Prepared PR text only; identified old-head review/CI as stale, current-head CI pending, house commit convention and unrelated dirty file to preserve | Passed simulated hosting-state trial; no real PR/CI inspection |
| Worklog duplicate and conflicting event | Identical retry retained one event; changed payload for the same ID returned conflict, preserved file bytes, and never upgraded a reported result to verified | Passed actual filesystem trial |
| Interrupted checkpoint and later retry | Retried an already-persisted event with missing checkpoint; repaired it without duplicate history. Older retry preserved a newer checkpoint; conflicting predecessor returned conflict | Passed post-repair fixture assertions; no process-crash or simultaneous-writer injection |
| Full candidate identity | Captured staged bytes, divergent worktree bytes, and untracked test; each independent mutation changed identity and restoration reproduced it | Passed actual temporary Git/index trial with unborn HEAD; no commits |
| Missing runtime capabilities | Evaluators disclosed unavailable model switching, self-review, browser checks, and publication without claiming full completion | Passed fallback behavior in these trials; other hosts untested |

## Skill defects found and repaired

Independent review identified two P2 defects in the initial skill text of the eight-skill set:

1. A recorder could return Done for an existing event even if interruption had left its checkpoint stale. The instructions were changed to verify both, repair only against the expected prior checkpoint, and preserve established newer state. Follow-up filesystem cases passed.
2. A saved unstaged diff could omit staged changes and untracked implementation/tests. Candidate evidence was changed to cover all relevant content and index/worktree divergence. Mutation/restoration identity cases passed.

The reviewer rechecked both changes and reported no remaining finding in that bounded scope. These corrections were made before final repository validation. Both behaviors left the skills with decision 0009.

## Reproducible evidence

- [Observed candidate patch](observed-candidate.patch) applies to a copy of `fixture/`; [file hashes](observed-candidate.json) identify original and repaired app/tests.
- [Candidate verification](observed/candidate-verification.md), [review history](observed/candidate-review.md), and [eight-test output](observed/candidate-final-tests.txt) preserve the author's observed results and limitations.
- [Independent candidate review](observed/independent-candidate-review.md) records exact examined hashes and scope.
- [Checkpoint trial results](observed/recording-results.json) and [candidate identity results](observed/snapshot-results.json) preserve post-repair outcomes. The evidence files they name (`logs/*.md`, `test_logic.py`) were temporary trial files and are not in this repository; the assertions and outcomes are retained here.

The main-agent grader command was `python3 evaluations/product-engineering/grade.py <candidate>/app.py`: original fixture **six tests, three failures** after loopback permission; repaired candidate **six passed** in 0.543 seconds. An earlier sandbox run had two assertion failures plus a bind error; that environment failure was not counted as defect detection. The candidate's own eight-test suite passed in 2.110 seconds. Times are observed test-run durations, not complete agent-task latency.

The combined title fixture had three aggregate errors before repair and five passes afterward. Its public contract accepts titles of at most 12 characters after trimming. The repair changed composition from trimming after validation to validation after trimming; original package assertions were retained. This case is reproducible from the [exercise description](../../README.md#parallel-integration-exercise) in the evaluation guide.

## Remaining evaluation limits

The repaired application did not complete browser acceptance, a deployed-environment check, or PR publication. The skills of that set retained those gaps; backend success was not a claim the full fixture initiative was complete. Live multi-model routing, cross-host portability, repeated stochastic trials, and concurrent-writer/crash behavior were left for future evaluation. All loopback servers started by the main evaluator were stopped after the trial.
