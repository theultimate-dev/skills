# 0008: Package prompt and context engineering as a `prompt-engineering` category

- Status: accepted
- Date: 2026-09-16

## Context

The skills so far cover project hygiene (`foundations`) and delivery workflows (`product-design`, `product-engineering`). Improving a prompt before it is sent is neither: it is a per-request craft that applies in every harness, chat client, and pipeline, whatever the project. The first skill of this kind rewrites a user's prompt using current prompt and context engineering practice and explains which techniques it applied and which it rejected.

Two constraints shape the packaging. Skills stay harness-neutral and carry only three frontmatter fields (0002), so argument handling and invocation rules live in the description and body. Prompt work must also run where nobody can answer a question, such as a non-interactive run, so the skill cannot depend on a dialogue.

## Options

1. **Add the skill to `foundations`.** One category fewer, but `foundations` promises what every project needs regardless of stack, and a prompt improver is not project-scoped; the category description would stop being true.
2. **A narrow `prompt-engineering` category.** Matches how users look for the capability and leaves room for related skills such as writing system prompts, designing tool descriptions, and prompt evaluations.
3. **A broad `agent-engineering` category.** Would also hold agent design and harness configuration, overlapping the routing guidance in `product-engineering` and the harness-specific repository planned in 0002.

## Decision

Option 2. `prompt-engineering` is a category and plugin, starting with `improving-prompts`.

- The technique catalog is model-neutral. Model-specific adjustments live in one reference that carries a review date and is applied only when the user names the target model or family.
- The skill runs in one pass and never blocks on questions, except when no prompt was supplied. Facts it cannot infer become bracketed placeholders listed in the report.
- The output contract is fixed: diagnosis, techniques applied with reasons, techniques rejected with reasons, assumptions and placeholders, settings that belong outside the prompt, then the enhanced prompt inside an `enhanced_prompt` tag as the last thing in the reply.
- Each technique group is a separate reference linked from `SKILL.md`, so a run loads only the groups it applies or rejects on a judgment call.

## Consequences

- A fourth plugin with one skill; adding it is a minor version bump under 0005.
- The model-family notes go stale as providers ship new generations. The review date makes that visible; rechecking them is part of maintaining the category.
- The catalog's apply and reject criteria, severity scale, and output contract are design choices to validate on real prompts, not established practice; a small evaluation set is the natural follow-up.
- Prompts that need harness-specific features, such as argument hints or invocation gating, still cannot get them here, per 0002.
