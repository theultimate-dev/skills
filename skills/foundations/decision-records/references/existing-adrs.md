# Projects that already keep ADRs

Many projects already have a decisions folder in some shape. The rule is to adopt in place: keep their location, numbering, and template, and add only what is missing for people and agents to find and trust the log. Moving or renumbering breaks links in issues, pull requests, and other people's notes.

## Recognise the convention

| You find | What it is | Keep |
|---|---|---|
| `docs/adr/NNNN-title.md`, `doc/adr/`, `adr/` | Nygard-style ADRs, often created with `adr-tools` (an `.adr-dir` file at the root) | Location and numbering. `adr-tools` expects the `.adr-dir` path and `NNNN-title.md` names |
| `docs/decisions/NNNN-title.md` with `status`, `date`, `deciders`, `consulted`, `informed` in YAML frontmatter | MADR | The frontmatter and the MADR section names. Fill in the same fields |
| `docs/adr/` plus `.log4brains.yml` and `package.json` scripts | log4brains, which generates a website from the records | Their frontmatter and status vocabulary. Use the `log4brains` CLI rather than editing generated output |
| Records under `architecture/decisions/`, an ADR section in `ARCHITECTURE.md`, or a wiki | House convention | Whatever they do. Ask before changing anything beyond adding an index |
| `decisions/` without a `README.md` | This skill's shape, unfinished | Add the index and the `AGENTS.md` link |

## Adopt, then add what is missing

1. **Index.** If the folder has no index (`README.md`, `index.md`, or a tool-generated listing), add `README.md` in that folder with the same table this skill uses: number, title, status, one-line summary, in their numbering. If they already have an index in another format, leave it.
2. **Agent link.** Add the Decisions section to `AGENTS.md` or `CLAUDE.md`, pointing at their folder and index (see `bootstrapping.md`, step 3). This is the change that makes the log visible to agents, and it is almost always missing.
3. **Status vocabulary.** Map, do not rename. MADR uses `proposed`, `rejected`, `accepted`, `deprecated`, `superseded by ADR-0005`. Nygard uses `Proposed`, `Accepted`, `Deprecated`, `Superseded`. Use their words in their records and in the index.
4. **New records** follow their template, not this skill's. Treat the four-section structure as a checklist for content, not a format to impose.

## When two conventions coexist

Sometimes there is a `docs/adr/` from years ago and a newer `decisions/` folder, or ADRs scattered across READMEs. Do not merge them silently. Propose one of two paths and record the choice as a new decision in whichever folder stays canonical:

- **Keep both, freeze the old one.** A note at the top of the old index says new records go to the new folder; the new index lists the old folder under a "Historical" heading.
- **Consolidate.** Copy the old records into the new folder with their original identifiers preserved in the title ("0003 (was ADR-0012): …") and leave a redirect stub in the old location. Rarely worth it.

## What not to do

- Do not renumber, rename, or move existing records.
- Do not edit the body of an accepted record to match a new template.
- Do not delete records marked rejected or deprecated. They are the most useful ones.
- Do not introduce a second tool. If they use `adr-tools`, run `adr new`; if they use log4brains, use its CLI.
