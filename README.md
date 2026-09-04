# The Ultimate Dev · Skills

The agent skills I use every day, in the open [Agent Skills](https://agentskills.io) format, grouped into categories you install with one command. They work in Claude Code, Codex, GitHub Copilot, Grok Build, Pi, Cursor, and any other harness that reads `SKILL.md`. I switch between several of those daily; this repository is how the same skill follows me across all of them.

A skill is a set of instructions your agent follows with your permissions. Read it before you install it.

## Categories

| Category | Skills | What it covers |
|---|---|---|
| `foundations` | [`decision-records`](skills/foundations/decision-records/SKILL.md) · [`release-process`](skills/foundations/release-process/SKILL.md) | What every project needs regardless of stack: a decision log that people and agents can read, and releases with a changelog and a tag on `main`. |

## Install

Two routes. Use one per machine; installing the same skill through both gives you two copies.

- **Route A, plugin marketplace.** You work in Claude Code or Copilot CLI and want categories as named, versioned plugins that update in place.
- **Route B, `npx skills`.** Any other harness, or you want one skill without the rest.

### Route A: plugin marketplace

Claude Code:

```bash
claude plugin marketplace add theultimate-dev/skills
claude plugin install foundations@theultimate-dev
```

Add `--scope project` to share a plugin with everyone working in the current repository.

Copilot CLI reads the same manifest:

```bash
copilot plugin marketplace add theultimate-dev/skills
copilot plugin install foundations@theultimate-dev
```

You get skills namespaced by category, for example `/foundations:decision-records`.

### Route B: `npx skills`

The [skills CLI](https://github.com/vercel-labs/skills) installs into 77 agents, Claude Code, Codex, Copilot, Grok Build, Pi and Cursor among them. It asks which agents to target and can symlink one copy into all of them.

```bash
# a whole category (the repository folder is skills/, hence skills/skills)
npx skills add theultimate-dev/skills/skills/foundations

# every agent on this machine, user scope, no prompts
npx skills add theultimate-dev/skills/skills/foundations -g -a '*' -y

# one skill
npx skills add theultimate-dev/skills --skill decision-records
```

You get flat skills invoked by name, `/decision-records` or `$decision-records` depending on the harness.

## Update

Releases drive both routes. A release bumps the plugin version in the marketplace manifest and tags `main`, so route A sees a new plugin version and route B gets the new content on update.

Route A:

```bash
claude plugin marketplace update theultimate-dev
claude plugin update foundations@theultimate-dev
```

Or turn it on once: `/plugin` → Marketplaces → `theultimate-dev` → Enable auto-update. Third-party marketplaces are off by default. With it on, Claude Code updates in the background after startup and prompts you to `/reload-plugins`.

Copilot CLI: `copilot plugin marketplace update theultimate-dev && copilot plugin update foundations`.

Route B:

```bash
npx skills update                      # everything this CLI installed
npx skills update decision-records -g  # one skill, user scope
```

## Pin a release

Route A: add the marketplace at a tag. To move to a newer tag, remove the marketplace (this uninstalls its plugins) and add it again.

```bash
claude plugin marketplace add https://github.com/theultimate-dev/skills.git#v0.1.0
```

Route B: a pinned install stays at its tag until you run `add` again with a new one.

```bash
npx skills add theultimate-dev/skills/skills/foundations#v0.1.0
```

## Remove

```bash
claude plugin uninstall foundations@theultimate-dev   # route A
claude plugin marketplace remove theultimate-dev      # route A; also uninstalls its plugins
npx skills remove decision-records                    # route B; `npx skills list` shows what is installed
```

## Other harnesses and GUI clients

Documented by the tools, not yet run by me. Open an issue if one misbehaves.

| Client | Install | Update |
|---|---|---|
| Pi | `pi install git:github.com/theultimate-dev/skills` (all categories; Pi reads nested folders) | `pi update git:github.com/theultimate-dev/skills` |
| APM | `apm install theultimate-dev/skills/skills/foundations` | `apm update` |
| Claude.ai, Claude Desktop, Cowork, ChatGPT | Download `<skill>-<version>.zip` from the [latest release](https://github.com/theultimate-dev/skills/releases/latest) and upload it in the client's skills settings | Upload the newer zip |

## Versioning

One version for the whole repository, [SemVer](https://semver.org/spec/v2.0.0.html), released from `v*` tags on `main`. Renaming or removing a skill or a category is a breaking change. Every change is listed in [CHANGELOG.md](CHANGELOG.md). The decisions behind this shape are in [decisions/](decisions/README.md).

## License

[MIT](LICENSE).
