# Sources for the product-engineering skills

Maintainers' list. Reviewed 2026-09-25: every link below was fetched on that date and matched its description. These sources inform the loop's design. They do not prove that it works on any given host; the [scenario catalog](evaluation-scenarios.md) and [results](results.md) are where that is tested. Recheck a source when host capabilities change or a trial exposes a gap. The skills themselves name tools by capability, with dated examples, and link to none of these pages.

## Agent design and evaluation

- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (Anthropic, 2025-09-29): curate the smallest high-signal context, retrieve detail just in time, and use compaction, structured notes or sub-agents for long tasks. Informs the task briefs, the lens briefs, and loading references only when needed.
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (Anthropic, 2025-06-13): give each subagent an objective, an output format, tool guidance and clear boundaries, and evaluate the end state rather than the steps. Informs the parallel lens reviewers and outcome-based grading. Its research workload does not establish the right number of coding agents.
- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (Anthropic, 2026-01-09): combine code-based, model-based and human graders, grade outcomes as well as transcripts, separate capability evals from regression evals, and read pass@k and pass^k over repeated trials. Informs the method section of the scenario catalog and the three-trial minimum.
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) (Claude Code documentation; the older `anthropic.com/engineering/claude-code-best-practices` address redirects here): give the agent a check it can run and have it show evidence, let it interview you and write a spec for larger features, explore and plan before coding, and review in a fresh context. Informs G1, G3 and the fresh-context review.

## Verification

- [Playwright best practices](https://playwright.dev/docs/best-practices): test user-visible behavior, isolate tests, prefer role and text locators, and use web-first assertions that wait. Applies to browser checks without imposing Playwright on projects that use other tooling.

## Pull requests and merging

- [`gh pr merge`](https://cli.github.com/manual/gh_pr_merge) (GitHub CLI manual): `--match-head-commit` makes the merge fail unless the PR head is the given SHA; `--auto` merges once requirements are met; `--admin` bypasses requirements and merge queues. Informs the head-pinned merge gate and the rule never to use `--admin`.
- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) (GitHub Docs): required approving reviews, required code-owner review, required checks and merge queues. On GitHub Free, protected branches work only in public repositories. Informs the merge gate and the disposable-repository trials.
- [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) (GitHub Docs): CODEOWNERS is read from `.github/`, the root, then `docs/`; the last matching pattern wins; owners can be users, teams or email addresses; an owner without write access is not assigned. Informs the host-protection rule in PR categorization and the fixture's `CODEOWNERS`.

## Design choices, not established practice

The four gates, the track table, the `human` and `agent` categories with their defaults, the five lenses, the three-round review limit, the two-attempt rule, and stack depth 1 are design choices for this loop, recorded in [decision 0009](../../decisions/0009-product-engineering-front-loaded-loop.md). Validate them through the scenarios and real project use rather than presenting them as universal best practice.
