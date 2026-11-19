---
name: recovering-built-architecture
description: "Recovers the architecture an existing codebase really has as evidenced standing views: context.md and containers.md (under context/architecture/ by default) with Status: built, a Verified line with date and commit, a repository path or the word assumed as evidence on every element and relationship, and a Recovery section in its README.md listing blind spots and where names or documents disagree with the code; then has architecture.html rebuilt. Reads manifests, entry points, configuration, deployment files and schema, keeps what the code shows, what deployment configuration says and what only runtime could confirm apart, and trusts the code over folder names and old documents. Use when the user says what is really there, recover the architecture, map this codebase, draw what we actually have, onboard me to this code, or our architecture docs are out of date. Not for recording why things are this way (decision-records), or a product context repository's baseline (designing-system-architecture)."
license: MIT
---

# Recovering built architecture

Answers "what is really there?" for an application that nobody has drawn, or whose drawings nobody trusts. The result is a small set of standing views that describe the system as built, where every box and arrow points at the file that proves it, plus an honest list of what the repository cannot prove. Reviews, option studies and simplifications all start from these views, so a wrong box here becomes a wrong conclusion three steps later. That is why this skill draws only what it can evidence, marks the rest `assumed`, and says out loud when a folder name, a README or an old diagram claims something the code does not do.

The views follow [the view conventions](references/view-conventions.md) and [the view template](templates/view.md): where the work lives, the view format, statuses, element ids, evidence, the Mermaid subset and the link forms are all defined there. Read the conventions before writing the first view. [Reading a codebase](references/reading-a-codebase.md) is the method for finding structure and telling evidence apart; read it before step 3.

## Modes

| Situation | What to do |
|---|---|
| No architecture folder, or one with no views | Recover: steps 1 to 10 |
| Views exist, but nobody has checked them against the code, or their `Verified` commit is old | Re-check: steps 1 to 10, starting from the existing views. Keep their file names and ids, correct each row from the code, and refresh `Verified` only on views you checked in full |
| Hand-written architecture documents exist (an `overview.md`, a wiki export, a diagram in the README) | Recover as above. Treat every document as a list of claims to test, never as a source to copy (step 2) |
| The person names a flow ("how does an offline phone catch up?") | After context and containers, add one runtime view for that flow (step 8) |
| The architecture lives in a separate product context repository | Write no standing view there: that repository's as-built work belongs to `designing-system-architecture`. Return the recovered views and the Recovery section as Markdown for it, unless the person names another place |

## Recover

1. **Find where the work lives.** Apply the location rule in the conventions: read `AGENTS.md` (or `CLAUDE.md`) and anything it imports. Where it points to an architecture folder and a decision log, use them and keep the existing file names. Where it points nowhere, use `context/architecture/` and `context/decisions/`, and propose the pointer line in your report. Note the decision log's location even when it is empty; this skill writes no record into it.

2. **Collect the claims, then set them aside.** Read `AGENTS.md`, the root `README.md`, every file already in the architecture folder, and the decision log. Write down each claim they make about the structure: "the API sends the reminder emails", "`packages/search` is a library", "the web client talks to the API directly". Each is a hypothesis to test in steps 3 to 6, with its file and line. Decision records are the exception in kind: they say why something was chosen, which the code cannot tell you, so link them from the views they explain. When the code contradicts an accepted decision, that is a disagreement to report, not a decision to rewrite.

3. **Read the structure, outside in.** Read in this order, because each layer tells you what to look for in the next: deployment manifests and container files (what runs in production), workspace and package manifests (what is built), entry points and process commands (what each unit starts), configuration and environment variables (what each unit connects to), CI (what is tested and deployed, and which services it needs), schema and migrations (what the stores hold and who writes them). [Reading a codebase](references/reading-a-codebase.md) lists where each of these hides per stack.

4. **List the deployable units and the stores.** In your working notes, one row per separately started process: what starts it (the command), what it is built from (the image or build), where it is deployed (the manifest entry), and how many instances. One image started with three commands is three units; a migration run before each deploy is a step, not a unit. Then one row per store: databases, streams, queues, caches, buckets, each with the units that read and write it. Then the people and the external systems.

5. **List the calls between them.** For each unit, find what it calls and what calls it: database clients and the tables they query, stream and queue producers and consumers, outbound HTTP with the host it reaches, inbound routes and the clients that call them. Cite the line that makes the call, and, where configuration decides the target, the configuration line that names it. An import of a client library shows that a call is possible; the call site and the configured target make it a relationship.

6. **Sort every fact by the kind of evidence behind it.** Three kinds, kept apart because they fail differently:

   | Kind | It shows | Draw it? |
   |---|---|---|
   | Static: the code | That a unit imports, calls, queries, sends | Yes, with the code path |
   | Configuration: deployment, CI, environment files | Which units exist in which environment, counts, schedules, which host a variable names | Yes, with the configuration path; say in the row's text when configuration is the only evidence, such as "named only in `render.yaml`" |
   | Runtime only | Whether a flag is on, a path is exercised, a domain routes where you think, a setting outside the repository holds | Only when code or configuration shows it can happen; say "unconfirmed at runtime" in the row and add a blind spot |

   Where two sources disagree, the code wins over names and documents, and the production manifest wins over the development stack for what runs in production. Record every disagreement for the Recovery section, with both paths.

7. **Name each element by what it does.** Describe a unit from its behaviour: what it reads, writes, calls and sends. When the folder, package or service name says something else (a `cache/` package that is the only writer of a table, a `shared/` package that opens its own database connection, a `legacy/` folder still on the login path), use the behaviour for the element's name and id, keep the folder in the Technology or Responsibility cell, and say in the row that the name misleads. Reuse an id that an existing view or the index already gives the same element.

8. **Draw context and containers.** Write `context.md` (the people, the system as one box, the external systems it calls or is called by) and `containers.md` (every unit and store from step 4 inside the system boundary, with the calls from step 5), each from the view template. In both:
   - `Status: built`, and the `Verified` part with today's date and the short commit from `git rev-parse --short HEAD`, written only when you checked every row of that view against the code at that commit and the files you cite have no uncommitted changes. The check is this: after the view is written, open every cited path at every cited line and confirm that the line shows what its row says, then correct or widen the citation where it does not. A path that exists but proves something else makes the line false. Read each row for its qualifiers as well as its nouns: "every member" is wrong where the query filters to members who opted in, and a version number needs the line that states the version. An author rereads a row and sees what they meant, so where the harness lets you start another agent with a fresh context, give one the view and the code, without your notes, and ask it to find every row whose cited lines do not show the whole of what the row says; correct the rows it finds before you write `Verified`, and say in your report who did the check. Where it cannot, do the same pass yourself from the last row upwards. Otherwise leave `Verified` off and say why.
   - Every element and relationship has evidence: a backticked path from the repository root, with a line where one statement proves it, code before configuration; `stated by <person>, <date>` for what the person told you; or `assumed`. A person's evidence is the text that names the role and what they do, such as the README or the auth code, not a client's entry file.
   - Elements that only configuration reveals, and facts unconfirmed at runtime, say so in their row (step 6).
   - Link the decision records that explain an element under Related.
   - At most 15 elements per view. Past that, split the containers view by concern, as the conventions describe.

   Draw no runtime, deployment or module view unasked. When the person named a flow, add one `runtime-<topic>.md` sequence view for that flow, with the same ids, each message evidenced like a relationship. When a further view would answer a question you noticed, offer it in the report instead.

9. **Write the index and its Recovery section.** Create or update `README.md` in the architecture folder as the conventions describe, with the views, the element ids and the decision log's location. Add or replace its Recovery section from [the recovery section template](templates/recovery-section.md): the date and commit, what was read, the blind spots, and where names and documents disagree with the code. When an existing document in the folder is out of date, leave its content as it is, list it in the index as not verified, and put each wrong claim in the disagreements table; propose in your report that the person replace or remove it, because it is their document and the page will otherwise show two contradicting pictures.

10. **Build the page and read the checks.** The page `architecture.html` beside the index draws every Markdown file in the folder. When `drawing-architecture-views` is available, rebuild the page by its steps before you report: run its build script on the architecture folder where a shell is available, or follow its by-hand steps where none is, then read the check lines. Where the harness can open a browser, open the page, wait for the `DONE` line, fix every `FAIL` in the Markdown, rebuild and read again. Where it cannot, say the views were not drawn and ask the person to open the page and tell you the `DONE` line. When `drawing-architecture-views` is not available, the views stand as Markdown: say in your report that `architecture.html` was not rebuilt, and that `drawing-architecture-views` is the skill that rebuilds it. Write no HTML yourself.

Configuration files hold secrets. Read them for names and structure only: cite the file and line and name the variable, and never copy a secret's value (a token, a password, a key, a connection string with credentials) into a view, the index or your report, because those files get committed and shown to other people. Where a value is needed to make a point, describe it ("a hosted Postgres URL"). Keep configuration and runtime apart in what you write: when the production configuration turns a dependency on, say it is configured on and cite the line; a blind spot is only what the running system alone could show, such as whether the configured path is exercised. And make each citation carry its whole row: when a row makes two claims, cite the line for each. Ask the person nothing before you are done. What the repository cannot answer becomes a blind spot with what would establish it, and the questions a person could answer in a minute go in the report, in one list.

## What this skill does not write

- **No decision record for an inferred decision.** The code shows what was built, not why, nor whether anyone chose it. When the code reveals a consequential choice with no record (an outbox table instead of sending mail inline, a read replica, a cache in front of the database), list it in the report as a choice the person may want to record, with its evidence. Recording it, with the reasons only the person knows, is a separate step.
- **No judgement of the design.** Describe what is there, including what looks redundant or risky, in neutral terms in the Responsibility cells. Risks and simplifications are for the skills named in the hand back, which start from these views.
- **No change to code, configuration or the person's documents.**

## Output

- `context.md` and `containers.md` in the architecture folder, and one `runtime-<topic>.md` only for a flow the person named. Each with `Status: built`, a `Verified` part where earned, evidence on every row.
- `README.md`: the index, with the Recovery section (blind spots, disagreements).
- `architecture.html` rebuilt with a new stamp and its check lines read, or the report saying it was not rebuilt or not drawn.

## Done when

- Every element and relationship in every view written has evidence (a path that exists at the verified commit and whose cited line shows the row, or a `stated by`) or is marked `assumed`.
- Every element the code or the production configuration shows is drawn, or its absence is a blind spot; every disagreement between code and a name or a document is in the Recovery section.
- No decision record was written, and no runtime view was drawn that nobody asked for.
- The page reports `DONE n/n` with no `FAIL`, or the report says the views were not drawn, or that the page was not rebuilt and which skill rebuilds it.

## Example

Larder's `AGENTS.md` points to no architecture folder, so the work goes to `context/architecture/`. Its README says "the API sends reminder emails", and its layout table lists `packages/search` as "search helpers". The production manifest starts the API image twice, as the web service and as a second service with the command `node dist/mailer.js`, and it deploys `packages/search` from its own Dockerfile as a private service. Reading the code: the API's reminder routes only insert rows into an `outbox` table; the mailer polls that table and posts to the mail provider. So the containers view has `api`, `mailer` and `search` as three units, `search` named for what it does (a search service over HTTP, code in `packages/search`, the name says library), and the README's claim goes in the disagreements table with both paths. An error tracker appears only as a DSN variable in the production manifest: it is drawn, its row says "named only in the deploy manifest", and its evidence cites the code that reads the variable and the manifest line that sets it. The manifest lets the API scale from one to four instances, and its rate limiter keeps counts in process memory; how many instances run is unconfirmed at runtime, so the blind spot reads: "How many API instances run in production, which decides whether the rate limit is per instance. Would establish it: the hosting dashboard's instance count for the API service, or the person." No decision record is written for the outbox, and the report lists "mail sent through an outbox and a separate mailer" as a choice worth recording.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| One element per top-level folder | One element per separately started process or store, found from manifests and entry points |
| Redrawing the old diagram with better styling | Test each of its claims against the code; draw what the code shows; list what it got wrong |
| An element named after its folder when the code does something else | Name it by behaviour; keep the folder in the row; record the disagreement |
| An arrow because a library is imported | An arrow for a call site, with the configured target where one decides it |
| Reading the development stack as production | The production manifest decides what runs; note development-only services in prose |
| Evidence that looks precise but proves nothing: a path that does not mention the element | A path whose content shows the row, or `assumed` |
| A `Verified` line on a view you checked only in part | Leave it off and say what was not checked |
| A decision record for "why there is an outbox" written from the code | List the choice in the report for the person to record |
| A runtime, deployment and module view "while you are at it" | Context and containers; one runtime view for a named flow; offer the rest |
| Blocking on questions before drawing | Draw what the repository proves; list the questions and blind spots |

## Hand back

Report, in this order:

- **Written**: each file's path, created or changed, and the page's `DONE` line with every `FAIL` and what you did about it; or that the views were not drawn; or that the page was not rebuilt and `drawing-architecture-views` rebuilds it, with a request to have it rebuilt and to read its `DONE` line before relying on the pictures.
- **Disagreements**: each place the code contradicts a name, a document or a decision record, in one line with both paths.
- **Uncertain**: the elements and relationships marked `assumed` or "unconfirmed at runtime", and the blind spots, each with what would establish it. Then the questions a person could answer quickly, as one list.
- **Choices worth recording**: consequential choices the code shows with no decision record, for the person to record with their reasons.
- **Next**: `evaluating-architecture-risks` for a critical look at what the views show, which is the usual next step on an existing application; `simplifying-system-architecture` when the views show more units, stores or hops than the job seems to need; `drawing-architecture-views` to explain the views to a named audience, or to rebuild the page when it was not rebuilt. Where the location rule found no pointer, give the pointer line for `AGENTS.md`.

Commit nothing: the person reviews the views and commits them. Without file access, return the views and the Recovery section as Markdown, and say that nothing was written and the page was not rebuilt.

## Not for

- Recording why the system is the way it is. Decisions come from people; a decision record is written with the person, through the decision log's own process (`decision-records` where installed), never inferred from code.
- The architecture baseline of a product context repository: `designing-system-architecture` owns those views.
- Reviewing the design for risks (`evaluating-architecture-risks`), comparing options (`exploring-architecture-options`) or removing parts (`simplifying-system-architecture`). Each of them starts from what this skill leaves behind.

## References

| Read | When |
|---|---|
| [reading a codebase](references/reading-a-codebase.md) | Before step 3: where structure hides per stack, one image run as several processes, the three kinds of evidence, names and documents that mislead, writing a blind spot |
| [view conventions](references/view-conventions.md) | Before the first view: location rule, view format, statuses, the Verified line, ids, evidence, Mermaid, links |
| [view template](templates/view.md) | Writing `context.md`, `containers.md` or a runtime view |
| [recovery section template](templates/recovery-section.md) | Writing the Recovery section of the architecture index |
