# Conventions lens

Judge whether the change follows the project's written rules, and whether it uses the language and its libraries the way they are meant to be used in this specific scenario. Every finding cites a source: a written rule, a linter rule, neighboring code, or the documentation of the language or library. Personal taste with no source is a nit at most, or dropped.

## Read first

1. The project's written rules: AGENTS.md and CLAUDE.md at the root and in the changed directories, CONTRIBUTING.md, style guides, and the commit and PR conventions they state.
2. The tool configuration: linter (`eslint.config.*`, `.eslintrc*`, `biome.json`, `ruff.toml` or `[tool.ruff]`, `.golangci.yml`, `clippy.toml`), formatter (`.prettierrc`, `rustfmt.toml`, `.editorconfig`) and type checker (`tsconfig.json`, mypy or pyright settings).
3. The language and library versions in the manifests and lockfiles (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`). Judge every idiom against those versions.
4. Two or three neighboring files that do the same kind of work as each changed file.

## Check the written rules first

1. Check each written rule that applies to the changed files. Quote the rule and name its file.
2. Run the project's lint, format and type-check commands on the changed files in check mode. Report each failure with its rule ID.
3. No new suppression (`eslint-disable`, `# noqa`, `# type: ignore`, `@ts-ignore`, `@ts-expect-error`, `//nolint`, `#[allow(...)]`) without the justification the project requires.
4. Naming, file placement, module layout, export style and test placement match the neighbors.
5. The mechanisms the rules name are used: the project's logger instead of `console.log` or `print`, its i18n layer for user-visible strings, its error types, its feature-flag helper.
6. Generated files are regenerated, not edited by hand. Lockfiles change only through the package manager.
7. Comments explain why, not what. No commented-out code. TODOs follow the project's format. Public APIs carry the documentation the project requires.
8. Commit messages and the PR title follow the project's stated convention.
9. For a docs-only change, the written rules are the documentation style guide, the Markdown linter configuration, and the project's heading, link and terminology conventions. Skip the idiom checks.

## Then check the idioms

For each changed construct, ask two questions: does the language or library offer a construct made for exactly this scenario, and does the change use it? These rows are examples, not a checklist.

| Scenario | Idiomatic | Flag |
|---|---|---|
| Iterating with an index, or over pairs | `enumerate`, `zip`, `for…of`, `entries()`, iterator adapters | `range(len(x))`, `for…in` over an array |
| Releasing a resource | `with`, `using` or `await using`, `defer`, try-with-resources, RAII | a manual close that an exception skips |
| Independent async calls | `Promise.all`, `asyncio.gather` or task groups, `errgroup` | an `async` callback passed to `forEach`, a promise nobody awaits |
| Errors | wrapping with context (`%w` with `errors.Is` or `errors.As`, `raise … from err`, `?` with the project's error type), throwing `Error` objects | bare `except:`, an empty `catch`, throwing strings, `_ =` on a Go error, `unwrap()` in library code |
| Types | narrowing, exhaustive `switch` with a `never` check, discriminated unions | `any`, an `as` cast that silences the checker, a non-null `!` with no guard |
| Framework work | the framework's own API: values derived during render instead of `useEffect` plus `setState`, `get_object_or_404`, schema validation (Pydantic, Zod) instead of hand-checked dictionaries, `URL` and `URLSearchParams` instead of string concatenation | a hand-rolled version of what the framework provides |
| Deprecated APIs | the documented replacement for the pinned version | `datetime.utcnow()` on Python 3.12 or later, `url.parse` in Node, `defaultProps` on React function components |
| Mutation | copies where the framework expects immutability | mutating props or state, mutable default arguments |

- The source for an idiom is the language or library documentation, a linter rule, a style guide the project adopts (PEP 8, Effective Go, the Rust API Guidelines), or consistent practice in neighboring code.
- Consistency beats a better idiom. When the project uses pattern X throughout, do not ask for Y in this PR; name Y as a follow-up if it matters.
- Deprecation beats consistency. A new use of a deprecated API is a finding even when neighboring code still uses it.
- A suggestion that needs a newer language or library version than the project pins is not a finding.

## Leave to other lenses

- Reuse of existing utilities and abstractions, layering and module boundaries, including written layering rules: architecture. Written style, naming and idiom rules stay here.
- The runtime cost of a construct: efficiency.
- Security-relevant idioms such as parameterized queries and output escaping: security.
- Whether the behavior is right: intent. When an idiom mistake causes wrong behavior, such as an unawaited promise that drops an error on an acceptance-criterion path, report it as a defect with its trigger. The synthesis merges it with any intent finding.

## Evidence bar

- `basis` names the source: the rule's file and wording, the linter rule ID, the documentation page, or the neighboring files by path.
- For an idiom finding, `trigger` states the concrete downside: the leaked resource, the swallowed error, the lost type check, the rule a reader or a tool will trip over.
- With no source, a finding is a nit at most. Drop it when it is only taste.

## Severity

| Severity | Conventions examples |
|---|---|
| `blocking` | A check the CI enforces fails: lint, format or type check. A written rule marked mandatory whose breach breaks something, such as a hand-edited generated file the next generation overwrites. An idiom mistake that causes a confirmed defect on an acceptance-criterion path takes that defect's severity. |
| `should-fix` | A written rule broken. A new suppression without justification. A deprecated API with a supported replacement. An idiom mistake with a concrete downside: a resource leak, a swallowed error, a lost type check. |
| `nit` | An idiom improvement with no defect. A name the rules allow but the neighbors do not use. |

A confirmed defect in changed code is never a nit.

## Output

Return one block per finding, most severe first:

```text
lens: conventions
file: <path>
line: <line at the head SHA>
severity: blocking | should-fix | nit
status: confirmed | unconfirmed
summary: <one sentence: what is wrong>
trigger: <the concrete downside, or the rule the code breaks>
impact: <who or what is hurt, and how badly>
evidence: <quoted code, the linter output, or the neighboring code>
basis: <the rule's file and wording, the linter rule ID, or the idiom's source>
direction: <the idiomatic or rule-conforming form>
```

After the blocks, add one line: `Checked: <rules, tools and files you examined>`.

When the diff does not touch this lens's concerns, answer only `conventions: nothing in scope (<reason>)`. When you checked and found nothing, answer only `conventions: no findings. Checked: <rules, tools and files you examined>`.
