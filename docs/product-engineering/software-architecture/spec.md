# Spec: software-architecture, a plugin of five skills for working on the architecture of long-lived applications

Status: agreed (G1, 2026-11-17: "G1 agreed")
Track: feature
Source: the agreed design `specifications/software-architecture/spec.md` in the main checkout (untracked; agreed by Igor on 2026-11-17, LOG D16 and D17), with `plan.md` (requirements R1 to R6 of the idea), `LOG.md` (decisions D1 to D18) and `research/findings-fit.md` section 5.2 (the checklist for adding a category) beside it. The agreed design and the checklist name the decision record 0021; `main` took that number for `dev-environment` on 2026-11-17, so this work item's record is 0022. "Agreed spec §N" below means section N of that file; "checklist N" means step N of section 5.2.

## Problem

Agents working on a long-lived application have no skills in this marketplace for its architecture outside a product context repository. `designing-system-architecture` (product-context) writes the architecture of a planned product inside a context repository, and `brainstorming-solutions` (product-engineering) chooses how to build one work item. Nothing recovers what an existing application really is, takes a critical look at it, compares system-level options, or simplifies it, and nothing gives other people a way to look at the result without installing a diagram tool (idea requirement R6).

Igor will use the plugin on his own applications first and then with clients, so every skill must work in any repository with no other plugin installed (D5).

Outcome: a new category `skills/software-architecture/` with five skills. The architecture lives in Markdown files with Mermaid diagrams, which are the source of truth (D6, D12). People look at it through one built HTML file (D9, D10, D13). The plugin is released as `software-architecture` 0.1.0 together with the patch releases of the plugins it touches.

## Requirements

The plugin (agreed spec §1; checklist 2, 4)
- R1: A category `skills/software-architecture/` holds five skills: `recovering-built-architecture`, `evaluating-architecture-risks`, `exploring-architecture-options`, `simplifying-system-architecture` and `drawing-architecture-views`. Each works in any repository with no other plugin installed, and each is self-contained as `AGENTS.md` requires.
- R2: There is no coordinator skill. Each skill ends with a report that states what was written, what is uncertain, and which skill fits next. Without file access a skill returns the Markdown and says nothing was written.

Where the work lives (agreed spec §2)
- R3: Location rule. A skill reads the repository's `AGENTS.md` or `CLAUDE.md`; where it points to an architecture folder and a decision log, the skill uses them; where it points nowhere, it uses `context/architecture/` and `context/decisions/`. The skills commit nothing; the person commits.
- R4: When the plugin creates the folder itself, the tree is: `README.md` (the index of every standing view and study, by link, with status), `architecture.html`, one Markdown file per standing view, and `studies/YYYY-MM-DD-<slug>/` with a `README.md` and the views that belong to that study only. With nothing found, the skill also proposes one pointer line for the root `AGENTS.md`.
- R5: Standing views describe the system, built or accepted and not yet built. A study is a dated piece of thinking and never edits a standing view. When a study's outcome is accepted, the standing views are updated as a separate step and the study stays as the record.
- R6: Inside a context that already exists: in a prototype context (`context/AGENTS.md`) a skill follows its map, view template and index rules, and puts studies in `architecture/studies/`; for a product context repository it writes no standing view there and hands the study over as input to `designing-system-architecture`; in an existing architecture folder that `AGENTS.md` points to, it keeps the file names and adds `studies/` and the HTML file.

The view format (agreed spec §3)
- R7: One view per Markdown file, in this shape: title; a `Status:` line; two or three sentences on the question the view answers, for whom, at what level; one fenced Mermaid block; one or two sentences for what the picture cannot show; an Elements table (Id, Element, Responsibility, Technology, Status, Evidence); a Relationships table (From, To, What flows, Evidence); Related. The shape matches the view template of `structuring-prototype-context`, with the evidence column and the verified line added.
- R8: Status is `built` or `planned` on standing views and `proposed` only inside a study. `Verified:` with a date and a commit is written only by a skill that checked the view against the code. An element keeps one Mermaid node id in every view and study, and risks, matrices and notes refer to elements by id. Evidence is a repository path, optionally with a line, or `stated by <person>, <date>`; an element with neither is marked `assumed`.
- R9: Diagram choice. The view sentence comes first ("This view helps *audience* answer *question* about *scope* in *state*."), then the highest level that shows the disputed fact, then the concern, from seven defaults: context, containers, sequence, deployment, data flow, state machine, module graph. One view first; a second only for a question the first leaves open.
- R10: No board format (D11). Options against criteria are a table; clusters a Mermaid mindmap or a flowchart with subgraphs; forces a quadrant chart with short labels; before and after are two views compared in the HTML file.
- R11: Mermaid subset: `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`, `mindmap`, `quadrantChart`. C4 views are `flowchart` with styled nodes. Every label is quoted wherever the diagram type takes a quoted string; sequence diagram text (participants, messages, notes), state transition labels and a quadrant chart's title stay bare, because Mermaid draws their quotes literally (settled by Igor at G4, 2026-11-17, in place of the agreed spec's "every label quoted"). A view has at most 12 to 15 elements; a larger system is split by concern or level. The label form the conventions prescribe draws on GitHub as well as in the HTML file.

The HTML file (agreed spec §4)
- R12: One file, `architecture.html`, beside the index, holds a copy of every standing view and study and draws them in a current browser. The Markdown files stay the source of truth.
- R13: The agent never writes the HTML by hand. It copies `templates/architecture.html` once and afterwards changes only the source blocks, one per Markdown file, each between two marker lines.
- R14: Mermaid loads from one pinned CDN address with an exact version, set in one line of the template. With no network the file says so and shows the sources as text.
- R15: The file states in its header when it was built and from which commit.
- R16: A reader can switch between views, grouped as standing views and studies; pan, zoom, fit and go full screen; use light and dark; compare any two views side by side, through a link form that a study's text can use; and read prose, tables, lists and links between views as formatted text.
- R17: A Save offline copy button writes a second file that carries the drawn pictures and no library. That file opens with no network, keeps the theme it was saved in, and keeps pan and zoom. A person makes it in a browser; it is not committed (O4).
- R18: Build and rebuild. First build: copy the template and insert one block per file listed in the index. Rebuild: replace the blocks of changed files, add blocks for new files, remove blocks for deleted files, update the built stamp; where a shell is available, assemble the blocks with a command. Any skill run that adds or changes a view or a study rebuilds the file before it reports; a skill that cannot says the file is out of date.
- R19: The template writes `PASS name`, `FAIL name: detail` and `DONE passed/total` as text into the page, the form decision 0017 uses. Where the harness can open a browser the skill reads those lines; where it cannot, it says the views were not drawn and asks the person to open the file.

The shared intake (agreed spec §5)
- R20: Before any judgement, `evaluating-architecture-risks`, `exploring-architecture-options` and `simplifying-system-architecture` write at the top of the study: the real question, restated without the solution the person named; three to five priority scenarios with six fields each (source, stimulus, environment, the part affected, response, measure); hard constraints; facts, assumptions and proposals kept apart, each fact with evidence and each assumption with what would confirm it; and what is already decided, read from the decision log and the standing views. The skill asks the person only for what the repository cannot answer, in one message.

The skills (agreed spec §6, §7)
- R21: Every skill follows the location rule, reads `AGENTS.md`, the decision log and the standing views before writing, writes in the view format, and rebuilds the HTML file (R18).
- R22: `recovering-built-architecture` answers "what is really there?". It reads manifests, entry points, configuration, infrastructure files and schema; lists deployable units and stores, then the calls between them; separates what the code shows statically, what configuration says about deployment, and what only runtime could confirm; and draws context and containers, plus one runtime view only for a flow the person names. It leaves standing views with `Status: built`, a `Verified:` line, evidence on every element and relationship, and a "Blind spots" list. It trusts what the code does over what a folder is called. It writes no decision record for an inferred decision.
- R23: `evaluating-architecture-risks` answers "take a critical look". It runs the intake, traces each priority scenario through the views element by element, then looks for what the scenarios miss (single points of failure, each dependency slow or down, trust boundaries crossed by sensitive data, a short premortem), and ranks by likelihood and impact. It leaves a study from `templates/risk-review.md`: a verdict per scenario (met, at risk, unknown), risks pinned to element ids with cause and evidence, trade-off points, the next check for each top risk, one annotated view, and a failure sequence where order matters. "The problem does not need an architecture change" is a valid finding.
- R24: `exploring-architecture-options` answers "what are our options?" and covers a new system. It runs the intake, checks what the code and the decision log already settle, researches prior art where the harness can search, and sketches two or three options that differ in kind, each as a `proposed` view at the same level with shared element ids; one option is the smallest change that could work. It leaves a study from `templates/options.md`: one view per option, a matrix of options against scenarios and constraints with a sentence per cell and no score, a recommendation, what would reverse it, and what was not checked. Gate Pick: the person chooses in their own words; the choice is recorded in the study with its date and the skill offers a decision record. Silence is not a pick; the study then states that the choice is waiting.
- R25: `simplifying-system-architecture` answers "can this be simpler?". It runs the intake, with the scenarios as the guarantees to keep; asks of each component, hop, store and technology what breaks if it is removed or merged; names the guarantee each provides; proposes only removals and merges that keep every guarantee; re-traces every scenario through the result; and counts where the complexity went. It leaves a study from `templates/simplification.md`: before and after views with the same ids, a row per scenario and constraint showing it still holds and why, each removed mechanism with the guarantee it gave and where that guarantee now lives, and what must be measured first. "Nothing should change" is a valid result, stated with its reasons. Gate Accept: the person accepts, narrows or declines; accepted changes are offered as a decision record and the standing views show them as `planned`.
- R26: `drawing-architecture-views` answers "draw this", "explain this to X" and "rebuild the page", and the other four use it for the build step. It states the view sentence, picks the view, writes or updates the view file and the index, builds or rebuilds `architecture.html`, and reads the check lines. For an audience request it chooses the two or three existing views that answer that audience's question and writes a short guide to them as a study.
- R27: Each of the other four skills carries one line for a missing sibling: without `drawing-architecture-views`, write the views in Markdown, say the HTML file was not rebuilt, and name the skill that rebuilds it.
- R28: The skills share one vocabulary (view format, element ids, scenarios) and state the usual order: on an existing app recover, evaluate, simplify or explore, decision record, standing views updated; on a new system explore, evaluate the chosen option, draw the standing views as `planned`. Each also stands alone: evaluating without prior recovery works on the views that exist and lists what it had to assume.
- R29: Each skill states its boundary with its neighbours, and no two skills claim the same request: recovering is not for a product context repository's baseline (`designing-system-architecture`); evaluating is not for reviewing a code change (`reviewing-code-changes`) or a full security assessment; exploring is not for choosing how to build one work item (`brainstorming-solutions`) or a prototype idea (`framing-prototype-ideas`); simplifying is not for refactoring code inside one module; drawing is not for UI prototypes (`building-html-prototypes`) or data modelling.

References, templates and mirrors (agreed spec §6, §8; checklist 8)
- R30: Each skill carries the files the agreed spec names, with the content it names:
  - recovering: `references/reading-a-codebase.md` (where structure hides per stack, static against runtime evidence, folder names that mislead);
  - evaluating: `references/review-methods.md` (scenario tracing, premortem, failure modes per dependency, trust boundaries), `references/scenario-intake.md`, `templates/risk-review.md`;
  - exploring: `references/designing-from-drivers.md` (deriving options from the scenarios, when a spike settles more than a comparison), `templates/options.md`;
  - simplifying: `references/subtraction.md` (essential against accidental complexity, the cost of each technology in operation, published cases and what does not transfer from them), `templates/simplification.md`;
  - drawing: `templates/architecture.html`, `templates/architecture-index.md`, `references/building-the-page.md` (first build, rebuild, reading the checks, the offline copy), `references/growing-into-a-model.md` (signs that hand-kept views are drifting, the LikeC4 route past roughly ten views).
- R31: `templates/view.md` and `references/view-conventions.md` have their source in `drawing-architecture-views` and a byte-identical copy in each of the other four. `references/scenario-intake.md` has its source in `evaluating-architecture-risks` and a copy in exploring and simplifying. Every pair is listed in `MIRRORS` in `scripts/validate.py` with the comment decision 0019 requires, and no mirrored file names a file of one skill only.

Changes outside the category (agreed spec §9; checklist 1, 3, 5, 6, 7)
- R32: `brainstorming-solutions` gains one sentence: system-level choices go to `exploring-architecture-options` when it is installed (D15).
- R33: `designing-system-architecture` gains one sentence naming the new plugin for work outside a product context repository.
- R34: The prototype profile's "Markdown only" rule gains one exception, the built `architecture/architecture.html` (O1), in its source and in every mirrored copy in `product-prototyping`.
- R35: Decision record `0022-software-architecture-category.md` records the category and its boundary, the skill list, the location rule, the view format, the HTML file with its CDN departure from the offline rule of `building-html-prototypes`, the mirrors, the convention that keeps the view template compatible with `structuring-prototype-context`'s without mirroring it, and the "Not for" pairs with `designing-system-architecture`, `brainstorming-solutions` and `framing-prototype-ideas`. `decisions/README.md` indexes it. No accepted record is rewritten.
- R36: `.claude-plugin/marketplace.json` has a `software-architecture` plugin entry with a user-facing description, `"version": "0.0.0"` until the release, `"source": "./"`, `"strict": false`, `"license": "MIT"`, the repository URL as `homepage`, keywords that say what the plugin is for, and the five skill paths.
- R37: `skills/software-architecture/CHANGELOG.md` exists in the house shape with one user-facing entry per skill. The root `CHANGELOG.md` lists the plugin, decision 0022 and the `MIRRORS` change, and names the new plugin changelog. The changelogs of `product-engineering`, `product-context` and `product-prototyping` each have an entry for their wording change.
- R38: The root `README.md` has the category row linking each skill's `SKILL.md`, the plugin in its changelog list, and a section for the plugin with a step, skill, output and gate table, a one-line install and example requests.

Format and release (checklist 11, 12; `AGENTS.md`)
- R39: Every `SKILL.md` has exactly `name`, `description` and `license` in its frontmatter, a description in the newer house pattern (what it does, concrete artifacts, "Use when the user says …", "Not for …"), fewer than 500 lines, and ends with a References table. Each skill name is free on skills.sh and in the ten widely installed packs the research inspected (`research/findings-methods.md`, "ten packs"). `python3 scripts/validate.py` reports no error and no warning.
- R40: The release commit comes last on the same branch and touches only the released changelogs and the matching versions: `software-architecture` 0.1.0, a patch release for each of `product-engineering`, `product-context` and `product-prototyping`, and a marketplace release with at least a minor bump, whose section lists the four plugins as `AGENTS.md` prescribes.

## Acceptance criteria

The plugin and its format
- AC1 (R1, R39): `python3 scripts/validate.py` in the worktree prints "0 errors, 0 warnings", and `skills/software-architecture/` holds exactly the five skill directories and `CHANGELOG.md`.
- AC2 (R1, R29, R39): Each of the five `SKILL.md` files has a description that names its artifacts, its "Use when the user says" phrases and a "Not for" clause with the neighbours R29 lists; `wc -l` gives fewer than 500 for each; each ends with a References table whose links all resolve inside the skill. A search of skills.sh and of the ten packs' repository trees returns no skill of any of the five names.
- AC3 (R30): Every file R30 names exists at its path, is linked from its skill's References table, and covers each topic R30 lists for it.
- AC4 (R31): Each of the ten mirror pairs is byte-identical (`cmp`), each is in `MIRRORS`, and the validator fails when one copy is changed by one byte and passes again when it is restored.
- AC5 (R1): A fresh-context agent given only one staged skill directory and a fixture completes that skill's task without reading any file outside its run folder (transcript scan `CLEAN`). Observed once per skill, in the trials of AC17 to AC26.

The HTML template, in a real browser
- AC6 (R12, R13, R18): An agent with a fresh context, given only `drawing-architecture-views` and the Larder fixture's Markdown views, produces `architecture.html` by copying the template and inserting blocks. A diff between the template and the result shows changes only between marker lines and in the built stamp.
- AC7 (R12, R19): Opened in Chrome with network, the built file writes one `PASS` line per view and study and `DONE n/n` with no `FAIL`, and a screenshot shows a drawn diagram with its prose and a formatted table.
- AC8 (R19): A source block with a Mermaid syntax error produces a `FAIL <name>: <detail>` line for that view, the `DONE` line counts it as not passed, and the other views still draw.
- AC9 (R16): The view switcher lists standing views and studies as two groups, and choosing an entry shows that view. Zoom, pan and fit each change the diagram's transform, read from the DOM before and after. The full-screen control is present and requests full screen.
- AC10 (R16): Light and dark each draw: after the theme switch, the page background and the diagram colours differ between two screenshots, and both are readable.
- AC11 (R16): Opening the file with the compare link form shows the two named views side by side, and a link in a study's text that uses the form opens the same comparison. A link from one view's prose to another view switches to it.
- AC12 (R14): The template contains exactly one external URL that is fetched, the Mermaid address with an exact version. Opened with the network refused, the file shows a message that the diagrams could not be drawn and shows each source as text, with no uncaught error.
- AC13 (R15): The header of the built file shows the build date and the short commit the agent stamped.
- AC14 (R17): Save offline copy produces a second file. That file contains no `<script src>`, no Mermaid library and no CDN address; opened with the network refused it makes zero requests, shows every picture, and switches views.
- AC15 (R17): In the offline copy, zoom and pan change the picture's transform, and a copy saved in dark shows dark pictures.
- AC16 (R18): After a rebuild in which one fixture view changed, one was added and one was deleted, the file has the changed block replaced, the new block present, the deleted block gone and a new stamp; it reports `DONE` with no `FAIL`.
- AC17 (R12, R16): The built file draws in Firefox with `DONE n/n` and no `FAIL`.
- AC18 (R11): A view file whose flowchart labels are quoted and use both `<b>` and `<br/>` renders on github.com as a diagram with bold text and line breaks in its labels. The conventions prescribe a label form only after it passes this check.

Each skill, tried by an agent with a fresh context on the Larder fixture
- AC19 (R3, R4, R21): In a fixture whose `AGENTS.md` points nowhere, the skill writes under `context/architecture/`, creates the index, and proposes the pointer line; in a fixture whose `AGENTS.md` names `docs/architecture`, it writes there and keeps the existing file names. In both, the agent creates no commit.
- AC20 (R7, R8, R22): Recovering leaves `context.md` and `containers.md` with `Status: built`, a `Verified:` line with date and commit, an Evidence cell on every element and relationship that is a real path in the fixture or `assumed`, and a "Blind spots" list.
- AC21 (R22): In the fixture, a folder whose name says one thing holds code that does another. The recovered views describe what the code does, cite the file as evidence, and note the misleading name.
- AC22 (R20, R23): Evaluating leaves a study in `studies/YYYY-MM-DD-<slug>/README.md` that opens with the intake (the question restated, three to five scenarios with all six fields, constraints, facts apart from assumptions), gives each scenario a verdict of met, at risk or unknown with reasoning, pins each risk to an element id that exists in the views, and names a next check for each top risk. No standing view is changed.
- AC23 (R24): Exploring leaves a study with two or three `proposed` views at the same level sharing element ids, one of them the smallest change, a matrix with a sentence per cell and no scores, a recommendation and what would reverse it. Given no answer from the person, the study states that the choice is waiting and records no pick; given "go with B", it records the pick with the date and offers a decision record.
- AC24 (R25): Simplifying, asked whether the fixture's queue can go, finds that the queue provides the replay guarantee a scenario depends on, keeps it or shows where the guarantee would live, and does not propose a removal that breaks the guarantee.
- AC25 (R25): Simplifying on the fixture variant with a sound simple design reports that nothing should change, with its reasons, and proposes no change.
- AC26 (R25): When the person accepts a simplification, the study records the answer, a decision record is offered, and the standing views show the accepted change as `planned`; the study's own files are unchanged by that update.
- AC27 (R9, R26): Drawing, asked for one diagram, states the view sentence, writes one view file in the R7 shape, updates the index and rebuilds the HTML file. Asked to explain the architecture to a named audience, it writes a guide as a study that links two or three existing views and adds no new standing view.
- AC28 (R2, R27, R28): Each trial's final report states what was written, what is uncertain and the next skill. A trial of one of the other four with `drawing-architecture-views` absent ends with the views in Markdown, a statement that the HTML file was not rebuilt, and the name of the skill that rebuilds it.
- AC29 (R5, R6): In a fixture with a prototype context (`context/AGENTS.md`), a study lands in `architecture/studies/` and standing views use that context's statuses. Told that the architecture lives in a separate product context repository, the skill writes no standing view there and hands the study over as input for `designing-system-architecture`.
- AC30 (R10, R11): The views the trials write use only the six Mermaid diagram types, quote every label, and stay within 15 elements; options against criteria appear as a table.

Changes outside the category
- AC31 (R32, R33): `git diff main` shows one added sentence in `brainstorming-solutions/SKILL.md` naming `exploring-architecture-options`, and one in `designing-system-architecture/SKILL.md` naming the new plugin; neither skill links outside its own directory.
- AC32 (R34): The prototype profile and each of its mirrored copies in `product-prototyping` carry the same exception for `architecture/architecture.html`, and the validator's mirror check passes.
- AC33 (R35): `decisions/0022-software-architecture-category.md` has Status, Date, Context, Options, Decision and Consequences, covers every point R35 lists, and has a row in `decisions/README.md`. `git diff main -- decisions` changes no other record.
- AC34 (R36, R37, R38): `marketplace.json` lists the plugin with every field R36 names and five skill paths that match the disk; the four plugin changelogs and the root changelog carry the entries R37 names, under `[Unreleased]` before the release commit and in the released sections after it; the root README has the row, the changelog link and the plugin section.
- AC35 (R40): `git show --stat` of the release commit lists only `CHANGELOG.md` files and `.claude-plugin/marketplace.json`. Versions read: `software-architecture` 0.1.0, each of the three touched plugins one patch above its last release, and the marketplace one minor above 0.5.0, so 0.6.0, with the four plugins listed under "Plugins released with this version". The validator passes on that commit. The release workflow's checks that can run before a tag exists (tag-name parsing, the version match with `marketplace.json`, release-note extraction from each changelog, the marketplace section's plugin list and links) pass for each of the five tag names against the release commit. The workflow's own check that the tagged commit is on `main` runs when the tags are pushed, after the merge.
- AC36 (R18, R21): With the whole category staged, a skill other than `drawing-architecture-views` that writes a study also rebuilds `architecture.html`: the file holds a block for the new study and a new stamp, and reports `DONE` with no `FAIL`.
- AC37 (Done and review): An HTML overview is published as an artifact and its link is handed over with the pull request's. It shows: each skill with its request, output, references and templates, and a diagram of the handovers; screenshots of views drawn, compare, both themes and the offline copy; each change outside the category; each choice made where the agreed spec was silent and each departure from it; each acceptance criterion with its check, the evidence and the SHA it was observed on, and what was not verified; the review findings with their resolution; the versions released and what to look at before merging.

## Non-goals

- The second-wave skills `planning-architecture-evolution` and `checking-architecture-drift` (D7).
- A coordinator skill, and any script shipped in a skill. Decision 0021 (`dev-environment`, merged to `main` on 2026-11-17 while this work ran) now lets a skill ship bash scripts; this plugin ships none unless Igor decides otherwise (asked on 2026-11-17: a build script for the page).
- A board file format or a JSON Canvas export (D11); a terminal preview tool (D8).
- The HTML file with the Mermaid library inside (D13), and committing the offline copy (O4).
- One HTML file per study (O3).
- Changing the "Markdown only" rule of product context repositories (O1).
- A LikeC4 integration; `references/growing-into-a-model.md` describes the route and builds nothing.
- Mirroring the view template with `structuring-prototype-context`.
- A plugin README with rendered visuals (checklist 9) and committed evaluations (checklist 10): both go in a follow-up pull request (Igor, 2026-11-17: "1. a) 2. a)"). The follow-up's evaluations are written as an eval suite for `claude plugin eval`, the evals Anthropic released for testing whether skills work and trigger when they should (Igor, 2026-11-17).
- Pushing tags or merging before Igor confirms the merge.

## Constraints

- Skill format, layout, mirrors, commits and changelogs follow `AGENTS.md`; skills ship no executable scripts, and checks ship as browser-only HTML with inline, non-module JavaScript (decision 0017).
- No file in a skill contains a parent path or a harness-specific path (`scripts/validate.py`); skills are harness-neutral.
- Every skill is written for a reader that has only that skill, as positive directions with the reason attached (Igor, 2026-11-17).
- One PR slice: one plan with phases, the branch `feat/software-architecture`, one pull request that ends with the release commit (D18).
- The specifications folder is untracked and exists only in the main checkout; workers reach it by absolute path.
- Commit messages follow Conventional Commits with no AI attribution (`CLAUDE.md`).
- Where the agreed spec is silent, the orchestrator decides and records the choice for the overview. Where it is wrong or an implementation finding contradicts it, the point goes to Igor with a recommendation (Igor, 2026-11-17).
- Done and review: done is the pull request open with the review approved, the release commit added, and an HTML overview published as Igor's code review. Igor reads the overview instead of the diff, merges with a merge commit himself, and the tags are pushed after he confirms the merge.

## Assumptions and open questions

- Assumption: the template pins Mermaid 12.3.0, the version the lab tested. Basis: inferred from `research/viz-lab` and LOG 2026-11-17. If wrong: a newer version is pinned only after the same checks pass on it.
- Assumption: prose, tables, lists and links are formatted by a small renderer written inline in the template, so the Mermaid address stays the only external one. Basis: agreed spec §4 ("one pinned CDN address"). If wrong: a second pinned library is added and recorded in 0022.
- Assumption: the offline copy keeps a small inline script for switching views, pan and zoom, and carries no library. Basis: agreed spec §4 lists pan and zoom in the offline copy as to verify. If it cannot be done: the point goes to Igor.
- Assumption: `framing-prototype-ideas` gets no new sentence; the boundary is stated from the new skill's side and in 0022. Basis: agreed spec §9 names two sentences only. If wrong: one more wording line in the `product-prototyping` patch.
- Assumption: the marketplace entry sits after `product-prototyping`, with the repository URL as `homepage` while the plugin has no README. Basis: checklist 4.
- Assumption: all five skill names are free: the skills.sh search returned no skill of each name on 2026-11-17. Basis: checked. If one is taken before the merge: the name goes to Igor.
- Settled at G4 (Igor, 2026-11-17: "1a"): the quoting rule in R11. Observed in Chrome with Mermaid 12.3.0: a sequence diagram draws quotes literally around participant names, message text and notes, and a state diagram around transition labels; flowchart labels, state descriptions and ER relationship labels take quotes and draw without them.
- Assumption: the three items the agreed spec lists to verify (offline pan and zoom, Firefox, labels on GitHub) are acceptance criteria AC15, AC17 and AC18; how each is observed is settled at G3.
- Settled at G1 (Igor, 2026-11-17: "1. a) 2. a), but when it comes to the evaluations I'd like to follow the evals that Anthropic released"): the plugin README with visuals and the committed evaluations are a follow-up; see Non-goals.

## Approach

Chosen: the design in the agreed spec, as settled in `LOG.md` decisions D5 to D16. Recorded at G2 on 2026-11-17 from Igor's instruction: "The approach is chosen. Record it as chosen, citing the decisions in `LOG.md` with their dates, and do not reopen it."

| Decision | Date | What it settles | By |
|---|---|---|---|
| D5 | 2026-11-17 | A standalone plugin for any repository; `designing-system-architecture` stays in `product-context` | orchestrator, confirmed by Igor |
| D6 | 2026-11-17 | Mermaid in Markdown files is the source of truth; the HTML file is built from it | orchestrator, confirmed by Igor |
| D7 | 2026-11-17 | Five skills first, two later | orchestrator, confirmed by Igor |
| D8 | 2026-11-17 | The skills name no terminal preview tool | Igor |
| D9, D10 | 2026-11-17 | The workflow builds one HTML file that holds everything a reader needs | Igor |
| D11 | 2026-11-17 | No board file format; Mermaid, Markdown tables and the HTML layout cover it | orchestrator, confirmed by Igor |
| D12, D14 | 2026-11-17 | The architecture is committed where `AGENTS.md` or `CLAUDE.md` points; with no pointer, `context/architecture` and `context/decisions/` | Igor |
| D13 | 2026-11-17 | The agent builds the HTML file with the sources inside and Mermaid from a pinned CDN address; Save produces an offline copy with the drawn pictures | orchestrator, confirmed by Igor |
| D15 | 2026-11-17 | The overlap with `brainstorming-solutions` is split by level, one sentence in each skill | orchestrator, confirmed by Igor |
| D16 | 2026-11-17 | Open points O1 to O5: the prototype profile allows the built `architecture.html`; `studies/`; one HTML file; the offline copy is not committed; the name `software-architecture` | Igor |
| D18 | 2026-11-17 | One pull request that ends with the release commit; an HTML overview as Igor's review; Igor merges; tags after the merge | Igor |

How it is built:

- Five prose skills in `skills/software-architecture/`, each a `SKILL.md` with `references/` and `templates/`, self-contained, with the shared files mirrored under decision 0019 (R31).
- One browser-only HTML template, `drawing-architecture-views/templates/architecture.html`, with inline, non-module JavaScript in the manner of decision 0017. It starts from the lab prototype `research/viz-lab/poc/viewer.html` and adds the source blocks between marker lines, the formatted prose, compare, the built stamp, the check lines and the offline copy.
- Decision record 0022 carries the consequential choices into the repository's decision log, including the CDN departure from the offline rule of `building-html-prototypes`.

Not taken, with the reason on record:

- The HTML file with the 5.6 MB library inside: dropped by D13 in favour of the drawn-picture copy.
- A board file format or JSON Canvas: D11; Igor works in the git project, not in a vault.
- The methods researcher's skill list (evolution and drift first, no exploring or drawing skill): `plan.md` Q2; exploring is the only skill that covers a new system, the template needs one owner, and evolution and drift act on what the first five produce.
- D2 or LikeC4 as the source language: the three text languages cost about the same to write and rendering reach picks Mermaid (LOG 2026-11-17); LikeC4 stays the route past roughly ten views.
- Extending `product-context` instead of a new category: D5.

## Verification

Profile: `docs/product-engineering/verification-profile.md`, re-confirmed 2026-11-17 at 396ba72 (see its confirmation line for what was re-probed)
G3: agreed 2026-11-17, "G3 agreed, 1a (I just installed Firefox using homebrew), 2a"

### Fixtures

The fixtures are invented and live outside the repository, in `/Users/igor/dev/theultimate-dev/skills-fixtures/software-architecture/`. Each variant of the fictional Larder app is its own git repository with one commit, so a skill can cite a commit. `ANSWER-KEY.md` beside them holds the true architecture with the file and line behind each element; it is never copied into a trial.

| ID | Folder | What it holds |
|---|---|---|
| F-A | `larder/` | Web client, mobile client, API, Postgres and a queue, with a root `AGENTS.md` that points to no architecture folder and no decision log. Planted: a queue whose removal would break the replay guarantee two product promises depend on; a folder whose name misleads about what its code does; an external dependency that only deployment configuration reveals; a fact only runtime could confirm; one element that is safe to remove |
| F-B | `larder-docs-arch/` | F-A with `AGENTS.md` pointing to `docs/architecture` and `docs/decisions`, existing hand-written files with their own names, and a decision record on why the queue exists |
| F-C | `larder-simple/` | A sound simple design: one API, one Postgres, one web client. The right answer to "can this be simpler?" is that nothing should change |
| F-D | `larder-prototype-context/` | F-A with a prototype context: `context/AGENTS.md`, `context/architecture/` with its index and one view |
| F-V | `larder-views/` | A sample architecture folder in the view format that describes F-A: index, four standing views, one study with a proposed view |

### Trials

A trial is the profile's "Agent trial": an agent with a fresh context, started by `hc run` in `<scratchpad>/trials/<id>/` from a Claude Sonnet template at high effort. The run folder holds the candidate staged with `git archive <sha>` at `skill/` (one skill directory, or the whole category for T9), a copy of a fixture at `project/`, and a task that allows only absolute paths under the run folder. The orchestrator plays the person at the gates with `hc send`. Afterwards the output files are read against `ANSWER-KEY.md` and the transcript is scanned with `evaluations/product-design/scan_transcript.py`; a run whose transcript reaches outside its folder is void and is run again.

| ID | Skill staged | Fixture | Task given |
|---|---|---|---|
| T1 | recovering | F-A | "What is really there? Recover the architecture of this application." |
| T2 | recovering | F-B | The same request |
| T3 | evaluating | F-A with F-V as `context/architecture/` | "Take a critical look at how sync works before we add a second mobile app." |
| T4 | exploring | F-B with the Markdown of F-V added to `docs/architecture/` | "We want shared shopping lists to update live on every device. What are our options?" First no answer at the gate, then "go with B". The fixture's decision log already records why the queue exists |
| T5 | simplifying | F-A with F-V | "This feels heavy for a small app. Can we drop the queue and write to Postgres directly?" Then the person narrows: accepts only the removal the study shows is safe and declines the rest |
| T6 | simplifying | F-C | "Can this be simpler?" |
| T7 | drawing | F-A with the Markdown of F-V and no HTML file | "Build the page." Then "Draw where it runs and what fails together." Then, after the orchestrator changes one view and deletes one, "Rebuild the page." Then "Explain the architecture to a new mobile developer." |
| T8 | exploring | F-D | The T4 request; then the person says the architecture lives in a separate product context repository |
| T9 | the whole category | F-A with F-V and a built HTML file | The T3 request |
| T10 | exploring | an empty folder holding only a one-page brief for a new system, written by the orchestrator: a shared meal planner that must work offline | "We are starting this from nothing. What are our options for the architecture?" |
| T11 | drawing | F-D | "Draw where it runs and what fails together." |

### Contract

"Browser" below is Playwright 1.55 for Node driving the installed Google Chrome 157, with the built file opened from disk (`file://`), which is how a reader opens it. "Network refused" means every `http` and `https` request is aborted by the browser context and counted.

| AC | Check | Layer | Tool | Steps | Pass condition |
|---|---|---|---|---|---|
| AC1 (R1, R39) | Validator and category contents | cli | shell | 1. `python3 scripts/validate.py`. 2. `ls skills/software-architecture`. | Prints "0 errors, 0 warnings"; the listing is the five skill names and `CHANGELOG.md` |
| AC2 (R1, R29, R39) | Frontmatter, length, References | cli | shell, then a read | 1. `wc -l` on each `SKILL.md`. 2. A script resolves every relative link in each skill. 3. Read each description. 4. Query skills.sh for each name and search the ten packs' trees through the GitHub API. | Each count is below 500; no skill of any of the five names is found; every link resolves inside its skill; each description has "Use when the user says" and a "Not for" clause naming the neighbours R29 lists |
| AC3 (R30) | Files the spec names | cli | shell | 1. `ls` each path R30 names; `grep` each file name in its `SKILL.md`. 2. Read each reference against the topics R30 lists for it. | Every file exists and is linked from its References table; each topic has a section or passage, quoted in the report |
| AC4 (R31) | Mirrors hold and are enforced | cli | shell | 1. `cmp` each of the ten pairs. 2. Append one byte to one copy, run the validator, restore, run it again. | All ten are identical; the validator names the changed copy and exits non-zero, then prints "0 errors, 0 warnings" |
| AC5 (R1) | Standalone | cli | transcript scan | Scan the transcript of each of T1 to T8, T10 and T11. | Each prints `CLEAN`, and no trial called another skill |
| AC6 (R12, R13, R18) | An agent builds the page from the template | e2e | agent trial T7, then `diff` | After "Build the page", `diff` the staged template against `project/context/architecture/architecture.html`. | Every changed line lies between a pair of marker lines or in the built stamp; there is one block per file the index lists |
| AC7 (R12, R19) | The built page draws | e2e | browser | Open T7's file with network; read the check lines; take a screenshot of the containers view and of the study. | One `PASS` per view and study, `DONE n/n`, no `FAIL`, no console error; the screenshots show a drawn diagram, formatted prose and a table with borders |
| AC8 (R19) | A broken view fails alone | e2e | browser | Copy T7's file; break the Mermaid in one block (`flowchart LR` then `a --`); open it. | A `FAIL <that view>: <detail>` line; `DONE (n-1)/n`; every other view still has an `svg` |
| AC9 (R16) | Switcher, zoom, pan, fit, full screen | e2e | browser | 1. Read the switcher's groups. 2. Click the second study entry. 3. Read the diagram's transform, zoom in, drag, press fit, reading the transform after each. 4. Click full screen. | Two groups, standing views and studies; the clicked view is the visible one; the transform changes after zoom and after drag and returns to the fitted value after fit; `document.fullscreenElement` is set, or the request is recorded when the headless browser refuses it |
| AC10 (R16) | Light and dark | e2e | browser, screenshots read by the agent | Screenshot one view in light, switch the theme, screenshot it again. | The computed page background differs between the two; in both screenshots the node labels and edge labels are legible against their background |
| AC11 (R16) | Compare and links | e2e | browser | 1. Open the file with the compare link form naming `containers` and the study's proposed view. 2. Open the study and click its compare link. 3. Click a link from one view's prose to another view. | Steps 1 and 2 each show two diagrams side by side with those two titles; step 3 makes the linked view the visible one |
| AC12 (R14) | One pinned address; no network | e2e | shell, then browser | 1. `grep -o 'https\?://[^"]*'` on the template. 2. Open T7's file with the network refused. | The only fetched address is Mermaid's at an exact version, on one line; the page shows a message that the diagrams were not drawn, shows each source as text, and has no uncaught error |
| AC13 (R15) | Built stamp | e2e | browser | Read the header of T7's file. | It shows a date and a short commit that equals `git rev-parse --short HEAD` of the trial's `project/` |
| AC14 (R17) | Offline copy | e2e | browser | 1. In T7's file with network, click Save offline copy and capture the download. 2. `grep` the saved file. 3. Open it with the network refused; switch through every view. | The saved file has no `<script src`, no `mermaid` library code and no CDN address; zero requests are attempted; every view shows an `svg` with its labels |
| AC15 (R17) | Offline copy keeps pan, zoom and theme | e2e | browser | 1. In the saved file, read the transform, zoom, drag. 2. Save a second copy in dark and screenshot it with the network refused. | The transform changes after zoom and after drag; the dark copy's pictures have dark backgrounds and legible labels |
| AC16 (R18) | Rebuild | e2e | agent trial T7, then browser | After "Rebuild the page": compare the blocks with the Markdown files; open the file. | The changed file's block equals its new source; the new view has a block; the deleted view has none; the stamp is new; `DONE n/n`, no `FAIL` |
| AC17 (R12, R16) | Firefox | e2e | Firefox, installed by Igor with Homebrew, through its headless screenshot | `firefox --headless --screenshot <png> file://<T7's file>`; the agent reads the screenshot. | The screenshot shows a drawn diagram and the check lines `DONE n/n` with no `FAIL` |
| AC18 (R11) | Labels on GitHub | e2e | `gh gist create` (secret), then browser on the gist's page | 1. Create a secret gist holding one fictional Larder view whose flowchart labels are quoted and use `<b>` and `<br/>`. 2. Open its page; in the diagram's frame count the `svg`, `b` and `br` elements; screenshot it. 3. Delete the gist. | The frame holds a drawn `svg` with at least one `b` and one `br` inside its labels, and no error text. Observed once already as a probe on 2026-11-17 (3 `b`, 3 `br`); observed again on the conventions' own example in p2 |
| AC19 (R3, R4, R21) | Location rule | e2e | agent trials T1, T2 | Read `project/` after each; `git -C project log --oneline`. | T1: files under `context/architecture/` with a `README.md` index, and the report proposes one pointer line for `AGENTS.md`. T2: files under `docs/architecture/`, the existing files keep their names. Both: still one commit |
| AC20 (R7, R8, R22) | Recovered views are evidenced | e2e | agent trial T1, then shell | A script checks every Evidence cell of `context.md` and `containers.md` against the files in `project/`. | `Status: built`; `Verified:` with today's date and the fixture's commit; every Evidence cell is an existing path or `assumed`; a "Blind spots" list names the runtime-only fact from the answer key; and the recovering rubric below holds |
| AC21 (R22) | The misleading folder | e2e | agent trial T1 | Read the views against the answer key. | The element for that folder is described by what its code does, cites the file, and the views show the external dependency it hides; the text notes that the name misleads |
| AC22 (R20, R23) | Risk review | e2e | agent trial T3 | Read the study; `git -C project status --porcelain`. | The study opens with the intake: the question restated, three to five scenarios each with six fields, constraints, facts apart from assumptions. Each scenario has a verdict and reasoning; each risk names an element id present in the views; each top risk has a next check. No standing view is modified. The intake rubric and the evaluating rubric below hold |
| AC23 (R24) | Options study and the Pick gate | e2e | agent trials T4, T10 | Read the study after the first report; send "go with B"; read it again. | Two or three `proposed` views at one level with shared ids, one the smallest change; a matrix with sentences and no scores; a recommendation and what would reverse it. Before the answer: the study says the choice is waiting. After: the pick, the date and the offer of a decision record. T10 produces the same study shape for a system with no code. The intake rubric and the exploring rubric below hold for both |
| AC24 (R25) | The queue stays | e2e | agent trial T5 | Read the study against the answer key. | The study names the replay guarantee the queue gives and the scenario that depends on it, and proposes no removal that drops it. Where it proposes the queue's removal at all, it shows where replay would live and counts that complexity. The intake rubric and the simplifying rubric below hold |
| AC25 (R25) | Nothing should change | e2e | agent trial T6 | Read the study. | It states that nothing should change, with reasons tied to the scenarios, and proposes no removal or merge; it names the outbox as what looks removable and is not. The intake rubric holds |
| AC26 (R25) | The Accept gate | e2e | agent trial T5 | Send the narrowing answer; read `project/`. | The study records the answer and its date, with what was accepted and what was declined; only the accepted change appears in the standing view; a decision record is offered; the standing view shows the change as `planned`; the study's views are byte-identical to before the acceptance |
| AC27 (R9, R26) | One view, and an audience guide | e2e | agent trial T7 | Read the files after the second and the fourth request. | The view sentence is stated; one new view file in the R7 shape, listed in the index, with a block in the HTML file. The guide is a study that links two or three existing views; no new standing view |
| AC28 (R2, R27, R28) | Reports and the missing sibling | e2e | agent trials T1 to T8, T10, T11 | Read each final report. | Each states what was written, what is uncertain and the next skill, and the next skill is the one R28's order gives for that situation. T3 lists what it had to assume. Each of T1 to T6, T8 and T10 says the HTML file was not rebuilt and names `drawing-architecture-views`. A trial whose harness opened no browser says the views were not drawn and asks the person to open the file |
| AC36 (R18, R21) | A sibling rebuilds the page | e2e | agent trial T9, then browser | After the report, open the HTML file. | It holds a block for the new study, a new stamp, and reads `DONE n/n` |
| AC29 (R5, R6) | Existing contexts | e2e | agent trials T8, T11 | Read `project/` after the study; send the product-context statement; read the report. | The study is under `context/architecture/studies/`; the existing view keeps the context's statuses. After the statement: no standing view is written, and the report hands the study over as input for `designing-system-architecture`. T11: the new standing view follows that context's view template and statuses, and the context's architecture index lists it |
| AC30 (R10, R11) | Mermaid subset in what the trials wrote | cli | shell | A script reads every Mermaid block written in T1 to T11, and every view file. | Each view has the R7 parts in order; an element id means the same element in every view and study of a trial; `proposed` appears only under `studies/`; `Verified:` appears only on views a trial checked against code. Each block starts with one of the six types; every label is quoted where the diagram type takes quoted labels (the check uses the per-type table in the view conventions: sequence diagram text, state transition labels and a quadrant title stay bare); at most 15 nodes; the options matrix is a Markdown table |
| AC31 (R32, R33) | Neighbour sentences | cli | shell | `git diff main -- skills/product-engineering skills/product-context`. | One added sentence in each of the two `SKILL.md` files, naming `exploring-architecture-options` and the new plugin; no link leaves the skill |
| AC32 (R34) | Prototype profile exception | cli | shell | `grep -rl "architecture.html" skills/product-prototyping`; run the validator. | The source and every mirrored copy carry the exception; the validator passes |
| AC33 (R35) | Decision 0022 | cli | shell, then a read | `git diff --stat main -- decisions`; read the record. | Only `0022-…md` is added and `README.md` gains one row; the record has the six parts and each point R35 lists |
| AC34 (R36, R37, R38) | Catalog, changelogs, README | cli | shell | The validator; `git diff main -- .claude-plugin CHANGELOG.md README.md 'skills/*/CHANGELOG.md'`. | The entry has `source`, `strict`, `license`, `homepage` and `keywords` as R36 states and five paths that exist; each changelog R37 names has its entry, under `[Unreleased]` at the first checkpoint and in the released section at the second; the README has the row, the changelog link and the plugin section |
| AC35 (R40) | Release commit | cli | shell | `git show --stat HEAD` on the release commit; the validator; for each of the five tag names as a string, the workflow's tag parsing, version match, release-note extraction and marketplace plugin list, run against the release commit with scratch outputs. No tag is created. | Only changelogs and `marketplace.json` change; the versions read as R40 states; every replayed step passes. The workflow's check that the tag is on `main` is observed after the merge, when the tags are pushed |
| AC37 (Done and review) | The overview | e2e | Artifact tool, then a read | Publish the overview; read it back against the list in AC37. | The link opens; every part AC37 lists is present; each acceptance criterion has evidence with a SHA or is listed as not verified |

### Checkpoints

The contract is observed at two commits, and the report names the SHA behind every row.

1. Stage 6, on the implementation head before the pull request opens: AC1 to AC34 and AC36. After a repair, the affected rows run again on the new head.
2. After the release commit: AC35, AC1 again, and AC34's changelog part against the released sections. The release commit changes no skill file, so trial and browser evidence from the last implementation head stands; `git diff --stat <implementation head> <release commit>` shows that.

AC37 is observed when the overview is published.

### Rubrics for reading a trial

A trial passes its row only when the rubric holds too. Each judgement quotes the passage it rests on, and claims about the system are compared with `ANSWER-KEY.md`, not only checked for an existing path.

- Intake (T3 to T6, T8, T10; R20): the study opens with all five parts before any judgement: the question restated without the named solution; three to five scenarios with six fields each; hard constraints; facts with evidence, assumptions with what would confirm each, and proposals, kept apart; what is already decided. What the decision log settles is respected (T4: the queue's reason). The transcript shows at most one message of questions to the person, asking nothing the repository answers.
- Recovering (T1, T2; R22): the three kinds of evidence are told apart (static code, deployment configuration, runtime only); the element only configuration reveals cites the configuration; no decision record is written; no runtime view is drawn because none was asked for; each element and relationship of the answer key is present or its absence is in "Blind spots"; in T2 the outdated hand-written diagram is not copied as truth.
- Evaluating (T3; R23): single points of failure, each dependency slow or down, trust boundaries and a premortem each appear; risks are ranked by likelihood and impact and carry cause and evidence; trade-off points are named; there is one annotated view, and a failure sequence or the reason that order adds nothing; at least two of the answer key's real risks are found.
- Exploring (T4, T10; R24): the options differ in kind, not in detail; one is the smallest change; the study says what was not checked and what prior art it drew on, or that the harness could not search.
- Simplifying (T5, T6; R25): before and after views share ids; there is a row for every scenario and constraint; every removed mechanism has the guarantee it gave and where it now lives; the study says where complexity moved and what must be measured first; in T5 the gateway is found removable with its reason.

### Automated checks

Every command runs on the candidate SHA and must pass.

- `python3 scripts/validate.py`: "0 errors, 0 warnings" on 396ba72 in 0.1 s.
- `git diff --check origin/main...HEAD`.

### Who certifies

- The agent self-certifies every row above. Rows that read a skill's output (AC21 to AC29) are judged against `ANSWER-KEY.md`, and the overview quotes the passage each judgement rests on.
- Human eye: none as a blocking row. Igor's review of the overview, with its screenshots of both themes, compare and the offline copy, is the look at visual quality and at the skills' wording; the pull request is `human` for that reason.

### Environments and limits

- Allowed: this worktree, scratchpad folders, the fixtures folder, local files opened from disk, and the Mermaid CDN address fetched by the page under test.
- Never: GitHub releases and tags of `theultimate-dev/skills`, the published marketplace, the `main` branch. Verification creates no tag, release or merge.
- Data: only folders the session created.
- Side effects: one secret gist with fictional content for AC18, deleted in the same check (Igor, 2026-11-17: "2a").

### Mocks and what they exclude

- The trials run in Claude Code on Sonnet. They exclude other harnesses (Codex, Pi) and other models.
- A trial agent's harness still loads the machine's installed plugins and the user's global instructions, which hold none of the candidate text. The transcript scan voids any run that calls another skill, so "no other plugin installed" is observed as "no other plugin used".
- Not driven in a trial, checked by reading the instruction in each skill and reported as such: the reply without file access (R2), prior-art research where the harness can search (R24; the trials allow no search tool), and a declined Accept gate (R25; T5 exercises narrowing).
- Playwright's WebKit build stands in for Safari in one extra run of AC7; it is reported separately and is not a pass condition.

### Harness gaps

- Firefox (AC17): closed. Playwright's Firefox build does not start on this macOS (27.2.1). Igor installed Firefox 160.0.1 with Homebrew and opened it once ("Firefox opened once", 2026-11-17). Probed afterwards: its headless screenshot of a `file://` page that loads Mermaid from the CDN shows `PASS draw`, `DONE 1/1` and the drawn diagram. Clicks are not driven in Firefox; AC9 to AC11 are observed in Chrome only.
- GitHub (AC18): GitHub draws Mermaid only for content it hosts. Closed at G3 ("2a"): a secret gist with one fictional Larder view, read in the browser and deleted afterwards. Probed on 2026-11-17: the gist's diagram frame held a drawn picture with 3 `b` and 3 `br` elements, and the gist was deleted.
- No interactive browser tool in the agent harness: closed for this work item by Playwright for Node in the scratchpad, probed on 2026-11-17.
- No CI job runs browser checks, and the checks are not committed in this pull request (G1: the evaluations follow as a `claude plugin eval` suite).
- "How to verify" pointer in `AGENTS.md`: not offered again; the profile is linked from this spec, as in earlier work items.
