---
name: drawing-architecture-views
description: "Draws a system's architecture as Markdown views with Mermaid diagrams and builds the one page people read them in: writes a view file such as containers.md or runtime-sync.md in the architecture folder (context/architecture/ by default), updates its README.md index, writes a short guide study for a named audience, and builds or rebuilds architecture.html with scripts/build-page.sh, which copies templates/architecture.html and places each Markdown file in a source block, then reads the page's PASS and FAIL check lines. Starts every view from one sentence naming its audience, question, scope and state, and draws the highest level that shows the fact in question. Use when the user says draw this, draw the containers, diagram this flow, explain the architecture to X, show the architecture to a new engineer, or rebuild the architecture page. Not for recovering an undrawn codebase (recovering-built-architecture), UI prototypes (building-html-prototypes), or data modelling."
license: MIT
---

# Drawing architecture views

The architecture of a long-lived application lives in Markdown files with Mermaid diagrams: one view per file, an index beside them, and dated studies in their own folders. The files are the source of truth, readable on GitHub and in any editor. People look at them through one built file, `architecture.html`, which draws every view with pan, zoom, compare and light and dark themes, and needs nothing installed. This skill writes the views, keeps the index, explains the architecture to a named audience, and builds that page. The other architecture skills use it for the build step.

A view is a claim about the person's system, so every view answers one stated question and nothing else, and the page is rebuilt whenever a view changes: a picture that disagrees with its Markdown misleads the people who trust it most.

## Where the work lives

Read the repository's `AGENTS.md`, or its `CLAUDE.md` when there is none. Where it points to an architecture folder and a decision log, use them. Where it points nowhere, use `context/architecture/` and `context/decisions/`, and propose one pointer line for `AGENTS.md` in your report. The folder holds `README.md` (the index), `architecture.html` (the built page), one Markdown file per standing view, and `studies/YYYY-MM-DD-slug/` with the study's `README.md` and its own views. Standing views carry status `built` or `planned`; `proposed` appears only inside a study. Every file is named by its path relative to the folder, such as `containers.md` or `studies/2026-11-10-sync-risks/README.md`, in links, in the page and in the check lines.

[The view conventions](references/view-conventions.md) give the full location rule, what to do inside a prototype context, a product context repository or an existing `docs/architecture/`, the view format, element ids, evidence, the Mermaid subset and quoting, and the link forms. Read them before you write your first view in a folder.

## Modes

| Request | What to do |
|---|---|
| "Draw this", one diagram of one question | Draw one view: steps 1 to 7 |
| "Explain the architecture to X" | Write a guide study: steps 1 and 2, then [Explain to an audience](#explain-to-an-audience) |
| "Rebuild the page", or the Markdown changed | Steps 1, 6 and 7 |
| Another architecture skill wrote a view or study | It runs steps 6 and 7 before it reports |

## Draw one view

1. **Read first.** Open `AGENTS.md`, the decision log's index, the architecture index and the standing views the request touches. Note the element ids already in use: a view that renames an element splits one thing into two for every reader.
2. **State the view sentence.** "This view helps *audience* answer *question* about *scope* in *state*", where state is as built, as planned, or as proposed in this study. When you cannot fill it, the question is not clear yet: ask the person in one message, or state what you assumed.
3. **Pick the view.** The highest level that shows the fact in question (context, then containers, then one container's modules), then the concern: sequence for order and timeouts, deployment for what runs where and fails together, data flow for trust boundaries, state machine for allowed states, module graph for dependencies and cycles. The conventions' table maps each question to its file name and Mermaid type. One view first; a second only for a question the first leaves open.
4. **Check before drawing.** Look for an existing view that already answers the sentence. Update it rather than adding a near copy, because two views of one question drift apart.
5. **Write the view file** from [the view template](templates/view.md): the title, the Status line, the view sentence as the first sentence, one Mermaid fence, what the picture cannot show, the Elements and Relationships tables with evidence, and Related links. Keep it to at most 15 elements; split a larger system by concern or level. A view in a study is written in the study's folder and never edits a standing view.
6. **Update the index and build the page.** Before the first build in a folder, read the rules that govern it: where a context map or `AGENTS.md` says the folder holds Markdown only and does not name `architecture.html`, ask the person once whether to build the page there, because a built file would break a rule they set; without a yes, say the page was not built and why. Add or update the view's row in `README.md` (from [the index template](templates/architecture-index.md) when there is none), then build or rebuild `architecture.html`. Where a shell is available, run `bash`, then the path of [scripts/build-page.sh](scripts/build-page.sh) inside this skill, then the architecture folder:

   ```bash
   bash <this skill's directory>/scripts/build-page.sh context/architecture
   ```

   The same command does the first build and every rebuild: it copies the template when the folder has no page, places one block for every `.md` file under the folder, sets the built stamp, and writes only `architecture.html`. It needs bash 3.2 or newer and the standard `awk`, `find`, `sort`, `cut` and `date`; `git` is optional, for the stamp. It prints one `placed` line per file and stops with a message, writing nothing, when something is wrong. Where no shell is available, make the same changes by hand as [building the page](references/building-the-page.md) says: copy the template once, then change only the source blocks and the built stamp.
7. **Read the check lines.** The page writes `PASS path` or `FAIL path: detail` for every file, then `DONE passed/total`. Where the harness can open a browser, open the page, wait for the `DONE` line, fix every `FAIL`, rebuild and read again; then look at the drawn view once, because a diagram can parse and still read badly. Where it cannot, say the views were not drawn and ask the person to open the page and tell you the `DONE` line.

## Explain to an audience

An audience request ("explain this to the new mobile developer", "walk the client through it") is answered with the views that exist, not new ones: a new standing view made for one audience is one more thing to keep true.

1. Restate the audience and the question they bring. Pick the two or three existing views that answer it, in reading order.
2. Write a guide study at `studies/YYYY-MM-DD-guide-<audience>/README.md`: the title, the line `Date: YYYY-MM-DD · Kind: guide · Outcome: written`, a paragraph on what this audience needs to know and why, then one section per chosen view with a link to it, what to look at in it, and what it leaves out. Where two views are best read side by side, add a compare link. Explain the terms this audience will not know.
3. Add the study to the index's Studies table, rebuild the page and read the check lines (steps 6 and 7).

When no existing view answers the audience's question, say so and draw the missing view with steps 1 to 7 first.

## Output

- A view file in the architecture folder or in a study's folder, or a guide study.
- `README.md` listing it.
- `architecture.html` rebuilt with a block for every Markdown file and a new built stamp.

The offline copy (the page's **Save offline copy** button) is not output of this skill: a person makes it in a browser when they need to send the architecture to someone outside, and it is not committed.

## Done when

- The view states its sentence, answers that one question, and follows the conventions' checklist.
- The index lists every view and study, and its links resolve.
- The page reports `DONE n/n` with no `FAIL`, or your report says the views were not drawn and why.

## Example

The person asks: "Draw how a phone that was offline catches up." Reading the Larder folder shows `containers.md` and the ids `mobile`, `api`, `stream`, `worker`, `db`; no view covers order. The view sentence: "This view helps an engineer answer what happens, in what order, when a phone that was offline reconnects, about the sync path as built." Order makes it a sequence, so the file is `runtime-sync.md` with a `sequenceDiagram` whose participants use the same ids, Status `built`, and evidence paths for each step. The index gains a row; `scripts/build-page.sh` rebuilds `architecture.html`; the check lines end with `DONE 7/7`, one PASS for each Markdown file in the folder. Later the person asks to explain the sync to a new mobile developer: a guide study `studies/2026-11-17-guide-mobile/README.md` links `containers.md` (where the mobile client sits) and `runtime-sync.md` (what happens on reconnect), says to read the `alt` block for the 410 path, and adds no standing view.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| Writing or editing HTML in `architecture.html` | Run the script, or change only the source blocks and the stamp by hand |
| A view with no sentence, or one that answers three questions | One sentence, one question; a second view for a second question |
| A new id for an element another view already names | Reuse the id from the index's element ids table |
| A full set of views "for completeness" | Only the views someone's question needs |
| A new standing view for an audience request | A guide study that links the existing views |
| Reporting a rebuilt page without reading its checks | Read the `DONE` line, or say the views were not drawn |
| Committing the offline copy | It is a snapshot for sending; the Markdown and the page are the record |

## Hand back

Report what you wrote (each file's path), the view sentence, the page's `DONE` line and every `FAIL` with what you did about it, what is uncertain (assumed elements, evidence you could not find, a sentence you had to assume), and the skill that fits next: `evaluating-architecture-risks` for a critical look at what the view shows, `exploring-architecture-options` when the view exposed an open choice, `simplifying-system-architecture` when it looks heavier than its job, `recovering-built-architecture` when the views lack evidence from the code. Commit nothing: the person reviews and commits the views and the page together.

Without file access, return the view or the guide as Markdown, say that nothing was written and that the page was not rebuilt.

## Not for

- Finding out what an existing codebase contains when nobody has drawn it: `recovering-built-architecture` reads the code and writes the first evidenced views.
- UI prototypes or screen flows: `building-html-prototypes`.
- Data modelling: an `erDiagram` beside a view can show which store owns which information, but schema design belongs to the code.

## References

| Read | When |
|---|---|
| [view conventions](references/view-conventions.md) | Before the first view in a folder: location rule, view format, ids, evidence, Mermaid subset, links |
| [building the page](references/building-the-page.md) | Every build and rebuild of `architecture.html`, the script's messages, the by-hand route, reading the check lines, the offline copy |
| [the build script](scripts/build-page.sh) | Every build and rebuild where a shell is available: run it with `bash` |
| [growing into a model](references/growing-into-a-model.md) | When hand-kept views drift, or past about ten views of the same elements |
| [the page template](templates/architecture.html) | The first build by hand: copy it, never edit it. The script copies it itself |
| [the view template](templates/view.md) | Writing a view file |
| [the index template](templates/architecture-index.md) | Creating `README.md` in a new architecture folder |
