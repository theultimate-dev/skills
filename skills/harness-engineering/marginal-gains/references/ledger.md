# Ledger

The ledger is what makes the gains compound. Without it every run starts from zero: it cannot check whether a change worked, it re-proposes what the user declined, and it never sees friction that recurs across sessions.

## Location

- One ledger per person, across projects and harnesses.
- At user level, outside any repository. It quotes sessions from every project, and inside a public repository it would publish them.
- Found through one pointer line in each user-level instruction file the user's harnesses read, for example `Marginal gains ledger: <path>. Read it only when running marginal-gains.` The second sentence keeps agents from loading it into every session.
- When the user moves it, update every pointer line in the same edit.

## Shape

Start from `templates/ledger.md`. Four sections, in this order:

1. **Goals.** The user's goals in priority order. Only the user changes them; propose an edit when the session suggests one.
2. **Watchlist.** Friction and wins seen but not yet worth a card, one line each: the count of sessions it appeared in, the root cause, the dates first and last seen, and one pointer.
3. **Runs.** One section per run, newest first, headed with the date, the project, and the session in a few words, then a table of that run's cards: ID, suggestion, where, evidence with its session count, score, effort, status, check, and outcome.
4. **Folded.** One line per suggestion from runs folded out of the Runs section.

## IDs

`G` followed by a number: G1, G2, and on. The next ID is one more than the highest in the file, including the folded section. IDs are never reused, so the user can say "apply G14" at any time.

## Status

| Status | Means | Next run |
|---|---|---|
| `proposed` | Delivered, no answer yet | Name it in the opening line as unanswered, then set it to `deferred` |
| `applied` | The change is in the harness | Grade it while its outcome is `open` or `held` |
| `declined: <reason>` | The user said no; the reason when one was given | Stays out; returns only with evidence its decline reason did not cover |
| `deferred` | Not now | Re-enters the candidates when the session shows its friction again, with its count raised |

## Outcome

| Outcome | Means |
|---|---|
| `—` | Not applied, so nothing to observe |
| `open` | Applied, not yet observed; set when the change is applied |
| `held YYYY-MM-DD` | The check passed in that session |
| `settled` | Held in two sessions; no longer checked |
| `slipped YYYY-MM-DD → Gn` or `→ watchlist` | The friction came back; Gn is the escalated card, or the escalation waits on the watchlist |

## Upkeep

- Write the run before the reply is sent, and update statuses when the user answers. Grading results and watchlist counts go in the same edit.
- A watchlist count goes up by one per session the item appears in, however many times it appeared. An item that becomes a card leaves the watchlist; the card's evidence keeps its count.
- Past runs keep their evidence as written. Only status and outcome change.
- With more than twenty runs, fold the oldest run once none of its cards is still being checked or deferred: one line per suggestion, such as `G3 settled: <title>`, `G5 declined: <title> (<reason>)`, `G6 slipped → G9: <title>`. Remove watchlist items not seen in the last twenty runs.
- No secrets, credentials, personal data, or client material. Paraphrase anything sensitive in a pointer.
