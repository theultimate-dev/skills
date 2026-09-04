# AGENTS.md

This repository holds agent skills in the open [Agent Skills](https://agentskills.io) format, grouped into categories that install as one unit. Read this file first. Open the linked files only when the task needs them.

## Map

| Path | What it is |
|---|---|
| `skills/<category>/<skill>/` | One skill: `SKILL.md`, optional `references/` and `templates/` |
| `.claude-plugin/marketplace.json` | One plugin per category, read by Claude Code and Copilot CLI |
| [`decisions/README.md`](decisions/README.md) | Index of decision records. Read it before changing structure or conventions |
| [`CHANGELOG.md`](CHANGELOG.md) | Keep a Changelog 2.0.0. Every user-visible change gets an entry under `[Unreleased]` |
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
- Every category has a plugin entry in `marketplace.json` with the same name, listing all of its skills as `./skills/<category>/<skill>` paths.

Commits, changelog, versions
- Conventional Commits. Scope is the category or the skill: `feat(foundations): …`, `fix(release-process): …`. Renaming or removing a skill or category is breaking: `feat(foundations)!: …`.
- Add the changelog entry under `[Unreleased]` in the same change. Write it for users, not from the commit subject.
- Version files bumped in a release commit: `CHANGELOG.md` and `.claude-plugin/marketplace.json` (`plugins[].version` and `metadata.version`). Nothing else carries a version.

Conduct
- Never commit, push, tag, open a pull request, or publish without explicit confirmation in the current conversation.
- Never rewrite a released changelog section or an accepted decision record. Add an entry, or supersede the record.

## How to

Add a skill: create `skills/<category>/<name>/SKILL.md`, add its path to the category's `skills[]` in `marketplace.json`, add it to the README categories table, add a changelog entry, run `python3 scripts/validate.py`.

Add a category: new directory under `skills/`, new plugin entry in `marketplace.json` with the same name, README row, changelog entry, and a decision record when the split changes how users install.

Record a decision: use the `decision-records` skill in `skills/foundations/decision-records/`. Cut a release: use the `release-process` skill in `skills/foundations/release-process/`.

Dogfood: `npx skills add . -g -a claude-code` symlinks this working tree into your Claude Code skills directory, so edits are live without reinstalling.

See also: [README.md](README.md) · [CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md)
