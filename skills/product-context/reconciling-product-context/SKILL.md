---
name: reconciling-product-context
description: "Folds delivered work back into a product context repository and keeps it coherent. Closes a bet after its pull requests merge: confirms every acceptance criterion was observed on merged code, updates requirement statuses and the architecture as built, writes contract details settled during implementation into the contracts, links implementation decision records that moved the architecture, updates risks and open questions, writes the bet's outcome log, and rewrites the derived indexes. Also audits for drift: broken links, duplicate or reused IDs, requirements owned by no bet or by two, stale indexes and verified-on dates, facts kept in two places, stable files linking to volatile ones. Use when the user says bet N is merged, close bet N, drop bet N while it is in delivery, sync the docs with what we built, or audit the docs. Not for verifying or reviewing code (verifying-implementation, reviewing-code-changes)."
license: MIT
---

# Reconciling product context

A product context repository stays true only if every delivered bet folds back into it. This skill closes bets and audits for drift. It reads what was built from the code repository and its host, and writes only to the context repository. A bet is `built` when every acceptance criterion was observed on merged code, and `done` when the context repository says what was built.

The repository's shape, IDs and statuses are in its `AGENTS.md`. The examples use a fictional product, Larder, whose context lives in `larder-context` and whose code lives in `larder`.

## Two modes

| Mode | Triggers | Ends with |
|---|---|---|
| Close a bet | "Bet 07 is merged", "close bet 07", "drop bet 07" for a bet `in delivery`, the implementation loop's hand-back pasted in | The bet `done` or `dropped` with its outcome log, or a `built`, `partial` or `stopped` result with what is missing |
| Audit | "Audit the docs", "sync the docs with what we built", before a version boundary | An audit report: mechanical fixes made, substantive findings for the user |

## Close a bet

### 1. Find the bet and its work item

Read the bet file. Its status should be `in delivery`; a bet never handed off (`shaped` or `ready`) is dropped by `shaping-bets`, not here. The pin is on the bet's `Context pinned:` line, and its `## Handoff` names the code repository and the work-item slug. Locate the code repository checkout: the path the user gives, or the sibling the handoff names. Ask once when neither resolves.

Find the work item's `spec.md`, at `docs/product-engineering/<work-item-slug>/` unless the code repository keeps specs elsewhere. Confirm that its `Source:` line names this bet and this context repository. A different pin is fine when the Source line carries a `re-pinned from` mark, the roadmap's Decisions record a re-pin, or a later Kickoff line in the bet's Handoff names it.

A bet with no Handoff was pinned by the loop, or pasted into an issue. Take the pin from the spec's `Source:` line, which then ends in one of two ways:

- "pinned by the loop at intake": the loop pinned the context repository's HEAD itself; drift was checked against that commit.
- "pasted, not checked against the pin": the bet arrived pasted; nobody checked drift. Compare the bet's own fields at that commit with the latest commit, and report any difference in the outcome log.

Any other mismatch between the bet and the spec: stop and ask.

### 2. Gather the evidence, read-only

The code repository is read-only for this skill, exactly as the context repository is for the implementation loop: never write, commit, stash, fetch, pull or check out there. Read from the base branch with `git show <base>:<path>`. When the local base is behind the merges, read through the host's CLI or ask the user to update the checkout.

| Source | Gives |
|---|---|
| `spec.md` | The pin, the imported requirements and criteria, engineering criteria `AC-E1 (PAN-03)` added at its G1, and the marks appended to imported lines, each in the user's words: `cut (YYYY-MM-DD: "<user's words>")` on `~` items, `extended (…): L` on the Appetite line, `re-pinned from <sha> (…)` on the Source line. The marks are authoritative |
| `roadmap.md` | The `Appetite (bet):` line, and in Decisions: re-pins, cuts made after G4, appetite extensions and the outcomes of context escalations, each quoting the user. An extension given inside the loop is an `extended` mark in `spec.md`, mirrored here once a roadmap exists, and leaves the bet file unchanged; report it in the outcome log |
| `plans/NN-slug.md` | `Branch:` lines, Notes, Changes after launch, the plan's `Status:` |
| The code repository's decision log | Implementation decision records that name the bet |
| Pull requests on the host, found by branch | Merge state, merge commit, and the `## Verification` report: each criterion's result on a stated commit |
| The loop's hand-back, when pasted | A convenience. Where it disagrees with the sources above, they win |

Never invent evidence. A source you could not read is named in the outcome log as not checked. [Closing a bet](references/closing-a-bet.md) has the commands, how to match verification rows to merged heads, and how to treat carried-forward, human-eye and flaky rows.

### 3. Decide the result

The result uses the loop's hand-back words.

| Result | When | Status written |
|---|---|---|
| `built` | Every bet criterion and every `AC-E` passed on a merged head, or was cut with the user's words | `done` once step 5 completes; `built` while a context change still waits for the user |
| `partial` | Some criteria are not observed or some slices are unmerged, and the loop has not stopped | Unchanged. Report what is missing and close again when it lands |
| `stopped` | The circuit breaker fired and the bet waits for a reshape | Unchanged. Hand it to `shaping-bets` when it is installed |
| `dropped` | The user dropped the bet while it was in delivery, in their words | `dropped`, with the reason and the date |

A criterion that is neither observed nor cut keeps the bet from `built`. List it with what would close it. Never mark it passed because the code looks complete.

### 4. Show what changes

Present a short close summary before writing: the result, the criteria table, and every proposed change to the context repository. Mechanical updates go ahead without asking: statuses that follow from the evidence, the outcome log, derived indexes and links. Ask before anything that changes meaning: a requirement's wording, a promoted rule, an architecture divergence, a contract change, a new decision record. Record the user's answer in the outcome log.

### 5. Reconcile each layer

| Layer | Update |
|---|---|
| Requirements | `planned` becomes `built` when the last part lands. A requirement covered as `part:` stays `planned` until every bet covering it is built. A cut that leaves part of a requirement undelivered keeps it `planned`, with a note naming the cut |
| Catalogue rules | Promote durable behaviour the bet settled, including `AC-E` rules worth keeping, into the requirement text or a new requirement, with `curating-product-requirements` when it is installed |
| Architecture | Every section the bet touches moves from `planned` to `built`. Divergences become as-built text that names the code-repository record behind them, with `designing-system-architecture` in as-built mode when it is installed |
| Contracts | Details the bet left open and the code repository settled at its G2 are written into `architecture/contracts/`. The version is raised when the shape changed |
| Decisions | Link code-repository records that moved the architecture by repository name and path, such as `larder: decisions/0004-batch-sync-writes.md`, never a local checkout path. A code-side record that made an architecture-level choice gets a context record that adopts it, with `decision-records` and the user's agreement |
| Registers | Close retired risks, reword changed ones, add the ones failed approaches revealed. Mark answered questions `resolved` with a link |
| Glossary | Add terms the bet introduced |
| Bet | Fill `## Outcome log` from the [outcome log template](templates/outcome-log.md) and set `Status:` |
| Derived indexes | Rewrite the bet board, the version brief's coverage, the requirement counts and folder READMEs. Never mark a milestone exited: that is the user's judgment |

### 6. Close a dropped or stopped bet

A bet dropped while `in delivery` closes here. Its outcome log records what merged and what did not. Requirements whose criteria all passed on merged code become `built`. The rest return to `planned`, or `deferred` when the user says so. Bet numbers are never reused. A bet that was never handed off is dropped by `shaping-bets` and has no outcome log. A `stopped` bet, waiting to be reshaped, is not closed: hand it to `shaping-bets` when it is installed.

### 7. Report

Report the bet's result and status, the files changed, the questions still open with what each blocks, and the next step: the next bet on the board, a reshape, or the milestone exit check with `planning-product-roadmaps`. Leave committing to the user unless the project instructions or the user say otherwise; one close is one commit.

## Audit

Run the checks in [drift audit](references/drift-audit.md) over the whole repository, or over the paths the user names:

- Links: broken relative links.
- IDs: duplicate or reused.
- Ownership: requirements of a milestone owned by no bet, or by two.
- Indexes: derived indexes that disagree with their sources.
- Freshness: stale verified-on dates in `architecture/ecosystem.md`, and bets `in delivery` with no activity on the host.
- Placement: facts kept in two places, and stable files linking to volatile ones.
- Contracts: a contract version consumed by a `ready` or `in delivery` bet that is not `accepted`.

Fix mechanical findings in place: indexes, unambiguous links, counts. Ask about every substantive one. Report with the [audit report template](templates/audit-report.md), ranked by severity, with every check that could not run named as not checked.

## When a sibling skill is missing

Say in one line which skill is missing, then produce its essential outcome yourself.

| Skill | Essential outcome |
|---|---|
| `designing-system-architecture` | Flip the touched sections to `built`; rewrite a diverged section as built, citing the code-repository record |
| `curating-product-requirements` | Edit the requirement row in its capability file; never reuse an ID; confirm the wording with the user |
| `decision-records` | A short record in the repository's `decisions/` convention: status, date, context, options, decision, consequences, plus its index row |
| `shaping-bets` | For a stopped bet, list what is left, the cut options and the reshape question, and leave the bet `in delivery` |

Without file access, return the outcome log, the changed rows and the audit report as Markdown, and say that nothing was written.

## References

| Read | When |
|---|---|
| [closing a bet](references/closing-a-bet.md) | Reading the code repository and host, matching verification rows to merged heads, deciding built, reconciling each layer, a worked close |
| [drift audit](references/drift-audit.md) | Running the audit: each check, how to run it, severity and fix |
| [outcome log template](templates/outcome-log.md) | Writing the bet's `## Outcome log` |
| [audit report template](templates/audit-report.md) | Reporting an audit |
