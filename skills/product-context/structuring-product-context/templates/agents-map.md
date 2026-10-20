# AGENTS.md

<!-- Copy to AGENTS.md at the root of the product context repository. Keep it a table of contents of about 100 lines; never explain the product here. Delete this comment. -->

This is the product context repository for [product]: [one sentence on what the product is]. It holds the product's whole context in Markdown, apart from the code. Code repositories read it at the commit a bet was handed over at, and never write to it. Read this file first; open the linked files only when the task needs them.

## Map

| Path | What it answers |
|---|---|
| `product/overview.md` | Why the product exists, its principles, assumptions and constraints |
| `product/glossary.md` | What the product's words mean |
| `product/actors-and-use-cases.md` | Who uses it and for what |
| `product/requirements/README.md` | The requirement catalogue: ID scheme, statuses, one file per capability |
| `architecture/README.md` | How the product is structured, which views exist, what is planned or built |
| `architecture/contracts/` | Interfaces several bets share |
| `decisions/README.md` | Product and architecture decisions; read the index before changing structure or conventions |
| `roadmap/README.md` | Versions, the current focus, parked ideas |
| `roadmap/v[N]/README.md` | The current version's brief and milestones |
| `roadmap/v[N]/bets/README.md` | The bet board |
| `roadmap/risks.md`, `roadmap/open-questions.md` | The registers |
| `design/` | Product and design work per initiative |
| `research/` | Dated evidence; never current truth |

## Reading order by task

| Task | Read |
|---|---|
| Build a bet | The bet file, then its Context pack, in order, at the pinned commit |
| Change or add requirements | `product/overview.md`, `product/glossary.md`, `product/requirements/README.md`, the capability file |
| Change the architecture | `architecture/README.md`, the affected views, `decisions/README.md` |
| Plan, or check the status | `roadmap/README.md`, the version brief, the bet board, the registers |
| Shape bets | The version brief, the milestone's requirement files, `architecture/contracts/`, the bet board |
| Close a bet, or audit | The bet file and the files it touches, the derived indexes |

## House rules

1. One home per fact; everywhere else links to it by path or ID.
2. Volatile files link to stable ones, never the reverse; a plain-text ID may record provenance, a link may not.
3. IDs are permanent: never reuse or renumber; a dropped requirement stays, with its reason.
4. Folder indexes, the bet board, coverage tables and counts are derived; never edit them by hand.
5. Accepted decisions are superseded, never edited.
6. Research is evidence, not truth.
7. Point at the code, never copy it.
8. Markdown only, except prototypes under `design/<initiative>/`.
9. Code repositories only read this repository, at a pinned commit.

## Code repositories

| Repository | Remote | Builds |
|---|---|---|
| [name] | [remote URL] | [what it builds] |
