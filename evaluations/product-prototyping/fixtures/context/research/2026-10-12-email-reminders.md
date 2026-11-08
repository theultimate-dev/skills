# Framing: Email reminders

Date: 2026-10-12
Verdict: shape
Bet: 02 (bets/02-email-reminders.md)

## Idea

> Email me when a plant is due.

## Problem

The plant keeper forgets to run `due` on busy days.

## Evidence

- Code: `sprig.py`: answers only when run.

## Options

| Option | Value | Appetite estimate | Risk | Reversibility |
|---|---|---|---|---|
| A: A local script that sends mail | A message on the due day | 1 day | Needs a mail account | moderate |
| B: Do nothing | None | ½ day | The problem stays | easy |

## Recommendation

A, because it answers the problem directly. B would win if a mail account proves too much.

## Remove if

- The email is ignored for a week.

## Verdict

shape: try A.
