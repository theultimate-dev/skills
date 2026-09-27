# AGENTS.md

This repository holds agent skills in the open [Agent Skills](https://agentskills.io) format, grouped into categories that install as one unit. Read this file first. Open the linked files only when the task needs them.

## Map

| Path | What it is |
|---|---|
| `skills/<category>/<skill>/` | One skill: `SKILL.md`, optional `references/` and `templates/` |
| `skills/<category>/CHANGELOG.md` | The plugin's changelog, Keep a Changelog 2.0.0. Every user-visible change to the category gets an entry under `[Unreleased]` |
| `.claude-plugin/marketplace.json` | One plugin per category, read by Claude Code and Copilot CLI. Carries each plugin's version and the marketplace version |
| [`decisions/README.md`](decisions/README.md) | Index of decision records. Read it before changing structure or conventions |
| [`CHANGELOG.md`](CHANGELOG.md) | The marketplace and repository changelog: plugins added, renamed or removed, install routes, release assets, tooling |
| `scripts/validate.py` | Enforces the mechanical rules below; it cannot judge commit messages, changelog wording, or whether an entry was added. Run it before you finish |
| `.github/workflows/` | `validate.yml` on push and pull request, `release.yml` on `vX.Y.Z` and `<plugin>--vX.Y.Z` tags or run by hand with a tag |

## Rules

Skill format
- Frontmatter has exactly `name`, `description`, `license`, each a single `key: value` line. No other fields, no block scalars, no lists.
- `name` equals the directory name, kebab-case, unique across the repository.
- `description` says what the skill does and when to use it, names concrete artifacts rather than bare verbs, fits on one line under 1024 characters.
- A skill is self-contained: links stay inside its directory, and nothing in it assumes a particular harness, install path, or environment variable.
- `SKILL.md` stays under 500 lines. Depth goes in `references/`, copyable files in `templates/`.

Layout
- `SKILL.md` lives only at `skills/<category>/<skill>/SKILL.md`. One skill belongs to one category.
- A category directory holds its skill directories and one `CHANGELOG.md`, nothing else.
- Every category has a plugin entry in `marketplace.json` with the same name, listing all of its skills as `./skills/<category>/<skill>` paths.

Commits and changelogs
- Conventional Commits, description in the imperative mood, lowercase, no trailing period. Scope is the category or the skill: `feat(foundations): add …`, `fix(release-process): correct …`. A breaking change carries `!` and a `BREAKING CHANGE:` footer. Renaming or removing a skill, or moving it out of its category, is breaking for its plugin; renaming or removing a category is breaking for the marketplace: `feat(foundations)!: …`.
- Add the changelog entry under `[Unreleased]` in the same change, written for users, not from the commit subject. Anything inside a category, and that plugin's own entry in `marketplace.json`, goes in `skills/<category>/CHANGELOG.md`. The plugin catalog (plugins added, renamed, removed), install routes, release assets and repository tooling (validator, CI, decisions, evaluations) go in the root `CHANGELOG.md`. A change that spans both gets an entry in each.

Conduct
- Never commit, push, tag, open a pull request, or publish without explicit confirmation in the current conversation.
- Never rewrite a released changelog section or an accepted decision record. Add an entry, or supersede the record.

## Release

Plugins and the marketplace are versioned independently ([0010](decisions/0010-independent-plugin-versions.md)). Cut a release with the `release-process` skill in `skills/foundations/release-process/`, in its independent-versions mode. The components are the plugins, with changelogs at `skills/{component}/CHANGELOG.md`, and the root is the marketplace.

| Stream | Changelog | Version file | Tag |
|---|---|---|---|
| A plugin | `skills/<category>/CHANGELOG.md` | its entry's `version` in `.claude-plugin/marketplace.json` | `<category>--vX.Y.Z` |
| The marketplace | `CHANGELOG.md` | `metadata.version` in `.claude-plugin/marketplace.json` | `vX.Y.Z` |

- Every version equals the newest release in its changelog: `0.0.0` until the first release, which is `0.1.0`. Before 1.0.0 a breaking change bumps the minor version.
- Plugin bumps: patch for fixes and wording in its skills, minor for a new skill, reference or template, major for renaming, removing or moving out a skill.
- Marketplace bumps: patch for catalog fixes, minor for a plugin added or a new install route or asset type, major for a plugin renamed or removed or a changed marketplace name or install path.
- A release commit, `chore(release): …`, touches only the released changelogs and the matching versions. One commit may release several streams, with one annotated tag each. Push `main` first, then the tags by name, at most three per push; GitHub runs no workflow for larger tag pushes.

## How to

Add a skill: create `skills/<category>/<name>/SKILL.md`, add its path to the category's `skills[]` in `marketplace.json`, add it to the README categories table, add an entry to `skills/<category>/CHANGELOG.md`, run `python3 scripts/validate.py`.

Add a category: new directory under `skills/` with a `CHANGELOG.md` whose `[Unreleased]` links `https://github.com/theultimate-dev/skills/commits/main/skills/<category>`, new plugin entry in `marketplace.json` with the same name and `"version": "0.0.0"`, README row, an entry in both the new and the root changelog, and a decision record when the split changes how users install.

Rename, move or remove a skill: breaking for its plugin, and a move is minor for the plugin it joins. Update `marketplace.json`, the README table, and the changelog of each affected plugin.

Rename or remove a category: breaking for the marketplace. Add a `renames` entry to `marketplace.json` that maps the old name to the new one, or to `null`. A renamed category starts a new `CHANGELOG.md` whose first entry links the old changelog at its last tag. Log it in the root changelog.

Record a decision: use the `decision-records` skill in `skills/foundations/decision-records/`. Cut a release: see [Release](#release).

Dogfood: `npx skills add . -g -a claude-code -y` copies this working tree's skills into your Claude Code skills directory. Re-run it after each edit; the copy does not follow the working tree.

See also: [README.md](README.md) · [CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md)
