# Changelog

All notable changes to the `harness-engineering` plugin are documented in this file. Changes to the marketplace and the repository around it are in the [root changelog](../../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this plugin adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are tagged `harness-engineering--vX.Y.Z`.

## [Unreleased]

## [0.1.1] - 2026-10-14

### Added

- A README for the plugin, the page GitHub shows at `skills/harness-engineering/`: what the plugin is, how `marginal-gains` works from one session to the next, why small changes that hold compound, where the name comes from, and every install route.

### Changed

- The plugin's `homepage` in the marketplace manifest points at that page instead of the repository.

## [0.1.0] - 2026-10-14

### Added

- `marginal-gains` skill: run it at the end of a session with your agent to get two or three small changes to your harness that would pay off most, the most crucial first. It looks at instruction files, skills, memory, hooks and permissions, repository checks, and the way you prompt. Each suggestion quotes what happened in the session, gives the exact change, small enough to apply in minutes, and says what the next session should show if it worked. A ledger you keep outside your repositories carries the results forward:
  - changes you applied are checked against the next session
  - changes that slipped come back with a firmer fix
  - suggestions you declined stay out
  - friction that keeps recurring ranks higher each time

  Your goals, listed at the top of the ledger, decide which improvements matter most.

[Unreleased]: https://github.com/theultimate-dev/skills/compare/harness-engineering--v0.1.1...HEAD
[0.1.1]: https://github.com/theultimate-dev/skills/compare/harness-engineering--v0.1.0...harness-engineering--v0.1.1
[0.1.0]: https://github.com/theultimate-dev/skills/releases/tag/harness-engineering--v0.1.0
