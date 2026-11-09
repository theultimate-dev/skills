# Sprig

Sprig is a command-line tool that remembers when one person's houseplants were last watered and says which are due, so that nothing dries out because its turn was forgotten.

## Who it is for

- One person with a dozen houseplants and a terminal open most days.

## Principles

1. A plant that is due is always shown.
2. Everything works offline, from one file.

## Assumptions and constraints

- Assumption: one person uses one data file. If wrong: the data file needs locking.
- Constraint: Python standard library only, no network access. Source: [decision 0003](../decisions/0003-sprig-stays-offline.md).

## What it is not

- A reminder service: Sprig answers when it is run, and contacts nobody.

## Where to read next

- [Glossary](glossary.md)
- [Actors and use cases](actors-and-use-cases.md)
- [Requirements](requirements/README.md)
