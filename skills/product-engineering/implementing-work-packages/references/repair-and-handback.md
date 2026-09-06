# Repair and handback

## Diagnose before retrying

Capture the failing command or user action, expected and actual behavior, relevant output, environment, and revision. Distinguish product defects, fixture mistakes, unavailable services, known baseline failures, and flaky behavior using evidence. A previously failing test is not automatically irrelevant if this change depends on that behavior.

Form a bounded hypothesis, inspect the relevant path, make a justified repair, then rerun the check that exposed the failure and the affected regression checks. Increasing timeouts or rerunning until green does not resolve a race without evidence that the root cause was addressed.

When a repair fails, preserve what was learned and change the next investigation accordingly. After two equivalent unsuccessful attempts without new evidence, use stronger diagnosis, inspect missing context, or revise the plan. Do not burn through an unspecified series of near-identical agent calls.

## Review fixes

Read the finding's trigger, impact, evidence, examined revision, and intended requirement. Confirm the issue; if disputed, provide counterevidence or ask the reviewer to reproduce it. Prioritize by consequence, but repair every confirmed actionable in-scope defect before completion.

Add regression protection that would catch the reported failure where meaningful. Explain a changed test expectation using an agreed requirement change or demonstrated test error; never cite the implementation itself as the only reason the expected result changed.

Return finding ID, changed areas, candidate revision, reproduction/check results, and remaining uncertainty. The reviewer or verifier establishes closure. Repaired code can affect other findings and acceptance results, so identify invalidated evidence.

## Integration handback

List interface/configuration/migration changes, shared files touched with agreement, dependencies on other packages, and commands needed to run the result. Include required generated outputs according to project policy. Do not hide a manual prerequisite in a passing local result.

A passing isolated workspace is evidence for that workspace. After integration, run checks for combined contracts, shared state, and user behavior; inspect the aggregate diff. A conflict resolved syntactically still needs semantic verification.

Keep raw traces or large logs in the project's evidence location. Return concise durable references with retention limitations, not pages of tool output. Distinguish implemented, tested, independently reviewed, integrated, and published states.
