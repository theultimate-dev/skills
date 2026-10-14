# 0013: Package product context as a `product-context` category

- Status: accepted
- Date: 2026-10-14

## Context

A product that lives through several versions outgrows one specification. Its requirements, architecture, decisions and roadmap have to stay coherent for months, and the agents that build it in a code repository need that context in a form they can find and trust. `product-design` ends at one initiative's handoff. `product-engineering` takes one work item from spec to merged pull requests, with its artifacts in the code repository. Neither keeps a product's whole context across versions, and neither cuts that context into units of work sized for an agent. Established methods (arc42, C4, decision records, Shape Up, story mapping) and current agentic tools (Kiro's steering files and specs, Spec Kit, OpenSpec's specs and changes, BMAD) converge on the same shape: stable context kept apart from change-scoped work, with each change folding back into the living documents.

## Options

1. **Add the skills to `product-design`.** Its promise, rough ideas to a product/design handoff for one initiative, would have to stretch to architecture, roadmaps and work units across versions.
2. **Add them to `product-engineering`.** Its loop and artifacts live in the code repository, one work item at a time. A product's whole context does not, and nine skills already make the plugin large.
3. **A `product-context` category.** Names what the skills keep, a product context repository, and sits beside `product-design` and `product-engineering`. Costs a sixth plugin.

## Decision

Option 3. `product-context` is a category and plugin with six skills: `structuring-product-context`, `curating-product-requirements`, `designing-system-architecture`, `planning-product-roadmaps`, `shaping-bets` and `reconciling-product-context`.

- The product context repository is Markdown, kept apart from the code, in layers sorted by how often they change: `product/`, `architecture/`, `decisions/` and `roadmap/`, plus `design/` and `research/`. Every fact has one home. Indexes are derived. Volatile files link to stable ones, never the reverse. HTML is allowed only for prototypes under `design/`.
- The unit of work is a **bet**, in the Shape Up sense: shaped, bounded by an appetite, handed over whole, and stopped by a circuit breaker rather than extended. Appetite uses `product-engineering`'s effort scale: M is one plan, L is two or three.
- Code repositories read the context repository read-only, pinned to a commit at handoff. The context repository keeps product and architecture decisions; implementation decisions stay in the code repository's own log.
- The skills delegate rather than duplicate: decision records to `decision-records`, rough ideas and single initiatives to `product-design`, building a bet to `product-engineering` (0014). When a sibling is missing, a skill names it and produces the essential outcome itself.
- The skills are project-agnostic and harness-neutral under 0002.

## Consequences

- A sixth plugin. Its first release, `product-context--v0.1.0`, is a minor marketplace release under 0011.
- A bet is an interface between two plugins. The template in `shaping-bets` is authoritative and `product-engineering` reads bets by their fields; changing those fields is breaking for both plugins.
- The structure costs files and a reconciliation pass after every bet. It pays off for products with several versions or many work items; a one-off feature still goes straight to `product-engineering`.
- The skills have not run on a real product yet. The first adoption of an existing multi-version product, and evaluation scenarios, are the follow-up.
