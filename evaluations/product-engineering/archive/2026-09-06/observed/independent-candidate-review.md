# Independent candidate review

> Historical: recorded during the 2026-09-06 trials of the superseded eight-skill loop. See [the archived results](../results.md).

## Scope and examined candidate

- Requirements: R1 owner update persists across reload/restart; R2 Bob cannot read/update Alice's record and denial leaves state unchanged; R3 browser success/failure feedback and persisted title.
- Agreed fixture architecture: local JSON persistence and simulated X-Principal identity. Production authentication, deployment, and crash-durable databases are outside this review.
- Inspected complete candidate `app.py` and `test_app.py`, including inline browser JavaScript. No author review, justification, grader, answer key, or previous fixture implementation was read.
- Candidate identity below covers the exact two inspected files by SHA-256. No commit/index identity is claimed.

| File | SHA-256 |
|---|---|
| app.py | 9998aba34ae779616b79b0e357786f9d51d560d385037eed054238b83cf5e413 |
| test_app.py | 6247828c56344e861de5bcf007f4eac228cdf4adcb91e834cbc04d15887eeaa9 |

## Round 1: initial independent assessment

### Triage

High-risk attention applies to R2's ownership predicate and mutation ordering despite this being a small fixture. Persistence and browser result handling require substantive review. Review ran in the already assigned reviewer context; no model or effort switch was made or claimed.

### Findings

No actionable defects found within the inspected scope.

### Supporting inspection

- R1: `Store.update` reads current records, validates ownership before mutation, writes the JSON data before returning success (app.py:24–34). Reopening `Store` uses the existing file (app.py:10–15). Tests verify a fresh store and a restarted HTTP server read the saved value (test_app.py:19–21, 84–90).
- R2: reads and writes compare the supplied principal to the stored owner before returning record data or changing persisted content (app.py:17–34). HTTP maps permission failures to an unavailable response without returning the record (app.py:102–105, 111–118). Denial tests assert exact unchanged disk bytes and a subsequent owner's read, covering mutate-then-deny failures (test_app.py:28–35, 92–102).
- R3: browser success depends on an OK HTTP response and renders the returned title; request failures render error feedback (app.py:56–71). Principal changes clear prior title and invalidate in-flight responses; later stale responses cannot restore another principal's view (app.py:50–68). GET failure clears the title. Saving invalid input returns explicit error feedback while preserving disk state (test_app.py:104–109).
- Test quality: assertions observe persisted results and denial invariants using real local JSON and HTTP components. They would reject an in-memory-only update or mutation performed before access denial. The tests do not merely mirror private call structure.

### Limits and handback

This is independent static code/test review, not independent execution evidence. No application server, HTTP requests, browser journeys, or tests were run by this reviewer; the parent is independently executing those checks. Browser behavior, server restart outcomes, and broader acceptance remain dependent on that evidence. No fixture or repository code was changed. No findings need repair or closure. Later changes to either inspected file invalidate affected conclusions.
