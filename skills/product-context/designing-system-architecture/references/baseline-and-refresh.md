# Baseline, refresh and as-built

How much architecture to write before a version's milestones are shaped, how contracts follow when bets are shaped, how to move the architecture across a version boundary, and how to bring it in line with what was built. The examples use Larder: V1 is the web app with a sync service; V2 adds shared shopping lists across households.

## Contents

- Two passes
- The baseline checklist
- What to leave planned or open
- Refresh at a version boundary
- As-built in detail
- Divergences

## Two passes

Architecture before code has one job: let the first milestone's bets start from settled ground and run without colliding. Depth beyond that is guesswork that the code will correct. It comes in two passes, so the architecture never waits for bets and bets never wait for more architecture than they consume.

**Pass 1, baseline mode,** runs from the version's requirements before any milestone is shaped into bets. It is enough when:

1. Every container and store the first version's requirements need appears at C4 level 2, with the protocol on every arrow.
2. Every interface between containers is named, with its producers and consumers, and listed in the Contracts table as not written yet.
3. Every decision that would be expensive to undo once code exists is accepted (see the decisions reference).
4. Every cross-cutting rule the first version's requirements imply is written, such as the trust boundary or the error-recovery rule.
5. The main flow and the hardest path exist as runtime scenarios.

**Pass 2, contract mode,** runs when a milestone's bets are shaped: write the contracts those bets share. Each must be `accepted` before a bet that consumes it can be ready. Anything a later milestone needs gets its contract when that milestone's bets are shaped; a contract written two milestones early is usually rewritten.

## The baseline checklist

| Item | Done when | Larder example |
|---|---|---|
| Context | Every person and external system appears, with what flows | Household member, recipe provider, email service |
| Containers | Every running unit and store, technology, protocol per arrow | Web app, sync service, database |
| Components | Only for a container several bets build inside | Sync service: change log, merger, household access |
| Domain model | The entities the first version stores, with relationships | Household, member, item, plan, change |
| Data | Every store with what it holds, where, how long | Household data, offline cache, change log |
| Concepts | The rules the first version's requirements imply | Offline-first consistency; household as the access boundary |
| Deployment | Where each container runs, for each placement in scope | Hosted service and database; browser client |
| Build and release | How a commit becomes a running product | CI builds, tests, deploys on tag |
| Runtime | Main flow and hardest path | Plan a week; edit offline then reconcile a conflict |
| Interfaces | Named in pass 1; written and accepted in pass 2, when the first milestone's bets are shaped | The sync protocol between web app and sync service; `sync-protocol.md` 1.0 in pass 2 |
| Decisions | The choices expensive to undo after code | Sync model, household access boundary, runtime per container, code repository layout |
| Ecosystem | Every external dependency with a verified-on date | Recipe search API, email relay, database engine |

Mark every arc42 item without content as "not needed yet" in `architecture/README.md`, with the version that will need it.

## What to leave planned or open

- **Later versions.** Sketch at level 2 as `Status: planned`, with `Since:` set to that version. No components, no contracts.
- **Details one bet builds alone.** Leave them to the implementation loop: internal module structure, field names of a message only one bet produces, storage layout inside one container.
- **Open details of a contract.** Write them under "Open details" so the bet producing them knows it settles them, and the reconciliation knows to write them back.

## Refresh at a version boundary

Run when `planning-product-roadmaps` opens the next version.

1. Read the next version's brief and the requirement IDs targeted at it.
2. Never flip `planned` to `built` here: only as-built mode does, from a closed bet's evidence. A section of the shipped version still `planned` either did not ship, and is retargeted to the new version with an open question for the roadmap, or was built without a bet's evidence reaching it, and goes to the audit in `reconciling-product-context`.
3. Add the new version's elements at level 2 as `planned`. For Larder V2: a list-sharing component in the sync service and an invitation flow.
4. Mark retired elements with what replaced them.
5. Re-verify every dependency in `ecosystem.md`; update the version and the verified-on date, and raise a risk for any that went unmaintained or broke compatibility.
6. Name the interfaces the new version's first milestone needs. Write their contracts in contract mode when its bets are shaped.
7. Present the refreshed summary and record the user's agreement on any new decision.

## As-built in detail

`reconciling-product-context` calls as-built mode when a bet closes. Its inputs come from the code repository and the code host, read-only, never from memory:

| Source | What it gives |
|---|---|
| The bet file | Which containers, components and contracts it touches, consumes and produces |
| The implementation loop's hand-back, when given | The settled contract details, deviations, and the implementation decisions it recorded |
| The work item's `spec.md`, when the code repository runs the product-engineering loop | The Approach section: the chosen approach and the contract details settled at G2 |
| The work item's `roadmap.md` Decisions section, in the same case | Re-pins, cuts and escalations that changed scope |
| The code repository's decision records that name the bet | Implementation decisions, some of which may have moved the architecture |
| Merged pull requests on the code host | What actually landed |

The work item's `roadmap.md` is the implementation loop's plan of PR slices in the code repository; it is not this repository's `roadmap/`.

Then:

1. Flip each delivered element from `planned` to `built`. An element delivered in part keeps `planned` and gains a line saying what is built.
2. Write settled contract details into the contract, as the contracts reference describes.
3. Compare what landed with each touched section. Matching: nothing more to do. Diverging: see below.
4. Link each code repository decision record that moved the architecture from the section it changed, as `<repository>: decisions/NNNN-title.md`, never a local path.
5. Rebuild the Contracts table in `architecture/README.md` when a contract changed.

## Divergences

| What diverged | Do |
|---|---|
| A detail inside one element, invisible to other bets | Nothing; it is implementation |
| A container, boundary, store or technology differs from the description | Present both versions to the user. Accepted: update the section, and record a decision when the change is consequential. Not accepted: open a question in `roadmap/open-questions.md`, owned by the user, saying what a fix would have to change |
| A contract's shape differs from its accepted version | Never update silently. This should have stopped the loop as a context change; ask the user, then either write a new contract version or open a question for a fix |
| An element the bet should have built is missing | Leave it `planned` and pass the note to `reconciling-product-context` for the bet's outcome log; it decides whether the bet is `built`. Never write into the bet |
