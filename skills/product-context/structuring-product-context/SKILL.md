---
name: structuring-product-context
description: "Creates or adopts a product context repository: a Markdown repository, kept apart from the code, that holds a long-running product's whole context in layers sorted by how often they change (product, architecture, decisions, a roadmap with bets, design, research), with an AGENTS.md map, folder indexes and house rules. Adopts existing PRDs, specs and design docs by mapping every section to its new home, listing conflicts and duplicates as open questions, and moving content only after the user approves the map. Use when the user says set up a product context repository, set up a docs repo for this product, organize these specs, import this PRD, or restructure the product docs. Not for one feature's spec (specifying-work-items), a single product brief (shaping-product-briefs), or auditing drift after delivery (reconciling-product-context)."
license: MIT
---

# Structuring product context

A product context repository holds a long-running product's whole context in Markdown, kept apart from the code: why and what (`product/`), how it is structured (`architecture/`), why it is this way (`decisions/`), and when and in what order (`roadmap/`, with bets). Agents building the product in a code repository read it read-only, at the commit a bet was handed over at. This skill creates the repository, adopts existing product documents into it, and keeps its structure, map and indexes sound. The other `product-context` skills fill the layers.

## Choose the mode

| Mode | When | Output |
|---|---|---|
| Create | No product documents yet, or only a rough idea | The skeleton, `AGENTS.md`, `README.md` and folder indexes, ready for the other skills |
| Adopt | Existing PRDs, specs, design docs, decision notes or roadmaps, in one file or many | An approved migration map, then the content moved into the layers, links rewritten, and the originals removed |
| Restructure | The repository exists but has drifted: misplaced files, rates of change mixed in one file, a missing layer | A restructure map, under the same approval rule as adopt |

Start every mode the same way:

1. Agree with the user where the repository lives; the default is a sibling of the code repository named `<product>-context`. Read the project instructions and everything at its root. When it is not under git, initialise it with the user's agreement: a bet can be handed over only at a commit.
2. Establish the product's name, its purpose in one sentence, the versions in play, and the code repositories that will build it. Names are enough; the code repositories need not exist yet.
3. Never move, rewrite or delete a file before the user approves a map.

## The layers

| Directory | Holds | Changes |
|---|---|---|
| `product/` | Overview, glossary, actors and use cases, the requirement catalogue, non-functional requirements | Rarely |
| `architecture/` | C4 views, components, data, deployment, concepts, runtime scenarios, contracts, external dependencies | Per version and per closed bet |
| `decisions/` | Product and architecture decision records, with an index | Append-only |
| `roadmap/` | Versions, version briefs, milestones, bets, the risk and open-question registers | Often |
| `design/<initiative>/` | Product and design work for one initiative, prototypes included | Per initiative |
| `research/` | Dated evidence | Append-only |

The house rules keep it coherent: one home per fact; volatile files link to stable ones, never the reverse, though a plain-text ID may record provenance; IDs are permanent; indexes are derived; accepted decisions are superseded, never edited; research is evidence, not truth; point at the code, never copy it; Markdown only, except prototypes under `design/`; code repositories only read. Read [layers and rules](references/layers-and-rules.md) for the tree, the ID formats, the statuses and the reading order per task before writing anything.

## Create

1. Write the skeleton from the layers reference. Copy [the agents map](templates/agents-map.md) to `AGENTS.md` and [the repository readme](templates/repository-readme.md) to `README.md`, and fill both. When Claude Code is in use, add `CLAUDE.md` with the single line `@AGENTS.md`.
2. Give each folder an index. `product/requirements/README.md`, `architecture/README.md`, `roadmap/README.md` and each bet board come from their owning skills' templates when those skills are installed: `curating-product-requirements`, `designing-system-architecture`, `planning-product-roadmaps` and `shaping-bets`. Every other folder, and those when the owner is missing, uses [the folder index](templates/folder-index.md). Indexes are rebuilt from the files they list, never hand-edited.
3. Start the decision log with `decision-records` when it is installed: record 0001, the index, and the link from `AGENTS.md`. Otherwise create `decisions/README.md` with the index table and a first record that adopts four-section records (Context, Options, Decision, Consequences).
4. Leave the layers' content to their skills. A rough idea goes through `shaping-product-briefs` or `guiding-product-discovery` first; their output comes back through `curating-product-requirements`.

## Adopt

Read [adopting documents](references/adopting-documents.md) before the first step.

1. **Inventory.** Read every source document end to end. Number every section by its heading path, down to the level where content changes kind, such as a table of requirements inside a chapter on scope.
2. **Classify** each section by what it is (product intent, requirement table, architecture view, runtime scenario, decision or rationale, plan, risk, open question, business, evidence, or framing) and by the version it concerns.
3. **Map** every inventory row in [the migration map](templates/migration-map.md): its destination, and one treatment: move, split, merge, convert, derive or drop. A split names every destination. A drop states its reason. No row is left unmapped.
4. **Find conflicts and duplicates** across the sources: one fact stated twice, two numbering schemes for the same decisions, a promise without a requirement behind it, counts that disagree. Merge true duplicates into one home. Every real conflict becomes an open question with a recommended answer, unless the user settles it on the spot.
5. **Separate decisions.** A decision the sources state as made becomes a decision record with status `accepted` only when the user made it; otherwise `proposed`. Rationale moves into the record, out of tables and plans.
6. **Present the map** in one message: counts per treatment and destination, every ID that gets a new catalogue ID, the decision records to be written and which of them as `accepted`, the conflicts with recommendations, what is dropped and why, and what the sources lack, such as a glossary, contracts or acceptance criteria. Ask for approval. Only explicit approval counts; an edit request means revise and present again.
7. **Move.** Write each destination file, in the owning skill's format when that skill is installed. Keep an ID exactly as the source wrote it when it is unique and fits the repository's ID scheme; give any other a catalogue ID and record the pair in `product/requirements/id-map.md`. Keep diagrams with the text they belong to, and each citation next to the claim it supports. Rewrite links to the source documents, including links to hosted copies, as relative links to the new homes.
8. **Verify** against the inventory: every row's content is present at its destination, every ID table has the same count as its source, and every relative link resolves. Save the map as `research/YYYY-MM-DD-migration-map.md`; it is evidence of where things went.
9. **Remove the originals** that live in the context repository, in the same change, once the user confirms and the originals are committed, so git history keeps them. Without git, keep them and say why. Originals stored elsewhere, such as in a code repository's `docs/`, are listed for the user to remove: this skill never writes outside the context repository.

## Restructure

Treat the misplaced files as sources and run adopt steps 1 to 9 on them. Typical moves: rationale out of requirement tables into decision records, a hand-edited index back to derived, a version-specific architecture file merged into the living description with `Since:` tags, duplicated risks merged into the register. Restructure moves content to the right place; finding broken links, stale indexes, reused IDs and facts kept twice is the drift audit of `reconciling-product-context`, which hands structural findings back here.

## Make it findable for agents

- `AGENTS.md` is a table of contents of about 100 lines: the map, the reading order per task, the house rules, and the code repositories that build the product, by name and remote. It never explains the product.
- Folder indexes carry one line per file: path and what it answers.
- IDs are greppable: one prefix per capability, `NFR-`, `UC-`, `RSK-`, `OQ-`, four-digit decisions, two-digit bets.
- Code repositories reach the context as [code repository access](references/code-repository-access.md) describes. This skill never writes into a code repository; a pointer there is the user's change.

## Hand back

Report the mode, the files written per layer, where the map is saved, the open questions raised, the gaps found, and the next steps: `curating-product-requirements` for the product layer and glossary, `designing-system-architecture` for the baseline, `planning-product-roadmaps` for versions and registers, then `shaping-bets`. When the repository has no commit yet, say that the first bet cannot be handed over until it has one. Commit only when the user asks.

## When a sibling skill is missing

Name the missing skill in one line, then produce its essential outcome here: for `decision-records`, a numbered four-section record and an index row; for the layer skills, leave the layer's index with a one-line note of what it still needs. Do not guess content the sources do not hold.

Without file access, return the map, the conflicts and the skeleton as complete Markdown with file names, and say that nothing was written.

## References

| Read | When |
|---|---|
| [layers and rules](references/layers-and-rules.md) | Any mode: the tree, house rules, ID formats, statuses, reading order per task, sizes |
| [adopting documents](references/adopting-documents.md) | Adopt and restructure: inventory, classification, treatments, conflicts, link rewriting, verification, a worked example |
| [code repository access](references/code-repository-access.md) | Explaining how code repositories read the context, pinning, single-repository agents, the optional pointer |
| [agents map](templates/agents-map.md) | Writing `AGENTS.md` |
| [repository readme](templates/repository-readme.md) | Writing `README.md` |
| [folder index](templates/folder-index.md) | Writing or rebuilding a folder's `README.md` |
| [migration map](templates/migration-map.md) | Presenting and saving the map in adopt and restructure |
