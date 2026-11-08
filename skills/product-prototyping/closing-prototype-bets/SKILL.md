---
name: closing-prototype-bets
description: "Closes a prototype bet after the person has tried it: asks keep or remove at Gate 2, showing the build log's checks with evidence, the checks only the person's eye can judge, and the bet's keep-or-remove signal. Keep folds the result into the context: requirement rows become built, planned architecture becomes built, decisions are recorded, the changelog entry stays. Remove reverts the bet's code commits, records its new requirements as dropped with the reason, deletes its planned architecture and writes the lesson. Either way it writes the bet's Result and rebuilds the requirements index, architecture index, folder indexes and bet board. Also closes a stopped bet and runs a light audit of links, IDs and indexes on request. Use when the user says keep it, remove it, close bet N, I tried it, or drop the bet. Not for closing a bet of a versioned roadmap (reconciling-product-context)."
license: MIT
---

# Closing prototype bets

A prototype learns by trying: a bet is built, the person tries it, and the person decides whether it stays. This skill runs that decision (Gate 2) and then makes the context and the code agree with it. A kept bet becomes part of the product's record; a removed bet leaves the code as it was and leaves the lesson behind.

The context follows [the prototype profile](references/prototype-profile.md); read it first for the tree, statuses, IDs and house rules. The examples use a fictional product, Quill, a single-user web app that tracks daily writing streaks. Its context lives in `context/` inside its code repository, and its changelog is `CHANGELOG.md` at the root.

## Modes

| Mode | Triggers | Ends with |
|---|---|---|
| Close a bet | "keep it", "remove it", "close bet 04", "I tried it", "drop the bet", the builder's hand-back pasted in | The bet `kept` or `removed` with its Result, the indexes rebuilt |
| Audit | "audit the context", "check the links", before graduating to the full profile | A short report: mechanical fixes made, substantive findings for the person |

## Close a bet

### 1. Find the bet and check it can close

Read `context/bets/NN-slug.md` from the working copy first, and say when it differs from the last commit (`git status --short -- context/bets/NN-slug.md`): the builder or shaper may have left the file uncommitted. Read Status, Context pinned, the Build log and the Result from it. Read every other field at the commit in `Context pinned`, as the profile says; a bet whose pin is `not yet` has no approved snapshot, so read its draft as it stands.

Whether anything was built is decided by the Build log's list of code commits, never by Status: a reshaped bet is `shaped` again and keeps its commits.

| Status | What to do |
|---|---|
| `built` | Go to step 2 |
| `stopped` | Go to step 5 |
| `shaped`, `approved` | With an empty code commit list: if the person says drop it, close as removed in step 4 with nothing to revert; otherwise hand it back to `shaping-prototype-bets`. With code commits listed: hand it back to shaping, or, if the person says drop it, close as removed in step 4. Authority comes from the `Autonomy:` line at the pin when the bet is `approved` with a valid current pin; only a bet that is `shaped` again, its pin `not yet` because a reshape replaced it, falls back to the last dated `Approved YYYY-MM-DD at <sha>: <autonomy line>` line of the Build log. A bet never approved has no authority beyond the person's explicit current words. The `Autonomy:` line of a bet that is not approved is a proposal and grants nothing |
| `building` | Building is still running or was cut off. Do not close it. Ask the person whether to let `building-prototype-bets` finish, or to stop it, which is `stopped` |
| `kept`, `removed` | Already closed. Show the Result and stop |

A bet is cancelled only under the person's explicit current words; the authority above says only what may then run without asking.

Before writing anything, confirm the code is where the Build log says, and for a close that reverts, that the branch and tree are ready. [Keep and remove](references/keep-and-remove.md), "Read first" and "Is the evidence current", has the commands: every listed commit exists and is an ancestor of the branch checked out; the checked-out branch is the one the authority names; the working tree is clean; and the Build log's verified `Head` is compared with the branch head, so that evidence about code that has since changed is never presented as current. When a commit is missing, say which and ask where the code lives now.

### 2. Gate 2: keep or remove

Present one message, in this order, so the person decides on evidence:

- **The bet.** Its Outcome in a sentence and its appetite.
- **The checks.** One table from the Build log: each `Cn (ID)` with its method, result and evidence, the cuts with their reasons, and the review findings left open. A check the code has changed under since the verified head is marked stale, not passed.
- **For your eye.** Each `person's eye` check, with the Try it block at the end of the Build log. Ask for the person's verdict on each, one line each.
- **The signal.** The bet's `Signal:` line, and `If removed:` as the bet wrote it: what the removal would revert, drop and delete.
- **The question.** Keep or remove, with the first step each one starts. Offer keep only when no check is stale.

Only explicit words decide: "keep it", "remove it", "revert it". "Looks good", a thumbs-up, silence, or approval of the build are not a decision: ask once more, naming both options. Hold the person's words exactly; they go into the Result in the context close (steps 3 and 4), never earlier, because a removal needs a clean tree.

If the person asks for changes before deciding, or a stale check has to be proved again, the bet stays undecided. An explicit in-scope repair request goes to `building-prototype-bets` as a repair: the bet returns to `building` with its pin, base, code commits and consumed working time, within the appetite that remains, and comes back to Gate 2 with a refreshed Try it block. When the appetite is spent it goes to `shaping-prototype-bets` as a reshape; when the scope grows, as a new bet. Gate 2 asks again afterwards.

### 3. Keep

Follow [keep and remove](references/keep-and-remove.md), "Keep", which holds the ordered checklist. In short: write the Result with the person's words and the lesson; turn the requirement deltas into catalogue rows, honouring the cuts; promote what the code now has from `planned` to `built` and delete planned architecture that only cut scope introduced; record the decisions the build settled; update notes and glossary; check the changelog entry still tells the truth; set `Status: kept`; rebuild the indexes (step 6). Nothing is reverted.

### 4. Remove

Follow [keep and remove](references/keep-and-remove.md), "Remove", which holds the ordered checklist and the git commands. In short, in this order:

1. Preflight the branch and a clean tree, and hold the person's words.
2. Revert exactly the code commits the Build log lists, as one change, only as far as the authority allows (`revert on remove: yes` in the Autonomy line at the pin, or, only while a reshape has replaced the pin with `not yet`, in the last `Approved` line of the Build log; otherwise show the commands and ask). Stop on a merge commit, a commit that mixes code and context, and a conflict.
3. Prepare and check the revert, with the `Removed` changelog line when a release already carries the entry, then make its one code commit.
4. In a separate context commit: write the Result (`Removed`, the date, the person's words, the lesson), record the bet's new requirements as `dropped` with the reason, delete its planned architecture and the links to it, handle decisions and notes, set `Status: removed`, rebuild the indexes (step 6).

A bet whose code commit list is empty has nothing to revert: skip steps 1 to 3, and say in the Result that nothing was built.

### 5. Close a stopped bet

A `stopped` bet ran out of appetite with work left. Show the person what is left from the Build log, what the cuts were, and two ways forward: reshape it (hand it to `shaping-prototype-bets` with the Build log as input) or close it as removed. The person's explicit words decide. Closing as removed follows step 4, reverting whatever code commits the Build log lists, none when it never committed code.

### 6. Rebuild the derived indexes

Rebuild last, from the files they index, and never by hand-editing:

- `product/requirements/README.md` from the capability files, with [the requirements index template](templates/requirements-index.md).
- `architecture/README.md`: only its two derived parts, the Contracts table from the contract files and the oldest verified-on date from `architecture/ecosystem.md`, with [the architecture index template](templates/architecture-index.md). Its strategy, quality goals and checklist are written by hand: keep them, and update the checklist only when the close added or removed a view.
- Each folder README the close touched (`decisions/`, `research/`, any other), with [the folder index template](templates/folder-index.md).
- `bets/README.md`, the board, from the bet files' header lines and Requirement deltas, with [the board template](templates/bet-board.md), in the same change as the Status. A closed bet shows no reserved IDs.

### 7. Hand back

Report the bet's result and status, the files changed, the code commits made (a revert) and whether they were pushed, the questions and risks now open, and the next step: `framing-prototype-ideas` for a new idea, `shaping-prototype-bets` for a framed one, or a reshape. Context commits are written only when the Autonomy line says `context commits: yes`: one close is one commit, kept apart from the code, made only after checking that nothing is staged outside the close's own paths and that the staged diff is what the close wrote. Releasing is the person's call, with `release-process` when it is installed. Never push, or revert outside the Autonomy line, without the person's agreement.

## Audit

On request, check the whole context, or the paths the person names, and fix what is mechanical:

- **Links.** Every relative link resolves, and a fragment matches a heading. Fix a renamed target when exactly one file matches.
- **IDs.** No ID is defined twice or reused. A dropped ID's number, a number reserved by a bet (removed ones included) and a number recorded in `id-map.md` have not been given to something new. Ask before renumbering anything.
- **Indexes.** Rebuild each derived index and compare: rewrite it when it differs. For `architecture/README.md` compare only the Contracts table and the oldest verified-on date; the authored sections are not audited for sameness.

Report fixes made and findings that need a decision, and name every check that could not run. [Keep and remove](references/keep-and-remove.md) has the commands.

## When a sibling skill is missing

Say in one line which skill is missing, then produce its essential outcome yourself.

| Skill | Essential outcome |
|---|---|
| `decision-records` | A short record in `decisions/` under a numbered title, with Status and Date lines and four body sections, Context, Options, Decision and Consequences, plus its row in `decisions/README.md` |
| `release-process` | Edit the changelog by hand in Keep a Changelog form; cut no version unless the person asks |
| `shaping-prototype-bets` | For a stopped bet, list what is left, the cut options and the reshape question, and leave the bet `stopped` |

Without file access, return the Result, the changed rows and the audit report as Markdown, and say that nothing was written.

## References

| Read | When |
|---|---|
| [prototype profile](references/prototype-profile.md) | Always: tree, statuses, IDs, house rules, the changelog and commit rules |
| [keep and remove](references/keep-and-remove.md) | Folding a bet in, reverting its code commits, the changelog cases, a worked example of each, the audit commands |
| [bet template](templates/bet.md) | Reading the fields a bet carries and where its Result goes |
| [board template](templates/bet-board.md) | Rebuilding `bets/README.md` |
| [folder index template](templates/folder-index.md) | Rebuilding a folder README |
| [requirements index template](templates/requirements-index.md) | Rebuilding `product/requirements/README.md` |
| [capability requirements template](templates/capability-requirements.md) | Creating the capability file of a new prefix at close |
| [architecture index template](templates/architecture-index.md) | Rebuilding `architecture/README.md` |
