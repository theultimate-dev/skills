# 0005: One version, hand-written changelog, releases from tags on `main`

- Status: accepted
- Date: 2026-09-03

## Context

Consumers on every route can pin a tag: the marketplace with `#vX.Y.Z`, the `skills` CLI with `#vX.Y.Z`, APM with `#vX.Y.Z`. That only helps if tags are predictable and carry readable notes. The repository is Markdown, so there is no package manifest to hang a version on, and I already work with Conventional Commits, SemVer, and Keep a Changelog. Keep a Changelog 2.0.0 shipped in June 2026 with the same format as 1.1.0 and updated guidance.

## Options

1. **Per-skill versions** in each skill's `metadata`. Granular, and no installer reads it; it would need a changelog per skill and a release process per skill.
2. **Repository-wide SemVer with a generated changelog** (`git-cliff`, `release-please`). Automation, entries that read like commit subjects, and a bot pull request in the loop.
3. **Repository-wide SemVer, hand-written changelog, tag-triggered GitHub Action.**

## Decision

Option 3.

- **Version semantics.** Patch: fixes and wording inside existing skills. Minor: a new skill, a new category, a new reference or template. Major: renaming or removing a skill or category, or changing an install path.
- **Commits.** Conventional Commits; scope is the category or the skill. Breaking changes carry `!` and a `BREAKING CHANGE:` footer.
- **Changelog.** `CHANGELOG.md` in Keep a Changelog 2.0.0 form, written by hand for users, updated in the same change as the code. Released sections are immutable; mistakes are fixed forward or the version is marked `[YANKED]`.
- **Release commit.** `chore(release): vX.Y.Z` touches exactly two files: `CHANGELOG.md` (move `[Unreleased]` to `[X.Y.Z] - date`, refresh link references) and `.claude-plugin/marketplace.json` (set every `plugins[].version` and `metadata.version` to `X.Y.Z`).
- **Tag.** Annotated `vX.Y.Z` on a commit that is on `main`, pushed after `main`. Nothing else creates releases.
- **Action.** On a `v*.*.*` tag: verify the tag's shape, verify the commit is an ancestor of `main`, extract the version's changelog section, build one zip per skill plus checksums, create the GitHub Release with the section as notes. A hyphen in the version marks a pre-release.

## Consequences

- Adding a skill bumps the version for every skill in the repository. Accepted: the cost to consumers is nil, and one number is easy to reason about.
- Every change needs a changelog entry. The validator checks shape, not judgment; `CONTRIBUTING.md` asks for it.
- The `release-process` skill in this repository implements this decision for any project, and this repository runs the same workflow it ships as a template, plus the two packaging steps.
- First release: `0.1.0`, after one built archive has been uploaded to claude.ai by hand to confirm the format.
