# Bootstrapping releases in a project

## No changelog yet

1. Copy `templates/CHANGELOG.md` to the repository root. Replace `OWNER/REPO`.
2. Seed `[Unreleased]` from what has shipped since the last tag, or from the whole history when there are no tags. Read the log and the diffs, group by the six headings, write for users. Do not paste commit subjects. If the history is long, one `Added` entry per capability is enough; precision starts from now on.
3. Add the rule to the project's `AGENTS.md` or `CONTRIBUTING.md`: every user-visible change adds an entry under `[Unreleased]` in the same commit.

## No release workflow yet

Follow "Installing it in a project" in `github-release-workflow.md`. Commit with `ci: release from tags`.

## No tags yet

First decide whether the repository ships one version or several components that users install on their own. The second case uses `independent-versions.md` and `templates/release-components.yml`. Then decide the first version with the user. `0.1.0` says "usable, not yet stable" and leaves room; `1.0.0` is a promise about compatibility. Either way, the first `[X.Y.Z]` section links to `https://github.com/OWNER/REPO/releases/tag/vX.Y.Z`, because there is no previous tag to compare against. Then follow `cutting-a-release.md`.

## Version files

Find every file that carries the project version: `package.json`, `pyproject.toml`, `Cargo.toml`, `setup.cfg`, a gemspec, a plugin or extension manifest, a `VERSION` or `version.txt`, a constant in source. Write the list into `AGENTS.md` under a "Release" heading so releases stop depending on memory. Prefer one source of truth; if the build can derive the version from the tag, that beats a file.

## The project already uses another release tool

Do not rip it out to install this. Compare what it does with what the user wants, propose one path, and record the choice as a decision.

| Tool in place | What it does | Coexist | Replace |
|---|---|---|---|
| **release-please** | Opens a release pull request from Conventional Commits, writes `CHANGELOG.md`, tags on merge | Keep it. It already guarantees tags land on the default branch. This skill then only helps with better entries, which release-please regenerates. Usually: keep release-please, stop here | For hand-written notes: remove its config and workflow, keep the existing `CHANGELOG.md` (compatible format), install `release.yml` |
| **semantic-release** | Computes the version, tags, publishes, notes from commits | Poorly; two tools tagging is a mess | Keep its changelog output as the starting `CHANGELOG.md`, remove `.releaserc` and its workflow, install `release.yml`, add the version-file bump to the release commit |
| **changesets** | Per-change Markdown files, a versioning pull request, npm publish for monorepos | Keep it for monorepos publishing several packages; it owns versions and changelogs per package. Do not add this workflow on top | Single-package repos gain little from it: keep the accumulated `CHANGELOG.md`, drop `.changeset/`, install `release.yml`. Monorepos that want hand-written notes per package: keep the package changelogs and follow `independent-versions.md` |
| **git-cliff** | Generates `CHANGELOG.md` from commits with a template | Generate into `[Unreleased]` as a draft the human edits before release. Use its `keepachangelog` template | Drop the generation step and write entries by hand |
| **GoReleaser, cargo-release, npm version, standard-version** | Language-specific tag and publish | Often fine: they create the tag, this workflow reacts to it. Make sure only one of them creates the GitHub Release | Rarely necessary |
| A habit of running the GitHub CLI by hand | Notes typed at release time | Replace the habit, keep everything else | Install `release.yml` and stop creating releases by hand |

Whatever the path, the invariants stay: a human-readable `CHANGELOG.md`, tags on `main` only, exactly one tool creating the GitHub Release.
