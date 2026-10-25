# Prototype notes: Harbor, direction A (Verdict first)

- Artifact filename, or the tree's root folder and entry page: `project/direction-a.html`. Scripted checks for it: `project/direction-a-checks.js`.
- Contract: one-file artifact ([offline artifact contract](../skill/references/offline-artifact-contract.md)). It is the default for a direction sketch, and the project keeps no shared design files. One file, inline CSS, inline SVG, one inline script, no network, no sibling files.
- Fidelity: direction sketch (medium-high for type, spacing, state shapes and materials; low for application logic, as `visual-directions.md` asks).
- Purpose and user task: decide in a second whether last night's backup worked and, if not, which volume failed and why. The sketch answers the brief's questions for A: does the verdict block help the glance or only use space that rows could use, and can the status item's three shapes be told apart at menu-bar size.
- Related requirements and UX specification: `project/README.md` (content), `project/visual-directions.md` (Direction A, platform frame, shared scenes, sketch rendering request).
- Direction status: proposed. Nothing has been selected. B and C are not rendered here, so this file compares nothing yet.
- Status of this render: **not viewed.** This session had no browser and could not start a server, so the file was written and statically checked, and never opened. Treat every visual claim below as unverified until the manual checks at the end have been done. The brief says not to report the output as a prototype until the sketches have been viewed; this is a sketch under construction.

## Shared files (design tree)

Not applicable: one-file artifact.

## Native surface (fixed-scale scenes)

- Surfaces and platform: a macOS menu-bar status item, the panel it opens, and the Settings window that Settings… opens. The user named a MacBook Pro 14-inch (default scaled resolution, with camera cut-out), an external 27-inch display and macOS 15.
- Placements, each drawn as its own scene (one at a time through the Placement control; "All" shows everything):
  1. Built-in display with cut-out: panel, 1 failure and 1 warning; panel, all volumes OK. The menu bar is crowded on purpose so the status item sits just right of the cut-out, and the panel is clamped 8 pt clear of the cut-out (panel left edge 864, cut-out right edge 856).
  2. External display without cut-out: the same two panel states. The panel is centred under the status item.
  3. Full-screen app: the same two panel states over a busy app backdrop, with a black and white checker behind the panel as a stress test for the material.
  4. Settings window at its smallest size, at its default size, and beside another window. Each has the three sections behind tabs, and all three windows follow the chosen tab.
  5. Panel details, not tied to a display: the longest realistic volume name and failure reason wrapped at the panel width; the panel while Back up now is running; the status item at menu-bar size for all OK, warning and failure, in light and dark at once.
- Scale mapping: 1 CSS px = 1 pt. Every scene is drawn at that mapping and its width equals its token (`--display-width`, `--external-display-width`). No `transform`, `zoom` or percentage width is used on a scene.
- Scene height is a sketch choice: `--scene-height: 480px` shows the top 480 pt of the display. The `--display-height` tokens are declared and unused by the scenes. The Dock, which the frame lists as system UI, is therefore not drawn. Fidelity limit.
- System type: intended face is the macOS system font (SF). Apple's license, as recorded in the brief's frame (https://developer.apple.com/fonts/, retrieved 2026-10-24 per the brief; not re-read in this session, which had no network), says the font may not be embedded. The scenes render through `font-family: system-ui, sans-serif`. On a Mac this shows SF; on any other machine the reviewer sees that machine's system font and the line breaks, widths and wrapping will differ. Fidelity limit. No font file is embedded.
- System symbols: SF Symbols is restricted to Apple platforms and its license text could not be confirmed. No symbol is copied. All glyphs are original inline SVG stand-ins: three panel state shapes (circle with check, triangle with exclamation mark, square with cross, drawn filled), three monochrome status-item outline versions of the same shapes, and three settings tab icons (clock, disk, bell). The stand-ins match the brief's size and weight only roughly. Fidelity limit.
- System UI beside the surface: menu bar with stand-in menu labels ("Files, File, Edit, View, Window, Help" are generic text, not a real app's), the cut-out as a black shape, other status items as simple outlined shapes, the clock, and a system notification banner stand-in at the top right that the page's Show a notification banner switch adds over the panel scenes. The Dock is not drawn. The "other window" beside Settings is a plain stand-in with line bars.
- Settings the platform has, and the ones the scenes show: appearance (light, dark), contrast (increased), transparency (reduced) and motion (reduced). All four are shown, switched by one control in the page around the scenes, which sets `data-appearance`, `data-contrast`, `data-transparency` and `data-motion` on the page root. It starts from the operating system through `matchMedia()`. `prefers-reduced-transparency` is experimental, so if the browser reports neither value the control starts at full transparency and the switch still works. Reduced motion changes one thing in this direction: the running Back up now bar (see below). Everything else in A is static.

| Geometry token | Value | Source: document, device and date read, or the user's answer |
|---|---|---|
| `--display-width` | 1512pt | user's answer, 2026-10-24 (MacBook Pro 14-inch, default scaled resolution) |
| `--display-height` | 982pt | user's answer, 2026-10-24 |
| `--menu-bar-height` | 37pt | user's answer, 2026-10-24 |
| `--cutout-width` | 200pt | user's answer, 2026-10-24 |
| `--cutout-height` | 32pt | user's answer, 2026-10-24 |
| `--cutout-offset-x` | 656pt (centres the cut-out) | user's answer, 2026-10-24 |
| `--external-display-width` | 2560pt | user's answer, 2026-10-24 (external 27-inch display) |
| `--external-display-height` | 1440pt | user's answer, 2026-10-24 |
| `--external-menu-bar-height` | 24pt | user's answer, 2026-10-24 |
| `--status-item-width` | 28pt | user's answer, 2026-10-24 |
| `--settings-min-width` | 440pt | design choice of this render, set from A's tabbed layout |
| `--settings-min-height` | 320pt | design choice of this render (not a token of the frame; added) |
| `--settings-default-width` | 560pt | design choice of this render |
| `--settings-default-height` | 380pt | design choice of this render |

The user says these figures are their own and not checked against Apple's specifications. They are not presented as the devices' values. The target is macOS 15 per the user's answer; nothing in the sketch depends on a macOS 15 feature.

## Design decisions

- Composition and information priority: as the brief's Direction A. The top of the panel is a verdict block: a 40 pt state shape beside a two-line sentence ("1 failure, 1 warning" over "Today 03:12 · 41.2 GB"; on an all-OK day, "All volumes OK" over the same line). Then three equal rows in the README order (Photos, Documents, Server config), each with a shape, a name and the state as a word, plus the reason when there is one. Next run is a quiet line under the rows. At the bottom, Back up now is the one filled button; Open logs and Settings… are plain text buttons. Settings is a toolbar of three tabs with one short form each.
- Typography, actual fonts/fallbacks, and fidelity limitations: verdict 20/24 weight 600; row title 13/18 weight 500; reasons and metadata 12/16 secondary; buttons 13/16 weight 500; tabular numerals on the numbers. The face is `system-ui` (see above). Not checked in a browser: wrapping, rendered fallbacks and the real size of 12 pt text at hardware scale. The brief names this as A's main reading risk and it is open.
- Spacing, density, and responsive behavior: scale 4, 8, 12, 16, 24; panel 320 pt wide; panel padding 16 and a 16 gap from the verdict block to the list. The page around the scenes is an ordinary responsive page; the scenes keep their size and scroll sideways inside labelled, focusable containers.
- Existing style/token sources and preserve/evolve/replace decision: the README says there is no visual language, no design files and no code, so nothing is preserved or inherited. Tokens are the brief's candidate tokens, declared in `:root`, and then tuned (see departures).
- Asset provenance and notices: no external assets, fonts or images. All shapes and icons are original inline SVG. Sample content: destination names ("Atlas (USB disk, sample)", "Vault (network share, sample)", "Config mirror (disk, sample)"), their free-space figures, the "Settings" days and notification default, the long names in the details scene, the clock text and the notification banner are sample values, marked "sample" in the sketch or on the page, as the user agreed ("take your defaults").
- Departures from the brief to review (flagged, not silently made):
  1. Row height. The brief says rows are 36 tall with 8 vertical padding, and that reasons wrap to two lines. A row with a reason cannot be 36 tall, so 36 is the minimum height here and rows with a reason grow (about 50). OK rows are 36.
  2. State colors. The brief's `#2f9e55`, `#c98a00`, `#d33a2c` are kept as `--state-ok`, `--state-warn`, `--state-fail` in `:root`, but the tuned values that the glyphs use differ per appearance: light `#2a8f4d`, `#a56a00`, `#d33a2c`; dark `#4cc16f`, `#e3a21a`, `#ff6b5e`; increased contrast values are darker (light) or lighter (dark). Reason: computed against the light panel over a mid-gray backdrop, the brief's green is 2.79:1 and its amber 2.40:1, under the 3:1 I used as the target for a shape (the red is 3.88:1 and is kept). The brief invited tuning in the render. `--state-*` are therefore declared but not used by the glyphs; they are kept for the handoff comparison.
  3. System accent. The accent color for Back up now is a fixed blue (`#0a5fd0` light, `#0a68e0` dark, tuned so white 13 pt text reaches 4.5:1). A real Mac would use the user's chosen accent color. Link-colored text buttons use a separate link value.
  4. The Running state is a one-shot CSS fill to 42 percent, not a live progress. Normal motion shows "Running" with the bar filling; reduced motion shows "Running · 42%" and a static bar. The percentage is a sample.
  5. A sixth control, "All", in the Placement control, and a notification-banner switch, were added to the page (outside the scenes) so a reviewer can see every placement and the banner case. The brief allows one control for placements.

## Demonstrated behavior

- Starting state and sample content: Placement starts on the built-in display. Appearance, contrast, transparency and motion start from the operating system. The Settings tabs start on Schedule.
- Primary actions and expected results: Placement control shows one group of scenes (or all). The settings control restyles all scenes at once. A tab in any Settings window shows that section in all three windows; arrow keys, Home and End move between tabs. The form controls in Settings (time, day checkboxes, notification radios) work locally and are not saved.
- Recovery states: none to demonstrate. This is a status display with no destructive action. The failure state, with its reason, "Destination full", and a full destination in Settings, is the scenario.
- Simulations and omitted behavior: the panel's buttons (Back up now, Open logs, Settings…) are drawn controls and do nothing; they send no request and open nothing. The status item does not open the panel; the panel is always drawn open. Volumes do not scroll, and the many-volumes case is not drawn. Not drawn: an "idle" panel with nothing ever run, a warning-only panel, a first run, destination-add flows, window resizing by dragging, the Dock, the menu bar being full to the point of dropping the Harbor item, the panel clamped at the display edge. The Settings windows at their smallest size scroll inside the form if the content is taller than the window; that was not looked at.
- State reset behavior: reload resets everything. Nothing is stored.

## Verification

Legend: "performed" means run in this session. This session had no browser, no server and no screenshot tool, so every rendering and interaction check is "not performed". Static checks were run with the Python and Node scripts in `work/` (they are helpers, not deliverables).

| Check | Result: passed / failed / not performed | Evidence and conditions |
|---|---|---|
| Design-tree check (`tree-check.html`), for a design tree | not applicable | One-file artifact. |
| Static portability: no remote or sibling dependency | passed | Scan of `direction-a.html` for `http(s)://`, `//` URLs, `url(`, `@import`, `src=`, `<link`, `<iframe`, `<form`, `<img`, `fetch(`, `XMLHttpRequest`, `import(`: none found. The only `<use>` references are in-document (`#g-ok` and so on) and each resolves to a `<symbol>`. |
| Static portability: markup and script syntax | passed | Python `html.parser` pass: tags balanced, no duplicate ids, every `for`, `aria-labelledby` and `aria-controls` target exists. `node --check` on the extracted inline script and on `direction-a-checks.js`: no syntax errors. The script was read for requests and imports: it makes none. |
| Geometry tokens in `:root` match the user's answer | passed | Text match of all ten tokens and values from the table above against the declarations in the file. |
| Contrast, computed (not rendered) | passed, with listed exceptions | `work/check_contrast.py` over light, dark, increased-contrast light and dark. Targets: text and secondary text and link on the panel at least 4.5:1, state shapes at least 3:1 against the panel, marks on shapes at least 3:1, button text on the accent at least 4.5:1, text on the window and toolbar at least 4.5:1. Panel backdrop cases: mid-gray (the requirement), and pure black and white as stress. All requirements pass. Stress exceptions: light `--glyph-ok` against the panel over pure black is 2.88:1; dark link text over pure white is 4.45:1; light menu bar text was only checked at the stress extremes, not against the wallpaper actually drawn. Contrast against the real wallpaper and the real full-screen backdrop is not computed. |
| Direct file opening and offline behavior | not performed | No browser. Expected: opens through `file://` with no console errors and no requests. |
| Hosted render under a nested prefix (`/a/b/`), through the entry page, for an artifact reviewed through a host | not performed | One-file artifact with no relative paths; optional. |
| Hosted render on the review host | not performed | The host is not available to me. Please open the published file and confirm that it renders, with the scenes and controls working. Until you answer, this stays "not performed". |
| Primary task and recovery | not performed | Needs a rendering. |
| Scripted: placement control shows only the chosen group and All shows every group | not performed | Written in `direction-a-checks.js`; not run (no server or browser). |
| Scripted: settings control sets appearance, contrast, transparency, motion and banner on the page root | not performed | As above. Assumes the operating system is not already in reduced motion for the motion check. |
| Scripted: notification banner appears over the panel only when switched on | not performed | As above. |
| Scripted: choosing a settings tab shows that section in every settings window | not performed | As above. |
| Scripted: arrow keys move between tabs, wrap, and keep focus on the selected tab | not performed | As above. Real Tab order still needs a browser-driving tool or a manual pass. |
| Scripted: reduced motion replaces the Running label with Running and a percentage | not performed | As above. |
| Scripted: every fixed-scale scene keeps its token width and scrolls inside its own container | not performed | As above; run it in the harness with `width=320`, then `width=1024`. |
| Driven: (none) | not performed | No browser-driving tool was available. |
| Keyboard and focus | not performed | Expected: scene containers and the Settings controls are in the Tab order; the panel's drawn buttons are focusable but inert. |
| Narrow and wide layouts | not performed | Expected: the page reflows at 320 CSS px; scenes keep their size. |
| Native scenes at device scale factors 1 and 2 | not performed | Needs screenshots at both. Look at hairlines (0.5 pt borders on the panel and window), the SVG stand-ins and the cut-out corners. |
| Native scenes in a 320 CSS px frame: no page scroll, and each scene scrolls in its own container | not performed | The last scripted check covers it. |
| Native scenes under each setting they show, switched from the settings control | not performed | Needs a rendering of each of: light, dark, increased contrast, reduced transparency, reduced motion. |
| Long-page slices (`page-slices.html`) | not performed | Page is long with "All" selected; slice it at 1024 by 768 when a browser is available. |
| Zoom and text-spacing overrides | not performed | Expected risk: the panel is fixed-scale, so only the page around it reflows. Check the Settings form at the smallest size under the overrides. |
| Contrast and reduced motion, if applicable | partly | Contrast computed (above), not seen. Reduced motion has one effect (the running bar) and is written as CSS plus a scripted check; neither has run. |

### Manual checks for a reviewer (unverified until done)

1. Open `direction-a.html` from disk with the network off. Confirm no console errors, and that Placement starts on Built-in display.
2. Built-in display: the panel's left edge is clear of the black cut-out; the status item (square with a cross) is highlighted. Tick Show a notification banner: it covers the panel's top right and the buttons at the bottom stay visible.
3. At 100 percent browser zoom on the Mac you review on, read the 12 pt reasons ("3 files skipped", "Destination full") against a ruler of the real menu: are they readable? That answers A's first risk.
4. Panel details: in the long-names scene, "Destination full: the config mirror disk has 0 B free" wraps to at most two lines and nothing overlaps. Switch to the status-item scene and compare the three shapes at their drawn size, light and dark.
5. Full-screen app: read the panel text over the checker. Switch on Reduce transparency and compare.
6. Switch Dark, Increase contrast, Reduce transparency, Reduce motion one at a time in each placement. In the running scene, reduced motion shows "Running · 42%".
7. Settings: choose each tab; the three windows follow. Use Left, Right, Home and End. At the smallest size nothing should be cut off; scroll the form if needed.
8. At 320 CSS px wide: the page does not scroll sideways, and each scene scrolls inside its own bordered, focusable container.
9. Screenshot each scene at device scale factors 1 and 2.

## Review decision

- Observations and recommendation: not formed yet, because the sketch has not been viewed and B and C do not exist. By construction, A's verdict block uses about 64 pt of height (a 40 pt shape in a 16 pt padded block) that a dense list would give to volumes; the brief's question about that cost can only be answered by viewing. The brief's provisional lean toward C stands as a hypothesis, with A as the fallback.
- User feedback and resulting changes: the user supplied the device figures (2026-10-24) and accepted sample content and defaults. No feedback on the render yet.
- Unresolved questions or limitations: the render is unviewed and unrun; the departures listed under Design decisions need your decision, most of all the tuned state colors and the 36 pt row minimum; the display crop leaves the Dock out; fonts and symbols are stand-ins; the figures were not checked against Apple's specifications.
- Next refinement or handoff: open the file and do the manual checks, then render B and C against the same frame so the comparison table in `visual-directions.md` can be filled in from the rendered sketches. Choose a direction after that; this sketch should not be deepened before the choice.
