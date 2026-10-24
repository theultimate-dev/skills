# Spec: native platform surfaces in product-design, from direction briefs to handoffs

Status: agreed (G1, 2026-10-24: "Agreed")
Track: feature
Source: issue #10, https://github.com/theultimate-dev/skills/issues/10

## Problem

`exploring-visual-directions` (product-design 0.2.0) writes every direction brief for a responsive page:

- `SKILL.md:25` asks each direction for "responsive changes".
- `SKILL.md:33` selects a direction from sketches "at narrow and wide sizes".
- The template has "Narrow-screen changes" (`templates/direction-comparison.md:21`) and "Spacing, density, and responsiveness" (`:37`).
- `references/typography-and-spacing.md:25-29` covers embedding a font or falling back, and nothing else.

A native platform surface, such as the macOS menu-bar panel and settings window in the session behind the issue, has constraints of its own:

- It works only at the device's real scale.
- It sits beside the platform's own UI.
- It follows the platform's materials and conventions.
- It often uses system type and symbols that can't be embedded.

The briefs ask for none of this, so each sketch had to rediscover it, and "Narrow-screen changes" had nothing to describe.

The skills downstream use the same responsive-only wording:

- `designing-ux-flows`: "narrow layouts" (`SKILL.md:23`), "Narrow-screen behavior" (`templates/ux-specification.md:29`), and the responsive paragraph in `references/flows-and-states.md:38`.
- `preparing-implementation-handoffs`: "responsive rules" (`SKILL.md:23`, `templates/implementation-handoff.md:23`) and "responsive changes" (`references/readiness-and-traceability.md:19`).
- The coordinator's Converge row: "responsive behavior" (`guiding-product-discovery/references/workflow.md:12`).

`building-html-prototypes` 0.2.0 already draws native surfaces through its native-surface profile (#9 part 4), but no brief hands it a shared frame. Its type rule also ignores licences: "Do not embed a platform's system font file" (`references/native-surface-profile.md:45-46`; also `references/offline-artifact-contract.md:25`). Licences differ by platform:

- Apple's SF fonts can't be embedded, and SF Symbols' licence couldn't be reached to confirm.
- Microsoft's Segoe UI and Segoe Fluent Icons can't be embedded.
- Roboto (OFL 1.1) and Material Symbols (Apache 2.0) can be embedded.

Outcome: a native surface keeps its own variant from the first brief to the handoff:

- placements at real scale;
- one shared platform frame that the renderer consumes;
- platform fit;
- system type and symbols handled by their licence;
- risks specific to native surfaces.

Responsive pages keep today's guidance. The work ships as a product-design release.

## Requirements

`exploring-visual-directions` (issue #10)
- R1: The skill recognises a native platform surface from the brief and the project:
  - Signals: the brief or the project names a platform surface (a menu-bar or tray item, a window, a widget, a watch face, a TV or car screen), or the project is a native app.
  - A brief with both a responsive page and a native surface treats each surface separately.
  - When neither the brief nor the project settles it, the skill asks the user before writing the briefs.
- R2: For a native surface, each direction states placements in place of responsive changes. Placements are the display types and states the surface appears in, at real scale: for example a display with a hardware cut-out, an external display without one, and a full-screen app. The recommendation and the final selection compare the rendered sketches at real scale in each placement, in place of narrow and wide sizes.
- R3: The rendering task carries one platform frame, common to all three directions. Its fields use the terms of `building-html-prototypes`' native-surface profile:
  - the scale mapping;
  - the device geometry as tokens, each with its source, or marked for the user to supply when no source gives it;
  - the system UI the surface competes with, such as menus, status items and system bars;
  - the platform settings to honour: appearance, contrast, transparency and motion.
- R4: Each direction states how it uses the platform's materials, standard controls and design guidelines, and where it departs from them on purpose, with the reason.
- R5: When the intended face is the platform's system font, the direction says so and checks the font's licence:
  - If the licence forbids embedding, as for Apple's SF fonts and Segoe UI, the sketch renders through `system-ui`. The brief records that the font isn't embedded, and that other platforms show their own system font instead.
  - If the font is openly licensed, as Roboto is, it follows the existing embed-or-fall-back guidance.
  - The system symbol set follows the same rule. Drawn stand-ins replace symbols whose licence forbids embedding or is unconfirmed.
- R6: For a native surface, each direction's usability risks include:
  - reading at hardware size;
  - competing with system UI for space;
  - states that must not depend on colour or motion alone.
- R7: The comparison template has a native-surface variant:
  - "Placements and scale" in place of "Narrow-screen changes";
  - a "Platform fit" line;
  - the platform frame in the shared context and in the rendering request;
  - comparison rows for placements and scale in place of responsiveness.
- R8: A brief for a responsive page is unchanged. It keeps responsive changes, "Narrow-screen changes" and the narrow-and-wide comparison, and it has no platform frame.
- R9: The skill's description names native platform surfaces, so an agent picks it for native-surface directions.

`building-html-prototypes` (the hand-over)
- R10: The native-surface profile and the offline-artifact contract apply R5's licence check:
  - A system font or symbol set whose licence forbids embedding renders through `system-ui` or as drawn stand-ins, recorded as fidelity limits.
  - An openly licensed one follows the offline-artifact contract like any other font or asset.
  - The notes template records either case.
- R11: An agent following `building-html-prototypes` with a direction brief's platform frame takes these from the frame and doesn't rediscover or re-ask them:
  - the scale mapping;
  - the geometry tokens and their sources;
  - the type and symbol handling;
  - the settings.

Downstream skills
- R12: For a native surface, `designing-ux-flows` asks for placements in place of narrow-screen behavior: the display types and states the surface appears in, and what changes in each.
- R13: For a native surface, `preparing-implementation-handoffs` carries, in place of responsive rules:
  - placements and scale;
  - the platform frame: scale mapping, geometry tokens with their sources, and the settings honoured;
  - the system type and symbol fidelity limits, next to the font limitations.
- R14: The coordinator's Converge row reads "responsive behavior or, for a native surface, placements" (`guiding-product-discovery/references/workflow.md:12`).

Release
- R15: Once R1–R14 have merged, the product-design release and its marketplace release are cut with `release-process`, following AGENTS.md "Release".

## Acceptance criteria

The native, Android, responsive and ambiguous fixtures are the fictional "Harbor" briefs in `evaluations/product-design/fixtures/` (see Verification).

- AC1 (R1): `SKILL.md` covers detection:
  - the signals that mark a native surface;
  - a mixed brief treats each surface separately;
  - a brief that nothing settles means asking the user before writing any brief.
- AC2 (R1): Given the ambiguous fixture (a "backup status at a glance" view that names no platform, in a project with no app code), an agent following the skill asks which surface the view is for before writing any direction.
- AC3 (R2, R8): Given the native fixture (Harbor's macOS menu-bar panel and settings window), each direction lists placements at real scale. They include a display with a hardware cut-out, an external display without one, and a full-screen app. No direction has a narrow-screen or responsive-changes entry.
- AC4 (R3): In the same trial, the rendering task holds one platform frame for all three directions, with:
  - a scale mapping;
  - geometry tokens, each with a source or marked for the user to supply;
  - the system UI the panel competes with, naming the menu bar and status items;
  - the four settings: appearance, contrast, transparency and motion.
- AC5 (R4): In the same trial, each direction names the platform materials, standard controls and design guidelines it uses. It names at least one deliberate departure with its reason, or states that it has none.
- AC6 (R5):
  - In the native trial, the briefs name the macOS system font as the intended face and render it through `system-ui`. They record that it isn't embedded and that other platforms show their own system font. System symbols are drawn stand-ins, recorded as a limit.
  - Given the Android fixture (Harbor's home-screen widget), the briefs record Roboto as openly licensed and follow embed-or-fall-back. They don't record it as impossible to embed.
- AC7 (R6): In the native trial, each direction's risks include reading at hardware size, competing with system UI for space, and at least one state that must not depend on colour or motion alone.
- AC8 (R7): The template has the native variant described in R7. The native trial's filled comparison contains "Placements and scale" and does not contain "Narrow-screen changes".
- AC9 (R8): Given the responsive fixture (Harbor's web dashboard in a browser), each direction has narrow-screen changes, and the briefs have no platform frame, placements or platform fit.
- AC10 (R2): `SKILL.md` says that, for a native surface, the final selection compares the rendered sketches at real scale in each placement.
- AC11 (R9): The skill's description names native platform surfaces, stays one line, and is under 1024 characters.
- AC12 (R10):
  - The profile's "System type and symbols" section and the contract's "Fonts and imagery" state the licence check: forbidden means `system-ui` or drawn stand-ins as fidelity limits; openly licensed means the offline-artifact contract.
  - The notes template's type and symbol lines fit both cases.
  - No line in `building-html-prototypes` still says a system font is never embedded.
- AC13 (R3, R11): Given the native trial's rendering task, an agent following `building-html-prototypes` renders one direction:
  - Its notes' "Native surface" section carries the frame's scale mapping, each geometry token with the frame's source, the type and symbol limits, and the frame's settings.
  - The scene's CSS defines the frame's geometry tokens as custom properties.
  - The settings control sits outside the scenes.
  - The agent asks for no value the frame supplied.
- AC14 (R12): `designing-ux-flows` covers placements:
  - Its `SKILL.md`, UX template and `flows-and-states.md` name placements for a native surface.
  - Given the native fixture, an agent following it writes a UX specification with "Placements" naming the three placements, and no "Narrow-screen behavior".
  - Given the responsive fixture, the specification keeps "Narrow-screen behavior".
- AC15 (R13): `preparing-implementation-handoffs` carries the native variant:
  - Its `SKILL.md`, readiness reference and template name the variant in R13.
  - Given the native direction brief and prototype notes from the AC3 and AC13 trials, an agent following it writes a handoff whose "Selected design" carries the scale mapping, the geometry sources, the settings, and the type and symbol limits, and no responsive rules for the native surface.
- AC16 (R14): `workflow.md:12` reads "responsive behavior or, for a native surface, placements".
- AC17 (R15): The release is published:
  - `marketplace.json` gives product-design and the marketplace the versions `release-process` computed.
  - Both changelogs carry dated sections, and the root lists the plugin release under Changed.
  - The release PR merged with a merge commit.
  - Both tags sit on the release commit, and the release workflow published both GitHub releases.

## Non-goals

- Device geometry tables for specific platforms. The skills ship no device values, as the profile already says.
- Settings beyond the four, such as larger text sizes (Dynamic Type). Reading at hardware size is covered as a risk.
- Changing the one-file default for direction sketches (`direction-comparison.md:29`).
- Rendering changes in `building-html-prototypes` beyond R10's licence rule.
- `shaping-product-briefs`, which has no layout content.
- Platform UI kits, design tools or SDKs.

## Constraints

- Skill format (AGENTS.md):
  - Links stay inside the skill directory, and `scripts/validate.py:65` bans `../`.
  - Nothing assumes a harness, install path or environment variable.
  - Each `SKILL.md` stays under 500 lines. Today: 35 for `exploring-visual-directions`, 33 for `designing-ux-flows`, 35 for `preparing-implementation-handoffs`, 52 for `building-html-prototypes`.
  - Depth goes in `references/`.
  - The frontmatter keeps three single-line fields, with the description under 1024 characters.
- Decision 0006: the skills are stack-neutral and self-contained, and "accept equivalent artifacts without another skill installed". So the frame is plain content in the rendering task, and `exploring-visual-directions` names `building-html-prototypes` only as an optional renderer (`SKILL.md:31`).
- Licence facts, retrieved 2026-10-24:
  - Apple fonts: "You may not embed the Apple Font in any software programs or other products" (https://developer.apple.com/fonts/).
  - SF Symbols: the licence text was unreachable, so treat it as not embeddable.
  - Windows fonts: "you may not redistribute the Windows fonts" (https://learn.microsoft.com/en-us/typography/fonts/font-faq).
  - Segoe Fluent Icons: "you may not ship it to another platform" (https://learn.microsoft.com/en-us/windows/apps/design/iconography/segoe-fluent-icons-font).
  - Roboto: SIL OFL 1.1 (https://github.com/google/fonts/blob/main/ofl/roboto/OFL.txt).
  - Material Symbols: Apache 2.0 (https://developers.google.com/fonts/docs/material_symbols).
  - `system-ui`: "Glyphs are taken from the default user interface font on a given platform" (https://developer.mozilla.org/en-US/docs/Web/CSS/font-family).
- Changelogs: each content slice adds a user-facing entry under `[Unreleased]` in `skills/product-design/CHANGELOG.md`. New evaluation fixtures add a root `CHANGELOG.md` line. The release slice follows AGENTS.md "Release":
  - one `chore(release): …` commit touching only changelogs and versions;
  - its PR merged with a merge commit;
  - then the plugin tag, then the marketplace tag, pushed on that commit by name.
- Commits follow Conventional Commits: imperative, lowercase, no trailing period, scoped to the skill or category, with no AI attribution.
- Done and review: done means slices 1 and 2 have merged with the validator passing, and the release is published. The user reviews and merges every PR in this work item ("The PR, and I merge it (Recommended)", G1, 2026-10-24).

## Assumptions and open questions

- Assumption: wording is platform-neutral, with examples from macOS, iOS, watchOS, TV and car displays (from the issue), plus Windows and Android. Basis: decision 0006, "Skills are stack-neutral". If wrong: Apple-only wording.
- Assumption: the frame carries the four settings from the issue and the profile. Basis: not asked; the issue and #9's R15 both name four. If wrong: a fifth setting in the frame, the profile and the notes template.
- Assumption: a geometry value with no source is marked for the user to supply, matching the profile's "When no source gives a value, ask the user". Basis: inferred from `native-surface-profile.md`. If wrong: the skill ships sourced values.
- Assumption: SF Symbols get drawn stand-ins. Basis: the licence text was unreachable on 2026-10-24, and a forum quote restricts use to Apple-platform UIs. If wrong: no change, because stand-ins are always safe.
- Open: none.

## Approach

Chosen: A, route, reference and one marked template. Agreed at G2, 2026-10-24: "A: route + reference + one template (Recommended)"

How it works:

- **`exploring-visual-directions/SKILL.md`** gains a short "identify the surface" paragraph under "Ground the exploration", covering the signals, a mixed brief, and asking when the brief is unclear. It adds native wording in four places: the per-direction list (placements, platform fit), the rendering task (one platform frame) and the selection (real scale in each placement). It links a new `references/native-surfaces.md`.
- **`references/native-surfaces.md`** (new) holds the depth:
  - signals and examples across platforms;
  - placements;
  - the platform frame's fields, in the native-surface profile's terms;
  - platform fit;
  - system type and symbols, checked by licence;
  - native risks;
  - a short fictional example.
- **`references/typography-and-spacing.md`** gains a paragraph on platform system fonts and symbols with the licence check.
- **The comparison template** stays one file with marked native lines, mirroring `building-html-prototypes/templates/prototype-notes.md:18-30`.
- **`building-html-prototypes`** applies the licence check in the profile's "System type and symbols" and in the contract's "Fonts and imagery". The profile adds: start from a brief's platform frame and ask only for what it lacks. The notes template's type and symbol lines cover both cases.
- **Downstream:** `designing-ux-flows` and `preparing-implementation-handoffs` each get inline variant lines in `SKILL.md`, one reference paragraph and their template. The coordinator's Converge row gains six words: "or, for a native surface, placements".

- Touches:
  - Slice 1:
    - `skills/product-design/exploring-visual-directions/`: `SKILL.md`, new `references/native-surfaces.md`, `references/typography-and-spacing.md`, `references/inspiration-and-critique.md`, `templates/direction-comparison.md`.
    - `skills/product-design/building-html-prototypes/`: `references/native-surface-profile.md`, `references/offline-artifact-contract.md`, `templates/prototype-notes.md`.
    - `evaluations/product-design/`: `README.md` and the new Harbor fixtures.
    - Both changelogs.
  - Slice 2:
    - `skills/product-design/designing-ux-flows/`: `SKILL.md`, `references/flows-and-states.md`, `templates/ux-specification.md`.
    - `skills/product-design/preparing-implementation-handoffs/`: `SKILL.md`, `references/readiness-and-traceability.md`, `templates/implementation-handoff.md`.
    - `skills/product-design/guiding-product-discovery/references/workflow.md`.
    - `evaluations/product-design/`.
    - `skills/product-design/CHANGELOG.md`.
  - Slice 3: both changelogs and `.claude-plugin/marketplace.json`.
- Reuses:
  - #9's native-variant pattern: the routing sentence in `building-html-prototypes/SKILL.md:36`, a reference for depth, and the marked section in `templates/prototype-notes.md:18-30`.
  - The profile's field names.
  - The "Agent trials" format in `evaluations/product-design/README.md`.
  - `release-process` in its independent-versions mode.
- Contracts:
  - **Platform frame.** `exploring-visual-directions` produces it, `building-html-prototypes` consumes it and `preparing-implementation-handoffs` carries it forward. Each skill states it in its own words, because skills are self-contained (decision 0006). Slice 1 owns it. Its fields match the notes template's "Native surface" section, so a renderer copies them straight across:
    - Placements;
    - Scale mapping, for example 1 CSS px = 1 pt;
    - Geometry tokens: Token | Value | Source (document, device, date read), or "to supply";
    - System UI beside the surface;
    - Settings to honour: appearance, contrast, transparency, motion;
    - System type and symbols: the intended face, its licence, embedded or `system-ui`, and the symbol stand-ins.
  - **Template markers.** A line for one kind of surface only ends in "(native surface)" or "(responsive page)". A comment at the top says to delete the other kind's lines. Slice 2's templates reuse the convention.
- Evidence:
  - The code at `building-html-prototypes/SKILL.md:36`, `references/native-surface-profile.md:43-47`, `references/offline-artifact-contract.md:25` and `templates/prototype-notes.md:18-30`.
  - Decision 0006 (self-contained, stack-neutral). No decision record fixes the system-font rule: `grep -i "system font" decisions/` finds nothing.
  - The licence sources under Constraints, retrieved 2026-10-24.

Rejected alternatives:

- B, a separate native template: two templates that share most rows drift apart, and it departs from #9's one-template pattern.
- C, everything inline: it grows `SKILL.md` to about 75 lines that every responsive run loads, against "Depth goes in `references/`" in AGENTS.md.

Consequences:

- Easier: one template and one reference per concern. The frame reads the same in the brief, the prototype notes and the handoff.
- Harder: three skills restate the frame's fields, so a later change to the frame touches all three.
- Risk: an agent keeps both marked variant lines in a filled brief. AC8 and AC9 expose it in the first trial.
- Revisit if: AC8 or AC9 still fails on kept variant lines after a repair. That points to B.
- Decision record: none, because the choice isn't consequential.

## Verification

Profile: `docs/product-engineering/verification-profile.md`, re-confirmed at f401cae (slice 1 updates it: see Harness gaps)
G3: agreed 2026-10-24, "Agreed"

N = 3 ("3 on core trials, 1 elsewhere (Recommended)").

Fixtures live in `evaluations/product-design/fixtures/`. They are invented, local only, and each `README.md` holds a product brief with no task:

| ID | Folder | What it holds |
|---|---|---|
| F-mac | `harbor-menu-bar/` | macOS menu-bar panel and settings window. No placements named. "No visual language yet; nothing to preserve" |
| F-droid | `harbor-android-widget/` | Android home-screen widget and its configuration screen |
| F-web | `harbor-web-dashboard/` | A responsive web dashboard, with a `package.json` |
| F-amb | `harbor-status-unclear/` | "Backup status at a glance". No platform, no code |
| F-code | `harbor-status-app/` | The F-amb brief plus a `Package.swift` whose app uses `MenuBarExtra` |
| F-mix | `harbor-mixed/` | A macOS menu-bar panel plus a web account page |
| F-handoff | `harbor-handoff-inputs/` (slice 2) | A selected direction, frozen from a passing T1 run, and prototype notes from the passing T2 run |

Each trial runs one skill on one fixture in its own scratch folder, `<run>`:

1. The coordinator stages the skill at the candidate SHA with `git -C <worktree> archive <sha> <skill dir>` into `<run>/skill/`, and the fixture into `<run>/project/`.
2. A fresh executor gets only `<run>` and a fixed task text. The task texts are listed in `evaluations/product-design/README.md`. Each ends: "No network access and no user: if the skill tells you to ask the user, write the question, its options and your recommendation to `QUESTIONS.md`, and stop."
3. The executor's transcript is scanned for any tool call that reaches outside `<run>`, and for any Skill, Agent or web tool call: the installed product-design plugin is the f401cae text, so loading it would grade the baseline. Either voids the run, which is recorded as a tool error.
4. A baseline is the same trial on the skill at f401cae.
5. Graders are fresh agents. For each fixture, a grader sees that fixture's candidate and baseline outputs under random IDs, plus the rubric, and nothing else. It answers yes or no per criterion. Each yes carries an exact quote with `file:line`, and the grader tries to refute every yes.
6. The coordinator then runs `grep -F` on every quote in its file. A quote that isn't found voids the grade, and a fresh grader re-grades.

"Cold read" (CR): a fresh agent gets only the candidate skill directory and a list of questions. Each answer must cite a `file:line`, and the verifier opens every cited line.

Replicates: N runs per core trial (T1, T-web, T-amb, T-ux, T4), and one run for every other trial and baseline. A row passes only if every replicate passes. No runs are added after the results are seen.

| AC | Check | Layer | Tool | Steps | Pass condition |
|---|---|---|---|---|---|
| AC1 (R1) | Detection rules, read cold, and the mixed brief | ai-eval | CR (Haiku), T-mix (Sonnet), grader (Sonnet) | 1. CR: what marks a native surface, what a mixed brief does, what happens when nothing settles the question. 2. T-mix: `exploring-visual-directions` × F-mix | 1. Three answers, each citing a line of `SKILL.md`. 2. The panel's directions have placements and a platform frame. The web page's directions have narrow-screen changes. There is no `QUESTIONS.md` |
| AC2 (R1) | Ask only when unclear | ai-eval | T-amb ×N, T-code, B-amb (Sonnet), grader | 1. T-amb on F-amb. 2. T-code on F-code. 3. Controls: the `QUESTIONS.md` files of T1, T-web, T-droid and T-mix | 1. Every T-amb run stops with a `QUESTIONS.md` asking which surface the view is for, offering a responsive page and a native surface or two platforms, and with no direction file written. 2. T-code writes directions for a macOS menu-bar panel and asks no surface question. 3. No control asks which surface. B-amb is expected to fail (1) |
| AC3 (R2, R8) | Placements in place of responsive changes | ai-eval, cli | T1 ×N, B1, grader, `grep` | 1. T1: `exploring-visual-directions` × F-mac. 2. `grep -inE "narrow-screen\|responsive change\|breakpoint"` on the direction files | 1. In every run, each of the three directions lists placements at real scale, including a display with a hardware cut-out, an external display without one, and a full-screen app. 2. No output. B1 fails (1) |
| AC4 (R3) | One shared platform frame | ai-eval, cli | T1 ×N, grader, `grep -c` | Count the frame blocks; grade their fields | Exactly one frame, in the rendering task. It holds a scale mapping, a geometry table whose every row has a source or "to supply", system UI naming the menu bar and status items, and the four settings. No direction restates other frame values |
| AC5 (R4) | Platform fit | ai-eval | T1 ×N, grader | Grade each direction | Each direction names the materials, standard controls and guidelines it uses, and at least one departure with its reason, or "none" |
| AC6 (R5) | Type and symbols by licence | ai-eval, cli | T1 ×N, T-droid, B-droid, grader, `grep` | 1. Grade T1. 2. T-droid: `exploring-visual-directions` × F-droid. 3. `grep -inE "can.?t be embedded\|cannot be embedded\|never embedded\|not embeddable"` on the T-droid output | 1. The macOS system font is named, rendered through `system-ui`, and recorded as not embedded, noting that other platforms show their own font. Symbols are drawn stand-ins. 2. Roboto is recorded as openly licensed, with the licence named, and handled by embed-or-fall-back. 3. No matching line concerns Roboto or Material Symbols |
| AC7 (R6) | Native risks | ai-eval | T1 ×N, grader | Grade each direction | Each direction lists reading at hardware size, competing with system UI for space, and at least one state that must not rely on colour or motion alone |
| AC8 (R7) | Template variant | cli | `grep` | 1. `grep -n` for "Placements and scale (native surface)", "Platform fit (native surface)" and "Narrow-screen changes (responsive page)" in `templates/direction-comparison.md`. 2. `grep -c` in every T1 comparison | 1. Each phrase is found. 2. "Placements and scale" ≥ 1 and "Narrow-screen changes" = 0 in every run |
| AC9 (R8) | Responsive unchanged | ai-eval, cli | T-web ×N, grader, `grep`, `git diff` | 1. T-web: `exploring-visual-directions` × F-web. 2. `grep -inE "platform frame\|placements\|platform fit"` on the outputs. 3. `git diff origin/main -- …/templates/direction-comparison.md` | 1. Every direction in every run has narrow-screen changes. 2. No output. 3. No responsive line is removed; responsive lines only gain the "(responsive page)" marker |
| AC10 (R2) | Selection at real scale | ai-eval | CR (Haiku) | Ask: how is the final direction chosen for a native surface? | "At real scale in each placement", citing `SKILL.md` |
| AC11 (R9) | Description | cli | validator, `python3` | 1. `python3 scripts/validate.py`. 2. Print the description's length and line count from the frontmatter | 1. "0 errors". 2. One line, under 1024 characters, containing "native" |
| AC12 (R10) | Licence rule in the renderer | cli, ai-eval | `git grep`, CR (Haiku) | 1. `git grep -niE "never embedded\|do not embed a platform's system font" -- skills/product-design`. 2. `grep` for the licence check in the profile and the contract. 3. CR: where and how does the renderer record Roboto embedded, and a macOS font through `system-ui`? 4. Fault: run step 1 on a scratch copy with profile line 45 restored from f401cae | 1. No output. 2. Hits in both files. 3. Both cases cite the notes template's type line. 4. Step 1 now hits |
| AC13 (R3, R11) | Hand-over to `building-html-prototypes` | ai-eval, e2e | T2 (Sonnet), B2, grader, headless Chrome with `interaction-harness.html` | 1. T2: `building-html-prototypes` × T1 run 1's output, "render direction A". 2. Stage T2's output at `a/b/` with a generated checks file: every frame geometry token resolves to a non-empty computed value, plus "no page scroll at 320". 3. The grader compares the notes and HTML with the frame. 4. Fault: delete one token from the scene CSS and rerun step 2 | 1. Done, with no `QUESTIONS.md` entry asking for a value the frame supplied. 2. `DONE n/n`. 3. The notes' "Native surface" section carries the scale mapping, every token with the frame's source word for word, the type and symbol limits, and the four settings. The settings control is outside every scene. 4. `FAIL` naming the token |
| AC14 (R12) | UX flows variant | ai-eval | CR (Haiku), T-ux ×N, T-ux-web, B-ux (Sonnet), grader | 1. CR on `designing-ux-flows`. 2. T-ux: `designing-ux-flows` × F-mac. 3. T-ux-web: × F-web | 1. Placements for a native surface, citing `SKILL.md`, the template and `flows-and-states.md`. 2. "Placements" names the three placements, and there is no "Narrow-screen behavior". 3. "Narrow-screen behavior" is kept. B-ux fails (2) |
| AC15 (R13) | Handoff variant | ai-eval | CR (Haiku), T4 ×N, B4 (Sonnet), grader | 1. CR on `preparing-implementation-handoffs`. 2. T4: × F-handoff | 1. The variant is cited in `SKILL.md`, the readiness reference and the template. 2. "Selected design" carries the scale mapping, geometry sources, the settings, and the type and symbol limits, with no responsive rules for the native surface. B4 fails (2) |
| AC16 (R14) | Coordinator row | cli | `sed` | `sed -n 12p skills/product-design/guiding-product-discovery/references/workflow.md` | Contains "responsive behavior or, for a native surface, placements" |
| AC17 (R15) | Release published | cli | `gh`, `git`, `jq` | After the user merges the release PR and says yes to the tags: 1. `gh pr view <n> --json state,mergeCommit` and `git rev-list --parents -n1 <merge>`. 2. `git rev-list -n1` for both tags. 3. `jq` the versions in `marketplace.json`, and read both changelog headings. 4. `gh run list --workflow release.yml`. 5. `gh release view` for both tags | 1. Merged, with a two-parent merge commit. 2. Both tags point at the release commit. 3. The versions equal the dated headings. 4. Both runs succeeded. 5. Both releases exist |
| All slices | Wording, voice, design soundness | visual | user (human eye) | The PR diff, and T2's scene screenshots at device scale factors 1 and 2 | The user approves each PR |

### Automated checks

These run on every candidate SHA in the worktree. The baseline at f401cae in a clean tree is "0 errors, 0 warnings". The main checkout shows 1 error from the ignored file `skills/product-context/default.profraw`, which is not part of any tree.

- `python3 scripts/validate.py`: "0 errors, 0 warnings"
- `git diff --check origin/main...HEAD`: no output
- `wc -l` of every changed `SKILL.md`: under 500

### Who certifies

- The agent self-certifies:
  - every cli and e2e row;
  - every ai-eval row whose grader passed calibration and whose baseline result is reported;
  - AC17's published state.
- Human eye, reported as `blocked (human eye)`:
  - wording and voice;
  - whether the native design advice is sound;
  - T2's screenshots;
  - any rubric change made after results were seen;
  - any row labelled "regression guard" because its baseline also passed.

### Environments and limits

- Allowed: local only. That means this worktree, scratch folders, `127.0.0.1` servers and headless Chrome. Executors get no network.
- Never: during verification, no push, tag, merge or release. Tags wait for the user's yes.
- Data: delete only the scratch folders the run created, and stop every server it started.

### Mocks and what they exclude

- The invented fixtures exclude the variety of real briefs and codebases.
- `QUESTIONS.md` simulates the user, so how an agent continues after the user's answer isn't covered.
- Sonnet executors stand in for the Opus sessions that usually run these skills.
- A staged skill copy stands in for plugin loading, so description-based triggering isn't covered. AC11 checks the description text only.
- Executors run inside this session, so the repository's AGENTS.md and the session's environment reach them. Neither holds any of the changed skill text, and the transcript scan catches any read of it.

### Harness gaps

- No Plan 0. G3 was agreed on 2026-10-24: "Agreed", with "3 on core trials, 1 elsewhere (Recommended)", "Staged copies outside checkouts (Recommended)" and "Commit them (Recommended)". Slice 1 updates the profile:
  - "Confirmed" moves to f401cae.
  - The agent-trial row becomes "Opus, Sonnet or Haiku", run on a staged skill copy outside any checkout.
  - It gains a row for scanning a sub-agent transcript for file paths.
- "How to verify" pointer: declined 2026-10-24 on #9 ("Not now (Recommended)"), carried forward.
