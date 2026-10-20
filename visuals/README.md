# Visuals

Images for the plugin READMEs in `skills/<category>/README.md`, kept outside the skills tree so they never reach a skill zip or an install ([decision 0015](../decisions/0015-category-readmes-and-visuals.md)).

- `brand.css`: The Ultimate Dev tokens. Dark by default, light under `[data-theme="light"]`, one teal accent, Inter and JetBrains Mono from Google Fonts.
- `<category>/<name>.html`: one visual per file. Everything inside `.canvas`, 1200px wide, becomes the image. Open a file in a browser to preview it, and add `?theme=light` for the light variant.
- `<category>/<name>-dark.png` and `<name>-light.png`: the rendered images, at twice the canvas size. Never edit these by hand.

When a plugin changes what a visual shows, edit the HTML, then render again from the repository root:

```bash
uv run scripts/render_visuals.py harness-engineering
```

The script drives your installed Google Chrome through Playwright, needs network access for the fonts, and stops without writing a PNG if a font did not load. Commit the HTML and both PNGs together. The README shows each image with `<picture>`, so GitHub picks the variant that matches the reader's theme.
