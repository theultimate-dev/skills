# Spec: curating-design-systems, a design home and the graduation of a chosen direction

Status: agreed (G1, 2026-10-25: "agreed")
Track: feature
Source: issue #11, https://github.com/theultimate-dev/skills/issues/11

## Problem

The product-design skills (product-design 0.3.0) end at a refined prototype for one initiative. None of them sets up a project's long-lived design home, and none turns a chosen direction into shared foundations. In the session behind the issue both steps were improvised: the layout, the naming, the rules for what goes where, and the checks.

What exists today:

- `building-html-prototypes` reads a design tree but never writes its foundations. Its contract assumes a root such as `design/` with `design/foundations/` and views (`references/design-tree-contract.md:7`). It links shared files "as they are" and changes one "only when the user asks" (`:30`). It ships the tree check (`templates/tree-check.html`) and the hosted check from #9. Sketches keep their candidate tokens inline "until the user chooses a direction" (`SKILL.md:20`), and nothing says where they go next.
- `exploring-visual-directions` asks for a combined direction's "resulting composition and tokens" (`SKILL.md:35`). For a native surface it adds a platform frame with sourced geometry tokens (`references/native-surfaces.md:37-46`). The comparison template records the recommendation, the selection and the combination (`templates/direction-comparison.md:64-67`).
- `guiding-product-discovery` keeps work per initiative in `docs/product-design/<initiative>/` (`SKILL.md:19`). It keeps rejected directions with their reasons (`:47`). Its Converge phase lists "tokens" and routes to no specialist for them (`references/workflow.md:12`).
- `preparing-implementation-handoffs` asks for "Relevant project token/component sources" (`templates/implementation-handoff.md:30`) and has nowhere to point.
- Outside the plugin, `product-context` keeps design work per initiative under `design/<initiative>/`, Markdown plus prototypes only (`structuring-product-context/references/layers-and-rules.md:18,77`).

Outcome: one new product-design skill, `curating-design-systems`. It sets up or adopts the design home with your agreement and keeps the home's rules. It graduates each chosen direction into shared foundations and components, and checks the tree after every change. The neighboring skills route to it.

## Requirements

Set up or adopt the design home (issue part 1)
- R1: Before proposing anything, the skill inspects what exists: design folders, token and theme files, shared stylesheets, the code's layout of apps, the project's instructions and its decision log. It doesn't ask anything these answer.
- R2: Before creating any file, it proposes a layout with a recommendation and the reasons for it:
  - one foundations folder that every platform uses;
  - one folder per platform, mirroring the code's apps where there are any, or else the surfaces the brief names;
  - one folder per view inside its platform;
  - a README at the root.

  It says where the home sits and why. It follows the project's own rules on where files may live. When those rules forbid the location it proposes, it names the conflict and asks.
- R3: It creates the layout only once the user explicitly agrees.
- R4: When it adopts an existing design folder, it proposes where each existing file goes. It moves files and rewrites their relative paths only once the user agrees. After the move, the tree check and the render check pass. It reads the code's theme files as a source of values and never moves, edits or links them.
- R5: It writes a README at the home's root covering:
  - the layout and its rules;
  - how to add a platform, and how to add a view;
  - the graduated directions, each linked to its record;
  - open questions, including exporting tokens to code.
- R6: When the project keeps a decision log, the reasons for the layout go in a record there, through `decision-records` when it is installed, and the README links that record. Without a log, the README holds the reasons too.

Keep the layout's rules (issue part 2)
- R7: The skill states four rules and keeps them in every change it makes:
  - foundations hold no platform styles;
  - a platform stylesheet draws only what the operating system draws;
  - a view's own surfaces are styled once, in that view's stylesheet, and other views showing the same surface link to it;
  - pages link by relative path only, as the design-tree contract says.

Graduate a direction (issue part 3)
- R8: Graduation runs after the user selects or combines a direction and before the pages are refined. Its source is:
  - the chosen sketches;
  - the comparison's selection and combination;
  - a refined one-file prototype, which is also accepted.

  When there is no design home yet, the skill sets one up first (R1 to R3).
- R9: It moves the chosen tokens into foundations by role, grouped as colour, type, space, radius and motion. It graduates every appearance variant that the direction or its platform frame defines. When a platform the home serves has an appearance the direction lacks, it asks whether to draft that variant for review or record it as an open question. It never invents a variant silently.
- R10: A part that the direction repeats, such as a button, a status row or a badge, becomes a shared component, even when only one view uses it so far. A view's own surfaces stay in that view's stylesheet.
- R11: Sometimes the direction brings a role that foundations already define with another value. For each such conflict, graduation lists both values and the pages that link the role. The user then chooses: change it everywhere, keep the existing value, or add a new role. Until the user chooses, no foundation file changes. A view never overrides a foundation role locally.
- R12: Explorations stay where they were made, unchanged. Graduation records each direction's reason in the existing direction comparison, as chosen, combined in part (naming which parts), or not chosen. The README links the comparison.

Checks (issue part 4)
- R13: After setup, adoption and every graduation, the skill runs three checks and records their results:
  - every reference resolves inside the tree, which is the design-tree check from #9;
  - no token is defined twice;
  - every page still renders.

Fit
- R14: `curating-design-systems` joins product-design: its `SKILL.md` follows the skill format, and it is listed in `marketplace.json`, the README categories table and the plugin changelog.
- R15: `guiding-product-discovery` routes to it at Converge, after the direction is selected and before the pages are refined.
- R16: Three specialist skills point to it:
  - `exploring-visual-directions` hands the chosen or combined direction, with its tokens, to graduation.
  - `building-html-prototypes` has refined pages in a design tree link the graduated foundations. When the project has none yet, it names the new skill instead of improvising foundations.
  - `preparing-implementation-handoffs` takes its token and component sources from the foundations and components, and carries the open question on exporting tokens to code.

## Acceptance criteria

- AC1 (R1, R2, R3): Given a fixture project with code apps for the web and for macOS and no design folder, an agent following the skill sets up a design home. Before writing any file, it proposes:
  - a foundations folder;
  - one platform folder per code app;
  - views inside their platform;
  - a README;
  - where the home sits;
  - a recommendation with its reasons.

  It creates no file until the user agrees.
- AC2 (R2): `SKILL.md` says to follow the project's rules on where files may live. When they forbid the proposed location, it says to name the conflict and ask.
- AC3 (R3, R5): After agreement, the AC1 trial's home has the proposed folders and a README. The README has the layout, the four rules, how to add a platform, how to add a view, the graduated directions, and open questions, including token export.
- AC4 (R5): Given the home from AC3, a fresh agent that has only its README adds a `settings` view to the macOS platform. The view lands in the macOS platform's folder. It links the foundations and the platform stylesheet by relative path, and the design-tree check ends `DONE n/n` with no `FAIL`.
- AC5 (R4): Given a fixture project with:
  - an existing design folder holding a tokens file and two pages that link it;
  - a code theme file;

  the agent adopting it proposes where each existing file goes before moving any. After agreement:
  - the design-tree check ends `DONE n/n`;
  - both pages render with their shared styles;
  - the code theme file is byte-identical and no page links it.
- AC6 (R6): `SKILL.md` says where the layout's reasons go: a record in the project's decision log when there is one, linked from the README, and the README otherwise. In the AC1 trial, whose fixture keeps `decisions/`, the agent writes or proposes a record there, and the README links it.
- AC7 (R7): `SKILL.md` and the README template state the four rules.
- AC8 (R7, R9): The fixture direction's platform frame holds a geometry token for macOS, such as a menu-bar height. After graduation:
  - that token is defined in the macOS platform's folder with its source;
  - no foundations file defines it.
- AC9 (R8, R9, R10, R12): Given a fixture project with a design home, three one-file sketches with inline candidate tokens, and a comparison that combines A's typography with B's colour, an agent following the skill graduates the combination. Afterwards:
  - the foundations define the combined tokens by role, grouped as colour, type, space, radius and motion;
  - the button the sketch repeats is a shared component;
  - the view's own panel is in the view's stylesheet;
  - the three sketches are byte-identical to before;
  - the comparison gives a reason for A, B and C;
  - the README links the comparison.
- AC10 (R9): Given a direction that defines a light and a dark appearance, the foundations define each colour role in both. The dark values sit under an appearance condition in the same file, and the duplicate-token check reports no duplicate.
- AC11 (R9): Given a direction that defines only light, for a home whose macOS platform has a dark appearance, the agent asks whether to draft dark for review or record it as an open question. It writes no dark value before the answer.
- AC12 (R11): Given foundations with `--color-accent: #205d42`, linked by two views, and a new direction with `--color-accent: #9a3b1f`, the agent lists the conflict: both values and both pages. It offers the three choices. Before the answer, it changes no foundations file and adds no override in any view.
- AC13 (R13): The duplicate-token check, on a fixture tree where:
  - `--space-2` is defined in the foundations and again in a view's stylesheet;
  - `--color-ink` is defined twice in the foundations under the same condition;

  reports both, each with its files. It does not report `--color-ink`'s dark value under an appearance condition. Once the duplicates are removed, it reports the tree clean.
- AC14 (R13): Given a fixture tree in which graduation renamed a component class that `views/archive/index.html` still uses, the render check reports that page and passes the other pages.
- AC15 (R13): `SKILL.md` requires the three checks after setup, adoption and every graduation, with their results recorded. On the homes produced in AC3 and AC9, the design-tree check ends `DONE n/n` with no `FAIL`.
- AC16 (R14): The new skill appears in all the places the repository requires:
  - `marketplace.json` lists `./skills/product-design/curating-design-systems`;
  - the README categories table names the skill;
  - `skills/product-design/CHANGELOG.md` has an entry under `[Unreleased]`;
  - `SKILL.md` has exactly `name`, `description` and `license` and stays under 500 lines;
  - `python3 scripts/validate.py` reports 0 errors.
- AC17 (R15): `guiding-product-discovery` routes Converge to `curating-design-systems` after the direction is selected and before refinement, in its specialist table and in its workflow.
- AC18 (R16): The three specialists say what R16 states, each in its `SKILL.md` or the template named there.

## Non-goals

- The code side: exporting tokens to a platform format, such as Swift, Android XML or a CSS build. The README records it as an open question until the project's code reads the tokens.
- Changing `product-context`'s design layer or its house rule 8. A follow-up issue, #23, tracks giving it a slot for a design home.
- Moving, rewriting or re-rendering explorations.
- Building or refining pages, which `building-html-prototypes` does.
- Changing the one-file default for direction sketches.
- Device geometry values for specific platforms. The skills ship none, as #9 and #10 already say.
- Design tools, component libraries, CSS frameworks and token pipelines such as Style Dictionary.
- Changing a production theme or any application code.
- Cutting a product-design release.

## Constraints

- Skill format (AGENTS.md "Skill format"):
  - three frontmatter fields;
  - `SKILL.md` under 500 lines, with depth in `references/` and copyable files in `templates/`;
  - links stay inside the skill's directory, so the skill names other skills in prose and never links into them;
  - nothing assumes a harness, an install path or an environment variable.
- `scripts/validate.py:65` rejects the literal parent-path string in every skill file. The README template and the examples describe climbing to a parent folder in prose, as #9 did.
- Accepted decisions that bound the work:
  - 0006 fixes product-design's skill set: five specialists and a coordinator.
  - 0016 adds design trees.
  - 0017 ships the prototype checks as browser-only templates.

  None is edited (AGENTS.md "Conduct"); G2 decides whether a new record extends 0006.
- Name: `curating-design-systems` is free in this repository and on skills.sh (`npx skills find`, 2026-10-25). Taken names nearby: `design-system`, `extract-design-system`, `design-system-patterns`, `visual-design-foundations`.
- Changelogs (AGENTS.md "Commits and changelogs"):
  - every slice adds a user-facing entry under `[Unreleased]` in `skills/product-design/CHANGELOG.md`;
  - a decision record or evaluation tooling gets an entry in the root `CHANGELOG.md`;
  - commits follow Conventional Commits with the category or skill as scope;
  - `python3 scripts/validate.py` passes before each PR.
- Done and review: every PR slice is merged to `main` with its `[Unreleased]` entry, and the validator passes. You review every PR ("Every PR (Recommended)", G1 round 3, 2026-10-25).

## Assumptions and open questions

- Assumption: the default layout is:
  - `design/` at the root of the repository that keeps the designs;
  - `design/foundations/` with `tokens.css` and `components.css`;
  - `design/<platform>/`, with a platform stylesheet when the platform has system UI to draw;
  - `design/<platform>/<view>/`, with the view's pages and its stylesheet;
  - `design/README.md`.

  Basis: inferred from the issue and #9's `shared-foundations-project` fixture. If wrong: the README template and the trials' pass conditions change.
- Assumption: a web platform has no platform stylesheet, because the operating system draws nothing inside the page. Basis: inferred from the second rule. If wrong: the web gets a stylesheet for browser-chrome stand-ins.
- Assumption: a native platform frame's geometry tokens live in that platform's folder, with their sources, never in foundations. Basis: inferred from the first rule and #10's platform frame. If wrong: foundations gain platform values, against the first rule.
- Assumption: tokens are one tier of role names, such as `--color-surface` and `--space-2`, in five groups. There is no primitive palette tier unless the project already keeps one. Basis: "by role" in the issue; not asked, medium impact. If wrong: a primitive tier and the naming rules for it.
- Assumption: an appearance variant redefines the same role names, in the same file, under an appearance condition: a media feature, plus a root attribute that can force it, as in the native-surface profile. "Defined twice" means the same name defined in two files, or twice in one file under the same condition. Basis: inferred. If wrong: the duplicate-token check's rule changes.
- Assumption: "every page still renders" means two things:
  - each page opens from disk with its shared styles applied;
  - each page that existed before the change renders as it did, unless the change was meant to alter it.

  Basis: "still" in the issue. If wrong: the check only confirms that the shared styles apply, and AC14 goes.
- Assumption: when there is no direction comparison, graduation writes the reasons in a short record beside the sketches, with the comparison's selection fields. Basis: not asked, low impact. If wrong: the README holds the reasons.
- Assumption: the coordinator's discovery index gains a row for the design home. Basis: not asked, low impact.
- Assumption: the product-design release, a minor bump for a new skill, is cut separately with `release-process` after the slices merge. Basis: AGENTS.md "Release". If wrong: G4 adds a release slice.
- Open: how the checks ship. Self-containment means the new skill either carries its own copy of the tree check or relies on `building-html-prototypes`. The duplicate-token and render checks could be templates or procedures. Also open: whether a decision record extends 0006. Blocks: nothing at G1. Owner: G2. Resolved at G2: see Approach.
- Open: the fixtures and trials for AC1, AC3 to AC6, AC8 to AC14. Blocks: nothing at G1. Owner: G3.

## Approach

Chosen: A, own copies with new templates beside them, and two decision records. Agreed at G2, 2026-10-25: "A: own copies (Recommended)", "0018 and 0019 (Recommended)"

`curating-design-systems` is a prose skill: `SKILL.md`, references for setup and adoption, the layout rules and graduation, and a README template for the design home. It ships three browser-only check templates, built like those in `building-html-prototypes` and run the way 0017 describes:

- `templates/tree-check.html` is a byte-identical copy of `building-html-prototypes/templates/tree-check.html`. A new mirror rule in `scripts/validate.py` fails when the copy differs from its source or either file is missing.
- `templates/token-check.html` starts from the same entry page and page list as the tree check. It reads every stylesheet and `style` element each page links through the browser's CSS parser (`new CSSStyleSheet().replaceSync()`), and reports:
  - each custom property defined in two files;
  - each custom property defined twice in one file under the same selector and conditions;
  - each `var()` a page's styles use without a fallback, when no stylesheet that page links defines it.
- `templates/render-check.html` loads each page in a same-origin frame of a fixed width.
  - Its baseline mode walks the page's elements and writes a snapshot of their computed styles into the page.
  - Its compare mode reads a saved baseline from the staging root. It reports each page that renders differently, naming the element, the property, and the value before and after.

  The agent takes the baseline before setup moves, adoption or graduation touch any page. It compares afterwards, and records each difference as intended, with the user's choice behind it, or as broken.

`building-html-prototypes` changes only line 18 of its tree check's comment ("the notes list"), so that the mirrored copy reads correctly in both skills. Its own check and #9's expected results stay as they are.

- Touches:
  - new `skills/product-design/curating-design-systems/`;
  - `scripts/validate.py`, which gains the mirror rule;
  - `AGENTS.md` "Skill format", one line on mirrored files;
  - `skills/product-design/building-html-prototypes/templates/tree-check.html:18`;
  - the three specialists and the coordinator named in R15 and R16;
  - `.claude-plugin/marketplace.json` and `README.md`;
  - `decisions/0018-…`, `decisions/0019-…` and `decisions/README.md`;
  - both changelogs;
  - fixtures in `evaluations/product-design/`.
- Reuses:
  - the tree check as it is;
  - 0017's staging contract (the tree at `<staging>/a/b/`, templates at `<staging>/`) and its results format;
  - the interaction harness's same-origin frame pattern (`building-html-prototypes/templates/interaction-harness.html`) for the render check;
  - #9's `shared-foundations-project` fixture as the starting point for the graduation fixtures.
- Contracts:
  - **Home layout:** the agreed default layout (see Assumptions), plus an `index.html` at the home's root that links every view. It serves as the entry page for all three checks and for a host. The README names the entry page and every page that no link reaches.
  - **Check inputs and results:** all three templates take `entry=` and `pages=` exactly as the tree check does, and write `PASS <name>` and `FAIL <name>: <detail>` lines into `#results`, ending `DONE <passed>/<total>`.
    - Token check names: `token defined once: <name>` and `token resolves: <page> <name>`.
    - Render check names: `renders as before: <page>`. Baseline mode writes the snapshot as JSON into `#snapshot`, and the agent saves it as `render-baseline.json` at the staging root, outside the tree. Compare mode also takes `moved=<old>:<new>,…`, so a page that adoption moved is compared with its own baseline. This parameter was added at G3 for AC5.
  - **Mirror rule:** `scripts/validate.py` holds a list of source and copy paths, starting with the tree check, and reports an error for each pair that differs or is missing. A change to the source changes the copy in the same commit.
  - **Parent paths:** as in #9, no file in the skill contains the literal parent-path string. The README template and the references describe such paths in prose, and fixtures that use them live in `evaluations/product-design/`.
- Evidence:
  - `building-html-prototypes/templates/tree-check.html` is 254 lines. Its only line that names that skill's own files is line 18. It scans CSS as text (`stripComments`, `endOfUrl`, `unescapeCss`, lines 108–160).
  - No file is shared between two skills today: a checksum of every file under `skills/` found no duplicates (2026-10-25). The validator bans the parent-path string (`scripts/validate.py:65`) and checks self-containment (`:254`).
  - Decisions: 0006 says each skill "accepts equivalent artifacts without another skill installed". 0017 ships the checks as browser-only templates.
  - Probe, headless Google Chrome 155.0.8059.85, 2026-10-25, scratchpad only:
    - `replaceSync()` listed each custom property with its selector and `@media` condition, so a second `--a` in `:root` showed up as a duplicate.
    - A `var()` inside the shorthand `margin` appeared only in the rule's `cssText`, not when iterating its longhands, so the token check reads `cssText`.
    - `@import` was silently dropped. The tree check already fails it, so the token check doesn't rely on it.

Rejected alternatives:

- B, an extended tree check, mirrored: it changes a shipped check beyond the spec, which would reopen G1, and it means re-baselining #9's expected results.
- C, the sibling owns the checks: the skill would have only manual checks whenever it is installed without `building-html-prototypes`, which goes against 0006.
- Comparing screenshots before and after by eye, for the render check: it gives no pass or fail line, and the verification profile marks reading screenshots `unconfirmed`.

Consequences:

- Easier: the skill works on its own, and the checks run the same way on every project. The tree check has one source of truth, and the validator enforces it.
- Harder: about 400 lines of new template JavaScript to review. The mirror rule is the first repository tooling that ties two skills together. A change to the source tree check also means updating its copy.
- Risk: the render check compares computed styles, not pixels, so a change that only pixels show, such as an image file replaced under the same name, passes. The skill says so, and keeps the direct-opening check by eye.
- Risk: a page that changed on purpose fails the render check. The agent records each difference against the user's choice, which G3 makes checkable.
- Revisit if: a third skill needs one of these templates, or a project needs the checks without a browser, as in 0017.
- Decision records:
  - `decisions/0018-curate-a-design-home-in-product-design.md` extends 0006 with the seventh skill, the layout and its four rules, and graduation between selection and refinement.
  - `decisions/0019-mirror-shared-templates-across-skills.md` records mirrored templates, kept identical by the validator.

## Verification

Profile: `docs/product-engineering/verification-profile.md`, re-confirmed 2026-10-25 at fc87115
G3: agreed 2026-10-25, "Agree (Recommended)"

### Fixtures

The fixtures live in `evaluations/product-design/fixtures/`. They are invented and local only, and each slice adds the ones its rows need. Harbor is the fictional backup watcher of the #10 fixtures.

| ID | Folder | What it holds |
|---|---|---|
| F-new | `harbor-home-new/` | Harbor's brief in `README.md`, code apps `apps/web/package.json` and `apps/macos/Package.swift` (never built), a `decisions/` log with its index and one record, and no design folder |
| F-adopt | `harbor-home-adopt/` | An existing `designs/` folder: `tokens.css` and two pages that link it, `menu-panel.html` and `settings.html`. A code theme file, `apps/web/src/theme.css` |
| F-grad | `harbor-home-graduate/` | A design home in the default layout: README, root `index.html`, empty foundations, and a `macos/` platform with a `status-panel/` view folder. Beside it, `docs/product-design/status-panel/`, holding: three one-file sketches A, B and C with inline candidate tokens, where B defines light and dark; the comparison, which selects A's typography with B's colour; and a platform frame with `--menu-bar-height` and its source. The selected sketch repeats one button three times and has its own panel |
| F-light | `harbor-home-light-only/` | F-grad with B's dark values removed |
| F-conflict | `harbor-home-conflict/` | A home whose foundations define `--color-accent: #205d42`, linked by two views, and a newly selected direction with `--color-accent: #9a3b1f` |
| F-dupes, F-clean | `token-dupes/`, `token-clean/` | AC13: a tree with three faults, and the same tree fixed. The faults: `--space-2` is defined in the foundations and again in a view's stylesheet; `--color-ink` is defined twice in `tokens.css` under `:root`; a page uses `var(--missing)`. Both trees also define `--color-ink`'s dark value under `@media (prefers-color-scheme: dark)` |
| F-before, F-after | `render-before/`, `render-after/` | AC14: a home with three views. In F-after, `components.css` renames `.card` to `.guide-card`, two views follow the rename, and `views/archive/index.html` still uses `.card` |

### Trials

Trials follow #10's procedure, written up in `evaluations/product-design/README.md`:

1. The coordinator stages the candidate skill alone, with `git -C <worktree> archive <sha> skills/product-design/curating-design-systems`, into `<run>/skill/`. It copies the fixture to `<run>/project/` and records a checksum of every file there.
2. A fresh Sonnet executor gets only `<run>` and a fixed task text, which ends: "No network, no browser, no server and no user. Record any check that needs a browser as not performed. If the skill tells you to ask the user, write the question, its options and your recommendation to `<run>/project/QUESTIONS.md`, and stop."
3. Two-phase trials continue the same executor once, with a fixed answer that is written in the README.
4. `scan_transcript.py` runs on every executor transcript. A reach outside `<run>`, or any Skill, Agent or web tool call, voids the run, and the void is reported.
5. The coordinator runs the check templates on the output, staged as the profile describes.
6. Fresh Sonnet graders answer each judgment criterion yes or no. Each yes carries an exact quote with its `file:line`, and the grader tries to refute it. The coordinator then runs `grep -F` on every quote, and an unfound quote voids that grade.

Replicates: 3 runs each of T-setup and T-grad, and 1 run of every other trial. A row passes only when every run passes. No runs are added after the results are seen. There are no baselines, because there is no earlier version of the skill to compare against.

"Cold read" (CR) means a fresh Haiku agent gets only the candidate skill directory and a list of questions. Each answer must cite a `file:line`, and the verifier opens every cited line.

| AC | Check | Layer | Tool | Steps | Pass condition |
|---|---|---|---|---|---|
| AC1 (R1, R2, R3) | Propose before creating | ai-eval, cli | T-setup ×3 (Sonnet), grader, checksums | Phase 1 of T-setup on F-new: "Set up a design home for this project." | Each run stops with `QUESTIONS.md` proposing all of: a foundations folder, a `web` and a `macos` platform folder named after the code apps, views inside their platform, a README, where the home sits, and a recommendation with reasons. Apart from `QUESTIONS.md`, `project/` matches its checksums |
| AC2 (R2) | Location conflicts | ai-eval | CR (Haiku) | Ask: where may the home sit, and what happens when the project's rules forbid the proposed location? | The answers say to follow the project's rules, and to name the conflict and ask, citing `SKILL.md` |
| AC3 (R3, R5) | The created home | ai-eval, cli, e2e | T-setup ×3 phase 2, grader, `test -d`, headless Chrome | 1. Answer "Agreed: create the layout as proposed." 2. `test -d` each proposed folder. 3. Grade the README. 4. Stage the home with `tree-check.html` | 2. Every folder exists. 3. The README has the layout, the four rules, adding a platform, adding a view, graduated directions, and open questions including token export. 4. `DONE n/n` with no `FAIL` |
| AC4 (R5) | README alone is enough | ai-eval, e2e | T-readme (Sonnet), headless Chrome | 1. A fresh executor gets only T-setup run 1's home, with no skill: "Following only `README.md`, add a `settings` view to the macOS platform." 2. Stage the result with `tree-check.html` | The new view is in the macOS platform's folder and links the foundations and the platform stylesheet by relative paths. The tree check ends `DONE n/n` with no `FAIL` |
| AC5 (R4) | Adopt an existing folder | ai-eval, cli, e2e | T-adopt (Sonnet), checksums, `grep`, headless Chrome | 1. Before the trial, stage `designs/` and save a `render-check.html` baseline. 2. Phase 1: "Set up a design home for this project." 3. Answer "Agreed: move the files as proposed." 4. Stage the new home and run `tree-check.html`, then `render-check.html` with the baseline and `moved=` from the agreed mapping | 2. `QUESTIONS.md` places each of the three existing files, and `project/` matches its checksums. 4. The tree check ends `DONE n/n`, and both pages pass `renders as before`. `apps/web/src/theme.css` matches its checksum, and `grep -r theme.css` over the home finds nothing |
| AC6 (R6) | Reasons in the decision log | ai-eval, cli | CR (Haiku), T-setup ×3, `grep` | 1. CR: where do the layout's reasons go, with a decision log and without one? 2. In each T-setup run, list the new files in `decisions/` and `grep` the README for a link to them | 1. A record in the log, linked from the README, and the README otherwise, citing `SKILL.md`. 2. A new record in `decisions/` that the README links |
| AC7 (R7) | The four rules | ai-eval | CR (Haiku), template read | Ask for the layout's rules, then read the README template | Four rules, each citing `SKILL.md` or a reference. The README template states all four |
| AC8 (R7, R9) | Geometry stays in its platform | cli | T-grad ×3, `grep` | 1. `grep -rn -- "--menu-bar-height:" design/` 2. Read the matching file for the token's source | 1. One definition, under `design/macos/`, and none under `design/foundations/`. 2. The source from the platform frame appears next to the token or in the platform's README |
| AC9 (R8, R9, R10, R12) | Graduate a combination | ai-eval, cli, e2e | T-grad ×3 (Sonnet), grader, checksums, `grep`, headless Chrome | 1. T-grad on F-grad: "Graduate the selected direction into the design home." If it stops, continue once with "Go with your recommendation." 2. Compare every candidate token in A's typography and B's colour with the foundations. 3. Grade: the role groups; the button in `components.css`; the panel in the view's stylesheet; the comparison's reasons. 4. Checksum the sketches. 5. Check the README's link to the comparison. 6. Run `tree-check.html` and `token-check.html` | 2. Every chosen value is in the foundations. 3. Five groups (colour, type, space, radius, motion); the button is a shared component; the panel is in the view's stylesheet; A, B and C each have a reason. 4. The three sketches match. 5. The link resolves. 6. Both end `DONE n/n` with no `FAIL` |
| AC10 (R9) | Light and dark | cli, e2e | T-grad ×3, `grep`, headless Chrome | 1. List B's colour roles. 2. In the foundations, find each role under `:root` and under the appearance condition. 3. Run `token-check.html` | 2. Each role has a light and a dark definition, both in the same file. 3. No `FAIL token defined once` |
| AC11 (R9) | Ask about a missing appearance | ai-eval, cli | T-light (Sonnet), grader, `grep` | T-light on F-light, with T-grad's task | It stops with `QUESTIONS.md` offering to draft dark for review or to record it as an open question. `grep -rnE "prefers-color-scheme: *dark\|data-appearance=.dark" design/foundations` finds nothing |
| AC12 (R11) | Ask about a conflicting role | ai-eval, cli | T-conflict (Sonnet), grader, checksums, `grep` | T-conflict on F-conflict: "Graduate the newly selected direction into the design home." | `QUESTIONS.md` names `--color-accent`, both values and both views, and offers the three choices. Every file under `design/` matches its checksum |
| AC13 (R13) | Duplicate tokens, and tokens that don't resolve | e2e | headless Chrome, staged `token-check.html` | 1. Stage F-dupes and dump. 2. Stage F-clean and dump | 1. Exactly three `FAIL` lines: `token defined once: --space-2` naming both files; `token defined once: --color-ink` naming `tokens.css`; and `token resolves: <page> --missing`. No line mentions the dark value. 2. No `FAIL`, ending `DONE n/n` |
| AC14 (R13) | Renders as before | e2e | headless Chrome, staged `render-check.html` | 1. Stage F-before, dump in baseline mode, and save `#snapshot` as `render-baseline.json`. 2. Stage F-after with that baseline, and dump in compare mode. 3. Control: compare F-before with its own baseline. 4. Control: stage F-before with one view folder renamed, and compare with `moved=` | 2. `FAIL renders as before: views/archive/index.html`, naming an element and a property, and `PASS` for the other two views. 3. Every page passes, ending `DONE n/n`. 4. Every page passes |
| AC15 (R13) | Checks after every change | ai-eval, e2e | CR (Haiku), headless Chrome | 1. CR: which checks run, when, and where their results go? 2. The tree-check results of AC3 and AC9 | 1. The three checks, after setup, adoption and every graduation, recorded with their results, citing `SKILL.md`. 2. As in AC3 and AC9 |
| AC16 (R14) | Packaging | cli | validator, `jq`, `grep`, `wc` | 1. `python3 scripts/validate.py`. 2. `jq` the product-design `skills` list. 3. `grep` `README.md` and `[Unreleased]` in the plugin changelog for the skill. 4. `wc -l` on `SKILL.md` and read its frontmatter | 1. "0 errors". 2. It contains `./skills/product-design/curating-design-systems`. 3. Both match. 4. Under 500 lines; exactly `name`, `description` and `license` |
| AC16 (R14) | Mirror rule catches drift | cli | validator in a scratch worktree | 1. Append one byte to the copy of `tree-check.html`, and run the validator. 2. Delete the copy, and run it again. 3. Restore the copy, and run it a third time | 1. An error naming the copy and its source. 2. An error saying the copy is missing. 3. "0 errors" |
| AC17 (R15) | Coordinator routing | ai-eval | CR (Haiku) | Ask: after a direction is selected, what runs next and before what? | `curating-design-systems` runs after selection and before refinement, citing the specialist table in `SKILL.md` and the Converge row in `references/workflow.md` |
| AC18 (R16) | The three specialists | ai-eval | CR (Haiku) ×3 | One cold read per skill. `exploring-visual-directions`: what happens to a chosen direction's tokens? `building-html-prototypes`: what do refined tree pages link, and what if no foundations exist yet? `preparing-implementation-handoffs`: where do token and component sources come from, and what about exporting tokens? | Each answer states R16's clause for that skill and cites its `SKILL.md` or the named template |
| All slices | Wording, voice, design soundness | visual | user (human eye) | The PR's diff of the skill text, the templates, the fixtures and the decision records | You approve each PR ("Every PR (Recommended)", G1, 2026-10-25) |

### Automated checks

Every command runs on the candidate SHA and must pass. The baseline at fc87115 passes.

- `python3 scripts/validate.py`: "0 errors". This includes the parent-path ban for every skill file and, once slice 1 adds it, the mirror rule.
- `git diff --check origin/main...HEAD`: no output.

### Who certifies

- The agent self-certifies AC1 to AC18: content by cold read, behavior by trial, templates by staged headless runs, and packaging by the validator and `grep`.
- Human eye: the wording and voice of each PR. These rows are reported `blocked (human eye)` with the diff summary until you review, which puts every PR in the `human` category, matching "Every PR".

### Environments and limits

- Allowed: local only, on `127.0.0.1` servers, scratchpad folders, the work item's worktree, headless Chrome and subagents.
- Never: tags, releases, pushes or merges during verification, and no real host or artifact viewer.
- Data: delete only the scratchpad folders the run created, and stop every server the run started.
- Side effects: none. Fixtures link only local files.

### Mocks and what they exclude

- The fixture projects are invented. They exclude the variety of real design folders, code layouts and decision logs.
- `QUESTIONS.md` and one fixed continuation stand in for you. They exclude follow-up questions and answers that change the proposal.
- Executors run no browser. Their recorded checks stay "not performed", and the coordinator runs the templates instead. This excludes the agent's own handling of a failing check.
- The render check compares computed styles, which excludes changes that only pixels show.
- Replicates: 3 runs on the core trials and 1 elsewhere. This excludes rarer run-to-run variance.

### Harness gaps

- None needs Plan 0. Each slice builds its own fixtures and adds its rerun commands and task texts to `evaluations/product-design/README.md`.
- "How to verify" pointer in AGENTS.md: declined 2026-10-24 for #9, "Not now (Recommended)". Not offered again.
