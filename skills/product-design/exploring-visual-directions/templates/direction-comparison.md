# Visual directions: [initiative]

<!-- Lines marked "(native surface)" apply only to a native platform surface, and lines marked "(responsive page)" only to a responsive page. Keep the lines for the kind of surface this brief is for, delete the others without noting that they don't apply, and drop the markers. A brief with both kinds keeps each kind's lines in the directions for that surface. Delete this comment. -->

Status: proposals / selected / needs review

## Shared context

- Audience, task, and representative content:
- Existing constraints and inspected materials:
- Preserve / evolve / replace decision and allowed exceptions:
- Scenes and states every sketch must show:
- Surface and platform, such as a macOS menu-bar panel (native surface):

## Direction [A / B / C]: [descriptive name]

<!-- Repeat this section for each direction. -->

- Premise and audience fit:
- Composition and information hierarchy:
- Typography: roles, faces/fallbacks, sizes, weights, line heights, measure:
- Spacing: candidate scale, grouping, section rhythm, density:
- Color roles, imagery, surfaces, and motion when useful:
- Narrow-screen changes (responsive page):
- Placements and scale (native surface): what changes in each placement of the platform frame:
- Platform fit (native surface): materials, standard controls and design guidelines used, and each deliberate departure with its reason, or none:
- Concrete candidate tokens:
- Public/project references and principles adapted, if any:
- Usability tradeoffs and assumptions:
- Native risks (native surface): reading at hardware size, competing with system UI for space, and the states that must not rely on color or motion alone:
- Font or asset availability and offline rendering limitations:

## Sketch rendering request

[Render the same content/task in one offline HTML file per direction. Embed CSS and necessary assets; use minimal inline JavaScript. Describe the fidelity and questions to evaluate.]

### Platform frame (native surface)

<!-- One frame for all directions. Directions refer to it and don't repeat its values, the scale mapping included. Give each geometry token one length and a row of its own. -->

- Placements, each drawn at real scale:
- Scale mapping, for example 1 CSS px = 1 pt:
- System UI beside the surface:
- Settings to honor: appearance, contrast, transparency, motion:
- System type and symbols: the intended face and its license, embedded or rendered through `system-ui`, and the symbols drawn as stand-ins:

| Geometry token | Value | Source: document, device and date read, or "to supply" |
|---|---|---|
| | | |

## Comparison after rendering

| Criterion | A | B | C |
|---|---|---|---|
| Task clarity and hierarchy | | | |
| Typography and reading comfort | | | |
| Spacing, density, and responsiveness (responsive page) | | | |
| Spacing and density (native surface) | | | |
| Placements and scale (native surface) | | | |
| Platform fit (native surface) | | | |
| Identity and project fit | | | |
| Risks and limitations | | | |

- Recommendation and reasons:
- User selection or explicitly delegated decision:
- If combining: exact retained elements and the resulting coherent direction:
- Refinements to carry into the next prototype:
