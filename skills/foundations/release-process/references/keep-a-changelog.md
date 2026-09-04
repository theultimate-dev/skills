# Keep a Changelog, as practised here

The format is [Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/). The parts that matter day to day:

## File shape

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Something users can now do.

## [1.2.0] - 2026-08-30

### Changed

- Something that behaves differently, and what to do about it.

### Fixed

- A bug, described by its symptom.

[Unreleased]: https://github.com/OWNER/REPO/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/OWNER/REPO/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/OWNER/REPO/releases/tag/v1.1.0
```

- Newest version first. `[Unreleased]` always on top, even when empty.
- Version heading: `## [X.Y.Z] - YYYY-MM-DD`. Bracketed version, space, hyphen, space, ISO date.
- Link references at the bottom, one per heading, so every version links to a diff. Before the first tag exists, `[Unreleased]` points at `https://github.com/OWNER/REPO/commits/main`. The first released version links to its tag page, since there is nothing to compare against.
- Yanked: `## [1.2.1] - 2026-09-01 [YANKED]`, with a one-line note under it saying why.

## The six headings

| Heading | Use for |
|---|---|
| `Added` | New capabilities |
| `Changed` | Existing behaviour that now works differently |
| `Deprecated` | Still works, will be removed. Say when, and what to use instead |
| `Removed` | Gone. Say what to use instead |
| `Fixed` | Bugs, described by the symptom the user saw |
| `Security` | Vulnerabilities fixed. Lead with the CVE identifier when there is one |

Torn between `Changed` and `Fixed`? Ask whether the old behaviour was a bug. If yes, `Fixed`.

Not changes, so not entries: dependency bumps with no user-visible effect, refactors, CI tweaks, formatting, commit or pull request housekeeping. If a reader of the changelog would not notice, leave it out. The commit history keeps that.

## Writing an entry

- One line per change, starting with the thing that changed, not with "Added" (the heading already says that).
- Say what the user can do, sees, or must change. "Config file is validated on start; an invalid key fails with a message naming it" beats "Improve config validation".
- Put identifiers the user will type in backticks.
- Breaking changes get an explicit sentence on what to change, in the entry, not only in the commit footer.
- An issue or pull request reference in parentheses at the end is fine. Never as the whole entry.
- Do not copy commit subjects. Read the diff and describe the effect.

## Releasing the Unreleased section

At release time, rename the heading to the version and date, add a fresh `## [Unreleased]` above, and update the link references. Nothing else in the section changes. The GitHub Action extracts exactly this section as the release notes, so the section has to read well on its own: no "see above".

## Fixing a released section

Do not. A typo may be fixed. A missing entry goes into the next version with a note ("shipped in 1.2.0, undocumented at the time"). A wrong release gets `[YANKED]` and a patch release. Consumers, tooling, and the GitHub Release already read the old text; rewriting it makes the record untrustworthy.
