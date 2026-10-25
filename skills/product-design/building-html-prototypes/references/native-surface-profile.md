# Native-surface profile

## When it applies

A native surface, such as a menu-bar panel, a desktop window, a phone widget or a watch face, is drawn at the device's own scale. It cannot reflow to 320 CSS pixels the way a web page does. Draw each such surface as a fixed-scale scene on a page, and follow this profile for the scenes. The page around the scenes stays an ordinary responsive page with the usual checks. For fixed-scale scenes, this profile replaces the 320 px narrow-viewport check: a scene does not reflow, so the check in a 320 px frame asks instead that the page does not scroll sideways and that each scene scrolls inside its own container, as [Reflow around the scenes](#reflow-around-the-scenes) describes.

When a direction brief supplies a platform frame, start from it. A frame holds the placements, scale mapping, geometry tokens with their sources, the system UI beside the surface, settings, and system type and symbols. Draw a scene for each placement, and carry the frame's values and sources into the notes as written. Ask the user only for what the frame lacks or marks for the user to supply.

## Scale

- **State the scale mapping** in the notes, for example 1 CSS px = 1 pt for a platform that measures in points, or 1 CSS px = 1 dp for one that measures in density-independent pixels. Draw every scene at that mapping: a window 800 pt wide is 800 CSS px wide at any viewport size.
- **Keep the scale.** Do not shrink a scene to fit the page with `transform`, `zoom` or a percentage width; that changes the type and target sizes the scene exists to show.
- **Check each scene at device scale factors 1 and 2.** Screenshot it at both, for example with Chrome's `--force-device-scale-factor=2` in a headless run. At 2, look for blurred raster images (give each a source at twice its drawn size), hairlines that vanish or double, and edges that fall between device pixels. Record both checks in the notes.

## Device geometry as sourced tokens

Keep the device's geometry in custom properties on the scene, not as numbers scattered through its rules:

- the display size, in points or the platform's own unit;
- system bar heights, such as a status bar, menu bar, title bar or home indicator;
- safe areas;
- hardware cut-outs, such as a camera housing or rounded display corners.

Take each value from the platform's own design guidelines or specifications for the device the user names, and record its source in the notes: the document, the device, and the date you read it. The skill ships no device values, because they change with each device. When no source gives a value, ask the user for it, and record their answer as its source. Never present an invented value as the device's.

## Reflow around the scenes

The page around the scenes reflows at 320 CSS pixels: its headings, descriptions and settings control wrap without horizontal scrolling. Each scene keeps its fixed size and scrolls inside its own container, never the page:

```html
<div class="scene-viewport" role="region" aria-label="Phone home screen scene" tabindex="0">
  <div class="scene">…</div>
</div>
```

```css
.scene-viewport { max-width: 100%; overflow-x: auto; }
.scene { width: var(--display-width); height: var(--display-height); }
```

The container is labeled and can take focus, so a keyboard user can scroll it. WCAG 2.2's reflow criterion exempts "parts of the content which require two-dimensional layout for usage or meaning" ([W3C, Understanding Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)). A fixed-scale scene is such a part; the page around it is not.

Check it in a frame 320 CSS pixels wide with the interaction harness, as [Narrow viewports](scripted-checks.md#narrow-viewports) describes: the page's `scrollWidth` is no larger than 320, each scene container's `scrollWidth` is larger than its `clientWidth`, with `overflow-x` set to `auto` or `scroll`, and each scene's drawn width, `getBoundingClientRect().width`, equals the token that sets its width, such as `--display-width` above. A scene shrunk with `transform` or `zoom` can still overflow its container, so the `scrollWidth` check passes; only the drawn width shows that the scene lost its scale.

## System type and symbols

Check the license of the platform's system font and symbol set before embedding either. Some forbid it: Apple's SF fonts may not be embedded in other products, and Microsoft's Windows fonts, Segoe UI and Segoe Fluent Icons among them, may not be redistributed. Others are openly licensed, such as Roboto under the SIL Open Font License and Material Symbols under the Apache License 2.0.

- **Type whose license forbids embedding:** render it through `font-family: system-ui`. It shows the system font of the machine that opens the page, which is the target platform's only on that platform.
- **Symbols whose license forbids embedding, or can't be confirmed:** draw stand-ins, such as inline SVG shapes of a similar size and weight. Don't copy the set's glyphs.
- **An openly licensed font or symbol set** follows the [offline-artifact contract](offline-artifact-contract.md#fonts-and-imagery) like any other font or asset: embed it with its notice, or fall back and record the limit.
- **Record each case** in the notes: the face and its license, then either the embedded file or the font the scenes render through `system-ui` on the machines reviewers use. Record which symbols are embedded and which are stand-ins. A font rendered through `system-ui` and symbols drawn as stand-ins are fidelity limits.

## Appearance and accessibility settings

Where the platform has them, show the scenes under its appearance and accessibility settings: light and dark, increased contrast, reduced transparency and reduced motion.

- **One control, outside the scenes.** Put a settings control in the page around the scenes, never inside a scene. A scene stands for the device's screen, so a control drawn inside it reads as part of the product.
- **It switches every scene at once,** for example by setting attributes on the page's root element that the scenes' tokens read, such as `data-appearance="dark"`, `data-contrast="more"`, `data-transparency="reduce"` and `data-motion="reduce"`.
- **It starts from the operating system's settings** through the CSS media features `prefers-color-scheme`, `prefers-contrast`, `prefers-reduced-transparency` and `prefers-reduced-motion`, read with `matchMedia()` when the page loads.
- **It forces each setting where its media feature is unavailable.** `prefers-reduced-transparency` is experimental and not Baseline ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency)), so some browsers never report it. A feature is unavailable when none of its values matches, for example when neither `(prefers-reduced-transparency: reduce)` nor `(prefers-reduced-transparency: no-preference)` does. Start that setting at the platform's default, such as full transparency, and keep its switch, so the reviewer can still see the scenes under it.

Record in the notes which settings the platform has and which the scenes show, and record the check of the scenes under each setting in the notes' verification table.
