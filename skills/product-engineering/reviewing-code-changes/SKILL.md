---
name: reviewing-code-changes
description: "Triage change risk, review code and tests against requirements, and maintain revision-specific review.md histories through defect repair and verification. Use for package reviews, review-fix cycles, or aggregate review before a pull request is ready."
license: MIT
---

# Reviewing code changes

Find substantiated defects and missing acceptance evidence, then verify their resolution. Review scope includes tests and affected dependencies. A fast triage assigns attention; it is not the review itself.

## Establish the review boundary

Read applicable project instructions, intended requirements and technical decisions, baseline and candidate revisions, relevant tests, and surrounding code. Inspect the actual candidate, including relevant staged/unstaged modifications, untracked code/tests, and deletions. Identify it with a complete content snapshot or hashes and note index/worktree divergence; an ordinary unstaged diff is insufficient. Confirm what belongs to this initiative and preserve unrelated work.

Adopt project review conventions. Otherwise maintain `review.md` beside the package plan, or a review-history section for small work. Aggregate reviews use an initiative-level record referencing package histories. Use the [review template](templates/review.md).

## Triage every review

Read [triage and closure](references/triage-and-closure.md). Assess consequence of failure, affected trust/data/interface boundaries, uncertainty, complexity, and coverage needs. Use project priority definitions or P0 critical, P1 high, P2 medium, P3 low. Keep optional enhancements separate from defects.

Use a capable mid-tier model with low effort for bounded initial triage when routing is supported. Escalate ambiguous or high-risk areas. Small diffs can have critical impact. A low triage rating never exempts changed behavior from substantive review.

## Review independently where possible

Use available specialist capabilities or a fresh general reviewer when delegation is supported and authorized. Supply requirements, relevant decisions, baseline/candidate, source/test pointers, scope, expected evidence, result path, and escalation rules. Have the reviewer form an initial assessment before reading the implementer's justification or other reviewers' conclusions.

High/critical-risk review and fixes use a high/top capable tier; choose reasoning effort by the actual difficulty. Routine bounded review starts at mid tier with moderate effort. Complexity, uncertainty, or contradictory evidence can justify escalation regardless of priority. Apply only supported controls and record the actual route if observable.

Without independent agents, perform a separate review pass and label it self-review. Do not describe a new persona in the same context as independent verification. Never invent custom agent names or require a specific provider.

Inspect behavior, contracts, failure/recovery, regression potential, and relevant security, data, compatibility, operational, or UI concerns. Challenge tests for assertion quality, real boundary coverage, fixtures, and whether a plausible incorrect implementation could pass. An author's passing tests do not establish adequate coverage.

## Substantiate and repair

Findings identify trigger, impact, priority, location, requirement or contract, evidence, and examined revision. Mark hypotheses unconfirmed until substantiated. Do not flood the review with speculative edge cases or stylistic preferences presented as defects.

Resolve disagreements through reproduction, source inspection, or targeted checks. Prefer evidence over votes or reviewer confidence. Route uncertain consequential findings to stronger diagnosis. Preserve rejected findings and the reason so later rounds do not rediscover them without new evidence.

Fix all confirmed actionable in-scope defects, including low-priority ones, within the loop. If fixing a finding changes agreed scope or architecture, prepare that decision before dependent work. A real blocker stays open with its exact cause; do not label it an enhancement merely to finish.

Record repairs against stable finding IDs. Verify the exposing behavior and relevant regression evidence before closing a finding. The author's assertion of a fix is insufficient. Append review rounds rather than erasing the prior history.

## Reassess the integrated result

Review the combined diff after packages are integrated, with attention to interactions and omitted acceptance behavior. Every later round begins with updated triage; reuse still-valid observations and review the changed areas plus affected dependencies.

Tie coverage and closure to the candidate examined. Subsequent changes invalidate affected conclusions, including test-only changes that weaken evidence. A resolved finding can reopen with new evidence; a fresh revision cannot inherit blanket approval.

Return a concise finding summary, review artifact path, examined revision, open blockers, and coverage/independence limits. Say no actionable findings only for the actual inspected scope. Review alone does not establish deployment readiness or authorize commits, publication, or merge.
