# Changelog

All notable changes to the `theultimate-dev` marketplace and the repository around it are documented in this file: the plugin catalog, install routes, release assets, repository tooling, and every plugin release, with a link to its notes. Each plugin keeps its own changelog:

- [`foundations`](skills/foundations/CHANGELOG.md)
- [`product-design`](skills/product-design/CHANGELOG.md)
- [`product-engineering`](skills/product-engineering/CHANGELOG.md)
- [`prompt-engineering`](skills/prompt-engineering/CHANGELOG.md)

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Marketplace releases are tagged `vX.Y.Z`. Every plugin release is also a marketplace release, which lists the plugins released under Changed.

## [Unreleased]

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

[Unreleased]: https://github.com/theultimate-dev/skills/compare/v0.1.3...HEAD
[0.1.3]: https://github.com/theultimate-dev/skills/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/theultimate-dev/skills/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/theultimate-dev/skills/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/theultimate-dev/skills/releases/tag/v0.1.0
