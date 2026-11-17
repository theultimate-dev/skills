# Roadmap: software-architecture, a plugin of five skills for working on the architecture of long-lived applications

Spec: `spec.md` · Track: feature · Approved at G4: 2026-11-17, "G4 approved, 1a, Firefox opened once"

## Autonomy contract

The user's own words, quoted. The agent never edits this section, and quotes its authorization lines verbatim on resume and before any merge. A change is appended under "Changes" with its date and the user's new words, in the main checkout; `implementing-plans` commits it with the next PR slice. An unanswered field means not authorized. Use the narrowest reading of the user's words: a slice not clearly covered stays `human`. Push does not imply force-push.

Detected on 2026-11-17 at 396ba72:
- Host: GitHub via `gh`, repository `theultimate-dev/skills`.
- Base branch protection on `main`: a pull request is required, with 0 approving reviews; code-owner review is not required; the required check is `validate`; no merge queue; linear history is not required; deletion and non-fast-forward pushes are blocked.
- Merge settings: merge, squash and rebase are all allowed. The habit is merge commits (#17 to #30), and `AGENTS.md` prescribes a merge commit for a pull request that carries a release commit.
- CODEOWNERS: none. Pull request policy: `AGENTS.md` "Conduct" and "Release".
- Deploy on merge: no. `validate.yml` runs on every push and pull request; `release.yml` runs on tags or by hand.

Authorization, given at G4 on 2026-11-17.

Igor's session prompt of 2026-11-17 stated the contract he intended to approve: "commit on the branch, push it, open the pull request, and push the release tags after I confirm the merge; the pull request is categorized `human` and I merge it myself; agents merge nothing." At G4 the orchestrator described the contract as: "Commit and push: commit on `feat/software-architecture` and push it. Open PRs: the one pull request. Push release tags: after you confirm the merge. Merge: agents merge nothing; the pull request is `human` and you merge it with a merge commit. Force-push: not needed and not requested. Open issues: not requested. Stop and ask when: the loop's escalation triggers, plus any finding that contradicts the agreed spec." Igor answered: "G4 approved, 1a, Firefox opened once".

- Commit and push: "commit on the branch, push it" (session prompt), approved with "G4 approved"
- Force-push own PR branches after a rebase: not authorized
- Open PRs: "open the pull request" (session prompt), approved with "G4 approved"
- Open issues (deferred should-fix findings and follow-ups): not authorized
- Merge `agent`-category PRs: not authorized: "agents merge nothing"
- Merge method: merge: "I review and merge with a merge commit" (session prompt)
- Base branch: `main` (a detected fact, not a permission)
- Deploy-on-merge detected: no
- Human-review categories: the project policy and the skill defaults, plus "the pull request is categorized `human`". UI and visual changes: `human`
- Who merges a `human` PR after approval: the user: "I merge it myself"
- Push release tags: "push the release tags after I confirm the merge" (session prompt), approved with "G4 approved". Only after Igor says the pull request is merged
- Scope: this work item's one PR slice, into `main`
- Stop and ask when: the escalation triggers, plus "Where you believe it is wrong, or an implementation finding contradicts it, stop on that point and bring it to me with your recommendation, and keep working on everything the answer does not block." (session prompt)

Changes:

## Plans

| Plan | Phases | PR slices | Predicted category | Depends on |
|---|---|---|---|---|
| `plans/01-software-architecture-plugin.md` | p1: planning files and decision 0022; p2: `drawing-architecture-views` with the HTML template and the category scaffold; p3: `recovering-built-architecture` and `evaluating-architecture-risks`; p4: `exploring-architecture-options` and `simplifying-system-architecture`; p5: changes outside the category; p6: the release commit | whole plan: one pull request | `human`: Igor reviews and merges it himself (session prompt, 2026-11-17). It also changes `scripts/validate.py`, adds a decision record, and ships a user-visible HTML template | none |

## Order and parallelism

- Start now: p1, then p2.
- In parallel, each in its own worktree and local branch off `feat/software-architecture`: in p3 the two skills; in p4 the two skills. Each worker owns one skill directory and nothing else. The orchestrator integrates each branch into `feat/software-architecture` by rebasing it, which keeps one linear history; these worker branches are local and are never pushed.
- Contracts settled before their consumers start: the view format (`templates/view.md`, `references/view-conventions.md`) and the HTML template in p2, before any other skill is written; the scenario intake (`references/scenario-intake.md`) in p3 with `evaluating-architecture-risks`, before p4.
- Critical path: p1 → p2 → p3 → p4 → p5 → stages 6 to 9 → p6.
- `human` slices: the one pull request, opened after stage 7.
- Shared files and their owner: `.claude-plugin/marketplace.json`, `README.md`, `CHANGELOG.md`, `skills/software-architecture/CHANGELOG.md`, `scripts/validate.py` (`MIRRORS`) and every mirrored copy are written by the orchestrator when it integrates a phase, never by a parallel worker.
- Planning files: `spec.md`, `roadmap.md`, the changed `verification-profile.md` and the plan file are committed in p1.
- "How to verify" pointer in `AGENTS.md`: not requested.

## Decisions

- 2026-11-17 One PR slice with six phases, as Igor asked (D18 and the session prompt). The pull request fails the "one sitting" test on purpose: Igor reads an HTML overview instead of the diff.
- 2026-11-17 The HTML template is phase 2, directly after the decision record, because it carries the most risk and the other skills describe it. Its browser checks (AC7 to AC15, AC17) and the GitHub label check (AC18) run when the phase ends, on a page built from the fixture's sample views, so a finding that contradicts the agreed spec surfaces before four skills are written around it.
- 2026-11-17 The agent trials T1 to T11 run once at stage 6 on the branch head, and only the affected trials run again after a repair. Each phase's worker checks its own skill against the validator and against the fixture by reading, not by a graded trial.
- 2026-11-17 The category scaffold (plugin changelog, marketplace entry, README row) lands in p2 with the first skill, because the validator requires each of them as soon as a skill exists. Later phases add their skill to the same three files.
- 2026-11-17 Stages 7 and 9 run from the orchestrator. The quick review and the full review are done by agents that wrote none of the work; at least the review of the HTML template and the intent lens run on another vendor's model.
- 2026-11-17 The release commit is p6: it is written only after the full review approves, touches only changelogs and versions, and gets a delta review. Tags are pushed after Igor confirms the merge.
- 2026-11-17 Cross-vendor review of this roadmap by Codex (gpt-6.1-sol, high effort), which wrote none of it: 2 blocking, 14 should-fix, 1 nit; all resolved in the plan and the spec before G4. Blocking: the contract could not pass on one head, because AC35 needs the release commit and AC34 needs `[Unreleased]` (now two checkpoints); and the release workflow's "tag is on main" check cannot run before a tag exists (now named as post-merge, with the checks that can be replayed listed). Should-fix, in short: the overview, handover and tag steps had no task or criterion (AC37 and a plan section); parallel workers cannot pass the full validator inside their own directory (scoped checks, full validator at integration); the name check skipped the widely installed packs (done: none of the five in ten packs); the quoting exception was an assumption instead of a question to Igor (asked at G4, with browser evidence); AC18 could pass without `<b>` and `<br/>` (now required; probed); the trial pass conditions for the intake, recovering, evaluating, exploring and simplifying left agreed outputs unobserved (rubrics added, with trials T10 for a new system and T11 for a standing view in a prototype context); the reference files were checked for presence only (content topics added to R30 and AC3); the catalog check skipped `license`, `homepage` and `keywords`; Firefox was called closed while its probe fails (reopened). Nit: two rows shared AC28 (the second is AC36).
- 2026-11-17 A plugin README with visuals and committed evaluations are a follow-up pull request (G1). The follow-up's evaluations are a `claude plugin eval` suite.
- 2026-11-17 Igor settled the quoting rule at G4 ("1a"): labels are quoted wherever the diagram type takes a quoted string; sequence diagram text and state transition labels stay bare. R11 is reworded; this is a recorded departure from the agreed spec §3, which says "every label quoted".
- 2026-11-17 Igor's G4 approval also confirms the changes the roadmap review made to the Verification contract after G3: AC36, AC37, the rubrics, trials T10 and T11, the two checkpoints.
- 2026-11-17 `main` moved during phase 2: pull requests #31 and #32 added the `dev-environment` plugin, released the marketplace as 0.5.0, took decision number 0021 and allowed skills to ship bash scripts. The unpushed branch was rebased onto `main` at 74a0a63. Consequences: this work item's decision record is 0022; the marketplace release in p6 is 0.6.0; the plugin is the ninth. Igor decided the same day that `drawing-architecture-views` ships a bash script that builds and rebuilds the page ("Ship a script (Recommended)"): R41 and AC38 are added, p2 gains the script, and decision 0022 records it.
