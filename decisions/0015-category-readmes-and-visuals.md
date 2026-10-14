# 0015: Give a category an optional README, with its visuals outside the skills tree

- Status: accepted
- Date: 2026-10-14

## Context

Links shared on social media point at a plugin's directory, such as `skills/harness-engineering/`, and GitHub renders a `README.md` there if one exists. Under 0003 and the layout rule in `AGENTS.md`, a category directory holds its skill directories and one `CHANGELOG.md`, nothing else, and the validator enforces it. Every subdirectory of a category is treated as a skill: the validator expects a `SKILL.md` in it, and the release workflow zips each `skills/<category>/*/` as a skill. A landing page with images needs the README next to the skills and the images somewhere GitHub can resolve them, without either reaching what users install.

## Options

1. **README and an `assets/` directory inside the category.** Keeps a plugin's page in one place. Lost: the validator and the release workflow would both need an exception, and a forgotten exception ships `assets-X.Y.Z.zip` as a skill.
2. **README in the category, images and their sources in `visuals/<category>/` at the root.** A file never matches the release workflow's directory glob, and `npx skills`, Pi and the marketplace look only for `SKILL.md`, so nothing new reaches an install. Won.
3. **No category README; link to the root README.** No convention change. Lost: the root README covers five plugins, so a link to one plugin lands on a page about all of them.

## Decision

Option 2. A category directory may hold one optional `README.md`, the plugin's landing page.

- The README's images and their HTML sources live in `visuals/<category>/`, one HTML file per visual, rendered to `<name>-dark.png` and `<name>-light.png` next to it by `scripts/render_visuals.py`. Shared brand tokens live in `visuals/brand.css`.
- The README shows each visual with `<picture>` and `prefers-color-scheme`, the dark variant as the fallback, and links to it with a relative path (`../../visuals/<category>/...`).
- The validator accepts `README.md` next to `CHANGELOG.md` and checks that every relative link, `src` and `srcset` in a category README resolves.
- No other file or directory joins a category directory.

## Consequences

- A plugin can have a page of its own to link to, and the images on it can be regenerated when the plugin changes.
- The PNGs live in the repository, so every clone and every marketplace copy carries them. Keep them few and small.
- Rendering needs Google Chrome, `uv`, and network access for the fonts. CI does not render, so a stale PNG is caught only by reading the page.
- A category README is not part of any skill, so the self-containment rules do not apply to it, and nothing checks its wording. Its changes go in the category's changelog.
- 0003 still holds: a category remains the install unit, and `SKILL.md` still lives only at `skills/<category>/<skill>/SKILL.md`. This record extends it with the one file above.
