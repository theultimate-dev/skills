# Migration map: [sources] into [product] prototype context

Date: [YYYY-MM-DD] · Mode: [adopt] · Approved: [YYYY-MM-DD: "<person's words>" | pending]

<!-- Saved as research/YYYY-MM-DD-migration-map.md. Written before the move, updated with the approval before anything moves (see History), and closed with Verification. The presenting message summarises this file by count and by exception and names it for the rows; the rows are read here, not in the message. Delete this comment. -->

## Sources

<!-- Every document read gets a row per section in the Map, the ones that stay included. -->

| Source | Sections | Notes |
|---|---|---|
| [file or link] | [count] | [length, what it covers, built or planned] |

## Map

<!-- One row per inventory section. Treatment: move, split, merge, convert, derive, drop. A split names every destination; a drop states its reason, and a document that stays where it is gets drop rows that name where it stays, so line coverage can be checked.
Built behaviour becomes built rows. Unbuilt plans and unbuilt architecture never become requirement rows or planned sections without an open owning bet: they become a framing note with verdict park, or open questions. A planned legacy bet also keeps a numbered bet file with Status removed.
Behaviour the code has and no source states is proposed in its own rows, numbered X1, X2 and so on, apart from the S rows and outside their counts; each becomes a requirement row, with an ID, only when the person confirms it. -->

| # | Source section | Destination | Treatment | Notes |
|---|---|---|---|---|
| S1 | [file › heading path] | [path] | [treatment] | |

## Built rows and their evidence

<!-- One row for every built requirement row and every built architecture section the move writes. Evidence is a code path with lines, a test or a run. A fact about a system outside the code has no code evidence: write "the person's word" under Vouched by, which the approval confirms. -->

| Row or section | Source row | Evidence | Vouched by |
|---|---|---|---|
| [ID or `architecture/<file>.md`] | [S#] | [`path:lines`, test or run] | [code or the person's word] |

## Existing files

<!-- Only when a context folder already exists, for example a full-profile skeleton: one row for every file inside it, whatever happens to it, so completeness can be checked, and the count per treatment under the table. Versions, milestones and the roadmap folder have no home in the prototype profile: say where each row's content goes or why it is dropped.
Besides move, split, merge, convert, derive and drop, a row may use four treatments, defined here and nowhere else:
- restructure: the file stays and changes shape; its content stays in it, and its sections, columns or headings change.
- fill: a placeholder file gets its content.
- rebuild: a derived index is rewritten from the files it lists. Every derived index of an adopted skeleton is rebuilt, even when its rows do not change, so that its "Rebuilt by" line names the prototype skill and the date.
- keep: an authored file stays exactly as it is. Keep never applies to a derived index. -->

| File | Becomes | Treatment | Notes |
|---|---|---|---|
| [path inside the context] | [path, or none] | [treatment] | |

Count per treatment: [restructure n, fill n, rebuild n, keep n, move n, drop n; total n files]

## Beside the context

<!-- Only when documents outside context/ change: an app README, agent instructions, a docs folder, the pointer lines in the repository's root AGENTS.md, a new file such as an app's changelog. Each row is applied only with the person's agreement, row by row. Rows that are not agreed stay as they are and are listed for the person. A pointer line that already exists is listed as present, not changed.
Change holds the exact replacement text, or the line range plus the replacement, in a code span (double backticks when the text holds backticks) so that checks skip it. Links in it are relative to the edited file, not to this map. A new file is a row too: `file › lines` reads "new file" and Change holds its content or names its template.
Applying the rows: take one file's rows bottom-up, so that earlier line ranges stay valid; check the first words of the old text before replacing it; re-wrap the replacement to the file's width without splitting a link or a code span. -->

| # | File › lines | Change | Why | Agreed |
|---|---|---|---|---|
| B1 | [path outside the context › lines at HEAD] | [`replacement text`] | [reason] | [yes: "<person's words>" | no | pending] |

## Decision records

<!-- One row per record the move writes. Status is accepted only when the person made the decision; otherwise proposed. -->

| Record | Title | Status | Options and consequences from |
|---|---|---|---|
| [NNNN] | [title] | [proposed or accepted] | [S# or the person's words] |

## Judgment calls

<!-- What the person must confirm and the map recommends: a reading of a source, a boundary between two files, a row kept or dropped. -->

| # | Call | Recommended | Decision |
|---|---|---|---|
| J1 | [the call] | [answer and why] | [the person's words, or open] |

## Conflicts and duplicates

| ID | What disagrees | Where | Recommended answer | Decision |
|---|---|---|---|---|
| OQ-[NN] | [the conflict] | [S#, S#] | [answer and why] | [the person's words, or open] |

### Refinements

<!-- Places where the code is more exact than a source's wording. The row keeps the source's wording until the person confirms the refinement. -->

| Row | Source's wording | What the code does | Evidence |
|---|---|---|---|
| [ID or S#] | [wording] | [behaviour] | [`path:lines`] |

## Gaps

<!-- What the sources do not hold yet, and which skill fills it. Every section left out of a file because the sources do not fill it is listed here, with the one HTML comment the file carries. -->

- [gap]: [skill]

## History

<!-- One dated line for each change after the map was presented: the approval, the person's answer to a conflict or call, a question withdrawn. A question withdrawn before it is written to notes.md keeps its number, not reused, and has no row elsewhere. -->

- [YYYY-MM-DD]: [what changed]

## Verification

- Sections mapped: [n of n]
- ID tables: [table: source count = destination count]
- Relative links: [all resolve | list]
- Facts in two places: [none | list]
- Existing files handled: [n of n]
- Beside the context: [rows applied | rows left]
- Originals removed: [in commit [sha] | kept: [reason]]
