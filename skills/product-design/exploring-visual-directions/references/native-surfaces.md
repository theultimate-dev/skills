# Native surfaces

A native platform surface is drawn at the device's own scale, beside the platform's own interface. It doesn't reflow the way a web page does, so its directions describe placements instead of responsive changes, and its sketches share one platform frame.

## Identify the surface

Treat a view as a native surface when either of these names one:

- **The brief**, for example:
  - a menu-bar or tray item and the panel it opens;
  - a desktop window, a settings window or a notification;
  - a phone app screen, or a home-screen or lock-screen widget;
  - a watch face or complication;
  - a TV home screen, or a car's dashboard display.
- **The project**, when its code builds a native app, for example:
  - a Swift package or Xcode project with a macOS, iOS, watchOS or tvOS target, or a SwiftUI `MenuBarExtra`;
  - an Android module with a widget provider;
  - a Windows app project.

A web page opened in a browser is a responsive page, even on a phone. So is a web app with no native target.

A brief that covers both kinds, such as a menu-bar panel and a web account page, gives each surface its own directions: placements and a platform frame for the panel, narrow-screen changes for the page.

When neither the brief nor the project settles which kind a view is, ask the user before writing any direction. Name the plausible surfaces, such as a responsive web page or a native surface on a named platform, and recommend one with the reason.

## Placements

Placements are the display types and states the surface appears in, each at real scale. They replace the narrow and wide sizes of a responsive page. For example:

- **A menu-bar panel:** a built-in display with a hardware cut-out such as a camera housing; an external display without one; and a full-screen app, where the menu bar stays hidden until the pointer reaches it.
- **A phone widget:** each widget size it offers, on the home screen and on the lock screen.
- **A desktop window:** its smallest size, its default size, and side by side with another window.
- **A watch face:** each case size, and the always-on state.

List the placements once in the platform frame. Each direction then says what changes in each placement: what moves, what is truncated, what is hidden, and what the surface does when system UI takes its space.

## The platform frame

One frame per native surface, written once in the rendering task and shared by every direction. Directions refer to it, for example "at the frame's scale", and never repeat its values, the scale mapping included, so the sketches stay comparable. The fields use the terms of `building-html-prototypes`' native-surface profile, so a renderer can copy them into its prototype notes:

- **Placements:** as above.
- **Scale mapping:** how CSS pixels map to the platform's unit, for example 1 CSS px = 1 pt, or 1 CSS px = 1 dp.
- **Geometry tokens:** the display size, system bar heights, safe areas and hardware cut-outs the scenes need. Each token holds one length under a name of its own, such as `--display-width` and `--display-height` rather than one display size, so a renderer can define it as written. Give each its value and its source: the document, the device and the date read. Take values from the platform's own design guidelines or specifications for the device named. When no source gives a value, write "to supply" and add it to the questions for the user. Never present an invented value as the device's.
- **System UI beside the surface:** what competes with it for space and attention, such as the menu bar and other status items, the system's notification banners, a status bar, a home indicator or a dock.
- **Settings to honor:** appearance (light and dark), contrast (increased contrast), transparency (reduced transparency) and motion (reduced motion), where the platform has them.
- **System type and symbols:** the intended face and its license, whether the sketches embed it or render it through `system-ui`, and which symbols are drawn stand-ins. See [System type and symbols](#system-type-and-symbols).

## Platform fit

Each direction states how it uses the platform:

- **Materials:** such as translucent or blurred backgrounds, elevation, and the system's accent or wallpaper-derived color.
- **Standard controls:** such as the platform's switches, menus, segmented controls and buttons.
- **Design guidelines:** the platform guidance it follows, such as Apple's Human Interface Guidelines, Microsoft's Fluent design or Google's Material Design.

It also names each deliberate departure, with the reason: for example, a custom status row in place of a standard table, because three states must read at a glance. Or it states that it has none. A departure without a reason reads as an accident.

## System type and symbols

When the intended face is the platform's system font, say so, then check its license before deciding how the sketches render it:

- **The license forbids embedding:** render the font through `font-family: system-ui`. Record that it isn't embedded, and that machines on other platforms show their own system font in its place.
- **The font is openly licensed:** follow the embed-or-fall-back guidance in [typography and spacing](typography-and-spacing.md#offline-font-fidelity), like any other font.

The system's symbol set follows the same rule. Draw stand-ins for symbols whose license forbids embedding or can't be confirmed, such as inline SVG shapes of a similar size and weight, and record them as a limit.

Licenses retrieved on 2026-10-24. Read the current license before relying on one:

| Font or symbol set | License | Embed in a sketch? |
|---|---|---|
| Apple's SF fonts | "You may not embed the Apple Font in any software programs or other products" ([Apple](https://developer.apple.com/fonts/)) | No: `system-ui` |
| SF Symbols | Restricted to Apple platforms; the license text couldn't be confirmed | No: drawn stand-ins |
| Segoe UI | "You may not redistribute the Windows fonts" ([Microsoft](https://learn.microsoft.com/en-us/typography/fonts/font-faq)) | No: `system-ui` |
| Segoe Fluent Icons | "You may not ship it to another platform" ([Microsoft](https://learn.microsoft.com/en-us/windows/apps/design/iconography/segoe-fluent-icons-font)) | No: drawn stand-ins |
| Roboto | SIL Open Font License 1.1 ([Google Fonts](https://github.com/google/fonts/blob/main/ofl/roboto/OFL.txt)) | Yes, with its notice |
| Material Symbols | Apache License 2.0 ([Google](https://developers.google.com/fonts/docs/material_symbols)) | Yes, with its notice |

`system-ui` takes its glyphs "from the default user interface font on a given platform" ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/font-family)), so a sketch shows the target's system font only on the target platform.

## Native risks

Besides its other usability risks, each direction names these:

- **Reading at hardware size:** type, symbols and targets at the device's real size, as the frame's scale mapping draws them, not enlarged in a browser window. Small labels that read well in a large sketch can fail on the device.
- **Competing with system UI for space:** what the surface loses to the menu bar, a hardware cut-out, system bars or safe areas, and what it shows when the space shrinks.
- **States that rely on color or motion alone:** at least one state the direction must convey by shape, label or position as well, such as a failure that is not only red, or progress that still reads with reduced motion.

## Example

A fictional transit app, Linefinder, wants a phone home-screen widget that shows the next departures from a saved stop.

- **Placements:** the small and medium widget sizes on the home screen, and the lock-screen size.
- **Scale mapping:** 1 CSS px = 1 pt.
- **Geometry tokens:**
  - `--widget-small-width`: to supply.
  - `--widget-medium-width`: to supply, because the brief names no device and the platform's guidelines give sizes by device.
  - `--corner-radius`: from the platform's widget guidelines, with the document, the device and the date read.
- **System UI beside the surface:** the home screen's other icons and widgets, and the wallpaper behind them.
- **Settings to honor:** light and dark, increased contrast, reduced transparency and reduced motion.
- **System type and symbols:** the system font, whose license forbids embedding, renders through `system-ui`. Line badges are drawn as SVG stand-ins.

Direction A, "Departure board", uses the platform's standard widget material and type styles. It departs from them once: monospaced minutes, so the times line up as they change. Its native risks:

- the minutes at the small size;
- the lock-screen size losing the line colors;
- a delayed departure that is not shown by color alone.
