# Changelog

All notable changes to the `prompt-engineering` plugin are documented in this file. Changes to the marketplace and the repository around it are in the [root changelog](../../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this plugin adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are tagged `prompt-engineering--vX.Y.Z`.

## [Unreleased]

### Added

- `improving-prompts` has notes for Grok 4.7. xAI publishes no prompting guide for it, so the notes cover what its documentation states (always-on reasoning with an effort setting, parameters that return errors, parallel calls, schema guarantees, citations, cache-friendly ordering) and mark the rest as unconfirmed. The model notes and the source list now show a review date on each section or entry checked after the file's own date.

## [0.1.0] - 2026-09-28

### Added

- `improving-prompts` skill: rewrites a rough prompt into an engineered one by classifying where it will run, diagnosing its gaps, and applying only the prompt and context engineering techniques that close them. Returns the techniques applied and rejected with reasons, placeholders for facts it could not infer, settings that belong outside the prompt, and the enhanced prompt in a copy-paste-ready tag. Ships a technique catalog split by group, dated model-family notes, worked examples, and templates.

[Unreleased]: https://github.com/theultimate-dev/skills/compare/prompt-engineering--v0.1.0...HEAD
[0.1.0]: https://github.com/theultimate-dev/skills/releases/tag/prompt-engineering--v0.1.0
