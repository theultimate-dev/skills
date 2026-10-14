# Layers and house rules

The shape of a product context repository: what each directory holds, how often it changes, which IDs and statuses it uses, and the rules that keep it coherent. `AGENTS.md` in the repository carries a short copy of the house rules; this file is the full version.

The examples use a fictional product, Larder: a household pantry and meal-planning app with a web app and a sync service, kept in `larder-context` next to its code repository `larder`.

## The layers

Directories are sorted by how often their content changes. Slow layers never depend on fast ones.

| Directory | Holds | Changes | Written by |
|---|---|---|---|
| `AGENTS.md`, `README.md` | The map for agents (reading order per task, house rules) and the introduction for people | When the structure changes | `structuring-product-context` |
| `product/` | Why and what: overview, glossary, actors and use cases, the requirement catalogue, non-functional requirements; optionally platforms and business | Rarely; a new requirement, a retarget, a status after a bet closes | `curating-product-requirements`; target versions by `planning-product-roadmaps`; `built` statuses by `reconciling-product-context` |
| `architecture/` | How it is structured: C4 views, components, domain model, data, deployment, build and release, cross-cutting concepts, runtime scenarios, contracts, external dependencies | At the baseline, at each version boundary, when a contract is added, when a bet closes | `designing-system-architecture` |
| `decisions/` | Product and architecture decision records, with an index | Append-only: one record per consequential choice | `decision-records`, called by the other skills |
| `roadmap/` | When and in what order: versions, gates, version briefs, milestones, bets, the risk and open-question registers | Often: every shaping, handoff and close | `planning-product-roadmaps`, `shaping-bets` |
| `design/<initiative>/` | Product and design work for one initiative: briefs, UX flows, visual directions, prototypes | Per initiative | the `product-design` skills |
| `research/` | Dated evidence: comparisons, spikes, name checks, interview notes, source lists | Append-only | anyone |

```
<product>-context/
├── AGENTS.md                     map, reading order per task, house rules (about 100 lines)
├── CLAUDE.md                     one line, @AGENTS.md, when Claude Code is in use
├── README.md                     for people: what the product is, where to start
├── product/
│   ├── overview.md               vision, principles, assumptions and constraints
│   ├── glossary.md               the product's ubiquitous language
│   ├── actors-and-use-cases.md
│   ├── platforms.md              optional: what each surface does
│   ├── business.md               optional: ownership, licence, costs, pricing
│   └── requirements/
│       ├── README.md             ID scheme, statuses, counts (derived)
│       ├── <capability>.md       one file per capability, e.g. pantry.md for PAN-…
│       ├── non-functional.md     NFR-…
│       └── id-map.md             local IDs from briefs and handoffs mapped to catalogue IDs (append-only)
├── architecture/
│   ├── README.md                 the arc42 checklist mapped to files, the status legend
│   ├── context.md                C4 level 1
│   ├── containers.md             C4 level 2
│   ├── components/               C4 level 3, one file per container where it pays
│   ├── domain-model.md
│   ├── data.md
│   ├── deployment.md
│   ├── build-and-release.md
│   ├── concepts/                 cross-cutting rules: security boundaries, error handling, consistency
│   ├── runtime/                  key scenarios: flows, sequences, state machines
│   ├── contracts/                interfaces several bets share
│   └── ecosystem.md              external dependencies with versions and verified-on dates
├── decisions/
│   ├── README.md                 index
│   └── 0001-record-decisions.md …
├── roadmap/
│   ├── README.md                 versions, gates between them, current focus, parked ideas
│   ├── risks.md                  RSK-…
│   ├── open-questions.md         OQ-…
│   └── v1/
│       ├── README.md             version brief
│       └── bets/
│           ├── README.md         bet board (derived)
│           └── 01-<slug>.md …
├── design/<initiative>/
└── research/YYYY-MM-DD-<topic>.md
```

Omit what a product does not need: a single-container product has no `components/`, a product without a business side has no `business.md`. Keep the directory names; agents rely on them.

## House rules

1. **One home per fact.** Every fact lives in exactly one file. Everywhere else links to it by path or ID.
2. **Volatile links to stable, never the reverse.** A bet links to requirements, architecture and decisions; a requirement never links to a bet; architecture never links to the roadmap. Two exceptions: a derived index, and a plain-text ID that records provenance in a notes cell or a history line, such as `OQ-06` or `settled in Bet 05`, which is never a link.
3. **IDs are permanent.** Never reuse or renumber an ID. A requirement that no longer applies stays in its table with status `dropped` and a reason.
4. **Indexes are derived.** Folder READMEs, the bet board, coverage tables and counts are rebuilt from the files they index, by the skill that changed those files or by `reconciling-product-context`. Never edit them by hand.
5. **Decisions are superseded, never edited.** An accepted record's decision text never changes; a new record supersedes it.
6. **Research is evidence, not truth.** A research note records what was found on a date. A current fact belongs in its layer, citing the note.
7. **Point at the code, never copy it.** Describe structure, contracts and rules; leave file layouts and code to the code repository.
8. **Markdown only,** except prototypes under `design/<initiative>/`, which may be offline HTML.
9. **The context repository is read-only from code repositories.** Agents in a code repository read it at a pinned commit and never write there. Changes come back through reconciliation.

## IDs

| Thing | Format | Example | Notes |
|---|---|---|---|
| Functional requirement | `<CAP>-NN`, a 2–4 letter capability prefix | `PAN-03` | One prefix per capability file; numbers continue after the highest ever used |
| Non-functional requirement | `NFR-NN` | `NFR-07` | |
| Use case | `UC-NN` | `UC-02` | Actors are named, not numbered |
| Risk | `RSK-NN` | `RSK-04` | In `roadmap/risks.md` |
| Open question | `OQ-NN` | `OQ-11` | In `roadmap/open-questions.md`; a resolved question links to its decision |
| Decision record | `NNNN` | `0007` | Four digits, per `decision-records`. A code repository's record is cited as `<repository>: decisions/NNNN-title.md` |
| Bet | `NN`, numbered across all versions | `Bet 14` in `roadmap/v2/bets/14-shared-lists.md` | Never reused, even for a dropped bet; `Depends on: Bet 03` names the file `roadmap/v*/bets/03-*.md` |
| Acceptance criterion | `ACn (<requirement ID>)` | `AC3 (PAN-03)` | Numbered within one bet |
| Engineering criterion | `AC-En (<requirement ID>)` | `AC-E1 (PAN-03)` | Added by the code repository at its G1, inside the bet's boundaries; promoted at close when worth keeping |
| Contract | file slug plus a major.minor version | `contracts/sync-protocol.md`, `Version: 1.1 proposed · 1.0 accepted` | A compatible change raises the minor version, an incompatible one the major version; each live version shows its own status |

## Statuses

| Thing | Statuses | Where |
|---|---|---|
| Requirement | `planned`, `built`, `deferred`, `dropped` | A Status column in the capability file, next to its target Version: a version such as `V1` until a milestone is chosen, then a milestone such as `V1.2`; a `deferred` requirement has none |
| Architecture section | `Since: Vn · Status: planned` or `built`; `Status: retired in Vn, replaced by …`; optionally `Changed in: Vn (…)` | One line under the section heading; an untagged section reads as unverified |
| Contract | `proposed`, `accepted`, `superseded`, per version | The contract's header, newest version first; a bet consumes only a version that is `accepted` |
| Decision record | `proposed`, `accepted`, `deprecated`, `superseded` | Per `decision-records` |
| Version | `planned`, `in progress`, `shipped` | `roadmap/README.md` |
| Milestone | `planned`, `in progress`, `exited` with the date and the user's words | The version brief |
| Bet | `shaped`, `ready`, `in delivery`, `built`, `done`, `dropped` | The bet file's `Status:` line, the only authoritative place |
| Risk | `open`, `closed` | `roadmap/risks.md` |
| Open question | `open`, `resolved` with a link to the answer | `roadmap/open-questions.md` |

A bet is `built` when every acceptance criterion was observed on merged code, and `done` when the context repository has been reconciled with what was built. Live pull request state is never written into the context repository; it stays on the code host.

## Reading order by task

`AGENTS.md` gives agents the shortest path for each kind of task:

| Task | Read |
|---|---|
| Build a bet | The bet file, then its Context pack, in order |
| Change or add requirements | `product/overview.md`, `product/glossary.md`, `product/requirements/README.md`, the capability file |
| Change the architecture | `architecture/README.md`, the affected views, `decisions/README.md` |
| Plan or check the roadmap | `roadmap/README.md`, the version brief, the bet board, the registers |
| Shape bets | The version brief, the requirement files for the milestone, `architecture/contracts/`, the bet board |
| Close a bet or audit | The bet file and the files it touches, the derived indexes |

## Sizes

- `AGENTS.md` stays around 100 lines: a table of contents, never an encyclopedia.
- A file holds one concern that changes at one rate. Split a file when it mixes rates of change, such as rationale inside a requirement table; do not split by length alone.
- A bet file stays readable in one sitting, about two pages.
