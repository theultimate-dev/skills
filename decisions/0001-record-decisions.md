# 0001: Record decisions as short records in `decisions/`

- Status: accepted
- Date: 2026-09-03

## Context

This repository will accumulate small structural choices: skill format, directory layout, how people install and update, how releases work. The reasons behind such choices evaporate within weeks. Two audiences need them later: agents working in this repo, which otherwise re-litigate or quietly undo a choice because they only see the resulting tree, and readers who install these skills and ask "why not X".

The repository is also a public example of how I run projects, so the way decisions are kept is itself part of the product.

## Options

1. **No records.** Reasons live in commit messages and README prose. Cheap, and the reasons scatter until nobody can find them.
2. **Full ADR tooling.** `adr-tools`, `log4brains`, or the complete MADR template with a generated site. More structure than a small repo needs; long templates invite filler, and agents fill them dutifully.
3. **Short records with an index.** One Markdown file per decision in `decisions/`, four sections, one to two pages, listed in `decisions/README.md`, which `AGENTS.md` links to.

## Decision

Option 3.

- File: `decisions/NNNN-kebab-title.md`, numbered sequentially from `0001`, never renumbered.
- Head: `# NNNN: Title`, then `- Status:` and `- Date:` lines. `- Supersedes:` and `- Superseded by:` appear only when they apply.
- Body: `Context`, `Options`, `Decision`, `Consequences`. Write for a technical reader with five minutes. Options include the ones rejected and why.
- Status lifecycle: `proposed` → `accepted` → `deprecated` or `superseded`. Superseding means a new record that links back; the old record gets its status changed and a link forward. Nothing else in an accepted record changes.
- Index: `decisions/README.md` lists number, title, status, one-line summary. Agents read the index first and open records on demand. `AGENTS.md` links the index with a markdown link, not an import, so it is not loaded into every session.

## Consequences

- Reasons survive the people and sessions that produced them. Agents get progressive disclosure: index in `AGENTS.md`, record when relevant.
- A structural change without a record is incomplete work. `scripts/validate.py` keeps the index and the files in sync; judgment about what deserves a record stays with the author.
- The `decision-records` skill in this repository implements this decision for any project, including projects that already keep ADRs another way.
