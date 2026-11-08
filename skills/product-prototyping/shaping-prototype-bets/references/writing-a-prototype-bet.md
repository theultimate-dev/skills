# Writing a prototype bet

Section by section, what a bet file holds and how good text differs from weak text. A bet is read by two audiences: the person, who approves it at Gate 1 and judges it at Gate 2, and a builder with a fresh context, which builds it from the bet and its context pack alone and is reviewed against the bet's intent. Write for both.

The examples come from Quill, a single-user web app that tracks daily writing streaks. Bet 03 adds a weekly recap.

## Header

```
# Bet 03: A weekly recap after the last entry of the week
Status: shaped
Appetite: 1 day · Framing: research/2026-11-02-weekly-recap.md
Autonomy: code commits: main-proto; context commits: yes; push: no; revert on remove: yes
Context pinned: not yet
```

The title states the outcome, not the work. Keep the four header lines in this form: building and closing find them by their labels. The Autonomy line at shaping is a proposal; Gate 1 replaces it (see the last section). Framing is the path of the note whose verdict is `shape`.

- Weak: `# Bet 03: Recap feature`
- Better: `# Bet 03: A weekly recap after the last entry of the week`

## Outcome

Two to four sentences on who can now do what and what they see. One outcome a person can try on its own. No implementation.

- Weak: "Add a recap table, a job that aggregates entries and a recap page."
- Better: "The writer sees a recap after logging the last entry of a week: words written per day as seven bars, the total, and the longest run of the week. It appears on the page they land on after saving, and a week with no entries shows no recap."

## Requirement deltas

A table with one row per requirement the bet adds, changes or drops. The bet holds these rows until it closes; the catalogue holds only `built` and `dropped` rows.

| ID | Change | Text or reason |
|---|---|---|
| RCP-01 | new | After the writer saves the last entry of a calendar week, the app shows a recap of that week. |
| RCP-02 | new | The recap shows the words written on each day, their total and the longest run of consecutive days with an entry. |
| STK-03 | changed | The post-save page shows the streak count and, when RCP-01 applies, the recap. |

- New rows use IDs reserved by the next-free rule in [sizing and readiness](sizing-and-readiness.md). The text is a requirement in its own right: one thing, testable, in the product's words from `product/glossary.md`.
- A changed row carries the full new text, not a diff. The catalogue keeps the old text in its history note when the bet is kept.
- A dropped row names the reason. Weak: "obsolete". Better: "Superseded by RCP-02: the recap replaces the daily total."
- Weak: "RCP-01 new: recap" (no text). Better: the full sentence above.

## Acceptance checks

One observable result per line, from outside the code, with concrete values. Each names the requirement it proves and one Method.

| Method | Use when | Evidence the builder records |
|---|---|---|
| `test` | A rule or computation an automated test can pin | The test's name and that it failed before the change |
| `build` | The project must still compile, type-check or lint clean | The command and its result |
| `run and observe` | Behaviour is visible in the running product | The steps taken and what was seen, with a screenshot or captured output |
| `inspect output` | The result is a file, a response, a log line or command output | The output, quoted |
| `person's eye` | Only the person can judge it: feel, wording, layout | Nothing; it is listed for Gate 2 |

Choose the cheapest method that gives real evidence. `build` alone never proves behaviour; `person's eye` is not a condition for `built`, so a bet needs at least one check that is not the person's eye.

- Weak: `C1 (RCP-01): The recap works. · Method: test`
- Better: `C1 (RCP-02): Given entries of 300, 0, 450, 200, 0, 0 and 600 words on Monday to Sunday, the recap lists those seven values, a total of 1550 and a longest run of 2 days. · Method: test`
- Weak: `C2 (RCP-01): The recap looks nice. · Method: run and observe`
- Better: `C2 (RCP-01): After saving a Sunday entry, the post-save page shows the recap; after saving a Wednesday entry it does not. · Method: run and observe`
- Better, for a judgement: `~ C3 (RCP-02): The seven bars read at a glance on a phone-width window. · Method: person's eye`

Every requirement in the bet has at least one check, and every behaviour the shaping decided has one: the empty week, the limit, the error case. Mark with a leading `~` the checks that may be cut if the appetite runs short; cut from the least valuable up. Leave small engineering detail, such as exact bar colours or rounding of an average, to the builder, inside the bet's boundaries.

## Boundaries

- **No-go**: what the bet will not do, though a reasonable reader might expect it. "No-go: emailing the recap; it appears in the app only." The builder treats a no-go as a stop: it stops and reports rather than crossing it.
- **Rabbit hole**: a known risk that could eat the appetite, with how the shaping patched it. "Rabbit hole: which day a week starts on and the writer's time zone. Patched by: weeks run Monday to Sunday in the browser's local time; no setting." An unpatched one says what to do if it bites, usually "stop and reshape".
- **~ Cuttable**: scope to drop first when it is broader than one check. "~ Cuttable: the longest-run figure."

Weak: "No-go: anything out of scope." Better: a named thing someone might well have added.

## Keep or remove

The signal is what the person will judge at Gate 2 after trying the bet. It is concrete, can be seen within days, and points at value rather than at the bet working. `If removed` states what the removal leaves behind and what stays.

- Weak: "Signal: it feels useful." If removed: "Revert it."
- Better: "Signal: after three evenings of logging, the writer still opens the recap on Sunday without being prompted, and its figures match what they wrote. If removed: the code commits are reverted, RCP-01 and RCP-02 are recorded as dropped with the reason, the planned `recap` concept is deleted, and STK-03 stays as it was. The framing note and the lesson stay."

Draw the signal from the framing note's Remove if line; when the note has none, ask the person what would make them delete this.

## Architecture

```
- Touches: web app (architecture/context.md), streaks capability (product/requirements/streaks.md)
- Introduces: architecture/concepts/week-boundaries.md (Status: planned)
- Relies on: decisions/0004-store-entries-as-daily-totals.md
```

Paths are relative to `context/`. A relied-on contract must be `accepted` at the version named. An introduced section is written at shaping as `Status: planned` and says what the bet fixes about it; closing turns it to `built` or deletes it. Write `none` for a line that has nothing.

- Weak: "Relies on: the architecture."
- Better: the path of the decision or contract and, for a contract, its version.

## Context pack

The files the builder reads, in order, from general to specific, each with why. Usually five to ten entries, a guide rather than a count; the first is `product/overview.md` unless the bet needs less.

```
1. product/overview.md: what Quill is and who it is for
2. product/glossary.md: entry, streak, week
3. product/requirements/streaks.md: STK-03, the row this bet changes
4. architecture/context.md: where the web app and its storage sit
5. architecture/concepts/week-boundaries.md: the planned rule for week edges
6. decisions/0004-store-entries-as-daily-totals.md: why entries are totals per day
```

The pack is complete when a builder could build the bet without reading anything else in `context/`, and short when every entry earns its place. Every file in it is committed before the pin; a file written at shaping is committed with the bet at Gate 1, and the pack is checked at that commit before the pin is published.

## Build log and Result

Leave both empty. `building-prototype-bets` writes the Build log; `closing-prototype-bets` writes the Result.

## The Autonomy line

At shaping, propose a line with four fields: the branch the code commits go on, whether context commits are allowed, whether the builder may push, and whether closing as removed may revert the code commits. Recommend the branch the person works on, `yes`, `no`, `yes`: a removed bet is undone by a revert on that branch, while a bet branch would need a merge to keep, which this loop does not have.

```
Autonomy: code commits: main-proto; context commits: yes; push: no; revert on remove: yes
```

At Gate 1, replace it with the approved line and the person's words, copied as they said them:

```
Autonomy: code commits: main-proto; context commits: yes; push: no; revert on remove: yes. Approved 2026-11-06: "approved, keep it local"
```

- Weak: "Autonomy: full." Better: the four fields, each decided.
- Weak: paraphrasing the person ("the owner agreed"). Better: their words in quotation marks, with the date.

If the person approves the bet but changes the line, record their line. Anything the line does not allow, the builder asks for.
