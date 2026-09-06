# The Ultimate Dev · Skills

The agent skills I use every day, in the open [Agent Skills](https://agentskills.io) format, grouped into categories you install with one command. They work in Claude Code, Codex, GitHub Copilot, Grok Build, Pi, Cursor, and any other harness that reads `SKILL.md`. I switch between several of those daily; this repository is how the same skill follows me across all of them.

A skill is a set of instructions your agent follows with your permissions. Read it before you install it.

## Categories

| Category | Skills | What it covers |
|---|---|---|
| `foundations` | [`decision-records`](skills/foundations/decision-records/SKILL.md) · [`release-process`](skills/foundations/release-process/SKILL.md) | What every project needs regardless of stack: a decision log that people and agents can read, and releases with a changelog and a tag on `main`. |
| `product-design` | [`guiding-product-discovery`](skills/product-design/guiding-product-discovery/SKILL.md) · [`shaping-product-briefs`](skills/product-design/shaping-product-briefs/SKILL.md) · [`designing-ux-flows`](skills/product-design/designing-ux-flows/SKILL.md) · [`exploring-visual-directions`](skills/product-design/exploring-visual-directions/SKILL.md) · [`building-html-prototypes`](skills/product-design/building-html-prototypes/SKILL.md) · [`preparing-implementation-handoffs`](skills/product-design/preparing-implementation-handoffs/SKILL.md) | Rough ideas through product/design handoff: requirements, UX, contrasting visual sketches, and refined offline HTML prototypes, with user decisions at milestones. |
| `product-engineering` | [`running-implementation-loops`](skills/product-engineering/running-implementation-loops/SKILL.md) · [`preparing-engineering-specs`](skills/product-engineering/preparing-engineering-specs/SKILL.md) · [`planning-implementation`](skills/product-engineering/planning-implementation/SKILL.md) · [`implementing-work-packages`](skills/product-engineering/implementing-work-packages/SKILL.md) · [`verifying-implementation`](skills/product-engineering/verifying-implementation/SKILL.md) · [`reviewing-code-changes`](skills/product-engineering/reviewing-code-changes/SKILL.md) · [`recording-worklogs`](skills/product-engineering/recording-worklogs/SKILL.md) · [`preparing-pull-requests`](skills/product-engineering/preparing-pull-requests/SKILL.md) | Agreed architecture through a verified PR: bounded implementation, model-tier routing, meaningful tests, review and repair, and resumable evidence. |

## From an idea to a design handoff

Start with `guiding-product-discovery` for the whole workflow, or invoke any specialist with the context you already have. The coordinator works without subagents; the specialists work without the coordinator. Each skill includes its own references and templates.

The usual sequence is a product brief, UX flows, visual direction briefs, three comparable HTML sketches, a selected and refined prototype, then a product/design handoff. You decide scope, choose a direction after viewing the sketches, and review readiness. Small features can combine documents and skip settled phases; proofs of concept focus on the question they need to answer.

The skills inspect project instructions, existing technology, and design assets. You choose whether existing visual language should be preserved, evolved, or replaced. No production stack is prescribed. Each prototype opens as one offline HTML file with embedded CSS, required assets, and minimal JavaScript; font fallbacks and simulated behavior are documented. The handoff prepares engineering planning rather than claiming implementation or deployment is complete.

Example requests (use the invocation syntax your agent supports):

```text
Use guiding-product-discovery to turn my rough idea for a learning journal
into a product/design handoff. Start from this project's instructions.

Use designing-ux-flows to work out filtering and empty-state recovery for
our saved collection. Keep the existing design and agreed product scope.

Use exploring-visual-directions to propose three contrasting directions
for this brief, paying particular attention to typography and spacing.

Use building-html-prototypes to render these three direction briefs as
independent offline HTML sketches with the same content and task.

Use preparing-implementation-handoffs to reconcile this brief, selected
prototype, and feedback into a handoff for engineering planning.
```

Install the category with `claude plugin install product-design@theultimate-dev` after adding the marketplace, or `npx skills add theultimate-dev/skills/skills/product-design`. The routes below explain setup and updates.

## From a design handoff to a verified PR

Start with `running-implementation-loops` for the whole engineering workflow. It consumes the product-design handoff or equivalent requirements, inspects the code, and prepares consequential architecture choices for your agreement. Within that baseline, it coordinates implementation packages, tests, independent review where supported, defect repair, integration, and an open PR within your authorization.

The loop plans verification before coding. Unit, integration, and critical E2E checks cover the behavior and boundaries that matter; reviewers examine tests as well as code. Confirmed actionable defects are repaired at every priority. Combined changes receive aggregate verification, and evidence records the revision actually checked. Missing mandatory checks remain blockers.

Agents and model tiers are discovered from the host, with reasoning effort chosen separately from change risk. No model or custom agent names are hardcoded. Hosts without these controls run with explicit limitations. A factual worklog supports resumption, and small tasks can combine specification, plan, review, and evidence sections in one document.

Install with `claude plugin install product-engineering@theultimate-dev` after marketplace setup, or `npx skills add theultimate-dev/skills/skills/product-engineering`. Invoke only the coordinator for the complete loop; each specialist also works on its own. Publication follows the project's permissions, and merge, release, and deployment remain separate.

```text
Use running-implementation-loops with this product/design handoff.
Work out the consequential architecture choices with me, then implement
and verify the agreed scope. Prepare a PR for my review.

Use reviewing-code-changes to review this package against its plan,
including test quality. Record findings and verify the subsequent fixes.

Use verifying-implementation to challenge this test strategy before
coding, then record acceptance evidence against the implemented revision.
```

The [evaluation exercises](evaluations/product-engineering/README.md) describe isolated behavioral trials and their observed limits.

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
