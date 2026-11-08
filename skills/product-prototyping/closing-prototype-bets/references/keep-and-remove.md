# Keep and remove

How to fold a tried bet into the context (keep) or take it back out (remove), with the git commands for the code. This file holds the one ordered checklist for each outcome; SKILL.md holds the gate and the routing. Paths in the context are relative to `context/`; paths in the code repository are relative to its root. Context and code share one repository. The commands are `git`; another version-control tool applies the same steps.

## Read first

| What | Where | Notes |
|---|---|---|
| Status, Context pinned, Build log, Result | The bet file in the working copy | Check `git status --short -- context/bets/NN-slug.md` and report an uncommitted file. A bet pinned `not yet` has no approved snapshot: read its draft as it stands |
| Everything else in the bet | The bet file at `Context pinned` | `git show <pin>:context/bets/NN-slug.md` |
| The code commits | The Build log | Every SHA, oldest first; a context commit between them is named and left out of the revert. An empty list means nothing was built, whatever the Status |
| The authority | The `Autonomy:` line at the pin, for an `approved` bet or any bet with a valid current pin. Only a bet whose pin is `not yet` because a reshape replaced it uses the last dated `Approved YYYY-MM-DD at <sha>: <autonomy line>` line of the Build log. A bet never approved has no authority beyond the person's explicit current words | `code commits: <branch>; context commits: yes or no; push: yes or no; revert on remove: yes or no`. The `Autonomy:` line of a bet that is not approved is a proposal and grants nothing |
| The changelog | The app's `CHANGELOG.md`, outside `context/` | At the root when the repository is one app |

Closing writes in two places that stay in two commits: the code (a revert, only for remove) and the context. Never mix them, so the history keeps showing which commits are code. Before any context commit, run `git diff --cached --name-only`: a path outside the close's own files stops the commit, and `git diff --cached` must show only what the close wrote.

## Preflight

Do this before writing anything, so that a removal can run on a clean tree.

1. The authority's branch is the one checked out (`git branch --show-current`); otherwise switch only if the working tree allows it, or ask.
2. The working tree is clean (`git status --porcelain` prints nothing). An uncommitted bet file or other change stops a revert: say what it is and ask the person to commit it or tell you what to do. Never stash or discard it.
3. Every code commit in the Build log exists (`git cat-file -e <sha>`) and is reachable (`git merge-base --is-ancestor <sha> HEAD`). Say which is missing and ask where the code lives now.
4. The words. Hold the person's words exactly as spoken; they are written into the Result later, in the context close.

## Is the evidence current

The Build log records the verified `Head`. Before Gate 2 presents any result:

```
git merge-base --is-ancestor <head> HEAD
git diff --stat <head>..HEAD -- . ':(exclude)context'
```

The exclusion keeps the context folder out; the app's changelog is outside it and stays in. An empty diff means the evidence describes the code. Otherwise read the diff against each check: a check whose files and behaviour the later diff does not touch is carried forward, marked `carried forward from <head>`; any other check is stale. Show stale checks as stale and offer keep only when none is. Proving a stale check again is a repair: it goes to `building-prototype-bets` as the repair path says in SKILL.md, step 2. Remove never needs fresh evidence.

## Keep

Result, requirements, architecture, decisions, notes, changelog, status, indexes: one context close, no code commit.

1. **Result.** Fill `## Result`: `Kept`, the date, the person's words, and the lesson. Write it first; the other edits cite it.
2. **Requirement rows.** For each row in Requirement deltas, edit the capability file in `product/requirements/`:

   | Delta | Row written |
   |---|---|
   | `new` | The reserved ID, the delta's text, Status `built` |
   | `changed` | The same ID with the new text, Status `built`, and a note in the row: `changed by bet NN: was "<old text>"` |
   | `dropped` | The same ID, Status `dropped`, the date and the delta's reason |

   Rules that follow from the checks:
   - A new requirement whose checks were all cut under appetite pressure was not built. Write it `dropped` with `bet NN: cut, <reason from the Build log>`. The number stays permanent.
   - A changed requirement whose checks were all cut keeps its old text and status: the behaviour it describes is still built.
   - A requirement partly cut is written `built` with its text narrowed to what was built, and the note says what was left out.
   - A capability file for a new prefix is created from the capability template (`templates/capability-requirements.md` in this skill): a one-sentence scope, then the table of ID, Requirement, Status and Notes. A row never leaves the table.
   - A requirement never links to the bet. The note may carry `bet NN` as plain text for provenance.
3. **Architecture.** Reconcile each entry under `Introduces` with the scope that was kept, using the rows just written and the Build log's evidence and cuts:

   | The entry | Do |
   |---|---|
   | Built as planned | Change `Status: planned` to `Status: built` and replace intent with as-built detail (the structure and the rules as they now are, never the code) |
   | Partly built | As above, narrowed to what the code has; the section says what was left out |
   | Belongs only to cut scope | Delete the planned section, concept or contract, then search for links to it and remove or redirect them (`grep -rn "<file name>" .` inside `context/`) |

   For each entry under `Touches`: read the section against the Build log and correct what changed. A contract detail settled while building goes into the contract, and its version is raised when the shape changed (a minor version for a compatible addition, a major version for a break). A contract version the bet relied on stays as `accepted`.
4. **Decisions.** A choice made while building moved the architecture when it changes something `architecture/` describes, a contract, or an accepted decision. Those get a record through `decision-records`, with the person's agreement, and the architecture file links to it. A choice inside one component that nothing else depends on stays in the Build log. An accepted record that no longer holds is superseded by a new one.
5. **Notes.** In `notes.md`: close a risk the bet retired and say how; mark an open question `resolved` with a link to the answer; add the risks and questions the Build log and the person's words revealed, each with the next free `RSK-` or `OQ-` number. Add new terms to `product/glossary.md`.
6. **Changelog.** Check that the bet's entry exists, under `[Unreleased]` or in a release, and says what was kept. A cut check may make a line untrue: edit an `[Unreleased]` line; for a released entry, add a correcting line under `[Unreleased]`. Cut no version. This edit is a code-side file: when it is needed, make it as its own code commit within the Autonomy line, apart from the context close.
7. **Status.** Set `Status: kept`.
8. **Indexes.** Rebuild last, as SKILL.md step 6 says, then commit the context close if the Autonomy line allows it.

### Quill example: keep

Bet 03, "A weekly recap page shows the last seven days of words". Appetite 1 day. Pinned at `9f1c2ab`; code commits `c3d4e5f`, `b2c3d4e`, `a7b8c9d`; `~ C3` (a sparkline) was cut.

- Deltas: `STK-06` new ("The recap page lists words written per day for the last seven days"), `STK-07` new ("The recap page shows a sparkline of those days"), `STK-02` changed (the day boundary is local midnight, not UTC).
- Result: "Kept, 2026-11-12: 'Keep it. The page is what I open each morning.' Lesson: the recap is used daily, and the day boundary confused me twice, so it earned its own requirement."
- `streaks.md`: `STK-06` `built`; `STK-02` updated with the note `changed by bet 03: was "A day ends at 00:00 UTC"`; `STK-07` `dropped`, `bet 03: cut, sparkline over the appetite`.
- Architecture: `architecture/concepts/day-boundary.md` goes from `Status: planned` to `Status: built`, now describing where the boundary is computed. `architecture/runtime/recap-request.md` is corrected to the single query the build used.
- Decisions: the build chose to store streaks per local date instead of per timestamp, which moved a stated concept, so `decisions/0007-store-days-as-local-dates.md` is written through `decision-records`. Choosing a charting library for the page is not: it stays in the Build log.
- Changelog: `[Unreleased]` already holds "Added: weekly recap page" from the bet's commits; the line is kept as it is, because the sparkline was never in it.
- Indexes: requirements README counts (built +2, dropped +1), the Contracts table and the oldest verified-on date of the architecture README (unchanged: no contract moved, no dependency re-verified), `decisions/README.md`, the board row for bet 03 now `kept`, no reserved IDs.

## Remove

Code first, as one commit; then the context, as another.

1. **Preflight and words.** As in "Preflight" above: branch, clean tree, reachable commits, the person's words held. The code commit list decides whether there is anything to revert: with an empty list skip to step 7, and the Result says nothing was built.
2. **Read the commits.** The Build log lists every code commit by SHA, oldest first, and names any context commit between them. Show each one:

   ```
   git show --no-patch --format='%h %s' <sha>
   ```

   Compare each subject with the Build log's; a difference is a question for the person, not a guess. Then check that each listed commit holds only code:

   ```
   git show --name-only --format= <sha> | grep '^context/'
   ```

   Empty output means the commit is code only. The context commits the Build log names are left out of the revert, and the report says so. A commit that mixes code and context stops the revert: ask.

   A merge commit in the list also stops it. That command prints nothing for a merge, which proves nothing, and reverting a merge against its first parent would take back everything else it brought in, context included. Show the merge's full diff against the parent you would revert to (`git diff --name-only <merge>^1 <merge>`), propose which parent and which paths, and run nothing until the person has reviewed the plan.
3. **Check the authority.** `revert on remove: yes` (in the Autonomy line at the pin, or, only for a bet whose pin a reshape replaced with `not yet`, in the last `Approved` line of the Build log): continue on the branch `code commits:` names. `no`, or the line is silent: show the commands below and ask whether to run them, or leave them with the person; the context close then waits until the person says the revert is in. The same holds for pushing.
4. **Prepare the revert.**

   ```
   git revert --no-commit <newest> ... <oldest>
   ```

   Every listed SHA, newest first, and only those. On a conflict, a later commit depends on the bet's code: run `git revert --abort`, show the conflicting files, and ask. Never resolve one by guessing.
5. **Changelog, still uncommitted.** Search the changelog for the bet's entry text.
   - Entry only under `[Unreleased]`: the revert took it out. Confirm it is gone.
   - Entry in a released section (a release that carries the code, `git tag --contains <newest>`, always means this case): keep the released section exactly as it was. Add under `[Unreleased]`, `### Removed`, a line for users: what went away and, if useful, why. Cut no version.
6. **Check the prepared revert, then commit it.**

   ```
   git diff --cached --name-only
   git diff --stat <oldest>^ -- <the files the listed commits touched>
   git show --diff-filter=A --name-only --format= <oldest> ... <newest>
   ```

   - The staged paths are code and the changelog only; nothing under `context/`.
   - The second command compares every file the bet touched with its state before the bet. Empty means the code is back exactly. Output from later, unrelated commits is fine: read each hunk and confirm none comes from the bet.
   - Each file in the third list should no longer exist: `test ! -e <path>`.
   - Search for the bet's own identifiers (a new function name, a route, a table, a translation key). Nothing should match outside `context/` and the changelog's `Removed` entry, if one was added.
   - Run the project's build and tests as the Build log names them. A failure means the revert cut too much or too little: show it, do not patch around it.

   Then make one commit, the revert and the changelog line together, with the project's commit convention and its sign-off rule, naming the bet: for Quill, `revert: remove the weekly recap page (bet 03)`.
7. **Context close.** Now write, and commit apart from the code when `context commits: yes`:
   - **Result.** Fill `## Result`: `Removed`, the date, the person's words, and the lesson. Then set `Status: removed`.
   - **Requirements.** Each new ID in Requirement deltas is written as a row in its capability file with Status `dropped`, the date, and `bet NN removed: <reason>`. Keep the delta's text so the row says what was dropped. Create the capability file from the capability template (`templates/capability-requirements.md` in this skill) when the prefix is new. Rows the bet changed or dropped stay as they were; the revert restored the behaviour they describe. The reserved numbers stay used, so the next bet continues after them.
   - **Architecture.** Delete each section, concept and contract the bet introduced as `planned`, then search for links to the deleted files and remove or redirect them (`grep -rn "<file name>" .` inside `context/`). A relied-on, accepted contract stays.
   - **Decisions.** An accepted record stays. If one only made sense with the bet, write a superseding record through `decision-records`; otherwise leave the log alone.
   - **Notes and research.** Add the risks and open questions the try revealed. If the removal changes the framing note's conclusion, add a line under its Verdict naming the date and the bet; do not rewrite the note.
   - **Indexes.** Rebuild last, as SKILL.md step 6 says, the board in the same change as the Status.

   Before the commit, `git diff --cached --name-only` shows only the close's own paths.

### Quill example: remove

Bet 04, "A streak freeze protects one missed day". Appetite 1 day. Pinned at `5d6e7f8`; code commits `1a2b3c4`, `2b3c4d5`, `4c5d6e7`, `6d7e8f9`; reserved `STK-08` and `STK-09`. The person tried it for a week: "Remove it. A freeze makes the streak meaningless to me."

- Autonomy (at the pin): `code commits: main-proto; context commits: yes; push: no; revert on remove: yes`. The revert runs on `main-proto`, nothing is pushed.
- The branch is `main-proto` and the tree is clean. `git show --no-patch --format='%h %s'` on each of the four listed SHAs matches the Build log, and `git show --name-only --format= <sha> | grep '^context/'` is empty for each. `git revert --no-commit 6d7e8f9 4c5d6e7 2b3c4d5 1a2b3c4` prepares the revert.
- `git diff --stat 1a2b3c4^ -- <touched files>` is empty; the one added file, `src/freeze.ts`, no longer exists; `grep -rn "freeze" src` matches nothing; the build and tests pass. Then one commit: `revert: remove the streak freeze (bet 04)`.
- Changelog: the `Added: streak freeze` line sat under `[Unreleased]` and the revert removed it. Had it been in `0.3.0`, the line `### Removed` under `[Unreleased]`, "The streak freeze is gone; a missed day always ends the streak.", would have been staged with the revert and committed with it.
- The context close is a second commit, and the Result is written there.
- `streaks.md`: `STK-08` and `STK-09` become `dropped`, 2026-11-14, `bet 04 removed: a freeze made the streak meaningless to its only user`. `STK-02`, which the bet had changed, keeps its existing text.
- Architecture: the planned `architecture/concepts/streak-freeze.md` is deleted and a link to it in `architecture/README.md` is rebuilt away.
- Result: "Removed, 2026-11-14: 'Remove it. A freeze makes the streak meaningless to me.' Lesson: the value of a streak is that it can break; any softening needs a different signal than a counter."
- `notes.md` gains `OQ-05`, "Does Quill need a gentler way to recover after a broken streak?", and the board row for bet 04 shows `removed`.

## A stopped bet

The Build log says what was done and what is left. Show both, with the cut options. If the person chooses to reshape, hand the bet to `shaping-prototype-bets`, which keeps the bet's number, its reserved IDs and its whole Build log. If the person chooses to remove, follow "Remove": the commits are whatever the Build log lists, possibly partial or none, and the Result names what was left unbuilt as the lesson.

## Light audit

Run on request. Everything below is read-only until the report is assembled.

| Check | How | Fix |
|---|---|---|
| Broken links | Resolve every relative Markdown link outside code fences against its file's directory; check each fragment against the target's headings | Mechanical when the target was renamed and exactly one file matches; otherwise ask |
| Duplicate or reused IDs | Collect every requirement, NFR, use-case, risk, open-question, decision and bet ID with its file, and the IDs reserved on the board and recorded in `product/requirements/id-map.md`. An ID defined twice is a duplicate; a dropped, reserved or id-mapped number given to something new is reused | Ask; never renumber an ID a bet or record already cites |
| Stale indexes | Rebuild each derived index from its files and compare: requirements README, the Contracts table and the oldest verified-on date of the architecture README (its authored sections are not compared), folder READMEs, the board | Rewrite the index, the table or the date |
| Reserved IDs | Every ID reserved by an open bet is unused in the catalogue, in `id-map.md` and by every other open bet | Ask |
| Bets that contradict | A bet `kept` or `removed` with an empty Result; a `built` requirement row whose bet is `removed`; a `planned` section with no open bet that introduces it | Ask, or close the bet properly |

Report the fixes made and the findings that need a decision, and name every check that could not run, with the reason.
