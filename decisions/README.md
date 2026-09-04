# Decisions

Short records of the decisions that shape this repository. Read this index first; open a record only when you need the reasoning. New records take the next number. Accepted records are never edited or renumbered, only superseded by a newer record. To add one, use the `decision-records` skill in `skills/foundations/decision-records/`.

| # | Decision | Status | Summary |
|---|---|---|---|
| [0001](0001-record-decisions.md) | Record decisions as short records in `decisions/` | accepted | Four-section records, indexed here, linked from `AGENTS.md`. Supersede, never rewrite. |
| [0002](0002-agent-skills-open-format.md) | Skills use the open Agent Skills format with three frontmatter fields | accepted | `name`, `description`, `license` only, so every skill installs in every harness and uploads to GUI clients. |
| [0003](0003-categories-as-directories.md) | Categories are directories: `skills/<category>/<skill>/` | accepted | A category is the install unit and the plugin name. One skill, one category. Skill names unique repo-wide. |
| [0004](0004-distribution-through-existing-installers.md) | Distribute through existing installers, no bespoke one | accepted | Plugin marketplace for Claude Code and Copilot, `npx skills` for everything else, zips on releases for GUI clients. |
| [0005](0005-versioning-and-releases.md) | One version, hand-written changelog, releases from tags on `main` | accepted | Repo-wide SemVer, Conventional Commits, Keep a Changelog 2.0.0, GitHub Release built by an Action on tag push. |

Statuses: `proposed` (under discussion), `accepted` (in force), `deprecated` (no longer applies and nothing replaces it), `superseded` (replaced by a newer record; both records link to each other).
