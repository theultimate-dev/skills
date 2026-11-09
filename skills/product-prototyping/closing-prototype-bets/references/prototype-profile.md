# The prototype profile

The light profile of a context folder for a prototype: a product where ideas are tried, then kept or removed, and where no versions or milestones are planned. It keeps the discipline of a full product context (one home per fact, permanent IDs, derived indexes, decisions that are superseded) and drops what a prototype cannot use: versions, milestones, a roadmap, the `Since:` tags and a separate context repository. Every skill of the category carries this file unchanged, so it describes the profile in general terms and names the skills it hands work to in backticks.

The examples use a fictional product, Quill: a single-user web app that tracks daily writing streaks. Its code repository holds `context/`, and its changelog is `CHANGELOG.md` at the repository root.

## Where it lives

`context/` at the root of the code repository, and nowhere else. One repository means one history: the commit a bet is approved at and the commits that build it sit in the same log, and a removed bet is a revert. A context that must live apart from its code is a reason to use the full profile. An app keeps its own `CHANGELOG.md` beside its code, outside `context/`; when the repository is one app, that is `CHANGELOG.md` at the root.

## The tree

```
context/
├── AGENTS.md          map, reading order per task, house rules, the profile in one sentence
├── README.md          for people: what it is, where to start, how work flows
├── product/
│   ├── overview.md, glossary.md, actors-and-use-cases.md
│   └── requirements/  README.md (derived), <capability>.md, id-map.md, and non-functional.md
│                      only when a target is stated
├── architecture/      README.md, plus only the views that help: context.md, containers.md (when
│                      there is more than one container), ecosystem.md, contracts/, concepts/, runtime/
├── decisions/         README.md (index), NNNN-title.md
├── bets/              README.md (derived board), NN-slug.md
├── notes.md           open questions (OQ-) and risks (RSK-), two tables
├── design/            product and design work, offline HTML prototypes allowed
└── research/          README.md (derived), dated notes, framing notes included
CHANGELOG.md           Keep a Changelog; the app's file, outside context/
```

Omit what the prototype does not need. Keep the directory names; agents rely on them.

## House rules

1. **One home per fact.** Every fact lives in one file. Everywhere else links to it by path or ID.
2. **Volatile links to stable, never the reverse.** A bet links to requirements, architecture and decisions; a requirement never links to a bet. A derived index may link to anything it indexes, and a plain-text ID may record provenance, such as `OQ-02` or `bet 03 removed`.
3. **IDs are permanent.** Never reuse or renumber one. A requirement that no longer applies stays in its table as `dropped`, with the date and the reason.
4. **Indexes are derived.** Folder READMEs, the board, counts and `requirements/README.md` are rebuilt from the files they index, by the skill that changed those files, and every skill that changes a bet's Status rebuilds the board in the same change. Never edit them by hand. The one exception is `architecture/README.md`, a mixed file: its authored sections (strategy, quality goals, checklist) are kept as written, and only its derived parts are rebuilt: the Contracts table, from the contract files, and the oldest verified-on date, from `architecture/ecosystem.md`.
5. **Decisions are superseded, never edited.** An accepted record's decision text never changes; a new record supersedes it.
6. **Research is evidence, not truth.** A note records what was found on a date. A current fact belongs in its layer, citing the note.
7. **Point at the code, never copy it.** Describe structure, contracts and rules; leave file layouts and code to the code.
8. **Markdown only,** except prototypes under `design/`, which may be offline HTML.
9. **A bet is read at the commit it was approved at, so what it reads stays still.** The approved bet's shaped fields cannot drift. While a bet is open, the files its Context pack and Architecture › Relies on name change only through that bet, or with the person's agreement as a reshape. From approval, building writes the code and, in the bet file, only its Status and Build log; closing writes the Result and the catalogue. Research notes, `notes.md` rows and derived indexes may change at any time. Before approval, shaping writes the bet, the board, the planned sections and `notes.md` rows.

## Statuses

| Thing | Statuses | Where |
|---|---|---|
| Requirement | `built`, `dropped` with date and reason; no version column, no `planned` or `deferred` | Status column of the capability file |
| Architecture section | `Status: built`, or `Status: planned` while the bet that introduces it is open; no `Since:` tags | One line under the section heading |
| Contract | `proposed`, `accepted`, `superseded`, per contract version (its own major.minor, not a product version) | The contract's header |
| Decision record | per `decision-records` | The record |
| Bet | `shaped`, `approved`, `building`, `built`, then `kept` or `removed`; `stopped` when the appetite runs out | The bet file's `Status:` line, the only authoritative place; the board copies it |
| Framing note | verdict `shape`, `park` or `stop` | The note's Verdict section |
| Risk | `open`, `closed` | `notes.md` |
| Open question | `open`, `resolved` with a link to the answer | `notes.md` |

Architecture describes what is built. When a kept bet drops a requirement, closing deletes the sections that served only that requirement and narrows a shared one to what remains, as it already does for cut scope; the bet file and the decisions keep the history.

A bet moves `shaped` to `approved` at Gate 1 (the person approves it, on a current, passing readiness check), `approved` to `building` when work starts, which follows the approval at once unless the person holds it, `building` to `built` when every check that is not a person's-eye check passes and the review has no blocking finding, and `built` to `kept` or `removed` at Gate 2 (the person decides after trying it). A `built` bet with an explicit in-scope repair request from the person goes back to `building` with its pin, base commit and consumed working time, within the remaining appetite, and returns to Gate 2 with a refreshed Try it block. A `stopped` bet, or a `building` bet paused because a contract or decision must change, is reshaped (back to `shaped`, then Gate 1 again) or closed as `removed`. Whether removal reverts anything is decided by the code commit list in the Build log, never by Status: a bet with no listed code commit closes with nothing to revert, through `closing-prototype-bets`.

## IDs

| Thing | Format | Example |
|---|---|---|
| Requirement | `<CAP>-NN`, a 2-4 letter capability prefix, one per capability file | `STK-03` in `requirements/streaks.md` |
| Non-functional requirement | `NFR-NN` | `NFR-02` |
| Use case | `UC-NN` | `UC-01` |
| Risk, open question | `RSK-NN`, `OQ-NN` | `RSK-02`, `OQ-04` |
| Decision record | `NNNN`, four digits | `0003` |
| Bet | `NN`, two digits, never reused, even when removed | `03` in `bets/03-weekly-recap.md` |
| Acceptance check | `Cn (<requirement ID>)`, numbered within one bet | `C2 (STK-03)` |

A bet reserves the next free IDs for the requirements it adds, and the board lists them, so two open bets cannot take the same number. The numbers continue after the highest ever used, read from three places: the catalogue (dropped rows included), the board (reservations of removed bets included) and `product/requirements/id-map.md`. The map links the local IDs of adopted documents to catalogue IDs and records the IDs reserved at adoption for planned or deferred rows moved to parked notes; it is append-only, and `structuring-prototype-context` writes it; shaping appends only a claim line. A bet's own reservations never count as a collision for that bet. A bet that builds a requirement parked at adoption claims its reserved ID: the delta keeps that ID as `new`, `id-map.md` gets an appended line naming the claiming bet, and readiness treats the reservation as the bet's own. Unrelated scope never reuses a reserved number.

## The bet

One file per bet, `bets/NN-slug.md`, written from `shaping-prototype-bets`'s template. The header lines and the sections, in this order, are:

| Part | Holds |
|---|---|
| `# Bet NN: <the outcome, in a few words>` | The title states the outcome |
| `Status:` | One of the bet statuses |
| `Appetite:` and `Framing:` | `½ day`, `1 day` or `2 days` of working time, a total ceiling across the bet's life, in which waits for the person, recorded in the working log, do not count; a raised appetite is a new total in the person's words, never time on top; the path of the framing note that led to the bet, whose `Bet:` line shaping fills with the bet's number and path |
| `Autonomy:` | What the builder may do without asking, in four fields: `code commits: <branch>; context commits: yes or no; push: yes or no; revert on remove: yes or no`. Proposed at shaping and approved at Gate 1 with the person's words; that approval is also the go-ahead to build and the person's direct request for the commits the line names |
| `Context pinned:` | The full SHA of the commit the bet was approved at; `not yet` until then |
| `## Outcome` | Who can now do what, and what they see, in two to four sentences |
| `## Requirement deltas` | A table: reserved ID, change (`new`, `changed` or `dropped`), the text or the reason |
| `## Acceptance checks` | `Cn (ID)` lines, each an observable result with a `Method:` of `test`, `build`, `run and observe`, `inspect output` or `person's eye`; a leading `~` marks a check that may be cut |
| `## Boundaries` | No-go, Rabbit hole (patched by, or if it bites), `~ Cuttable` |
| `## Keep or remove` | The signal the person judges at Gate 2, and what removing would leave behind |
| `## Architecture` | Touches, Introduces (planned sections), Relies on (decisions, contracts) |
| `## Context pack` | The files to read, in order, each with why; five to ten is a guideline |
| `## Build log` | Written by `building-prototype-bets`: the base commit and consumed working time; every code commit by SHA, oldest first, with any context commit between them named; each check's result and evidence; cuts with reasons; review findings and fixes; the Try it block; and the dated lines of a bet's history (below) |
| `## Result` | Written by `closing-prototype-bets`: kept or removed, the date and the person's words, the lesson |

Read the shaped fields at the commit in `Context pinned`, so later edits cannot change what was approved: every header line except Status and Context pinned, and every section except the Build log and the Result. Read Status, Context pinned, the Build log and the Result from the working copy, because the builder or shaper may have left them uncommitted, and report any uncommitted state (`git status --short -- context/bets/NN-slug.md`). A bet file stays readable in one sitting.

### A bet keeps its history

- **Reshaping** keeps the Build log's code commits, base commit and consumed working time. The pin goes back to `not yet` and the Autonomy line to a proposal, but the replaced approval stays in the Build log as a dated line, `Approved YYYY-MM-DD at <sha>: <autonomy line>`. The reshape itself is a dated `Reshaped YYYY-MM-DD:` line.
- **Authority to act on a bet** (closing, above all) comes from one place at a time. A bet that is `approved`, or has any valid current pin, uses the `Autonomy:` line at that pin, so a reapproval that tightened the grant replaces the older one at once, before the Build log has a new dated line. Only a bet whose pin is `not yet` because a reshape replaced it falls back to the last dated `Approved` line of its Build log, because its own Autonomy line is a proposal and grants nothing. A bet never approved has no authority beyond the person's explicit current words.
- **Appetite** is one ceiling for the bet's whole life. Reapproval never restarts the clock.
- **Continuation.** `building-prototype-bets` treats an `approved` bet with a non-empty Build log as a continuation: it keeps the base commit, the consumed time and the commits, and appends the new pin.
- **A split** moves only scope with no implementation. Started scope and its commits stay in the original bet, so every code commit belongs to exactly one bet.
- **Contracts and decisions** that must change while a bet is paused: decisions are superseded through `decision-records`, a contract gets a new version, then readiness and Gate 1 run again.

`bets/README.md` is the board: one row per bet with its status, appetite, reserved IDs and framing note, rebuilt from the bet files' header lines and Requirement deltas.

## Where each fact lives while a bet is open

The bet holds its requirement deltas (new rows with text, changed rows with the new text, dropped rows with the reason) until it closes. The catalogue in `product/requirements/` holds only `built` and `dropped` rows. An architecture element that the bet introduces and other files must reference, such as a contract or a concept, may be written at shaping as `Status: planned`. Everything else reaches `architecture/` at close. Closing as kept turns the deltas into catalogue rows and `planned` into `built`; closing as removed writes the new IDs as `dropped` with `bet NN removed: <reason>`, leaves changed rows as they were, and deletes the planned sections. On keep, an Introduces entry that belongs only to cut scope is deleted, and a partly built one is narrowed to what was built. A capability file for a new prefix does not exist until closing creates it from the capability template. On keep, a new requirement whose checks were all cut is written `dropped` with `bet NN: cut, <reason>`, a changed one whose checks were all cut keeps its old text, and one whose checks were partly cut is written `built` with its text narrowed to what was built.

## Adoption keeps numbers

`structuring-prototype-context` classifies adopted material against the code. Requirements are `built` only with evidence. Architecture is classified the same way: `built` needs evidence, and unbuilt architecture goes to a parked framing note unless a retained open bet introduces it, so every `planned` section has an open owning bet. A legacy bet parked at adoption keeps a numbered bet file with Status `removed` and the Result "parked at adoption: not tried, see <note>", so the board and the next bet number see it. A question withdrawn before it is written to `notes.md` leaves no row there: the migration map's History records the withdrawal, and its number is not reused.

## The changelog

Building adds the bet's entry under `[Unreleased]` in the app's changelog, inside the bet's code commits. Removing a bet reverts those commits, which takes the entry with them. When a release already carries the entry, closing adds a `Removed` entry instead. Versions are cut only when the person asks, with `release-process` when it is installed. When the person wants a baseline for the behaviour already built, adoption writes one dated section under the label they give it, with one line per built capability and no tag; it omits the comparison links when the repository has no remote. A version number in the app's build settings is the person's to declare, as their own signal that the prototype phase is over, so adoption leaves it out of the map, the notes and the records: the changelog's sections are the only versions the context writes.

## Commits

Commit code as each step of a build finishes, so the history grows with the work and every result ties to a commit. Write commit messages as Conventional Commits, such as `feat: show the weekly recap` or `docs(context): start bet 03`, so the history reads the same from bet to bet. When the project's instructions, contributing guide or commit tooling state another convention, follow that one. Keep code commits and context commits separate, so a remove can revert exactly the code. The Build log lists every code commit by SHA, oldest first, and names any context commit that sits between them; every code commit belongs to exactly one bet. Before any context commit, check the index for staged changes outside the approved paths and stop on them, then verify that the staged diff holds exactly the approved changes. Review the code with the context folder excluded, the app's changelog included: `git diff <base>..<head> -- . ':(exclude)context'`. Commit only as far as the bet's Autonomy line allows: code commits on its branch, context commits only when it says `yes`, a push only when it says `yes`, a revert on remove only when it says `yes`. Shaping recommends the branch the person works on, `yes`, `no`, `yes`, because a removed bet is undone by a revert on that branch, while a bet branch would need a merge to keep, which this loop does not have. Closing as removed reverts the listed code SHAs only, and a merge commit in the list stops for a reviewed plan. It makes the revert, with the `Removed` changelog line when the entry was released, as its one code commit, then writes the Result and the catalogue in a separate context commit.

Adoption makes two commits back to back. The first holds `context/` and any new file beside it that `context/` links to, such as a new app changelog, so every link resolves at every commit; the second holds the edits to existing files beside the context.

## Graduation

A decision record states when the context moves to the full profile; the recommended trigger is a planned release or a second contributor. When it fires, `structuring-product-context` (the full profile's skill, from the product-context plugin) restructures the context, and a new record supersedes the profile record.

## Reading order by task

`context/AGENTS.md` gives agents the shortest path:

| Task | Read |
|---|---|
| Build a bet | The bet file at its pin, then its Context pack in order |
| Change requirements | `product/overview.md`, `product/glossary.md`, `product/requirements/README.md`, the capability file |
| Change the architecture | `architecture/README.md`, the affected views, `decisions/README.md` |
| Check status | `bets/README.md`, `notes.md` |
| Frame an idea | `product/overview.md`, `product/requirements/README.md`, `decisions/README.md`, `architecture/ecosystem.md`, `notes.md`, `research/README.md` |
| Shape a bet | The framing note, the requirement files it touches, `architecture/contracts/`, `bets/README.md`, `notes.md` |
| Close a bet or audit | The bet file, the files it touches, the derived indexes |

`AGENTS.md` stays around 100 lines: a table of contents, never an encyclopedia. A file holds one concern that changes at one rate.
