# Changelog

All notable changes to the `theultimate-dev` marketplace and the repository around it are documented in this file: the plugin catalog, install routes, release assets, and repository tooling. Each plugin keeps its own changelog:

- [`foundations`](skills/foundations/CHANGELOG.md)
- [`product-design`](skills/product-design/CHANGELOG.md)
- [`product-engineering`](skills/product-engineering/CHANGELOG.md)
- [`prompt-engineering`](skills/prompt-engineering/CHANGELOG.md)

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Marketplace releases are tagged `vX.Y.Z`.

## [Unreleased]

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

[Unreleased]: https://github.com/theultimate-dev/skills/commits/main
