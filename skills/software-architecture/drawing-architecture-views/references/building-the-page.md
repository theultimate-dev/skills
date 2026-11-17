# Building the page

`architecture.html` is the one file people open to read the architecture. It sits in the architecture folder beside the index (`README.md`) and holds a copy of every Markdown file in that folder, each in its own source block. In a browser it formats the prose and tables, draws every `mermaid` fence, and writes one check line per file. The Markdown files stay the source of truth; the page is rebuilt from them whenever they change.

You never write HTML for this page. You copy `templates/architecture.html` once, then change only two things: the source blocks and the built stamp. Everything else in the file is the template's own code, and leaving it untouched is what lets the next template update, a diff and the check lines be trusted.

## What the page holds

**The source blocks.** Between the two region lines `<!-- sources: begin -->` and `<!-- sources: end -->` the page holds one block per Markdown file. A block is the file between two marker lines that carry its path:

```html
<script type="text/markdown" data-path="containers.md">
# Larder: containers
...every line of containers.md, unchanged...
</script><!-- end containers.md -->
```

- The opening marker line is exactly `<script type="text/markdown" data-path="PATH">`, alone on its line.
- The closing marker line is exactly `</script><!-- end PATH -->`, alone on its line, with the same `PATH`.
- `PATH` is the file's path relative to the architecture folder, with forward slashes and its `.md` ending: `README.md`, `containers.md`, `studies/2026-11-10-sync-risks/README.md`. It is the same identifier the views use in links, the compare link form and the check lines.
- Between the marker lines goes the file exactly as it is, with one mechanical escape: wherever the file contains `</script` (in any letter case) or `<!--`, insert a backslash after the `<`, giving `<\/script` and `<\!--`. Where a backslash already follows that `<`, insert one more. The browser would otherwise end the block early or swallow the next one; the page removes the backslash again before it reads the file. Most views contain neither string, so their block is the file verbatim.
- The block order does not matter. The command below writes `README.md` first and the others sorted by path.

**The built stamp.** One line in the page header, which the template ships as:

```html
  <p id="stamp">Built <time>not yet</time> from <code>no commit</code></p>
```

A build sets the date (`YYYY-MM-DD`, the day of the build) and the short commit of the repository's `HEAD` (`git rev-parse --short HEAD`), and leaves the rest of the line as it is:

```html
  <p id="stamp">Built <time>2026-11-17</time> from <code>b93de10</code></p>
```

The commit says which committed state the views were built on. Views edited since then and not yet committed are still included; the person commits them together with the page. Where the folder is not in a git repository, write `no commit`.

**Which files.** One block for the index `README.md` and one for every other Markdown file in the architecture folder and its `studies/` folders: each standing view, each study's `README.md`, each view inside a study. The index is a block too: the page opens on it, and its check line fails when it links a file that has no block, which catches a file left out of the build.

The template ships with no source blocks. Opened as it is, it says so and writes `FAIL page: no source blocks; build the page from the Markdown files first`.

## First build

1. Copy `templates/architecture.html` from this skill into the architecture folder, beside `README.md`, as `architecture.html`.
2. Insert one block for `README.md` and one for every file it lists, and for every view inside each study, between the region lines.
3. Set the built stamp.
4. Read the check lines (below).

Where a shell is available, steps 2 and 3 are the command in the next section. Where it is not, do them by hand as the section after it says.

## Rebuild

Rebuild after every change to a view, a study or the index, before you report: a page that does not match its Markdown is worse than no page, because people trust what they see drawn.

1. Replace the block of every file that changed.
2. Add a block for every new file.
3. Remove the block of every deleted or renamed file, together with both its marker lines.
4. Set the built stamp to today and the current short commit.
5. Read the check lines.

Leave everything outside the region lines and the stamp line as it is. When this skill's template is newer than the page (a fix you were told about, or a different Mermaid version on the line `var MERMAID_URL = ...`), start again from a fresh copy of the template and run the first build instead.

## Assemble with one command

Where a shell is available, one command does steps 2 and 3 of the first build and every step of a rebuild except reading the checks: it regenerates the whole region from the Markdown files on disk, applies the escape, and sets the stamp. Unchanged files produce byte-identical blocks, so a diff shows only what changed. It uses only `sh`, `awk`, `sed`, `find`, `sort` and `git`, and works with both the BSD and the GNU versions of those tools. Run it with the architecture folder in place of `ARCH_DIR`:

```sh
cd ARCH_DIR || exit 1
date=$(date +%Y-%m-%d)
commit=$(git rev-parse --short HEAD 2>/dev/null || echo 'no commit')
{
  awk -v date="$date" -v commit="$commit" '
    /<p id="stamp">/ { sub(/<p id="stamp">.*<\/p>/, "<p id=\"stamp\">Built <time>" date "</time> from <code>" commit "</code></p>") }
    { print }
    /^<!-- sources: begin -->$/ { exit }' architecture.html
  { echo README.md; find . -name '*.md' ! -path './README.md' | sed 's|^\./||' | LC_ALL=C sort; } |
  while IFS= read -r f; do
    printf '<script type="text/markdown" data-path="%s">\n' "$f"
    awk 1 "$f" | sed -E 's#<(\\*)(/[Ss][Cc][Rr][Ii][Pp][Tt]|!--)#<\\\1\2#g'
    printf '</script><!-- end %s -->\n' "$f"
  done
  awk '/^<!-- sources: end -->$/ { on = 1 } on' architecture.html
} > architecture.html.new && mv architecture.html.new architecture.html
```

What each part does, so you can adapt it when a shell lacks one tool: the first `awk` copies the page up to and including `<!-- sources: begin -->` and rewrites the stamp line on the way; the loop writes one block per Markdown file (`awk 1` adds a final newline where a file lacks one, so the closing marker always starts its own line; `sed` applies the escape); the last `awk` copies the page from `<!-- sources: end -->` to the end. The result goes to a temporary file first, so a failure leaves the page as it was.

The command takes every `.md` file under the folder. When it adds a file the index does not list, add that file to the index: the index is how people find a view.

Then confirm the build with a diff against the template. Every changed line must be a block line or the stamp line:

```sh
diff TEMPLATE ARCH_DIR/architecture.html
```

with this skill's `templates/architecture.html` in place of `TEMPLATE`. On a first build, `diff` reports the stamp line as changed and the blocks as added after the `<!-- sources: begin -->` line, and nothing else.

## Build by hand

Where no shell is available, edit `architecture.html` as text, one file at a time.

- **Add a file.** Directly above the line `<!-- sources: end -->`, write the opening marker line with the file's path, then the file's full text, then the closing marker line with the same path. Apply the escape to any `</script` or `<!--` in the text.
- **Replace a file.** Find the line `<script type="text/markdown" data-path="PATH">` and the line `</script><!-- end PATH -->`. Replace every line between them with the file's current text, escaped. Keep both marker lines.
- **Remove a file.** Delete both marker lines of its path and every line between them.
- **Stamp.** Replace the date between `<time>` and `</time>` and the commit between `<code>` and `</code>` on the line that starts with `<p id="stamp">`.

Copy each file's text in full, not from memory and not shortened: the page shows exactly what the block holds.

## Reading the check lines

The page writes its checks as text into the element with id `results`, shown under **Checks** at the bottom of the left column. One line per source block, in block order, then a total:

```text
PASS README.md
PASS containers.md
FAIL deployment.md: diagram 1 could not be drawn: Parse error on line 3: ... Expecting 'SEMI', 'NEWLINE', ... got 'EOF'
DONE 6/7
```

- `PASS PATH`: every `mermaid` fence in the file drew, and every link from it to another Markdown file in the folder, and every compare or view link, reaches a file that has a block.
- `FAIL PATH: detail`: what went wrong, joined with `; ` when several things did. A diagram that does not parse fails its own file only; every other file still draws.
- `DONE passed/total`: `total` is the number of source blocks. The page is good when `passed` equals `total`.

What each kind of FAIL asks of you:

| Detail starts with | Fix |
|---|---|
| `diagram N could not be drawn` | Correct the Mermaid in that file's Nth `mermaid` fence at the line the parser names, then rebuild |
| `link "..." points to X, which has no source block` | Either the target file is missing (fix the link) or its block is (rebuild) |
| `compare link ... must name two sources` | Write the compare link with exactly two paths separated by a comma |
| `the block does not end on its own closing marker line` | The escape was not applied to that file; rebuild it with the escape |
| `the file is empty` | Write the file, or remove it and its block |
| `diagram N not drawn, the Mermaid library did not load` | No network; see below. Not a fault in the views |

**Where the harness can open a browser**, open the page as a `file://` URL, wait until the `results` element contains a line that starts with `DONE` (drawing takes a second or two), and read its text. Report the `DONE` line in your answer, and every `FAIL` line with what you did about it. Also look at the drawn page once: a diagram can parse and still read badly.

Where the harness can run a headless Chrome or Chromium but not drive it, this prints the page after drawing; read the `results` lines from its output:

```sh
chrome --headless --virtual-time-budget=15000 --dump-dom "file://$PWD/architecture.html" |
  sed -n '/<pre id="results">/,/<\/pre>/p' | sed -e 's/.*<pre id="results">//' -e 's/<\/pre>.*//'
```

Run it from the architecture folder. The browser's program name differs by system (`google-chrome`, `chromium`, or the full path to the application, such as `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` on macOS).

**Where the harness cannot open a browser**, say in your report that the views were not drawn and the checks were not read, and ask the person to open `architecture.html` and tell you the `DONE` line and any `FAIL` lines under Checks.

## What the reader can do

Knowing this lets you point a person at the right thing:

- The left column lists the index as **Overview**, then **Standing views** in the order the index links them, then **Studies**, newest first, each with its own views beneath it. Each entry shows its status.
- Every `mermaid` fence is drawn in a frame. Drag pans; Ctrl or Cmd with the mouse wheel, or a trackpad pinch, zooms; the buttons zoom in, zoom out, fit, and show the diagram full screen, where the plain wheel zooms too.
- **Theme** switches between light and dark. The page starts in the system setting and follows it until the person switches. Nodes styled in the view with `classDef` or `style` keep their fill; where a label would be hard to read on that fill in the current theme, the page draws it in black or white instead.
- **Compare** shows two sources side by side, each with its own pan and zoom, chosen in the two lists above them.
- A Markdown link to another file in the folder switches to that view inside the page. On GitHub the same link opens the Markdown file.

## Link forms the page understands

These are the links a view or study can use to steer the page. On GitHub they open `architecture.html` as a file, so put them beside the ordinary Markdown links, not instead of them.

- **One view:** `architecture.html#view=containers.md` shows that view.
- **Comparison:** `architecture.html#compare=containers.md,studies/2026-11-10-sync-risks/containers-household-feed.md` shows those two side by side.

The paths after `=` are always relative to the architecture folder. The part before `#` is an ordinary relative path from the file that holds the link to the page: from the index or a standing view it is just `architecture.html`; from a study's `README.md` or a view inside a study it goes two folders up first (two parent-folder steps, then `architecture.html`). The same forms work as the page's own address, so a person can send `architecture.html#compare=...` and the page opens on that comparison. The check line fails when a named path has no block.

## With no network

The page loads the Mermaid library from one pinned address, written on the single line `var MERMAID_URL = ...` in the template. It is the only address the page fetches. When the library cannot load (offline, or the address is blocked):

- a message at the top says the diagrams could not be drawn and why;
- every source still shows, with its prose formatted and each diagram as its Mermaid source text;
- every file with a diagram gets `FAIL PATH: diagram N not drawn, the Mermaid library did not load`, and files without diagrams pass, so the `DONE` line shows the page did not draw;
- the Save offline copy button is disabled, because there are no drawn pictures to save.

Do not try to fix this by editing the page. Say that the diagrams were not drawn because the library did not load, and that the views will draw once the page is opened with network.

## The offline copy

**Save offline copy** in the page header downloads a second file, `architecture-offline-YYYY-MM-DD.html`. It holds every view and study as the page showed it at that moment: the drawn pictures, the formatted prose, and a small script for switching views, compare, pan, zoom, fit and full screen. It contains no Mermaid library, no script loaded from an address and no CDN address, so it opens anywhere with no network, and it keeps the theme it was saved in.

- A person makes it in a browser, because drawing needs one. You cannot make it from the Markdown without a browser.
- It is what gets sent to someone outside: a client, a reviewer without access to the repository. One file, nothing to install.
- It is not committed. It is a snapshot that goes stale with the next change; the committed page and the Markdown are the record. Make a new copy when someone needs one.
- Its links to files outside the architecture folder (a decision record, say) do not work for a recipient who lacks the folder; links between views do.

## Worked example: Larder

Larder's architecture folder is `context/architecture/`:

```text
context/architecture/
├── README.md
├── context.md
├── containers.md
├── deployment.md
├── runtime-sync.md
└── studies/
    └── 2026-11-10-sync-risks/
        ├── README.md
        └── containers-household-feed.md
```

**First build.** Copy this skill's `templates/architecture.html` to `context/architecture/architecture.html`. Run the assembly command with `context/architecture` in place of `ARCH_DIR`, from the repository root. The page now holds seven blocks, in this order:

```text
README.md
containers.md
context.md
deployment.md
runtime-sync.md
studies/2026-11-10-sync-risks/README.md
studies/2026-11-10-sync-risks/containers-household-feed.md
```

and its stamp line reads `<p id="stamp">Built <time>2026-11-17</time> from <code>b93de10</code></p>`. Opened in a browser, the checks read:

```text
PASS README.md
PASS containers.md
PASS context.md
PASS deployment.md
PASS runtime-sync.md
PASS studies/2026-11-10-sync-risks/README.md
PASS studies/2026-11-10-sync-risks/containers-household-feed.md
DONE 7/7
```

The left column shows Overview; Standing views in the index's order (Context, Containers, Runtime, offline sync, Deployment); and under Studies, "Risk review: offline sync" dated 2026-11-10 with "Containers, household feed (proposed)" beneath it. The study can link the comparison of the standing containers view with its proposal by a link two folders up to `architecture.html#compare=containers.md,studies/2026-11-10-sync-risks/containers-household-feed.md`.

**Rebuild.** Later, `deployment.md` gains a Redis replica, a new view `runtime-expiry.md` is written and linked from the index, and the study's proposed view is deleted after the study is closed with its findings moved into its `README.md`. Run the same command again. The diff against the previous page shows the `deployment.md` block's changed lines, a new `runtime-expiry.md` block, the `containers-household-feed.md` block gone, and the new stamp. The checks then read `DONE 7/7`, with the index and the study `README.md` still passing because neither links the deleted file any longer. Had the study still linked it, its line would read `FAIL studies/2026-11-10-sync-risks/README.md: link "containers-household-feed.md" points to studies/2026-11-10-sync-risks/containers-household-feed.md, which has no source block`, and the fix would be to remove that link.
