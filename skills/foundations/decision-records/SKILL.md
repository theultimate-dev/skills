---
name: decision-records
description: "Keeps a project's decision log: short decision records (ADRs) in a decisions/ directory with an indexed README linked from AGENTS.md or CLAUDE.md. Use when the user settles a trade-off, asks to record or write up a decision, asks why something was chosen, mentions ADRs or architecture decisions, or when a project has no decision log yet and a structural choice is being made. Also use to adopt or tidy an existing docs/adr or docs/decisions folder."
license: MIT
---

# Decision records

A decision record captures one decision, why it was made, and what it costs, in a page a busy engineer reads in five minutes. The log of records is how a project remembers its own reasoning, and how an agent opening the project later avoids undoing a choice whose reason it cannot see.

This skill maintains that log: it creates one where none exists, writes new records, keeps the index in sync, and makes sure agents find it through the project's `AGENTS.md` or `CLAUDE.md`.

## What a good log looks like

```
decisions/
├── README.md                     index: number, title, status, one-line summary
├── 0001-record-decisions.md      the first record is the decision to keep records
├── 0002-kebab-title.md
└── ...
```

Each record: `# NNNN: Title`, then `- Status:` and `- Date:` lines, then Context, Options, Decision, Consequences. Template in `templates/decision-record.md`; writing guidance in `references/writing-a-record.md`.

Statuses: `proposed`, `accepted`, `deprecated`, `superseded`. The decision text of an accepted record never changes; a new record supersedes it and both link to each other. Numbers are never reused or renumbered.

## Workflow

### 1. Find out what state the project is in

Look, in this order:

- `decisions/` with a `README.md` index: the log exists in this skill's shape. Go to step 2.
- `docs/adr/`, `docs/decisions/`, `adr/`, `architecture/decisions/`, files named `ADR-*.md`, an `adr-tools` `.adr-dir` file or a `log4brains` config: the project already keeps records another way. Read `references/existing-adrs.md` before touching anything. The rule is to adopt in place, never to move or renumber.
- Nothing: bootstrap. Read `references/bootstrapping.md`. It covers the directory, the index, record 0001, and the section in `AGENTS.md` or `CLAUDE.md`. Create `AGENTS.md` if the project has neither.

### 2. Confirm there is a decision to record

Record a decision the user has made, or is making now with you. Not one you infer. If the conversation settled a trade-off ("let's go with Postgres", "we keep the monorepo"), name it back in one sentence and ask whether to record it. If the user asks for a record on something still open, write it with `Status: proposed` and say so.

Not every choice deserves a record. The test: would a competent newcomer, or an agent, plausibly undo or re-argue this without knowing the reason? Library and platform picks, data model shapes, process rules, things rejected on purpose: yes. Formatting preferences and config values nobody debated: no.

### 3. Draft the record

Use the template. Next free number, four digits, zero-padded. Filename `NNNN-kebab-title.md`. Title states the decision ("Use Postgres for the event store"), not the topic ("Database").

Context states the forces without arguing. Options list every option seriously considered, the chosen one included, each with the reason it won or lost in a line or two. Decision states what was chosen and the concrete rules that follow. Consequences list what gets easier, what gets harder, and what must now be done. One page, two at most. `references/writing-a-record.md` has the detail and the common mistakes.

Show the draft before writing it to disk when the decision is being made in this conversation. Write directly when the user asked you to record something already agreed.

### 4. Update the index

Add a row to `decisions/README.md`: number linked to the file, title, status, one-line summary. Keep rows in numeric order. When the new record supersedes an older one: set the older record's status to `superseded`, add `- Superseded by: NNNN` under its date line, add `- Supersedes: MMMM` to the new record, and update both index rows.

### 5. Make sure agents will find it

`AGENTS.md`, or `CLAUDE.md` when that is what the project uses, links `decisions/README.md` with a plain markdown link and one sentence: read the index before changing structure or conventions. A link, not an import, so the index loads when a task needs it rather than in every session. If the section is missing, add it; the snippet is in `references/bootstrapping.md`.

### 6. Report

Give the user the record number and path, the index row, and any record whose status changed. If the decision implies follow-up work, name it.

## When you cannot write files

In a chat client without a filesystem, or without the repository at hand, produce the complete record and the index row as Markdown for the user to paste, and say plainly that nothing was written. Never report a record as created when it was not.

## Rules worth keeping in mind

- One decision per record. A draft that contains two decisions gets split.
- Never edit the decision text of an accepted record, never renumber, never delete. Supersede. Typos and dead links may be fixed.
- Never record a decision the user has not made. `proposed` exists for that.
- Write for the reader, not for completeness. Cut whatever the reader does not need to understand the choice.
- Respect an existing convention. A project on MADR stays on MADR; this skill adds the index and the `AGENTS.md` link and follows the house template.

## References

| Read | When |
|---|---|
| `references/bootstrapping.md` | The project has no decision log, or has one without an index or without the `AGENTS.md` link |
| `references/writing-a-record.md` | Drafting any record, choosing a status, superseding |
| `references/existing-adrs.md` | The project already keeps ADRs in another folder, format, or tool |
| `templates/decision-record.md` | The file to copy for every new record |
