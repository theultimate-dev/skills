# Changelog

All notable changes to the `product-context` plugin are documented in this file. Changes to the marketplace and the repository around it are in the [root changelog](../../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this plugin adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are tagged `product-context--vX.Y.Z`.

## [Unreleased]

### Added

- `structuring-product-context` skill: sets up a product context repository, a Markdown repository kept apart from the code that holds a long-running product's whole context in layers sorted by how often they change: product, architecture, decisions, and a roadmap of bets. It adopts the documents you already have by mapping every section to its new home, raising conflicts and duplicates as open questions, and moving nothing until you approve the map. It writes the `AGENTS.md` map and the house rules that keep the repository coherent over months.

[Unreleased]: https://github.com/theultimate-dev/skills/commits/main/skills/product-context
