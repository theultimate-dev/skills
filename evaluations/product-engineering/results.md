# Observed evaluation results

> The first section records trials of the current nine-skill set. The sections after it cover the 2026-09-06 eight-skill set, which [decision 0009](../../decisions/0009-product-engineering-front-loaded-loop.md) superseded.

## 2026-09-25: trials of the nine-skill loop

Bounded trials of the rebuilt skills, run from Claude Code on macOS with Python 3.13.2. Every agent ran on Opus 5.5. Reviewers and the classifier had no access to this directory. These results come from one host and one trial each; they do not establish repeatability.

### Scenario 7: full-review recall

The coordinating agent followed `reviewing-code-changes` in full mode: it filled one [lens brief](../../skills/product-engineering/reviewing-code-changes/templates/lens-brief.md) per lens, pasted in the lens file, and launched five fresh-context agents in parallel on a fixture copy with [`seeded.patch`](review-recall/seeded.patch) applied (head `3b7963b`). Running code was allowed locally. Findings were graded against the [answer key](review-recall/answer-key.md).

| Trial | P1 security | P2 efficiency | P3 conventions | P4 architecture | P5 intent | N1 | False positives | Noise | Verdict | Category flagged | Lens runs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | found, blocking | found, blocking | found, blocking | found, blocking | found, blocking | reported (security, should-fix) | 0 | 1 | REQUEST CHANGES (from the confirmed blocking findings) | yes: the security lens says the PR is `human`, not the claimed `agent` | parallel agent ×5 |

- Every planted defect was found by its owning lens and confirmed by execution:
  - **P1:** traversal to another principal's attachment, to `records.json` and to `/etc/hosts`.
  - **P2:** 41.3 s for `GET /records` at 50,000 records.
  - **P3:** a DeprecationWarning, and a naive timestamp that fails AC2 on a UTC+2 host.
  - **P4:** 342 of 1,200 exports failed under concurrent saves.
  - **P5:** no export link on the page, and the report's missing AC6 row.
- The lenses stayed in lane: each listed the other planted defects as left to the owning lens.
- The intent lens found the same timestamp and export-lock defects through their effect on the ACs. Synthesis would deduplicate those into P3 and P4.
- **Additional true findings:**
  - the attachment path is built outside `Store`, against the Approach (architecture, should-fix);
  - two weak tests, shown by surviving mutations (intent, should-fix).
- **Noise:** one `unconfirmed` question about streaming large attachments.
- **Not exercised in this trial:** synthesis, posting, and delta rounds.

### Scenario 1: track classification

One agent with only the installed skills classified the seven requests in the scenario catalog and wrote its first message for each. The first attempt ended on an API connection error; the retry is recorded here.

| Request | Track | First message matches the rubric |
|---|---|---|
| Save button copy | quick fix | yes: no interview. It asked the authorization question, with the UI and copy release, open issues and the deploy clause. It added the environment question and a missing-remote question |
| Bob overwrites Alice | bugfix, G1 skipped | yes: reproduced at `ec2825a` before messaging. `Status: agreed (G1 skipped: repro reproduced at ec2825a)`. One message held the short spec, the approach, the repro as the first check, the authorization and deploy questions, and the data-repair scope. No roadmap. The PR is `human` (authorization) |
| Trim title | small change | yes: one interview round, then the batched gates |
| Read-only sharing | feature | yes: G1 round 1, on one theme, with 4 questions, each carrying a recommended default |
| Team reading list | new app | yes: the repository question, and product discovery routed to `guiding-product-discovery` |
| Storage interface | refactor | yes: G1 opens with the invariants. It flagged that characterization would pin the pre-existing owner bug |
| 50,000-record feasibility | spike | yes: question, exit observation, limits and timebox, plus permission for the spike branch in the same message. No spec. Never merged |

**Not yet run:**
- interview quality against a hidden answer sheet (scenario 2);
- real driving with a seeded title (scenario 5);
- merge safety and stacks on a disposable repository (scenarios 9 and 10, which need explicit authorization);
- the scenarios added in the catalog after these trials.

## 2026-09-06: trials of the eight-skill set

Date: 2026-09-06. Initial product-engineering implementation, followed by repairs from independent review. These are bounded trials, not a cross-host reliability benchmark.

Final format validation: `python3 scripts/validate.py` reported **0 errors, 0 warnings**; `git diff --check` passed and evaluation Markdown links resolved. The recorded candidate patch reconstructs the exact app/test hashes in its manifest. The 31-file skill corpus fingerprint is `eaaf1d741606b00f29ce180ca9054ca6c6565b41f7148e195ef193f05de70a97` (SHA-256 over sorted skill-relative paths plus each file's SHA-256, separated by a colon and terminated by a newline).

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

Independent review identified two P2 defects in the initial skill text:

1. A recorder could return Done for an existing event even if interruption had left its checkpoint stale. The instructions now verify both, repair only against the expected prior checkpoint, and preserve established newer state. Follow-up filesystem cases passed.
2. A saved unstaged diff could omit staged changes and untracked implementation/tests. Candidate evidence now covers all relevant content and index/worktree divergence. Mutation/restoration identity cases passed.

The reviewer rechecked both changes and reported no remaining finding in that bounded scope. These corrections were made before final repository validation.

## Reproducible evidence

- [Observed candidate patch](observed-candidate.patch) applies to a copy of `fixture/`; [file hashes](observed-candidate.json) identify original and repaired app/tests.
- [Candidate verification](observed/candidate-verification.md), [review history](observed/candidate-review.md), and [eight-test output](observed/candidate-final-tests.txt) preserve the author's observed results and limitations.
- [Independent candidate review](observed/independent-candidate-review.md) records exact examined hashes and scope.
- [Checkpoint trial results](observed/recording-results.json) and [candidate identity results](observed/snapshot-results.json) preserve post-repair outcomes. Their local fixture paths identify temporary trial files and may expire; assertions and outcomes are retained here.

The main-agent grader command was `python3 evaluations/product-engineering/grade.py <candidate>/app.py`: original fixture **six tests, three failures** after loopback permission; repaired candidate **six passed** in 0.543 seconds. An earlier sandbox run had two assertion failures plus a bind error; that environment failure was not counted as defect detection. The candidate's own eight-test suite passed in 2.110 seconds. Times are observed test-run durations, not complete agent-task latency.

The combined title fixture had three aggregate errors before repair and five passes afterward. Its public contract accepts titles of at most 12 characters after trimming. The repair changed composition from trimming after validation to validation after trimming; original package assertions were retained. This case is reproducible from the exercise description in the evaluation README.

## Remaining evaluation limits

The repaired application has not completed browser acceptance, a deployed-environment check, or PR publication. The skills correctly retain those gaps; backend success is not a claim the full fixture initiative is complete. Live multi-model routing, cross-host portability, repeated stochastic trials, and concurrent-writer/crash behavior require future evaluation. All loopback servers started by the main evaluator were stopped after the trial.
