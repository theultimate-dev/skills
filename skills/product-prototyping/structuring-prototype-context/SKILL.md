---
name: structuring-prototype-context
description: "Creates or adopts a prototype context: a context/ folder beside a prototype's code that keeps product, architecture, decisions, bets and notes in a light profile where ideas are tried and then kept or removed, with an AGENTS.md map, derived indexes, a decision record for the graduation trigger and a Keep a Changelog file per app. Adopts existing READMEs, specs, agent instructions and full-profile skeletons through an approved migration map. Use when the user says set up context for this prototype, adopt these docs into a prototype context, or move this context to prototype mode. Not for a product with planned versions and milestones (structuring-product-context)."
license: MIT
---

# Structuring prototype context

A prototype context is a `context/` folder in the code repository that holds a prototype's context in Markdown: why and what (`product/`), how it is structured (`architecture/`), why it is this way (`decisions/`), which ideas are being tried (`bets/`) and what is open (`notes.md`). It has no versions, no milestones and no roadmap: ideas are framed, shaped into small bets, built, tried, and then kept or removed. This skill creates the folder, adopts existing documents into it, and keeps its structure, map and indexes sound. The other `product-prototyping` skills fill it: `framing-prototype-ideas`, `shaping-prototype-bets`, `building-prototype-bets` and `closing-prototype-bets`.

## Choose the mode

| Mode | When | Output |
|---|---|---|
| Create | No product documents yet, or only a rough idea | The skeleton, `AGENTS.md`, `README.md`, the decision log, the board, `notes.md` and a changelog per app |
| Adopt | Existing READMEs, specs, agent instructions, decision notes or a full-profile skeleton | An approved migration map, then the content moved into the profile, links rewritten, and the originals removed or left as pointers |

Start every mode the same way:

1. Agree with the person where the context lives. The default is `context/` at the root of the code repository: one history means the commit a bet is approved at and the commits that build it are in the same log, and a removed bet is a revert. When the repository is not under git, offer to initialise it: a bet can be approved only at a commit.
2. Establish the product's name, its purpose in one sentence, the apps in the repository and where each keeps its changelog, and the graduation trigger. Recommend "a planned release or a second contributor": when it fires, the context moves to the full profile.
3. Read the project instructions and everything at the repository's root before proposing a layout. Never move, rewrite or delete a file before the person approves a map.

Read [the prototype profile](references/prototype-profile.md) before writing anything: the tree, house rules, statuses, ID formats, the bet and the reading order per task.

## Create

1. Write the skeleton from the profile's tree, leaving out what the prototype does not need. Copy [the agents map](templates/agents-map.md) to `context/AGENTS.md` and [the repository readme](templates/repository-readme.md) to `context/README.md`, and fill both. When the harness reads its own instruction file instead of `AGENTS.md`, add that file with a one-line import of `AGENTS.md`.
2. Write the product layer from the person's answers: [the overview](templates/overview.md), [the glossary](templates/glossary.md) with the terms already in use, [actors and use cases](templates/actors-and-use-cases.md), the requirements index from [the requirements index](templates/requirements-index.md), empty, and [the ID map](templates/id-map.md) as `product/requirements/id-map.md`, with no rows. Add a capability file from [the capability template](templates/capability-requirements.md) only for behaviour that is already built; [non-functional](templates/non-functional.md) only for targets the person states, and the index lists its row only when that file exists. Nothing unbuilt becomes a requirement row: new behaviour arrives through a bet.
3. Write the architecture index from [the architecture index](templates/architecture-index.md) and, only where they help, views from [the view template](templates/view.md), [contracts](templates/contract.md) and [external dependencies](templates/ecosystem.md). Every section carries `Status: built`; a contract carries it beside its Version, because Status is the code's and the version's status is the person's agreement.
4. Start the decision log with `decision-records` when it is installed: record 0001, the index and the link from `AGENTS.md`, then one record that adopts the prototype profile and states the graduation trigger. Otherwise create `decisions/README.md` with the index table and those two records in four sections (Context, Options, Decision, Consequences).
5. Write the empty bet board from [the bet board](templates/bet-board.md) as `bets/README.md`, and [the notes register](templates/notes.md) as `notes.md`. Give `research/` and any other folder an index from [the folder index](templates/folder-index.md). Indexes are rebuilt from the files they list, never hand-edited; the one exception is `architecture/README.md`, whose authored sections are kept and only its derived parts are rebuilt: the Contracts table and the oldest verified-on date.
6. Give each app a changelog outside `context/`. With `release-process` installed, let it create the file; otherwise copy [the changelog skeleton](templates/changelog.md). Leave an existing changelog as it is. When the person wants a baseline for the behaviour already built, the changelog template says how it is written.
7. Propose two pointer lines for the code repository's root `AGENTS.md`: the context map (`context/AGENTS.md`) and the decisions index (`context/decisions/README.md`). Write them when the person agrees. The pointer lines and a missing app changelog are the only changes this skill makes outside `context/` in Create.

## Adopt

Read [adopting into the profile](references/adopting-into-the-profile.md) before the first step.

1. **Inventory.** Read every source end to end, and the code where a source claims behaviour. Number every section by its heading path, down to the level where content changes kind. Every document read gets a row per section, the ones that only stay where they are included, as `drop` rows naming where they stay, so that line coverage can be checked.
2. **Classify** each section: built behaviour, unbuilt plan, architecture, decision or rationale, risk or open question, evidence, or code-side instructions. Decide for every statement of behaviour whether the code has it.
3. **Map** every inventory row in [the migration map](templates/migration-map.md) with a destination and one treatment: move, split, merge, convert, derive or drop. Built behaviour becomes `built` rows. Unbuilt plans, and unbuilt architecture that no retained open bet introduces, become framing notes with verdict `park`, or open questions, and never requirement rows or `planned` sections. A planned bet from an earlier profile keeps a numbered bet file with Status `removed`. An existing context folder, such as a full-profile skeleton, is restructured through the map's "Existing files" rows, one for every file, with the treatments restructure, fill, rebuild and keep as well. Documents beside the context, such as an app README or agent instructions, change only through its "Beside the context" rows. No row is left unmapped; every drop states its reason.
4. **Find conflicts and duplicates**, including sources that disagree with the code. Merge true duplicates. Every real conflict becomes an open question in `notes.md` with a recommended answer, unless the person settles it on the spot. A version number in the app's build settings is not a conflict: the adopting reference says why the context leaves it out.
5. **Separate decisions.** A decision the sources state as made becomes a record with status `accepted` only when the person made it; otherwise `proposed`. Write the profile record with the graduation trigger as in Create.
6. **Save and present the map.** Save it as `research/YYYY-MM-DD-migration-map.md`, then present it in one message that fits on one screen. The message summarises by count and by exception and names the saved map for the rows: counts per treatment and destination, the `built` rows with their evidence, the parked notes, the decision records and their statuses, the existing files, the beside-the-context rows with what each changes, the judgment calls, then the exceptions: the conflicts with recommendations, what is dropped and why, and what the sources lack. Ask for approval. Only explicit approval counts, and a beside-the-context row needs its own agreement; an edit request means revise and present again.
7. **Move.** First record the approval in the saved map: the Approved line, the person's words on each conflict, judgment call and beside-the-context row, and every row that waited on an answer rewritten to the decided text, with a History line for each change. Then write each destination in the profile's format, using the templates. Keep an ID exactly as the source wrote it when it is unique and fits the scheme; give any other a catalogue ID and record the pair in `product/requirements/id-map.md`, which also records every ID reserved at adoption; sources with no IDs and no reservations leave it with no rows. Number files for parked legacy bets so that the board and the next bet number see them. Rewrite links to the sources as relative links to the new homes. Create the files of Create that are still missing: board, notes, indexes, changelog, pointer lines.
8. **Verify** with the checks in the adopting reference, against the inventory: every row's content is present at its destination or has a drop reason, ID tables keep their counts, every `built` row and `built` architecture section has evidence, no requirement row describes something unbuilt, every `planned` section has an open owning bet, and every relative link resolves. Add the result as Verification to the saved map: the approved map plus Verification is the evidence of where things went.
9. **Commit and remove the originals.** Adoption makes two commits back to back, only as far as the person agrees. The first holds `context/`, with the removal of the originals that live in it, and any new file beside it that `context/` links to, such as a new app changelog, so that every link resolves at every commit. The second holds the edits to existing files beside the context. Remove originals in the context folder once the person confirms and the originals are committed, so git history keeps them. Originals beside the context are removed or replaced by pointers only through their agreed rows; a row without agreement stays as it was and is reported as a fact kept in two places. Without git, keep the originals and say why.

## Make it findable for agents

- `AGENTS.md` is a table of contents of about 100 lines: the map, the reading order per task, the house rules and the apps' changelogs. It never explains the product.
- Folder indexes carry one line per file: path and what it answers.
- IDs are greppable: one prefix per capability, `NFR-`, `UC-`, `RSK-`, `OQ-`, four-digit decisions, two-digit bets.
- The context and the code share one history. Context commits and code commits stay separate so that a removed bet can revert exactly the code.

## Hand back

Report the mode, the files written per folder, where the map is saved, the open questions raised, the gaps found, the decision records and their statuses, and the pointer lines written or declined. Say what comes next: `framing-prototype-ideas` for the first idea, then `shaping-prototype-bets`. When the repository has no commit yet, say that the first bet cannot be approved until it has one. When the context graduates later, `structuring-product-context` does the restructure. Commit only as far as the person agrees: adoption makes the two commits of step 9, and the code stays out of them.

## When a sibling skill is missing

Name the missing skill in one line, then produce its essential outcome here. For `decision-records`: numbered four-section records and an index row each. For `release-process`: the changelog skeleton, with the `[Unreleased]` section ready for the first bet's entry. For the other `product-prototyping` skills: leave the folder's index with a one-line note of what it still needs. Do not guess content the sources do not hold.

Without file access, return the map, the conflicts and the skeleton as complete Markdown with file names, and say that nothing was written.

## References

| Read | When |
|---|---|
| [prototype profile](references/prototype-profile.md) | Any mode: the tree, house rules, statuses, ID formats, the bet, reading order per task |
| [adopting into the profile](references/adopting-into-the-profile.md) | Adopt: inventory, built or planned, treatments, existing files, beside the context, conflicts, verification, a worked example |
| [agents map](templates/agents-map.md) | Writing `context/AGENTS.md` |
| [repository readme](templates/repository-readme.md) | Writing `context/README.md` |
| [overview](templates/overview.md) | Writing `product/overview.md` |
| [glossary](templates/glossary.md) | Writing `product/glossary.md` |
| [actors and use cases](templates/actors-and-use-cases.md) | Writing `product/actors-and-use-cases.md` |
| [capability requirements](templates/capability-requirements.md) | Writing a capability file of built behaviour |
| [requirements index](templates/requirements-index.md) | Writing or rebuilding `product/requirements/README.md` |
| [non-functional](templates/non-functional.md) | Writing `product/requirements/non-functional.md` |
| [notes](templates/notes.md) | Writing `notes.md`, the open questions and risks |
| [architecture index](templates/architecture-index.md) | Writing or rebuilding `architecture/README.md` |
| [view](templates/view.md) | Writing a view, concept or runtime scenario |
| [contract](templates/contract.md) | Writing a contract |
| [ecosystem](templates/ecosystem.md) | Writing `architecture/ecosystem.md` |
| [bet board](templates/bet-board.md) | Writing the empty `bets/README.md` |
| [folder index](templates/folder-index.md) | Writing or rebuilding any other folder's `README.md` |
| [migration map](templates/migration-map.md) | Presenting and saving the map in adopt |
| [ID map](templates/id-map.md) | Writing `product/requirements/id-map.md`, empty when the sources carry no IDs |
| [changelog](templates/changelog.md) | Giving an app a changelog when `release-process` is missing, or writing a baseline section |
