# Maintained guidance

Reviewed 2026-09-16. These sources inform the technique catalog; they do not prove that a technique improves a given prompt. Recheck the primary guidance when a provider ships a new model generation or when an enhanced prompt underperforms. Do not fetch every source for every prompt.

- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices): clarity, motivation, examples, tags, roles, long context, output control, prefill migration, tool use, thinking, and agentic systems for current Claude models.
- [Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) and [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5): the dated model-family adjustments.
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): altitude, minimal complete context, just-in-time retrieval, compaction, notes, subagents, context rot.
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents): chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, simplicity, tool design.
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching): static-first ordering and what invalidates a cached prefix.
- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) and [Mitigate jailbreaks and prompt injections](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks): uncertainty, quotes, citations, restriction to sources; the untrusted-content policy, tool-result delivery, JSON encoding, screening, least privilege.
- [Define success criteria](https://platform.claude.com/docs/en/test-and-evaluate/define-success): properties and dimensions of good criteria.
- [Claude Code best practices](https://code.claude.com/docs/en/best-practices): verification targets, specific context, explore-plan-implement, instruction files, interview-first specs, adversarial review. Harness features named there are not assumed by this skill.
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): progressive disclosure, conciseness, degrees of freedom; informs the shape of this skill.
- [Best practices for prompt engineering](https://claude.com/blog/best-practices-for-prompt-engineering): start simple, one technique per problem, test each addition.
- [GPT-5.2 prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide): eagerness, preambles, length constraints, schema nulls, citations, compaction consistency.
- [Gemini prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies): ordering, default parameters, built-in thinking, consistent examples, grounding.

The destination classification, the severity scale, the apply and reject criteria, and the output contract are design choices of this skill. Validate them on real prompts and the results they produce rather than presenting them as established universal practice.
