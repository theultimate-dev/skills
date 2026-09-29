# 0011: Release the marketplace with every plugin release

- Status: accepted
- Date: 2026-09-29
- Supersedes: 0010

## Context

0010 released the marketplace only when the catalog, the install routes, the release assets or the repository tooling changed. Since then, `foundations` 0.1.1 and `prompt-engineering` 0.2.0 were released on 2026-09-29 with no marketplace release. The marketplace release is the one GitHub marks Latest and the one `releases/latest` opens, so under 0010 the repository's visible release would sit on 0.1.0 for long stretches while its plugins move on. The catalog itself changes rarely: a plugin added, renamed or removed. The facts about installers and tag pushes that 0010 verified in September 2026 still hold.

## Options

1. **Keep 0010.** The marketplace is released only for its own changes. Accurate, but the Latest release goes stale and tells a visitor nothing about current plugin versions.
2. **Release the marketplace, at least a patch, with every plugin release, and list the plugins released in its notes.** Latest always names the newest plugin versions and links to their releases. The marketplace version keeps meaning "the catalog at this commit".
3. **Mark the newest plugin release Latest.** No extra release, but Latest would jump between plugins, and each one's notes speak for a single plugin.
4. **Derive the marketplace bump from the plugin bumps** (a plugin's minor release is a marketplace minor release). This ties the catalog's SemVer to plugin content. A breaking change inside a plugin does not break the catalog, and plugin pins already carry that meaning.

## Decision

Option 2. The rest of 0010 carries over unchanged, restated here so this record stands alone.

- **Plugins.** A plugin (a category) carries its own SemVer version in its `marketplace.json` entry. Its changelog is `skills/<category>/CHANGELOG.md` in Keep a Changelog 2.0.0 form. Its tags are `<category>--vX.Y.Z`. Its GitHub Release holds its notes, one zip per skill in the plugin, and `checksums.txt`.
  - Patch: fixes and wording inside its skills.
  - Minor: a new skill, reference, or template.
  - Major: renaming or removing a skill, or moving a skill out of the plugin.
  - A change inside a plugin's own `marketplace.json` entry belongs to that plugin.
- **Marketplace.** `metadata.version` versions the catalog and the repository around it. Its changelog is the root `CHANGELOG.md`, its tags are `vX.Y.Z`, and its GitHub Release holds notes only. It logs plugins added, renamed, or removed, install routes, release assets, repository tooling (the validator, CI, decisions, evaluations), and every plugin release.
  - Minor: a plugin added, or a new install route or asset type.
  - Major: a plugin renamed or removed, or the marketplace name or install path changed.
  - Patch: top-level catalog fixes, and every plugin release.
  - Renaming or removing a plugin also adds a `renames` entry to `marketplace.json`, mapping the old name to the new one or to `null`.
- **Every plugin release is a marketplace release.** The release commit that releases one or more plugins also releases the marketplace.
  - One marketplace release per release commit, whatever the number of plugins it releases.
  - Its bump is the highest one its changes call for. The plugin releases call for a patch. Unreleased marketplace entries that call for a minor or major bump raise it, and they ship in the same release, because the tag pins `main` at that commit.
  - Its section lists the plugins under `### Changed`, as a bullet `Plugins released with this version:` with one nested bullet per plugin: the plugin name in backticks, its new version linked to the plugin's release page (`…/releases/tag/<category>--vX.Y.Z`), and one line for users on what the release gives them. The full notes stay in the plugin's own release.
  - These lines are written in the release commit, since they only exist once the plugin versions are chosen.
  - A plugin release that went out without a marketplace release is listed under `[Unreleased]` and ships with the next marketplace release. The plugins' 0.1.0 releases are exempt, because they shipped with marketplace 0.1.0, which introduced them.
  - A marketplace release without plugin releases remains possible.
- **Before 1.0.0.** Every stream starts at `0.1.0`. Below 1.0.0, a breaking change bumps the minor version.
- **Changelogs.** Entries are written by hand for users, in the same change as the code, in every changelog the change touches. Released sections are immutable. A renamed category starts a new changelog whose first entry links the old one at its last tag.
- **Release commit.** `chore(release): …` touches only the released changelogs and the matching versions in `marketplace.json`. It carries one annotated tag per released stream, on a commit that is on `main`. Push `main` first, then the plugin tags, then the marketplace tag, at most three tags per push. That order means the marketplace notes never link to a plugin release that does not exist yet.
- **Enforcement.**
  - The validator refuses a plugin release, dated after the first marketplace release, that the root changelog does not link. It also refuses a link to a plugin release that does not exist.
  - The release workflow refuses a plugin tag unless the newest marketplace release at that commit links it.
- **Workflow.** On `vX.Y.Z` or `<plugin>--vX.Y.Z`, the workflow:
  1. Parses the tag.
  2. Checks that the commit is on `main`.
  3. Runs the validator.
  4. Checks that `marketplace.json` at the tag declares the tag's version.
  5. For a plugin tag, checks that the marketplace release at the tag lists the plugin.
  6. Extracts the matching changelog section.
  7. Packages the plugin's skills.
  8. Creates the release.

  Marketplace releases are marked Latest; plugin releases are not. A hyphenated version is a pre-release. A manual run with a `tag` input covers tags that GitHub did not act on.
- **Commits.** Conventional Commits. The description is in the imperative mood, lowercase, with no trailing period. The scope is the category or the skill. Breaking changes carry `!` and a `BREAKING CHANGE:` footer.

## Consequences

- The Latest release always names the newest plugin versions and links to their releases. A marketplace tag pin now moves with each plugin release, so it is a reasonable "everything as released" pin.
- A release carries one more tag. Releasing three or more plugins at once takes two tag pushes.
- The marketplace version climbs by patches much faster than the catalog changes. A patch no longer means only a catalog fix, so its notes have to say what it contains.
- The first marketplace release after this record lists `foundations` 0.1.1 and `prompt-engineering` 0.2.0.
- The release workflow departs further from the `release-process` template, by one more check.
- A manual re-run of a plugin tag cut before this record now fails the new check. This is harmless: those releases are published and immutable.
- Carried over from 0010: `main` remains the real delivery channel, so every merge has to be releasable. Release archives are per plugin, and download links go to each plugin's release list. Moving a skill between categories is breaking for the plugin it leaves and minor for the one it joins.
