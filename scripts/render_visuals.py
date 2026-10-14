#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright==1.55.0"]
# ///
"""Render the README visuals in `visuals/<category>/` to PNG.

Run `uv run scripts/render_visuals.py [category ...]` from the repository root;
with no category it renders every directory under `visuals/`. Each `<name>.html`
becomes `<name>-dark.png` and `<name>-light.png` next to it: the `.canvas`
element, at twice its CSS size, with transparent corners.

Needs Google Chrome (Playwright drives the installed browser, nothing is
downloaded) and network access for the fonts. A render fails when Inter or
JetBrains Mono did not load, rather than writing a PNG in a fallback font.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
VISUALS = ROOT / "visuals"
THEMES = ("dark", "light")
FONTS = ("Inter", "JetBrains Mono")
LOADED_FONTS = """() => document.fonts.ready.then(() =>
  [...document.fonts].filter(face => face.status === "loaded").map(face => face.family.replace(/"/g, "")))"""


def render(categories: list[str]) -> int:
    sources = [html for category in categories for html in sorted((VISUALS / category).glob("*.html"))]
    if not sources:
        print(f"no HTML sources in {', '.join('visuals/' + c for c in categories)}", file=sys.stderr)
        return 1
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome")
        try:
            for html in sources:
                for theme in THEMES:
                    page = browser.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=2)
                    page.goto(f"{html.as_uri()}?theme={theme}", wait_until="networkidle")
                    loaded = set(page.evaluate(LOADED_FONTS))
                    missing = [font for font in FONTS if font not in loaded]
                    if missing:
                        print(f"{html.relative_to(ROOT)}: fonts did not load: {', '.join(missing)}", file=sys.stderr)
                        return 1
                    target = html.with_name(f"{html.stem}-{theme}.png")
                    page.locator(".canvas").screenshot(path=str(target), omit_background=True)
                    page.close()
                    print(target.relative_to(ROOT))
        finally:
            browser.close()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="render_visuals.py", description="Render visuals/<category>/*.html to PNG.")
    parser.add_argument("categories", nargs="*", help="directories under visuals/ (default: all of them)")
    categories = parser.parse_args(argv).categories or sorted(d.name for d in VISUALS.iterdir() if d.is_dir())
    unknown = [c for c in categories if not (VISUALS / c).is_dir()]
    if unknown:
        print(f"no such directory: {', '.join('visuals/' + c for c in unknown)}", file=sys.stderr)
        return 1
    return render(categories)


if __name__ == "__main__":
    sys.exit(main())
