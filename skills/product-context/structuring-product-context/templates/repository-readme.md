# [Product]: product context

<!-- Copy to README.md at the root of the product context repository. Written for people; agents start at AGENTS.md. Delete this comment. -->

[Two or three sentences: what the product is, who it is for, and where it stands: the current version and what it delivers.]

This repository holds the product's whole context in Markdown, apart from the code: why and what it is, how it is structured, why it is this way, and when and in what order it is built. The code lives in [code repository], which reads this repository at the commit each piece of work was handed over at.

## Where to start

- `product/overview.md`: the product in one page.
- `roadmap/README.md`: versions, the current focus, and the bets in flight.
- `architecture/README.md`: the structure, from the system context down.
- `decisions/README.md`: why it is this way.

## How work flows

1. Requirements live in a catalogue with permanent IDs.
2. Each version is cut into milestones, and each milestone into bets: shaped units of work with a fixed appetite, an observable outcome, and acceptance criteria.
3. A ready bet is handed to [code repository] at a pinned commit and built there.
4. When its pull requests merge, the bet is closed here: the requirements, the architecture and the indexes are brought in line with what was built.
