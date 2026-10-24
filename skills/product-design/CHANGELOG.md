# Changelog

All notable changes to the `product-design` plugin are documented in this file. Changes to the marketplace and the repository around it are in the [root changelog](../../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this plugin adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are tagged `product-design--vX.Y.Z`.

## [Unreleased]

### Added

- `building-html-prototypes` can build a design tree: prototype pages that link the project's shared `tokens.css`, `components.css` and other design files by relative path instead of copying them, and that still open offline from disk while the tree stays together. Its rules are in a new design-tree contract, and the prototype notes name the contract and the tree's root folder, and list the shared files each page links.
- `templates/tree-check.html` in `building-html-prototypes`, a page you serve locally next to a staged copy of a design tree. It reads the references in the tree's pages and stylesheets and reports each one that points to a remote host, uses a root-absolute path, climbs out of the tree or names a missing file, as `PASS` and `FAIL` lines that a headless browser can read.
- `building-html-prototypes` exercises stateful interactions without a browser-driving tool. A new scripted-checks reference and `templates/interaction-harness.html` load the prototype in a same-origin frame over local HTTP, dispatch pointer and keyboard events, let timers run, and assert on DOM state, focus and ARIA attributes. A scripted check is required for every stateful interaction no browser-driving tool can exercise, and the notes record each check by name.
- `templates/page-slices.html` in `building-html-prototypes` shows a long page in a frame of fixed size scrolled to an offset, so a headless screenshot captures it in readable slices instead of one tall image.

### Changed

- A single offline HTML file stays the default, and direction sketches stay one file even in a project with shared design files; a sketch may keep its candidate tokens inline until you choose a direction. The skill, the plugin description, the repository README and the coordinator's task brief no longer say that every prototype is one file.

## [0.1.0] - 2026-09-28

### Added

- Six stack-neutral skills for guided discovery, product briefs, UX flows, visual direction exploration, offline HTML prototypes, and product/design handoffs. Includes copyable templates, fictional worked examples, typography and spacing guidance, and checkpoints for user decisions.

[Unreleased]: https://github.com/theultimate-dev/skills/compare/product-design--v0.1.0...HEAD
[0.1.0]: https://github.com/theultimate-dev/skills/releases/tag/product-design--v0.1.0
