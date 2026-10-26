# Layout rules

A design home keeps four rules so that every value has one home and every page still works when it is copied or published as a whole. This reference explains each rule with examples, and says how to fix a breach.

## Contents

- [An example home](#an-example-home)
- [Foundations hold no platform styles](#foundations-hold-no-platform-styles)
- [A platform stylesheet draws only what the operating system draws](#a-platform-stylesheet-draws-only-what-the-operating-system-draws)
- [A view's own surfaces are styled once](#a-views-own-surfaces-are-styled-once)
- [Pages link by relative path only](#pages-link-by-relative-path-only)
- [What the tree check cannot see](#what-the-tree-check-cannot-see)

## An example home

A fictional backup watcher with a macOS menu-bar app and a web account page might keep this home:

```
design/
├── README.md             the layout, its rules, how to add a platform or a view
├── index.html            entry page: links every view
├── foundations/
│   ├── tokens.css        colour, type, space, radius and motion roles
│   └── components.css    shared components, such as buttons and status rows
├── macos/
│   ├── macos.css         what macOS draws: the menu bar, window chrome, geometry tokens
│   ├── status-panel/
│   │   ├── index.html
│   │   └── status-panel.css
│   └── settings/
│       ├── index.html
│       └── settings.css
└── web/
    └── account/
        ├── index.html
        └── account.css
```

The status panel's page links `foundations/tokens.css` and `foundations/components.css` by climbing two folders, to the home's root, and then down. It links `macos/macos.css` by climbing one folder, and its own `status-panel.css` by name. The web platform has no platform stylesheet, because the operating system draws nothing inside a web page.

## Foundations hold no platform styles

The foundations hold what every platform shares:

- **Tokens by role:** colour, type, space, radius and motion. Each role holds a value that reads correctly wherever the home's platforms use it, such as `--color-surface` or `--space-2`.
- **Shared components:** parts that look and behave the same wherever they appear, such as a button or a status row. They are written with the tokens.

Test each value: would it be wrong on another platform the home serves? If so, it is a platform style, and it goes in that platform's folder. Examples:

| Value | Where it goes | Why |
|---|---|---|
| `--color-accent: #205d42` | foundations | The product's own colour, on every platform |
| `--menu-bar-height` | `macos/` | Only macOS draws a menu bar, and its height comes from Apple's specifications for the device |
| A safe-area inset for a phone's camera cut-out | the phone platform's folder | It belongs to one device's geometry |
| A translucent panel material that imitates the system's | the platform's folder | It is the operating system's look, not the product's |

**Fix a breach:** move the value into the platform's folder, and link that platform's stylesheet from its views. When a foundation component needs the value, give the component a token that each platform's stylesheet sets, or keep a platform variant of the component in the platform's folder.

## A platform stylesheet draws only what the operating system draws

A platform stylesheet draws the system UI beside the product, so that a view can be judged in place:

- the menu bar and other status items;
- window chrome;
- a status bar or a home indicator;
- the device's frame.

It also holds the platform's geometry tokens, each with its source: display size, system bar heights, safe areas and hardware cut-outs. Each source is the document, the device and the date it was read, so nobody mistakes an invented value for the device's.

It never holds the product's own controls, even when they imitate the platform. A switch the product shows is the product's component: it goes in the foundations, or in the view's stylesheet when only that view has it.

**Fix a breach:** move the product's rule into the foundations or the view's stylesheet, and keep only the system UI in the platform's file.

## A view's own surfaces are styled once

A surface is a region of a view that the view owns, such as a status panel, a settings pane or an account summary. Its rules live once, in that view's stylesheet next to its pages.

When another view shows the same surface, its page links the first view's stylesheet by relative path, for example climbing out of its own folder into its sibling's. It never copies the rules: a copy drifts the first time either view changes.

A part that repeats, such as a status row shown several times, is not a surface. It is a shared component in the foundations, even while only one view uses it.

**Fix a breach:** delete the copied rules, link the owning view's stylesheet, and confirm with the tree check that the link resolves.

## Pages link by relative path only

Every page in the home follows these rules:

- **Full documents.** Each page is a full HTML document with its own doctype, `html`, a `head` with `meta charset` and `title`, and a `body`, so it opens on its own in a browser.
- **Relative paths only.** Every `href`, `src`, `srcset` and CSS `url()` that names a file is a relative path to a file inside the home.
  - A path may climb to a parent folder, as long as it stays inside the home. It never climbs above the home's root.
  - Name the file, not its folder, because a folder does not open its index page from disk.
  - Do not add a `base` element, which changes how every relative path resolves.
- **No root-absolute paths.** A path that starts with `/` resolves against the host or the disk, not the home.
- **No network.** No remote fonts, styles, scripts, images or frames.
- **No build step.** The files in the home are the files a browser opens.
- **No modules or imports.** No JavaScript modules and no CSS `@import`. Link each stylesheet from every page that uses it, so each page's dependencies are visible in its `head`. Classic scripts linked by `<script src>` are allowed.
- **No requests.** No `fetch`, `XMLHttpRequest`, remote forms, service workers or external APIs for the behavior a page demonstrates.

Every page then renders and completes its demonstrated task through `file://`, with the network off, as long as the home is copied or moved as a whole. A page moved out of the home is expected to break.

**Fix a breach:** replace the reference with a relative path to a file inside the home. When a font, image or script must come from elsewhere, copy it into the home where its license allows, and keep the source and license in the README.

## What the tree check cannot see

The tree check follows the entry page's links, reads the pages listed in `pages`, and reads every stylesheet they link. It does not see:

- pages that no link reaches and that `pages` does not list;
- scripts: read each one for requests and imports;
- an `image-set()` string, an `iframe` `srcdoc` or a `ping` attribute;
- a `url(` whose name is written with escapes, such as `ur\l(` or `\75rl(`;
- an unquoted `url()` whose hex escape ends in a space, such as `url(Foo\28 1\29.png)`.

The local server decides whether a file exists, and a local file system may ignore the case of a file name where a host does not. Check that every reference matches the case of its file name.
