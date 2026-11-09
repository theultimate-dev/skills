# Changelog

All notable changes to the `product-prototyping` plugin are documented in this file. Changes to the marketplace and the repository around it are in the [root changelog](../../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this plugin adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are tagged `product-prototyping--vX.Y.Z`.

## [Unreleased]

### Added

- A README for the plugin, the page GitHub shows at `skills/product-prototyping/`: what each of the five skills does, how a bet moves between its two gates, the `context/` folder beside your code, when to use this plugin or `product-context`, and every install route.

### Changed

- The plugin's homepage in the marketplace opens this page instead of the repository.
- Approving a bet now starts its build, and the build runs on its own until you have something to try. It decides what stays inside the bet and records those choices for you to read at Gate 2, and it comes back early only for what only you can answer, such as a credential, a decision the bet relies on or anything a revert cannot undo. Say so when you approve if you want the build held.
- A build now commits each step as soon as its checks pass, before planning the next, rather than leaving the work for commits at the end.
- Commit messages in a bet are Conventional Commits by default. When your project's instructions, contributing guide or commit tooling state another convention, the agent follows that one.

## [0.1.0] - 2026-11-08

### Added

- `structuring-prototype-context` skill: sets up the context of a prototype in a `context/` folder beside its code, in a light profile with no versions: requirements that are either built or dropped with a reason, architecture views marked built or planned, decisions, one file per bet, one file of open questions and risks, and a Keep a Changelog file per app. It adopts the README, specs and agent instructions you already have through a map you approve, and records the trigger that later moves the context to `product-context`.
- `framing-prototype-ideas` skill: thinks an idea through before any bet exists. It reads the context, the code and the relevant docs, checks whether a decision, a dropped requirement or an earlier note already settles it, compares two or three options, recommends one, says what would make you remove it after a try, and ends with a one-page note and a verdict: shape, park or stop.
- `shaping-prototype-bets` skill: turns a framed idea into one bet of half a day to two days, with an observable outcome, the requirement changes and their reserved IDs, checks that each say how they are proved, no-gos, rabbit holes, scope that may be cut, a keep-or-remove signal, and what the agent may do on its own. You approve the bet, and it records the commit you approved it at.
- `building-prototype-bets` skill: builds an approved bet in a loop until the result matches its intent: plan, implement in small commits within what you allowed, prove every check by its method, have a fresh reviewer compare the result with the bet, fix, repeat. It cuts scope or stops when the appetite runs out, adds the changelog entry, and leaves you the steps to try it.
- `closing-prototype-bets` skill: asks you to keep or remove a bet once you have tried it. Keep marks its requirements and architecture as built and records the decisions it made. Remove reverts its code, records its requirements as dropped with your reason, and writes the lesson. Either way it rebuilds the board and the indexes.

[Unreleased]: https://github.com/theultimate-dev/skills/compare/product-prototyping--v0.1.0...HEAD
[0.1.0]: https://github.com/theultimate-dev/skills/releases/tag/product-prototyping--v0.1.0
