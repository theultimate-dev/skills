# 0019: Mirror a template that two skills share, and let the validator keep the copies identical

- Status: accepted
- Date: 2026-10-25

## Context

`AGENTS.md` makes every skill self-contained: links stay inside its directory. 0006 adds that each product-design skill works without the others installed. A skill can be installed alone: from a release zip, or picked out of a flat installer.

`curating-design-systems` (0018) needs the design-tree check that `building-html-prototypes` ships as `templates/tree-check.html` (0017), a 254-line browser-only template. Until now, no file in one skill has been the same as a file in another.

## Options

1. **The new skill names its sibling's template and falls back to manual steps.** No copy. Lost: installed alone, the skill has only manual checks, against 0006.
2. **Move the shared check into the new skill, and extend it with the new token checks.** Lost: it changes a check that `building-html-prototypes` already ships, beyond what #11 asks.
3. **A byte-identical copy in each skill, listed as a mirror that the validator compares.** Won: each skill works on its own, and the copies can't drift.

## Decision

Option 3.

- **The list.** `scripts/validate.py` holds a list of mirrored files, each a source path and a copy path. The first pair is `building-html-prototypes/templates/tree-check.html` and `curating-design-systems/templates/tree-check.html`.
- **The check.** The validator reports an error when the copy differs from its source by a byte, or when either file is missing.
- **Changing a mirrored file.** A change to the source changes every copy in the same commit. The file's text names no skill's own files, so it reads correctly in each skill.
- **Who this applies to.** Only templates that two skills need unchanged are mirrored. A file that one skill adapts stays its own file, as the `task-brief.md` templates of `implementing-plans` and `running-implementation-loops` do.

## Consequences

- A skill can ship another skill's check unchanged and still install alone.
- A mirrored file costs one review, of its source. The copy is proven by the validator rather than read.
- The validator now ties two skills together, and `AGENTS.md`'s skill-format rules name the mirror list.
- Revisit if a third skill needs a mirrored file. Then a mirrored file could carry a marker the validator reads, instead of a list kept in the validator.
