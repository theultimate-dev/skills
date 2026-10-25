# Offline artifact contract

This contract governs the one-file artifact. It applies unless the project already keeps shared design files or the user asks for them, and direction sketches use it by default even then. A design tree follows the [design-tree contract](design-tree-contract.md) instead.

## One artifact, one file

Every one-file artifact must open through `file://` and complete its demonstrated local interactions without a network connection, server, package installation, or build step.

- Put CSS in inline `style` elements and necessary JavaScript in inline, non-importing scripts.
- Embed required images and fonts as data URLs; inline SVG is appropriate for original diagrams and icons. Use font embedding only with suitable files and redistribution permission, retaining required notices.
- Do not load remote fonts, CDN styles or scripts, sibling stylesheets, image files, iframes, or application modules. Do not use `fetch`, remote forms, imports, service workers, or external APIs for the demonstrated behavior.
- Ordinary outbound reference links may exist if useful, but they are not part of the offline task and must not be required for it. Prefer keeping research links in companion notes.
- Avoid persistence for a disposable prototype unless the task requires exploring it. File-origin storage behavior varies; local in-memory state is sufficient for many demonstrations.

When the [design-tree contract](design-tree-contract.md) applies, link the shared files rather than copying their rules into every page, and state the change of contract and its implications. Do not silently relax offline behavior because a font or image is inconvenient to embed.

## Existing styles

Respect the user's preserve/evolve/replace choice. For continuity, inspect project styles and copy the smallest coherent set of relevant tokens and rules; a design tree links the project's shared design files instead. Resolve inherited or framework-generated values into plain CSS where needed. Record source locations in companion notes so the implementer can map back later.

Do not modify the production theme as a side effect of exploration. For an intentional redesign, record what changes and which product constraints remain. Approval of a prototype does not automatically authorize migrating the existing application.

## Fonts and imagery

Prefer a small, deliberate asset set. Embedding increases file size, so avoid unnecessary weights and oversized imagery. A system font stack is an acceptable offline fallback but does not guarantee identical typography on every machine. Record the intended face, actual fallback, language coverage concerns, and any resulting fidelity limitation. A platform's system font or symbol set is embedded only when its license allows it, like any other font. When the license forbids embedding, as for Apple's SF fonts and Segoe UI, a native surface renders the font through `system-ui` and draws stand-ins for the symbols, as the [native-surface profile](native-surface-profile.md#system-type-and-symbols) describes.

Never package a locally installed commercial font merely because it can be read. When a suitable font is unavailable, preserve the offline contract, show a considered fallback, and expose the choice in the review notes. The [MDN font-face documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@font-face) explains the source and descriptor mechanisms.

Keep content and provenance notes accurate. Sample data should be fictional or explicitly provided for this use. Do not fabricate real testimonials or customer claims to make a sketch persuasive.

## Behavior boundary

Demonstrate the task with local data and make visible actions work at the agreed fidelity. A static sketch may intentionally omit downstream flows; record the omission. Avoid misleading buttons that appear to send real requests. A form simulation should provide appropriate local feedback and never transmit data.

For multiple simulated screens in one artifact, use sections and local state with deliberate focus and back behavior. Add such navigation only when the task needs it. Companion notes document simulations; they must not be needed to understand ordinary UI labels or operate the artifact.
