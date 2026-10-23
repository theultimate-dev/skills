# Changelog

All notable changes to the `foundations` plugin are documented in this file. Changes to the marketplace and the repository around it are in the [root changelog](../../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this plugin adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are tagged `foundations--vX.Y.Z`.

## [Unreleased]

## [0.2.1] - 2026-10-23

### Fixed

- `release-process` now covers a `main` that accepts changes only through pull requests, such as one behind a ruleset: the release commit goes in a pull request merged with a merge commit, and the tags go on the commit that reaches `main`. Its preflight no longer rules that branch out.

## [0.2.0] - 2026-09-29

### Added

- `release-process` can release the root with every component release, so the Latest release of a plugin marketplace or another catalog always names the newest component versions and links to their releases. A new reference covers when the option fits, the root bump (at least a patch), the notes format, the order to push tags in, catching up releases that skipped the root, and a check to add to a project's own validator. Setting up independent versions now asks whether to adopt it.
- The components workflow template can refuse a component tag unless the root release in the same commit lists it. Set `ROOT_FOLLOWS_COMPONENTS` to `"true"` to turn the check on; it is off by default, and component pre-releases are exempt.

## [0.1.1] - 2026-09-29

### Fixed

- `release-process` explains why a component release shows as Latest before the first root release: GitHub falls back to the newest tag date until a release is marked Latest. It no longer blames a missing `--latest=false` for that.

## [0.1.0] - 2026-09-28

### Added

- Two skills: `decision-records` keeps a project's decision log, `release-process` keeps its changelog and cuts tagged releases.
- `release-process` also handles repositories whose components, such as packages or plugins, are versioned independently. Each component gets its own changelog and `name--vX.Y.Z` tags, and one release commit can release several components. A second workflow template releases both root `vX.Y.Z` tags and component tags, and can be run by hand for a tag GitHub skipped.

[Unreleased]: https://github.com/theultimate-dev/skills/compare/foundations--v0.2.1...HEAD
[0.2.1]: https://github.com/theultimate-dev/skills/compare/foundations--v0.2.0...foundations--v0.2.1
[0.2.0]: https://github.com/theultimate-dev/skills/compare/foundations--v0.1.1...foundations--v0.2.0
[0.1.1]: https://github.com/theultimate-dev/skills/compare/foundations--v0.1.0...foundations--v0.1.1
[0.1.0]: https://github.com/theultimate-dev/skills/releases/tag/foundations--v0.1.0
