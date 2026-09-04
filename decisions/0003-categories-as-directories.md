# 0003: Categories are directories: `skills/<category>/<skill>/`

- Status: accepted
- Date: 2026-09-03

## Context

The requirement is one command to install a whole category, on more than one installer. The well-known public skill repositories keep a flat `skills/<name>/` tree and express groups only in manifests, which gives category installs to Claude Code plugins and nothing else.

Verified against the installers' own source and docs: the `skills` CLI walks skill containers three levels deep and, given a path such as `owner/repo/skills/<dir>`, installs every skill directly under that directory. The Claude Code marketplace lists skills with explicit paths, so it does not care about nesting. Pi discovers nested `SKILL.md` directories recursively. APM addresses arbitrary subdirectories.

## Options

1. **Flat `skills/<name>/`, categories in manifests.** Matches Anthropic's repo. `npx skills` users install a category only through an interactive picker or a list of `--skill` flags.
2. **Nested `skills/<category>/<name>/`.** A category is a path. `npx skills add owner/repo/skills/<category>` and a marketplace plugin entry both install it with one command. A skill lives in exactly one category.
3. **One repository per category.** Clean isolation and N repositories to maintain, contradicting the point of one shareable repo.

## Decision

Option 2.

- A category is a directory under `skills/`, the unit of install, and the name of its plugin in `.claude-plugin/marketplace.json`.
- `SKILL.md` exists only at `skills/<category>/<skill>/SKILL.md`. Never at the repository root, which would make the `skills` CLI vendor the whole repository, and never at category level.
- One skill belongs to one category. Cross-listing, if it is ever needed, happens in the marketplace manifest, not by copying.
- Skill names are unique across the repository because flat installers place them side by side.
- No dot-prefixed category directories; tools that skip dotfiles would miss them.

## Consequences

- One command per category on every route that reads paths, and named plugins for the routes that read manifests.
- Moving a skill between categories changes its install path and is a breaking change under 0005.
- `theultimate-dev/skills/skills/foundations` reads like a typo. The README says why once.
- The three-level walk leaves one more nesting level available. It stays unused.
