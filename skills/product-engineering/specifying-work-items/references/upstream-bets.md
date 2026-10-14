# Upstream bets

How to turn a bet from a product context repository into `spec.md`: read it at its pinned commit, import it into the spec's existing headings without changing a word of what was agreed upstream, and interview only what it leaves open.

A bet is a shaped unit of work with a fixed appetite. It holds an outcome, catalogue requirement IDs, acceptance criteria, boundaries, the contracts and decisions it relies on, and an ordered context pack. Recognize it by its fields: an H1 that starts `# Bet NN:`, a `Status:` line, an `Appetite:` line, and a `## Acceptance criteria` section.

## Read at the pin

The bet names the commit it was handed over at on its `Context pinned:` line. Read the bet and everything it names at that commit, and never write to the context repository: no edits, commits, fetches or checkouts there.

```bash
git -C <ctx> show <sha>:<bet path>
git -C <ctx> grep -n -e 'ABC-01' <sha>
git -C <ctx> show <sha>:<contract or decision path>
```

Read the bet's bookkeeping fields (Status, Context pinned, Handoff, Outcome log) at the latest commit instead; the context side writes them after the pin. When the Handoff names a work-item slug, use it for the spec's folder. When `running-implementation-loops` is coordinating, it has already run the intake checks; when this skill runs alone, check at least that the pinned commit exists in the checkout and that the bet names this repository, and ask when either fails.

## Import table

Every heading of the spec template stays, in its order. Everything the bet holds goes under one of them.

| Bet | `spec.md` |
|---|---|
| Path and pin | `Source: bet <path in the context repository> @ <full sha> in <context repository name> (read-only)`, plus "pinned by the loop at intake" or "pasted, not checked against the pin" when either applies |
| Track | `feature`, or `new app` when there is no codebase |
| Outcome | Problem: the outcome quoted, then what happens today, from the code |
| Requirements | Requirements: one line per ID with the catalogue's text verbatim, read at the pin, the coverage and the bet's note: `- ABC-01: <text> (bet: all)` or `(bet: part: …; note: …)`. No other requirements |
| Acceptance criteria | Acceptance criteria: verbatim, with their IDs and `~` marks |
| No-gos | Non-goals: `- No-go (bet): …` |
| Rabbit holes | Constraints: `- Rabbit hole (bet): …`, with its "Patched by:" or "If it bites:" text verbatim; one without a patch is also listed under Assumptions and open questions |
| `~ Cuttable` items | Constraints: `- ~ Cuttable (bet): …` |
| Appetite | Constraints: `- Appetite (bet): M, at most one plan, Plan 0 not counted. Exceeding it stops the loop; only the user's words extend it.` For L: two or three plans |
| Touches | Constraints: `- Touches (bet): …` |
| Consumed contracts | Constraints: `- Contract consumed (bet): <path> version X.Y @ <short sha>`, with the clauses this work relies on quoted |
| Produced or changed contracts | Constraints: `- Contract produced (bet): <path>: <what the bet fixes>`; the details it leaves open are settled at G2 |
| Relied-on decisions | Constraints: `- Context decision (bet): <path> @ <short sha>: <one line>` |
| Risks and open questions | Assumptions and open questions: each register ID with its line; a product question is owned by the context side and decided by the user |
| Context pack | Constraints: `- Context pack (bet), in order: …` |
| Depends on | Assumptions: each dependency's status, and where it was read |
| Version, Milestone, Status, Context pinned, Handoff, Outcome log | Not imported |

Three marks may be appended to imported lines, each with the date and the user's words; none replaces the line:

- `cut (YYYY-MM-DD: "<user's words>")` on a `~` criterion or a `~ Cuttable (bet)` line. The cut criterion's Verification row and its phase are removed in the same change.
- `extended (YYYY-MM-DD: "<user's words>"): L` on the Appetite line. The latest mark sets the appetite.
- `re-pinned from <old short sha> (YYYY-MM-DD: "<user's words>")` on the Source line, whose SHA is updated.

When a roadmap exists, each mark also gets a dated entry in its Decisions; G4 copies the marks made before it.

The Done and review line under Constraints is still asked and filled as on any work item.

## Interview what the bet leaves open

- Never re-ask behavior the bet fixes. Ground yourself in the code as on any work item, and ask only engineering unknowns and detail the bet leaves open: error wording, limits it does not state, edge cases inside its requirements.
- A decision inside the bet's boundaries becomes an engineering criterion in its own series, after the imported ones: `AC-E1 (ABC-01): …`. It never changes an imported line.
- An engineering need with no requirement of its own, such as a performance limit the user wants checked, becomes an `AC-E` on the closest imported requirement, or a constraint. Never add a requirement.
- A context change is anything that would add a requirement, change an imported line, cross a no-go, or change a contract or a context decision. Record it under Assumptions and open questions as `Open: … Blocks: … Owner: the context side`, and stop: it goes to the user, who reshapes the bet upstream.
- An imported criterion that cannot be observed as written is flagged for G3, which settles it without rewording. A requirement with no criterion gets an `AC-E` that restates it observably, confirmed at G1, or it is a context change.

## The G1 summary

Add to the usual summary: the imported counts (requirements, partial coverages, criteria, cuttable criteria), the engineering additions (`AC-E` criteria and constraints), and any context change raised. The status line format does not change: `Status: agreed (G1, YYYY-MM-DD: "<user's words>")`.

## Reopen

Imported lines change only with a new pin: the user reshapes the bet upstream, and G1 reopens for the lines that changed. Here, only the three marks above are appended, each in the user's words. A cut, when the appetite runs short:

```
- ~ AC4 (ABC-02): Items expiring within three days are listed first. cut (2026-10-20: "cut the sorting, ship without it")
```

A cut criterion loses its Verification row and its phase in the same change, and the hand-back reports it.
