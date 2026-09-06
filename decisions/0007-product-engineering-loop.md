# 0007: Package engineering delivery as a verified implementation loop

- Status: accepted
- Date: 2026-09-06

## Context

Product-design discovery ends with agreed behavior, visual intent, acceptance criteria, prototype limitations, and suggested delivery slices. Engineers need a portable next stage that settles consequential architecture choices, coordinates agent implementation, and verifies the combined result before handing a PR to the user. Available agents, models, effort controls, and hosting tools differ across environments.

## Options

1. **One comprehensive implementation skill.** One invocation, but research, planning, testing, review, logging, and publication would share an oversized context and lose focused reuse.
2. **Independent engineering specialists only.** Focused capabilities, but every user must coordinate handoffs, recovery, and evidence gates themselves.
3. **One coordinator with independent specialists.** One workflow invocation plus focused reuse; requires portable task contracts and explicit fallbacks for unavailable capabilities.

## Decision

Choose option 3 as the `product-engineering` category and plugin, separate from product-design. `running-implementation-loops` coordinates seven specialists for engineering specs, implementation plans, bounded implementation, verification, review, worklogs, and pull requests.

Consequential architecture decisions are agreed with the user before autonomous implementation. Existing agreement carries forward. The loop ends with coherent commits and an open, technically ready PR awaiting human review, within the user's authorization and project rules. Merge, release, and deployment remain separate actions.

Use compact, linked artifacts for requirements, technical context, package plans, roadmap, revision-specific review and verification, and factual session history. Small work may combine sections. Verification is planned before coding, covers appropriate test layers and actual boundaries, and is repeated where repairs or integration invalidate evidence. All confirmed actionable in-scope defects are repaired; blockers and missing evidence remain visible.

Discover agents, model tiers, and effort controls at runtime rather than hardcoding names. Supply bounded task and context packets. A lowest-capable-tier recorder persists supplied facts with a minimal acknowledgment. Sequential fallback preserves evidence gates and discloses unavailable controls and reduced review independence.

## Consequences

- Users install one category and invoke one entry skill, or use any specialist with equivalent artifacts.
- Test and review evidence remains traceable to requirements and the actual candidate; a green check alone cannot establish completion.
- Independent skills repeat a small set of essential invariants to remain self-contained; detailed procedures load progressively.
- Missing host capabilities limit what can be demonstrated, even though the process can continue useful work.
- Behavioral evaluations and a runnable isolated exercise are needed alongside format validation; cross-host reliability cannot be inferred from one successful trial.
