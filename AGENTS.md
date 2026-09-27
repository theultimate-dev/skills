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
| `scripts/validate.py` | Enforces every rule below. Run it before you finish |
| `.github/workflows/` | `validate.yml` on push and pull request, `release.yml` on `v*` tags |

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

Commits, changelog, versions
- Conventional Commits, description in the imperative mood, lowercase, no trailing period. Scope is the category or the skill: `feat(foundations): add …`, `fix(release-process): correct …`. Renaming or removing a skill is breaking for its plugin, renaming or removing a category is breaking for the marketplace: `feat(foundations)!: …`.
- Add the changelog entry under `[Unreleased]` in the same change, written for users, not from the commit subject. Anything inside a category goes in `skills/<category>/CHANGELOG.md`. The plugin catalog (plugins added, renamed, removed), install routes, release assets and repository tooling go in the root `CHANGELOG.md`. A change that spans both gets an entry in each.
- Each plugin has its own SemVer version in its `marketplace.json` entry, equal to the newest release in its changelog. `metadata.version` does the same for the root changelog. Before 1.0.0 a breaking change bumps the minor version.
- A release commit touches only the released changelogs and the matching versions in `marketplace.json`. Tags are `<plugin>--vX.Y.Z` for a plugin and `vX.Y.Z` for the marketplace. Push at most three tags at once; GitHub runs no workflow for larger tag pushes.

Conduct
- Never commit, push, tag, open a pull request, or publish without explicit confirmation in the current conversation.
- Never rewrite a released changelog section or an accepted decision record. Add an entry, or supersede the record.

## How to

Add a skill: create `skills/<category>/<name>/SKILL.md`, add its path to the category's `skills[]` in `marketplace.json`, add it to the README categories table, add an entry to `skills/<category>/CHANGELOG.md`, run `python3 scripts/validate.py`.

Add a category: new directory under `skills/` with a `CHANGELOG.md` whose `[Unreleased]` links `https://github.com/theultimate-dev/skills/commits/main/skills/<category>`, new plugin entry in `marketplace.json` with the same name and `"version": "0.0.0"`, README row, an entry in both the new and the root changelog, and a decision record when the split changes how users install.

Record a decision: use the `decision-records` skill in `skills/foundations/decision-records/`. Cut a release: use the `release-process` skill in `skills/foundations/release-process/`, in its independent-versions mode. The components are the plugins, with changelogs at `skills/{component}/CHANGELOG.md`, and the root is the marketplace.

Dogfood: `npx skills add . -g -a claude-code` symlinks this working tree into your Claude Code skills directory, so edits are live without reinstalling.

See also: [README.md](README.md) · [CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md)
