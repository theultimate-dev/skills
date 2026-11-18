# Plan 01: the software-architecture plugin

Status: planned

Spec: `spec.md` · Roadmap: `roadmap.md`
Requirements: R1 to R40
Acceptance criteria that pass in this plan: AC1 to AC38
Depends on: none
PR slices: whole plan
Branch: feat/software-architecture

The agreed design and its research are in `/Users/igor/dev/theultimate-dev/skills/specifications/software-architecture/` (untracked, main checkout only). Every worker gets that absolute path.

## Outcome

A person can install `software-architecture` and ask an agent, in any repository, what is really built, for a critical look, for options, for a simpler design or for a drawing, and gets Markdown views with Mermaid plus one `architecture.html` that anyone can open. The plugin is released as 0.1.0.

## Boundaries

- In scope: `skills/software-architecture/`, decision 0022, the catalog and changelogs, `MIRRORS` in `scripts/validate.py`, one sentence each in `brainstorming-solutions` and `designing-system-architecture`, the prototype profile exception and its mirrors, the root README, the release commit.
- Out of scope: the spec's non-goals; a plugin README, visuals and committed evaluations (follow-up).
- Contracts produced or consumed: the view format and the HTML template's marker lines, link form and check lines (settled in p2, consumed by p3 and p4); the scenario intake (settled in p3, consumed by p4).
- Shared files and their owning slice: one slice. Within it, the orchestrator owns `marketplace.json`, `README.md`, both changelogs of the category and the root, `scripts/validate.py` and the mirrored copies.

## Phase 1: planning files and decision 0022

- Tasks:
  1. Commit `spec.md`, `roadmap.md`, this plan and the re-confirmed `verification-profile.md`.
  2. Write `decisions/0022-software-architecture-category.md` with the `decision-records` skill, covering every point of R35, and add its row to `decisions/README.md`.
  3. Add the root changelog entry for the decision.
- Files: `docs/product-engineering/software-architecture/**`, `docs/product-engineering/verification-profile.md`, `decisions/0022-software-architecture-category.md`, `decisions/README.md`, `CHANGELOG.md`
- ACs: AC33 passes here
- Leaves the base working because: additive only; the validator passes

## Phase 2: `drawing-architecture-views`, the HTML template and the category scaffold

- Tasks:
  1. Check each of the five names again on skills.sh and in the ten packs' repository trees, and keep the output as evidence. A collision goes to Igor before the affected skill is written.
  2. Write `templates/architecture.html` from the lab prototype `research/viz-lab/poc/viewer.html`: source blocks between marker lines, the pinned Mermaid address on one line, formatted prose with tables, lists and links, the switcher in two groups, pan, zoom, fit, full screen, light and dark, compare with its link form, the built stamp, the no-network message with sources as text, the check lines, and Save offline copy with pan, zoom and theme kept.
  3. Write `scripts/build-page.sh` (R41) from the build steps, and check it with `/bin/bash` 3.2 on macOS and in a Linux container (AC38).
  3. Write `templates/view.md`, `references/view-conventions.md`, `templates/architecture-index.md`, `references/building-the-page.md`, `references/growing-into-a-model.md` and `SKILL.md`.
  4. Create `skills/software-architecture/CHANGELOG.md`, the `marketplace.json` entry at `0.0.0`, the README category row and the root changelog entry for the plugin.
  5. Build a page from the fixture's `larder-views/` by the steps in `building-the-page.md` and run the browser rows AC7 to AC15 and AC17 on it; run AC18 on the conventions' own example with `<b>` and `<br/>` labels; write the quoting rule as Igor settled it at G4 (R11).
- Files: `skills/software-architecture/drawing-architecture-views/**`, `skills/software-architecture/CHANGELOG.md`, `.claude-plugin/marketplace.json`, `README.md`, `CHANGELOG.md`
- ACs: AC6 to AC18, AC27 and AC38 pass here (AC6, AC16 and AC27 are observed in trial T7 at stage 6); AC1, AC2, AC3 and AC34 progress only
- Leaves the base working because: additive only; the validator passes with a one-skill category
- Stop point: a finding that contradicts any section of the agreed spec goes to Igor with a recommendation before p3 depends on it. This holds in every phase

## Phase 3: `recovering-built-architecture` and `evaluating-architecture-risks`

- Tasks:
  1. Two workers in parallel, one skill each: `SKILL.md`, its references and templates with the content R30 lists, including `references/scenario-intake.md` in evaluating. A worker's own checks are scoped to its skill directory: the frontmatter keys, the line count, the banned path strings, and every link except those to the two mirrored files, which arrive at integration. The full validator runs on the integrated branch, because the catalog, the README and the mirrors are the orchestrator's.
  2. The orchestrator integrates both, copies `templates/view.md` and `references/view-conventions.md` into each, adds the `MIRRORS` entries with their comments, and adds each skill to `marketplace.json`, the README row and the plugin changelog.
  3. Run the validator; tamper one mirrored copy and see the validator fail.
- Files: `skills/software-architecture/recovering-built-architecture/**`, `skills/software-architecture/evaluating-architecture-risks/**`, `scripts/validate.py`, `.claude-plugin/marketplace.json`, `README.md`, `skills/software-architecture/CHANGELOG.md`, `CHANGELOG.md` (the `MIRRORS` line)
- ACs: AC19 to AC22 pass here (observed in T1 to T3 at stage 6); AC2 to AC5, AC28 and AC30 progress only
- Leaves the base working because: additive only

## Phase 4: `exploring-architecture-options` and `simplifying-system-architecture`

- Tasks:
  1. Two workers in parallel, one skill each, as in phase 3.
  2. The orchestrator integrates both, copies the three mirrored files into each, and completes `MIRRORS` (ten pairs), `marketplace.json`, the README row and the plugin changelog.
  3. Run the validator; `cmp` all ten pairs.
- Files: `skills/software-architecture/exploring-architecture-options/**`, `skills/software-architecture/simplifying-system-architecture/**`, and the shared files of phase 3
- ACs: AC2 to AC5, AC23 to AC26, AC28 to AC30 and AC36 pass here (the trial rows observed in T4 to T11 at stage 6)
- Leaves the base working because: additive only

## Phase 5: changes outside the category

- Tasks:
  1. One sentence in `brainstorming-solutions/SKILL.md` and one in `designing-system-architecture/SKILL.md`, each with its plugin's changelog entry.
  2. The prototype profile exception for `architecture/architecture.html` in its source and every mirrored copy, with the `product-prototyping` changelog entry.
  3. The root README: the plugin in the changelog list and the plugin section with its step, skill, output and gate table, the install line and example requests.
  4. Run the validator and `git diff --check origin/main...HEAD`.
- Files: `skills/product-engineering/brainstorming-solutions/SKILL.md`, `skills/product-context/designing-system-architecture/SKILL.md`, the prototype profile and its copies under `skills/product-prototyping/`, three plugin changelogs, `README.md`, `CHANGELOG.md`
- ACs: AC1, AC31, AC32 and AC34 pass here
- Leaves the base working because: wording only; the mirror check passes

After phase 5 the loop runs stage 6 (the first checkpoint of the Verification contract: AC1 to AC34, AC36 and AC38 on the implementation head), stage 7 (quick review), stage 8 (push, pull request, `review:human`) and stage 9 (full review and repairs until it approves).

## Phase 6: the release commit

- Tasks:
  1. With the `release-process` skill in independent-versions mode: `software-architecture` 0.1.0; a patch release for each of `product-engineering`, `product-context` and `product-prototyping`; the marketplace release with at least a minor bump, listing the four plugins.
  2. Set this plan to `Status: done` in the commit before the release commit, so the release commit touches only changelogs and versions.
  3. Run the second checkpoint: AC35 with the workflow checks it names, AC1, and AC34 against the released sections. Create no tag. Get a delta review of the release commit.
- Files: `CHANGELOG.md`, four `skills/<category>/CHANGELOG.md`, `.claude-plugin/marketplace.json`
- ACs: AC35 passes here
- Leaves the base working because: the validator and the replayed release checks pass on the commit; no tag exists until Igor confirms the merge

## After the release commit: overview, handover, tags

These are the orchestrator's steps. They change no tracked file, so the release commit stays last.

1. Build the HTML overview with the parts AC37 lists, from the verification report, the review findings and the screenshots, and publish it with the Artifact tool.
2. Hand over the pull request link and the overview link, and stop. Igor reviews and merges with a merge commit.
3. Only when Igor says the pull request is merged: confirm on `origin/main` that the merge commit contains the release commit; create the annotated tags on that release commit; push the plugin tags first, by name and at most three per push (`software-architecture--v0.1.0`, `product-engineering--v0.2.1`, `product-context--v0.2.1`, then `product-prototyping--v0.2.1`), then the marketplace tag; confirm that the release workflow ran and succeeded for each of the five tags; report the result; remove the worktrees this session created.

- ACs: AC37 passes at step 1.

## Notes

## Changes after launch

- 2026-11-18 The decision record is 0022 and the marketplace release 0.6.0, because `main` gained `dev-environment` during phase 2; the branch was rebased before its first push.
- 2026-11-18 Phase 2 gained `scripts/build-page.sh` (R41, AC38) on Igor's decision.
- 2026-11-18 AC5's check changed to a classified scan on Igor's decision (roadmap, Decisions).
- 2026-11-18 Phase 5's wording changes were committed during phase 3, and the trials for a skill started as soon as that skill's directory stopped changing; a trial is rerun whenever its skill's files change afterwards.
