# Architecture lens

Judge whether the change fits the system it lands in: the approach the user chose, the module boundaries, the building blocks that already exist, and who owns each piece of data. Line-level correctness belongs to other lenses.

## Read first

1. The spec's Approach section: the chosen approach and the alternatives it rejected. Outside the loop there is no Approach; judge fit against the decision records and the existing code.
2. The architecture notes in AGENTS.md, CLAUDE.md or the docs, and the decision records (`decisions/`, `docs/adr/` or the project's equivalent).
3. The neighborhood of each changed file: its module, what it imports, and who calls it.
4. The utilities, components and patterns near the change. Search by name and by behavior, meaning the calls such a helper would make, before you call anything a duplicate.

## Check

1. **The chosen approach.** The diff implements the Approach the user picked, not a rejected alternative or an unannounced third one. A deviation the PR does not explain is a finding. An explained deviation that changes behavior or scope is an escalation: the chosen approach proved infeasible, and the user decides.
2. **Boundaries and layering.** Each piece of code sits in the layer that owns its concern. No call skips a layer the project routes through, such as a handler querying the database directly when every other handler goes through a repository or store. Dependencies point the same way as the project's existing ones, and the change adds no import cycle.
3. **Reuse.** The change uses the project's existing utilities, components and patterns instead of re-implementing them: validation, HTTP clients, error types, date handling, configuration access, UI primitives. Name the existing one by path.
4. **One source of truth.** A fact the system must agree on (a price, a permission list, an enum, a schema, a configuration value, derived state) is defined once. Every copy is derived from the owner or kept in sync by one mechanism. Client state that mirrors server state has an invalidation path.
5. **Data flow and ownership.** One owner creates, changes and deletes each piece of data. Side effects happen in the layer where the project puts them. Every resource the change creates has a lifecycle: something closes, cleans up or expires it.
6. **Coupling and altitude.** A new abstraction has two real callers or a stated reason. No speculative generality: an interface with one implementation and no second one planned, configuration for a value that never changes, a framework for a one-off. The opposite also counts: a third copy of a block the project already abstracts. Public surfaces export only what callers need.
7. **Contracts and compatibility.** Changes to public APIs, events, file formats, schemas, CLI flags and stored data are backward compatible, versioned, or allowed by the spec. A migration survives old and new code running side by side during a deploy (expand, migrate, then contract) and has a rollback.
8. **Error boundaries.** Errors are translated where the project translates them, for example domain errors mapped to HTTP responses in the transport layer and not deep inside the domain.

## Leave to other lenses

- Every authentication, authorization and trust-boundary question, including where a check is placed: security.
- Written style rules, naming, formatting and local idioms: conventions. Written layering and module-boundary rules stay here.
- Runtime cost, even when the structure causes it: efficiency.
- Whether the behavior meets the acceptance criteria, edge cases and tests: intent.

## Evidence bar

- Point to the changed line (file and line at the head SHA) and to what it conflicts with: the existing utility by path, the sentence in the Approach, the decision record, the written rule, or the other definition of the same fact.
- For this lens the trigger is a failure scenario: the change or event that makes the structure fail. For example, "when the price changes in `config/prices.ts`, the copy in `checkout/constants.ts` keeps the old value and checkout charges it."
- State the concrete cost: what breaks, what drifts, or what has to change in two places. "Could be cleaner" is not a finding.
- When the fit depends on intent you cannot see, mark the finding `unconfirmed` and ask.

## Severity

| Severity | Architecture examples |
|---|---|
| `blocking` | Implements a rejected or unapproved approach without explanation. Creates a second source of truth for data that must agree. Breaks a public contract the spec does not allow to break. Ships a migration that breaks the running version during a deploy. |
| `should-fix` | Duplicates an existing utility. Bypasses an established layer or pattern. Couples modules that were independent. Adds an abstraction with one caller and no reason. |
| `nit` | A placement that works but differs from where neighboring code puts similar things. |

A confirmed defect in changed code is never a nit.

## Output

Return one block per finding, most severe first:

```text
lens: architecture
file: <path>
line: <line at the head SHA>
severity: blocking | should-fix | nit
status: confirmed | unconfirmed
summary: <one sentence: what is wrong>
trigger: <the failure scenario; expected versus actual>
impact: <who or what is hurt, and how badly>
evidence: <quoted code, a command and its output, or the reproduction>
basis: <the Approach sentence, decision record, rule, or existing code it conflicts with>
direction: <a suggested fix, without an unrelated refactor>
```

After the blocks, add one line: `Checked: <what you examined>`.

When the diff does not touch this lens's concerns, answer only `architecture: nothing in scope (<reason>)`. When you checked and found nothing, answer only `architecture: no findings. Checked: <what you examined>`.
