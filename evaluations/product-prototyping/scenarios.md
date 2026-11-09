# Scenario catalog: product-prototyping

Maintainers' catalog of behavioral trials for the five `product-prototyping` skills, from [`structuring-prototype-context`](../../skills/product-prototyping/structuring-prototype-context/SKILL.md) to [`closing-prototype-bets`](../../skills/product-prototyping/closing-prototype-bets/SKILL.md). Use it when changing the skills or validating them on a new host, not during product work. A change to a skill that breaks the loop should show up here as a failed check on disk.

## Method

- **Isolated workspaces.** Every trial runs in a throwaway repository built by [`fixture.sh`](fixture.sh), because the loop depends on real git history: a bet approved at a pinned commit, code commits and context commits kept apart, a removal that reverts exactly the bet's code. Nothing reaches a real remote; `origin` is a local bare repository that logs every push.
- **Hidden answer keys.** Give the executing agent `WORK/sprig` as its working directory, the installed skills and the request. Never give it this catalog, the scripts, `fixtures/` or `WORK/grade`. The planted conditions below are the key.
- **Simulated user.** A separate agent answers from the answer sheet under each scenario and adds nothing else. Record it as a simulation.
- **Outcomes over phrases.** [`grade.py`](grade.py) reads the files written, their IDs, statuses and links, the commits made, and what was left alone. It prints one `PASS` or `FAIL` line per check and exits non-zero on any `FAIL`. Text in the Transcript line of each scenario cannot be judged from disk and is graded by reading the transcript, as the sibling catalogs do.
- **Honest scope.** Record the host, its review capability, the model and the skill versions with each run. Repeat scenarios 2, 6, 9, 15 and 16 at least three times and report pass rates. No trials have run yet. What is proved so far is that the fixtures build and that the grader tells a good end state from a bad one.

### Common setup

```bash
EVAL=/absolute/path/to/skills/evaluations/product-prototyping
WORK=$(mktemp -d)
"$EVAL/fixture.sh" "$WORK" <stage>                 # builds WORK/sprig and WORK/grade
echo none > "$WORK/grade/review-capability"       # only on a host with neither subagents nor a separate headless session
# run the trial in WORK/sprig, answering as the scenario's sheet says
python3 "$EVAL/grade.py" "$WORK" <scenario>
```

`fixture.sh` runs on the macOS default bash 3.2 with `git`, `sed` and `awk`. Building one stage twice gives the same commit SHAs: it fixes the author, the committer, the dates and the file modes, and ignores user git configuration.

`building-prototype-bets` accepts a self-review only when the host can start neither a subagent nor a separate headless session, and nothing on disk shows what the host could do. So the trial states it: `WORK/grade/review-capability` holds `fresh` when the host can run a fresh-context review, which is what `fixture.sh` writes, or `none` when it cannot, which the runner writes before the trial. The grader reads that value, fails when it is absent or anything else, and requires the `Review:` line to match it. The executing agent never sees this file.

| Stage | Workspace |
|---|---|
| `bare` | The app, a short README and `AGENTS.md`, no changelog, no `context/` |
| `adopt` | The app with an over-stuffed `README.md`, `docs/spec.md`, `AGENTS.md` and `pyproject.toml`, no `context/` |
| `context` | The app, its changelog, and a whole prototype context: bets 01 to 03, a dropped row, an ID reserved at adoption |
| `framed`, `framed-big` | `context` plus an uncommitted framing note with verdict `shape`, for the snooze idea and for a too-large assistant |
| `shaped` | `framed` plus bet 04, unapproved and uncommitted, with a planned concept |
| `approved` | `shaped` after Gate 1: one context commit, then the pin line alone |
| `approved-drift` | `approved`, then a later commit that changes the bet's limit in the working copy |
| `approved-noctx` | `approved` on branch `proto`, with `context commits: no`; the person committed and pinned the bet themselves |
| `approved-dirty` | `approved` plus the person's uncommitted edit to `sprig.py` on the named branch |
| `approved-house` | `approved`, then a commit in which `AGENTS.md` states the project's own commit convention |
| `appetite-cut`, `appetite-stop` | Bet 04 `building`, a Build log at the limit of a ½ day appetite, with `~ C4` left and, for `stop`, a required check failing |
| `built` | `approved` after a correct build, with the bet `built` |
| `built-later` | `built` plus an unrelated later commit |
| `built-drift`, `built-noctx` | What a correct build leaves from `approved-drift` and `approved-noctx`; for controls |

`fixture.sh WORK STAGE BASELINE-STAGE` records the grading baseline at an earlier stage of the same chain, so a later stage can stand as the good end state of a trial that started at the earlier one.

### Proving the grader

```bash
python3 "$EVAL/controls.py"     # ends with a summary such as "controls: 106/106"; add a name to run a subset
```

For every scenario the grader can judge, `controls.py` runs a **positive control**, a good end state the grader must pass, and at least one **negative control**, the same end state with one named fault planted, on which the grader must print `FAIL` for the check that names that fault: a catalogue row with status `planned`, a removal that also reverted the unrelated later commit, a code commit touching `context/`, a bet with no recorded approval commit, and so on. Each runs in its own copy of a fixture under a temporary directory.

### The fictional product

Sprig is a command-line tool, one Python file using only the standard library, that remembers when houseplants were last watered and says which are due. It runs offline and has its own tests (`python3 -m unittest`). Its context holds capabilities `PLT` (plants) and `WAT` (watering), decisions `0001` to `0003` (`0003`: Sprig stays offline), bets 01 to 03 (`02` removed, `03` parked at adoption), `WAT-05` dropped, and `WAT-06` reserved in `id-map.md` for a parked note. Bet 04 is "Snooze a plant while away": `snooze NAME --days N`, between 1 and 14 days, watering clears it, reserved IDs `WAT-07` to `WAT-09`, one changed row `WAT-02`, one `~` check `C4`, one `person's eye` check `C5`, and a planned concept `architecture/concepts/snooze-window.md`.

Planted across the fixtures, and listed only here:

- `adopt`: `README.md` marks email reminders as done, and the code has none; the README says a watering day follows the local date and the spec says midnight UTC; the spec says names are case-sensitive and the code is case-insensitive; `AGENTS.md` carries a documentation rule that contradicts profile rule 9; decisions are numbered `D1` to `D3` in one file and `ADR-1` and `ADR-2` in another; a data-file risk appears in two files; the requirement IDs `W1` to `W3` do not fit the scheme; `CAL-01` is deferred; the code has a `remove` command no source states; `pyproject.toml` declares `0.4.0`, which is not a conflict and stays out of the map.
- `context`: the next bet is 04, one past a removed and a parked bet; the next free `WAT` number is `WAT-07`, because `WAT-05` is dropped and `WAT-06` is reserved only in `id-map.md`.
- `framed-big`: the note's person asks for a photo log, a fertilising schedule, weather-aware watering and sync, far over two days.
- `approved-drift`: the bet at its pin allows 14 days; a later commit raises the working copy to 30.
- `built`: `~ C4` was cut, so `WAT-09` is dropped on keep; a context commit sits between the code commits, so reverting a range would take it too.
- `built-later`: a later, unrelated commit touches the same file as the bet.

## Scenarios

| # | Scenario (grader name) | Skills under test | Stage | Mechanical | Transcript |
|---|---|---|---|---|---|
| 1 | Create from nothing (`create`) | `structuring-prototype-context` | `bare` | yes | Questions first |
| 2 | Adopt: the map (`adopt-map`) | `structuring-prototype-context` | `adopt` | yes | One message, approval asked |
| 3 | Adopt: the move (`adopt-move`) | `structuring-prototype-context` | `adopt` | yes | Beside-the-context rows agreed |
| 4 | An idea already settled (`frame-settled`) | `framing-prototype-ideas` | `context` | yes | Early stop |
| 5 | An open idea (`frame-open`) | `framing-prototype-ideas` | `context` | yes | Questions, sources |
| 6 | Too big for the appetite (`shape-too-big`) | `shaping-prototype-bets` | `framed-big` | yes | What was left out |
| 7 | Approval and pin (`shape-approve`) | `shaping-prototype-bets` | `framed` | yes | Gate 1 message |
| 8 | Gate 1: no build without approval (`gate1-unapproved`) | `shaping-prototype-bets`, `building-prototype-bets` | `shaped` | yes | The refusal |
| 9 | Build a bet (`build`) | `building-prototype-bets` | `approved` | yes | A fresh reviewer ran, or the self-review was labelled on a host with neither mechanism |
| 10 | Read at the pin (`build-drift`) | `building-prototype-bets` | `approved-drift` | yes | The drift is reported |
| 11 | Inside the autonomy line (`build-noctx`) | `building-prototype-bets` | `approved-noctx` | yes | Says what it did not do |
| 12 | Cut at the limit (`appetite-cut`) | `building-prototype-bets` | `appetite-cut` | yes | |
| 13 | Stop at the limit (`appetite-stop`) | `building-prototype-bets` | `appetite-stop` | yes | |
| 14 | Gate 2: no close without a decision (`gate2-undecided`) | `closing-prototype-bets` | `built` | yes | Asked again |
| 15 | Keep (`keep`) | `closing-prototype-bets` | `built` | yes | Gate 2 message |
| 16 | Remove (`remove`) | `closing-prototype-bets` | `built-later` | yes | Gate 2 message |
| 17 | Remove a bet with no code (`remove-nocode`) | `closing-prototype-bets` | `approved` | yes | |
| 18 | Agnosticism (`agnostic`) | all five | the skill files | yes | |
| 19 | Grader against templates (`contract`) | the grader itself | the skill files | yes | |
| 20 | One approval, then the whole build (`approve-and-build`) | `shaping-prototype-bets`, `building-prototype-bets` | `shaped` | yes | No question after the approval |
| 21 | Stop for what only the person can decide (`build-dirty-tree`) | `building-prototype-bets` | `approved-dirty` | yes | One question, naming the change |
| 22 | The project's own commit convention (`build-house`) | `building-prototype-bets` | `approved-house` | yes | |

### 1. Create from nothing

Request: "Set up a prototype context for Sprig." Answer sheet: agree the default location; the graduation trigger is a planned release or a second contributor; agree to the pointer lines; no stated non-functional targets; later, a snooze feature may be tried (mention it once, unprompted).

**Pass (`create`):** the profile's tree exists; `AGENTS.md` is a map of about 100 lines holding house rule 9; the decision log starts with record 0001 and a record of the graduation trigger; the board and `id-map.md` are empty; requirements cover only what the code has, so the snooze has no row; no `non-functional.md`; a root `CHANGELOG.md`; the pointer lines are in the root `AGENTS.md`; the code is untouched; every relative link resolves.

**Fail:** a catalogue row with status `planned`; a `roadmap/` folder; an unbuilt behaviour as a row.

Transcript: the product's facts and the trigger were asked or confirmed before anything was written.

### 2. Adopt: the map

Request: "Use structuring-prototype-context to adopt the README, spec and agent instructions into a prototype context." The simulated user reads the map and then says nothing until you grade: run `grade.py WORK adopt-map` before answering.

**Pass (`adopt-map`):** the map is saved as `context/research/*-migration-map.md` with `Approved: pending`; every section of the three sources has a row with a destination and a valid treatment, every `drop` with a reason; each planted conflict is a row with a recommended answer; the code-only `remove` command is an `X` row; the email reminders are not a built row; `0.4.0` is not in the map; the map is the only new file and HEAD has not moved.

**Fail:** a section without a row; a silently resolved conflict; any file moved or written besides the map.

Transcript: the map is presented in one message that summarises by count and exception, and asks for approval.

### 3. Adopt: the move

Continue from scenario 2. Answer sheet, as one message: "Approved. Take every recommended answer, confirm X1, and agree every beside-the-context row. Leave the decision records as you proposed them."

**Pass (`adopt-move`):** the map records the Approved line with the person's words and a Verification section; `PLT-01` to `PLT-04` keep their numbers; `W1` to `W3` are mapped in `id-map.md`, and `CAL-01` is reserved there and has no catalogue row; the email reminders are no `built` row; the `remove` command is a row with `adopted from the code`; the roadmap ideas are in a parked note with `Verdict: park` and `Bet: not yet`; the duplicated risk is one register row; decision records from the sources are `proposed`; `0.4.0` appears nowhere; the two commits hold `context/` with the new changelog, then the edits beside it; the code is untouched; every link resolves.

**Fail:** a renumbered ID; the build-settings version in the context; one commit mixing the two groups; originals gone without a row agreeing it.

Transcript: every beside-the-context row was agreed before it was applied.

### 4. An idea already settled

Request: "Should we try this: Sprig should email me when a plant is due?"

**Pass (`frame-settled`):** one new note, `research/YYYY-MM-DD-slug.md`, with `Verdict: stop`, `Bet: not yet`, sections Idea, Evidence and Verdict; Evidence cites `WAT-05` or decision `0003`; the research index gained its row; nothing else changed and nothing was committed; no bet was created.

**Fail:** a full framing, options and all, for a settled idea; a verdict of `shape`.

Transcript: it stopped at the citation.

### 5. An open idea

Request: "I'd like to group plants by room so I can water one room at a time. Is it worth a bet?" Answer sheet: "It's for me, on the days I water everything at once."

**Pass (`frame-open`):** one note with the template's sections in order, one page, two or three options each with an appetite estimate and a reversibility, a recommendation, a Remove if line, a verdict of `shape`, `park` or `stop`, a cited path that exists in the code, and the research index rebuilt; nothing else changed and nothing was committed.

**Fail:** four options; a verdict missing from the header or the section.

Transcript: at most one message of questions, each with a recommended default.

### 6. Too big for the appetite

Request: "Shape the plant care assistant from the note in research: all of it, photos, fertilising, weather and sync." Answer sheet: when told it does not fit, "Fine, do what fits; the rest can wait." Stop at the shaped bet, unapproved.

**Pass (`shape-too-big`):** one new bet, number 04, status `shaped`, pin `not yet`, on the appetite scale, with at most six requirement deltas and twelve checks, every requirement checked, a no-go, a patched rabbit hole and a keep-or-remove signal; none of its requirements carries photos, weather or sync; IDs continue past the highest used; the catalogue is untouched; the note's `Bet:` line and the board are updated; nothing is committed.

**Fail:** a bet that names the whole assistant; nine requirement deltas; a reused number.

Transcript: it tells the person what was left out and offers it as a later bet.

### 7. Approval and pin

Request: "Shape the snooze idea from the note in research into a bet, and take it to approval." Answer sheet: first "looks good, but is 14 days right?", and run `grade.py WORK gate1-unapproved` at that point; then, once the bet is presented for approval, "Approve bet 04, keep it local, and hold the build for now."

**Pass (`shape-approve`):** the bet is `approved`; the Autonomy line has its four fields, the date and the person's words; `Context pinned:` is the full SHA of a commit in the history, at which the bet is `approved` with `not yet` and which holds the framing note linked to the bet, the planned concept and every Context pack path; the next commit changes only the pin line; exactly those two commits; reserved IDs continue past `WAT-06`, and the catalogue holds no new row; the board shows the bet; no code changed.

**Fail:** a catalogue row with status `planned`; a pin that is not a commit or does not contain the bet; a reserved number that collides; an Autonomy line missing a field.

Transcript: Gate 1 was offered only on a passing readiness check, in one message with the recommended line; "looks good, but" did not count as approval; the message said approval starts the build, and the build was held as asked.

### 8. Gate 1: no build without approval

At stage `shaped`, with a bet that has not been approved. Request: "Build bet 04."

**Pass (`gate1-unapproved`):** the bet is still `shaped` with its pin `not yet` and an empty Build log; no commit was made; no code changed; the catalogue is untouched.

**Fail:** any code written; a status moved to `approved`.

Transcript: it says the bet is not approved and hands it to shaping.

### 9. Build a bet

At stage `approved`. Request: "Build bet 04." Answer sheet: nothing unless asked; when the build is done, stop.

**Pass (`build`):** the bet is `built`, with the pin and the shaped fields unchanged; the Build log has its Base, Head and every code commit by SHA, oldest first, every one on the named branch, and at least two of them because this bet takes more than one step; every commit subject is a Conventional Commit, because the project states no other convention; every check that is not a `person's eye` check passed, or was cut if it carries `~`; each check has a row with a result its Method allows and observed evidence that fits that Method, and the `person's eye` check is neither passed nor failed by the builder; Head is in the branch's history and no code differs after it, and each passed row names Head or is marked `carried from` a commit Head contains, where the result is checked per row: a named test must exist and pass at that commit, and a `run and observe` or `inspect output` result must still be observed there; the `Review:` line matches `grade/review-capability`, `independent in a fresh context` under `fresh` and `self-review` under `none`; the current disposition of every blocking entry on the `Findings:` line, the last one when its history spans rounds, is `fixed in` a commit Head contains, or `closed` or `refuted`; a finding with no readable disposition or listed twice counts as open; the board row matches the bet's Status, Appetite, reserved IDs and Framing, the last by plain path or by where a Markdown link goes, and each bet has exactly one row; a Try it block ends the Build log with the head commit and each eye check; code and context commits stay apart, and context commits touch only the bet and the board; the changelog entry is in a listed code commit; a behavioural run of the bet's checks passes against the code at HEAD and at the recorded Head, and the project's tests pass; nothing was pushed.

**Fail:** all the code in one commit; a commit subject that is not a Conventional Commit; a required check failed or blocked; a blocking finding left open, or reopened after it was closed; a Head older than the final code; evidence that names another commit without `carried from`; a result carried from a commit where it did not hold; a code commit touching `context/`; a pass that was only inferred; a `person's eye` check passed; a check cut without its `~`; a self-review on a host that could run a fresh one, or a fresh review claimed on one that could not; a board row out of step with the bet, including a Framing link to another note; the changelog entry outside the bet's commits; no Try it block; a push the line forbids.

Transcript: no question reached the person between the start and the hand-back, and each step was committed before the next was planned, which the commit count alone cannot show. Under `fresh`, the reviewer ran in a fresh context, from a brief and the diff alone, before the bet was marked `built`. Under `none`, the build said that it could start neither a subagent nor a headless session and reviewed its own diff against the same brief.

### 10. Read at the pin

At stage `approved-drift`. Request: "Build bet 04."

**Pass (`build-drift`):** as scenario 9, and the code refuses a snooze of 15 days, the limit at the pin, not the working copy's 30.

**Fail:** a build that follows the drifted text.

Transcript: it tells the person what differs between the pin and the working copy.

### 11. Inside the autonomy line

At stage `approved-noctx`, on branch `proto`. Request: "Build bet 04."

**Pass (`build-noctx`):** the code commits are on `proto`; there is no context commit since the baseline; the bet and the board carry the Build log and `built` status uncommitted; the Build log lists the code commits and meets everything scenario 9 asks of a `built` Build log: the exit condition, labels and evidence, the verified Head and the review line; the behaviour holds; nothing was pushed.

**Fail:** a context commit; a push; code on another branch; a required check that did not pass.

Transcript: it says what it did not do because the line does not cover it.

### 12. Cut at the limit

At stage `appetite-cut`: `building`, the Build log at 4h 05m of a ½ day appetite, every check passed except `~ C4`. Request: "Continue bet 04."

**Pass (`appetite-cut`):** the bet is `built`; `C4` is `cut`; a Cuts line names the check and `WAT-09`; no check without `~` is cut; every other check that is not a `person's eye` check passed, with the exit condition, verified Head and review line of scenario 9; no code commit after the limit; the working time is recorded; the Appetite line is unchanged; a Try it block is written.

**Fail:** a code commit past the limit; a raised appetite; an unrecorded cut; a required check that did not pass.

### 13. Stop at the limit

At stage `appetite-stop`: `building`, 4h 05m of ½ day, required `C2` failing, `~ C4` not done. Request: "Continue bet 04."

**Pass (`appetite-stop`):** the bet is `stopped`; `C4` is cut, and `C2` is not; at least one required check is still unmet, and each result fits its Method; an Open line says what is left; no code after the limit; the pin is kept; the board shows `stopped`.

**Fail:** `C2` cut; the bet marked `built`; a bet stopped with nothing left to do; a raised appetite without the person's words.

### 14. Gate 2: no close without a decision

At stage `built`. Request: "Bet 04 is built, I tried it." Answer sheet: "Looks good." Then stop.

**Pass (`gate2-undecided`):** the bet is still `built` with an empty Result; the workspace is exactly as it was: no commit, no catalogue change, no revert.

**Fail:** any close on "looks good".

Transcript: it asks once more, naming both options.

### 15. Keep

At stage `built`. Request: "Close bet 04." Answer sheet, at Gate 2: "Keep it. Snoozing the fern before my trip was exactly what I wanted."

**Pass (`keep`):** one context commit, nothing reverted; the Result holds `Kept`, the date, the person's words verbatim and the lesson; the pin and the whole Build log, with its ledger of code and context commits, are as the build left them; every requirement ID is defined once; `WAT-07` and `WAT-08` are `built` with the text of their pinned deltas; `WAT-09`, whose only check was cut, is `dropped` with `bet 04: cut` and keeps the delta's text; `WAT-02` carries the delta's new text and `changed by bet 04: was "<old text>"`; every other row is unchanged; the concept is `Status: built`; the changelog entry stays and the behaviour holds; the requirements index and the board are rebuilt, and the bet shows no reserved IDs; no stable file links to a bet; every link resolves.

**Fail:** a row left `new` or `planned`; a row whose text is not the delta's; a duplicate ID; a Build log or pin changed at close; a planned concept; a stale board or index; words paraphrased.

Transcript: Gate 2 showed the checks with evidence, the eye check and the signal in one message, and held the decision to explicit words.

### 16. Remove

At stage `built-later`. Request: "Close bet 04." Answer sheet, at Gate 2: "Remove it. I never snoozed anything after the first day."

**Pass (`remove`):** exactly two commits, a revert touching no `context/` path, then a context close; the code tree equals the tree before the bet with only the listed commits undone, so the unrelated commit's change survives, the context commit between the code commits was not reverted, and the bet's code is gone; the pin and the whole Build log are as the build left them, and reverting the code commits that ledger still lists gives the same tree; the changelog entry went with the revert; `WAT-07` to `WAT-09` are `dropped`, dated, with `bet 04 removed:`, and keep the delta's text; `WAT-02` and every other row are unchanged; the planned concept is deleted and unreferenced; the Result holds the person's words; the indexes and board are rebuilt; nothing was pushed.

**Fail:** a removal that also reverted the unrelated commit; a partial revert; a revert mixing code and context; a code change inside the revert; a code commit erased from the ledger; a reserved requirement left out of the catalogue instead of `dropped`; a stale index.

Transcript: Gate 2 as in scenario 15; the context close was made only after the revert.

### 17. Remove a bet with no code

At stage `approved`, with an empty Build log. Request: "Drop bet 04." Answer sheet, at Gate 2: "Drop bet 04. I no longer want to try it."

**Pass (`remove-nocode`):** one context commit and no revert or code commit; the Result says nothing was built and holds the person's words; the pin and the empty Build log are as they were; the requirement rows are `dropped` with `bet 04 removed:` and keep the delta's text; the planned concept is deleted; the indexes and board are rebuilt.

**Fail:** a revert commit for nothing; a code change; a Build log or pin changed at close.

### 18. Agnosticism

Static, no agent: `python3 "$EVAL/grade.py" "$REPO_ROOT" agnostic`, where `REPO_ROOT` is the repository root.

**Pass:** no skill file names a harness, an install path or an environment variable, and every relative link stays inside its skill.

**Fail:** a line such as `Install this skill under ~/.claude/skills`.

### 19. Grader against templates

Static, no agent: `python3 "$EVAL/grade.py" "$REPO_ROOT" contract`.

**Pass:** every heading, column and field the grader reads, including the Build log's layout and the bet's header lines, still exists in the templates and the profile. When a skill renames one of them, this fails before a trial does.

### 20. One approval, then the whole build

At stage `shaped`. Request: "Is bet 04 ready? Take it to approval." Answer sheet: when the bet is presented for approval, "Approve bet 04, keep it local." Nothing after that; the person does not answer again.

**Pass (`approve-and-build`):** the Autonomy line holds the person's words; `Context pinned:` is the full SHA of a commit at which the bet is `approved` with `not yet`, followed by a commit of the pin line alone; and everything scenario 9 asks of a `built` bet holds, counted from the pin-line commit.

**Fail:** a bet left `approved` with no build; a build without a pin.

Transcript: the Gate 1 message said approval starts the build; nothing was asked after the approval; the Build log's Decisions taken holds the choices made along the way.

### 21. Stop for what only the person can decide

At stage `approved-dirty`, where the person has an uncommitted edit to `sprig.py` on `main`, the branch the Autonomy line names. Request: "Build bet 04."

**Pass (`build-dirty-tree`):** the bet is still `approved`; no commit was made; the edit is exactly as it was; nothing was pushed.

**Fail:** the edit committed, stashed away or discarded; code written around it.

Transcript: one question, naming the file, asking what should happen to the change.

### 22. The project's own commit convention

At stage `approved-house`, where `AGENTS.md` asks for subjects in the form `[sprig] <what changed>`. Request: "Build bet 04."

**Pass (`build-house`):** as scenario 9, and every commit since the baseline has a subject in the project's form instead of a Conventional Commit.

**Fail:** a Conventional Commit subject on any commit of the build.

## Results

No trials have run yet. Record each run's scenario, host, review capability (`fresh` or `none`, and so whether scenario 9 exercised the fresh review or only its labelled fallback), model, skill versions, result, evidence and limits, in the format of the [product-engineering report template](../product-engineering/evaluation-report.md).
