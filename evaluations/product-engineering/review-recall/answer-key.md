# Review-recall answer key

**Hidden from the reviewing agent.** Never copy this file, this directory or `seeded.patch` into the reviewer's workspace, and never quote them in its prompt.

Locations are for the commit that applies [`seeded.patch`](seeded.patch) to an unchanged [`fixture/`](../fixture/). The spec is `docs/product-engineering/records-overview/spec.md` in that commit. Evidence was observed on 2026-09-25 with Python 3.13.2 on macOS.

## Planted defects

| ID | Owning lens | Location | Defect | Expected severity | Observed evidence |
|---|---|---|---|---|---|
| P1 | security | `app.py:126-128` | Path traversal. The attachment name is URL-decoded and joined to `attachments/1/` with no normalization or containment check, so `..` segments or an absolute path escape the directory. The ownership check on record 1 does not limit which file is read | `blocking` | As `alice`: `GET /records/1/attachments/..%2F..%2Frecords.json` returned 200 with the whole data file, including `bob`'s record 2. `GET /records/1/attachments/%2Fetc%2Fhosts` returned `/etc/hosts` |
| P2 | efficiency | `app.py:47`, in `Store.list_for` (`app.py:40-52`) | `any()` scans the growing `summaries` list for every owned record: O(k²) in the records one principal owns. The duplicate check is also unnecessary, because dict keys are unique | `should-fix`; `blocking` is acceptable with a measured latency | `list_for` took 0.41 s at 5,000 records, 1.69 s at 10,000 and 6.88 s at 20,000; a linear version took 0.011 s at 20,000. Extrapolated to the spec's 50,000 (spec.md:33): about 43 s per request |
| P3 | conventions | `app.py:36` | `datetime.utcnow()` breaks the rule in the fixture's `AGENTS.md` ("Conventions"): a naive timestamp from an API deprecated since Python 3.12 | `should-fix` | The test run prints `DeprecationWarning: datetime.datetime.utcnow() is deprecated` at `app.py:36`. A saved record showed `"updated_at": "2026-09-24T22:52:29.626036"`, with no offset |
| P4 | architecture | `app.py:115-118` | The export handler reads the data file directly. It bypasses `Store` and its lock, and re-implements the ownership filter that `Store` owns. This breaks the agreed Approach (spec.md:42: "`Store` stays the only code that reads or writes the data file") and the pattern every other handler follows | `should-fix`; `blocking` is acceptable as an unexplained deviation from the Approach | `grep -n "store.path" app.py` shows the handler reading `store.path` at line 116; every other handler calls a `Store` method |
| P5 | intent | AC6 (spec.md:23); page HTML `app.py:54-80` | AC6 is not implemented: the page has no "Export my records" link. The plan claims AC1 to AC6 pass in this PR (spec.md:70), and the PR description's verification report has no AC6 row | `blocking` | `curl -s <app-url>/ \| grep -ci export` printed `0` |

## Secondary checks

- **Verdict.** `REQUEST CHANGES`. An `APPROVE` fails the trial outright.
- **Category check.** The PR description says `agent`, and so does the plan's prediction (spec.md:63). The diff adds ownership checks on three new read paths (`Store.list_for`, the export filter, the attachment handler's `store.read`), which is authorization, so the PR is `human`. The review should say so and hand the PR to `shipping-pull-requests` to relabel it.
- **Verification report.** The report claims a six-AC contract with only five rows. The intent lens should connect this to P5, not treat the report as proof.

## Not planted

- **N1, pre-existing.** `Store.update` (`app.py:27-38`) never checks the owner (`app.py:33`), so `bob` can overwrite `alice`'s title. This is the fixture's seeded defect for the runnable trial, inside a function this diff touches. A report of it is a true finding outside the planted set. Record it separately; it counts as neither recall nor a false positive. Either a blocking finding or a follow-up is acceptable, because the changed line (`app.py:36`) does not change the missing check.
- **Judged not defects under the spec.** `/records` and `/records/export` return empty results for an unknown or missing principal (consistent with AC1). The export includes each record's `owner` field, as `GET /records/1` does. Attachments are served as `application/octet-stream`. Only record 1 has routes, as in the rest of the fixture. A confirmed `blocking` or `should-fix` finding on one of these is a false positive unless it brings evidence that the spec requires otherwise.

## Scoring

1. **Found.** A planted defect counts as found when a finding points at its location (the same function, or within three lines) and states its root cause. A symptom reported elsewhere does not count. Record `confirmed` and `unconfirmed` findings separately; recall is computed on confirmed findings.
2. **Lens.** Record which lens raised the finding, from the lens output when it is visible, and which lens owns it after synthesis. When another lens raises the same root cause, synthesis should assign it to the owning lens.
3. **Severity.** Rating a planted defect below the expected severity is a severity miss. A `nit` on any planted defect is always a miss, because a confirmed defect in changed code is never a nit.
4. **False positive.** A finding reported as a confirmed `blocking` or `should-fix` that is not P1 to P5 or N1, and that the grader refutes by reading the code or running a check. Count unconfirmed questions and nits as noise, separately.
5. **How the lenses ran.** Record each lens as a parallel agent, a headless CLI run, or self-review, as the review labels it. Unlabeled sequential passes in one context are a failure of the skill, whatever the recall.

Per trial, record:

| Trial | P1 security | P2 efficiency | P3 conventions | P4 architecture | P5 intent | N1 | False positives | Noise | Verdict | Category flagged | Lens runs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | found / unconfirmed / missed, severity | | | | | reported / not | count | count | | yes / no | parallel / headless / self-review |
