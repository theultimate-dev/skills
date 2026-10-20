# Changelog

All notable changes to the `theultimate-dev` marketplace and the repository around it are documented in this file: the plugin catalog, install routes, release assets, repository tooling, and every plugin release, with a link to its notes. Each plugin keeps its own changelog:

- [`foundations`](skills/foundations/CHANGELOG.md)
- [`harness-engineering`](skills/harness-engineering/CHANGELOG.md)
- [`product-context`](skills/product-context/CHANGELOG.md)
- [`product-design`](skills/product-design/CHANGELOG.md)
- [`product-engineering`](skills/product-engineering/CHANGELOG.md)
- [`prompt-engineering`](skills/prompt-engineering/CHANGELOG.md)

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Marketplace releases are tagged `vX.Y.Z`. Every plugin release is also a marketplace release, which lists the plugins released under Changed.

## [Unreleased]

### Added

- `product-context` plugin, for skills that keep a long-running product's whole context in a Markdown repository apart from the code: requirements, architecture, decisions, and a roadmap of bets that the `product-engineering` loop builds. It starts with `structuring-product-context`. Decision 0013 records why the product's context gets a category of its own, and decision 0014 records how `product-engineering` implements its bets.
- Evaluation scenarios for `product-context`: nine trials, from adopting over-stuffed product documents to closing a bet and auditing for drift, using a fictional product.
- Six scenarios in the `product-engineering` catalog for bets: intake and import, the appetite circuit breaker, a context change at G2, drift after the pin, the hand-back, and a check that work items without a bet behave as before.

## [0.2.1] - 2026-10-14

### Added

- A plugin can have a README of its own, the page GitHub shows at `skills/<category>/`, with its images and their HTML sources in `visuals/<category>/`. Decision 0015 records the layout, and the validator checks that every link and image in the README resolves.
- `scripts/render_visuals.py` renders the visuals in `visuals/<category>/` from their HTML sources to PNG, in The Ultimate Dev's dark and light themes, so a plugin README's images can be regenerated when the plugin changes.

### Changed

- Plugins released with this version:
  - `harness-engineering` [0.1.1](https://github.com/theultimate-dev/skills/releases/tag/harness-engineering--v0.1.1): a page of its own on GitHub, with how `marginal-gains` works from one session to the next and every install route, tested; the plugin's homepage now points there.

## [0.2.0] - 2026-10-14

### Added

- `harness-engineering` plugin, for skills that improve the harness your agents run on: instruction files, skills, memory, hooks and permissions, repository checks, and your own prompts. It starts with `marginal-gains`. Decision 0012 records why the harness gets a category of its own rather than joining `prompt-engineering`.

### Changed

- Plugins released with this version:
  - `harness-engineering` [0.1.0](https://github.com/theultimate-dev/skills/releases/tag/harness-engineering--v0.1.0): first release, with `marginal-gains`: at the end of a session, two or three small harness changes ranked by the session's evidence and your goals, followed up across sessions in a ledger.
  - `prompt-engineering` [0.4.0](https://github.com/theultimate-dev/skills/releases/tag/prompt-engineering--v0.4.0): `improving-prompts` has notes for Claude Haiku 5.5, including effort and what changed from prompts written for Haiku 4.5.

## [0.1.3] - 2026-09-30

### Changed

- Plugins released with this version:
  - `prompt-engineering` [0.3.0](https://github.com/theultimate-dev/skills/releases/tag/prompt-engineering--v0.3.0): `improving-prompts` has notes for GPT-6 Astra and GPT-6.1 Sol, and covers the whole GPT-6 family in one section.

## [0.1.2] - 2026-09-29

### Added

- Evaluation scenarios for the `release-process` option that releases the root with every component release, with a script that builds a throwaway marketplace to run them in and a script that runs the release workflow's checks on a tag locally.

### Changed

- Plugins released with this version:
  - `foundations` [0.2.0](https://github.com/theultimate-dev/skills/releases/tag/foundations--v0.2.0): `release-process` can release the root with every component release, so a marketplace's Latest release always names the newest plugin versions, and its components workflow template can enforce that.

## [0.1.1] - 2026-09-29

### Changed

- Plugins released with this version:
  - `foundations` [0.1.1](https://github.com/theultimate-dev/skills/releases/tag/foundations--v0.1.1): `release-process` explains correctly why a plugin's release can show as Latest before the first marketplace release.
  - `prompt-engineering` [0.2.0](https://github.com/theultimate-dev/skills/releases/tag/prompt-engineering--v0.2.0): `improving-prompts` has notes for Grok 4.7, GPT-6 Sol and Luna, and Claude Opus 5.5 and Sonnet 5.5.
- Every plugin release now also releases the marketplace, with at least a patch bump, so the Latest release on GitHub always names the newest plugin versions. Its notes list each plugin released with its new version and a link to that plugin's release. Decision 0011 records the rule.
- `scripts/validate.py` requires this changelog to link every plugin release made after the first marketplace release, and refuses a link to a plugin release that does not exist.
- The release workflow refuses a plugin tag unless the marketplace release at the same commit lists that plugin release.

## [0.1.0] - 2026-09-28

### Added

- Plugin marketplace with four plugins, one per category: `foundations`, `product-design`, `product-engineering`, and `prompt-engineering`. Claude Code and Copilot CLI install a category as one plugin, and each plugin carries its own version and changelog.
- Product-engineering evaluation guide with lifecycle diagrams, a runnable fixture and grader, and behavioral scenarios for interviews, real app verification, per-lens review recall, PR categorization, merge safety, and stacked PRs.
- Decision log in `decisions/` recording why the repository and its release process are shaped the way they are.
- `scripts/validate.py` and a CI workflow that enforce the repository rules on every push and pull request, including a changelog per plugin whose newest release matches the plugin's version.
- Release workflow for tags on `main`:
  - A `vX.Y.Z` tag publishes a marketplace release, with that version's section of this changelog as notes. It is marked Latest.
  - A `<plugin>--vX.Y.Z` tag publishes that plugin's release: the section from its changelog, one archive per skill in the plugin, and checksums.
  - Either tag is refused unless `marketplace.json` declares the tag's version.
  - A tag that GitHub did not act on can be released by hand from the Actions tab.

### Security

- Published releases are immutable: their archives, `checksums.txt` and tag cannot change after publication.
- The CI and release workflows run `actions/checkout` pinned to a full commit SHA, and Dependabot proposes updates to it weekly.

[Unreleased]: https://github.com/theultimate-dev/skills/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/theultimate-dev/skills/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/theultimate-dev/skills/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/theultimate-dev/skills/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/theultimate-dev/skills/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/theultimate-dev/skills/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/theultimate-dev/skills/releases/tag/v0.1.0
