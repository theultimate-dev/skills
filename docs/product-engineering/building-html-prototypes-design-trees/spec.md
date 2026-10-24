# Spec: building-html-prototypes beyond the one-file sketch

Status: agreed (G1, 2026-10-24: "agreed")
Track: feature
Source: issue #9, https://github.com/theultimate-dev/skills/issues/9

## Problem

`building-html-prototypes` (product-design 0.1.0) builds every artifact as one self-contained offline file and verifies it only from disk. That suits disposable direction sketches. It fails a designer or agent who refines a chosen direction into prototype pages that a project keeps and reviewers open elsewhere:

- **Shared files.** The contract is "One artifact, one file" and forbids "sibling stylesheets" (`references/offline-artifact-contract.md:3,9`). `SKILL.md:15` says to copy "the relevant token values or minimal CSS into the artifact", and `SKILL.md:41` says "no HTML artifact may need another file to render". Decision 0006 fixes the same rule (`decisions/0006-product-design-discovery-skills.md:22`). A project whose designs share `tokens.css` and `components.css` either copies them into every page, so the pages drift, or breaks the contract. The escape hatch, "a different portability contract" (`offline-artifact-contract.md:13`), names no replacement guarantees.
- **Hosts.** Verification step 2 says "open the file itself, not a development server" (`references/interaction-and-verification.md:14`). A tree that renders from disk can lose its styles on a host that serves it under a path prefix, publishes only one entry page, or refuses paths that climb above the entry. A `file://` check can't catch that.
- **Interactions.** The reference ends with "Use available browser tooling; no particular automation library is required" (`interaction-and-verification.md:21`). With only a headless browser, the agent has screenshots, which don't exercise behavior. In the session behind the issue, a control's click also reached a click-outside handler, so a panel opened and closed on the same click; only a scripted check caught it. Full-page screenshots of long pages are too tall to read.
- **Native surfaces.** Step 5 inspects "a narrow viewport around 320 CSS pixels" (`interaction-and-verification.md:17`). A menu-bar panel, desktop window, phone widget or watch face is drawn at the device's real scale and can't reflow to 320 px. Platform system fonts and symbols usually can't be embedded, so the choice between embedding and falling back (`offline-artifact-contract.md:21-25`) always ends in fallback, and the skill gives no guidance on recording it.

Outcome: the skill keeps the one-file sketch as the default and adds what long-lived, hosted, interactive and native-scale prototypes need. Each addition has a check the agent can run.

## Requirements

Design tree (issue part 1)
- R1: The skill names two portability contracts and when to use each. The design tree applies when the project already keeps shared design files or the user asks for them. The one-file artifact applies otherwise, and is the default for direction sketches. A sketch may keep its candidate tokens inline until a direction is chosen.
- R2: In a design tree, every page is a full HTML document that links shared files by relative path only. It uses no root-absolute paths, network, build step, imports or `fetch`, and it opens from disk and works offline as long as the tree stays together.
- R3: A static design-tree check confirms that every `href`, `src` and CSS `url()` resolves to a file inside the tree. It reports anything that points outside the tree or to a remote host.
- R4: The prototype notes list the shared files each page depends on.

Hosted review (issue part 2)
- R5: Verification keeps the `file://` check. When the artifact will be reviewed through a host, the agent also serves the exact file set from a local static server under a nested prefix such as `/a/b/` and repeats the render check. That result is recorded separately. When the agent can't open the host itself, it records the hosted render as "not performed" and asks the user to confirm it.
- R6: The skill describes an entry page for hosts that publish one page: a small page at the root of the tree that links or forwards to the view. The shared files are published at their tree-relative paths, so the view's relative paths still resolve.

Scripted checks (issue part 3)
- R7: A reference holds a tool-neutral harness-page recipe. The harness loads the prototype in a same-origin frame served over local HTTP. It dispatches pointer and keyboard events, lets timers run, and asserts on DOM state, focus and ARIA attributes. It writes PASS or FAIL into the DOM, so a headless browser that dumps the DOM can run it.
- R8: A scripted check is required for every stateful interaction the prototype demonstrates, such as open and close, timers and focus return, when no browser-driving tool can exercise it. When such a tool exists, the agent drives the interaction with it instead.
- R9: A reference holds a long-page recipe: screenshot the page in slices by loading it in a fixed-size frame and scrolling to each offset, instead of cropping one full-page image.
- R10: The notes' verification table records each scripted or driven check by name.

Native surfaces at a fixed scale (issue part 4)
- R11: A native-surface profile replaces the 320 px check for fixed-scale scenes. It states the scale mapping (for example 1 CSS px = 1 pt), renders each scene at that scale, and checks it at device scale factors 1 and 2.
- R12: Device geometry comes from sourced values kept as tokens: display size in points, system bar heights, safe areas and hardware cut-outs. The notes record each value's source.
- R13: The 320 px check applies to the page around the scenes. Each fixed-scale scene scrolls inside its own container, never the page.
- R14: Scenes render the platform's system font through `system-ui` and use drawn stand-ins for system symbols. The notes record both as fidelity limits.
- R15: Where the platform has them, the prototype shows its appearance and accessibility settings: light and dark, increased contrast, reduced transparency and reduced motion. A settings control in the page around the scenes, never inside a scene, switches them, and it starts from the operating system's settings through CSS media features.

Consistency
- R16: Every statement that a prototype is always one offline file is updated where it becomes false: `README.md:26`, `skills/product-design/guiding-product-discovery/templates/task-brief.md:21`, the product-design plugin description (`.claude-plugin/marketplace.json:61`) and the skill's description (`SKILL.md:3`). A new decision record amends the one-file clause of decision 0006.

## Acceptance criteria

- AC1 (R1): `SKILL.md` names the one-file artifact and the design tree, and says when each applies: the tree when the project already keeps shared design files or the user asks for them, and one file otherwise and by default for direction sketches. It also says a sketch may keep candidate tokens inline until a direction is chosen.
- AC2 (R1, R2, R4): Given a fixture project with `design/foundations/tokens.css` and `design/foundations/components.css`, when an agent following the skill refines a chosen direction into one view, the view page links both files by relative path, copies neither file's rules inline, and its notes list both files as dependencies.
- AC3 (R1): Given a fixture project with no shared design files, when an agent following the skill renders three direction sketches, each sketch is one HTML file that opens from disk with no other file present.
- AC4 (R2): The design-tree contract states each rule in R2: a full HTML document per page; relative paths only; no root-absolute path, network, build step, JavaScript module or CSS `@import`, or `fetch`; and every page opens from disk offline while the tree stays together.
- AC5 (R3): Given a fixture tree whose page has an `href` to `https://cdn.example.com/x.css`, a root-absolute `src="/img/logo.svg"`, a CSS `url()` that resolves outside the tree and an `href` to a missing file, the design-tree check reports all four, each with its file and reference. Once they are fixed, it reports the tree clean.
- AC6 (R5): The verification sequence keeps the `file://` step and adds a hosted step for artifacts reviewed through a host: serve the exact file set under `/a/b/` from a local static server, repeat the render check, and record the result in its own row of the notes' verification table.
- AC7 (R5, R6): Given the clean fixture tree from AC5 with an entry page at its root, served from a local static server under `/a/b/`, the entry page reaches the view, and the view renders with its shared stylesheets applied and no failed request for any file in the tree.
- AC8 (R5): The notes template's hosted-render row allows "not performed", and the skill tells the agent to ask the user to confirm the hosted render when it can't open the host itself.
- AC9 (R7): Given a fixture prototype whose control click also reaches a click-outside handler, so its panel opens and closes on one click, the harness page built from the recipe and run in a headless browser that dumps the DOM shows FAIL for "panel stays open after one click". Once the handler is fixed, it shows PASS.
- AC10 (R7): The harness recipe covers loading the prototype in a same-origin frame over local HTTP and says why: `file://` origins are opaque in most browsers. It also covers dispatching pointer and keyboard events, letting timers run, asserting DOM state, focus and ARIA attributes, and writing PASS or FAIL into the DOM.
- AC11 (R8): The verification guidance requires a scripted check for each stateful interaction when no browser-driving tool can exercise it, and says to drive the interaction with the tool when one exists.
- AC12 (R9): Given a fixture page 4,000 CSS px tall, the long-page recipe produces slices of one fixed frame height that together cover the page from top to bottom, with no full-page image cropped.
- AC13 (R10): The notes template's verification table has a row for each named scripted or driven check, for example "Scripted: panel closes on Escape and focus returns to its control".
- AC14 (R11): The native-surface profile states the scale mapping, with 1 CSS px = 1 pt as its example, renders scenes at it, checks them at device scale factors 1 and 2, and says it replaces the 320 px check for fixed-scale scenes.
- AC15 (R12): The profile keeps display size in points, system bar heights, safe areas and hardware cut-outs as tokens and requires each value's source. The notes template has a place to record those sources.
- AC16 (R13): Given a fixture page with a fixed-scale scene 800 CSS px wide, at a 320 CSS px viewport the page has no horizontal scroll and the scene scrolls inside its own container.
- AC17 (R14): The profile says to render the system font through `system-ui`, to draw stand-ins for system symbols, and to record both as fidelity limits in the notes.
- AC18 (R15): The profile says to show light and dark, increased contrast, reduced transparency and reduced motion through a settings control in the page around the scenes, never inside a scene. The control starts from `prefers-color-scheme`, `prefers-contrast`, `prefers-reduced-transparency` and `prefers-reduced-motion`.
- AC19 (R16): `README.md`, the coordinator's task brief, the plugin description and the skill description no longer say that every prototype is one file. A new record, numbered after 0015 and indexed in `decisions/README.md`, amends 0006's one-file clause, and 0006 itself is unchanged.

## Non-goals

- A native-surface variant of `exploring-visual-directions` and its shared platform frame (#10). This work item only defines the profile that #10 hands over to.
- Setting up a design system, proposing a design-folder layout, or graduating a direction into shared foundations (#11). The design-tree contract applies to a tree that exists or that the user asks for.
- Changing the one-file default for direction sketches, or the one-file line in `exploring-visual-directions/templates/direction-comparison.md:29`, which stays true for sketches.
- Publishing to any particular host or using a host's API. The skill describes the entry-page pattern and a local check.
- Requiring a particular browser, automation library or server.
- Tables of device geometry for specific platforms.
- Cutting a product-design release.

## Constraints

- Skill format (AGENTS.md "Skill format"): links stay inside the skill directory, and nothing assumes a particular harness, install path or environment variable. `SKILL.md` stays under 500 lines; it is 41 now. Depth goes in `references/`, copyable files in `templates/`.
- `scripts/validate.py:65` rejects the string `../` in every file of a skill directory, fenced code included. So the skill can't show a parent-relative path literally, which a design tree normally uses.
- Decision 0006 is accepted. AGENTS.md "Conduct": never rewrite an accepted record; add one or supersede it.
- Changelogs (AGENTS.md "Commits and changelogs"): each slice adds a user-facing entry under `[Unreleased]` in `skills/product-design/CHANGELOG.md`, which also covers the plugin's own entry in `marketplace.json`. The decision record gets an entry in the root `CHANGELOG.md`. Commits follow Conventional Commits with the category or skill as scope. `python3 scripts/validate.py` passes before each PR (CONTRIBUTING.md).
- External facts the guidance relies on:
  - `file://` origins are usually opaque, so same-folder files "may trigger CORS errors" ([MDN, Same-origin policy: File origins](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy#file_origins)).
  - WCAG 1.4.10 exempts "parts of the content which require two-dimensional layout for usage or meaning" from 320 CSS px reflow ([W3C Understanding Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)).
  - `prefers-reduced-transparency` is experimental and not Baseline ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency)), so the settings control must force each setting where the media feature is unavailable.
- Done and review: done means all three PR slices are merged to `main`, with `[Unreleased]` entries and the validator passing. The user reviews all three PRs ("All three", G1 round 1, 2026-10-23).

## Assumptions and open questions

- Assumption: "no imports" covers JavaScript modules and CSS `@import`, so every page links each stylesheet it uses and its dependency list is complete. Basis: inferred from the issue, because the check covers `href`, `src` and `url()` but not a bare `@import "x.css"`. If wrong: allow `@import` and extend the check to follow it.
- Assumption: classic, non-module shared scripts linked by `<script src>` are allowed in a tree. Basis: inferred; the issue says pages link "shared files", and classic scripts load from disk. If wrong: a tree shares only CSS and assets.
- Assumption: the hosted check is required for design trees reviewed through a host and optional for one-file artifacts. Basis: not asked, low impact, because a one-file artifact has no relative references to break. If wrong: AC6 and AC7 extend to one-file artifacts.
- Assumption: the skill ships no device values. The profile tells the agent to source each value for the project from the platform's own guidelines or specifications and record the source. Basis: not asked; device values change and each needs a citation. If wrong: a reference with sourced values for each platform, which needs ongoing upkeep.
- Assumption: the product-design release (a minor bump for new references and templates) is cut separately with `release-process` after the slices merge. Basis: AGENTS.md "Release". If wrong: G4 adds a release slice.
- Open: whether the design-tree check, the harness page and the long-page recipe ship as files the agent runs or copies (a script, an HTML template) or as described procedures, and how the skill shows a parent-relative path under the validator's `../` ban. Blocks: nothing at G1. Owner: G2. Resolved at G2: see Approach.
- Open: where the fixtures for AC2, AC3, AC5, AC7, AC9, AC12 and AC16 live (for example `evaluations/product-design/`) and which ACs a trial with a fresh agent checks. Blocks: nothing at G1. Owner: G3. Resolved at G3: see Verification.

## Approach

Chosen: B, browser-only templates. Parent paths are described in prose, with no change to the tooling. Agreed at G2, 2026-10-24: "B: browser templates (Recommended)", "Prose, no tooling change (Recommended)"

The skill gains prose references for the design-tree contract, scripted checks and the native-surface profile, plus three copyable HTML templates for checking. Each template is a standalone page with inline, non-module JavaScript, built like `templates/collection-example.html`, and needs only a browser and a static file server. For any check over HTTP, the agent copies the exact file set into a staging folder at `a/b/`, puts the filled-in template at the staging root, outside the tree, and serves the staging root with any static file server.

- `tree-check.html` starts from the entry page and the notes' page list. It reads each page's `href` and `src` and each stylesheet's `url()`, and reports every reference that is remote, resolves outside `/a/b/`, or returns no file. This one tool covers the static check (R3) and the nested-path check (R5).
- `interaction-harness.html` loads a page from `/a/b/` in a same-origin frame. It provides helpers that dispatch events, wait for timers and assert, and the agent writes only the checks.
- `page-slices.html` shows a page in a frame of fixed height, scrolled to `?offset=`, so any tool that screenshots a URL produces the slices.

Native surfaces stay prose: the profile describes the scene container and the settings control, with no template.

- Touches: `skills/product-design/building-html-prototypes/`: `SKILL.md`, `references/offline-artifact-contract.md`, `references/interaction-and-verification.md`, new `references/design-tree-contract.md`, `references/scripted-checks.md` and `references/native-surface-profile.md`, new `templates/tree-check.html`, `templates/interaction-harness.html` and `templates/page-slices.html`, and `templates/prototype-notes.md`. Outside the skill: `README.md:26`, `skills/product-design/guiding-product-discovery/templates/task-brief.md:21`, `.claude-plugin/marketplace.json:61`, a new decision record and its index entry, both changelogs, and fixtures in `evaluations/product-design/`.
- Reuses: the copyable-template pattern of `templates/prototype.html` and `templates/collection-example.html`; the notes' verification table (`templates/prototype-notes.md`), which gains rows rather than a new format; and the existing sequence in `interaction-and-verification.md`, which gains a hosted step.
- Contracts:
  - Staging layout: the tree is copied untouched to `<staging>/a/b/`, and the check templates sit at `<staging>/`. The agent serves `<staging>/` from the server root. Slice A defines this in the hosted step of `interaction-and-verification.md`; slices B and C refer to it and don't restate it.
  - Result format: every template writes its results into one element, `#results`, one line per check, as `PASS <name>` or `FAIL <name>: <detail>`, and ends with `DONE <passed>/<total>`. One DOM dump reads any template's result, and each name goes into the notes' verification table as it is (R10).
  - Notes template rows: slice A adds the hosted-render row (with "not performed" allowed) and the shared-files list; slice B adds one row per named scripted or driven check; slice C adds the scale mapping, the geometry sources and the fidelity limits.
  - Parent paths: no file in the skill contains the literal parent-path string. The prose says "paths that climb to a parent folder inside the tree". Fixtures that use parent paths live in `evaluations/product-design/`, which `check_self_containment` never scans (`scripts/validate.py:175-184,254`).
- Evidence:
  - Code: there is no `scripts/` folder in any skill; the only non-Markdown files are templates (`find skills -type f ! -name '*.md'`). The validator rejects the parent-path string (`scripts/validate.py:65`) and allows only three frontmatter fields (`:67`).
  - Decisions: 0002 keeps three frontmatter fields and leaves `compatibility` for a skill that needs a runtime (`decisions/0002-agent-skills-open-format.md`). 0006 fixes one file per prototype (`decisions/0006-product-design-discovery-skills.md:22`).
  - Sources:
    - The optional `scripts/` folder and the `compatibility` field ([agentskills.io/specification](https://agentskills.io/specification), retrieved 2026-10-24).
    - Opaque `file://` origins ([MDN, Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy#file_origins), retrieved 2026-10-24).
    - The two-dimensional layout exception in WCAG 2.2 SC 1.4.10 ([W3C](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), retrieved 2026-10-24).
    - `prefers-reduced-transparency`, experimental and not Baseline ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency), retrieved 2026-10-24).

Rejected alternatives:

- A, written recipes only: the agent rewrites the checker, harness and slicer on every run, so AC5, AC9 and AC12 would prove one run's code, not the skill.
- C, a Python script with templates: it assumes a Python runtime, against AGENTS.md's "nothing in it assumes a particular … environment". Declaring the runtime needs `compatibility`, which `scripts/validate.py:67` rejects, and it would be the first executable code in any skill.
- Narrowing the validator to allow parent paths in `templates/*.html`: it weakens a repository invariant for a need that prose covers.

Consequences:

- Easier: the checks repeat exactly from project to project. One checker serves both the static check and the hosted check. The results read the same through any tool that dumps the DOM.
- Harder: about 300 lines of template JavaScript to maintain in a skill, which you review in every PR.
- Risk: the checker only sees pages reachable from the entry page or listed in the notes. The AC5 fixture includes a page that only the notes list.
- Risk: a headless DOM dump must let timers run before it reads `#results`. G3 picks the tool and how long it waits.
- Revisit if: a project needs the tree check without a browser, such as in CI. That points to C.
- Decision records: `decisions/0016-design-trees-for-html-prototypes.md` (amends 0006's one-file clause) and `decisions/0017-browser-only-checks-for-html-prototypes.md`.

## Verification

Profile: `docs/product-engineering/verification-profile.md`, confirmed 2026-10-24
G3: agreed 2026-10-24, "Agreed"

"Cold read" below means: a fresh-context subagent receives only the path of the candidate skill directory in the worktree, plus the listed questions. The pass condition is that each answer states the AC's clause and cites a `file:line`, and that the verifier opens each cited line and finds the clause there. "Staged" means the fixture is copied to `<run>/a/b/`, with the filled-in template at `<run>/`, served by `python3 -m http.server` on `127.0.0.1`, and read with Chrome's `--headless --virtual-time-budget=5000 --dump-dom`. The fixtures live in `evaluations/product-design/fixtures/`.

| AC | Check | Layer | Tool | Steps | Pass condition |
|---|---|---|---|---|---|
| AC1 (R1) | Cold read: when each contract applies | ai-eval | subagent (Haiku) | Ask: which contract applies with shared design files, which when the user asks, which for direction sketches, and what may stay inline in a sketch | Four answers match AC1, each citing a line of `SKILL.md` |
| AC2 (R1, R2, R4) | Trial: refine a direction in a project with shared files | ai-eval | subagent (Sonnet), staged, headless Chrome | 1. Copy `fixtures/shared-foundations-project/` to `<run>/`. 2. A fresh agent following the candidate skill refines its chosen direction into one view. 3. Read the page and its notes. 4. Run `tree-check.html` on the result | The page links `design/foundations/tokens.css` and `design/foundations/components.css` by relative path; none of the custom properties defined in `tokens.css` is defined in the page; the notes list both files; the tree check ends `DONE n/n` with no `FAIL`. One trial; its transcript excerpt goes in the report |
| AC3 (R1) | Trial: three sketches without shared files | ai-eval | subagent (Sonnet), headless Chrome | 1. Copy `fixtures/no-shared-files-project/` to `<run>/`. 2. A fresh agent following the candidate skill renders three direction sketches. 3. Inspect each file, then open it through `file://` with `--dump-dom` | Three `.html` files; each `href` and `src` is a fragment, a `data:` URI or an outbound link; each DOM dump from `file://` contains the sketch's main heading. One trial |
| AC4 (R2) | Cold read: the design-tree rules | ai-eval | subagent (Haiku) | Ask for every rule a design-tree page must follow | The answers name each of: full HTML document, relative paths only, no root-absolute path, no network, no build step, no JavaScript module, no CSS `@import`, no `fetch`, opens from disk while the tree stays together. Each cites `references/design-tree-contract.md` |
| AC5 (R3) | Tree check on a broken tree, then the clean tree | e2e | headless Chrome, staged | 1. Stage `fixtures/broken-tree/`: one remote `href`, one root-absolute `src`, one `url()` outside the tree, one missing `href`, the last on a page that only the notes list. 2. Dump `tree-check.html`. 3. Repeat with `fixtures/clean-tree/` | Broken: exactly four `FAIL` lines, each naming its file and reference, and no request goes to `example.com`. Clean: no `FAIL`, ending `DONE n/n` |
| AC6 (R5) | Cold read: the hosted step | ai-eval | subagent (Haiku) | Ask: when the hosted step runs, the prefix, what is served, what is repeated, where the result goes | The answers match AC6, citing `references/interaction-and-verification.md` and the notes template's hosted row |
| AC7 (R5, R6) | Hosted render through the entry page, with a negative control | e2e | headless Chrome, staged, `interaction-harness.html` | 1. Stage `fixtures/clean-tree/` with its root entry page. 2. The harness loads `/a/b/index.html`, follows the entry page to the view, and reads a token's computed value. 3. Dump `tree-check.html`. 4. Negative control: stage only the view's folder at `/a/b/` and rerun step 2 | Steps 2 and 3: `PASS entry reaches view`, `PASS shared tokens applied`, and the tree check ends `DONE n/n`. Step 4: `FAIL shared tokens applied`, showing the check catches a host that publishes only the view |
| AC8 (R5) | Cold read and template read: "not performed" | ai-eval | subagent (Haiku) | Ask: what to record when the agent can't open the host, and what to ask the user | The answers state "not performed" and the request to confirm, citing the skill; `templates/prototype-notes.md` has a hosted-render row that lists "not performed" |
| AC9 (R7) | Harness catches the click-propagation bug | e2e | headless Chrome, staged | 1. Stage `fixtures/panel-bug/`, whose control click reaches a document click-outside handler. 2. Fill `interaction-harness.html` with checks: opens on click, stays open after one click, closes on Escape, focus returns to the control, `aria-expanded` follows, closes after the timeout. 3. Dump. 4. Repeat with `fixtures/panel-fixed/` | Bug: `FAIL panel stays open after one click`. Fixed: all six `PASS`, ending `DONE 6/6`. Each check name appears in the dump exactly as it will appear in the notes |
| AC10 (R7) | Cold read: the harness recipe | ai-eval | subagent (Haiku) | Ask how to load the prototype and why, how events, timers and assertions work, and how results are reported | The answers cover each clause of AC10, including opaque `file://` origins as the reason, citing `references/scripted-checks.md` |
| AC11 (R8) | Cold read: when a scripted check is required | ai-eval | subagent (Haiku) | Ask: when is a scripted check required, and what to do when a browser-driving tool exists | Required for each stateful interaction when no driver can exercise it; with a driver, drive it. Cites the skill |
| AC12 (R9) | Long page in slices | e2e | headless Chrome, staged, `page-slices.html` | 1. Stage `fixtures/long-page/`, 4,000 CSS px tall with bands labeled 0, 1000, 2000 and 3000. 2. For each offset, dump the DOM and take a 1,000 px-high screenshot of `page-slices.html?src=…&offset=<n>` | Each dump shows `PASS scrolled <n>`. Each of the four screenshots shows only its band's label at the top. No full-page image is produced |
| AC13 (R10) | Template read: named checks | ai-eval | subagent (Haiku) | Ask how a scripted or driven check is recorded | The notes template's verification table has a row form for a named scripted or driven check, with an example name |
| AC14 (R11) | Cold read: scale | ai-eval | subagent (Haiku) | Ask for the scale mapping, the device scale factors, and what replaces the 320 px check | The answers state 1 CSS px = 1 pt as the example, factors 1 and 2, and that it replaces the 320 px check for fixed-scale scenes, citing `references/native-surface-profile.md` |
| AC15 (R12) | Cold read and template read: geometry sources | ai-eval | subagent (Haiku) | Ask which device values become tokens and where their sources go | The four kinds of value named in AC15, a source required for each, and a place for those sources in the notes template |
| AC16 (R13) | Fixed-scale scene in a 320 px viewport | e2e | headless Chrome, staged, `interaction-harness.html` | 1. Stage `fixtures/native-scene/`, a page with an 800 CSS px scene built by the profile. 2. The harness loads it in a 320 px frame and measures the page's and the scene container's scroll widths | `PASS no page scroll at 320` (page `scrollWidth` ≤ 320) and `PASS scene scrolls in its container` (container `scrollWidth` > `clientWidth`, `overflow-x` is `auto` or `scroll`) |
| AC17 (R14) | Cold read: system type and symbols | ai-eval | subagent (Haiku) | Ask how to render system type and symbols, and what to record | `system-ui`, drawn stand-ins, and both recorded as fidelity limits, citing the profile |
| AC18 (R15) | Cold read: settings control | ai-eval | subagent (Haiku) | Ask which settings to show, where the control lives, and what it starts from | The four settings; a control in the page around the scenes, never inside one; starts from the four named media features; forces each setting where its media feature is unavailable |
| AC19 (R16) | One-file claims and the decision records | cli | `git grep`, `git diff`, validator | 1. `git grep -n -i "one offline HTML file\|independent offline HTML" -- README.md .claude-plugin/marketplace.json skills/product-design`. 2. `git diff origin/main -- decisions/0006-product-design-discovery-skills.md`. 3. `python3 scripts/validate.py` | Step 1: no line claims that every prototype is one file; remaining hits concern direction sketches only. Step 2: empty. Step 3: "0 errors"; `decisions/README.md` indexes 0016 and 0017 |
| All slices | Wording and voice | visual | user (human eye) | The PR's diff of the skill text, the templates' comments and the decision records | The user approves the PR ("All three", G1, 2026-10-23) |

### Automated checks

Every command runs on the candidate SHA and must pass. The baseline at 9982dc6 passes.

- `python3 scripts/validate.py`: "0 errors". Includes the parent-path ban for every file in the skill.
- `git diff --check origin/main...HEAD`: no output.

### Who certifies

- The agent self-certifies AC1 to AC19: content by cold read, behavior by trial, templates by staged headless runs, and claims by `git grep`.
- Human eye: the wording and voice of each PR. These rows are reported `blocked (human eye)` with the diff summary until the user reviews. They put every PR in the `human` category, which matches "All three".

### Environments and limits

- Allowed: local only, on `127.0.0.1` servers, scratchpad folders, this worktree, headless Chrome and subagents.
- Never: tags, releases, pushes or merges during verification, and no real host or artifact viewer. Per R5, a real host's render is the user's to confirm.
- Data: delete only scratchpad folders the run created. Stop every server the run started.
- Side effects: none. `example.com` (reserved for documentation, [RFC 2606](https://www.rfc-editor.org/rfc/rfc2606)) appears in fixtures only as a value the check must report without fetching.

### Mocks and what they exclude

- The fixture projects are invented: they exclude the variety of real design folders and hosts.
- Trials AC2 and AC3 run once each: they exclude run-to-run variance across agents and models.
- A local static server under `/a/b/` stands in for a host: it excludes host-specific rules beyond a path prefix and a single entry page, such as content security policies or upload limits.

### Harness gaps

- None needs Plan 0. Each slice builds its own fixtures in `evaluations/product-design/fixtures/`, together with an `evaluations/product-design/README.md` that lists the rerun commands.
- "How to verify" pointer in AGENTS.md: declined 2026-10-24, "Not now (Recommended)".
