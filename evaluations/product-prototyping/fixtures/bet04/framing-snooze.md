# Framing: Snooze a plant while away

Date: 2026-11-02
Verdict: shape
Bet: not yet

## Idea

> Before a trip I want the due list to stop nagging me about plants someone else is watering.

## Problem

The plant keeper is away for a week now and then, and the due list then shows plants they cannot water, so the list stops being read. WAT-02 lists every due plant, with no way to set one aside.

## Evidence

- Code: `sprig.py`: `is_due` decides what the due list shows.
- Context: WAT-02 and WAT-03 define due; decision 0003 keeps this local.
- Inference: a date on the plant is enough, with no new store.

## Options

| Option | Value | Appetite estimate | Risk | Reversibility |
|---|---|---|---|---|
| A: Snooze one plant for N days | The list stays quiet per plant | 1 day | The limit is a guess; exposed in the first try | easy |
| B: Pause all reminders until a date | One command before a trip | ½ day | A plant someone else is not watering disappears too | easy |

## Recommendation

A, because the problem is plants someone else is watering, which is per plant. B would win if every trip covers every plant.

## Remove if

- After the next trip, no plant was snoozed.

## Verdict

shape: option A. Shaping settles the limit on the days.
