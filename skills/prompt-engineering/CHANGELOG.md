# Changelog

All notable changes to the `prompt-engineering` plugin are documented in this file. Changes to the marketplace and the repository around it are in the [root changelog](../../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this plugin adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are tagged `prompt-engineering--vX.Y.Z`.

## [Unreleased]

### Added

- `improving-prompts` has notes for GPT-6 Astra. OpenAI's GPT-6 prompts were written from Astra's behaviour, so the notes apply them to Astra directly and add its API settings: no `none` effort, no sampling or log-probability parameters, and tool calling only through the Responses API. They also add OpenAI's advice on having the model name the skill instruction that made it pause, keeping skill descriptions short and AGENTS.md pointers tied to when each doc applies, and granting standing permission for workflows known to be safe. Where OpenAI's pages call Astra's clarifying questions a strength while its prompting guidance treats them as a cause of early stops, the notes say which page says what.
- `improving-prompts` has notes for GPT-6.1 Sol: effort from `low` to `max` with `medium` as the default and no `none` or `minimal`, tool calling only through the Responses API, and multi-agent delegation in beta. They add what its system card reports against GPT-6 Astra, such as pressing on past warnings more often, and say that no source shows whether a prompt changes it. OpenAI has published no prompting guidance specific to GPT-6.1 Sol, so the family's Astra-derived prompts are a starting point and the rest is listed as unconfirmed.

### Changed

- `improving-prompts` covers the GPT-6 family in one section. The GPT-6 Sol and Luna notes now list the log-probability parameters to remove when effort is above `none`, and describe Luna's intended use in the words OpenAI's pages now use: extraction, classification, transformation, and structured summaries.

## [0.2.0] - 2026-09-29

### Added

- `improving-prompts` has notes for Grok 4.7. xAI publishes no prompting guide for it, so the notes cover what its documentation states (always-on reasoning with an effort setting, parameters that return errors, parallel calls, schema guarantees, citations, cache-friendly ordering) and mark the rest as unconfirmed. The model notes and the source list now show a review date on each section or entry checked after the file's own date.
- `improving-prompts` has notes for GPT-6 Sol: its effort levels and API constraints, and what OpenAI's GPT-6 guide changes from GPT-5.x, namely more clarifying questions and earlier stops, sensitivity to conflicting instruction files, heavier formatting, unprompted testing, and less delegation. The guide's prompts were written from GPT-6 Astra, so the notes present them as a starting point for Sol and list what stays unconfirmed.
- `improving-prompts` has notes for GPT-6 Luna. Luna shares GPT-6 Sol's effort levels, API constraints, and family guidance, and the notes add what OpenAI says Luna is for: focused, high-volume work such as summarization, extraction, and focused coding. OpenAI has published no Luna-specific prompting guidance, so its behaviour stays unconfirmed.
- `improving-prompts` has notes for Claude Opus 5.5, from Anthropic's Opus 5.5 guide, migration guide, and system card. They cover always-on thinking with `medium` as the default effort; removing thinking and reasoning-in-the-response instructions; the rejected forced tool choice; progress updates that arrive as thinking blocks; early stops on unattended runs; exploring before acting in multi-app work; time signals for agent teams; marking pasted text; and frontend and visual inputs. They also list which Opus 5 adjustments no source confirms for Opus 5.5. The reasoning reference now rejects manual chain of thought for models that can decline requests to write out their reasoning, and prefers a lower effort setting over prompt text where the provider says effort is the more reliable control.
- `improving-prompts` has notes for Claude Sonnet 5.5, from Anthropic's Sonnet 5.5 guide, migration guide, and system card, published at launch on 2026-09-28. They cover recalibrated effort with a `high` API default; the `between_tools` setting; a think-first line for JSON answers on reasoning tasks; early check-ins and skipped checks at low effort, unrequested additions at every level, and self-started review rounds at the top levels; progress updates that arrive as thinking blocks; under-used search in chat; mid-turn user messages misread as injections; and the loss of the context awareness that the Sonnet 5 notes relied on. The reasoning reference now allows a measured think-first line and treats the self-check as depending on effort where the provider says so.

## [0.1.0] - 2026-09-28

### Added

- `improving-prompts` skill: rewrites a rough prompt into an engineered one by classifying where it will run, diagnosing its gaps, and applying only the prompt and context engineering techniques that close them. Returns the techniques applied and rejected with reasons, placeholders for facts it could not infer, settings that belong outside the prompt, and the enhanced prompt in a copy-paste-ready tag. Ships a technique catalog split by group, dated model-family notes, worked examples, and templates.

[Unreleased]: https://github.com/theultimate-dev/skills/compare/prompt-engineering--v0.2.0...HEAD
[0.2.0]: https://github.com/theultimate-dev/skills/compare/prompt-engineering--v0.1.0...prompt-engineering--v0.2.0
[0.1.0]: https://github.com/theultimate-dev/skills/releases/tag/prompt-engineering--v0.1.0
