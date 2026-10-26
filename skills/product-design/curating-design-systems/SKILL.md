---
name: curating-design-systems
description: "Keep a project's design home, the long-lived folder of shared design foundations such as tokens.css and components.css with a folder per platform and per view, to its four layout rules, and check after every change that each page's links, sources and CSS url() references resolve inside it. Use when adding to or reviewing a design home, or when asked where a token, component, platform style or view stylesheet belongs."
license: MIT
---

# Curating design systems

A design home is where a project keeps its designs as the source of truth. It has three kinds of folder:

- **Foundations:** one folder of shared tokens and components, which every platform uses.
- **Platforms:** one folder per platform.
- **Views:** one folder per view, inside its platform.

Pages link the shared files instead of copying them, so a change to a foundation reaches every page that links it. This skill keeps the home's layout coherent and checks it after every change. Shared files change only with the user's agreement.

## Read the home first

Read the project instructions that apply, including `AGENTS.md` or `CLAUDE.md` when present, and the home's README. The README states the layout, its rules, the entry page and every page that no link reaches. Do not require another skill or a particular input format.

Find the home's root: the folder that holds the entry page, the foundations, and the platform and view folders, such as `design/`. Application source and the production theme stay outside it. Never link a page to the application's stylesheets, build or components.

## Keep the four rules

Every change to the home keeps these rules. [Layout rules](references/layout-rules.md) explains what each one allows, gives examples, and says how to fix a breach.

1. **Foundations hold no platform styles.** Tokens and shared components that read correctly on every platform the home serves go in the foundations. A value that is right on only one platform belongs to that platform, such as a menu-bar height or a safe area.
2. **A platform stylesheet draws only what the operating system draws.** It holds the system UI beside the product, such as the menu bar, window chrome or a status bar, plus the platform's geometry tokens. It never holds the product's own controls.
3. **A view's own surfaces are styled once,** in that view's stylesheet. Another view that shows the same surface links that stylesheet instead of copying its rules.
4. **Pages link by relative path only.** Every page is a full HTML document. Each of its links is a relative path to a file inside the home, and every page opens from disk, offline, while the home stays together.

When a requested change would break a rule, name the rule and say where the change belongs instead.

A change to a shared file, such as a foundation or a platform stylesheet, changes every page that links it. Make it only when the user asks or agrees. Before you do, name the pages it reaches.

## Check the tree after every change

Run the [design-tree check](templates/tree-check.html) after every change to the home, before you open any page. The browser treats each `file://` document as its own origin and blocks the reads the check needs, so the check runs over HTTP.

1. **Stage.** Create an empty staging folder outside the project. Copy the home, untouched, to `<staging>/a/b/`. The nested prefix stands in for a host that serves the files under a path. Copy `tree-check.html` to `<staging>/`, outside the home.
2. **Serve.** Serve `<staging>/` from the server root with any static file server bound to the local machine, for example `python3 -m http.server 8000 --bind 127.0.0.1` run in `<staging>/`.
3. **Open.** Open `http://127.0.0.1:<port>/tree-check.html?entry=<entry page>&pages=<every page in the home>`. Page paths are relative to the home's root and separated by commas. Pass every page in the home, not only those the README names, so a page that a change left unlinked is still checked. A page that a link also reaches is checked once. Instead of the query string, the entry page and the page list can be filled in at the top of the copied template.
4. **Read `#results`.**
   - There is one line per reference: `PASS <name>`, or `FAIL <name>: <detail>`.
   - A `FAIL` names the file, the attribute, the reference, and the reason: a remote host, an absolute URL, a root-absolute path, a path outside the home, a folder, or a missing file. The check also fails a page that isn't a full HTML document, a `base` element, a module script and a CSS `@import`.
   - The last line is `DONE <passed>/<total>`. Without it, the check has not finished, and that is not a pass.
   - In a headless browser, read the results from a DOM dump that lets the page's timers and requests finish first, for example Chrome's `--headless --virtual-time-budget=5000 --dump-dom <url>`.
5. **Fix and rerun.** Fix every `FAIL`, then rerun until the check ends `DONE <n>/<n>`. A `FAIL` inside a shared file goes to the user with the file and the reference, and you change the file only once they agree. Report the final `DONE` line with the change. Report every `FAIL` you could not fix, with its reason.
6. **Clean up.** Stop the server and delete the staging folder.

The check reaches only the pages linked from the entry page or listed in `pages`. It reads URL attributes and CSS `url()`, but not scripts. Read each script for requests and imports, and check the other loads by eye, as [Layout rules](references/layout-rules.md#what-the-tree-check-cannot-see) lists. Then open each changed page from its place in the home through `file://`, with the network off.

Without a browser or a local server, give the user these steps and record the check as not performed. Never report it as passed.
