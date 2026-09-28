# Changelog

All notable changes to the `foundations` plugin are documented in this file. Changes to the marketplace and the repository around it are in the [root changelog](../../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this plugin adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are tagged `foundations--vX.Y.Z`.

## [Unreleased]

### Fixed

- `release-process` explains why a component release shows as Latest before the first root release: GitHub falls back to the newest tag date until a release is marked Latest. It no longer blames a missing `--latest=false` for that.

## [0.1.0] - 2026-09-28

### Added

- Two skills: `decision-records` keeps a project's decision log, `release-process` keeps its changelog and cuts tagged releases.
- `release-process` also handles repositories whose components, such as packages or plugins, are versioned independently. Each component gets its own changelog and `name--vX.Y.Z` tags, and one release commit can release several components. A second workflow template releases both root `vX.Y.Z` tags and component tags, and can be run by hand for a tag GitHub skipped.

[Unreleased]: https://github.com/theultimate-dev/skills/compare/foundations--v0.1.0...HEAD
[0.1.0]: https://github.com/theultimate-dev/skills/releases/tag/foundations--v0.1.0
