# Test design and evidence

## Choose the layer by what must be proven

| Need | Useful check | Common false confidence |
|---|---|---|
| Logic, validation, state invariants | Fast unit/property cases around the behavioral contract | Testing private call order or reimplementing the function in the assertion |
| Persistence, API boundaries, authorization | Integration using real application components and controlled data | Mocking away the boundary under test |
| Critical user journey | E2E through the running application and observable persisted outcome | Only checking a success message while the write failed |
| Visual/interaction intent | Representative viewport and interaction inspection; stable visual checks where useful | Blindly accepting regenerated snapshots |
| Migration or compatibility | Old/new data and caller behavior, failure/recovery checks | Testing only a fresh empty database |
| Performance or concurrency | Representative measured workload against agreed criteria | Invented targets or a single trivial timing sample |
| AI behavior | Representative evaluation cases, deterministic invariants, calibrated quality judgment, repeated trials where needed | A mocked model response presented as quality evidence |

Use the smallest set of checks that gives meaningful coverage. Existing evidence can satisfy an obligation if it actually exercises the current behavior. Coverage reports help locate omissions; no arbitrary percentage proves adequacy.

## Construct durable tests

Start with the actor/caller, trigger, input, observable result, and relevant failure modes. Assert public behavior rather than internal structure. Prefer inputs that discriminate a correct implementation from plausible shortcuts.

For ownership, test two principals and denied reads/writes as relevant, not only a valid owner's happy path. For persistence, verify a later read or restart where required, not just the POST response. For an error path, assert both the failure feedback and that unwanted state changes did not occur.

Control fixtures, clocks, randomness, and data cleanup where they affect determinism. Make tests independently runnable. Keep third-party boundaries controlled and disclose mocks; add separate contract/sandbox verification when a real integration obligation requires it. Never exercise live destructive operations to validate a test without authorization.

For browser tests, use user-facing roles/labels and waiting assertions, isolate session/data state, and avoid fixed sleeps or selectors coupled to incidental DOM structure. Test critical journeys at relevant layouts and input modes. Preserve traces for failures when supported. These practices follow [Playwright guidance](https://playwright.dev/docs/best-practices), reviewed 2026-09-06.

## Check whether the test can catch the defect

A regression test should fail on the original behavior for the intended reason, then pass after the repair. Missing infrastructure or a syntax error is not evidence that the assertion detects the defect. If the original revision cannot be safely executed, record that limit and substantiate the case by another bounded method.

For consequential new behavior, a targeted valid mutation can expose weak assertions: remove an ownership check, bypass persistence, or return a constant result in an isolated copy. Inspect whether the relevant test fails for the right reason. Restore and verify the original candidate; never leave deliberate faults in the working branch.

Do not require mutation testing for every trivial edit. Use it when uncertainty about test strength matters. LLM review of a test is useful analysis, not a replacement for execution.

## Preserve evidence quality

Record the command or inspection procedure, revision, uncommitted snapshot if present, environment, timestamp, result, and evidence reference. Snapshot all relevant tracked modifications, whether staged or unstaged, untracked code/tests, and deletions using hashes or a complete content snapshot. Identify index/worktree divergence; an ordinary unstaged diff cannot identify all tested content. An untracked local screenshot path is not durable shared evidence; identify storage/retention and include an adequate textual observation when needed.

Report initially failed and subsequently passed retries together. Classify and fix a flake rather than increasing retry counts to satisfy the gate. Baseline failures need explicit impact analysis; they cannot be silently ignored or blamed on the branch without checking.

After a repair, rerun the exposing check and impacted regressions. After package integration, validate combined contracts and required project-wide checks. Before PR readiness, CI must correspond to the current PR head. A check attached to an older head does not verify a newer candidate.

For AI work, distinguish deterministic correctness checks from quality evaluations and observe multiple trials where non-determinism matters. Record model/environment details in the project evidence, not fixed model names in this reusable skill. [Agent evaluation guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), reviewed 2026-09-06, explains why outcome checks and calibrated qualitative judgment serve different purposes.
