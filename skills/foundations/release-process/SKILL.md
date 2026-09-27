---
name: release-process
description: "Maintains a project's CHANGELOG.md in Keep a Changelog form and cuts releases: picks the SemVer bump from Conventional Commits, moves Unreleased into a dated version section, bumps declared version files, commits, tags vX.Y.Z on main, pushes, and relies on a GitHub Action to publish the GitHub Release. Also handles repositories whose components (packages, plugins) are versioned independently, each with its own changelog and tags such as api--v1.2.0. Use when the user asks to add a changelog entry or note what changed, asks to release, ship, tag, or bump a version of the project or of one component, asks what changed since the last release, or when a project has no CHANGELOG.md, release workflow, or version tags yet."
license: MIT
---

# Release process

Two habits make releases boring, which is the goal. Every change lands with a line in `CHANGELOG.md` under `[Unreleased]`, written for the people who use the project. A release is one commit and one tag on `main`; a GitHub Action turns the tag into a GitHub Release with that version's changelog section as the notes. Nobody writes release notes at release time, and nobody creates releases by hand.

This skill has three entry points. Most of the time you are in the first.

## Entry point 1: log a change

Whenever a change is user-visible, add an entry under `## [Unreleased]` in `CHANGELOG.md`, in the same commit as the change, under one of six headings: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`. Create the heading if it is missing and keep the headings in that order.

Write the entry for a user, not from the commit subject: what they can now do, what behaves differently, what they must change. One line, plain words. Read the diff if you did not make the change yourself. `references/keep-a-changelog.md` covers what belongs under each heading and what is not a change at all.

In a repository whose components are versioned independently, the entry goes in the changelog of each component the change touches, and catalog or shared-tooling changes go in the root changelog. `references/independent-versions.md` covers the layout.

Commit messages follow Conventional Commits: `type(scope): description`. `feat` means a minor bump, `fix` a patch, and `!` after the type or a `BREAKING CHANGE:` footer means a major bump. The scope is whatever the project uses (a package, a module, a skill name); check recent history and follow it. Other types (`docs`, `chore`, `ci`, `refactor`, `test`) do not bump the version on their own.

## Entry point 2: cut a release

First decide which mode the project is in. Independent versions show as a changelog per component, tags such as `api--v1.2.0`, or a note in `AGENTS.md`. In that mode, read `references/independent-versions.md` before anything else: it changes which tag, changelog, and version files each step below uses, and a release commit may release several components at once.

Read `references/cutting-a-release.md` and follow it step by step. The short form:

1. **Preflight.** On `main`, working tree clean, in sync with `origin/main`, CI green on the head commit, `[Unreleased]` has entries, the intended tag exists neither locally nor remotely.
2. **Pick the version.** From the commits since the last tag: any breaking change means major, otherwise any `feat` means minor, otherwise patch. Confirm the version with the user; the changelog entries are the argument for it.
3. **Release the changelog.** Rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, add a fresh empty `## [Unreleased]` above it, update the link references at the bottom.
4. **Bump version files.** Every file the project declares as carrying the version: `package.json`, `pyproject.toml`, `Cargo.toml`, a plugin manifest, `version.txt`. The list lives in `AGENTS.md` or `CONTRIBUTING.md`; if there is none, ask once and suggest recording it there.
5. **Commit, tag, push.** One commit `chore(release): vX.Y.Z` containing exactly those files. Annotated tag `vX.Y.Z` on it. Push `main` first, then the tag. Watch the workflow run and confirm the GitHub Release appeared with the right notes.

The tag is the publish button. Do not create it or push it without the user's explicit confirmation in the current conversation, even if they asked for "a release" earlier. Show what you are about to run and wait for a yes.

## Entry point 3: bootstrap a project

The project has no `CHANGELOG.md`, no release workflow, or no version tags. Read `references/bootstrapping.md`. It covers creating the changelog from `templates/CHANGELOG.md`, installing the workflow from `templates/release.yml` (or `templates/release-components.yml` for independently versioned components), the first tag, and what to do when the project already uses release-please, changesets, git-cliff, or semantic-release.

## When you cannot run git

In a chat client without a shell, or without the repository checked out, do the writing and hand over the doing: produce the released changelog section, the version-file changes, and the exact command list, and say plainly that nothing was run. Never report a tag or a release as created when you could not create it.

## Hard rules

- Released changelog sections are immutable. Fix forward in the next version, or mark the version `[YANKED]`. Only `[Unreleased]` is edited freely.
- Tags are never moved, deleted after push, or force-pushed. A bad release gets yanked and a patch release follows.
- Releases are created by the workflow from a tag. Not by running the GitHub CLI on a laptop, not by editing a release in the web UI, because then the notes and the tag drift apart.
- The release commit is on `main`. The workflow refuses tags whose commit is not on `main`; do not work around it.
- No tag without confirmation. No push of a tag without confirmation.
- Push tags by name, at most three per push. GitHub starts no workflow run for a push that carries more tags, so never push pending tags with `--tags` or `--follow-tags`.

## References

| Read | When |
|---|---|
| `references/keep-a-changelog.md` | Writing entries, choosing a heading, link references, yanking |
| `references/cutting-a-release.md` | Every release: preflight, version choice, commands, rollback |
| `references/github-release-workflow.md` | Understanding, installing, or debugging the release workflow |
| `references/bootstrapping.md` | No changelog or workflow yet, or another release tool is in place |
| `references/independent-versions.md` | Components versioned on their own: changelog per component, `name--vX.Y.Z` tags, several releases at once |
| `templates/CHANGELOG.md` | Starting file for a new changelog |
| `templates/release.yml` | The workflow to install at `.github/workflows/release.yml` |
| `templates/release-components.yml` | The same workflow for root `vX.Y.Z` and component `name--vX.Y.Z` tags |
