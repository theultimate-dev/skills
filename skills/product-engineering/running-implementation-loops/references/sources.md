# Maintained guidance

Reviewed 2026-09-06. These sources inform the workflow; they do not prove its effectiveness in every host. Recheck relevant primary guidance when capabilities change or evaluations expose a gap. Do not fetch every source for every task or embed a model catalog in the skill.

- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): curate relevant context, retrieve detail when needed, and preserve durable notes for long tasks.
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system): bounded delegation, clear output contracts, and evaluating outcomes. Its research workload does not establish an optimal number of coding agents.
- [Effort controls](https://platform.claude.com/docs/en/build-with-claude/effort): an example of provider-specific runtime controls. Discover supported settings in the active host; conceptual effort levels here are not portable API values.
- [Playwright best practices](https://playwright.dev/docs/best-practices): user-visible behavior, isolated tests, resilient locators, and waiting assertions. Apply to browser tests without imposing this framework on unrelated software.
- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents): evaluate actual outcomes, combine appropriate graders, and distinguish capability trials from regression protection.

The tier table, artifact contract, all-defect repair gate, and escalation policy are design choices for this loop. Validate them through the accompanying scenarios and real project use rather than presenting them as established universal best practices.
