# 0009: Front-load human decisions and give the agent PR-level autonomy in product-engineering

- Status: accepted
- Date: 2026-09-25
- Supersedes: 0007

## Context

The loop from 0007 was sound in principle but hard to use. Nothing mapped work-item types (quick fix, bugfix, feature, new app, refactor) to skills. The only human gate was architecture agreement: the agent never interviewed the user, never brainstormed approaches with them, and never agreed how it would verify its own work. Verification described test design, not driving the running software. Review was one pass. Delivery was a single PR at the end that the agent never merged. A clerical worklog protocol, model-tier tables, and hedged, repeated evidence rules added ceremony without helping the user.

What changed since 0007: the owner wants human involvement concentrated at the start, and full autonomy afterwards, down to merging PRs the agent may safely merge.

## Options

1. **Patch the eight skills.** Add an interview step, a browser-verification section, and multi-agent review. Smallest diff, but the stage map, PR model, and hedged prose remain the root problems.
2. **Rebuild around one loop with human gates up front and autonomy per PR.** Clear stages, one skill per stage, PR slices as the unit of autonomy. Renames and removes skills before the first release.
3. **One large skill.** Rejected for the same reasons as in 0007: an oversized context and no focused reuse.

## Decision

Option 2. The `product-engineering` category has nine skills in one loop:

- Human gates, in order: G1 `specifying-work-items` (the agent interviews the user and writes `spec.md`), G2 `brainstorming-solutions` (two to four distinct approaches, the user picks), G3 `defining-verification` (a per-project `verification-profile.md` plus one check per acceptance criterion), G4 `planning-implementation` (`roadmap.md` with plans, phases, PR slices, predicted review categories, and the autonomy contract). Small tracks batch the gates into one message. Existing approval carries forward.
- Autonomous stages: `implementing-plans`, `verifying-implementation` (drives the running app and records observed evidence per criterion, tied to a commit SHA), `reviewing-code-changes` in quick mode (one fresh-context intent reviewer before the PR) and full mode (five parallel lenses on the PR: architecture, security, conventions and idioms, efficiency, intent), and `shipping-pull-requests` (opens one PR per slice, categorizes it, and lands it).
- `running-implementation-loops` classifies the work item into a track (quick fix, bugfix, small change, feature, new app, refactor, spike) and runs the stages that track needs.
- Every PR is `human` or `agent` category. Precedence: host protections, then the project's pull request policy, then the autonomy contract (which may tighten, and loosens only in the user's words), then skill defaults. The category is computed from the actual diff and only escalates.
- Merge policy (which diffs are safe) and merge authorization (the user letting the agent merge, recorded at G4) are separate. An agent-category PR merges only with an APPROVE verdict, required CI green on the reviewed head, a complete verification report, and recorded authorization, pinned to the reviewed head. The agent never bypasses branch protection, and treats a deploy-on-merge base as needing explicit authorization.
- Evidence lives on the PR: the verification report in the body, the review as a comment review, because an author cannot approve their own PR. `docs/product-engineering/` holds the spec, roadmap, and plans; `verification.md` and `review.md` are written only when there is no PR.
- `recording-worklogs` and `preparing-engineering-specs` are removed. Plan status lives in each plan file; live state is read from the PR host on resume. `implementing-work-packages` becomes `implementing-plans`, and `preparing-pull-requests` becomes `shipping-pull-requests`.
- Tools are described by capability, with dated example tools (Playwright MCP, Claude in Chrome, and others) in references. This is within 0002: no harness path, dependency, or install location is assumed, and a missing tool leaves a check unverified rather than substituted.

## Consequences

- Users get one table that answers which skill runs when, and are asked for decisions only at the start.
- Agents can merge low-risk PRs without waiting, so throughput depends on how well the category rules and verification contracts are written; a weak contract lets weak work merge.
- Branch protection that requires approvals blocks agent merges entirely; the skills report this and do not work around it.
- Renames and removals happen before the first release, so no installed users break, but the change is still committed as breaking under the repository convention.
- The behavioral evaluations from 0007 no longer match the skills. New trials must cover interview quality, real app driving, per-lens review recall, categorization, merge safety, and stacked PRs.
