# 0003: Sprig stays offline

- Status: accepted
- Date: 2026-10-02

## Context

Sprig is for one person on one machine. Anything that reaches the network needs an account, a server and a way to keep a secret.

## Options

Stay offline, or add a small hosted service.

## Decision

Sprig uses no network access and no accounts. It answers when it is run.

## Consequences

Reminders, sync and anything else that needs a server are out of scope unless this record is superseded.
