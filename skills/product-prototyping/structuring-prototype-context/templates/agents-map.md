# AGENTS.md

<!-- Copy to context/AGENTS.md. Keep it a table of contents of about 100 lines; never explain the product here. Delete this comment. -->

This is the prototype context for [product]: [one sentence on what the product is]. It lives in `context/` beside the code and holds product, architecture, decisions, bets and notes in the prototype profile: ideas are framed, shaped into bets, built, tried, and then kept or removed. Read this file first; open the linked files only when the task needs them.

The profile in one sentence: a bet is read at the commit it was approved at, building writes the code, the bet's Status and Build log and the board, and closing folds the result into the files below.

## Map

| Path | What it answers |
|---|---|
| `product/overview.md` | Why the product exists, its principles, assumptions and constraints |
| `product/glossary.md` | What the product's words mean |
| `product/actors-and-use-cases.md` | Who uses it and for what |
| `product/requirements/README.md` | The requirement catalogue: ID scheme, built and dropped rows, one file per capability |
| `architecture/README.md` | How the product is structured, which views exist, what is planned or built |
| `architecture/contracts/` | Interfaces several parts share |
| `decisions/README.md` | Decisions, including the graduation trigger; read the index before changing structure or conventions |
| `bets/README.md` | The bet board: every bet, its status and reserved IDs |
| `notes.md` | Open questions and risks |
| `design/` | Product and design work |
| `research/README.md` | Dated evidence and framing notes; never current truth |
| [`CHANGELOG.md` or `<app>/CHANGELOG.md`] | What changed for users, per app; outside `context/` |

## Reading order by task

| Task | Read |
|---|---|
| Frame an idea | `product/overview.md`, `product/requirements/README.md`, `decisions/README.md`, `architecture/ecosystem.md`, `notes.md`, `research/README.md` |
| Shape a bet | The framing note, the requirement files it touches, `architecture/contracts/`, `bets/README.md`, `notes.md` |
| Build a bet | The bet file at its pinned commit, then its Context pack, in order |
| Change requirements | `product/overview.md`, `product/glossary.md`, `product/requirements/README.md`, the capability file |
| Change the architecture | `architecture/README.md`, the affected views, `decisions/README.md` |
| Check status | `bets/README.md`, `notes.md` |
| Close a bet, or audit | The bet file, the files it touches, the derived indexes |

## House rules

1. One home per fact; everywhere else links to it by path or ID.
2. Volatile files link to stable ones, never the reverse; a plain-text ID may record provenance, a link may not.
3. IDs are permanent: never reuse or renumber; a dropped requirement stays, with its date and reason.
4. Folder indexes, the bet board, counts and the requirements index are derived; never edit them by hand. `architecture/README.md` keeps its authored sections; only its derived parts are rebuilt: the Contracts table and the oldest verified-on date.
5. Accepted decisions are superseded, never edited.
6. Research is evidence, not truth.
7. Point at the code, never copy it.
8. Markdown only, except prototypes under `design/`.
9. A bet is read at the commit it was approved at, so its shaped fields cannot drift. While a bet is open, the files its Context pack and Architecture › Relies on name change only through that bet, or with the person's agreement as a reshape. Research notes, `notes.md` rows and derived indexes may change at any time. Building writes the code and, in the bet file, only its Status and Build log, and rebuilds the board when the Status changes; closing writes the Result and the catalogue.

## Code and changelogs

| App | Path | Changelog |
|---|---|---|
| [name] | [path from the repository root] | [path] |

## Graduation

[The trigger recorded in `decisions/NNNN-title.md`, for example "a planned release or a second contributor". When it fires, use `structuring-product-context`.]
