# Readiness and handoff

How a shaped bet becomes ready, how it is pinned and handed to the implementation loop, how it moves through its statuses, and how it is resumed after a reshape or dropped.

## Checking readiness

| Check | How |
|---|---|
| Requirements | Each ID in the Requirements table appears in `product/requirements/` with this milestone as its target Version and status `planned` |
| Acceptance criteria | Each criterion names a requirement of the bet, has a concrete pass condition, and can be observed without reading the code; each requirement has at least one |
| Contracts | Each consumed contract's header lists the version the bet names as `accepted`, as in `Version: 1.1 proposed · 1.0 accepted` for a bet that names 1.0; a produced or changed contract states what the bet fixes |
| Decisions | Each decision the bet relies on has status `accepted` in `decisions/README.md` |
| Dependencies | Each bet in Depends on has `Status: built` or `done`; a dependency still `in delivery` blocks readiness. `Bet 03` is the file `roadmap/v*/bets/03-*.md` |
| Design | A bet that changes a user interface links an agreed design handoff under `design/` |
| Open questions | No open question listed against the bet blocks it |
| Code repository | The Code repository line names a repository that exists, or the bet is the first in a new one, shaped L |
| Context repository | `git status --porcelain -- <every path the bet names>` prints nothing, and the repository has commits. The paths are the bet, the requirement files for its IDs, the contracts, the decisions and the context pack: the loop reads all of them at the pin |

Report every failed check with the skill or person that fixes it. Never make a bet ready by weakening a criterion or dropping a check.

## Pinning

The pin is the commit the implementation loop reads the bet at. The loop reads the bet's own fields at the pin: every header line except `Status:` and `Context pinned:`, and every section except Handoff and Outcome log. It reads the bookkeeping fields (Status, Context pinned, Handoff, Outcome log) at the latest commit, so writing them after the pin never looks like a change to the bet.

```bash
git -C <context repository> status --porcelain -- <every path the bet names>   # must print nothing
git -C <context repository> add <bet file>
git -C <context repository> commit -m "<the repository's convention for shaping bet NN>"
git -C <context repository> rev-parse HEAD        # the pin: the full SHA
```

Then write `Status: in delivery`, `Context pinned: <full sha>` and the Handoff section, and commit again.

## The Handoff section

```
## Handoff

- Date: 2026-10-20
- Code repository: larder
- Work item: 04-pantry-items
- Kickoff: Use running-implementation-loops on bet roadmap/v1/bets/04-pantry-items.md in <context repository checkout> at 1f3c9a2e5b7d4c6a8e0f2b4d6c8a0e2f4b6d8c0a as work item 04-pantry-items
```

The work-item slug is the bet's file name without its extension, so the loop's folder in the code repository and the bet share a name. The kickoff names the context repository checkout as the user has it locally; replace that placeholder only in the message to the user, never in a committed file.

## Statuses

| Status | Set by | When |
|---|---|---|
| `shaped` | `shaping-bets` | The bet file is written and the slate is agreed |
| `ready` | `shaping-bets` | Every readiness check holds |
| `in delivery` | `shaping-bets` | At handoff, with the pin and the Handoff section |
| `built` | `reconciling-product-context` | Every criterion was observed on merged code, or cut in the user's words |
| `done` | `reconciling-product-context` | The context repository has been reconciled with what was built |
| `dropped` | `shaping-bets` for a bet never handed off; `reconciling-product-context` for a bet `in delivery` | The user decided not to build it; the reason is recorded |

Only the bet file's Status line is authoritative. The bet board copies it.

## Dropping

A bet that was never handed off (`shaped` or `ready`) is dropped here: set `Status: dropped`, add a dated line to the Handoff section with the reason and the user's words, rebuild the bet board, and commit when the user asks. Its requirements stay `planned`, free for another bet. Its number is never reused.

A bet `in delivery` has work in a code repository, merged or not. Hand it to `reconciling-product-context` when it is installed: it closes the bet as dropped and writes the outcome log from what merged. Without it, set the status as above and list in the Handoff section what merged in the code repository, by pull request.

## Resuming after a reshape

The implementation loop keeps working on everything that does not depend on the reshape, and starts no new slice of the bet. After the reshape:

1. Commit the reshaped bet, checking the same paths as at handoff. Take the new pin.
2. Update Context pinned. Add a dated line to the Handoff section: what changed, and the user's words when the appetite was raised. Next to it, write a new Kickoff line with the new SHA; the first one stays as history.
3. Give the user that kickoff line: the same format and work-item slug as the first, with the new SHA. The loop treats a kickoff for an existing work item with a new SHA as the user's re-pin, and reopens its spec only for the lines that changed.

Raising the appetite is a reshape. Edit the bet's `Appetite:` line, which is one of the bet's own fields, so the loop sees the new value at the new pin; the dated Handoff line records the user's words. An appetite extension the user gives inside the loop instead is recorded in the work item's `roadmap.md` Decisions in the code repository and leaves the bet file unchanged; `reconciling-product-context` reports it in the outcome log.

```
## Handoff

- Date: 2026-10-20
- Code repository: larder
- Work item: 04-pantry-items
- Kickoff: Use running-implementation-loops on bet roadmap/v1/bets/04-pantry-items.md in <context repository checkout> at 1f3c9a2e5b7d4c6a8e0f2b4d6c8a0e2f4b6d8c0a as work item 04-pantry-items
- 2026-10-27: appetite raised from M to L: "take the extra plan, the offline cache is worth it"
- Kickoff: Use running-implementation-loops on bet roadmap/v1/bets/04-pantry-items.md in <context repository checkout> at 7d2e4f6a8c0b1d3e5f7a9c1e3b5d7f9a1c3e5b7d as work item 04-pantry-items
```

## Agents without the context repository

Render the bet with the kickoff template. Paste the bet's own fields as they read at the pinned commit, and fill the bookkeeping fields with their values at the latest commit: `Status: in delivery`, `Context pinned: <full sha>`, and the Handoff's code repository and work item. Then paste each context pack file, and the requirement text, contracts and decisions the bet names, at the pinned commit, in order. The implementation loop records that the content was pasted rather than read at the pin, and reports drift as not checked.
