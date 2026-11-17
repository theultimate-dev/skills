# Growing into a model

Hand-kept views are separate pictures: each view draws its elements again, and nothing checks that two views agree. That is cheap and readable everywhere for a handful of views. Past roughly ten, keeping them in agreement can cost more than drawing them. This reference says how to notice that, what to do first within the Markdown format, and when to move to a model-based tool. It describes the route; it builds nothing.

## Signs the views are drifting

Look for these whenever you read or change the architecture folder, and name any you find in your report:

- **The same element described differently in two views**: a different technology, responsibility or label for one id. Compare the Elements tables row by row for each id.
- **Ids that no longer match**: an id in a view that is missing from the index's element ids table, two ids for one element, or one id for two elements.
- **More than roughly ten standing views**, or one element drawn in four or more of them.
- **Renames that need many edits**: a change in the code that touched one element made you edit five files.
- **Verified lines falling behind**: several views with no Verified part, or Verified at commits far older than the code they describe.

One sign is a reason to tidy. Several, recurring after each tidy, are the reason to consider a model.

## First, within this format

These keep hand-kept views honest for longer and cost nothing new to install:

1. **Make the index's element ids table complete**, and fix every view to it: one id, one name, one kind. It is the one place an element is defined.
2. **Put each fact in one view.** The full responsibility and technology of an element belong in the Elements table of the view at its own level (a container in the containers view). Other views give the short label and say "detailed in containers.md".
3. **Remove views nobody uses.** A view that answers no current question still has to be kept true. Delete it, list it under Related in the view that replaced it, and remove it from the index.
4. **Split by level instead of by audience.** Several views of the same level for different readers multiply the copies of each element; one view per level, plus a guide study per audience that links them, does not.
5. **Re-verify the oldest views first**, so Verified lines show where to trust the folder.

Where a shell is available, a search for each id across the folder (for example `grep -rn "\bapi\b" context/architecture`) shows every place it is drawn, which is most of what a model would tell you.

## The route to a model

A model-based tool holds each element and relationship once, in one source, and derives every view from it. LikeC4 is the one to consider first: its source is plain text, it is MIT-licensed and actively released, and it can write Mermaid.

**What it gives.**

- One definition per element: a rename is one edit, and every view follows.
- Views as queries over the model ("this system's containers", "everything the API touches"), so a new view costs a few lines and cannot disagree with the others.
- Checks: its validate command reports an unknown element or a broken relationship in under a second.
- A built site with pan, zoom and navigation between levels, which it can also write as one HTML file that opens offline.

**What it costs.**

- Node and a build step on the machine of whoever changes the architecture; nothing draws its source natively, not GitHub and not common Markdown editors.
- A second syntax for agents and people to learn, and a model that has to be kept true like any code.
- Stricter scope: it leaves out relationships that do not belong at a view's level, which is correct and can surprise an author who wanted that arrow.

**How the existing views carry over.**

1. Write one model file from the element ids table and the Elements and Relationships tables: each id becomes an element with the same id, name, technology and description, and each relationship row becomes a relationship with the What flows text as its title.
2. Define one view per existing standing view, with the same name and the same question.
3. Generate Mermaid from the model into the views' fenced blocks, so the Markdown files, the index and the built page keep working for everyone who reads them. The Evidence and Status columns, the view sentence and the "cannot show" sentence stay in the Markdown, written by hand, because the model does not hold them.
4. Keep studies as they are. A study is a dated record; it keeps its own hand-written views, with the same ids as the model.
5. Record the move as a decision in the decision log, with what triggered it, and add the model file's location to the pointer line in `AGENTS.md`.

Propose the move to the person with the signs you found and the cost above; make it only when they agree, because it changes how everyone edits the architecture.
