# Framing: A plant care assistant

Date: 2026-11-03
Verdict: shape
Bet: not yet

## Idea

> A proper plant care assistant: photo log, fertilising schedule, weather-aware watering and sync between my laptop and phone.

## Problem

The plant keeper manages everything but the water in their head, and forgets fertiliser most of all.

## Evidence

- Code: `sprig.py`: holds only watering dates.
- Context: decision 0003 keeps Sprig offline, so weather and sync need a superseding record.

## Options

| Option | Value | Appetite estimate | Risk | Reversibility |
|---|---|---|---|---|
| A: The whole assistant | Everything in the request | over 2 days; cut to the fertilising schedule, or split | Weather and sync reach the network | hard |
| B: A fertilising schedule only | The most forgotten task gets a date | 1 day | Too few plants need it | easy |

## Recommendation

B, because fertiliser is what is forgotten and it needs no network. A would win if decision 0003 were superseded.

## Remove if

- No fertilising date is recorded within a month.

## Verdict

shape: option B, cut from the whole assistant. Photos, weather and sync are left out.
