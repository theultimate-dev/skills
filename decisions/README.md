# Decisions

Short records of the decisions that shape this repository. Read this index first; open a record only when you need the reasoning. New records take the next number. Accepted records are never edited or renumbered, only superseded by a newer record. To add one, use the `decision-records` skill in `skills/foundations/decision-records/`.

| # | Decision | Status | Summary |
|---|---|---|---|
| [0001](0001-record-decisions.md) | Record decisions as short records in `decisions/` | accepted | Four-section records, indexed here, linked from `AGENTS.md`. Supersede, never rewrite. |
| [0002](0002-agent-skills-open-format.md) | Skills use the open Agent Skills format with three frontmatter fields | accepted | `name`, `description`, `license` only, so every skill installs in every harness and uploads to GUI clients. |
| [0003](0003-categories-as-directories.md) | Categories are directories: `skills/<category>/<skill>/` | accepted | A category is the install unit and the plugin name. One skill, one category. Skill names unique repo-wide. |
| [0004](0004-distribution-through-existing-installers.md) | Distribute through existing installers, no bespoke one | accepted | Plugin marketplace for Claude Code and Copilot, `npx skills` for everything else, zips on releases for GUI clients. |
| [0005](0005-versioning-and-releases.md) | One version, hand-written changelog, releases from tags on `main` | superseded by [0010](0010-independent-plugin-versions.md) | Repo-wide SemVer, Conventional Commits, Keep a Changelog 2.0.0, GitHub Release built by an Action on tag push. |
| [0006](0006-product-design-discovery-skills.md) | Package product discovery as independent skills with an optional coordinator | accepted | Six stack-neutral skills in `product-design`, from rough idea to product/design handoff, with user milestones and offline HTML prototypes. |
| [0007](0007-product-engineering-loop.md) | Package engineering delivery as a verified implementation loop | superseded by [0009](0009-product-engineering-front-loaded-loop.md) | Eight skills in `product-engineering`, from architecture agreement through bounded implementation, evidence-based repair, and an open PR; runtime capability routing and compact artifacts. |
| [0008](0008-prompt-engineering-category.md) | Package prompt and context engineering as a `prompt-engineering` category | accepted | One skill to start, `improving-prompts`: neutral technique catalog by group, dated model-family notes, one-pass operation, fixed output contract with the enhanced prompt in a tag. |
| [0009](0009-product-engineering-front-loaded-loop.md) | Front-load human decisions and give the agent PR-level autonomy in product-engineering | accepted | Supersedes 0007. Nine skills in one loop: interview, brainstorm, verification method and roadmap as human gates, then autonomous implementation, real verification, quick and five-lens review, PR slices categorized human or agent, and merge within a recorded autonomy contract. |
| [0010](0010-independent-plugin-versions.md) | Version, log, and release each plugin on its own | accepted | Supersedes 0005. Per-plugin SemVer, `skills/<category>/CHANGELOG.md`, `<plugin>--vX.Y.Z` tags and releases with that plugin's zips; the root changelog and `vX.Y.Z` tags version the marketplace; one workflow validates the manifest and publishes both. Imperative Conventional Commits. |

Statuses: `proposed` (under discussion), `accepted` (in force), `deprecated` (no longer applies and nothing replaces it), `superseded` (replaced by a newer record; both records link to each other).
