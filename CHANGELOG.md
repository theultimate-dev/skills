# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `product-engineering` category with eight skills for a single-entry implementation loop: technical specifications and architecture agreement, work-package planning, implementation, verification, code review and repair, factual worklogs, and pull request delivery. Includes runtime model-tier routing, portable delegation packets, compact evidence artifacts, and behavioral evaluation scenarios.
- `product-design` category with six stack-neutral skills for guided discovery, product briefs, UX flows, visual direction exploration, offline HTML prototypes, and product/design handoffs. Includes copyable templates, fictional worked examples, typography and spacing guidance, and checkpoints for user decisions.
- `foundations` category with two skills: `decision-records` keeps a project's decision log, `release-process` keeps its changelog and cuts tagged releases.
- Plugin marketplace manifest so Claude Code and Copilot CLI install a category as one plugin.
- Decision log in `decisions/` with the five founding decisions of this repository.
- `scripts/validate.py` and a CI workflow that enforce the repository rules on every push and pull request.
- Release workflow: a `v*` tag on `main` publishes a GitHub Release with the changelog section as notes, one archive per skill, and checksums.

[Unreleased]: https://github.com/theultimate-dev/skills/commits/main
