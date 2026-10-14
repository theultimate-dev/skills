# Versions and milestones

How to cut a product into versions and a version into milestones, how to write gates and exit criteria that someone can actually judge, and what happens when a version ships. The examples use Larder, a fictional household pantry and meal-planning app: V1 is the web app with a sync service, V2 adds shared households.

## Versions

A version is a state of the product that someone can use for a long time on its own. It is not a sprint, a quarter, or a release number.

| Good version | Why |
|---|---|
| "V1: Larder on the web. One household tracks its pantry and plans meals in the browser; lists stay in sync between devices." | Usable on its own, for months |
| "V2: Shared households. Several people in a household edit one pantry and one meal plan." | A new kind of use, built on V1 |

| Weak version | Problem |
|---|---|
| "V1: Backend", "V2: Frontend" | Neither is usable on its own |
| "V3: Polish and bug fixes" | Not a state of the product; that work belongs inside the versions |

### Gates

A gate is the condition that must hold before the next version starts. It is observable, judged by the user, and about use, not about code:

- "V1 is in daily use by five households for a month, and no household has lost a list."
- "A V2 household of three edits the same pantry for two weeks without a conflict anyone notices."

A gate is never "V1 is finished" or "all V1 bets are done". When the user cannot say how they would judge a gate, it is an open question, not a gate.

### When a version's folder opens

- `roadmap/README.md` holds every version as a section: status, one line on what it gives, the gate. A version's status lives there and nowhere else.
- `roadmap/vN/` holds the version brief and its bets. It opens when the previous version ships.
- The first two versions may be planned together when the user asks, because a later version often shapes decisions the first must not block (V2's shared households decide whether V1's data model has an owner per list or per household). Plan the second only as far as its brief: it lives in `roadmap/v2/README.md`, with no `bets/` folder, and no bet is shaped for it until the first ships.
- Versions after that stay sections. Planning them in detail before the earlier ones ship produces documents that will be wrong.

## Version brief

| Part | Write | Avoid |
|---|---|---|
| Outcome | Who can do what, and what they see, in two to four sentences | A feature list |
| Done when | An observable condition the user judges: "used daily by me for a month and by three other households without my help" | "All milestones exited" |
| Scope | An In / Not in table; each "Not in" names the version that takes it, or Parked | Silent omissions |
| Milestones | Release slices in delivery order, each with what the user gets and its exit criterion | Layers or components as milestones |
| Coverage index | Derived from the catalogue's Version column | A hand-typed list of IDs |
| Prerequisites outside the code | Checkboxes, each naming the milestone it gates | Mixing them into requirements |

## Milestones as release slices

Treat the version like a story map: the activities a user goes through, left to right, with the work under each. A milestone is a horizontal cut through all of them.

1. **Walking skeleton first.** The thinnest slice that runs end to end through every major container and through the release path: built, deployed or packaged, and tested automatically. Larder's 1.0 Skeleton: sign in, add one pantry item in one browser, see it in another; the sync service, the web app, the database and the deploy pipeline all exist, and almost nothing else does.
2. **Then usable slices.** Each later milestone gives the user something they can use on its own: Larder's 1.1 Pantry (items, quantities, expiry dates, a "use soon" list), 1.2 Meal plans (a week of meals planned from the pantry, with a shopping list for what is missing).
3. **Order by learning value and dependency.** Put the riskiest assumption as early as its dependencies allow. A milestone that only another milestone makes useful should follow it closely.
4. **Size.** A milestone usually holds one to four bets. More than about five means it is two milestones. A milestone that is less than one bet is part of a neighbour.

### Exit criteria

One per milestone, observable, about use, judged by the user.

| Good | Weak |
|---|---|
| "A full day of cooking from Larder's pantry list, with no paper list" | "Pantry feature complete" |
| "A week of meal plans made from the pantry without a spreadsheet" | "All 1.2 bets done" |
| "Another household installs and uses Larder without my help" | "Onboarding implemented" |

The user records the exit in their words; write `exited (YYYY-MM-DD: "<user's words>")`. Merged code never exits a milestone by itself: a milestone whose bets are all `done` but whose exit criterion has not been seen stays `in progress`, and the status report says so.

### Coverage

A requirement row's target Version names a milestone, such as `V1.2`, or only a version, such as `V1`, while it waits for a milestone. A `deferred` row has no target and appears in no index. The coverage index is a table of milestone to requirement IDs, rebuilt from those columns:

| Milestone | Functional | Non-functional |
|---|---|---|
| 1.0 Skeleton | ACC-01 | NFR-01 |
| 1.1 Pantry | PAN-01 to PAN-04, PAN-06, PAN-07, SYN-01 (part) | NFR-02, NFR-03 |
| 1.2 Meal plans | MEA-01 to MEA-04, SHO-01 to SHO-04, SYN-01 (part), SYN-02 | NFR-04 |

Flag, never fix by hand:

- a row targeted at the version only (`V1`): not yet in a milestone;
- a row targeted at a milestone the brief does not list (`V1.3` with no 1.3);
- a milestone with no requirement;
- a promise in the milestone's prose ("a notification when an item expires") that no requirement row covers;
- a requirement targeted at two versions without `part` notes on the bets that deliver it.

Each flag goes to the user as a one-line question with a recommended fix: add a requirement (via `curating-product-requirements`), retarget it, or reword the milestone.

### Prerequisites outside the code

Things that must be true before a milestone can exit and that no bet builds: an account with a store or a payment provider, a domain name, a legal check, a purchase, a person agreeing to try the product. Each is a checkbox with the milestone it gates, so the status report can say "1.3 is blocked by a prerequisite, not by code".

## When a milestone exits

1. The user says the exit criterion holds; quote them.
2. Set the milestone to `exited` with the date and quote.
3. Move the current focus to the next milestone.
4. Any requirement of the exited milestone whose status is still `planned` is a gap: report it, and ask whether it is retargeted, dropped, or the exit was premature.

## When a version ships

1. The user confirms the version's Done-when holds; quote them, set the version to `shipped`, record the date.
2. Check the gate to the next version. When it does not hold yet, the next version stays `planned` and the focus says what is being waited for.
3. Open `roadmap/vN+1/` with its version brief, drafted from its section in `roadmap/README.md`, and leave the section as a one-line pointer. When the version was planned together with the shipped one, its brief already exists: add its `bets/` folder.
4. Recommend an architecture refresh with `designing-system-architecture` before any bet of the new version is shaped: a shipped version changes what is `built`, and the next version's contracts are usually not settled yet.
5. Review the registers: close risks that the shipped version retired, and retarget open questions.

## Worked example: Larder V1

`roadmap/README.md`:

| Version | Status | What it gives | Gate to the next |
|---|---|---|---|
| V1 Larder on the web | in progress | One household tracks its pantry and plans meals in the browser, in sync across devices | In daily use by five households for a month, no list lost |
| V2 Shared households | planned | Several people edit one pantry and one meal plan | |

Current focus: V1, milestone 1.1 Pantry. Parked: barcode scanning (needs a product database licence; revisit after V2).

`roadmap/v1/README.md` milestones:

| Milestone | What the user gets | Exit criterion | Status |
|---|---|---|---|
| 1.0 Skeleton | Sign in; one pantry item added in one browser shows in another | The skeleton runs from a clean deploy for a week with no manual fix | exited (2026-11-02: "skeleton is boring, which is the point") |
| 1.1 Pantry | Items with quantities and expiry dates, a "use soon" list | A full day of cooking from the pantry list, no paper | in progress |
| 1.2 Meal plans | A week planned from the pantry, a shopping list for the gaps | A week of meal plans without a spreadsheet | planned |

Prerequisites outside the code:

- [ ] A domain for the public web app (gates 1.1, because other households test it)
- [ ] Privacy notice reviewed (gates 1.2, which stores meal history)
