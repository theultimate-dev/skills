# Writing a bet

Section by section, what a bet file holds and how good text differs from weak text. A bet is read by two audiences: the user, who agrees to spend the appetite on it, and an implementing agent in another repository, which builds it from the bet and its context pack alone. Write for both.

## Header

```
# Bet 04: Pantry items survive a reload
Status: shaped
Version: V1 · Milestone: 1.1 Pantry · Appetite: M · Depends on: Bet 03
Code repository: larder · Context pinned: not yet
```

The title states the outcome. Keep the header lines exactly in this form: implementation loops find them by their labels.

## Outcome

Two to four sentences on who can now do what, and what they see. No implementation.

- Weak: "Implement the pantry CRUD endpoints and the list view."
- Better: "A household member can add, edit and remove pantry items in the web app. The list shows every item with its quantity and unit, and nothing is lost on a reload or a new session."

## Requirements

Catalogue IDs only, with `all` or `part: …`. Never copy the requirement text: it lives in `product/requirements/`, and the implementing agent reads it there at the pinned commit. A note explains a partial cover or a reading the bet relies on.

## Acceptance criteria

Each criterion is one outcome observable from outside the code: the user interface, an API response, command output, or state read back through the product. It uses concrete values, names the requirement it proves, and has one pass condition. Use Given/When/Then when order matters.

- Weak: `AC2 (PAN-02): Editing works.`
- Better: `AC2 (PAN-02): Given an item "Rice, 2 kg", when the member changes the quantity to 1 kg and reloads the page, the list shows "Rice, 1 kg".`

Every requirement in the bet has at least one criterion, and every behaviour the shaping decided, an error case or a limit, has one. Mark with a leading `~` the criteria that may be cut if the appetite runs short; cut them from the least valuable up.

Leave engineering detail open: error message wording, retry timing, the exact layout of an empty state. The implementation loop settles such detail at its own spec gate, inside the bet's boundaries, as engineering criteria in their own series, such as `AC-E1 (PAN-03)`, and reports them back when the bet closes.

## Boundaries

- **No-go**: what the bet will not do, though a reasonable reader might expect it. "No-go: barcode scanning; items are typed in." The loop treats a no-go as out of scope and stops rather than cross it.
- **Rabbit hole**: a known risk that could eat the appetite, and how the shaping patched it. "Rabbit hole: unit conversion between kilograms and cups. Patched by: quantities keep the unit the member typed; no conversion." An unpatched rabbit hole says what to do if it bites, usually "stop and reshape".
- **~ Cuttable**: scope to drop first if the appetite runs short, when it is broader than a single criterion.

## Architecture

```
- Touches: web app (architecture/components/web-app.md), sync service (architecture/components/sync-service.md)
- Consumes: architecture/contracts/sync-protocol.md, version 1.0, accepted
- Produces or changes: none
- Relies on: decisions/0004-store-pantry-items-per-household.md
```

A produced or changed contract states what the bet fixes about it, such as "adds pantry item operations: create, update, delete, with last-write-wins on update". Details the bet leaves open are settled by the implementation loop and written back into the contract when the bet closes.

## Risks and open questions

Register IDs that bear on the bet, each with one line on why. An open question that blocks the bet blocks readiness; one that does not is listed so the loop can see it.

## Context pack

The files an implementing agent reads, in order, each with why. Five to ten entries, from general to specific:

```
1. product/overview.md: what Larder is and its principles
2. product/glossary.md: household, member, item, unit
3. product/requirements/pantry.md: PAN-01 to PAN-03
4. product/requirements/non-functional.md: NFR-03
5. architecture/containers.md: where the web app and the sync service sit
6. architecture/contracts/sync-protocol.md: the operations this bet calls
7. decisions/0004-store-pantry-items-per-household.md: why items belong to a household
```

The pack is complete when an agent could build the bet without reading anything else in the context repository. It is short when every entry earns its place.

## Handoff and Outcome log

Leave both empty. `shaping-bets` writes the Handoff at handoff; `reconciling-product-context` writes the Outcome log at close.
