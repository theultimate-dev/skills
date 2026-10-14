# Architecture: [product]

[One paragraph: what the product is made of, at the level of containers, and where to start reading.]

<!-- Paths in this file are relative to the repository root and written as backticked text or relative links that stay inside this repository.
Only the Contracts table is derived: contract mode and as-built mode rebuild it from the contract files, and reconciling-product-context checks it. The checklist and every other section are written by hand.
Architecture never links to the roadmap: risks live in the roadmap's risk register. Delete this comment. -->

## Status legend

Every section carries one line under its heading: `Since: Vn · Status: planned | built`.

- `Since:` the version in which the element first exists. `Changed in: Vn (…)` records a later change of shape.
- `planned`: described, not yet built. `built`: a bet that builds it is built. `retired in Vn, replaced by …`: no longer part of the product.
- An untagged section is a mistake; read it as unverified.

## Strategy

[Three to six sentences: the few ideas that shape everything else, each linked to the decision record behind it.]

## Quality goals

| NFR | Goal | Served by |
|---|---|---|
| [NFR-01] | [one line] | [concept or view file] |

## Checklist

| arc42 section | File | Status |
|---|---|---|
| Context and scope | `architecture/context.md` | [current through Vn] |
| Building blocks | `architecture/containers.md`, `architecture/components/` | |
| Runtime | `architecture/runtime/` | |
| Deployment | `architecture/deployment.md`, `architecture/build-and-release.md` | |
| Cross-cutting concepts | `architecture/concepts/`, `architecture/domain-model.md`, `architecture/data.md` | |
| Decisions | `decisions/README.md` | |
| Quality requirements | `product/requirements/non-functional.md` | |
| Risks and technical debt | the roadmap's risk register; not linked from here | |
| Glossary | `product/glossary.md` | |
| [Section with nothing yet] | not needed yet | [the version that will need it] |

## Contracts

<!-- Derived from the contract files: one row per contract, its versions with their statuses newest first, and one row per interface named in the baseline but not written yet. -->

| Contract | Versions | Producers | Consumers |
|---|---|---|---|
| `architecture/contracts/[name].md` | [1.1 proposed · 1.0 accepted, or superseded by …] | [container] | [containers] |
| [interface name] | not written yet | [container] | [containers] |

## External dependencies

See `architecture/ecosystem.md`. Oldest verified-on date: [YYYY-MM-DD].
