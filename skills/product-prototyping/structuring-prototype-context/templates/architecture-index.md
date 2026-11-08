# Architecture: [product]

[One paragraph: what the product is made of, at the level of containers, and where to start reading.]

<!-- Paths in this file are relative to the context folder and written as backticked text or relative links that stay inside it.
This file mixes derived and authored content, the one exception to "indexes are rebuilt, never hand-edited". Only the Contracts table and the oldest verified-on date are derived: they are rebuilt from the contract files and the ecosystem file. The status legend, strategy, quality goals and checklist are authored by hand; a rebuild keeps them. Include only the views that help; a prototype rarely needs them all.
Architecture never links to bets. Delete this comment. -->

## Status legend

Every section carries one line under its heading: `Status: built | planned`.

- `planned`: written at shaping for an element the open bet introduces and other files must reference. Closing the bet as kept turns it into `built`; closing it as removed deletes it.
- `built`: the code has it. There are no version tags.
- A section without a status line is a mistake; read it as unverified.

## Strategy

[Three to six sentences: the few ideas that shape everything else, each linked to the decision record behind it.]

## Quality goals

| NFR | Goal | Served by |
|---|---|---|
| [NFR-01] | [one line] | [concept or view file] |

## Checklist

| Section | File | Status |
|---|---|---|
| Context and scope | `architecture/context.md` | |
| Building blocks, when there is more than one container | `architecture/containers.md` | |
| Runtime | `architecture/runtime/` | |
| Cross-cutting concepts | `architecture/concepts/` | |
| Decisions | `decisions/README.md` | |
| Quality requirements | `product/requirements/non-functional.md` | |
| [Section with nothing yet] | not needed yet | |

## Contracts

<!-- Derived from the contract files: one row per contract, its versions with their statuses newest first. -->

| Contract | Versions | Producers | Consumers |
|---|---|---|---|
| `architecture/contracts/[name].md` | [1.1 proposed · 1.0 accepted, or superseded by …] | [container] | [containers] |

## External dependencies

See `architecture/ecosystem.md`. Oldest verified-on date: [YYYY-MM-DD].
