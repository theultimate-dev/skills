# Ranking

The aim is the 20 percent of changes that move 80 percent of the outcome, one small step per session. A score keeps the choice honest; the user's goals decide what the score values.

## Score

Score each candidate from 1 to 3 on three scales and multiply. The result runs from 1 to 27.

| Score | Frequency: how often it bites | Cost: what one occurrence costs | Reach: how far the fix travels |
|---|---|---|---|
| 1 | Once in this session, not seen before | A turn or two, a minute of the user's time | One task, or a rare path in one project |
| 2 | Twice or more in this session, or once in one earlier session | Rework, a wrong turn of several steps, or the user stepping in by hand | Every session in this project, or every session of one kind, such as releases or reviews |
| 3 | Seen in two or more earlier sessions, or certain to recur because every session passes through it | A wrong result reaching someone (a reader, a client, a published artifact, the main branch), a risky action that nearly ran, or the user losing trust in delegating | Every session in every project, or what ships to the people the user's first goal serves |

Frequency comes from this session and the ledger. A watchlist item's count is the number of sessions it has appeared in; a slipped suggestion scores at least 2, because it came back after a fix.

Score a win by the miss it prevents: frequency is how often the situation recurs, cost is what a miss would cost. Score a removal by its load and its harm: a line that loads in every session has frequency 3; cost is 2 when it misled the agent in this session, 1 when it only takes space.

Effort is not in the product; it filters and breaks ties. A candidate that takes more than about fifteen minutes is cut to its first step before it is scored.

## Goals

The ledger lists the user's goals in priority order. They do three jobs:

- **Reach.** A fix that reaches the people the first goal serves scores reach 3, even from one project. For a user whose first goal is helping readers and clients, a fix to a published skill, a template, or documentation outranks a fix to private settings at the same frequency and cost.
- **Naming.** Every card names the goal it serves. A candidate that serves none of the goals goes on the watchlist, whatever its score.
- **Ties.** Equal scores go to the card serving the higher goal.

Without goals, as on a first run, score reach without the goal rule, name on each card the goal it would serve as you understand the user, and say so in the caveat line. The rule that sends goal-less candidates to the watchlist waits until goals are set.

## Ties and order

At equal score, prefer in this order:

1. The higher goal.
2. The smaller effort.
3. A removal over an addition.
4. The longer history: more sessions on the watchlist, or a slip after an earlier fix.

Order the cards by score, highest first. Then check two rules: at least one card takes five minutes or less, and no two cards share a root cause. When the five-minute rule fails, swap the third card for the best small candidate; with only two cards, add it as a third.

## A thin session

Two cards is the floor. When the session offers fewer than two candidates worth one, fill in this order:

1. The highest-count watchlist item, if its fix is now clear. Its evidence is its ledger entry: the count, the date last seen, and the pointer.
2. A win from this session, written down so it repeats.
3. A removal: a line in the instruction files the session loaded that is wrong, stale, duplicated, or restates what the repository shows. The loaded files are part of the session, so the line itself is the pointer.

All three come from evidence. A card made from general advice fails the pointer rule and does not ship.

## What does not rank

- Rewording a rule more forcefully. Escalate the mechanism instead.
- A change whose check cannot be observed. Rewrite the check, or drop the card.
- A redesign. Its first step can rank; the redesign goes on the watchlist.
