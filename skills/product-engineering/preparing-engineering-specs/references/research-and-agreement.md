# Research and architecture agreement

## Inspect a useful boundary

Start at the changed behavior's entry point and follow relevant state, dependencies, and failure handling. Examine tests alongside code. Capture source paths and symbols, current revision, important constraints, and reproducible baseline commands. Avoid a repository-wide inventory when a bounded path answers the question.

Check whether the proposed behavior fits existing interfaces, persistence and migrations, authentication/authorization, deployment topology, observability, and UI conventions where relevant. A dependency graph is useful when relationships affect sequencing; otherwise concise prose suffices.

For an upstream design handoff, inspect both intended behavior and prototype limitations. A static success screen does not establish persistence, identity, idempotency, accessibility, or real third-party integration. Convert only agreed production behavior into engineering obligations; surface missing consequential behavior for decision.

## Use external evidence selectively

Research when an unresolved technical question changes feasibility or the plan. Prefer official documentation, source, standards, or original research. Record the URL, retrieval date, version/applicability, finding, and implication. Known solutions are options with tradeoffs, not permission to copy their architecture wholesale.

Distinguish a source's claim from your inference and a tested local observation. Conflicting or inaccessible sources leave uncertainty. Never imply an experiment ran because an example looked plausible. Do not include credentials, irrelevant private code, or whole external documents in delegated context.

For a delegated investigation, supply the exact question, relevant starting points, source expectations, scope boundary, output path, and what evidence would settle the question. Use a capable investigator for architecture synthesis; clerical extraction can use a lower tier. Report unavailable routing controls honestly.

## Decisions that need the user

Typical consequential decisions change persistent data ownership, public contracts, deployment/platform commitments, security boundaries, major dependencies, cost structure, or a product tradeoff. Show the concrete proposal before asking. Do not substitute repeated approval of routine local details for these decisions.

An existing agreed architecture can settle a choice. Explicit user delegation can settle who decides it. State the actual basis; do not label an assumption agreed. If a change would invalidate an earlier agreement, show what changed and request only the affected decision.

Separate blockers from bounded uncertainty. A missing API contract needed by two parallel packages blocks their implementation. The name of a private helper generally does not. Record small reversible details as implementation choices within the baseline instead of forcing them into architecture approval.

## Example

The product handoff says saved entries remain available after a reload, while the prototype holds them in memory. Inspect the existing storage and identity model first. If the application already has an agreed authenticated storage service, plan within it. If no storage exists, present viable persistence and identity options, their data and operational consequences, and a recommendation. The prototype's local array cannot silently become the production storage decision.
