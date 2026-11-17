# 0022: Package architecture work on existing applications as a `software-architecture` category

- Status: accepted
- Date: 2026-11-17

## Context

A long-lived application needs its architecture looked at more than once: when someone joins it, before a consequential change, when it feels heavier than its job. The marketplace covers two neighbouring cases. `designing-system-architecture` writes the architecture of a planned product inside a product context repository ([0013](0013-product-context-category.md)), and `brainstorming-solutions` chooses how to build one work item. Neither recovers what an existing application really is, takes a critical look at it, compares system-level options or simplifies it, and neither works in a plain code repository with no other plugin installed.

Two more things shaped the decision. Other people have to be able to look at the result without being told to install one tool for diagrams and another for boards. And the author works in the git project, in a terminal, so the architecture has to live as text in the repository.

## Options

1. **Extend `product-context`.** One home for everything called architecture, but its skills assume a separate context repository with versions and bets. A client's code repository has neither, and the plugin would have to be installed for one skill.
2. **Add an architecture mode to `brainstorming-solutions` and `reviewing-code-changes`.** No new plugin, but both work at the level of one work item or one change, and neither leaves standing views behind.
3. **A standalone `software-architecture` category of five skills.** Costs a ninth plugin and a boundary to keep with three neighbours. Works in any repository on its own.

For the medium: Mermaid, D2 and LikeC4 cost about the same to write, and hand-written HTML about four times as much. Mermaid is the one GitHub, editors and a single HTML page can all draw. A board file format was considered and dropped: a table, a mindmap, a quadrant chart and two views side by side cover what a board was for.

## Decision

Option 3. `software-architecture` is a category and plugin, starting at `0.0.0`, with five skills: `recovering-built-architecture`, `evaluating-architecture-risks`, `exploring-architecture-options`, `simplifying-system-architecture` and `drawing-architecture-views`. There is no coordinator skill; each skill's report names the skill that fits next. Two more skills, for planning an evolution and checking drift, wait until these five have been used on real applications.

- **Standalone.** Every skill works in any repository with no other plugin installed. When `drawing-architecture-views` is missing, the other four write their views in Markdown and say that the page was not rebuilt.
- **Where the work lives.** A skill reads the repository's `AGENTS.md` or `CLAUDE.md` and uses the architecture folder and the decision log they point to. Where they point nowhere, it uses `context/architecture/` and `context/decisions/`, the names the other plugins use. Standing views describe the system, as `built` or `planned`. Dated studies under `studies/` hold reviews, option comparisons and simplifications, and never edit a standing view. The skills commit nothing.
- **The view format.** One view per Markdown file: a status line, a Mermaid diagram, an Elements table and a Relationships table with an evidence cell for every row, and one stable id per element across all views. The shape matches the view template of `structuring-prototype-context` and adds the evidence column and the `Verified:` line. The two templates are kept compatible by convention and are not mirrored, because each plugin's template names its own statuses and rules.
- **Notation.** Mermaid only, in six diagram types, with C4 views drawn as flowcharts with styled nodes and at most 12 to 15 elements in a view. Past roughly ten views a model-based tool such as LikeC4 is the route, described in a reference and not built.
- **What people look at.** One built file, `architecture.html`, beside the index, holding a copy of every view and study. The agent copies the template once and afterwards only replaces source blocks between marker lines. The page writes `PASS`, `FAIL` and `DONE` lines as text, the form [0017](0017-browser-only-checks-for-html-prototypes.md) uses, and ships as browser-only HTML with inline, non-module JavaScript.
- **A CDN, on purpose.** The page loads Mermaid from one pinned address with an exact version. This departs from the offline rule of `building-html-prototypes`, where every file must open with no network. The reason is size: the library inside the file makes it 5.6 MB, against about 25 KB plus the sources. With no network the page says so and shows the sources as text. The offline answer is the page's Save button, which writes a copy that carries the drawn pictures and no library. That copy is made by a person in a browser and is not committed.
- **Inside other contexts.** In a prototype context the skills follow its map and its view template, put studies in `architecture/studies/`, and may build `architecture/architecture.html` there; the prototype profile gains that one exception to "Markdown only". For a product context repository they write no standing view and hand a study over as input to `designing-system-architecture`. Product context repositories stay Markdown only.
- **Boundaries with the neighbours.** `recovering-built-architecture` is not for a product context repository's baseline (`designing-system-architecture`). `exploring-architecture-options` is not for choosing how to build one work item (`brainstorming-solutions`) or for a prototype idea (`framing-prototype-ideas`); the split is by level, and `brainstorming-solutions` and `designing-system-architecture` each gain one sentence that names the other side. `evaluating-architecture-risks` is not for reviewing a code change (`reviewing-code-changes`).
- **Mirrors.** Under [0019](0019-mirror-shared-templates-across-skills.md), `templates/view.md` and `references/view-conventions.md` have their source in `drawing-architecture-views` and a copy in each of the other four skills, and `references/scenario-intake.md` has its source in `evaluating-architecture-risks` and a copy in `exploring-architecture-options` and `simplifying-system-architecture`. Ten pairs, listed in `scripts/validate.py`.
- The skills are project-agnostic and harness-neutral under [0002](0002-agent-skills-open-format.md), and the plugin is the install unit under [0003](0003-categories-as-directories.md). [0013](0013-product-context-category.md), [0017](0017-browser-only-checks-for-html-prototypes.md), [0020](0020-product-prototyping-category.md) and [0021](0021-dev-environment-category-with-shell-scripts.md) stay unchanged. The skills ship no script: the page's checks run in the browser that draws it, and building the page is a text edit an agent can do with or without a shell.

## Consequences

- A ninth plugin. Its first release, `software-architecture--v0.1.0`, is a minor marketplace release under [0011](0011-marketplace-release-with-every-plugin-release.md).
- The built page needs the network once to draw, unless someone saved an offline copy. A reader behind a firewall that blocks the CDN sees the sources as text and a message, not a broken page.
- The pinned Mermaid version is a line someone has to move. A new version is pinned only after the page's checks pass on it.
- `architecture.html` is a built file in the repository and can fall behind its sources. Every skill run that changes a view rebuilds it or says it is out of date, and the page shows the date and the commit it was built from.
- Three plugins now touch architecture. The skill descriptions each name the neighbour to use instead, and the boundary needs watching as the two later skills arrive.
- Ten mirrored files tie the five skills together: a change to a source changes every copy in the same commit.
- The view template can drift from `structuring-prototype-context`'s, since no check ties them. A change to either is a reason to read the other.
