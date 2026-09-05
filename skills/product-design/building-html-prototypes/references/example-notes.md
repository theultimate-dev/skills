# Collection example: annotation

The bundled collection is a fictional Fieldnotes screen demonstrating local topic filtering and recovery. It is an example of implementation technique, not an approved design for any real project.

## Design intent

The serif heading and reading text support a quiet editorial character; system sans-serif labels keep controls distinct. A large introductory hierarchy gives way to clearly separated guide entries. Metadata sits alongside entries at wide sizes and moves above the titles on narrow screens. A deliberately long title exercises wrapping.

The font stacks use system fonts and may render differently across machines. No font files or external assets are included. All copy is fictional example content. There is no claim of user testing or final brand suitability.

## Demonstration

- Initially show three guides. Writing returns two, Research one, and Making zero.
- The empty result explains recovery. Clear filter restores all three and moves focus to the topic select before hiding the clear button.
- A short polite status reports the result count. Native disclosures open local exercises with keyboard support.
- Filtering retains focus on the select. The page performs no requests and does not save state; reload restores the initial collection and closed disclosures.
- With JavaScript unavailable, filtering controls stay hidden and all guides and native disclosures remain usable.

The toolbar is not a search API, disclosures are not full guide navigation, and this file does not implement saved-item persistence. There is no animation, so no reduced-motion variant is needed. Production mapping and broader accessibility testing remain separate work.

## Verification targets

Open directly as a local file with network disabled. Select each topic; verify counts 2, 1, and 0, then clear and verify 3 and focus on the select. Use keyboard alone for the same sequence and open an exercise. Inspect at narrow and wide sizes, zoom to 200%, and apply text-spacing overrides to check wrapping and recovery controls. Confirm no document network requests or script errors with available browser tools.

These are repeatable checks, not a claim that a particular environment passed them. Record actual results in the consuming project's prototype notes.
