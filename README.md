# The Ultimate Dev · Skills

The agent skills I use every day, in the open [Agent Skills](https://agentskills.io) format, grouped into categories you install with one command. They are written for any harness that reads `SKILL.md`: Claude Code, Codex, GitHub Copilot, Grok Build, Pi, Cursor, and others. I switch between several of those daily; this repository is how the same skill follows me across all of them.

A skill is a set of instructions your agent follows with your permissions. Read it before you install it.

## Categories

| Category | Skills | What it covers |
|---|---|---|
| `foundations` | [`decision-records`](skills/foundations/decision-records/SKILL.md) · [`release-process`](skills/foundations/release-process/SKILL.md) | What every project needs regardless of stack: a decision log that people and agents can read, and releases with a changelog and a tag on `main`. |
| `product-design` | [`guiding-product-discovery`](skills/product-design/guiding-product-discovery/SKILL.md) · [`shaping-product-briefs`](skills/product-design/shaping-product-briefs/SKILL.md) · [`designing-ux-flows`](skills/product-design/designing-ux-flows/SKILL.md) · [`exploring-visual-directions`](skills/product-design/exploring-visual-directions/SKILL.md) · [`building-html-prototypes`](skills/product-design/building-html-prototypes/SKILL.md) · [`preparing-implementation-handoffs`](skills/product-design/preparing-implementation-handoffs/SKILL.md) | Rough ideas through product/design handoff: requirements, UX, contrasting visual sketches, and refined offline HTML prototypes, with user decisions at milestones. |
| `product-engineering` | [`running-implementation-loops`](skills/product-engineering/running-implementation-loops/SKILL.md) · [`specifying-work-items`](skills/product-engineering/specifying-work-items/SKILL.md) · [`brainstorming-solutions`](skills/product-engineering/brainstorming-solutions/SKILL.md) · [`defining-verification`](skills/product-engineering/defining-verification/SKILL.md) · [`planning-implementation`](skills/product-engineering/planning-implementation/SKILL.md) · [`implementing-plans`](skills/product-engineering/implementing-plans/SKILL.md) · [`verifying-implementation`](skills/product-engineering/verifying-implementation/SKILL.md) · [`reviewing-code-changes`](skills/product-engineering/reviewing-code-changes/SKILL.md) · [`shipping-pull-requests`](skills/product-engineering/shipping-pull-requests/SKILL.md) | Specify by interview, brainstorm and pick an approach, agree how the agent verifies itself, approve the roadmap; then autonomous implementation, real verification in the running app, quick and five-lens review, and one PR per slice, merged by the agent when safe and authorized. |
| `prompt-engineering` | [`improving-prompts`](skills/prompt-engineering/improving-prompts/SKILL.md) | A rough prompt to an engineered one: destination and gap diagnosis, a technique catalog with apply and reject criteria, dated model-family notes, and a copy-paste-ready result with the reasoning behind it. |

Each category is a plugin with its own version and changelog: [`foundations`](skills/foundations/CHANGELOG.md) · [`product-design`](skills/product-design/CHANGELOG.md) · [`product-engineering`](skills/product-engineering/CHANGELOG.md) · [`prompt-engineering`](skills/prompt-engineering/CHANGELOG.md).

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

## From a work item to merged PRs

`product-engineering` runs one loop for everything from a one-line fix to a new app. You take part at the start; after that the agent works on its own and comes back only for PRs you want to see yourself, or when something changes what you agreed.

| Stage | Skill | Who | What comes out |
|---|---|---|---|
| Start or resume | `running-implementation-loops` | agent | The track for this work item; live state read from open and merged PRs |
| 1. Specify | `specifying-work-items` | you + agent | The agent interviews you about the unknowns, then writes `spec.md` with requirements and acceptance criteria |
| 2. Approach | `brainstorming-solutions` | you + agent | Two to four distinct approaches compared; you pick or combine one |
| 3. Verification | `defining-verification` | you + agent | How the agent proves each acceptance criterion in the running app, plus a reusable `verification-profile.md` for the project |
| 4. Launch | `planning-implementation` | you approve | `roadmap.md`: plans, phases, one PR per slice, which PRs need a human, and the autonomy contract (what the agent may push and merge) |
| 5. Implement | `implementing-plans` | agent | A branch and small commits for each PR slice |
| 6. Verify | `verifying-implementation` | agent | The app started and driven by browser, API or CLI; observed evidence for every acceptance criterion |
| 7. Quick review | `reviewing-code-changes` | agent | A fresh-context check that the change does what the spec says, before the PR exists |
| 8. Open the PR | `shipping-pull-requests` | agent | A PR with the verification report, marked `review:human` or `review:agent` |
| 9. Full review | `reviewing-code-changes` | agent | Up to five parallel reviewers, chosen by what the diff touches: architecture, security, conventions and idioms, efficiency, intent |
| 10. Land | `shipping-pull-requests` | agent or you | Agent PRs merge once approved, green on the reviewed head, and authorized; human PRs wait for you while the agent continues with independent work |

Not every work item needs every stage:

| Track | Stages |
|---|---|
| Quick fix | Implement, verify, PR with a review sized to the diff |
| Bugfix | A short spec from the repro, a failing check first, then the loop |
| Small change | The four starting stages in one message, one plan inline in the spec |
| Feature | All stages, one loop per PR slice |
| New app | `product-design` first if the product or UX is still open, then all stages with a walking skeleton as plan 1 |
| Refactor | Invariants in the spec, characterization checks before the first edit, small mechanical PRs |
| Spike | A timeboxed branch that is never merged; its findings feed the approach |

By default, the agent leaves these to your review: changes to authentication or authorization, crypto, secrets, payments or personal data; schemas, migrations and backfills; breaking public APIs; new or major-bumped dependencies; CI, infrastructure and build configuration; instruction files such as AGENTS.md; and user-visible UI, which you can release to the agent when you approve the roadmap. Deleted or weakened tests, unobserved acceptance criteria, and reviews that ran without a fresh context always go to you. Your project's pull request policy can change the defaults. The agent merges only with your recorded permission, only the exact commit it reviewed, never bypasses branch protection, never approves its own PR on the host, and asks before a merge that would deploy. Browser checks use whatever the agent can drive: Playwright MCP, Chrome DevTools MCP, Claude in Chrome, the Playwright test runner, or plain HTTP and CLI calls. A check that cannot run is reported as blocked, never as passed, and stops that slice until you decide how to verify it.

Install with `claude plugin install product-engineering@theultimate-dev` after marketplace setup, or `npx skills add theultimate-dev/skills/skills/product-engineering`. Start with the coordinator, or call any stage on its own:

```text
Use running-implementation-loops for this feature: saved searches with
email alerts. Interview me first, then take it all the way to PRs.

Use specifying-work-items to interview me about this bug report and
write the spec.

Use reviewing-code-changes to run the full five-lens review on PR 42.

Use shipping-pull-requests to open this branch as a PR and merge it if
it qualifies for agent review.
```

The [evaluation guide](evaluations/product-engineering/README.md) describes the behavioral trials and what they have shown so far. Track classification and full-review recall have been trialed; merge safety, stacked PRs and most other scenarios have not yet run on a real host, so treat the merge rules above as what the skills instruct, not yet as observed behavior.

## From a rough prompt to an engineered one

Hand `improving-prompts` the prompt you were about to send, in any language, for any model or harness. It works out where the prompt will run, diagnoses what is missing or in the way, and applies only the prompt and context engineering techniques that close those gaps. Missing facts become marked placeholders rather than invented details, and the skill never stops to ask questions, so it also works in non-interactive runs.

The reply is a short report and the prompt itself: the techniques applied and why, the techniques considered and rejected and why, the placeholders to fill, settings that belong outside the prompt text, and the enhanced prompt inside an `enhanced_prompt` tag, ready to copy. Name the target model to get the dated model-family adjustments; leave it out to get a neutral prompt.

Install with `claude plugin install prompt-engineering@theultimate-dev` after marketplace setup, or `npx skills add theultimate-dev/skills/skills/prompt-engineering`.

```text
Use improving-prompts on this prompt: "write a blog post about our new
export feature"

Use improving-prompts on the task below. It will run unattended in a
coding agent with the test suite available.

Use improving-prompts to turn this draft into a system prompt for a
support assistant that reads customer emails. Target Claude Opus 5.
```

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

The [skills CLI](https://github.com/vercel-labs/skills) installs into dozens of agents, Claude Code, Codex, Copilot, Grok Build, Pi and Cursor among them. It asks which agents to target and can symlink one copy into all of them.

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

The two routes update on different signals.

Route A updates a plugin when that plugin is released. Each release bumps the plugin's version in the marketplace manifest, and Claude Code and Copilot CLI fetch a new copy only when that version changes. A fresh install copies whatever is on `main` at that moment.

```bash
claude plugin marketplace update theultimate-dev
claude plugin update foundations@theultimate-dev
```

Or turn it on once: `/plugin` → Marketplaces → `theultimate-dev` → Enable auto-update. Third-party marketplaces are off by default. With it on, Claude Code updates in the background after startup and prompts you to `/reload-plugins`.

Copilot CLI: `copilot plugin marketplace update theultimate-dev && copilot plugin update foundations@theultimate-dev`.

Route B follows `main`, not releases. `npx skills update` reinstalls every skill whose folder changed on `main` since you installed it, released or not. To get released versions only, pin a release tag, as described below.

```bash
npx skills update                      # everything this CLI installed
npx skills update decision-records -g  # one skill, user scope
```

## Pin a release

Each plugin's releases are tagged `<category>--vX.Y.Z`, for example `foundations--v0.1.0`. The marketplace's own releases are tagged `vX.Y.Z`. The [releases page](https://github.com/theultimate-dev/skills/releases) lists them all with their notes.

Route A: add the marketplace at a tag. This pins the whole catalog, every plugin included, at that tag's commit, including any plugin changes merged but not yet released at that commit. To move to a newer tag, remove the marketplace (this uninstalls its plugins) and add it again.

```bash
claude plugin marketplace add https://github.com/theultimate-dev/skills.git#v0.1.0
```

Route B: pin each category at its own tag. A pinned install stays at its tag until you run `add` again with a newer one.

```bash
npx skills add theultimate-dev/skills/skills/foundations#foundations--v0.1.0
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
| Claude.ai, Claude Desktop, Cowork, ChatGPT | On the [releases page](https://github.com/theultimate-dev/skills/releases), open the newest `<category>--vX.Y.Z` release, download `<skill>-<version>.zip`, and upload it in the client's skills settings | Upload the zip from the category's next release |

## Versioning

Each category is a plugin with its own [SemVer](https://semver.org/spec/v2.0.0.html) version, changelog (`skills/<category>/CHANGELOG.md`), and releases, tagged `<category>--vX.Y.Z` on `main`. A plugin release carries that plugin's notes and one zip per skill. A new skill is a minor release of its plugin. Renaming or removing a skill is a breaking change, and until a plugin reaches 1.0.0 a breaking change bumps its minor version.

The marketplace is versioned too. [CHANGELOG.md](CHANGELOG.md) and `vX.Y.Z` tags cover plugins added, renamed, or removed, install routes, and release assets. Every plugin release is also a marketplace release, at least a patch, whose notes list each plugin released with a link to its release, so the Latest release on the [releases page](https://github.com/theultimate-dev/skills/releases) always names the newest plugin versions. The decisions behind this shape are in [decisions/](decisions/README.md).

## License

[MIT](LICENSE).
