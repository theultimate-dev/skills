# Verification

Candidate observed 2026-09-06T13:31:03.339877+00:00; Python 3.13.2 on Darwin.
- `app.py` SHA256 `9998aba34ae779616b79b0e357786f9d51d560d385037eed054238b83cf5e413`
- `test_app.py` SHA256 `6247828c56344e861de5bcf007f4eac228cdf4adcb91e834cbc04d15887eeaa9`

Command: `python3 -m unittest -v` from candidate root, approved loopback execution outside sandbox. Outcome: **8 tests passed** in 2.110 seconds. Raw output: final-tests.txt. Real disk and loopback HTTP, no dependency mocks.

| Requirement | Evidence | Judgment |
|---|---|---|
| R1 | Store reopened after save; real HTTP server stopped/recreated from same JSON and GET returned saved title | Passed backend persistence; browser reload remains pending |
| R2 | Bob and missing principals denied reads and updates; exact disk bytes unchanged; owner reads preserve saved title | Passed API and Store checks |
| R3 | HTTP success/error response bodies tested; HTML response handling inspected | Browser execution pending parent evaluator, not verified complete |

Baseline: one original happy-path test passed. Added tests against unchanged original app failed 5 subtests during approved HTTP run: Bob and missing-principal unauthorized PUT received 200; Store did not reject; persisted data was changed. Earlier sandbox baseline had 2 assertions fail and 3 bind errors (baseline-tests.txt). After repair, sandbox run passed all 5 Store tests but again blocked 3 HTTP tests; approved run above passed all 8. Infrastructure retries are recorded rather than misclassified as flakes.

Test quality: denial assertions check failure and persisted side effects, persistence crosses reopened application/store state, data is isolated per test. No internal helper mocking or fixed ports. Wrong ownership implementation is demonstrably caught on baseline. Browser stale-response and identity-switch code has only source review locally; parent must exercise real DOM. No CI exists in fixture; no remote head or required CI checked. No independent reviewer or runtime routing controls in this assignment. No full-completion claim.
