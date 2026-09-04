# 0002: Skills use the open Agent Skills format with three frontmatter fields

- Status: accepted
- Date: 2026-09-03

## Context

Every harness I use reads the same `SKILL.md` folder format, published as the open Agent Skills specification. They differ in how they treat frontmatter. Claude Code accepts around fourteen extensions beyond the spec, such as `disable-model-invocation`, `argument-hint`, `context: fork`, and `hooks`. Uploading a skill to claude.ai rejects any key outside the six spec fields. Copilot CLI warns on every unknown field at startup. Pi ignores unknown fields. Grok Build reads Claude-shaped extensions.

The skills in this repository must install and behave the same in all of them, including the GUI clients that only accept an upload.

## Options

1. **Claude Code's full frontmatter.** Best experience in my main harness. Breaks claude.ai upload, produces warnings elsewhere, and signals "Claude only" to readers on other tools.
2. **The six spec fields.** Portable by definition. `allowed-tools` is marked experimental and support varies; `metadata` has no use here yet and has a history of breaking Copilot discovery when placed last; `compatibility` matters only when a skill needs a tool.
3. **Three fields: `name`, `description`, `license`.** The subset every implementation agrees on today, each a single `key: value` line.

## Decision

Option 3, with the door open to `compatibility` when a skill genuinely requires a tool or runtime. Adding it happens in a change that says why.

Behaviour that Claude Code would express in frontmatter, such as "only run when the user asks explicitly", goes into the description and the body instead. Those work in every harness.

Frontmatter is limited to single-line `key: value` pairs. No block scalars, lists, or comments. This keeps parsing identical across tools and lets `scripts/validate.py` check it without a YAML library.

## Consequences

- Every skill installs by every route, including zip upload to claude.ai, Claude Desktop, Cowork, and ChatGPT.
- I give up Claude-specific conveniences: argument hints, forked context, invocation gating in metadata. Accepted. Skills that need harness-specific behaviour belong in a harness-specific repository, which is planned separately.
- The `name` must match the directory name and stay unique across the repository, because flat installers copy skills side by side.
