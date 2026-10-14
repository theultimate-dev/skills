# Closing a bet

How to read what a bet produced, decide whether it is built, and fold it back into the context repository. The commands use `git` and GitHub's `gh`; another host's CLI or API applies the same way.

## Reading the code repository and its host

The code repository is read-only for this skill. Allowed:

| Purpose | Command |
|---|---|
| Find the base branch | `git -C <code> symbolic-ref --short refs/remotes/origin/HEAD`, or the base the roadmap's contract names |
| Read a file as merged | `git -C <code> show <base>:docs/product-engineering/<slug>/spec.md` |
| List what the base holds | `git -C <code> ls-tree -r --name-only <base> -- docs/product-engineering/<slug>/ decisions/` |
| Check state without locks | `git -C <code> --no-optional-locks status --porcelain` |
| Find a slice's pull request | `gh pr list -R <owner/repo> --head <branch> --state all --json number,url,state,mergedAt,mergeCommit,headRefOid,body` |
| Read a file the local base lacks | `gh api repos/<owner/repo>/contents/<path>?ref=<base>`, decoding the base64 content |

Never write, commit, stash, fetch, pull, check out or run scripts in the code repository. When the local base is behind the host, read through the host or ask the user to update their checkout.

## The evidence, source by source

**`spec.md`.** The `Source:` line has the form `bet <path in the context repository> @ <full SHA> in <context repository name> (read-only)`. Requirements and acceptance criteria were imported verbatim from the bet at that pin, so they should match the bet's text at that commit: `git -C <context> show <sha>:<bet path>`. Additions live in a separate series, `AC-E1 (PAN-03)`, added at the code side's G1 for detail inside the bet's boundaries. Three marks may be appended to imported lines, each with the date and the user's words, and they are authoritative: `cut (…)` on a `~` item, `extended (…): L` on the Appetite line, and `re-pinned from <short sha> (…)` on the Source line. When the Source line ends "pinned by the loop at intake" or "pasted, not checked against the pin", read SKILL.md step 1 for what that means for drift.

**`roadmap.md`.** The header's `Appetite (bet):` line states the appetite and the plan count. The Decisions section holds every dated change after launch, each quoting the user: re-pins, cuts made after G4, appetite extensions, and the outcome of each context escalation. A cut made at the first G1 happens before the roadmap exists, so it appears only as the mark in `spec.md`. An appetite extension given inside the loop is an `extended` mark in `spec.md`, mirrored here once a roadmap exists, and is never written into the bet file; report it in the outcome log's Appetite line.

**`plans/NN-slug.md`.** One `Branch:` line per PR slice finds the pull requests. Notes and Changes after launch hold routine deviations; a deviation that touched an architecture element is a candidate for as-built text. A plan whose `Status:` is not `done` has unmerged slices.

**Decision records.** New records in the code repository's log that name the bet in their Context. They are implementation decisions by default. Apply the test below to find the ones that moved the architecture.

**Pull requests.** For each branch: merge state, merge commit, `headRefOid` at merge, and the body's `## Verification` report. Each report states the commit it ran on and one row per criterion: `pass`, `fail`, `blocked` or `blocked (human eye)`.

**The hand-back.** When the loop's finish report is pasted, use it to find things faster. Check every claim against the sources above, and cite the sources, not the hand-back.

## Matching criteria to merged code

A criterion is observed when a merged pull request's verification report shows it `pass` on that pull request's final head. Rules:

- **Commit.** The report's commit equals the pull request's head at merge, or it is an earlier commit and every commit after it, up to the merged head, touches only the work item's planning folder (`docs/product-engineering/` by default), the same rule the merge gate uses. Check it read-only with `git -C <code> diff --name-only <report sha> <merged head>`, or the host's compare API. A report on an earlier commit also counts when its "Carried forward" note says the later diff touched only other paths, and that diff agrees.
- **Latest wins.** When two merged pull requests report the same criterion, the later merge counts. A later `fail` on a merged head means the criterion regressed: not observed.
- **Human eye.** A `blocked (human eye)` row on a pull request that a human reviewed and merged counts as observed by that reviewer. Record it as `human eye, merged by <login>`.
- **Progress only.** A row marked as progress toward a later phase is not an observation.
- **Flaky.** A row that failed and passed on retry counts as `pass` only when the report quotes a tool error for the first failure.
- **Cut.** A criterion cut with the user's words in `spec.md` is accounted for, not observed; the mark in `spec.md` is authoritative. A matching entry in the roadmap's Decisions is expected only for a cut made after G4. Cutting is allowed only for `~` items, so a cut on a criterion without `~` is a finding: ask.

List every bet criterion and every `AC-E` in one table with its result and evidence (pull request, short SHA), as the outcome log does. A criterion with no row in any merged report is not observed.

## Architecture or implementation

A code-repository record moved the architecture when it changes something the context repository describes:

- an element, boundary or technology in `architecture/`;
- a contract in `architecture/contracts/`;
- a context decision.

Anything inside one element that no other bet consumes stays an implementation decision. Mention it in the outcome log only when a later bet needs to know it. When a record moved the architecture:

- **The loop escalated it.** The context escalation's outcome is in the roadmap's Decisions. Write the as-built text and link the record.
- **The loop did not escalate it.** That is a finding. Show the divergence and ask whether to adopt it, with a context decision record, or to open a follow-up that restores the architecture.

## Reconciling, in order

1. Write the outcome log first: it is the record the other edits cite.
2. Requirements and catalogue rules.
3. Architecture and contracts.
4. Decision links and adopting records.
5. Registers and glossary.
6. Bet status.
7. Derived indexes last, rebuilt from the files they index.

### Promoting rules

Promote when a rule will outlive this bet:

- an `AC-E` that states product behaviour a later bet must preserve, such as an error message users rely on, or a limit;
- a behaviour the code side decided inside the bet's boundaries that changes what a requirement means.

Do not promote implementation detail or test mechanics. A promotion edits a requirement's text or adds a requirement with the next free ID. Show the wording and get the user's yes.

### Contract details

The bet's `Produces or changes` line states what the bet fixed about a contract. Details it left open were settled by the code side, in `spec.md`'s Approach (its Contracts line) or in a decision record. Write them into the contract file and cite the source. When the shape changed, raise the minor version for a compatible change and the major version for an incompatible one. A bet that consumed a contract version not `accepted` at handoff is a finding: bets consume only `accepted` versions.

## Worked close

Larder's Bet 07, "Shared shopping lists sync across a household", appetite L, pinned at `a1b2c3d`. The work item `07-shared-list-sync` in `larder` has two plans and five merged pull requests.

- **Criteria.** AC1 to AC5 passed on merged heads. `~ AC6 (SHO-04)`, list colours, was cut: `cut (2026-11-03: "drop colours, ship without them")`, mirrored in the roadmap's Decisions. `AC-E1 (SYN-02)`, a conflict notice reading "Changed on another device", passed on #41 at `e4f5a6b`.
- **Decisions.** `larder: decisions/0004-batch-sync-writes.md` batches writes inside the sync service. It is internal to one element, so it stays an implementation decision and is noted in the outcome log. `larder: decisions/0005-sync-cursor-format.md` fixed the cursor format that `architecture/contracts/sync-protocol.md` left open. The bet named that contract under `Produces or changes`, so the contract goes from version 1.0 to 1.1 with the cursor format, a compatible addition, citing the record.
- **Requirements.** SHO-01 to SHO-03 become `built`. SHO-04 stays `planned` with a note: "colours cut in Bet 07". SYN-02 becomes `built`. The conflict-notice wording is promoted into SYN-02's text after the user agrees, because a later mobile bet must keep it.
- **Registers.** RSK-03, "sync conflicts lose edits", is closed and cites AC3 and AC-E1.
- **Status.** `done`. The bet board, the V1 brief's coverage and the requirement counts are rewritten.
