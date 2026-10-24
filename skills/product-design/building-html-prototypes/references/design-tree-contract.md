# Design-tree contract

## When it applies

Use a design tree when the project already keeps shared design files, such as `tokens.css`, `components.css`, a platform stylesheet or shared images, or when the user asks for them. The pages link those files instead of copying their rules, so a change to a shared file reaches every page and the pages do not drift apart.

The tree's root is the folder that holds the entry page, every page and the shared design files they link, such as `design/` in a project that keeps `design/foundations/` and `design/views/`. Application source and the production theme stay outside it. Name the root in the notes, and stage that folder and nothing wider, so the tree check can tell when a page reaches outside it.

Otherwise use the [one-file artifact](offline-artifact-contract.md). Direction sketches use it by default, even in a project that keeps shared design files: a sketch may keep its candidate tokens inline until the user chooses a direction. State the contract in the notes, and state a change of contract when the user asks for one.

## Page rules

Every page in the tree follows these rules:

- **A full HTML document.** Each page has its own doctype, `html`, `head` with `meta charset` and `title`, and `body`, and opens on its own in a browser.
- **Relative paths only.** Every `href`, `src`, `srcset` and CSS `url()` that names a file is a relative path to a file inside the tree. A path may climb to a parent folder as long as it stays inside the tree; a view in `views/saved-guides/` reaches `shared/tokens.css` by climbing two folders. Never climb above the tree's root. Name the file, not its folder, because a folder does not open its index page from disk. Do not add a `base` element, which changes how every relative path resolves.
- **No root-absolute paths.** A path that starts with `/`, such as `/shared/tokens.css`, resolves against the host or the disk, not the tree.
- **No network.** Do not load remote fonts, CDN styles or scripts, images or iframes. Keep research links in the notes, because the tree check fails remote links too.
- **No build step.** The files in the tree are the files a browser opens: no preprocessor, bundler, compiled template or generated CSS.
- **No JavaScript modules and no CSS `@import`.** Link each stylesheet from every page that uses it, so a page's dependency list is complete. Classic scripts linked by `<script src>` are allowed; module scripts and `import` do not load from disk.
- **No `fetch`** or other requests: no `XMLHttpRequest`, remote forms, service workers or external APIs for the demonstrated behavior.
- **Opens from disk, offline, while the tree stays together.** Every page renders and completes its demonstrated task through `file://` with the network off, as long as the tree is copied or moved as a whole. A page moved out of its tree is expected to break.

A browser treats each `file://` document as an opaque origin, so requests and module scripts that work over a server fail from disk ([MDN, Same-origin policy: File origins](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy#file_origins)). Plain links, stylesheets, classic scripts and images do load.

The [one-file contract](offline-artifact-contract.md)'s guidance on fonts, imagery, sample content and the behavior boundary applies to the tree as a whole. A font or image file that several pages use can be a shared file in the tree.

## Shared files

Link the project's shared files as they are. Put rules that only one page needs in that page's `style` element or in a file next to it. Changing a shared file changes every page that links it: record the change in the notes, and make it only when the user asks.

The prototype notes (`templates/prototype-notes.md`) name the contract, the tree's root folder, the entry page and every page in the tree, including pages that no link reaches yet. For each page they list the shared files it links. An implementer reads the list to map each page back to its foundations, and the tree check reads the page list to reach every page.

## Publish through an entry page

Some hosts publish one page and the files beside it, such as an artifact viewer or a preview that opens a single URL. Publish the tree from its root, so the view's relative paths still reach the shared files:

- **An entry page at the tree's root.** A small page that follows the page rules and links to the view, or to each view when the tree has several. It may also forward to the view with a `meta` refresh, such as `<meta http-equiv="refresh" content="0; url=views/saved-guides/index.html">`; keep the link as well, for a host or browser that ignores the refresh. Publish the entry page as the host's one page.
- **The shared files at their tree-relative paths.** Publish the entry page, every page in the notes and every file they reach, each at its path relative to the tree's root: the shared files the pages link, and the images and fonts those files load in turn. A view that climbs to a parent folder for `shared/tokens.css` then still finds it there. Leave out the tree's other files, such as the prototype notes or direction briefs, unless the user wants them shared. A host that publishes only the view's folder leaves the shared files above its root, where no relative path reaches them, and the view renders without its shared styles.

Name the entry page in the notes. Before reviewers open the tree through a host, check that set of files served under a nested prefix, as the [hosted render step](interaction-and-verification.md#verification-sequence) describes; the design-tree check on that stage fails on any file the pages reach but the set leaves out. Before you publish the tree to a host yourself, confirm the checked set with the user, and who can open it there.

## Check the tree

Run the design-tree check, `templates/tree-check.html`, after every change to the tree, before opening any page:

1. Stage the tree as [Serve files locally](interaction-and-verification.md#serve-files-locally) describes, with `tree-check.html` at the staging root.
2. Open `tree-check.html?entry=<entry page>&pages=<pages no link reaches>` over HTTP, with page paths relative to the tree and separated by commas. Instead of the query string, the entry page and page list can be filled in at the top of a copy of the template.
3. Read `#results`. The check starts from the entry page and the listed pages, follows links to other pages in the tree, and reads each linked stylesheet. It reports each reference as `PASS` or `FAIL`. A `FAIL` names the file, the attribute and the reference, and says why: a remote host, an absolute URL, a root-absolute path, a path outside the tree, a folder, or a missing file. It also fails a page that is not a full HTML document, a `base` element, a module script and a CSS `@import`.
4. Fix every `FAIL` and rerun the check until it ends with `DONE <n>/<n>`. A `FAIL` inside a shared file goes to the user with the file and the reference: change the file only when they agree, as [Shared files](#shared-files) says, and until then record the check as failing, with the reason. Record the result in the notes' verification table.

The check only reaches pages linked from the entry page or listed in the notes. It reads URL attributes such as `href`, `src`, `srcset` and `background`, CSS `url()` and `@import`, `url()` in SVG attributes such as `mask`, and `meta` refresh, not scripts. Read each script for requests and imports, and read by eye any other way a page loads a file, such as an `image-set()` string, an `iframe` `srcdoc`, a `ping` attribute, a `url(` whose name is written with escapes, such as `ur\l(` or `\75rl(`, or an unquoted `url()` whose hex escape ends in a space, such as `url(Foo\28 1\29.png)`. The local server decides whether a file exists, and a local file system may ignore the case of a file name where a host does not: check that every reference matches its file name's case. Then open each page from its place in the tree through `file://`, with the network off, as the verification sequence describes.
