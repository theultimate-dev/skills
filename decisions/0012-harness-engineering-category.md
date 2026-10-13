# 0012: Package harness improvement as a `harness-engineering` category

- Status: accepted
- Date: 2026-10-12

## Context

A harness is everything a coding agent runs under apart from the model: instruction files such as AGENTS.md and CLAUDE.md, skills, memory, hooks, permissions and settings, sub-agents, tool configuration, the repository checks the agent relies on, and the prompts its user writes. The first skill of this kind, `marginal-gains`, reads a finished session and proposes the two or three smallest harness changes that would pay off most, keeping a ledger so the gains compound from one session to the next. More skills about the harness are planned. Decision 0008 rejected a broad `agent-engineering` category because it would also hold agent design, which overlaps `product-engineering`, and harness-specific configuration, which 0002 sends to a separate repository.

## Options

1. **Add the skill to `prompt-engineering`.** Most suggestions edit text the model reads, and `improving-prompts` already treats agent operating instructions as a destination. But many suggestions are hooks, permissions, and repository checks, the plugin's promise of turning a rough prompt into an engineered one would have to stretch, and every planned harness skill would land in a category named for prompts.
2. **A `harness-engineering` category.** Names what the skills improve and the term readers look for, and holds the planned skills without stretching another category. Costs a fifth plugin that starts with one skill.
3. **Add it to `foundations`.** That category promises what every project needs; a harness belongs to a person and spans projects, so the category description would stop being true.

## Decision

Option 2. `harness-engineering` is a category and plugin, starting with `marginal-gains`.

- Its skills improve the harness a person runs agents under, across projects: what the agent reads, the controls around it, the checks it relies on, and how its user prompts it. Product code is out of scope.
- They stay harness-neutral under 0002. They work from what the harness has loaded into the session and name mechanisms generically, such as instruction file, hook, or permission rule, never a particular harness's paths or frontmatter. Harness-specific skills still belong to the separate repository 0002 plans.
- Engineering a single prompt stays in `prompt-engineering`. A harness skill may suggest rewriting an instruction; it does not carry the technique catalog.
- `marginal-gains` keeps its state in a ledger file at user level, outside any repository by default, at a path the user chooses.

## Consequences

- A fifth plugin. Its first release, `harness-engineering--v0.1.0`, is a minor marketplace release under 0011.
- The boundary with `prompt-engineering` needs watching, because instruction wording is context engineering in both. New skills follow the rule above: one prompt belongs to `prompt-engineering`, the system of files, controls, and checks around the agent to `harness-engineering`.
- The category holds one skill until the next harness skill arrives. Folding it into another category later would be breaking for the marketplace.
- The ledger is the first skill state in this repository that lives outside a project. Its format, the ranking, and the suggestion card are design choices to validate on real sessions; a small evaluation set is the natural follow-up.
