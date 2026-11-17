# 0021: Package machine upkeep as a `dev-environment` category whose skills may ship shell scripts

- Status: accepted
- Date: 2026-11-17

## Context

Some recurring work is upkeep of the machine a person develops on, not of a product or a harness: a Docker disk that fills up, caches that grow, tools that drift. The first case is a Docker cleanup that removes unused data older than a chosen age. Docker cannot filter volumes by age, so the cleanup needs a loop over volumes with date arithmetic, and it deletes data. Written as prose, the agent would rewrite that loop on every run, and a mistake in it removes the wrong volumes. No existing category fits: `foundations` is what every project needs, `harness-engineering` is the agent's harness, and the product categories are about a product. Decision [0017](0017-browser-only-checks-for-html-prototypes.md) noted that no skill ships executable code and rejected a Python script because it assumes a runtime the frontmatter cannot declare under [0002](0002-agent-skills-open-format.md); it named a script as something to revisit.

## Options

1. **Commands written out in `SKILL.md`, no script.** Nothing executable to maintain. Lost: the agent reassembles a destructive loop each time, so a dry run proves that run's commands, not the skill's.
2. **A new `dev-environment` category whose skills may ship shell scripts in `scripts/`.** The cleanup repeats exactly, has one dry run, and can be read and tested once. The shell is the runtime the commands already need. Won.
3. **Put the skill in `foundations`.** No new plugin. Lost: a full Docker disk is not something every project needs, so the category description would stop being true, and every later upkeep skill would land there too.

## Decision

Option 2. `dev-environment` is a category and plugin, starting with `reclaiming-docker-disk-space`, and a skill may ship shell scripts.

- **Scope**: the category's skills keep the machine a person develops on in working order: disk, containers, caches, local tools. Product code and the agent's harness are out of scope.
- **Where scripts live**: `skills/<category>/<skill>/scripts/`, the directory the Agent Skills format names for executable code. `SKILL.md` links each script and says how to run it.
- **Runtime**: a script may assume only bash 3.2 or newer and the tools the skill's subject already implies, such as the `docker` CLI for a Docker skill. It works on macOS and Linux without installing anything. The skill's text states what the script needs, because the frontmatter cannot.
- **How it is run**: with `bash <path>`, never by relying on the executable bit, which installers and zip archives do not all preserve.
- **Deleting**: a script that removes data has a dry run that removes nothing and lists what would go, and the skill requires the user's yes before the real run.
- 0017 stays in force for the HTML prototype checks, which run in a browser the verification already uses. Python and other runtimes stay out of skills.

## Consequences

- A destructive routine runs the same way on every machine and can be tested once, instead of being rewritten per session.
- Shell scripts are now code in the skills tree. They need review, a syntax check and a run on both macOS and Linux before release, and the validator does not check them yet.
- A script cannot run in a GUI client without a shell. There the skill's text still describes what to remove, but the cleanup is manual.
- An eighth plugin that starts with one skill. Its first release, `dev-environment--v0.1.0`, is a minor marketplace release under [0011](0011-marketplace-release-with-every-plugin-release.md).
- Revisit if a script needs a runtime beyond the shell, or if scripts multiply enough to need a check in `scripts/validate.py`.
