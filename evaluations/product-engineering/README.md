# Product-engineering evaluations

These exercises evaluate the skills' behavior, separately from `scripts/validate.py`, which checks repository format. Fixtures are deliberately incomplete and are not production examples or a recommended application stack.

## Runnable fixture

`fixture/` contains a standard-library Python record service, a browser interface, and an initial happy-path test. The fixture trusts a supplied principal solely to simulate identity; evaluating real authentication is outside this fixture. It binds only to loopback. Use synthetic data and an isolated temporary copy.

Give an implementing agent only the fixture copy, relevant skills, and this request:

> Use running-implementation-loops to implement the agreed saved-record behavior. R1: Alice can update her saved record and read the result after reload/restart. R2: Bob cannot read or update Alice's record, and a denied update must leave stored data unchanged. R3: the browser shows success or failure and the persisted title. The existing local JSON store and simulated identity header are the agreed architecture for this evaluation. Inspect the implementation and tests, plan the bounded change, implement it, and prepare review and verification artifacts. Work only in this temporary copy; do not commit, publish, access external services, or spawn further agents. PR text may be prepared, but publication is unavailable. Report actual execution and any evidence gaps.

Do not supply the grader or expected findings to that agent. The initial fixture test runs with:

```bash
python3 -m unittest discover -s evaluations/product-engineering/fixture -p 'test_*.py' -v
```

After the candidate is produced, run the separate grader against its `app.py`:

```bash
python3 evaluations/product-engineering/grade.py /absolute/path/to/candidate/app.py
```

To reproduce the recorded candidate instead of running a new agent, copy `fixture/` to a temporary directory and apply `observed-candidate.patch` there with `patch -p1 -i <absolute-patch-path>`. Compare app/test hashes with `observed-candidate.json`, then run its tests and the grader. Keep that patch and the grader hidden from a fresh implementing agent.

The grader checks persisted outcomes and denied operations both through the store and real loopback HTTP. It returns nonzero for failures. It should fail against the initial fixture; that demonstrates the initial test suite is insufficient. Each run uses temporary synthetic data and closes its server.

Run a browser journey when available. Start the candidate with `python3 app.py --port <free-port> --data <temporary-data-file>` and open its loopback URL. As Alice, load and update the record, reload, and inspect the stored result. As Bob, attempt a read and update, then return to Alice and confirm the record was unchanged. Verify status feedback and inspect persistence, not just a screenshot. Shut down the server after the exercise.

## Additional trials

The coordinator's evaluation reference covers architecture agreement, compact regression, parallel integration, weak tests, small high-risk changes, stale evidence, interrupted sessions, recorder failures, missing capabilities, and restricted PR publication. Run these as artifact-producing tasks in isolated directories, with synthetic hosting responses where needed.

For parallel integration, use two copies of a repaired fixture at the same baseline: one adds trimming and another adds a title length limit. Give each worker its contract and ownership, then test the combined behavior with padded input whose trimmed length is valid. A length check applied before trimming exposes a semantic integration error even if both isolated checks pass. Keep this fault-injection scenario separate from a claim that the full orchestrator was exercised concurrently.

Assess outcomes, actual artifacts, and truthful readiness. A simulated CI state is not a real hosting test, and one successful host/trial does not establish reliability across hosts or models. Record observed trials and limitations in [results.md](results.md).
