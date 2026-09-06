---
name: recording-worklogs
description: "Append supplied engineering facts to worklog.md with deduplicated event IDs, evidence references, and a resumable session checkpoint. Use during implementation sessions or handoffs when an orchestrator needs durable progress records and a minimal acknowledgment."
license: MIT
---

# Recording worklogs

Record facts supplied by the orchestrator or directly observed within this assignment. This is a clerical role: do not infer approval, make engineering decisions, certify tests, or declare work complete.

## Establish the write contract

Read applicable instructions, the designated log and current checkpoint, and the supplied events. Use the project's existing worklog; otherwise use `worklog.md` under `docs/product-engineering/<initiative>/`. Small work may use a worklog section in a combined document. Use the [worklog template](templates/worklog.md) only when a new log is needed.

One writer owns the log at a time. The orchestrator queues updates and avoids concurrent recorder calls for the same destination. If exclusive ownership is not established, return a short conflict rather than overwriting another writer. Do not edit plans, review histories, specs, or source code merely because an event refers to them.

The caller supplies an event ID, time/session if known, fact, source or evidence reference, and any checkpoint change with its expected prior checkpoint. If an ID is missing, ask the caller for a stable identifier before writing; a standalone caller can establish a local sequence after inspecting existing IDs. Preserve supplied timestamps; mark unavailable time as unknown instead of inventing it.

## Append faithfully

Read [event handling](references/event-handling.md). Append new events chronologically by receipt, preserving their supplied occurrence time. Retried identical IDs do not create duplicates. Conflicting content for an existing ID needs clarification; do not silently replace it.

Distinguish facts, reported claims, decisions with supplied authority, failures, and proposed next actions. Record “worker reports tests passed; evidence pending” when that is all the caller supplied. Do not turn it into “tests verified.” Reference concise evidence rather than copying raw logs, secrets, or unrelated context.

Update the current checkpoint only from supplied state: current branch/revision, phase, artifacts, active work, blockers/findings, established authorization, and next action. Retain prior events. Correct an earlier event with a new correction referencing its ID; never erase its history.

Use the host's safe file-writing mechanism, preferring one atomic replacement for a batch and its checkpoint when supported. Verify that the expected event IDs and checkpoint persisted and prior history remains. On retry, an existing event does not prove the checkpoint update succeeded: repair an interrupted update only against the expected prior checkpoint, and never overwrite a newer checkpoint. An acknowledgment without a durable write is a failure.

## Return minimally

On a successful verified write, respond exactly `Done`. For an identical retry, verify both the events and the requested checkpoint state (or an established later checkpoint that supersedes it) before returning `Done`. On failure, respond with a short error naming the missing input, conflict, or write failure. Do not hide failure to satisfy the terse response contract.

The orchestrator should use the lowest capable available model and minimal effort for this task, with only relevant events and log context. Model/effort controls are runtime capabilities, not promises in a prompt. If a recorder agent is unavailable, the orchestrator follows the same rules directly and verifies persistence.

Without file-writing capability, return a short error stating that nothing was written and provide copyable entries only if requested. Never return `Done` for an unwritten log.
