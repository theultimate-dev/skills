# 0010: Version, log, and release each plugin on its own

- Status: superseded
- Date: 2026-09-27
- Supersedes: 0005
- Superseded by: 0011

## Context

0005 gave the repository one version and one changelog. Since then the catalog has grown to four plugins, with more planned, and nothing has been released yet. One version would bump every plugin whenever any of them changes, one changelog mixes notes for four audiences, and a user cannot pin or download a single plugin's release.

Verified in September 2026:
- Claude Code offers a plugin update only when the plugin's `version` changes. An install copies the plugin from the marketplace clone at its current HEAD, so content merged after a release reaches new installs under the old version. `metadata.version` changes nothing for installs.
- A `#ref` pin pins the whole catalog.
- Claude Code tags per-plugin releases as `<plugin>--v<version>` and resolves dependency version ranges against those tags.
- The `skills` CLI reads no version at all. It reinstalls a skill whenever the skill folder's tree hash changes at the installed ref, so unpinned installs follow `main`. A `@` inside `#ref` breaks its parsing.
- GitHub creates no push event when more than three tags are pushed at once.

## Options

1. **Keep one version (0005).** Simple, but every plugin moves together and the notes stay mixed.
2. **One version per plugin, a hand-written changelog per plugin, plus a marketplace changelog, released from tags by one workflow.** Matches how both installers work and keeps notes written for users.
3. **One version per skill.** No installer reads it, and it would mean dozens of changelogs.
4. **Per-plugin versions through release-please or changesets.** Automated, but the entries read like commit subjects and a bot pull request joins the loop, which is what 0005 rejected.
5. **Plugin entries pinned to their tags (`github` sources with `ref`).** Route A would get exactly the released content. It breaks `source: "./"`, local dogfooding, and the validator, and installs fail between pushing `main` and pushing the tag.

## Decision

Option 2.

- **Plugins.** A plugin (a category) carries its own SemVer version in its `marketplace.json` entry. Its changelog is `skills/<category>/CHANGELOG.md` in Keep a Changelog 2.0.0 form. Its tags are `<category>--vX.Y.Z`, and its GitHub Release holds its notes, one zip per skill in the plugin, and `checksums.txt`.
  - Patch: fixes and wording inside its skills.
  - Minor: a new skill, reference, or template.
  - Major: renaming or removing a skill, or moving a skill out of the plugin.
  - A change inside a plugin's own `marketplace.json` entry belongs to that plugin.
- **Marketplace.** `metadata.version` versions the catalog and the repository around it. Its changelog is the root `CHANGELOG.md`, its tags are `vX.Y.Z`, and its GitHub Release holds notes only. It logs plugins added, renamed, or removed, install routes, release assets, and repository tooling: the validator, CI, decisions, and evaluations.
  - Minor: a plugin added, or a new install route or asset type.
  - Major: a plugin renamed or removed, or the marketplace name or install path changed.
  - Patch: top-level catalog fixes.
  - Renaming or removing a plugin also adds a `renames` entry to `marketplace.json`, mapping the old name to the new one or to `null`.
- **Before 1.0.0.** Every stream starts at `0.1.0`. Below 1.0.0, a breaking change bumps the minor version.
- **Changelogs.** Entries are written by hand for users, in the same change as the code, in every changelog the change touches. Released sections are immutable. A renamed category starts a new changelog whose first entry links the old one at its last tag.
- **Release commit.** `chore(release): …` touches only the released changelogs and the matching versions in `marketplace.json`. One commit may release several streams, with one annotated tag each, on a commit that is on `main`. Push `main` first, then at most three tags per push.
- **Workflow.** On `vX.Y.Z` or `<plugin>--vX.Y.Z`, the workflow:
  1. Parses the tag.
  2. Checks that the commit is on `main`.
  3. Runs the validator.
  4. Checks that `marketplace.json` at the tag declares the tag's version.
  5. Extracts the matching changelog section.
  6. Packages the plugin's skills.
  7. Creates the release.

  Marketplace releases are marked Latest; plugin releases are not. A hyphenated version is a pre-release. A manual run with a `tag` input covers tags that GitHub did not act on.
- **Commits.** Conventional Commits. The description is in the imperative mood, lowercase, with no trailing period. The scope is the category or the skill. Breaking changes carry `!` and a `BREAKING CHANGE:` footer.

## Consequences

- A change to one plugin no longer moves the others, and each release page speaks to that plugin's users.
- `main` remains the real delivery channel. The `skills` CLI and new marketplace installs pick up whatever is merged, so every merge has to be releasable and the affected plugins should be released soon after. Only tag pins follow releases alone.
- Pinning the marketplace to any tag pins the whole catalog at that commit, including other plugins' unreleased work.
- There are five version streams to keep straight. The validator ties every version to its changelog, and the workflow refuses a tag that disagrees with the manifest.
- Release archives are per plugin, which refines the GUI route in 0004. `releases/latest` now points at a notes-only marketplace release, so download links go to each plugin's release list.
- The `release-process` skill gains an independent-versions mode and a matching workflow template. This repository runs that template plus a manifest check and packaging.
- Moving a skill between categories is breaking for the plugin it leaves and minor for the one it joins. 0003's reference to 0005 now reads as this record.
- Carried over from 0005: before the first release, one built archive is uploaded to claude.ai by hand to confirm the format.
