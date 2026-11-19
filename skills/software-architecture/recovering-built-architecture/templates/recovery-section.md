## Recovery

<!-- Paste this section at the end of the architecture index (README.md), after the Decisions section, and fill it. On a later recovery, replace the whole section: it describes one recovery at one commit.
Every path is backticked and relative to the repository root, as evidence paths are. Ids are the element ids the views use. Delete this comment and any placeholder row. -->

Recovered on [YYYY-MM-DD] at [short commit] from the code, by reading [the manifests, entry points, configuration, deployment files, CI and schema read, by path or folder]. [Scope: the whole repository | only the parts named, and what was left out.]

### Blind spots

What the repository cannot establish. Each row says what would settle it, so the next person can close it with one check.

| Blind spot | Why the repository cannot settle it | What would establish it | Ids |
|---|---|---|---|
| [The fact, as a question or a statement to confirm] | [Runtime only: a flag value, a setting outside the repository, traffic, a domain mapping, a secret; or code that is not in the repository] | [A command, a query, a dashboard page, a log search, or the person who knows] | [ids] |

### Where names and documents disagree with the code

The views follow the code. Each row is a claim the code does not bear out.

| Source | It says | The code does | Evidence |
|---|---|---|---|
| [`path/to/document.md:line`, a folder name, a package name] | [The claim, quoted or in a few words] | [What the code does instead] | [`path/from/repository/root.ext:line`] |
