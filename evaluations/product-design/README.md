# Product-design evaluations

Fixtures and rerun commands for the checks that `building-html-prototypes` ships as templates. The acceptance criteria they prove are in `docs/product-engineering/building-html-prototypes-design-trees/spec.md`. Every fixture is invented and links only local files; `example.com` appears only as a reference the checks must report without fetching.

| Fixture | Used by | What it holds |
|---|---|---|
| `fixtures/broken-tree/` | AC5 | The clean tree with four faults: a remote stylesheet, a root-absolute image, a CSS `url()` that climbs out of the tree, and a missing stylesheet on `views/archive/index.html`, a page that only the notes list |
| `fixtures/outside-tree/` | AC5 | `paper.svg`, the file that broken tree's `url()` reaches next to the tree, so only the rule against leaving the tree can catch it |
| `fixtures/edge-tree/` | AC5 | Edge cases the check must report: a folder linked without its trailing slash, a missing file whose name has a malformed percent escape, a page with no `meta charset`, a remote `table` background and a remote SVG `mask` |
| `fixtures/clean-tree/` | AC5, AC7 | An entry page at the root, a view in `views/saved-guides/`, the notes-only page, and `shared/` with tokens, components and images |
| `fixtures/shared-foundations-project/` | AC2 trial | A project whose `design/foundations/` holds `tokens.css` and `components.css`, with a selected direction to refine into one view |
| `fixtures/no-shared-files-project/` | AC3 trial | A project with three direction briefs and no design files |
| `fixtures/panel-bug/` | AC9 | A filter panel whose button click also reaches a document click-outside handler, so the panel opens and closes on one click |
| `fixtures/panel-fixed/` | AC9 | The same panel with the click-outside handler ignoring its button |
| `fixtures/visibility/` | AC9 | Three visibility cases for the harness's `visible()`: an element whose `hidden` attribute the page's CSS overrides, an element inside a hidden one, and plain text |
| `fixtures/long-page/` | AC12 | A page 4,000 CSS px tall, in four bands labeled 0, 1000, 2000 and 3000 |
| `checks/panel-checks.js` | AC9 | The six harness checks for the panel, loaded with `?checks=panel-checks.js` |
| `checks/visibility-checks.js` | AC9 | The three harness checks for `fixtures/visibility/`, loaded with `?checks=visibility-checks.js` |
| `checks/scope-checks.js` | AC9 | One check for `fixtures/panel-fixed/` in a file that declares names the harness uses internally, such as `frame` and `report` |
| `checks/hosted-checks.js` | AC7 | The two harness checks for the hosted render of `fixtures/clean-tree/`: the entry page reaches the view, and the view's shared tokens apply. Loaded with `?checks=hosted-checks.js` |

## Stage and serve

The checks run over HTTP from a staging folder, as `references/interaction-and-verification.md` in the skill describes under "Serve files locally". From the repository root, with `<fixture>` and `<template>` filled in:

```sh
run=$(mktemp -d)
mkdir -p "$run/a/b"
cp -R evaluations/product-design/fixtures/<fixture>/. "$run/a/b/"
cp skills/product-design/building-html-prototypes/templates/<template> "$run/"
python3 -m http.server 8765 --bind 127.0.0.1 --directory "$run" &
```

Read a template's results from a headless DOM dump. On macOS the Chrome binary is `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`:

```sh
chrome --headless --disable-gpu --virtual-time-budget=5000 --dump-dom "<url>" | sed -n '/id="results"/,/<\/pre>/p'
```

Stop the server with `kill %1` and delete `$run` afterwards.

## Design-tree check (AC5)

Stage `broken-tree` with `tree-check.html`, and put `outside-tree/` next to the tree, where the faulty `url()` reaches it: `mkdir -p "$run/a/outside-tree" && cp evaluations/product-design/fixtures/outside-tree/paper.svg "$run/a/outside-tree/"`. Then dump `http://127.0.0.1:8765/tree-check.html?entry=index.html&pages=views/archive/index.html`.

- Pass: exactly four `FAIL` lines, each with its reason:
  - `views/saved-guides/index.html href "https://cdn.example.com/x.css"`: points to a remote host.
  - `views/saved-guides/index.html src "/img/logo.svg"`: root-absolute path.
  - the `url()` in `shared/components.css`: resolves to `/a/outside-tree/paper.svg`, outside the tree.
  - `views/archive/index.html href` to `shared/archive.css`: no file.
- To confirm nothing reaches `example.com`, add `--log-net-log=<file>` to the Chrome command and search the log for the host.
- Repeat with `clean-tree`. Pass: no `FAIL`, and the last line is `DONE 14/14`.
- Repeat with `edge-tree` and no query string. Pass: `FAIL index.html href "views": points to a folder…`, `FAIL index.html src "shared/100%.png": no file at shared/100%.png`, `FAIL views/index.html is a full HTML document…`, `FAIL index.html background "https://cdn.example.com/table.png": points to a remote host`, `FAIL index.html url() "https://cdn.example.com/mask.svg#m": points to a remote host`, and `DONE 3/8`.
- Repeat with `clean-tree` three times, each on a fresh stage with one slow input appended to `"$run/a/b/shared/tokens.css"` with `>>`: an unclosed `url(` and 100,000 spaces, `python3 -c "print('a{b:url(' + ' ' * 100000, end='')"`; 60,000 unclosed comments, `python3 -c "print('/*a' * 60000, end='')"`; and `url(` repeated 40,000 times, `python3 -c "print('url(' * 40000, end='')"`. Pass: each dump returns within a few seconds and ends `DONE 14/14`. A scanner that backtracks on one of these shapes takes far longer on that input.
- Repeat with `clean-tree` after appending four escaped URLs: `printf '%s' 'a{b:url(https://cdn.example.com/Foo_\(bar\).png)} c{d:url("q\"uote.png")} e{f:url("https://cdn.example.com/Hex_\28 bar\29.png")} g{h:url(\68ttps://cdn.example.com/h.png)}' >> "$run/a/b/shared/tokens.css"`. Pass: `FAIL shared/tokens.css url() "https://cdn.example.com/Foo_(bar).png": points to a remote host`, `FAIL shared/tokens.css url() "q"uote.png": no file at shared/q"uote.png`, `FAIL shared/tokens.css url() "https://cdn.example.com/Hex_(bar).png": points to a remote host`, `FAIL shared/tokens.css url() "https://cdn.example.com/h.png": points to a remote host`, and `DONE 14/18`.
- Repeat with `clean-tree` after appending a `/*` inside a string and inside an unquoted `url()`, each followed by a remote URL: `printf '%s' '.s1{content:"/*"} .s2{background:url(https://cdn.example.com/after-string.png)} .s3{background:url(img/*.png)} .s4{background:url(https://cdn.example.com/after-url.png)} /* closing */' >> "$run/a/b/shared/tokens.css"`. Pass: `FAIL shared/tokens.css url() "https://cdn.example.com/after-string.png": points to a remote host`, `FAIL shared/tokens.css url() "img/*.png": no file at shared/img/*.png`, `FAIL shared/tokens.css url() "https://cdn.example.com/after-url.png": points to a remote host`, and `DONE 14/17`. A scan that reads `/*` as a comment there reports none of them.
- Repeat with `clean-tree` after appending an escaped quote outside any string and a string continued across CR LF, each followed by a `/*` in a string and a remote URL: `printf '.a\\"x{color:red} .b{content:"/*"} .c{background:url(https://cdn.example.com/after-escaped-quote.png)} .d{content:"a\\\r\n/*"} .e{background:url(https://cdn.example.com/after-crlf.png)}' >> "$run/a/b/shared/tokens.css"`. Pass: `FAIL shared/tokens.css url() "https://cdn.example.com/after-escaped-quote.png": points to a remote host`, `FAIL shared/tokens.css url() "https://cdn.example.com/after-crlf.png": points to a remote host`, and `DONE 14/16`.

## Hosted render (AC7)

Stage `clean-tree` with both `interaction-harness.html` and `tree-check.html`, and copy its checks to the staging root, `cp evaluations/product-design/checks/hosted-checks.js "$run/"`. Dump `http://127.0.0.1:8765/interaction-harness.html?checks=hosted-checks.js`, then `http://127.0.0.1:8765/tree-check.html?entry=index.html&pages=views/archive/index.html`.

- Pass: `PASS entry reaches view`, `PASS shared tokens applied` and `DONE 2/2`, and the tree check ends `DONE 14/14`.
- Negative control: stage only the view's folder, as a host that publishes only the view would: `cp -R evaluations/product-design/fixtures/clean-tree/views/saved-guides/. "$run/a/b/"` in place of the fixture copy, with the same two templates and checks file. Dump the same harness URL. Pass: `FAIL entry reaches view: the page at a/b/index.html has no link to the view`, `FAIL shared tokens applied: --color-paper is "", so shared/tokens.css did not apply` and `DONE 0/2`. Dump `tree-check.html` with no query string as well. Pass: four `FAIL` lines that say the view's references resolve outside the tree, such as `FAIL index.html href "../../shared/tokens.css": resolves to /shared/tokens.css, outside the tree`, and `DONE 1/5`.
- Wrong prefix: stage the fixture one folder deeper, `mkdir -p "$run/a/b/c"` and `cp -R evaluations/product-design/fixtures/clean-tree/. "$run/a/b/c/"` in place of the fixture copy, with the same two templates and checks file. Dump the same harness URL. Pass: `FAIL entry reaches view: /a/b/index.html returned HTTP 404`, `FAIL shared tokens applied: /a/b/index.html returned HTTP 404` and `DONE 0/2`.

## Interaction harness (AC9)

Stage `panel-bug` with `interaction-harness.html`, copy its checks to the staging root as well, `cp evaluations/product-design/checks/panel-checks.js "$run/"`, then dump `http://127.0.0.1:8765/interaction-harness.html?checks=panel-checks.js`.

- Pass: `FAIL panel stays open after one click`, while `PASS panel opens on click` shows the panel did open inside the click.
- Repeat with `panel-fixed`. Pass: six `PASS` lines, named as in `checks/panel-checks.js`, and `DONE 6/6`.
- Repeat with `visibility`, copying its checks instead, `cp evaluations/product-design/checks/visibility-checks.js "$run/"`, and dumping `interaction-harness.html?checks=visibility-checks.js`. Pass: three `PASS` lines and `DONE 3/3`. A `visible()` that trusts the `hidden` attribute over the page's CSS fails the first check.
- Repeat with `panel-fixed`, copying in both `panel-checks.js` and `scope-checks.js`, and dump `interaction-harness.html?checks=scope-checks.js`. Pass: `PASS a checks file may reuse the harness names` and `DONE 1/1`. A harness whose internal names share the checks file's global scope gives `FAIL checks load: Uncaught SyntaxError: Identifier 'frame' has already been declared` instead.
- On the same stage, put the checks in the harness's checks script instead, `python3 -c 'import sys; h, c = sys.argv[1:]; s = open(h).read(); open(h, "w").write(s.replace("*/\n  </script>\n</body>", "*/\n" + open(c).read() + "  </script>\n</body>"))' "$run/interaction-harness.html" evaluations/product-design/checks/scope-checks.js`, and dump `interaction-harness.html` with no query string. Pass: `PASS a checks file may reuse the harness names` and `DONE 1/1`. Then append `check(` to the same script, `python3 -c 'import sys; h = sys.argv[1]; s = open(h).read(); open(h, "w").write(s.replace("  </script>\n</body>", "check(\n  </script>\n</body>"))' "$run/interaction-harness.html"`, and dump it again. Pass: one `FAIL checks load: Uncaught SyntaxError: …` line and `DONE 0/1`.
- On a fresh `panel-fixed` stage with `panel-checks.js` copied in, dump `?checks=https://cdn.example.com/checks.js`, `?checks=panel-checks.js&page=javascript:void(0)` and `?checks=panel-checks.js&timeout=0`. Pass, in order: `FAIL checks load: https://cdn.example.com/checks.js is not on the staging server` and `DONE 0/1`; six `FAIL` lines that end `javascript:void(0) is not on the staging server` and `DONE 0/6`; `FAIL settings: width, height and timeout must be positive numbers` and `DONE 0/1`.

## Page slices (AC12)

Stage `long-page` with `page-slices.html`. For each offset 0, 1000, 2000 and 3000, dump and screenshot `http://127.0.0.1:8765/page-slices.html?src=a/b/index.html&width=1000&height=1000&offset=<n>`, with `--hide-scrollbars --window-size=1000,1000 --screenshot=<file>` for the screenshot.

- Pass: each dump reads `PASS scrolled <n>` and lists `data-offsets="0 1000 2000 3000"`; each 1000 × 1000 screenshot shows only its own band's label at the top. No full-page image is taken.
- Negative control: offset 3500 reads `FAIL scrolled 3500: stopped at 3000`.
- Invalid input: `height=0` reads `FAIL settings: width and height must be at least 1, and offset at least 0`, and `src=javascript:void(0)` reads `FAIL page loads: javascript:void(0) is not on the staging server`. Each dump returns within a few seconds.

## Agent trials (AC2, AC3)

Each trial gives a fresh agent, with no other context, the path of the candidate skill directory and a copy of the fixture project, then reads what it produced.

- **AC2.** Copy `shared-foundations-project/` to a new folder. Task: "Follow the skill at `<skill path>` to do the task in this project's README. Work only in this folder." Pass: the view page links `design/foundations/tokens.css` and `design/foundations/components.css` by relative path; the page defines none of the custom properties defined in `tokens.css`; the notes list both files for the page; `tree-check.html`, run on the project's `design/` folder staged at `a/b/`, ends `DONE <n>/<n>` with no `FAIL`.
- **AC3.** Copy `no-shared-files-project/` to a new folder, with the same task. Pass: three `.html` files; every `href` and `src` in them is a fragment, a `data:` URI or an outbound link; a DOM dump of each file through `file://` contains its sketch's main heading.

A trial runs once, so it does not show variance across runs or models.
