# Changelog

All notable changes to the `dev-environment` plugin are documented in this file. Changes to the marketplace and the repository around it are in the [root changelog](../../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this plugin adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are tagged `dev-environment--vX.Y.Z`.

## [Unreleased]

## [0.1.0] - 2026-11-17

### Added

- `reclaiming-docker-disk-space` skill: when your Docker disk is full, ask your agent to clean it up. It removes the data nothing uses any more and that is older than an age you pick, 24 hours by default: stopped containers, unused networks, unused images, build cache and anonymous volumes. The cleanup is one bundled shell script, so it runs the same way every time:
  - a dry run first shows where the space is and every volume that would go
  - anything a container uses is kept, however old
  - named volumes are never removed; the unused ones are listed for you to decide
  - on Colima the disk is trimmed afterwards, so macOS gets the space back

[Unreleased]: https://github.com/theultimate-dev/skills/compare/dev-environment--v0.1.0...HEAD
[0.1.0]: https://github.com/theultimate-dev/skills/releases/tag/dev-environment--v0.1.0
