# Plan 01: Native surfaces in direction briefs, and the renderer's hand-over

Status: done

Spec: `spec.md` · Roadmap: `roadmap.md`
Requirements: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11
Acceptance criteria that pass in this plan: AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13
Depends on: none
PR slices: whole plan
Branch: feat/exploring-visual-directions-native-surfaces

## Outcome

Given a native platform surface, `exploring-visual-directions` writes each direction with:

- its placements at real scale;
- its platform fit;
- system type and symbols, handled according to their licence;
- the risks specific to native surfaces.

The three sketches share one platform frame, which `building-html-prototypes` takes as given. When nothing settles what kind of surface it is, the skill asks first. A responsive page keeps the briefs it gets today.

## Boundaries

- In scope: R1 to R11.
  - `exploring-visual-directions`: `SKILL.md`, a new `references/native-surfaces.md`, `references/typography-and-spacing.md`, `references/inspiration-and-critique.md` and `templates/direction-comparison.md`.
  - `building-html-prototypes`: the licence check, and "start from a brief's platform frame", in `references/native-surface-profile.md` and `references/offline-artifact-contract.md`, plus the type and symbol lines of `templates/prototype-notes.md`.
  - The six Harbor fixtures and their trials in `evaluations/product-design/`.
- Out of scope:
  - `designing-ux-flows`, `preparing-implementation-handoffs` and the coordinator row, which belong to plan 02.
  - The release.
  - The spec's non-goals: device geometry tables, settings beyond the four, the one-file default, and any other rendering change.
- Contracts produced:
  - The platform frame: placements, scale mapping, geometry tokens with sources, the system UI beside the surface, the four settings, and system type and symbols. Its fields match the "Native surface" section of `building-html-prototypes/templates/prototype-notes.md`.
  - The template markers: a line for one kind of surface ends in "(native surface)" or "(responsive page)", and a comment at the top of the template says to delete the other kind's lines.
- Contracts consumed: the native-surface profile of `building-html-prototypes`, from #9 part 4.
- Shared files and their owning slice:
  - `skills/product-design/CHANGELOG.md` and `evaluations/product-design/README.md`: 01, then 02.
  - The frame contract and the marker convention: 01.

## Phase 1: Native surfaces from direction brief to sketch

- Tasks:
  1. Failing check first.
     - Add the fixtures F-mac, F-droid, F-web, F-amb, F-code and F-mix under `evaluations/product-design/fixtures/`.
     - Add an "Agent trials: native surfaces" section to `evaluations/product-design/README.md`, with the task texts, rubrics, staging and transcript scan, and rerun steps.
     - Add a root `CHANGELOG.md` `[Unreleased]` line.
     - Run baselines B1, B-amb and B-droid on f401cae. They must fail: B1 on AC3, AC4, AC5, AC7 and AC8; B-amb on AC2; B-droid on AC6's Android part. A baseline that passes marks its row "regression guard", and its fixture is sharpened before the skill changes, with the change logged under Notes.
  2. `exploring-visual-directions`:
     - `SKILL.md`: an "identify the surface" paragraph, and native wording for the per-direction list, the rendering task and the selection. The description names native platform surfaces.
     - `references/native-surfaces.md` (new): the signals, placements, the frame's fields, platform fit, system type and symbols by licence, native risks, and a short example.
     - `references/typography-and-spacing.md`: platform system fonts and symbols, with the licence check.
     - `references/inspiration-and-critique.md`: the critique checks placements and scale for a native surface.
     - `templates/direction-comparison.md`: the marked native and responsive lines.
     - `skills/product-design/CHANGELOG.md` `[Unreleased]` Added.
  3. `building-html-prototypes`:
     - `references/native-surface-profile.md` "System type and symbols": the licence check. Plus a rule to start from a brief's platform frame and ask only for what it lacks.
     - `references/offline-artifact-contract.md` "Fonts and imagery": the same licence rule.
     - `templates/prototype-notes.md`: type and symbol lines that fit both cases.
     - `skills/product-design/CHANGELOG.md` `[Unreleased]` Changed.
  4. Run the trials and the AC rows (stage 6), then set this plan's `Status: done` before the PR opens.
- Files:
  - `skills/product-design/exploring-visual-directions/**`
  - `skills/product-design/building-html-prototypes/{references/native-surface-profile.md, references/offline-artifact-contract.md, templates/prototype-notes.md}`
  - `evaluations/product-design/**`
  - `skills/product-design/CHANGELOG.md` and `CHANGELOG.md`
  - the planning files
- ACs: AC1 to AC13 pass here.
- Leaves the base working because: it's additive, and responsive briefs keep their wording, with markers added.
- PR slice: own PR, about 300 changed lines, not counting the planning files. Predicted category: `human`, because the user reviews every PR.

## Notes

- 2026-10-24 01: the transcript scan ships as `evaluations/product-design/scan_transcript.py`, not as a scratchpad script, so a later rerun has it. The profile's changes therefore land with the fixtures in task 1, not with the planning files.
- 2026-10-24 01: in the fixtures that aren't macOS, the action reads "Settings" without the macOS ellipsis. The shared schedule setting drops "while on battery". Both changes keep a device hint out of the brief that names no platform.
- 2026-10-24 01: a baseline executor found that "41.2 GB · 2 warnings" disagreed with the volume list, which shows one warning and one failure. The line now reads "1 warning, 1 failure". No criterion reads that line. The baselines are rerun on the corrected fixtures with the candidate trials, so both sides grade the same input.
- 2026-10-24 01: the transcript scan read arithmetic in a shell heredoc, such as `/255`, as a path. A path now has to start with a letter, `_`, `.` or `~`. The fault probe still gives its three hits, and the clean probe still prints `CLEAN`.
- 2026-10-24 01: B-droid at f401cae already records Roboto as open source and embeddable, so D1 can't fail on the baseline. D1 guards against the licence rule overcorrecting, and it's reported as a regression guard. No fixture change could make the baseline fail without making the expected behaviour wrong.
- 2026-10-24 01: the first scan of the stage-6 runs flagged two runs, and neither was an escape. T-web-2 had changed into `<run>/project`, and B-amb had written `/etc` as sample text inside a `cat` heredoc. The scan now normalizes the `cd` target and skips the bodies of heredocs that `cat` or `tee` writes. A Python heredoc is still scanned, and so is a `cd` that climbs out of the run, and the fault probe covers both. All 15 runs then scanned `CLEAN`.
- 2026-10-24 01: the graders are grouped by the criteria they share, not one per fixture. One grades the menu-bar runs (N1–N7), one the surface runs (A1, C1, M1), one the web and Android runs (W1, W2, D1), and one the hand-over (H1–H3). Each still sees only candidate and baseline outputs under random IDs, plus the rubric.
- 2026-10-24 01: correction to the B-droid note above. That note read only D1's grep, which is empty on the baseline. The blind grader graded B-droid D1 "no": it names no licence for Roboto ("Roboto-class", "no embedding task"). So D1's positive part discriminates, and only its grep is a regression guard.
- 2026-10-24 01: repair round 1, `250a92d`. Grading at `3e81673` failed N3 in two of three T1 runs, whose directions repeated the frame's scale mapping in their risks. The strict N2 and W2 greps printed lines in two T1 runs and all three T-web runs, each saying that the other kind's entries don't apply. The skill now says directions refer to the frame without repeating its values, and leave the other kind's entries out without noting them. The selection sentence was clarified at the same time, after a cold reader at `3e81673` read the native case as adding sizes.
- 2026-10-24 01: repair round 2, `e0ee116`. At `3e81673` the hand-over harness reported `DONE 16/17`. The frame's `--window-default-size` held two lengths, so the renderer split it, and the frame's own name resolved nowhere. The fault run, with `--cutout-width` deleted, failed on that token as intended. The reruns at `250a92d` still wrote size tokens and reused one name for two values. The frame now asks for one length per token, under its own name and on its own row. Every exploring-visual-directions trial reran at `e0ee116`. The `250a92d` runs show the round-1 fix only.
- 2026-10-24 01: the transcript scan skipped a whole `cat` heredoc line, so `cat > /tmp/dummy; python3 - <<'E'` hid both the redirect and the Python body. The `250a92d` T-droid run wrote an empty `/tmp/dummy` that way and scanned clean. Since `e4750da`, the scan skips only the body. Rescanned with it, that run is void (it was superseded anyway, and the file was removed), and every other run is clean or clean on a second pass that lists every filesystem-root path. A grader at `3e81673` had also created and removed an empty `/tmp/q.sh`. Grader briefs now forbid temporary files.
- 2026-10-24 01: T1's frame marks every geometry token "to supply", because executors have no network. So T2 and B2 stop and ask for exactly those values, and H1 can't tell them apart. H1 is a regression guard. The hand-over continues with a simulated answer, `ANSWERS.md`, in which the user gives their own numbers, recorded as "user's answer, 2026-10-24". At `3e81673` a fresh agent continued from the folder. At `e0ee116` the same executor is resumed with the answer. The step was added after the results were seen, so it goes to the user for review. H2 reads a token's source as the frame's, or as the user's answer for a token the frame left to supply.
- 2026-10-25 01: the transcript scan read HTML closing tags, such as `</div>`, in a renderer's generated markup as paths. Since `7019add` a closing tag right after `<` is read as text, and `wc -l </etc/hosts` is still flagged. The profile's probe row records both cases.
- 2026-10-25 01: at `e0ee116` the hand-over passes H1 to H4 for T2, and also for B2 on the `f401cae` renderer. The renderer from #9 already takes a sourced frame as given, so AC13 shows the candidate's frame is consumable rather than that the renderer's new "start from the frame" line changed anything. H1 to H4 are reported as regression guards. The grader noted that B2's notes cite Apple's licence only "per the brief".

## Changes after launch
