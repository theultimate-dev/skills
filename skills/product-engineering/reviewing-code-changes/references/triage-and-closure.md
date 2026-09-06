# Triage and closure

## Risk and difficulty are different

Triage reads enough code and context to identify affected boundaries. File count and line count measure size, not consequence. A one-line missing ownership predicate can expose other users' data; a large mechanical rename may be lower risk.

| Default priority | Meaning | Example |
|---|---|---|
| P0 critical | Catastrophic or broadly exploitable failure needing immediate attention | Broad unauthorized access or irreversible widespread data loss |
| P1 high | Serious correctness, security, or core-journey failure | A caller can mutate another owner's record |
| P2 medium | Material bounded defect in required behavior | A supported filter combination returns incorrect results |
| P3 low | Smaller confirmed defect within scope | Incorrect recovery text that misdirects the user |

Follow the project's definitions if different. Likelihood, exposure, and blast radius affect priority; complexity affects investigation effort. Do not downgrade severe potential impact because a reproduction requires work. Label uncertainty and investigate it.

Assign review coverage to the relevant capability, not an imagined fixed agent roster. Fast triage must still lead to substantive review of every changed behavioral area. For a large change, divide coverage explicitly and perform aggregate synthesis to identify gaps.

## A useful finding

Include a stable ID, priority, confirmed/unconfirmed status, trigger/preconditions, expected versus actual behavior, practical impact, exact source location and examined revision, and supporting reproduction or code evidence. Reference the violated requirement or established contract where available. Suggest a direction without forcing an unnecessary refactor.

Static evidence can substantiate a defect even if the environment cannot execute it. State that limitation. Conversely, an unsupported suspicion is not a confirmed defect. Distinguish a missing mandatory check from evidence that the software itself is wrong; both can prevent completion for different reasons.

## Dispositions preserve history

Use statuses such as unconfirmed, confirmed, fixing, fixed-awaiting-verification, closed, rejected-with-evidence, or blocked. Track each transition with the revision and rationale. Duplicate findings reference a canonical ID. Do not delete inconvenient findings or rewrite their original evidence.

Close a confirmed defect only after inspecting the repair and appropriate verification. When a separate verifier is unavailable, disclose who performed the recheck. Reopen on new evidence or affected edits. Reject a false positive with concrete counterevidence, not a vote among agents.

An optional improvement may be deferred with a reason. A confirmed actionable in-scope defect is repaired at every priority. A scope-changing repair needs an explicit revised decision; a blocked defect remains a blocker. Do not silently lower the quality gate because a loop is taking longer than expected.

## Example review progression

Round 1 finds that an update looks up a record by ID without checking its owner. Record the candidate revision, second-principal request, resulting mutation, and P1 impact. The repair adds the ownership predicate and a denied-update test.

Round 2 begins with a quick reassessment of that change. Inspect the predicate and verify both the denied update and absence of state mutation, then check the valid owner's update. A test asserting only an error status would miss a handler that mutates first and rejects afterward.

At aggregate review, confirm another package did not bypass the same boundary through a new endpoint. Passing the original repair test alone does not establish that all integrated paths preserve ownership.
