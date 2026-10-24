# 0017: Ship the HTML prototype checks as browser-only templates

- Status: accepted
- Date: 2026-10-24

## Context

The design tree in 0016, hosted review and stateful interactions each need a check that the agent runs the same way on every project. Today the skill only lists what to check and says no particular automation library is required. No skill in this repository ships executable code. Under 0002 the frontmatter carries three fields, so a skill cannot declare a runtime with `compatibility`, and `AGENTS.md` requires that nothing in a skill assume a particular harness or environment. The skill's verification already uses a browser when one is available.

## Options

1. **Written recipes only.** No code to maintain. Lost: the agent rewrites the checker, harness and slicer on every run, so a check proves that run's code, not the skill.
2. **Copyable HTML templates with inline, non-module JavaScript, run in a browser over any static file server.** Matches the skill's existing templates and needs nothing the verification does not already use. Won.
3. **A standard-library Python script for the tree check, HTML for the rest.** Runs without a browser. Lost: it assumes a Python runtime, declaring that runtime needs a frontmatter field 0002 excludes, and it would be the first executable code in a skill.

## Decision

Option 2. `building-html-prototypes` ships `templates/tree-check.html`, `templates/interaction-harness.html` and `templates/page-slices.html`.

- **Staging**: the agent copies the exact file set, untouched, to `<staging>/a/b/`, puts the filled-in templates at `<staging>/`, and serves `<staging>/` with any static file server.
- **Results**: every template writes into one `#results` element, one line per check as `PASS <name>` or `FAIL <name>: <detail>`, ending with `DONE <passed>/<total>`. Any tool that dumps the DOM can read them, and each name goes into the notes' verification table as it is.
- **Parent paths**: no file in the skill contains a literal parent-path string, which the validator rejects. The prose describes such paths in words, and fixtures that need them live in `evaluations/product-design/`.

## Consequences

- The checks repeat exactly from project to project. One checker covers the static check and the hosted check, and the results read the same through any tool.
- About 300 lines of template JavaScript need maintenance and review. Without a browser, the checks fall back to manual steps marked unverified, as the skill already says.
- Revisit if a project needs the tree check without a browser, such as in CI. A script would then need a change to 0002's frontmatter rule.
