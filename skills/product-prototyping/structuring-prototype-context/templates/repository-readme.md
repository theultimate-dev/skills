# [Product]: prototype context

<!-- Copy to context/README.md. Written for people; agents start at AGENTS.md. Delete this comment. -->

[Two or three sentences: what the product is, who it is for, and where it stands: what is built and what is being tried.]

This folder holds the product's context in Markdown beside its code: why and what it is, how it is structured, why it is this way, and which ideas have been tried. The code and the changelog sit outside it, in the same repository.

## Where to start

- `product/overview.md`: the product in one page.
- `bets/README.md`: the bets, built, kept and removed.
- `architecture/README.md`: the structure, from the system context down.
- `decisions/README.md`: why it is this way, and when this context moves to a fuller profile.

## How work flows

1. An idea is framed in a dated research note that ends in a verdict: shape, park or stop.
2. A framed idea becomes one bet: an observable outcome, a small appetite, acceptance checks and a keep-or-remove signal. You approve it, and the commit it was approved at is recorded.
3. The bet is built and checked against its acceptance checks, and an independent reviewer compares the result with the bet's intent.
4. You try it and decide: keep it, and the requirements, architecture and decisions are brought in line; or remove it, and its code is reverted and the lesson recorded.
