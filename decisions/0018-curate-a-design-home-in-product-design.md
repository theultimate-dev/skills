# 0018: Curate a design home in product-design with a seventh skill

- Status: accepted
- Date: 2026-10-25

## Context

0006 ends product discovery at a refined prototype for one initiative, through five specialists and a coordinator. 0016 lets prototypes link a project's shared design files as a design tree, but nothing creates those files.

Issue #11 reported two steps that had to be improvised in one session. The first set up the project's long-lived design home, where each platform and each view has its own folder and the shared foundations sit in one place. The second graduated a chosen combination of directions into that home: its candidate tokens into shared tokens, its repeated parts into shared components, and its view's own surfaces into one stylesheet that other views link to. The layout, the naming, the rules for what goes where, and the checks were all decided on the spot.

## Options

1. **Extend `building-html-prototypes`.** No new name. Lost: that skill builds pages, and writing the foundations every page links is a second job with its own approvals.
2. **Two new skills, one to set up the home and one to graduate directions.** Their triggers are sharper. Lost: both need the same layout, rules and checks, which each skill would have to carry.
3. **One new specialist that sets up or adopts the home, keeps its rules, and graduates each chosen direction into it.** Won: setup and graduation share one layout and one set of checks.

## Decision

Option 3: `curating-design-systems` joins product-design as its seventh skill. The rest of 0006 holds: every skill works without the others installed, and the user decides at each milestone.

- **Setup and adoption.** The skill inspects what exists and proposes a layout with its reasons, then creates it only once the user agrees. The default layout is:
  - one foundations folder that every platform uses;
  - one folder per platform, mirroring the code's apps;
  - one folder per view inside its platform;
  - a README with the layout and its rules.

  When it adopts an existing folder, it moves files only after the user agrees to a mapping, and it never changes the code's theme files.
- **Four rules:**
  - foundations hold no platform styles;
  - a platform stylesheet draws only what the operating system draws;
  - a view's own surfaces are styled once, and other views link to that stylesheet;
  - pages link by relative path only, as 0016 says.
- **Graduation** runs after the user selects or combines a direction and before the pages are refined:
  - tokens move into the foundations by role, with every appearance variant the direction defines;
  - repeated parts become shared components;
  - explorations stay where they were made, with each direction's reason recorded in the direction comparison.

  A missing appearance, or a role that conflicts with the foundations, goes to the user.
- **Checks** after every change: every reference resolves inside the tree, no token is defined twice, and every page still renders as it did.
- **Out of scope:** exporting tokens to the code, which the home's README keeps as an open question; and `product-context`'s design layer, which #23 tracks.

## Consequences

- A project's design home keeps one layout and one set of rules from its first view on, and every later direction lands in it the same way.
- Discovery gains a step at Converge, between selecting a direction and refining it. The coordinator and the neighboring specialists must name it.
- Changing a foundation role changes every page that links it, so graduation asks before any such change, and the render check records what changed.
- Revisit if projects need the design home's tokens in the code's own formats, or if `product-context` gains a design-home layer (#23).
