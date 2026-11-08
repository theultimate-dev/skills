# Sprig

Sprig remembers when houseplants were last watered and says which are due. Current release label: 0.3.

## What Sprig is

A command-line tool for one person who keeps houseplants and forgets their turns.

## Features

- Add a plant with a watering interval: done
- List plants: done
- Water a plant: done
- See which plants are due: done
- Email reminders when a plant is due: done

## Roadmap

Ideas for later: group plants by room, snooze a plant while away, and plant photos.

## Decisions

| # | Decision |
|---|---|
| D1 | A watering day follows the local date |
| D2 | Data is one JSON file |
| D3 | Sprig is offline |

## Risks

- Two runs at once can overwrite each other's data file, losing a watering.

## Usage

Run `python3 sprig.py --help`.
