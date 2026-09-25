# Driving the app

How the agent observes the running product. Choose by capability first. The tools are examples, and they change over time.

## Contents

- Capabilities
- Example tools (reviewed 2026-09-25)
- Picking a tool
- Probing a tool
- When no tool fits

## Capabilities

| Capability | What the agent can observe with it | Typical layers |
|---|---|---|
| Drive a real browser | Navigate; act on elements by accessible role or name; read DOM text; read console messages and network requests; take screenshots; resize the viewport; slow down or fail the network | `e2e`, `visual`, `accessibility` |
| Call an HTTP API | Status, headers and body for any method, as any account | `api` |
| Run a CLI | Stdout, stderr, exit code, files written | `cli` |
| Exercise a library | Return values and errors of the public API, through a scratch script | `integration` |
| Inspect persisted state | Database rows, files on disk, stored objects, cache entries | The side effect of any row; `migration` |
| Capture outbound side effects | Emails, webhooks, queue messages, log lines the app emits | `job`, notification criteria |
| Drive a native mobile or desktop UI | Screens, taps or clicks, text on screen | `e2e` for native apps |

## Example tools (reviewed 2026-09-25)

| Capability | Example tool | What matters for verification |
|---|---|---|
| Drive a real browser | Playwright MCP | Acts on elements through references from an accessibility snapshot; reads console and network; `--isolated` starts each session with a clean profile |
| | Playwright CLI (`playwright-cli`) | The same model from the shell; saves snapshots to disk instead of returning them into context, so it costs fewer tokens; named sessions with `-s=<name>` |
| | Chrome DevTools MCP | Console with source-mapped stacks, network detail, performance traces, network and CPU throttling |
| | Claude in Chrome | Drives the user's own Chrome and shares its signed-in sessions; runs in a visible window; pauses on login pages and CAPTCHAs for the user |
| | Playwright test runner (`npx playwright test`) | Repeatable checks that run in CI; traces on failure |
| Call an HTTP API | curl, HTTPie | One cookie jar per account keeps sessions apart |
| Run a CLI | The app's own CLI, the shell | |
| Exercise a library | A scratch script in the project's language, a REPL | |
| Inspect persisted state | psql, mysql, sqlite3, redis-cli, mongosh, the framework's console | Read-only queries |
| Capture outbound side effects | A local mail catcher such as Mailpit, a local webhook sink, the payment provider's CLI in test mode | |
| Drive a native UI | The platform's UI test runner (XCUITest, Espresso), Maestro, Appium, a computer-use tool | |

Check a tool's current behavior on the host before relying on a detail in this table.

## Picking a tool

| Situation | Prefer | Why |
|---|---|---|
| The check must rerun in CI | The project's test runner | Repeatable, versioned, leaves traces |
| Observing a criterion once, or the exploratory pass | A browser-driving agent tool with an isolated session (Playwright MCP, Playwright CLI) | Quick to drive, reads the accessibility tree, starts from clean state |
| A long session or a tight context budget | Playwright CLI over Playwright MCP | Output lands on disk; the agent reads only what it needs |
| Console, network or performance depth; throttling | Chrome DevTools MCP | The fullest DevTools access |
| The flow needs the user's real browser: an extension, single sign-on, a visual check the user watches | Claude in Chrome, on local or ephemeral URLs only | It carries the user's real signed-in sessions, production accounts included |
| The behavior has no UI, or the UI hides the detail | An API call, a CLI run, a database query | Faster and more precise. A user-facing criterion still gets one run through the UI |

Tie-breakers, in order:

1. The tool the project already uses.
2. The tool the profile confirmed.
3. An isolated session over a shared one.
4. One tool per capability for the whole work item, so evidence stays comparable.

## Probing a tool

A tool counts as available only after it worked on this host:

- Browser: open the readiness URL and read one heading by its role.
- HTTP: request the readiness URL and read the status.
- CLI: run its help or version command and read the exit code.
- Database: run a read-only count on a seeded table.
- Mail catcher: list its messages through its UI or API.

Record the probe and the date in the profile's tool table. Another host or machine may expose different tools, so a later session probes again.

## When no tool fits

A layer without a tool stays unverified. Reading the code, the diff or a test file is not an observation of the running product, and it never substitutes for one.

Mark the row `blocked` and name the missing capability. Then take one of three paths with the user at G3: propose the gap for Plan 0, reword the AC to something an available tool can observe, or move the row to the human eye, where it is reported `blocked (human eye)` with a screenshot and puts its pull request in the `human` review category. A row left `blocked` stops its slice before the PR opens and escalates as "the verification contract cannot run".
