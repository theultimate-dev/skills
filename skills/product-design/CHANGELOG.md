# Changelog

All notable changes to the `product-design` plugin are documented in this file. Changes to the marketplace and the repository around it are in the [root changelog](../../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this plugin adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are tagged `product-design--vX.Y.Z`.

## [Unreleased]

## [0.3.0] - 2026-10-25

### Added

- `exploring-visual-directions` handles native platform surfaces, such as a menu-bar panel, a desktop window, a phone widget, a watch face, or a TV or car screen.
  - It recognizes one from the brief or from the project's code, and asks you when neither settles it.
  - Each direction states:
    - its placements at real scale, in place of narrow-screen changes;
    - its platform fit: materials, standard controls, guidelines, and each deliberate departure with its reason;
    - native risks, such as reading at hardware size.
  - The rendering task carries one platform frame for all three sketches: the placements, the scale mapping, geometry tokens with their sources, the system UI beside the surface, and the appearance and accessibility settings to honor.
  - System type and symbols are embedded only when their license allows it. Otherwise they render through `system-ui` and as drawn stand-ins.
  - A new native-surfaces reference holds the detail, and the comparison template marks its native and responsive lines.
  - Responsive pages keep their briefs as before.
- `designing-ux-flows` gives a native platform surface its placements in place of narrow-screen behavior: the displays and states it appears in, at real scale, and what changes in each. The UX specification template marks its native and responsive lines.
- `preparing-implementation-handoffs` carries a native surface's design into the handoff:
  - its placements and scale, in place of responsive rules;
  - its platform frame: the scale mapping, the geometry tokens with their sources, the system UI beside the surface, and the settings honored;
  - the system type and symbol limits, next to the font limitations.

  The handoff template marks its native and responsive lines. Responsive pages keep their narrow-screen behavior and responsive rules.

### Changed

- The native-surface profile in `building-html-prototypes` checks the license of a platform's system font and symbol set, rather than never embedding them:
  - When the license forbids embedding, as for Apple's SF fonts and Segoe UI, the scenes render the font through `system-ui` and draw stand-ins for the symbols, as before.
  - An openly licensed one, such as Roboto, is embedded or falls back like any other font.
  - The prototype notes record the face, its license, and which case applies. A font rendered through `system-ui` and symbols drawn as stand-ins are recorded as fidelity limits.
- When a direction brief supplies a platform frame, the profile starts from it. It draws a scene for each placement, its values and sources go into the notes as written, and you're asked only for what the frame lacks. The prototype notes gain Placements and System UI lines, so every field of the frame has a place.
- `guiding-product-discovery` lists placements for a native surface next to responsive behavior in the Converge phase.

## [0.2.0] - 2026-10-24

### Added

- `building-html-prototypes` can build a design tree: prototype pages that link the project's shared `tokens.css`, `components.css` and other design files by relative path instead of copying them, and that still open offline from disk while the tree stays together. Its rules are in a new design-tree contract, and the prototype notes name the contract and the tree's root folder, and list the shared files each page links.
- `templates/tree-check.html` in `building-html-prototypes`, a page you serve locally next to a staged copy of a design tree. It reads the references in the tree's pages and stylesheets and reports each one that points to a remote host, uses a root-absolute path, climbs out of the tree or names a missing file, as `PASS` and `FAIL` lines that a headless browser can read.
- `building-html-prototypes` exercises stateful interactions without a browser-driving tool. A new scripted-checks reference and `templates/interaction-harness.html` load the prototype in a same-origin frame over local HTTP, dispatch pointer and keyboard events, let timers run, and assert on DOM state, focus and ARIA attributes. A scripted check is required for every stateful interaction no browser-driving tool can exercise, and the notes record each check by name.
- `templates/page-slices.html` in `building-html-prototypes` shows a long page in a frame of fixed size scrolled to an offset, so a headless screenshot captures it in readable slices instead of one tall image.
- `building-html-prototypes` checks a design tree that reviewers will open through a host. Besides opening it from disk, the agent serves the exact file set under a nested prefix such as `/a/b/` from a local server, repeats the render check with the tree check and the interaction harness, and records the result in its own row of the notes. The design-tree contract describes an entry page at the tree's root for hosts that publish one page, and says to publish only the pages and the files they reach, after you confirm the list and who can open it. For any artifact reviewed through a host the agent can't open itself, the notes record the host's render as "not performed", and the agent asks you to confirm it.
- A native-surface profile in `building-html-prototypes` for prototypes of a menu-bar panel, desktop window, phone widget or watch face. Each surface is drawn as a scene at a stated scale, such as 1 CSS px = 1 pt, and checked at device scale factors 1 and 2. The device's geometry comes from sourced values kept as tokens. Each scene scrolls inside its own container while the page around it still reflows at 320 CSS px, which replaces the 320 px check for the scenes. The system font renders through `system-ui`, and system symbols are drawn stand-ins. A settings control outside the scenes shows light and dark, increased contrast, reduced transparency and reduced motion, and it starts from the operating system's settings. The prototype notes gain a section for the scale, the geometry sources and these fidelity limits.

### Changed

- A single offline HTML file stays the default, and direction sketches stay one file even in a project with shared design files; a sketch may keep its candidate tokens inline until you choose a direction. The skill, the plugin description, the repository README and the coordinator's task brief no longer say that every prototype is one file.

## [0.1.0] - 2026-09-28

### Added

- Six stack-neutral skills for guided discovery, product briefs, UX flows, visual direction exploration, offline HTML prototypes, and product/design handoffs. Includes copyable templates, fictional worked examples, typography and spacing guidance, and checkpoints for user decisions.

[Unreleased]: https://github.com/theultimate-dev/skills/compare/product-design--v0.3.0...HEAD
[0.3.0]: https://github.com/theultimate-dev/skills/compare/product-design--v0.2.0...product-design--v0.3.0
[0.2.0]: https://github.com/theultimate-dev/skills/compare/product-design--v0.1.0...product-design--v0.2.0
[0.1.0]: https://github.com/theultimate-dev/skills/releases/tag/product-design--v0.1.0
