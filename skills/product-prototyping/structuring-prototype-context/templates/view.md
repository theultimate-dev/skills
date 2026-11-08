# [View, concept or scenario name]

Status: [built | planned]

<!-- One concern per file: a C4 view (context, containers, one container's components), a cross-cutting concept, or one topic's runtime scenarios.
Status is built, or planned while the open bet that introduces the element is not closed. A kept bet turns it into built; a removed bet deletes it. There are no version tags.
Paths are relative to the context folder, as backticked text. Never describe classes, files or functions; point at the code instead.
When sections arrive with different bets, give each section its own Status line and drop the one above. Delete this comment. -->

[Two or three sentences: what this file shows and why it matters. Name the requirement IDs it serves.]

```mermaid
flowchart TB
  a["<b>[Element]</b><br/>[responsibility in a few words]"]
  b["<b>[Element]</b><br/>[responsibility]"]
  a -->|"[protocol or message family]"| b
```

[One or two sentences for what the diagram cannot show: the riskiest arrow, what never talks to what.]

## Elements

| Element | Responsibility | Technology | Status |
|---|---|---|---|
| [name] | [one line] | [runtime, store or protocol] | [built] |

## Rules

<!-- For a concept: the rules every element obeys, one per line, each with the NFR IDs it serves. For a view: the constraints that hold across its elements. -->

- [Rule]. Serves: [NFR-NN].

## Related

- Contracts: [`architecture/contracts/name.md`, version X.Y | none]
- Decisions: [`decisions/NNNN-title.md`, … | none]
