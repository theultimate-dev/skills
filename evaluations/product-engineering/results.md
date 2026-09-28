# Observed evaluation results

> This file records trials of the current nine-skill set. The 2026-09-06 trials of the eight-skill set, which [decision 0009](../../decisions/0009-product-engineering-front-loaded-loop.md) superseded, are [archived](archive/2026-09-06/results.md) for history; they are not evidence about the current loop.

## 2026-09-25: trials of the nine-skill loop

Bounded trials of the rebuilt skills, run from Claude Code on macOS with Python 3.13.2. Every agent ran on Opus 5.5. Reviewers and the classifier had no access to this directory. The skills commit was not recorded: the trials ran against the uncommitted working tree that was committed minutes later as `83e0ab1`, so small differences from that commit cannot be ruled out. These results come from one host and one trial each; they do not establish repeatability, and the catalog asks for at least three trials of scenarios 1 and 7.

### Scenario 7: full-review recall

The coordinating agent followed `reviewing-code-changes` in full mode: it filled one [lens brief](../../skills/product-engineering/reviewing-code-changes/templates/lens-brief.md) per lens, pasted in the lens file, and launched five fresh-context agents in parallel on a fixture copy with [`seeded.patch`](review-recall/seeded.patch) applied (head `3b7963b`). Running code was allowed locally. Findings were graded against the [answer key](review-recall/answer-key.md).

| Trial | P1 security | P2 efficiency | P3 conventions | P4 architecture | P5 intent | N1 | False positives | Noise | Verdict | Category flagged | Lens runs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | found, blocking | found, blocking | found, blocking | found, blocking | found, blocking | reported (security, should-fix) | 0 | 1 | REQUEST CHANGES, inferred by the evaluator from the confirmed blocking findings; no verdict line was produced | yes: the security lens says the PR is `human`, not the claimed `agent` | parallel agent ×5 |

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
- **Against the pass bar:** P1 and P5 were confirmed `blocking`, the category was flagged `human`, and no false positive was reported. Because synthesis did not run, no verdict line opened the round naming the full head SHA, so this trial does not meet the scenario's bar in full. Per-lens recall needs at least three trials; this is one.

### Scenario 1: track classification

One agent with only the installed skills classified the seven requests in the scenario catalog and wrote its first message for each. The first attempt ended on an API connection error; the retry is recorded here.

| Request | Track | First message matches the rubric |
|---|---|---|
| Save button copy | quick fix | partial: no interview. It asked the authorization question, with the UI and copy release, open issues and the deploy clause. It then added two more questions, the environment and a missing remote, where the rubric allows at most one |
| Bob overwrites Alice | bugfix, G1 skipped | yes: reproduced at `ec2825a` before messaging. `Status: agreed (G1 skipped: repro reproduced at ec2825a)`. One message held the short spec, the approach, the repro as the first check, the authorization and deploy questions, and the data-repair scope. No roadmap. The PR is `human` (authorization) |
| Trim title | small change | yes: one interview round, then the batched gates |
| Read-only sharing | feature | yes: G1 round 1, on one theme, with 4 questions, each carrying a recommended default |
| Team reading list | new app | yes: the repository question, and product discovery routed to `guiding-product-discovery` |
| Storage interface | refactor | yes: G1 opens with the invariants. It flagged that characterization would pin the pre-existing owner bug |
| 50,000-record feasibility | spike | yes: question, exit observation, limits and timebox, plus permission for the spike branch in the same message. No spec. Never merged |

**Not yet run.** Only scenarios 1 and 7 have results, one trial each. None of these has run yet:
- scenarios 2 to 6 and 8 to 17 of the [scenario catalog](evaluation-scenarios.md): interview quality, brainstorm distinctness, the verification contract, real driving, quick review, categorization, merge safety, stacks, resume, missing capabilities, intake authorization, G4 autonomy questions, the refactor and spike tracks end to end, and the finish report;
- the runnable bugfix trial in the [evaluation guide](README.md#runnable-fixture).

So the behaviors the repository README states for merging and verification are designed and documented but not yet observed: merge safety and stacks on a real host (scenarios 9 and 10), driving the running app (scenario 5), and reporting a check as `blocked` on a host without the capability (scenario 12).
