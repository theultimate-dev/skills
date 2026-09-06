# Event handling

## Facts in, durable facts out

Useful events include accepted user decisions, completed bounded tasks, check commands and results, review findings, repair outcomes, integration, blockers, authorization, and session handoff. The orchestrator supplies them after meaningful transitions, not after every token or trivial tool call.

Use IDs stable across retries, such as a session identifier plus sequence. The writer checks the destination before appending. A supplied ID already present with the same payload needs no duplicate event, but its requested checkpoint change still needs verification. The same ID with a different payload is a conflict; report it without altering the original.

Do not infer missing approval from an implementation starting or an agent returning successfully. A reported test result remains a report until the caller supplies inspected evidence. The recorder can verify the file write; it is not tasked with adjudicating every engineering claim.

## Single-writer discipline

The orchestrator owns the queue and delegates one batch at a time. Do not let code workers update the same log concurrently. They return events to the orchestrator. Before a phase gate, context compaction, or session handoff, flush pending events and verify their IDs persisted.

If a call fails or its acknowledgment is lost, inspect both events and checkpoint before retrying the same IDs. An interruption can persist the event but not its checkpoint. Repair that checkpoint only when its current state matches the caller's expected predecessor. If a later checkpoint explicitly supersedes the requested state, preserve it and acknowledge the already-persisted batch. If ordering is unclear or state conflicts, return a short conflict rather than overwriting it. If the recorder is unavailable, the orchestrator takes ownership and completes pending writes directly. Do not run the fallback writer concurrently with an uncertain active recorder; resolve its status first.

## Checkpoints and corrections

Keep the current checkpoint short enough to read at session start. It points to specs, plans, latest evidence, active packages, open findings, and next action. Preserve existing authorization in the user's terms; do not broaden it when summarizing.

Chronology remains append-only. If event S2-E4 stated a check passed but later evidence shows it was run on an older revision, append a correction referencing S2-E4 and update the current checkpoint accordingly. Do not silently rewrite the old claim.

For long logs, use the project's archival convention and retain a discoverable index. Archive only completed chronological segments; do not delete unresolved findings or the evidence needed to resume. A raw conversation dump is not a worklog.
