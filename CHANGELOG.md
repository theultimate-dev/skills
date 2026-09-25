# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `prompt-engineering` category with the `improving-prompts` skill: rewrites a rough prompt into an engineered one by classifying where it will run, diagnosing its gaps, and applying only the prompt and context engineering techniques that close them. Returns the techniques applied and rejected with reasons, placeholders for facts it could not infer, settings that belong outside the prompt, and the enhanced prompt in a copy-paste-ready tag. Ships a technique catalog split by group, dated model-family notes, worked examples, and templates.
- Product-engineering evaluation guide with lifecycle diagrams, a runnable fixture and grader, and behavioral scenarios for interviews, real app verification, per-lens review recall, PR categorization, merge safety, and stacked PRs.
- `product-engineering` category with nine skills built around one implementation loop. You take part at the start: `specifying-work-items` interviews you and writes `spec.md`, `brainstorming-solutions` lays out distinct approaches for you to pick from, `defining-verification` agrees how the agent will prove the work runs, and `planning-implementation` turns it into a roadmap of PR slices with an autonomy contract you approve. From there the agent works alone: `implementing-plans` builds each slice, `verifying-implementation` starts the app and drives it (browser, API, CLI) to observe every acceptance criterion, `reviewing-code-changes` runs a quick intent review before the PR and a five-lens review (architecture, security, conventions and idioms, efficiency, intent) on it, and `shipping-pull-requests` opens one PR per slice, marks it for human or agent review, and merges agent-reviewed PRs only when checks pass on the reviewed head and you authorized it. `running-implementation-loops` picks the track for the work item (quick fix, bugfix, small change, feature, new app, refactor, spike) and runs the stages it needs.
- `product-design` category with six stack-neutral skills for guided discovery, product briefs, UX flows, visual direction exploration, offline HTML prototypes, and product/design handoffs. Includes copyable templates, fictional worked examples, typography and spacing guidance, and checkpoints for user decisions.
- `foundations` category with two skills: `decision-records` keeps a project's decision log, `release-process` keeps its changelog and cuts tagged releases.
- Plugin marketplace manifest so Claude Code and Copilot CLI install a category as one plugin.
- Decision log in `decisions/` with the five founding decisions of this repository.
- `scripts/validate.py` and a CI workflow that enforce the repository rules on every push and pull request.
- Release workflow: a `v*` tag on `main` publishes a GitHub Release with the changelog section as notes, one archive per skill, and checksums.

[Unreleased]: https://github.com/theultimate-dev/skills/commits/main
