# Contract: [name]

Version: [1.0] proposed
Producers: [container] · Consumers: [containers]
Decisions: [`decisions/NNNN-title.md` | none]

<!-- A contract states the shape every implementation must honour; it is never code in a programming language. Write one only when two or more parts depend on the same interface.
Version lists each live version, newest first, with its status: proposed until the person agrees in explicit words, then accepted with a History line, for example `Version: 1.1 proposed · 1.0 accepted`. Versions are the contract's own major.minor; they are not product versions.
A bet relies only on an accepted version; its readiness reads the status of the version it names. A contract the open bet introduces may be written at shaping as proposed and marked planned in the architecture index; a removed bet deletes it.
Producers and consumers are containers, never bets: bets point at contracts, never the reverse.
When the contract's purpose or parties change, a new file replaces it: add `Superseded by: [path]` under the header and add no more versions. Delete this comment. -->

## Purpose

[One paragraph: what flows, between whom, and why more than one part depends on it.]

## Transport and framing

[How messages travel, how they are delimited, how a session or connection starts and ends, how the caller authenticates.]

## Operations

| Operation or message | Direction | Request or payload | Result | Errors |
|---|---|---|---|---|
| [name] | [producer → consumer] | [fields, required or optional] | [fields] | [error names] |

## Invariants

- [A rule that holds across every operation: ordering, idempotency, request IDs, size limits, timeouts.]

## Errors

| Error | Meaning | What the caller does |
|---|---|---|
| [name] | [when it occurs] | [retry, re-sync, show the user, give up] |

## Versioning and compatibility

- How a version is announced: [header, handshake field, path].
- Unknown fields: [ignored]. Unknown messages: [ignored or rejected with a named error]. A newer major version: [rejected with a named error].
- Compatible changes raise the minor version; incompatible ones raise the major version and list every consumer that must change.

## Examples

```json
{ "operation": "[name]", "requestId": "[…]" }
```

## Open details

<!-- What this contract leaves to the build on purpose. Building reports them; closing writes the settled ones back here. -->

- [Detail]: open. When settled: settled by `decisions/NNNN-title.md`.

## History

- [1.0], [YYYY-MM-DD]: [proposed | accepted ("person's words") | what changed, settled by `decisions/NNNN-title.md`; a bet number may appear in plain text].
