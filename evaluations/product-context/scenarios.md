# Scenario catalog: product-context

Maintainers' catalog of behavioral trials for the six `product-context` skills, from [`structuring-product-context`](../../skills/product-context/structuring-product-context/SKILL.md) to [`reconciling-product-context`](../../skills/product-context/reconciling-product-context/SKILL.md). Use it when changing the skills or validating them on a new host, not during product work. The hand-off into the implementation loop is graded from the other side in the [`product-engineering` catalog](../product-engineering/evaluation-scenarios.md), scenarios 18 to 23.

## Method

- **Isolated workspaces.** Run each trial in a temporary directory with its own git repositories: a context repository, and for scenarios 6 and 7 a code repository next to it. Use the fictional product below and synthetic data only.
- **Hidden answer keys.** Give the executing agent the workspace, the installed skills and the request. Never give it this catalog or the planted conflicts and faults listed under each scenario.
- **Simulated user.** A separate agent answers from a hidden answer sheet: it approves maps and slates when they meet the scenario's key, and otherwise asks for the missing item. Record it as a simulation.
- **Outcomes over phrases.** Grade the files written, their IDs, statuses and links, the commits made, and what was left untouched, such as the code repository in scenario 7. Matching headings does not show that the repository stays coherent.
- **Honest scope.** Record the host, the model and the skill versions with each run. Repeat scenarios 1, 4 and 5 at least three times and report pass rates. No trials have run yet.

### Common setup

```bash
WORK=$(mktemp -d)
mkdir -p "$WORK/acme-context" "$WORK/acme" && git -C "$WORK/acme-context" init -q -b main && git -C "$WORK/acme" init -q -b main
```

The fictional product is Tally, a shared household expense tracker with a web app and an API. Its sources, written by the grader into `$WORK/acme-context` before each adopt trial:

- `tally-prd.md`: about 30 sections. Summary, assumptions, actors and use cases, 24 requirements in three capabilities (`EXP-` expenses, `SPL-` splitting, `SET-` settling up), eight non-functional requirements, a container diagram, two sequence diagrams, a state machine for an expense, nine "key decisions" in a table, risks, open questions, a roadmap of V1 and V2, and a list of sources.
- `tally-v1.md`: V1 scope, four milestones with exit criteria, a requirement-to-milestone table, six ADRs to write before code, V1 risks and questions.
- `tally-v2.md`: V2 scope, three milestones, V2 risks and questions.

Planted, and listed only in the answer key:

- two of the PRD's risks repeated in `tally-v1.md`;
- the same open question in all three files;
- the nine key decisions and the six ADRs overlapping under different numbers;
- milestone 1.2 promising "a weekly summary email" that no requirement covers;
- the V1 requirement table counting 19 requirements where the rows give 18.

## Scenarios

| # | Scenario | Skills under test | Needs |
|---|---|---|---|
| 1 | Adopt over-stuffed documents | `structuring-product-context` | The three sources, simulated user |
| 2 | Create from nothing | `structuring-product-context` | An empty context repository |
| 3 | Integrate a design handoff | `curating-product-requirements` | The result of 1, a product/design handoff with local IDs |
| 4 | Architecture baseline | `designing-system-architecture` | The result of 1 or 3, simulated user |
| 5 | Shape a milestone | `shaping-bets` | The result of 4, one contract left `proposed` |
| 6 | Hand off a bet | `shaping-bets` | A ready bet, a committed context repository, the code repository next to it |
| 7 | Close a bet | `reconciling-product-context` | A code repository holding the loop's artifacts and simulated merged pull requests |
| 8 | Drift audit | `reconciling-product-context` | A context repository with seeded faults |
| 9 | Agnosticism | all six | The skill files |

### 1. Adopt over-stuffed documents

Request: "Use structuring-product-context to adopt the three Tally documents into this repository."

**Pass:**
- Before any file moves, one message holds the map: every section of the three sources has one row with a destination and a treatment, and every drop has a reason.
- Every planted conflict appears: the duplicated risks and question are merged into one register row each; the decision numbering, the uncovered weekly email and the wrong count each become an open question with a recommended answer.
- Nothing is written before the simulated user approves. After approval, the layers exist; every requirement and NFR ID is unchanged, and each ID table's row count equals its source's; decisions are separate records, accepted only where the sources state them as made; every relative link resolves.
- The map is saved under `research/`, and the originals are removed in the same commit only after the user confirms.

**Fail:** a section without a row; a silently resolved conflict; any write before approval; a renumbered ID; a fact kept in two files; originals deleted without git history.

### 2. Create from nothing

Request: "Set up a product context repository for Tally, a shared household expense tracker. The code will live in `acme`."

**Pass:** the skeleton follows the layers; `AGENTS.md` is a table of contents of about 100 lines with the map, the reading order per task, the house rules and the code repository; the folder indexes exist; the decision log starts with record 0001 and is linked from `AGENTS.md`; the product layer is left to `curating-product-requirements`, or a rough idea is routed to `shaping-product-briefs`. The report says the first bet cannot be handed off until the repository has a commit.

**Fail:** invented requirements, architecture or decisions; an `AGENTS.md` that explains the product instead of mapping the repository.

### 3. Integrate a design handoff

Give a product/design handoff for "split by percentage" with local IDs `R1` to `R4`, where `R2` duplicates `SPL-03` and `R4` contradicts an accepted decision.

**Pass:** `R1` and `R3` become new `SPL-` rows with the next free numbers; `R2` maps to `SPL-03` without a new row; `R4` is raised with a recommended default and not written; the mapping is appended to `product/requirements/id-map.md`; new terms reach the glossary; no acceptance criteria are written into the catalogue; the requirements index is rebuilt, not hand-edited.

**Fail:** a duplicate row, a reused or renumbered ID, a contradiction resolved silently, criteria in the catalogue.

### 4. Architecture baseline

Request: "Use designing-system-architecture to write the baseline before we shape V1's bets."

**Pass:** C4 levels 1 and 2 cover every person, external system, container and store, with the protocol on every arrow; every section carries `Since:` and `Status:` lines; the interface between the web app and the API is named, and its contract is left to contract mode when the first milestone is shaped; the decisions that precede code are records through `decision-records`, accepted only with the user's words; `ecosystem.md` lists dependencies with verified-on dates; the report says when the baseline is enough, by the version's requirements and containers. No section designs files, classes or functions. Variant: "write the contract for the web app and the API" produces a contract with operations, invariants, errors and versioning, with `Version: 1.0 proposed` until the user agrees.

**Fail:** a contract written as code; an untagged section; a contract or decision accepted without the user's words; a contract that names the bets building it; a V2 element designed beyond C4 level 2.

### 5. Shape a milestone

Request: "Use shaping-bets to shape milestone 1.1." The milestone has nine requirements; one of them depends on a contract left `proposed`.

**Pass:**
- The slate covers each of the nine requirements exactly once, with partial coverage named; every bet is M or L, and none is cut by layer.
- Each bet file follows the template: outcome, requirement IDs only, observable criteria naming their requirement, no-gos, rabbit holes, `~` marks, architecture lines, a context pack of five to ten entries.
- Bet numbers continue after the highest used; the board is rebuilt from the bet files.
- The bet that consumes the `proposed` contract fails readiness, and the report names `designing-system-architecture` as the fix.

**Fail:** a requirement covered twice or not at all; requirement text copied into a bet; a criterion nobody can observe; a bet made ready with a `proposed` contract.

### 6. Hand off a bet

Request: "Hand off bet 05."

**Pass:** the bet's final text is committed before the pin; `Context pinned:` holds the full SHA of that commit; Status, Context pinned and Handoff are written in a second commit; the Handoff holds the date, the code repository, the work-item slug equal to the bet's file name, and the kickoff line with that SHA; the code repository is untouched. With an uncommitted change in a context-pack file, the handoff stops and says why.

**Fail:** a pin that does not contain the bet; a local checkout path committed into the bet; any write in the code repository.

### 7. Close a bet

The grader writes into the code repository the artifacts a finished loop leaves: `docs/product-engineering/05-<slug>/spec.md` with a `Source: bet …` line, an `AC-E1`, and one `~` criterion marked `cut (… "<words>")`; `roadmap.md` with an `Appetite (bet):` line and a Decisions entry for the cut; plan files with `Branch:` lines; one implementation decision record that settles a detail the bet's produced contract left open. Merged pull requests and their verification reports are simulated as files the agent is told to read in place of the host, and recorded as a simulation.

Request: "Use reconciling-product-context: bet 05 is merged."

**Pass:**
- The code repository is unchanged: `git -C "$WORK/acme" status --porcelain` is empty and its HEAD did not move.
- The criteria table lists every bet criterion and `AC-E1` with the pull request and short SHA, and the cut criterion with the user's words; the bet becomes `built`, then `done`.
- The requirements become `built`, except one covered only in part; the contract gains the settled detail and a minor version, citing the record by repository name and path; promoting `AC-E1` into the catalogue is proposed and waits for a yes.
- The outcome log follows the template, and the board, coverage and counts are rebuilt.

**Fail:** a write in the code repository; a criterion marked observed without a merged report; a promotion written without the user's yes; a local path in a committed link.

### 8. Drift audit

Seed one each: a broken relative link, two requirements with the same ID, a requirement owned by two bets, a milestone requirement owned by none, a hand-edited bet board that disagrees with a bet file, a verified-on date older than the repository's limit, a fact stated in two files, and an architecture file that links to a bet.

Request: "Audit the docs."

**Pass:** all eight are found and ranked; the link, the board and the counts are fixed in place; the duplicate ID, the double and missing ownership, the duplicated fact and the volatile link are reported as questions; every check that could not run is named.

**Fail:** a missed fault; a substantive fix made without asking.

### 9. Agnosticism

Static, no agent:

```bash
grep -rniwE '<names of the author’s own products and their parts>' skills/product-context
```

**Pass:** no match, and every example uses a fictional product.

## Results

No trials have run yet. Record each run's scenario, host, model, skill versions, result, evidence and limits, in the format of the [product-engineering report template](../product-engineering/evaluation-report.md).
