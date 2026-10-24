# Product-design evaluations

Fixtures and rerun commands for the checks that `building-html-prototypes` ships as templates, and for the agent trials of the native-surface variant across the product-design skills. The acceptance criteria they prove are in `docs/product-engineering/building-html-prototypes-design-trees/spec.md` and, for the `harbor-` fixtures, in `docs/product-engineering/exploring-visual-directions-native-surfaces/spec.md`. Every fixture is invented and links only local files; `example.com` appears only as a reference the checks must report without fetching.

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
| `fixtures/native-scene/` | AC16 | A desktop window drawn at 1 CSS px = 1 pt as an 800 × 500 scene: `index.html` scrolls it inside its own container, and `widens.html`, the control, lets it widen the page |
| `fixtures/harbor-menu-bar/` | #10 AC3–AC8, AC13 | Harbor, a fictional backup watcher, as a macOS menu-bar panel and settings window. It names no placements |
| `fixtures/harbor-android-widget/` | #10 AC6 | Harbor as an Android home-screen widget (4 × 2 cells) and its configuration screen |
| `fixtures/harbor-web-dashboard/` | #10 AC9 | Harbor as a web dashboard opened in a browser on phones and desktops, with a `package.json` |
| `fixtures/harbor-status-unclear/` | #10 AC2 | Harbor's "backup status at a glance" view with no platform and no code |
| `fixtures/harbor-status-app/` | #10 AC2 | The same brief with a `Package.swift` for macOS 14 and a `MenuBarExtra` app in `Sources/`, never built |
| `fixtures/harbor-mixed/` | #10 AC1 | Harbor's macOS menu-bar panel and its web account page |
| `checks/panel-checks.js` | AC9 | The six harness checks for the panel, loaded with `?checks=panel-checks.js` |
| `checks/visibility-checks.js` | AC9 | The three harness checks for `fixtures/visibility/`, loaded with `?checks=visibility-checks.js` |
| `checks/scope-checks.js` | AC9 | One check for `fixtures/panel-fixed/` in a file that declares names the harness uses internally, such as `frame` and `report` |
| `checks/hosted-checks.js` | AC7 | The two harness checks for the hosted render of `fixtures/clean-tree/`: the entry page reaches the view, and the view's shared tokens apply. Loaded with `?checks=hosted-checks.js` |
| `checks/native-scene-checks.js` | AC16 | The two harness checks for `fixtures/native-scene/` in a 320 CSS px frame: the page has no horizontal scroll, and the scene keeps its scale and scrolls in its container. Loaded with `?checks=native-scene-checks.js&width=320` |

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
- Publish set: after the fixture copy, remove the files a host would not get if the set held only the shared files the pages link, `rm "$run/a/b/notes.md" "$run/a/b/shared/texture.svg"`. Dump both URLs. Pass: the harness still ends `DONE 2/2`, and the tree check reports `FAIL shared/components.css url() "texture.svg": no file at shared/texture.svg` and ends `DONE 13/14`, because `components.css` loads `texture.svg` itself.

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

## Native scene at 320 px (AC16)

Stage `native-scene` with `interaction-harness.html`, copy its checks to the staging root as well, `cp evaluations/product-design/checks/native-scene-checks.js "$run/"`, then dump `http://127.0.0.1:8765/interaction-harness.html?checks=native-scene-checks.js&width=320`.

- Pass: `PASS no page scroll at 320`, `PASS scene scrolls in its container` and `DONE 2/2`.
- Negative control: on the same stage, dump `interaction-harness.html?checks=native-scene-checks.js&width=320&page=a/b/widens.html`, the same scene in a container that does not scroll. Pass: `FAIL no page scroll at 320: the page is 816 px wide, so it scrolls sideways at 320`, `FAIL scene scrolls in its container: the container's overflow-x is visible, so the scene does not scroll inside it` and `DONE 0/2`.
- Dump `interaction-harness.html?checks=native-scene-checks.js` without the width. Pass: `FAIL no page scroll at 320: the frame is 1024 px wide; open the harness with width=320`, `FAIL scene scrolls in its container: the scene fits its 960 px container, so nothing scrolls in it` and `DONE 0/2`.
- On a fresh stage, shrink the scene to fit, `python3 -c 'import sys; p = sys.argv[1]; s = open(p).read(); open(p, "w").write(s.replace("  </style>", "    .scene { transform: scale(0.35); transform-origin: 0 0; }\n  </style>"))' "$run/a/b/index.html"`, and dump the URL with `&width=320` again. Pass: `PASS no page scroll at 320`, `FAIL scene scrolls in its container: the scene is drawn 280 px wide, not at its 800 px scale` and `DONE 1/2`.

## Agent trials (AC2, AC3)

Each trial gives a fresh agent, with no other context, the path of the candidate skill directory and a copy of the fixture project, then reads what it produced.

- **AC2.** Copy `shared-foundations-project/` to a new folder. Task: "Follow the skill at `<skill path>` to do the task in this project's README. Work only in this folder." Pass: the view page links `design/foundations/tokens.css` and `design/foundations/components.css` by relative path; the page defines none of the custom properties defined in `tokens.css`; the notes list both files for the page; `tree-check.html`, run on the project's `design/` folder staged at `a/b/`, ends `DONE <n>/<n>` with no `FAIL`.
- **AC3.** Copy `no-shared-files-project/` to a new folder, with the same task. Pass: three `.html` files; every `href` and `src` in them is a fragment, a `data:` URI or an outbound link; a DOM dump of each file through `file://` contains its sketch's main heading.

A trial runs once, so it does not show variance across runs or models.

## Agent trials: native surfaces (#10)

These trials check the native-surface variant of `exploring-visual-directions`, and its hand-over to `building-html-prototypes`, on the `harbor-` fixtures. Each trial runs one skill on one fixture, in a run folder of its own outside any checkout:

```sh
run=$(mktemp -d)
mkdir -p "$run/skill" "$run/project"
git archive <sha> skills/product-design/<skill> | tar -x -C "$run/skill" --strip-components=3
cp -R evaluations/product-design/fixtures/<fixture>/. "$run/project/"
```

- **Executor.** A fresh agent gets only the run folder's absolute path and the task below. It may use absolute paths under the run folder only, runs every shell command as `cd "<run>" && …`, and uses only the file and shell tools that `scan_transcript.py` allows: no skill, agent, web tool or connector.
- **Baseline.** The same trial on the skill at `f401cae`, before the native-surface variant.
- **Transcript scan.** After each run, `python3 -I evaluations/product-design/scan_transcript.py <transcript.jsonl> "$run"` lists every tool call that may reach outside the run folder, and every call to a tool other than the file and shell tools, such as a skill, an agent, a web tool or a connector. `CLEAN` keeps the run. Read each line it prints: a call to any other tool, or a real read or write outside the run, voids the run, while a path that is only text the run writes, such as a Markdown link in a string, doesn't. The scan reads tool calls, not the scripts a run writes and then runs, so read any such script yourself. An agent host that loads installed skills would otherwise serve the released text instead of the candidate.
- **Grading.** A fresh grader sees one fixture's candidate and baseline outputs under random IDs, and the rubric below. It answers yes or no for each criterion, quotes each yes with its `file:line`, and tries to refute it. Every quote is then found with `grep -F` in its file, and a quote that isn't found voids the grade.
- **Calibration.** Before grading, a grader marks five mutated copies of one T1 output, and must fail each on its criterion:
  - an inserted "Narrow-screen changes" line (N2);
  - a second platform frame (N3);
  - a dropped full-screen placement (N1);
  - Roboto marked "can't be embedded", on T-droid's rubric (D1);
  - a departure without its reason (N4).

The task for every trial on `exploring-visual-directions` is:

> Follow the skill at `<run>/skill/SKILL.md` to propose three visual directions for the product in `<run>/project/README.md`, and the rendering task for their sketches. Write Markdown in `<run>/project/`. Work only inside `<run>`. No network access and no user: if the skill tells you to ask the user, write the question, its options and your recommendation to `<run>/project/QUESTIONS.md`, and stop.

T2 stages `building-html-prototypes` as `skill/` and T1 run 1's `project/` as its project:

> Follow the skill at `<run>/skill/SKILL.md` to render direction A from the direction briefs in `<run>/project/`, as their rendering task asks, as one sketch with its prototype notes. Write the files in `<run>/project/`. Work only inside `<run>`. No network access and no user: if the skill tells you to ask the user, write the question, its options and your recommendation to `<run>/project/QUESTIONS.md`, and stop.

With no network, T1's frame leaves the device geometry to supply, so T2 stops and asks for it, which H1 grades. The trial then puts the user's answer in `<run>/project/ANSWERS.md` and resumes the same executor to render. The answer names a MacBook Pro 14-inch with a camera cut-out, an external 27-inch display and macOS 15. It gives the user's own numbers for the tokens asked for, each with the source "user's answer, <date>":
- the built-in display, 1512 × 982 pt, with a 37 pt menu bar and a cut-out of 200 × 32 pt centred in it;
- the external display, 2560 × 1440 pt, with a 24 pt menu bar;
- a status item 28 pt wide.

| Trial | Fixture | Runs | Rubric |
|---|---|---|---|
| T1 | `harbor-menu-bar` | 3 | N1–N7 |
| T-droid | `harbor-android-widget` | 1 | D1 |
| T-web | `harbor-web-dashboard` | 3 | W1–W2 |
| T-amb | `harbor-status-unclear` | 3 | A1 |
| T-code | `harbor-status-app` | 1 | C1 |
| T-mix | `harbor-mixed` | 1 | M1 |
| T2 | T1 run 1's output | 1 | H1–H4 |

Rubric, each criterion yes or no:

- **N1.** Each of the three directions lists placements at real scale, among them a display with a hardware cut-out, an external display without one, and a full-screen app.
- **N2.** No direction has a narrow-screen or responsive-changes entry. Mechanical part: `grep -inE "narrow-screen|responsive change|breakpoint"` on the direction files prints nothing.
- **N3.** There is exactly one platform frame, in the rendering task, with:
  - a scale mapping;
  - a geometry table in which every token has a source or is marked for the user to supply;
  - the system UI the panel competes with, naming the menu bar and status items;
  - the four settings: appearance, contrast, transparency and motion.
  No direction restates other frame values.
- **N4.** Each direction names the platform materials, standard controls and design guidelines it uses. It also names at least one deliberate departure with its reason, or states that it has none.
- **N5.** The briefs name the macOS system font as the intended face and render it through `system-ui`. They record that the font isn't embedded and that other platforms show their own system font. System symbols are drawn stand-ins, recorded as a limit.
- **N6.** Each direction's risks include reading at hardware size, competing with system UI for space, and at least one state that must not depend on colour or motion alone.
- **N7.** The filled comparison contains "Placements and scale" and no "Narrow-screen changes", checked with `grep -c`.
- **D1.** The briefs record Roboto as openly licensed, naming the licence, and follow embed-or-fall-back. No line says Roboto or Material Symbols can't be embedded: `grep -inE "can.?t be embedded|cannot be embedded|never embedded|not embeddable"` finds no such line.
- **W1.** Every direction has narrow-screen changes.
- **W2.** `grep -inE "platform frame|placements|platform fit"` on the outputs prints nothing.
- **A1.** `project/` holds only `README.md` and `QUESTIONS.md`. `QUESTIONS.md` asks which surface the view is for, offering a responsive page and a native surface, or two platforms.
- **C1.** The directions are for a macOS menu-bar panel, and no `QUESTIONS.md` asks which surface the view is for.
- **M1.** The panel's directions have placements and a platform frame, and the web page's directions have narrow-screen changes. There is no `QUESTIONS.md`.
- **H1.** No `QUESTIONS.md` entry asks for a value the frame supplied.
- **H2.** The notes' "Native surface" section carries the frame's scale mapping, every geometry token with the frame's source word for word (or the user's answer, for a token the frame left to supply), the type and symbol limits, and the four settings.
- **H3.** The scene's CSS defines each of the frame's geometry tokens as a custom property, and the settings control sits outside every scene.
- **H4.** Staged at `a/b/` with `interaction-harness.html` and a checks file generated from the frame's tokens, the harness reports `DONE n/n`: every token resolves to a non-empty computed value, and the page has no horizontal scroll at 320. With one token deleted from the scene's CSS, it reports `FAIL` naming that token.

A row passes only when every run passes. A row whose baseline also passes is reported as a regression guard, not as proof of the change. The trials stand in for real briefs and codebases. `QUESTIONS.md` stands in for the user, so, apart from T2's simulated answer in `ANSWERS.md`, they don't show how an agent goes on after an answer.
