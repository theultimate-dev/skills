# 0016: Let HTML prototypes share files as a design tree

- Status: accepted
- Date: 2026-10-24

## Context

0006 made every prototype one offline HTML file with embedded CSS, scripts and assets. That suits disposable direction sketches. Projects that keep their designs as the source of truth hold them as a long-lived tree of pages that share `tokens.css`, `components.css` and platform styles, and reviewers often open those pages through a host. Under one file per page, the shared CSS is copied into every page and the pages drift after the first edit. The only way out, "a different portability contract" at the user's request, does not say what replaces the guarantees it gives up. Issue #9 reported this with product-design 0.1.0.

## Options

1. **One file only, shared CSS copied into each page.** No new rules. Lost: copies drift, and the project's shared files stop being the source of truth.
2. **An unnamed opt-out at the user's request.** Already in the contract. Lost: nothing states what still holds, so nothing can be checked.
3. **A second named contract, the design tree, with its own rules and checks.** Won: it keeps the offline guarantee for the tree as a whole and makes it checkable.

## Decision

Option 3. `building-html-prototypes` has two portability contracts.

- **One-file artifact**: the default, and always used for direction sketches. 0006's rule applies to it unchanged.
- **Design tree**: used when the project already keeps shared design files or the user asks for them. Every page is a full HTML document that links shared files by relative path only, with no root-absolute paths, network, build step, JavaScript modules, CSS `@import` or `fetch`. Every page opens from disk and works offline while the tree stays together. The notes list the shared files each page depends on. A static check confirms that every `href`, `src` and CSS `url()` resolves to a file inside the tree. When reviewers open the tree through a host, the tree is also checked under a nested path prefix, with an entry page at its root.

The rest of 0006 holds. Its sentence that each prototype is one offline HTML file now describes the one-file artifact.

## Consequences

- Shared foundations stay single-sourced, and hosted reviews can be checked before reviewers see them.
- A page in a tree no longer works on its own: moving it out of the tree breaks it, and a tree needs its check after every change.
- Must do: the plugin README, the coordinator's task brief, and the plugin and skill descriptions stop saying that every prototype is one file. A design-system skill (#11) can build on this contract.
- Revisit if hosts or reviewers need pages that a build step produces.
