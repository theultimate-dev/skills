# Visual directions: Harbor

Status: proposals (nothing rendered yet; these are briefs, not prototypes)

## Shared context

- Audience, task, and representative content:
  - Audience: someone who runs a home server and glances at Harbor several times a day. They open it fully only when something failed.
  - Primary task: decide in a second whether last night's backup worked, and if not, which volume failed and why.
  - Representative content, identical in every direction (from `project/README.md`):
    - Last backup: Today 03:12 · 41.2 GB · 1 warning, 1 failure
    - Next run: Tonight 03:00
    - Volumes: Photos OK; Documents Warning, 3 files skipped; Server config Failed, destination full
    - Actions: Back up now, Open logs, Settings…
    - Settings window: Schedule (daily time, days to skip), Destinations (backup disks and network shares, each with its free space), Notifications (failures only, warnings and failures, every run).
- Existing constraints and inspected materials:
  - Inspected: `project/README.md` only. No application code, design files, tokens, fonts, brand assets or public references exist. No `AGENTS.md` or `CLAUDE.md` in the project.
  - The README gives no destination names, free-space figures or schedule times. The sketches use sample values for these, marked as sample in the sketch, and a direction may not rely on them.
  - No browsing was available, so there are no researched references. Every direction below is a stated design hypothesis, not a finding.
- Preserve / evolve / replace decision and allowed exceptions: the README states there is no visual language to preserve. Nothing is fixed except the content, the platform and the user task above. No exceptions needed, so no question was asked.
- Scenes and states every sketch must show:
  1. Panel, the README state (1 warning, 1 failure), in each placement of the platform frame.
  2. Panel, all volumes OK. This is the state seen most days and tests how little the panel needs to say.
  3. The status item in the menu bar for both of those states, at real scale, in light and dark.
  4. Settings window, each of its three sections, in each placement. Destinations includes one destination with no free space, matching "destination full".
  5. Each state shown in light, dark, increased contrast and reduced transparency.
  6. The longest realistic volume name and failure reason wrapped, in the narrowest panel.
- Surface and platform: native surface. A macOS menu-bar status item and the panel it opens, plus the settings window that Settings… opens. The brief names both, so no surface question is needed.

## Direction A: Verdict first

- Premise and audience fit: the person wants an answer, not a list. The panel opens with one plain sentence and one large state shape that say whether last night worked, then the detail. Suits the several-glances-a-day habit: the top 80 pt answer the question and the rest can be ignored.
- Composition and information hierarchy:
  - Top: a verdict block. A large state glyph beside a two-line sentence, "1 failure, 1 warning" over "Today 03:12 · 41.2 GB".
  - Middle: the three volumes as equal rows, ordered as given, each with a state glyph, name and reason.
  - Next run as a quiet line under the volumes.
  - Bottom: Back up now as the one prominent button; Open logs and Settings… as plain text buttons.
  - Settings window: tabbed toolbar with three tabs (Schedule, Destinations, Notifications), one short form per tab.
- Typography: system face (`system-ui`, SF on macOS; not embedded, see limits below).
  - Verdict: 20 px / 24, weight 600.
  - Row title: 13 px / 18, weight 500.
  - Row reason and metadata: 12 px / 16, weight 400, secondary color.
  - Button labels: 13 px / 16, weight 500.
  - Numerals use `font-variant-numeric: tabular-nums`.
  - Measure is bounded by the panel width; reasons wrap to two lines at most.
- Spacing: scale 4, 8, 12, 16, 24. Verdict block has 16 padding and a 16 gap to the list. Rows are 36 tall with 8 vertical padding. Moderate density, roomy at the top, regular below.
- Color roles, imagery, surfaces, and motion:
  - Surface: the system's translucent panel material, so the panel reads as part of macOS.
  - State colors: OK green, warning amber, failure red, each paired with a distinct shape (see risks). Neutral text otherwise. One accent, the system accent color, for Back up now.
  - Imagery: none. The state glyph is the only graphic.
  - Motion: none, except the progress state of Back up now, which shows a labeled determinate bar; under reduced motion it becomes a static "Running" label with a percentage.
- Placements and scale: what changes in each placement of the platform frame.
  - Built-in display with cut-out: panel anchors below its status item. If the status item sits near the cut-out, the panel is clamped to stay clear of the cut-out. Content does not change. If a notification banner covers the panel's top right, the panel stays put and the actions stay at the bottom.
  - External display without cut-out: panel anchors under the status item with its full width and the verdict block unchanged.
  - Full-screen app: the panel appears after the menu bar is revealed and sits over arbitrary app content, so the translucent material has to hold its contrast over busy backgrounds.
  - Settings window: smallest size keeps the tab bar and shortens the form; default size is as drawn; beside another window it behaves as at default size. Nothing is hidden at the smallest size.
- Platform fit:
  - Materials: system panel material, system accent color.
  - Standard controls: system buttons, pop-up menus, time picker and checkboxes in Settings, standard tab toolbar.
  - Design guidelines: Apple's Human Interface Guidelines for menu-bar extras, windows and settings.
  - Deliberate departure: a custom verdict header in place of a plain menu list, because the answer must be readable without parsing three rows.
- Concrete candidate tokens (to be tuned in the render):
  - `--font-ui: system-ui`
  - `--text-verdict: 20px`, `--text-body: 13px`, `--text-meta: 12px`
  - `--space-1: 4px`, `--space-2: 8px`, `--space-3: 12px`, `--space-4: 16px`, `--space-5: 24px`
  - `--panel-width: 320px` (a design choice of this direction, not a platform value)
  - `--row-height: 36px`
  - `--state-ok: #2f9e55`, `--state-warn: #c98a00`, `--state-fail: #d33a2c`
- Public/project references and principles adapted, if any: none consulted. Hypothesis: a headline-first layout shortens the time to the answer for a glance.
- Usability tradeoffs and assumptions: the verdict block uses height that a denser list would give to volumes. If the user has many volumes the list will scroll sooner. Assumes three volumes are typical. Assumes people prefer a sentence over scanning glyphs.
- Native risks:
  - Reading at hardware size: 12 px reasons are secondary text at the frame's scale; the render must show them at real scale, not enlarged, and check the wrapped "destination full" line.
  - Competing with system UI for space: the status item can be pushed under the cut-out or dropped when the menu bar is full, so the panel can't be opened; the status item must stay narrow (glyph only, no text). The panel must stay clear of the cut-out and the display edge.
  - States that rely on color alone: the status item is typically drawn monochrome, so its failure and warning states are separate shapes (a circle with a check, a triangle, a square with a cross), and the panel rows repeat the state as a word as well as shape and color.
- Font or asset availability and offline rendering limitations: SF is not embedded (license forbids it); it renders through `system-ui`, so machines that are not macOS show their own system font. SF Symbols are not embedded; glyphs are inline SVG stand-ins of similar size and weight. Both are limits to record in the render.

## Direction B: Volume ledger

- Premise and audience fit: someone who runs a home server is used to tables and logs. The panel is a dense ledger where each volume is a row with aligned columns, and the run summary is one compact line. Suits the person who wants to see everything at once and compare volumes.
- Composition and information hierarchy:
  - Top: one summary line, "Today 03:12 · 41.2 GB · 1 warning · 1 failure", with Next run right-aligned on the same line.
  - Body: a table with columns State (shape and word), Volume, and Detail. Failures are not sorted ahead; order is stable so rows keep their position between glances.
  - Footer: a toolbar row with Back up now, Open logs and Settings… as equal-weight standard buttons.
  - Settings window: a single scrolling grouped form with the three sections stacked and labeled, no tabs.
- Typography: system face (`system-ui`, not embedded).
  - Summary: 12 px / 16, weight 500.
  - Table text: 12 px / 16, weight 400; State words in weight 600.
  - Column headers: 11 px / 14, weight 500, secondary color.
  - Volume names and numerals tabular-nums; detail text single-line with truncation and a full-text tooltip.
- Spacing: scale 2, 4, 8, 12, 16. Rows are 24 tall, 4 vertical padding, 8 column gap, 12 panel padding. High density, no card boundaries; hairline separators.
- Color roles, imagery, surfaces, and motion:
  - Surface: the system's standard menu or panel material, near-flat with hairlines.
  - Color is restrained: neutral text, and state color only on the state shape and its word.
  - Imagery: none.
  - Motion: none. A running backup shows a text status in the summary line, so reduced motion changes nothing.
- Placements and scale: what changes in each placement of the platform frame.
  - Built-in display with cut-out: panel clamps away from the cut-out; the detail column truncates first, never State or Volume. If a notification banner covers the panel's top right, the summary line's Next run may be covered; it moves below the summary.
  - External display without cut-out: same panel; detail column has more room before truncating.
  - Full-screen app: the panel sits over arbitrary app content, so hairlines and text must hold over the translucent material.
  - Settings window: smallest size lets the form scroll vertically with section headings pinned; default size shows all three sections without scrolling; beside another window it reflows labels above fields only if the window is below default width. Nothing is hidden.
- Platform fit:
  - Materials: system panel material; no custom surfaces.
  - Standard controls: table-style list, system buttons, grouped form with system controls.
  - Design guidelines: Apple's Human Interface Guidelines, closest to a stock macOS utility.
  - Deliberate departure: none beyond content; it keeps to the stock look to be the most native option.
- Concrete candidate tokens:
  - `--font-ui: system-ui`
  - `--text-body: 12px`, `--text-header: 11px`
  - `--space-1: 2px`, `--space-2: 4px`, `--space-3: 8px`, `--space-4: 12px`, `--space-5: 16px`
  - `--panel-width: 360px` (a design choice of this direction, not a platform value)
  - `--row-height: 24px`
  - `--state-ok: #2f9e55`, `--state-warn: #c98a00`, `--state-fail: #d33a2c` (used for shapes only)
- Public/project references and principles adapted, if any: none consulted. Hypothesis: aligned columns let the eye compare states without reading each line.
- Usability tradeoffs and assumptions: the failure does not stand out by position or size, only by its shape and word, so a glance may take longer than in A. Truncating the detail may cut "destination full" if the column is short; the render must show the cut at the narrowest width. Assumes the user's volume count stays small.
- Native risks:
  - Reading at hardware size: 11 and 12 px text at the frame's scale is the smallest of the three directions; the render must check column headers and the wrapped detail at real scale.
  - Competing with system UI for space: the wider panel (360) is the one most affected by the display edge or the cut-out; the status item must stay narrow. If the status item shows a count it can be dropped when the menu bar is full, so the count is not the only carrier of the state.
  - States that rely on color alone: shape plus word in every row and distinct shapes in the status item, the same as A, and the state word is the primary carrier here.
- Font or asset availability and offline rendering limitations: same as A. SF is not embedded and renders through `system-ui`; SF Symbols are inline SVG stand-ins.

## Direction C: Triage queue

- Premise and audience fit: most days nothing is wrong. The panel leads with what needs attention and folds the rest away. Failures first and expanded, warnings next, OK volumes collapsed to one line. Suits a person who opens Harbor only to act.
- Composition and information hierarchy:
  - Top: a short status line, "Needs attention · 2 of 3 volumes", then run time and size in secondary text.
  - Body: an ordered queue. The failed volume, Server config, is an expanded card with its reason, "destination full", and a primary contextual action (Open logs). Documents, with the warning, is a compact card with "3 files skipped". Photos is folded into a single line "1 volume OK" that expands on click.
  - When every volume is OK, the body is one line, "All volumes OK", and Next run.
  - Footer: Back up now and Settings…, with Open logs moved into the failure card and also kept as a text button.
  - Settings window: sidebar with the three sections, list on the left and form on the right.
- Typography: system face (`system-ui`, not embedded).
  - Status line: 15 px / 20, weight 600.
  - Card title: 13 px / 18, weight 600.
  - Card reason: 13 px / 18, weight 400.
  - Meta: 11 px / 14, weight 400, secondary color.
  - Numerals use tabular-nums.
- Spacing: scale 4, 8, 12, 16, 20. Cards have 12 padding and 8 gap; the failure card has 16 padding. Medium density that varies with the state: the worse the news, the more space.
- Color roles, imagery, surfaces, and motion:
  - Surface: translucent panel material with opaque inset cards, which keeps the failure card legible over any backdrop.
  - Failure card gets a tinted state surface and a heavier left edge; the warning card a lighter tint; OK is neutral.
  - Imagery: none.
  - Motion: the folded line expands and collapses with a short 150 ms height change; under reduced motion it switches instantly.
- Placements and scale: what changes in each placement of the platform frame.
  - Built-in display with cut-out: the panel is clamped away from the cut-out; its height varies by state, so a long queue is capped and scrolls rather than reaching the cut-out or the display edge. If a notification banner covers the panel's top right, the status line is on the left and stays readable.
  - External display without cut-out: height cap is larger; no content change.
  - Full-screen app: opaque cards matter most here, since the panel material sits over arbitrary app content.
  - Settings window: smallest size collapses the sidebar into a pop-up menu above the form; default size shows sidebar and form; beside another window keeps the sidebar. Nothing is hidden.
- Platform fit:
  - Materials: translucent panel material plus custom opaque cards; system accent color.
  - Standard controls: system buttons, disclosure for the folded line, system form controls in Settings, standard sidebar list.
  - Design guidelines: Apple's Human Interface Guidelines for menu-bar extras, sidebars and settings.
  - Deliberate departures: (1) cards instead of a plain list, so a failure can show its reason and action in place; (2) reordering rows by severity, which breaks position stability between glances, accepted because failures are what the person opens Harbor for.
- Concrete candidate tokens:
  - `--font-ui: system-ui`
  - `--text-status: 15px`, `--text-body: 13px`, `--text-meta: 11px`
  - `--space-1: 4px`, `--space-2: 8px`, `--space-3: 12px`, `--space-4: 16px`, `--space-5: 20px`
  - `--panel-width: 340px` (a design choice of this direction, not a platform value)
  - `--card-radius: 10px` (design choice; the sketch must not present it as a system value)
  - `--state-ok: #2f9e55`, `--state-warn: #c98a00`, `--state-fail: #d33a2c`, with 12 percent tinted surfaces for warn and fail
- Public/project references and principles adapted, if any: none consulted. Hypothesis: showing the failing item with its action in place saves a trip to the logs.
- Usability tradeoffs and assumptions: folding OK volumes hides information that a person might want, and the order of volumes changes from one night to the next. A layout that changes height with state can feel unsteady. Assumes failures are rare enough that the common view is short.
- Native risks:
  - Reading at hardware size: 11 px meta text and the card edge cue at real scale; the render must check the failure card's tint and the left edge against the panel material.
  - Competing with system UI for space: the variable height must be capped by the display height and the cut-out clearance; the status item must show the state by shape and stay narrow.
  - States that rely on color alone: failure and warning are told apart by their position in the queue, their shape and their word, and not only by the tint; the expanded or folded state of the OK line is shown by a disclosure arrow and not by motion alone.
- Font or asset availability and offline rendering limitations: same as A. SF is not embedded; SF Symbols are inline SVG stand-ins. The disclosure arrow is a drawn stand-in.

## Sketch rendering request

Render the same content and task in one offline HTML file per direction, three files in all (`direction-a.html`, `direction-b.html`, `direction-c.html`).

- Embed CSS; use no external assets and minimal inline JavaScript (only the light/dark and settings toggles, the C folded line, and the placement switcher).
- Every geometry token goes into `:root` as a custom property as the frame lists it. The sketches share the frame and each direction's own tokens.
- Fidelity: medium-high for type, spacing, state shapes and materials; low for application logic. Draw the system menu bar, the other status items and the cut-out as simple stand-in shapes, at real scale from the frame's tokens.
- Show the scenes under "Shared context", in every placement of the frame, in light, dark, increased contrast and reduced transparency. A single control may switch placements.
- Questions each sketch should answer:
  - A: does the verdict block help the glance, or does it only take up space that rows could use? Can the status item's shapes be told apart at menu-bar size?
  - B: can the ledger be read at 11 and 12 px at real scale, and does the failure stand out enough without a size or position cue? Does the detail truncate "destination full"?
  - C: does the queue make the failure faster to find and act on, and does the changing order or height cost orientation? Is the failure card legible over a busy full-screen app backdrop?
  - All: does each carry the three states without color? Does the panel hold up beside the cut-out and at the display edge?
- Do not report the output as a prototype until the sketches exist and have been viewed.

### Platform frame

One frame for all three directions; the directions refer to it and do not repeat its values.

- Placements, each drawn at real scale:
  - Panel on a built-in display with a hardware cut-out.
  - Panel on an external display without one.
  - Panel in a full-screen app, with the menu bar revealed over the app.
  - Settings window at its smallest size, at its default size, and side by side with another window.
- Scale mapping: 1 CSS px = 1 pt.
- System UI beside the surface: the macOS menu bar and the other status items, including the clock, which compete with the Harbor status item for width; system notification banners at the top right, which can cover the panel; the Dock; and, on a display with a cut-out, the cut-out itself.
- Settings to honor: appearance (light and dark), contrast (increased contrast), transparency (reduced transparency) and motion (reduced motion).
- System type and symbols: the intended face is the macOS system font (SF). Apple's license says "You may not embed the Apple Font in any software programs or other products" (https://developer.apple.com/fonts/, license list retrieved 2026-10-24 per the skill's reference; read the current license before relying on it), so the sketches render it through `font-family: system-ui` and do not embed it. Other platforms show their own system font. SF Symbols is restricted to Apple platforms and its license text could not be confirmed, so all symbols are drawn as inline SVG stand-ins of similar size and weight. Both are limits to carry into the handoff.

| Geometry token | Value | Source: document, device and date read, or "to supply" |
|---|---|---|
| `--display-width` | to supply | to supply: built-in display; no device is named and no network was available to read Apple's specifications |
| `--display-height` | to supply | to supply: built-in display |
| `--menu-bar-height` | to supply | to supply: built-in display; Apple's Human Interface Guidelines or the device's specifications |
| `--cutout-width` | to supply | to supply: built-in display |
| `--cutout-height` | to supply | to supply: built-in display |
| `--cutout-offset-x` | to supply | to supply: horizontal position of the cut-out in the menu bar |
| `--external-display-width` | to supply | to supply: no external display is named |
| `--external-display-height` | to supply | to supply |
| `--external-menu-bar-height` | to supply | to supply |
| `--status-item-width` | to supply | to supply: width of a status item with a glyph |
| `--settings-min-width` | to supply | to supply: a design choice that this brief leaves to the render; set it from the chosen direction's layout and record it |
| `--settings-default-width` | to supply | to supply, as above |
| `--settings-default-height` | to supply | to supply, as above |

The sketches may use clearly labeled placeholder values to draw these, but may not present them as the device's.

### Open questions for the user

None blocks the directions, so none stopped the work. For the render:

1. Which Mac and display do you want the sketches sized for, and which macOS version is the target? The geometry tokens above need a named device. Recommendation: the current MacBook Pro built-in display for the cut-out placement, and a common 16:9 external display, on the latest macOS you target, since the cut-out placement is the one that constrains the panel most.
2. May the sketches use sample destination names and free-space figures, since the README gives none? Recommendation: yes, marked as sample in the sketch.

## Comparison after rendering

To fill in after the sketches are rendered and viewed.

| Criterion | A | B | C |
|---|---|---|---|
| Task clarity and hierarchy | | | |
| Typography and reading comfort | | | |
| Spacing and density | | | |
| Placements and scale | | | |
| Platform fit | | | |
| Identity and project fit | | | |
| Risks and limitations | | | |

- Recommendation and reasons: provisional, and it will be revised after rendering. Lean toward C for the first render pass: Harbor's main use is to find out whether something failed and then act, and C is the one direction that puts the failure and its action in the same place. A is the fallback if the changing order of C unsettles the glance. B is the stock baseline and the best fit if the user wants maximal native familiarity, but it asks the most of 11 and 12 px text at hardware size. This is a hypothesis, not a finding; the final choice should use the rendered sketches at real scale in each placement.
- User selection or explicitly delegated decision: none yet.
- If combining: exact retained elements and the resulting coherent direction: none yet. If the user combines, for example A's verdict header with C's severity order, rewrite one brief with one hierarchy and one token set, and not "mix A and C".
- Refinements to carry into the next prototype: none yet.
