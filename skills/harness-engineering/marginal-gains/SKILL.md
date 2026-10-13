---
name: marginal-gains
description: "Reviews a working session with a coding agent and proposes the two or three smallest changes to the user's harness that would pay off most: instruction files such as AGENTS.md or CLAUDE.md, skills, memory, hooks, permissions and settings, repository checks, and the user's own prompts. Reads the session for corrections, restated instructions, failures, rediscovery, and wins; ranks by frequency, cost, reach, and the user's goals; returns each as a card with the evidence, the exact change, and a check for the next session; and keeps a user-level ledger so applied changes get graded, declined ones stay out, and recurring friction rises. Use when the user asks, usually at the end of a session, for a session retro or debrief, lessons learned about working with the agent, what to change in their instruction files, skills, memory, or setup so the next session goes better or a mistake stops recurring, or marginal gains. Not for rewriting one prompt on its own or reviewing product code."
license: MIT
---

# Marginal gains

Find the few smallest changes to the user's harness that will pay off most across future sessions, back each one with evidence from this session, and keep score so the gains compound. Every run returns two or three suggestions, never more, the most crucial first, each small enough to apply in fifteen minutes or less. A one-percent gain that is checked next session beats a rebuild nobody checks.

## What counts as the harness

Everything persistent that the agent runs under and the user controls, apart from the model and the product code.

| Layer | Examples | Typical gain |
|---|---|---|
| Instruction files | User-level and project-level AGENTS.md or CLAUDE.md, rules files | One line the agent could not infer; a contradiction or a dead rule removed |
| Skills | The skills the user invokes, and the ones the user writes | A description that triggers when it should; a missing step; depth moved to a reference |
| Memory | The facts and preferences the harness saves between sessions | A fact the agent had to rediscover; a stale entry deleted |
| Controls | Hooks, permission rules, settings, sub-agent definitions, tool and server configuration | A rule the model keeps breaking, enforced; a permission the user always grants, allowed |
| Repository checks | Validators, tests, linters, and CI that the agent runs | A mistake caught before the user sees it |
| Prompts | How the user asks: openers, saved prompts, invocation habits | A fact supplied up front; a saved prompt for a request that recurs |

Locate these from what the harness has already loaded into the session: the instruction files it shows, the skills it lists, the memory location it names, and the settings and checks the instruction files mention. Do not sweep the disk for them. Read a file when a candidate points at it, and always before proposing a change to it.

## Run

1. Open the ledger.
2. Read the session for evidence.
3. Grade the suggestions still being checked.
4. Turn evidence into candidates, each with a mechanism and an exact change.
5. Rank them and keep two or three.
6. Record the run and deliver the cards.
7. Apply what the user picks and update the run.

One pass over what is already in context. Do not delegate any step to a sub-agent, and ask nothing before the cards are delivered.

### 1. Open the ledger

The ledger is one Markdown file per person: the user's goals in priority order, a watchlist of friction that has not yet earned a card, and every suggestion made so far with its status and outcome. Find it through a pointer line in a user-level instruction file, such as `Marginal gains ledger: <path>. Read it only when running marginal-gains.`, or at a path the user names. Read the goals, the watchlist, and the newest five runs. Then scan the Status and Outcome columns of every older run, and the Folded section, for suggestions still being checked and for declined ones; open an older run in full only when a candidate needs its history. [Ledger](references/ledger.md) has the format and the upkeep rules.

No ledger means a first run. Carry on without one; the setup is proposed after the cards (step 6).

### 2. Read the session for evidence

The session is the conversation in context plus what it changed: commits, diffs, and files written. When earlier turns were compacted into a summary, work from the summary and the changes, and say the evidence is partial.

Look for these signals. [Evidence](references/evidence.md) shows what each one looks like and where its fix usually lives.

- Corrections and redirects by the user.
- Instructions the user had to restate, above all ones a harness file already says.
- Tool calls the user denied or interrupted, and permission prompts the session shows the user approving again and again.
- Tool failures, retries, and checks that failed.
- Questions the agent asked that the repository or the harness could have answered.
- Rediscovery: files read, commands tried, or conventions worked out again.
- Skills that should have triggered and did not, triggered wrongly, or were followed and still went wrong.
- Steps the user did by hand for the agent.
- What went unusually well and would be lost unless written down.

Every candidate carries at least one pointer: a short quote of the turn, the tool call, a `file:line`, or a commit. A candidate without a pointer is generic advice; drop it. Do not infer what the session does not show, such as approvals the harness never displayed to the agent. Quote a phrase at most, and never copy secrets, credentials, personal data, or client material into a card or the ledger.

Read earlier sessions' transcripts only when the user asks for a wider look and the harness exposes them, and name the sessions read.

### 3. Grade the suggestions still being checked

For each ledger suggestion that is `applied` with outcome `open` or `held`, look for its check in this session:

- **Held**: the check passed, or the situation came up and went right. A second hold, in a later session than the first, makes it `settled`; stop checking it.
- **Slipped**: the friction came back. The suggestion returns as a candidate on a firmer mechanism, linked to the original ID.
- **Not exercised**: nothing in this session touched it. Leave it as it is.

### 4. Turn evidence into candidates

Group the evidence by root cause: one cause with three symptoms is one candidate. Add the slipped suggestions, and the deferred suggestions and watchlist items this session saw again. Leave out what is `applied` and not yet `settled`, and what the ledger shows as declined. A declined suggestion returns only when this session shows something its decline reason did not cover, such as a higher cost or a different consequence; the same friction recurring is not new evidence.

For each candidate:

- **Mechanism.** The lightest one that will hold, at the narrowest scope that covers every occurrence. A rule that is written down and still broken is moved to where the agent reads it at the right moment, or made concrete with an example, never reworded more forcefully; once a fix to it has slipped, it needs a firmer mechanism. [Mechanisms](references/mechanisms.md) has the ladder, from a prompt habit to a check in CI, and when removing beats adding.
- **Exact change.** The file and its scope (user, project private, project shared, or published), the section or setting, and the text or diff, matching the target's style. Instruction text says what to do, gives the reason in a clause when it is not obvious, and carries no capitals for emphasis and no prohibition without the alternative.
- **Size.** Fifteen minutes or less to apply. A bigger change is cut to its first step; the step becomes the card and the rest goes on the watchlist.
- **Check.** What the next session will show if the change worked, observable without asking the user: no restated instruction, a command that runs first time, a skill that triggers on its own.

### 5. Rank and keep two or three

Score frequency, cost per occurrence, and reach from 1 to 3 each and multiply. The user's goals in the ledger decide what reach means and break ties. [Ranking](references/ranking.md) defines the scales, how to score wins and removals, how the ledger's counts raise frequency, and the tie-breaks.

- The highest score goes first.
- At least one card takes five minutes or less.
- Never more than three. Every other candidate goes on the watchlist with its count, so it can rise.
- Two is the floor. With fewer than two candidates worth a card, fill from the watchlist, then from writing down something that worked, then from removing a line in the instruction files the session loaded that is wrong, stale, duplicated, or restates what the repository shows. Every fill still carries a pointer; never invent friction.

### 6. Record the run and deliver the cards

Before sending the reply, write this run to the ledger: every card `proposed`, the grades from step 3, any card the last run left `proposed` set to `deferred`, and the watchlist counts. The reply often ends the session, so the record cannot wait for the user's answer. On a first run there is no ledger yet; write nothing until the user confirms its location.

Then fill the [suggestions template](templates/suggestions.md), and nothing else: no preamble and no session summary.

1. One line of caveats, only when one applies: the evidence is partial, a focus left candidates out, there are no goals yet, or earlier sessions were read.
2. One line on the suggestions graded in step 3 and on any the last run left unanswered. Omit it when there are none.
3. Two or three cards. Each has the next free ID (`G` and a number continuing the ledger), an imperative title, effort in minutes, the goal it serves, the score, the evidence, the exact change with its scope, why it ranks, and its check.
4. One line naming the watchlist items this session saw.
5. The question: which cards to apply, decline, or defer, by ID.

On a first run, add the ledger setup to that question:

- **Location**: a user-level path outside any repository, because the ledger quotes sessions from every project. A folder the user's harnesses share, or the one holding the user-level instruction file, is a sound default. A user who already keeps a ledger gives its path instead.
- **Pointer line**: for each user-level instruction file of the harnesses the user works in.
- **Goals**: in priority order, taken from what the user said in this session or from the instruction files when they state them. When neither does, ask for them in the same question.

### 7. Apply and update the run

Apply exactly the cards the user picks, re-reading each target first. Never commit, push, or publish; name the files changed. Apply a change that grants permissions or runs commands exactly as the card shows it, never with a wider pattern.

Then update the run: `applied` with outcome `open`, `declined` with the reason when one is given, or `deferred`. On a first run, create the ledger from the [ledger template](templates/ledger.md) once the user confirms the location, record this run in it, and add the pointer lines the user approved.

## Edge cases

- **Nobody to answer**, as in an unattended run: write the run with every card `proposed` and apply nothing. On a first run, deliver the cards and the setup proposal, and write nothing.
- **No file access**: deliver the cards and the ledger entry as text, and say that nothing was written.
- **Asked mid-session**: run on the session so far; the run's heading in the ledger says so.
- **The user names a focus**, such as skills only or one repository: rank within it, and say in the caveat line what was left out.

## References

| Read | When |
|---|---|
| [ledger](references/ledger.md) | Opening, creating, updating, or folding the ledger; IDs, statuses, outcomes, the watchlist |
| [evidence](references/evidence.md) | Reading the session: signals, pointers, what is not evidence |
| [mechanisms](references/mechanisms.md) | Choosing where a fix lives, escalating a slipped one, removing instead of adding, safe allow rules |
| [ranking](references/ranking.md) | Scoring candidates, wins, and removals; using the goals; breaking ties; filling a thin run |
| [worked example](references/worked-example.md) | Calibrating cards and a ledger entry against a sample session, including a card that fails |
| [suggestions template](templates/suggestions.md) | The reply |
| [ledger template](templates/ledger.md) | A new ledger |
