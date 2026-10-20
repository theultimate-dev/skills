# Drift audit

A context repository drifts quietly: a link breaks in a rename, an index stops matching its files, a fact gets copied into a second place and only one copy is updated. The audit finds this before an agent reads a stale fact and builds on it.

Run it on request, before a version boundary, and after a large restructure. It is read-only until the report: mechanical fixes are made after the report is assembled, and substantive findings wait for the user.

## Severity

| Severity | Meaning |
|---|---|
| Blocking | An agent building or shaping a bet would read something wrong or nothing at all: a broken link in a context pack, a reused ID, a consumed contract that is not accepted |
| Should fix | The repository contradicts itself: an index disagrees with its files, a requirement is owned twice, a fact lives in two places |
| Note | Worth a look, not yet harmful: an aging verified-on date, a quiet bet in delivery |

## Checks

| # | Check | How | Severity | Fix |
|---|---|---|---|---|
| 1 | Broken relative links | Resolve every relative Markdown link outside code fences against its file's directory, the fragment dropped, then check the fragment against the target's headings | Blocking inside a context pack or AGENTS.md; otherwise should fix | Mechanical when the target was renamed and exactly one file matches; otherwise ask |
| 2 | Duplicate or reused IDs | Collect every requirement, NFR, use-case, risk, open-question, bet and decision ID with its file. An ID defined twice is a duplicate. A `dropped` ID whose number was given to something new is reused | Blocking | Ask. Never renumber an ID a bet, a code repository or a record already cites; give the newer item the next free number |
| 3 | Requirement ownership | For each milestone, list its requirements (Version column) and the bets covering them (`## Requirements`, `Covered:`). Each requirement or part must be owned exactly once by a bet that is not `dropped` | Should fix; blocking for a bet about to be handed off | Ask; `shaping-bets` resolves it |
| 4 | Derived indexes | Rebuild each index from its sources and compare: folder READMEs, the bet board (status, appetite, dependencies), the version brief's coverage, requirement counts, the decisions index | Should fix | Mechanical: rewrite the index |
| 5 | Stale verified-on dates | Each entry in `architecture/ecosystem.md` carries a verified-on date. Flag dates older than the interval the repository states, or else older than the current version's start | Note; should fix for a dependency a ready bet relies on | Ask whoever owns the dependency to re-verify; never update a date without checking |
| 6 | Facts in two places | Look for the same table rows, targets, numbers, names or paragraphs in more than one file, such as an NFR target restated in the architecture or a risk copied into a version brief | Should fix | Ask which copy is the home, then replace the other with a link |
| 7 | Stable linking to volatile | Links from `product/`, `architecture/` or `decisions/` into `roadmap/`, `design/` or `research/`. A product or architecture file may cite a research note as evidence; only derived indexes may point at the roadmap. A plain-text ID that records provenance, such as `OQ-06` or `Bet 05` in a notes cell, is not a link and is allowed | Should fix | Ask, then move the fact or reverse the link |
| 8 | Quiet bets in delivery | For each `in delivery` bet, look up its work item's branches on the code host. Flag it when there has been no commit or pull-request activity for 14 days, or the interval the repository states | Note | Ask whether it is stopped, waiting for a human, or should be reshaped |
| 9 | Unsettled contracts | Every contract version a `ready` or `in delivery` bet consumes must be listed as `accepted` in the contract's header, which may show several versions, as in `Version: 1.1 proposed · 1.0 accepted` | Blocking | Ask; `designing-system-architecture` settles the contract |
| 10 | Statuses that contradict | A requirement `built` while every bet covering it is still open; a bet `done` with no outcome log; an architecture section `built` that no closed bet touched | Should fix | Ask, or close the bet properly |

A check that cannot run is reported as not checked, with the reason. Two examples: check 8 without host access, and check 5 when the repository has no ecosystem file.

## Reading the results

- Group findings by file so a fix touches each file once.
- One root cause with several symptoms is one finding. A capability file renamed without updating its links is one finding with a list of locations.
- Mechanical fixes go in the report's Fixed table, each with what changed.
- Everything else goes in Needs a decision, each with a proposed fix and the evidence.

## After the audit

When the user has decided, apply the fixes, then rebuild the derived indexes once at the end. A finding the user defers stays in the report. It is not copied into the registers unless it is a real product risk or open question.
