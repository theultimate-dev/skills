# Contracts

A contract is an interface that two or more bets build from different sides, or that more than one container depends on. It lives under `architecture/contracts/` so that bets can consume it as settled, build in parallel, and be checked against it in review. The examples use Larder's `architecture/contracts/sync-protocol.md`.

## Contents

- When an interface needs a contract
- Anatomy
- Status and acceptance
- Versioning and compatibility
- How bets use contracts
- Details settled during delivery
- Example outline

## When an interface needs a contract

| Interface | Contract? |
|---|---|
| A protocol between two containers that different bets build | Yes |
| A public API, an event stream or a file format other systems read | Yes |
| A configuration format users edit by hand | Yes |
| A schema owned by one container and read by another | Yes |
| An interface inside one container that one bet builds | No; the code repository settles it |
| A library's API the product calls | No; it goes in `ecosystem.md` |

When in doubt, ask which bets touch it. One bet: implementation detail. Two or more, or another system: contract.

## Anatomy

Write each contract from the contract template. It holds:

| Part | Content |
|---|---|
| Header | `Version:` with each live version and its status, newest first, and `Since:`; producers and consumers (containers, never bets); the decisions it relies on; `Superseded by:` when replaced |
| Purpose | One paragraph: what flows, between whom, and why it is a contract |
| Transport and framing | How messages travel, how they are delimited, how a connection or session starts and ends |
| Operations or messages | One table row per operation or message: name, direction, fields, result, errors |
| Invariants | Rules that hold across all operations: ordering, idempotency, request IDs, authentication, size limits |
| Errors | The error codes or shapes, what each means, what the caller does |
| Versioning and compatibility | How a version is announced, what a receiver does with unknown fields, which changes are compatible |
| Examples | One or two payloads per important message, in a neutral notation such as JSON |
| Open details | What the contract leaves to the implementation loop, explicitly |
| History | One line per version: date, what changed, the user's words when accepted |

Never write a contract as code in a programming language. Types belong to the code repository; the contract states the shape any implementation must honour.

## Status and acceptance

Each version carries its own status on the header's Version line, newest first, for example `Version: 1.1 proposed · 1.0 accepted`.

- `proposed`: written, not yet agreed. No bet may consume this version, so a bet that names it is not ready.
- `accepted`: agreed by the user in explicit words, recorded in a History line with the date. Bets may consume this version.
- `superseded`: the whole contract was replaced by another file because its purpose or parties changed; a `Superseded by:` line under the header links the replacement, and the file takes no more versions.

A bet's readiness reads the status of the version the bet names, not the newest one.

Present a proposed contract with its producers, consumers, the decisions it implies, and what it leaves open. Silence, "looks fine for now" or an edit request is not acceptance. When the contract embodies a consequential choice, such as a transport or an authentication scheme, record that choice with `decision-records` and link it from the header.

## Versioning and compatibility

A compatible change, such as an optional field or a new message a receiver may ignore, raises the minor part of the version. An incompatible change, such as a removed or renamed field, a changed meaning or a new required field, raises the major part and lists every consumer that must change. Versions are always major.minor: `1.0`, `1.1`, `2.0`.

- An incompatible change stays in the same file while the interface keeps its purpose and parties. A contract whose purpose or parties change is a new file, and the old one is `superseded`.
- Keep every version's operations in the same file, newest first, until no consumer uses the old one.
- A bet `in delivery` keeps the version it was pinned to. A change it needs arrives from the implementation loop as a context change; `shaping-bets` reshapes the bet, and this skill writes the new version.
- State the receiver's rule for unknown fields, unknown messages and newer versions. "Ignore unknown fields; reject a newer major version with a named error" is a common default.

## How bets use contracts

A bet's Architecture section names what it consumes and what it produces or changes:

```
- Consumes: architecture/contracts/sync-protocol.md, version 1.0, accepted
- Produces or changes: architecture/contracts/sync-protocol.md: adds the shared-list messages (version 1.1); field names are left to the implementation loop
```

`shaping-bets` checks that the version each bet consumes is `accepted` before the bet is ready. The implementation loop in the code repository reads the contract at the bet's pinned commit, honours it exactly, and treats any needed change as a context change. Its architecture review checks the diff against it.

## Details settled during delivery

A contract may leave details open on purpose, such as field names or error codes for a new message, when the bet producing them is the only one building them yet. The implementation loop settles them at its G2 and reports them in its hand-back. In as-built mode, write them into the contract:

1. Read the implementation loop's hand-back, its settled contract details, when it is given. When the code repository runs the product-engineering loop, also read the work item's `spec.md` Approach section and the code repository's decision records that name the bet.
2. Write the settled details into the contract's operations, errors and examples.
3. Raise the version when the shape changed; leave it when the details only filled what was declared open.
4. Remove the details from "Open details" and add a History line naming the record that settled them, as `<repository>: decisions/NNNN-title.md`. A bet number may appear in plain text for provenance; never link to the roadmap.
5. Rebuild the Contracts table in `architecture/README.md`.

## Example outline

```
# Contract: sync protocol

Version: 1.1 proposed · 1.0 accepted · Since: V1
Producers: sync service · Consumers: web app
Decisions: decisions/0004-sync-over-https-with-change-log.md

## Purpose
## Transport and framing
## Operations
| Operation | Direction | Request | Response | Errors |
| pull | client → service | household ID, last change ID | changes since, new cursor | stale-cursor, unauthorized |
| push | client → service | request ID, changes | accepted change IDs, conflicts | conflict, too-large |
## Invariants
- Every push carries a request ID; a repeated request ID returns the first result and applies nothing twice.
## Errors
## Versioning and compatibility
## Examples
## Open details
## History
- 1.1, 2026-04-10: proposed: adds the shared-list messages.
- 1.0, 2026-03-02: accepted ("agreed, go with change-log sync").
```
