# Building the page

`architecture.html` is the one file people open to read the architecture. It sits in the architecture folder beside the index (`README.md`) and holds a copy of every Markdown file in that folder, each in its own source block. In a browser it formats the prose and tables, draws every `mermaid` fence, and writes one check line per file. The Markdown files stay the source of truth; the page is rebuilt from them whenever they change.

You never write HTML for this page. It starts as a copy of `templates/architecture.html`, and after that only two things change: the source blocks and the built stamp. Everything else in the file is the template's own code, and leaving it untouched is what lets the next template update, a diff and the check lines be trusted. Where a shell is available, the script `scripts/build-page.sh` makes both changes; where it is not, you make them by hand as text edits.

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
- The block order does not matter to the page. The script writes `README.md` first, then the standing views, then the studies, each group sorted by path, so the order is the same on every run.

**The built stamp.** One line in the page header, which the template ships as:

```html
  <p id="stamp">Built <time>not yet</time> from <code>no commit</code></p>
```

A build sets the date (`YYYY-MM-DD`, the day of the build) and the short commit of the repository's `HEAD` (`git rev-parse --short HEAD`), and leaves the rest of the line as it is:

```html
  <p id="stamp">Built <time>2026-11-17</time> from <code>b93de10</code></p>
```

The commit says which committed state the views were built on. Views edited since then and not yet committed are still included; the person commits them together with the page. Where the folder is not in a git repository, the commit is `no-git`; in a repository with no commit yet, `uncommitted`. Committing the page moves `HEAD`, so a rebuild after that commit changes the stamp line even when no view changed.

**Which files.** One block for the index `README.md` and one for every other Markdown file in the architecture folder and its `studies/` folders: each standing view, each study's `README.md`, each view inside a study. The index is a block too: the page opens on it, and its check line fails when it links a file that has no block, which catches a file left out of the build.

The template ships with no source blocks. Opened as it is, it says so and writes `FAIL page: no source blocks; build the page from the Markdown files first`.

## Build or rebuild with the script

Where a shell is available, build and rebuild with the script in this skill, `scripts/build-page.sh`. Run `bash`, then the script's path inside this skill, then the architecture folder:

```bash
bash <this skill's directory>/scripts/build-page.sh context/architecture
```

It does the whole build except reading the checks, and the same command serves the first build and every rebuild:

- When the folder has no `architecture.html`, it copies the template from this skill's `templates/` folder, which it finds from its own path.
- It replaces the whole region between the region lines with one block for every `.md` file under the folder, in the stable order above, with the escape applied. Changed files are replaced, new files added, deleted files dropped. Folders whose names start with a dot are skipped.
- It sets the built stamp.
- It writes only `architecture.html`, through a temporary file moved into place, so a failure leaves the page as it was.
- It prints `placed PATH` for each file and a final line with the count and the stamp, for example `built context/architecture/architecture.html: 7 files, stamp 2026-11-17 from b93de10`.

Unchanged files give byte-identical blocks, so a second run with no change gives a byte-identical page (only the stamp line moves when the date or the commit changed), and `git status` shows `architecture.html` as the only changed file.

It needs bash 3.2 or newer and the standard `awk`, `sed`, `find`, `sort`, `cut` and `date`, in their macOS or Linux versions; `git` is optional and only used for the stamp. Run it with `bash`, because installers do not always keep a script's executable bit.

It stops with exit code 1 and a message on standard error, writing nothing, when:

| Message | What to do |
|---|---|
| `no such folder` | Pass the architecture folder that holds `README.md` |
| `no template at ...` | Run the copy of the script that sits inside this skill, beside its `templates/` folder |
| `... lacks its region lines ... or its stamp line` | The page was edited outside its blocks: copy the template over it and run the script again |
| `no Markdown files under ...` | Write the index and the views first |
| `the page cannot carry this path, rename the file` | Rename the file: a path with `"`, `<`, `>`, `&` or a backslash cannot sit in a marker line |

A missing `README.md` is only a warning: the page builds, but it has no index to open on, so write one.

The script takes every `.md` file under the folder. When it places a file the index does not list, add that file to the index: the index is how people find a view.

When this skill's template is newer than the page (a fix you were told about, or a different Mermaid version on the line `var MERMAID_URL = ...`), move the old page aside or delete it and run the script: with no page in the folder, it starts from the current template.

To confirm a first build, diff it against the template. Every changed line must be a block line or the stamp line:

```bash
diff <this skill's directory>/templates/architecture.html context/architecture/architecture.html
```

`diff` reports the stamp line as changed and the blocks as added after the `<!-- sources: begin -->` line, and nothing else.

## Build or rebuild by hand

Where no shell is available, edit `architecture.html` as text. The result is the same page; only the order of the blocks may differ, which the page does not mind.

**First build.**

1. Copy `templates/architecture.html` from this skill into the architecture folder, beside `README.md`, as `architecture.html`.
2. Add a block for `README.md`, one for every file it links, and one for every view inside each study, as **Add a file** below says.
3. Set the stamp.
4. Read the check lines.

**Rebuild**, after every change to a view, a study or the index:

1. Replace the block of every file that changed.
2. Add a block for every new file.
3. Remove the block of every deleted or renamed file, together with both its marker lines.
4. Set the stamp to today and the current short commit.
5. Read the check lines.

**The edits.**

- **Add a file.** Directly above the line `<!-- sources: end -->`, write the opening marker line with the file's path, then the file's full text, then the closing marker line with the same path. Apply the escape to any `</script` or `<!--` in the text: a forgotten escape lets the rest of the file spill into the page as HTML, and the page then fails that file with `the block does not end on its own closing marker line`.
- **Replace a file.** Find the line `<script type="text/markdown" data-path="PATH">` and the line `</script><!-- end PATH -->`. Replace every line between them with the file's current text, escaped. Keep both marker lines.
- **Remove a file.** Delete both marker lines of its path and every line between them.
- **Stamp.** Replace the date between `<time>` and `</time>` and the commit between `<code>` and `</code>` on the line that starts with `<p id="stamp">`.

Copy each file's text in full, not from memory and not shortened: the page shows exactly what the block holds. Leave everything outside the region lines and the stamp line as it is.

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
- A long or wide table scrolls inside its own box, with its header row kept in view.
- **Theme** switches between light and dark. The page starts in the system setting and follows it until the person switches. Nodes styled in the view with `classDef` or `style` keep their fill; where a label would be hard to read on that fill in the current theme, the page draws it in black or white instead.
- **Compare** shows two sources side by side, each with its own pan and zoom, chosen in the two lists above them.
- A Markdown link to another file in the folder switches to that view inside the page. On GitHub the same link opens the Markdown file.

## Link forms the page understands

These are the links a view or study can use to steer the page. On GitHub they open `architecture.html` as a file, so put them beside the ordinary Markdown links, not instead of them.

- **One view:** `architecture.html#view=containers.md` shows that view.
- **Comparison:** `architecture.html#compare=containers.md,studies/2026-11-10-sync-risks/containers-household-feed.md` shows those two side by side.

The paths after `=` are always relative to the architecture folder. The part before `#` is an ordinary relative path from the file that holds the link to the page: from the index or a standing view it is just `architecture.html`; from a study's `README.md` or a view inside a study it goes two folders up first (two parent-folder steps, then `architecture.html`). The same forms work as the page's own address, so a person can send `architecture.html#compare=...` and the page opens on that comparison. The check line fails when a named path has no block. Opened anyway, a comparison that names only one path shows that view alone with a line saying so, and a named path with no block is named on its side of the comparison.

## With no network

The page loads the Mermaid library from one pinned address, written on the single line `var MERMAID_URL = ...` in the template. It is the only address the page fetches. When the library cannot load (offline, or the address is blocked):

- a message at the top says the diagrams could not be drawn and why;
- every source still shows, with its prose formatted and each diagram as its Mermaid source text;
- every file with a diagram gets `FAIL PATH: diagram N not drawn, the Mermaid library did not load`, and files without diagrams pass, so the `DONE` line shows the page did not draw;
- the Save offline copy button is disabled, because there are no drawn pictures to save.

Do not try to fix this by editing the page. Say that the diagrams were not drawn because the library did not load, and that the views will draw once the page is opened with network.

## The offline copy

**Save offline copy** in the page header downloads a second file, `architecture-offline-YYYY-MM-DD.html`, dated with the local date like the built stamp. It holds every view and study as the page showed it at that moment: the drawn pictures, the formatted prose, and a small script for switching views, compare, pan, zoom, fit and full screen. It contains no Mermaid library, no script loaded from an address and no CDN address, so it opens anywhere with no network, and it keeps the theme it was saved in.

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

**First build.** From the repository root, run `bash <this skill's directory>/scripts/build-page.sh context/architecture`. The folder has no page yet, so the script copies the template, then places seven blocks, in this order:

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

**Rebuild.** Later, `deployment.md` gains a Redis replica, a new view `runtime-expiry.md` is written and linked from the index, and the study's proposed view is deleted after the study is closed with its findings moved into its `README.md`. Run the same script again. It places `runtime-expiry.md` and drops the deleted file. The diff against the previous page shows the `deployment.md` block's changed lines, a new `runtime-expiry.md` block, the `containers-household-feed.md` block gone, and the new stamp. The checks then read `DONE 7/7`, with the index and the study `README.md` still passing because neither links the deleted file any longer. Had the study still linked it, its line would read `FAIL studies/2026-11-10-sync-risks/README.md: link "containers-household-feed.md" points to studies/2026-11-10-sync-risks/containers-household-feed.md, which has no source block`, and the fix would be to remove that link.
