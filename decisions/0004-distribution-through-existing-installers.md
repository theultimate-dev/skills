# 0004: Distribute through existing installers, no bespoke one

- Status: accepted
- Date: 2026-09-03

## Context

Readers arrive from Claude Code, Codex, GitHub Copilot, Grok Build, Pi, Cursor, and the desktop and web clients of Claude and ChatGPT. Surveyed in September 2026: the `skills` CLI from Vercel (77 agents, symlink installs, weekly releases), Microsoft APM (manifest and lockfile, twelve targets), Claude Code plugin marketplaces (also read by Copilot CLI), Codex and Grok plugin systems, skills.sh packs, the `.well-known/agent-skills` discovery index, per-skill zip upload, and several stale community CLIs.

Two facts shaped the choice. Claude Code delivers a plugin update only when the plugin's `version` in the marketplace entry changes. The `skills` CLI has no repo-side bundle manifest, but it installs a directory subtree with one command.

## Options

1. **A bespoke installer script.** Full control over paths and updates. One more thing readers must trust and I must maintain across every harness's path changes.
2. **Claude Code marketplace only.** One manifest, two harnesses. Everyone else copies files by hand.
3. **Existing installers, with the layout doing the work.** Two documented routes plus release archives for GUI clients.

## Decision

Option 3.

- **Route A, plugin marketplace.** `.claude-plugin/marketplace.json` with one plugin per category, `source: "./"`, `strict: false`, an explicit `skills` array, and a `version` that every release bumps. Claude Code and Copilot CLI install, update, pin, and remove with their own commands.
- **Route B, `skills` CLI.** `npx skills add theultimate-dev/skills/skills/<category>` for a category, `--skill` for one skill, `#tag` to pin, `npx skills update` to update. Covers Codex, Grok Build, Pi, Cursor, and the rest.
- **GUI clients.** Each release attaches `<skill>-<version>.zip` per skill and a `checksums.txt`. Users upload the zip; updating means uploading the newer one.
- The README documents install, update, pin, and remove for both routes side by side and tells readers to use one route per machine.

Documented but not yet exercised by me: Pi's `pi install git:` and APM's path installs. Deferred until someone asks: an `apm.yml`, Codex and Grok plugin manifests, skills.sh packs (membership lives on Vercel's servers, not in git), a self-hosted discovery index (needs hosting on theultimate.dev).

## Consequences

- No installer code to maintain. New harness support arrives through the tools, not through this repository.
- Two routes mean two explanations and a "don't install twice" caveat, because Route A namespaces skills by plugin and Route B installs them flat.
- A release must bump the marketplace versions or Route A users never see it. `scripts/validate.py` fails when the versions do not match the newest released changelog entry.
- The `skills` CLI cannot yet restore from its lockfile; project-scope users re-run `add`.

Revisit when a major harness gains first-class category installs, or when APM or Codex plugin demand shows up in issues.
