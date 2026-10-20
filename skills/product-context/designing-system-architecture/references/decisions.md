# Decisions

A product built from a context repository keeps two decision logs. The context repository's `decisions/` records product and architecture decisions. The code repository's own log records implementation decisions, written by the implementation loop at its G2. This reference says which choice goes where, which decisions must precede code, and how the two logs stay linked.

## Contents

- The test
- Examples
- Decisions that precede code
- Writing a record
- Linking the two logs

## The test

A choice is **architecture**, and goes to the context repository's `decisions/`, when it changes:

- an element, boundary or technology that `architecture/` describes: a container, a store, a trust boundary, a runtime, a deployment target, a distribution channel;
- a contract under `architecture/contracts/`;
- a decision already recorded in the context repository.

A choice inside one element that no other bet consumes is **implementation**. The implementation loop settles it and records it in the code repository's log when it is consequential there. When a bet's work would need an architecture choice, the loop stops and returns it as a context change; this skill then makes the choice with the user.

A product choice, such as what a user can do or who may do it, is neither: it belongs to `curating-product-requirements`.

## Examples

Larder, a fictional pantry and meal-planning app:

| Choice | Log | Why |
|---|---|---|
| Sync by an append-only change log rather than whole-state replacement | Context | Shapes the sync service, the database and the sync protocol contract |
| The household is the access boundary: no data crosses households | Context | A trust boundary every container obeys |
| The sync service runs as one process per region | Context | A deployment element |
| The web app keeps an offline cache in the browser | Context | A store, listed in `data.md` |
| Field names inside a new sync message only one bet produces | Implementation, then written back | Declared "open" in the contract; settled at G2 and written into the contract at close |
| Which state-management library the web app uses internally | Implementation | Inside one container; no other bet consumes it |
| The table layout of the change log | Implementation | Inside the database's owning container, as long as the data view still holds |
| Retrying failed pushes with backoff in the web client | Implementation | Inside one container; the contract already says pushes are idempotent |
| Replacing the database engine | Context | A technology in `containers.md` |

When a choice sits on the line, ask whether a second bet would have to know about it. Yes: architecture. No: implementation.

## Decisions that precede code

Record these in the baseline, before any bet is ready, because undoing them after code exists is expensive:

- data ownership: which container owns which data, and what is the source of truth;
- trust and isolation boundaries: what may never cross between users, tenants, devices or environments;
- the protocols between containers, and their transport and authentication;
- the runtime or language per container, when a bet cannot reasonably choose it alone;
- the distribution channel and the platforms supported;
- the code repository layout: one repository or several, and which containers live where;
- any commitment with a recurring cost or an external party.

Other decisions are recorded when the choice is actually made, usually when a contract is written or a version is refreshed.

## Writing a record

When the `decision-records` skill is installed, use it. Otherwise follow the repository's existing convention, or this format:

- File `decisions/NNNN-kebab-title.md`, the next free four-digit number, never reused.
- `# NNNN: Title that states the decision`, then `- Status:` and `- Date:` lines.
- Sections Context, Options, Decision, Consequences; one page, two at most.
- A row in `decisions/README.md`: number linked to the file, title, status, one-line summary.

Record only decisions the user made or is making with you. A choice still open is a record with `Status: proposed`, or an open question in `roadmap/open-questions.md`. An accepted record is never edited: a new record supersedes it, and both link to each other.

Link each record from the architecture sections it shapes, and from the contracts it settles.

## Linking the two logs

The logs never merge, but the context side must see code-side records that moved the architecture.

- The implementation loop names the bet and its pinned commit in the Context section of every record it writes for a bet's work item.
- In as-built mode, find those records, apply the test, and for each one that moved the architecture: update the section, and link the record by repository name and path, as `larder: decisions/0012-batch-sync-writes.md`. Never write a local checkout path.
- A code-side record that should have been an architecture decision is a divergence: present it to the user, and when they accept it, write a context record that cites it.
