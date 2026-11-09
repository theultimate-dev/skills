# Architecture: Sprig

One Python file reads and writes one JSON file on the person's machine. Start with [the context view](context.md).

## Status legend

Every section carries one line under its heading: `Status: built | planned`.

- `planned`: written at shaping for an element the open bet introduces and other files must reference.
- `built`: the code has it.

## Strategy

Sprig is one file and one data file, because a prototype for one person needs nothing else; see [decision 0003](../decisions/0003-sprig-stays-offline.md).

## Quality goals

None stated yet.

## Checklist

| Section | File | Status |
|---|---|---|
| Context and scope | `architecture/context.md` | built |
| Cross-cutting concepts | `architecture/concepts/` | |
| Decisions | `decisions/README.md` | built |

## Contracts

| Contract | Versions | Producers | Consumers |
|---|---|---|---|

## External dependencies

See `architecture/ecosystem.md`. Oldest verified-on date: 2026-10-01.
