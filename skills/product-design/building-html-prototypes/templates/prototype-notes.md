# Prototype notes: [initiative / direction]

- Artifact filename, or the tree's root folder and entry page:
- Contract: one-file artifact / design tree
- Fidelity: direction sketch / refined prototype / bounded experiment
- Purpose and user task:
- Related requirements and UX specification:
- Direction status: proposed / selected / needs review

## Shared files (design tree)

List every page in the tree, including pages that no link reaches yet, and the shared files each one links.

| Page | Shared files it links |
|---|---|
| | |

## Native surface (fixed-scale scenes)

For a native surface drawn as fixed-scale scenes, as the native-surface profile describes.

- Surfaces and platform:
- Scale mapping, for example 1 CSS px = 1 pt:
- Type fidelity limit: the font the scenes render through `system-ui` on the machines reviewers use:
- Symbol fidelity limit: the system symbols drawn as stand-ins:
- Settings the platform has, the ones the scenes show, and how each was checked:

| Geometry token | Value | Source: document, device and date read, or the user's answer |
|---|---|---|
| | | |

## Design decisions

- Composition and information priority:
- Typography, actual fonts/fallbacks, and fidelity limitations:
- Spacing, density, and responsive behavior:
- Existing style/token sources and preserve/evolve/replace decision:
- Asset provenance and notices:

## Demonstrated behavior

- Starting state and sample content:
- Primary actions and expected results:
- Recovery states:
- Simulations and omitted behavior:
- State reset behavior:

## Verification

| Check | Result: passed / failed / not performed | Evidence and conditions |
|---|---|---|
| Design-tree check (`tree-check.html`), for a design tree | | |
| Direct file opening and offline behavior | | |
| Hosted render under a nested prefix (`/a/b/`), through the entry page, for an artifact reviewed through a host | | |
| Hosted render on the review host: "not performed" when you cannot open the host; ask the user to confirm it, and record their answer here | | |
| Primary task and recovery | | |
| Scripted: [check name], one row per check, for example "Scripted: panel closes on Escape and focus returns to its control" | | |
| Driven: [check name], one row per check exercised with a browser-driving tool | | |
| Keyboard and focus | | |
| Narrow and wide layouts | | |
| Native scenes at device scale factors 1 and 2 | | |
| Native scenes in a 320 CSS px frame: no page scroll, and each scene scrolls in its own container | | |
| Long-page slices (`page-slices.html`): frame size and offsets, for a long page | | |
| Zoom and text-spacing overrides | | |
| Contrast and reduced motion, if applicable | | |

## Review decision

- Observations and recommendation:
- User feedback and resulting changes:
- Unresolved questions or limitations:
- Next refinement or handoff:
