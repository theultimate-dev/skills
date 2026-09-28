# Changelog

All notable changes to the `product-engineering` plugin are documented in this file. Changes to the marketplace and the repository around it are in the [root changelog](../../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this plugin adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are tagged `product-engineering--vX.Y.Z`.

## [Unreleased]

## [0.1.0] - 2026-09-28

### Added

- Nine skills built around one implementation loop. `running-implementation-loops` picks the track for the work item (quick fix, bugfix, small change, feature, new app, refactor, spike) and runs the stages it needs.
- Four stages where you take part:
  - `specifying-work-items` interviews you and writes `spec.md`.
  - `brainstorming-solutions` lays out distinct approaches for you to pick from.
  - `defining-verification` agrees how the agent will prove the work runs.
  - `planning-implementation` turns it into a roadmap of PR slices with an autonomy contract you approve.
- Four stages the agent runs alone:
  - `implementing-plans` builds each slice.
  - `verifying-implementation` starts the app and drives it (browser, API, CLI) to observe every acceptance criterion.
  - `reviewing-code-changes` runs a quick intent review before the PR and a five-lens review (architecture, security, conventions and idioms, efficiency, intent) on it.
  - `shipping-pull-requests` opens one PR per slice, marks it for human or agent review, and merges agent-reviewed PRs only when checks pass on the reviewed head and you authorized it.

[Unreleased]: https://github.com/theultimate-dev/skills/compare/product-engineering--v0.1.0...HEAD
[0.1.0]: https://github.com/theultimate-dev/skills/releases/tag/product-engineering--v0.1.0
