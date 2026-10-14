---
name: designing-system-architecture
description: "Designs and evolves the architecture in a product context repository: C4 context and container views, components where they pay, runtime scenarios, data, deployment, cross-cutting concepts, and the versioned contracts several bets share, each section tagged with the version it arrives in and whether it is planned or built. Writes the baseline before a version's milestones are shaped and each contract before a bet consumes it, raises consequential choices as decision records, and leaves code-level approaches to the implementation loop. Use when the user says design the product's architecture, draw the C4 or arc42 views, what must exist before we build, write a contract in architecture/contracts, plan the architecture for V2, refresh the architecture for the next version, or update the architecture as built. Not for choosing how to build one work item (brainstorming-solutions)."
license: MIT
---

# Designing system architecture

Produce and evolve `architecture/` in a product context repository: one living description of how the product is structured, with every section tagged by the version it arrives in and whether it is planned or built. Bets consume this architecture; they never define it. When a bet needs a new interface, this skill writes the contract first, and the bet depends on it.

This skill works at the level of containers, boundaries, contracts and cross-cutting rules. How to build one work item inside that structure belongs to the implementation loop in the code repository (`brainstorming-solutions` at its G2). Product scope and behaviour belong to `curating-product-requirements`.

## Modes

| Mode | When | Produces | User agreement |
|---|---|---|---|
| **Baseline** (pass 1) | Before a version's milestones are shaped, from the version's requirements | C4 levels 1–2, level 3 where it pays, domain model, data, cross-cutting concepts, deployment, build and release, the main runtime scenarios, the decisions that must precede code, `ecosystem.md`, and the names of the interfaces between containers | The baseline summary, each decision record accepted |
| **Contract** (pass 2) | When a milestone's bets are shaped and share an interface, or an accepted contract must change | One file under `architecture/contracts/`, or a new version in it; the Contracts table in `architecture/README.md` rebuilt | The version moved to `accepted` |
| **Refresh** | At a version boundary, when `planning-product-roadmaps` opens the next version | Retagged sections, the next version's elements sketched as `planned`, retired elements marked, re-verified dependencies, the interfaces the next version's first milestone needs, named | The refreshed summary |
| **As-built** | When a bet closes, called by `reconciling-product-context`, or on request | Sections flipped from `planned` to `built`, contract details settled during delivery, divergences resolved or recorded, the Contracts table rebuilt | Only for a divergence the user must accept |

## Start from the repository

1. Read `AGENTS.md`, `product/overview.md`, `product/glossary.md`, the requirement files and `non-functional.md` for the versions in scope, `architecture/README.md`, `decisions/README.md`, `roadmap/README.md` and the current version brief. Read the research notes they cite.
2. When a code repository already exists, read it for what is built: its structure, its interfaces, its decision log. Describe what you find; never copy code into the context repository.
3. Write down every open structural choice as one line, and classify each with the test below before designing anything.

Never ask the user what the repositories answer. Ask about trade-offs: where a boundary sits, what a contract must guarantee, what the product may depend on.

## The architecture-versus-implementation test

A choice is **architecture**, and belongs to this skill and the context repository's `decisions/`, when it changes:

- an element, boundary or technology that `architecture/` describes, such as a container, a store, a trust boundary, a runtime or a deployment target;
- a contract under `architecture/contracts/`;
- a decision already recorded in the context repository's `decisions/`.

Anything inside one element that no other bet consumes is an **implementation** choice. It is settled by the implementation loop and recorded in the code repository's own decision log. Read [decisions](references/decisions.md) for examples on both sides and for which decisions must precede code.

## Baseline

The baseline is pass 1. It runs from the version's requirements, before any milestone is shaped into bets, so it never waits for bets and never depends on them.

1. **Map the checklist.** Use arc42 as a checklist mapped to files, never as a form to fill in. Each of its twelve sections either has a home or is marked "not needed yet". See [views and checklist](references/views-and-checklist.md).
2. **Context and containers, complete.** `context.md` (C4 level 1) names every person and external system the product touches. `containers.md` (C4 level 2) names every deployable or separately running unit and every store, with the protocol on each arrow.
3. **Components where they pay.** Add `components/<container>.md` (C4 level 3) only for containers the first version builds and whose inside several bets will touch.
4. **Domain model and data.** `domain-model.md` holds the entities and their relationships; terms go to `product/glossary.md` through `curating-product-requirements`. `data.md` lists every store: what it holds, where it lives, how long it is kept.
5. **Cross-cutting concepts.** One file per rule that spans containers under `concepts/`: security and trust boundaries, error handling and recovery, consistency, identity, observability. Only the rules this product actually needs.
6. **Deployment, build and release.** `deployment.md` shows where each container runs per placement; `build-and-release.md` shows how a commit becomes a running product.
7. **Runtime scenarios.** Under `runtime/`, grouped by topic, not by diagram type: the main flow, the hardest path, and the flows the first milestone's requirements describe.
8. **Interfaces, named.** Name every interface between containers that the version's requirements imply, with its producers and consumers, and list it in the Contracts table as not written yet. Its contract is written in pass 2, in contract mode, when the first milestone whose bets share it is shaped.
9. **Decisions that precede code.** Record each with `decision-records` when it is installed. These are the choices that would be expensive to undo once code exists: data ownership, trust boundaries, the protocols between containers, the runtime or language per container, the distribution channel, the code repository layout.
10. **Ecosystem.** List every external dependency in `ecosystem.md` with its version, maturity, how it plugs in, and a verified-on date.

Tag every section with `Since: Vn · Status: planned`, or `built` only when an existing code repository shows the element built. Write `architecture/README.md` from the [architecture index template](templates/architecture-index.md).

**Stop at enough.** The baseline is done when every container and store the first version's requirements need is at C4 level 2 with the protocol on every arrow, the cross-cutting rules and the main runtime scenarios are written, every decision that must precede code is accepted, and every interface between containers is named. Contracts come in pass 2; each must be `accepted` before a bet that consumes it can be ready. Read [baseline and refresh](references/baseline-and-refresh.md) for the depth rules.

Present the baseline in one message: the containers and their arrows, the interfaces named for pass 2, the decisions to accept, what was left as "not needed yet", and the open questions. The user's explicit agreement accepts it; record their words in each accepted decision.

## Contract

1. Name the producers and consumers: containers, never bets. Bets point at contracts through their Architecture section; a contract never points back.
2. Write the operations or messages, the invariants, the error semantics, and the versioning and compatibility rules, from the [contract template](templates/contract.md). Use tables and example payloads; never code in a programming language.
3. Give each version its status on the header's Version line, newest first: `Version: 1.1 proposed · 1.0 accepted`. A version is `proposed` until the user agrees in explicit words; then `accepted`, with a History line holding the date and their words. A bet's readiness reads the status of the version the bet names.
4. A compatible change raises the minor version. An incompatible change raises the major version, in the same file while the interface keeps its purpose and parties. Report every consumer, and every bet `in delivery` that consumes an older version: those bets keep the version they were pinned to, and a change they need arrives as a context change from the implementation loop, which `shaping-bets` turns into a reshaped bet.
5. A contract whose purpose or parties change is a new file. The old one gets `Superseded by:` with a link to the new file, and takes no more versions.
6. Rebuild the Contracts table in `architecture/README.md` from the contract files.

## Refresh

At a version boundary: re-read the next version's brief; retag what moved; sketch the next version's new elements as `planned`, at C4 level 2 and no deeper; mark retired elements and say what replaced them; re-verify `ecosystem.md`; and name the interfaces the next version's first milestone needs. Write those contracts in contract mode when their bets are shaped, not before.

Never flip `planned` to `built` here. A section of the shipped version that is still `planned` either did not ship, and is retargeted, or was built without a bet's evidence reaching it, and goes to the audit in `reconciling-product-context`.

## As-built

Run when a bet closes. `reconciling-product-context` calls this mode with the bet and the code repository's evidence; run it directly when that skill is missing.

1. For each element the bet delivered, flip `Status: planned` to `built`.
2. For each contract the bet produced or changed, write the details the implementation loop settled: from its hand-back's settled contract details when given, and, when the code repository runs the product-engineering loop, from the work item's `spec.md` Approach and the code repository's decision records that name the bet. A change in shape is a new contract version. Rebuild the Contracts table.
3. For each divergence between what was built and what `architecture/` says: when the user accepts the built version, update the architecture and record a decision when the change is consequential; otherwise record an open question in `roadmap/open-questions.md`, owned by the user.
4. Link each code repository decision record that moved the architecture from the section it changed, as `<repository>: decisions/NNNN-title.md`.
5. Pass anything meant for the bet's outcome log to `reconciling-product-context`. Never write into the bet.

## Diagrams

Draw C4 views as Mermaid flowcharts. Mermaid's C4 syntax is still experimental and renders unevenly, so prefer `flowchart` with styled nodes. One diagram per view, labels of a few words, the protocol on every arrow, and a sentence under the diagram for what it cannot show. Sequence and state diagrams belong in `runtime/`. Examples are in [views and checklist](references/views-and-checklist.md).

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| Designing down to files, classes or functions | Stop at containers, components and contracts; the code repository decides the rest |
| Full depth for a version nobody has planned | Sketch it as `planned` at level 2; add contracts when its bets are shaped |
| A section without `Since:` and `Status:` | Tag it; an untagged section reads as unverified |
| A contract written as code in one language | Operations and messages in tables, with example payloads |
| A contract or a view that names the bets building it | Name containers; bets point at the architecture, never the reverse |
| Copying requirement text into architecture | Name the requirement IDs a section serves |
| Re-arguing an accepted decision | Cite it; reopen only with new evidence, as its own question, and supersede |
| An implementation choice recorded here | Leave it to the code repository's log; record it here only when it moved the architecture |

## When a sibling skill is missing

Say in one line which skill is missing, then produce its essential outcome yourself.

| Skill | Essential outcome |
|---|---|
| `decision-records` | A record in `decisions/NNNN-kebab-title.md` with `- Status:` and `- Date:` lines and the sections Context, Options, Decision, Consequences, plus its row in `decisions/README.md` |
| `curating-product-requirements` | A missing requirement or term becomes an open question in `roadmap/open-questions.md`; never edit `product/` from here |
| `reconciling-product-context` | Run as-built mode directly from the merged pull requests, the loop's hand-back when given, and, when the code repository runs the product-engineering loop, its `spec.md` and decision records |

## Report

Return the files written or changed, each contract with its versions and their statuses, the interfaces named but not written yet, each decision recorded with its status, the sections left `planned`, the open questions with what they block, and the next step: `planning-product-roadmaps` when the roadmap is not planned yet, otherwise `shaping-bets`. A request to design is not a request to build: change no code repository. Without file access, return the files as Markdown and say that nothing was written.

## References

| Read | When |
|---|---|
| [views and checklist](references/views-and-checklist.md) | Mapping arc42 to files, choosing C4 depth, drawing views and runtime scenarios, the data view, the tag format |
| [contracts](references/contracts.md) | Writing, accepting, versioning or superseding a contract; what bets read from it |
| [baseline and refresh](references/baseline-and-refresh.md) | The two passes, how much to design before a version's milestones, refreshing at a version boundary, the as-built procedure in detail |
| [decisions](references/decisions.md) | Telling architecture from implementation choices, which decisions precede code, which log a record belongs in |
| [architecture index template](templates/architecture-index.md) | Writing `architecture/README.md` |
| [view template](templates/view.md) | Writing any view, concept or runtime file |
| [contract template](templates/contract.md) | Writing a contract |
| [ecosystem template](templates/ecosystem.md) | Writing `architecture/ecosystem.md` |
