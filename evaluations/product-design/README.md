# Product-design evaluations

Fixtures and rerun commands for the checks that `building-html-prototypes` ships as templates. The acceptance criteria they prove are in `docs/product-engineering/building-html-prototypes-design-trees/spec.md`. Every fixture is invented and links only local files; `example.com` appears only as a reference the checks must report without fetching.

| Fixture | Used by | What it holds |
|---|---|---|
| `fixtures/broken-tree/` | AC5 | The clean tree with four faults: a remote stylesheet, a root-absolute image, a CSS `url()` that climbs out of the tree, and a missing stylesheet on `views/archive/index.html`, a page that only the notes list |
| `fixtures/outside-tree/` | AC5 | `paper.svg`, the file that broken tree's `url()` reaches next to the tree, so only the rule against leaving the tree can catch it |
| `fixtures/edge-tree/` | AC5 | Edge cases the check must report: a folder linked without its trailing slash, a missing file whose name has a malformed percent escape, and a page with no `meta charset` |
| `fixtures/clean-tree/` | AC5 | An entry page at the root, a view in `views/saved-guides/`, the notes-only page, and `shared/` with tokens, components and images |
| `fixtures/shared-foundations-project/` | AC2 trial | A project whose `design/foundations/` holds `tokens.css` and `components.css`, with a selected direction to refine into one view |
| `fixtures/no-shared-files-project/` | AC3 trial | A project with three direction briefs and no design files |

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
- Repeat with `edge-tree` and no query string. Pass: `FAIL index.html href "views": points to a folder…`, `FAIL index.html src "shared/100%.png": no file at shared/100%.png`, `FAIL views/index.html is a full HTML document…`, and `DONE 3/6`.
- Repeat with `clean-tree` three times, each on a fresh stage with one slow input appended to `"$run/a/b/shared/tokens.css"` with `>>`: an unclosed `url(` and 100,000 spaces, `python3 -c "print('a{b:url(' + ' ' * 100000, end='')"`; 60,000 unclosed comments, `python3 -c "print('/*a' * 60000, end='')"`; and `url(` repeated 40,000 times, `python3 -c "print('url(' * 40000, end='')"`. Pass: each dump returns within a few seconds and ends `DONE 14/14`. A scanner that backtracks on one of these shapes takes far longer on that input.

## Agent trials (AC2, AC3)

Each trial gives a fresh agent, with no other context, the path of the candidate skill directory and a copy of the fixture project, then reads what it produced.

- **AC2.** Copy `shared-foundations-project/` to a new folder. Task: "Follow the skill at `<skill path>` to do the task in this project's README. Work only in this folder." Pass: the view page links `design/foundations/tokens.css` and `design/foundations/components.css` by relative path; the page defines none of the custom properties defined in `tokens.css`; the notes list both files for the page; `tree-check.html`, run on the project's `design/` folder staged at `a/b/`, ends `DONE <n>/<n>` with no `FAIL`.
- **AC3.** Copy `no-shared-files-project/` to a new folder, with the same task. Pass: three `.html` files; every `href` and `src` in them is a fragment, a `data:` URI or an outbound link; a DOM dump of each file through `file://` contains its sketch's main heading.

A trial runs once, so it does not show variance across runs or models.
