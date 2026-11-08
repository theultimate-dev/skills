# Sizing and readiness

How to size a prototype bet to a fixed appetite, what to do with an idea that does not fit, how to reserve IDs, how to check readiness, and how the bet is pinned at Gate 1.

## Appetite, not estimate

An estimate asks how long the work will take. An appetite says how much the try is worth, and the shaping makes the work fit it. The appetite is set before building starts and is a ceiling: when the work outgrows it, the builder cuts the `~` checks and scope, and when nothing is left to cut the bet is `stopped` and reshaped. Only the person's words raise an appetite, and a raise is a new total for the whole bet across reshapes: a bet that has used a day of a one-day appetite and is raised to two days has one day left, not two.

| Appetite | Fits | Typical shape |
|---|---|---|
| ½ day | One requirement, one or two checks, no new contract | A small behaviour on a screen or command that already exists |
| 1 day | Two to four requirements, up to about eight checks, at most a planned concept | One flow end to end through what the prototype already has |
| 2 days | Up to about six requirements, up to about twelve checks, at most one new contract | A flow that needs a new rule, a new store or a new surface |

The figures are guides, not limits; the appetite counts working time, and a wait for the person, recorded in the working log, does not count, so a question the bet cannot do without is settled at shaping, not in the middle of the build. Work smaller than half a day joins a neighbouring bet, or is done without a bet. Never pad a bet to fill its appetite.

## Size signals

| Signal | Too big: cut or split | Too small: merge |
|---|---|---|
| Outcome sentence | Needs "and" to say what the person gets | Describes a step, not a result |
| Requirements | More than about six | One that makes no outcome on its own |
| Checks | More than about twelve; they would not fit one sitting to review | None the person could try |
| Contracts and concepts | Introduces more than one contract | |
| Rabbit holes | An unpatched one that could eat the appetite | |
| Person's attention | Needs the person's eye at several points mid-build | |

## An idea that does not fit

Cut by outcome, never by layer: each bet ends in something a person can try, end to end through what it needs. A bet for "the storage" then another for "the screen" cannot be tried or judged on its own.

1. Find the thinnest outcome that still answers the framing note's question: can the writer see a recap at all?
2. Shape that as the bet. Put the rest into the Cuttable line only if it is cheap to drop; otherwise it is out of this bet.
3. Tell the person what was left out. They may ask for it as a second bet, shaped after this one or alongside it, citing the same framing note; each bet has its own Gate 1. An idea that does not survive a first try may never need the rest.
4. When one unknown dominates, shape a small bet that tests only that unknown first.

## Reserving IDs

Reserved IDs are the new requirement numbers a bet will use, so two open bets cannot take the same one.

1. Open the capability file in `product/requirements/` and find the highest number used, `built` and `dropped` rows included.
2. Read the board (`bets/README.md`) and every open bet's Requirement deltas: take the highest number any of them reserved in that capability.
3. Also count reservations of removed bets: their IDs sit in the catalogue as `dropped`, which step 1 finds. A bet parked at adoption is a `removed` row on the board, and the IDs reserved for rows moved to parked notes are in `product/requirements/id-map.md`; read both. Numbers continue after the highest ever used and are never reused.
4. Reserve the next numbers in order, one per new requirement, except one the bet claims under step 5.
5. **Claim, don't reallocate, a parked requirement.** When the bet builds a requirement that adoption parked and reserved in `id-map.md`, do not take a new number: the `new` delta keeps the reserved ID, so the requirement keeps the identity adoption preserved. Append a line to `id-map.md` naming the claiming bet (`claimed by bet NN`, with the date), never editing the earlier lines. From then on the reservation is the bet's own, like its board reservations, and a reshape keeps the claim. Scope that is not the same requirement never reuses the number, and a claim that the bet abandons stays recorded: the number is then `dropped` at close like any other.

A new capability needs a prefix of two to four letters not used by any file in `product/requirements/` and not clashing with `NFR`, `UC`, `RSK` or `OQ`. Its file is created at closing, when the rows become `built`; until then the rows live in the bet.

Example: `streaks.md` holds STK-01 to STK-05, STK-05 `dropped`, and no open bet reserves STK numbers. A bet adding one streak requirement reserves STK-06. A bet adding the first recap requirements reserves RCP-01 and RCP-02.

## Checking readiness

| Check | How |
|---|---|
| Requirement deltas | For each reserved ID, no catalogue row defines it and no other bet reserves it (another board row, another bet's deltas, a removed or parked bet, `id-map.md`); the bet's own board row and deltas are not a collision, and a reshape keeps them. An `id-map.md` reservation of a parked requirement is the bet's own when the bet builds that requirement and a line naming the bet claims it; for any other scope it is a collision. Look up each changed or dropped ID: its row is `built`. Each dropped delta has a reason written in full |
| Acceptance checks | List the requirements from the deltas and check each has a `Cn` line. Read each check as a stranger: could they decide pass or fail from outside the code, with the values given? Each has one Method; at least one check is not `person's eye` |
| Person's-eye checks | Collect every `person's eye` check into the Gate 1 message with what the person will look at, so Gate 2 can ask for it |
| Appetite | Compare the number of requirements and checks with the table above; confirm every `~` item is cheap to drop |
| Boundaries | Find at least one no-go a reasonable reader might expect to be in scope. For each rabbit hole, find the patch or the stop-and-reshape line |
| Keep or remove | Read the signal as the person: can they tell, after trying it, whether it holds? Check the removal list against the deltas and the planned sections |
| Architecture | For each consumed contract, read its header: the version named is `accepted`. For each relied-on decision, check its status in `decisions/README.md`. Introduced sections carry `Status: planned` |
| Open questions | Read `notes.md`: no `open` question that the bet depends on is unanswered. Open risks that bear on the bet are named in a rabbit hole |
| Context pack | Every path exists, committed or pending as a shaping artifact the Gate 1 commit will include; the entries run general to specific; each earns its place, and nothing the builder needs is missing. Five to ten is a guide, not a gate |
| Context repository | `git status --porcelain -- <every path the bet names>` prints nothing, except the pending shaping artifacts: the bet, the board, the planned sections, `notes.md` rows, and the whole framing note with its research index. Uncommitted changes to any other pack file would be missing from the pin |

Report every failed row with the skill or person that fixes it: `decision-records` for a decision, the `product-design` skills for a design, the person for an open question. A contract that the bet only introduces is not a blocker: it is written as planned. Never make a bet ready by weakening a check or dropping a boundary. A failed row keeps the bet `shaped`; Gate 1 offers approval only when every row passes on a check made now, and again before approval is recorded if anything the rows read has changed.

## Pinning at Gate 1

The pin is the commit the builder reads the bet at. The builder reads the shaped fields at the pin: every header line except `Status:` and `Context pinned:`, and every section except Build log and Result. It reads `Status:`, `Context pinned:`, the Build log and the Result from the working copy, reporting any uncommitted state, so writing them after the pin never looks like a change to the bet.

```bash
git diff --cached --name-only                          # must be empty, or only the paths below; otherwise stop and tell the person
git status --porcelain -- <every path the bet names>   # only the pending shaping artifacts
git add <the bet, the board, the planned sections, notes.md, the framing note, research/README.md>
git diff --cached --name-only                          # exactly those paths, nothing else
git commit -m "<the project's convention, for shaping bet NN>"
git rev-parse HEAD                                     # the commit: the full SHA
git cat-file -e <sha>:context/<path>                   # for every Context pack path
```

Staged work that is not part of the approved paths is the person's: stop, name it, and commit nothing until it is unstaged or the person says what to do. Never unstage or include it yourself.

Write the SHA as `Context pinned: <full sha>` and commit that line alone, with the same two index checks around it. A pack path missing at the commit means the pin is not published: fix the pack, commit again and take the new SHA. Commit only when the approved Autonomy line says `context commits: yes`; otherwise the bet stays `approved` with `Context pinned: not yet`.

## Statuses this skill sets

| Status | When |
|---|---|
| `shaped` | The bet file is written, or a stopped or paused bet was reshaped |
| `approved` | The person approved the bet and its Autonomy line at Gate 1, in explicit words |

`building`, `built`, `stopped`, `kept` and `removed` belong to the other skills. Only the bet file's Status line is authoritative; the board copies it.
