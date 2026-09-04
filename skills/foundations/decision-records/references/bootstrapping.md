# Bootstrapping a decision log

Use this when the project has no `decisions/` directory, or has one without an index or without a link from the agent instructions.

## 1. Create the directory and the index

Create `decisions/README.md`:

```markdown
# Decisions

Short records of the decisions that shape this project. Read this index first; open a record only when you need the reasoning. New records take the next number. Accepted records are never edited or renumbered, only superseded.

| # | Decision | Status | Summary |
|---|---|---|---|
| [0001](0001-record-decisions.md) | Record decisions as short records in `decisions/` | accepted | Four-section records, indexed here, linked from `AGENTS.md`. Supersede, never rewrite. |

Statuses: `proposed` (under discussion), `accepted` (in force), `deprecated` (no longer applies and nothing replaces it), `superseded` (replaced by a newer record; both link to each other).
```

If the project uses `CLAUDE.md` and has no `AGENTS.md`, say `CLAUDE.md` in the summary.

## 2. Write record 0001

The first record is the decision to keep records. It is short and it sets the conventions everyone will follow. Adapt it: the Context should name the actual project and its situation.

```markdown
# 0001: Record decisions as short records in `decisions/`

- Status: accepted
- Date: YYYY-MM-DD

## Context

Two or three sentences: this project makes choices whose reasons vanish; agents and new contributors need those reasons; there is no place to look them up today.

## Options

1. **No records.** Reasons stay in commit messages and chat history, and scatter.
2. **Full ADR tooling.** More structure than this project needs; long templates invite filler.
3. **Short records with an index.** One file per decision, four sections, listed in `decisions/README.md`.

## Decision

Option 3. Files are `decisions/NNNN-kebab-title.md`, numbered from 0001 and never renumbered. Each record has `# NNNN: Title`, `- Status:`, `- Date:`, then Context, Options, Decision, Consequences, one to two pages. Statuses: proposed, accepted, deprecated, superseded. An accepted record is never edited; a new record supersedes it and both link to each other. `decisions/README.md` indexes every record and `AGENTS.md` links the index.

## Consequences

- Reasons survive. Agents read the index first and records on demand.
- A structural change without a record is incomplete work.
- A small discipline cost on every significant choice.
```

## 3. Link the index from the agent instructions

Agents read `AGENTS.md` (Codex, Copilot, Pi, Cursor, and others) or `CLAUDE.md` (Claude Code, which can import `AGENTS.md` with a single line containing `@AGENTS.md`). Add this section to whichever file the project uses. If it has neither, create `AGENTS.md` with a one-paragraph description of the project and this section, and add a `CLAUDE.md` whose only line is the import if Claude Code is in use.

```markdown
## Decisions

Decisions that shape this project are recorded in [decisions/README.md](decisions/README.md). Read the index before changing structure, conventions, or dependencies. Record new decisions as a new numbered file; never edit an accepted record, supersede it.
```

Use a markdown link. Do not write the path with a leading `@`: in Claude Code that imports the whole index into every session, which defeats the point of having an index.

## 4. Keep the index honest

Every time a record is added or its status changes, the index row changes in the same commit. If the project has a validation script or CI, a check that every `decisions/NNNN-*.md` appears in the index is a ten-line job and worth adding.

## 5. Tell the user what changed

List the files created or edited and show the `AGENTS.md` section. If you could not write files, hand over the three snippets above, filled in, and say so.
