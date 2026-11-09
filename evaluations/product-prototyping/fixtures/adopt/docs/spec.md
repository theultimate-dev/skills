# Sprig specification

## Overview

What Sprig does, by capability.

## Plant requirements

| ID | Requirement |
|---|---|
| PLT-01 | `add NAME --every DAYS` registers a plant with its interval |
| PLT-02 | Plant names are case-sensitive |
| PLT-03 | `list` shows every plant with its interval and next watering date |
| PLT-04 | Adding a plant stores today as its first watering |

## Watering requirements

| ID | Requirement |
|---|---|
| W1 | `water NAME` records today as the last watering |
| W2 | `due` lists every plant whose next watering date is today or earlier |
| W3 | The next watering date is the last watering plus the interval |

### Watering day boundary

A watering day ends at midnight UTC.

## Planned requirements

| ID | Requirement | Status |
|---|---|---|
| CAL-01 | Export the due dates as a calendar file | deferred |

## Architecture

One Python file reads and writes one JSON file. There is no background process.

## Decisions

| # | Decision |
|---|---|
| ADR-1 | Data is one JSON file |
| ADR-2 | Nothing reaches the network |

## Risks

- Concurrent runs can overwrite the data file.

## Open questions

- Should the data file be human-editable?
