# Driving the app

How the agent observes the running product, and how to operate the tools so the observation holds up. Choose by capability first. The tools are examples, and they change over time.

## Contents

- Capabilities
- Example tools (reviewed 2026-09-25)
- Picking a tool
- When no tool fits
- Start the app and wait for readiness
- Locate elements
- Wait for conditions, not time
- Capture console, network and server errors
- Act as a second user
- Verify persistence
- APIs, CLIs, libraries and stored state
- Network, viewport and keyboard
- Capture evidence
- Credentials
- Tool trouble
- Clean up

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

Tie-breakers, in order: the tool the contract names; the tool the profile confirmed; an isolated session over a shared one; one tool per capability for the whole run, so evidence stays comparable.

## When no tool fits

A layer without a tool stays unverified. Reading the code, the diff or a test file is not an observation of the running product, and it never substitutes for one. Mark the row `blocked`, name the missing capability, and report it. The slice stops before its pull request opens and escalates: the verification contract cannot run (G3). Only a row the user agreed at G3 to certify by eye is `blocked (human eye)`: it goes to the user with a screenshot, its pull request is `human`, and the loop continues.

## Start the app and wait for readiness

Start the app yourself, from the checkout at the SHA under test, as a background process the host keeps running: a background shell job, or the host's background-task feature. Send its output to a log file and write the PID to a file, because shell variables may not survive between tool calls. `RUN_DIR` depends only on the commit, so set it again the same way in every call. Put logs, cookie jars, evidence and worktrees under it.

```sh
RUN_DIR="${TMPDIR:-/tmp}/verify-$(git rev-parse --short HEAD)"; mkdir -p "$RUN_DIR"
pnpm dev > "$RUN_DIR/app.log" 2>&1 &
echo $! > "$RUN_DIR/app.pid"
```

Poll the readiness signal from the profile with a bound. Stop early when the process has died.

```sh
for i in $(seq 1 90); do
  curl -fsS -o /dev/null http://localhost:3000/health && echo ready && break
  kill -0 "$(cat "$RUN_DIR/app.pid")" 2>/dev/null || { echo "app exited"; tail -n 40 "$RUN_DIR/app.log"; break; }
  sleep 1
done
```

A short sleep inside a bounded poll on a condition is correct. A fixed sleep in place of the condition is not. On timeout, quote the last log lines in the report and mark the dependent rows `blocked`.

Before starting, check the port. A port held by a process you did not start stays untouched: use another port, or mark the rows `blocked`.

## Locate elements

Take an accessibility snapshot, then act by what the user perceives. In order of preference:

1. Role and accessible name: button "Save", textbox "Title", link "Settings".
2. The label of a form field.
3. Visible text.
4. A test id the project already uses.

Never target CSS classes, positional selectors or XPath; they break on harmless markup changes and do not reflect what the user sees. An interactive element with no accessible name is an `accessibility` finding in its own right. Snapshot references are valid for one snapshot only: take a fresh snapshot after navigation or a re-render.

## Wait for conditions, not time

Wait for the thing the user would wait for: text appears, a spinner disappears, the URL changes, a specific response arrives.

- Agent browser tools: the tool's wait-for-text or wait-for-condition action (Playwright MCP `browser_wait_for`, Chrome DevTools MCP `wait_for`).
- Test runner: assertions that retry until a timeout, such as `await expect(page.getByRole('status')).toHaveText('Saved')`.

A fixed sleep hides races and slows every run. When one is unavoidable, such as an animation with no end signal, keep it short and say so in the report.

## Capture console, network and server errors

1. Load the page and record the console errors and failed requests that exist before the journey. Those are the baseline for this page.
2. Run the journey.
3. Read the console at error and warning level, and list the network requests. Flag every 4xx and 5xx response and every failed or aborted request.
4. Read the server log for errors and stack traces written during the journey.

Examples: Playwright MCP `browser_console_messages` and `browser_network_requests`; Playwright CLI `console` and `requests`; Chrome DevTools MCP `list_console_messages` and `list_network_requests`.

A failure the row expects, such as the 404 of a denied-access check, is part of the pass condition, not an error. Anything new and unexpected makes the row `fail`, unless the same error also occurs on the base; then report it as pre-existing.

## Act as a second user

Permission criteria need two principals in fully separate sessions:

- Agent browser tools: a second isolated session (Playwright MCP started with `--isolated`, a Playwright CLI session such as `-s=user-b`).
- Test runner: a second browser context.
- HTTP: a second cookie jar (`curl -c "$RUN_DIR/b.jar" -b "$RUN_DIR/b.jar"`) or a second token.

Sign in as user B through the UI or the API with B's own environment variables. Never reuse user A's cookies or tokens. Check both paths: B does not see A's record in any list, and B's direct request for A's record (by URL and by API) is denied without leaking content. Check the signed-out case as well.

## Verify persistence

Choose the strength the pass condition names, from weakest to strongest:

1. Reload the page.
2. Navigate away and come back.
3. Start a new session as the same user.
4. Restart the app process. This catches data held only in memory.
5. Read the store directly with a read-only query or a file read.

Any criterion that creates, updates or deletes data gets at least a reload and one direct read of the store:

```sh
psql "$DATABASE_URL" -At -c "select title from tasks where title = 'verify-1727262000'"
```

## APIs, CLIs, libraries and stored state

- **API:** record the method, the path, the status and the relevant body fields.
  ```sh
  curl -sS -b "$RUN_DIR/a.jar" -o "$RUN_DIR/body.json" -w '%{http_code}\n' http://localhost:3000/api/tasks
  jq -r '.[].title' "$RUN_DIR/body.json"
  ```
- **CLI:** capture stdout, stderr and the exit code separately, then inspect any files it wrote.
  ```sh
  ./bin/export --out "$RUN_DIR/out.csv" > "$RUN_DIR/stdout.txt" 2> "$RUN_DIR/stderr.txt"; echo "exit=$?"
  ```
- **Library:** write a scratch script outside the working tree that imports only the public API, prints the results, and is deleted afterwards.
- **Stored state:** read-only queries. Destructive statements run only against a local database the agent created or seeded, and only when the contract's limits allow it.
- **Outbound side effects:** read the mail catcher or the webhook sink, never a real inbox.

## Network, viewport and keyboard

- **Slow or offline network:** Chrome DevTools MCP `emulate` offers Slow 3G, Fast 3G and Offline, plus CPU throttling.
- **A failing request:** make one endpoint return 500 (Playwright MCP `browser_route`, the test runner's `page.route`), or stop a local backend service briefly. Observe the error state and confirm no data was lost.
- **Viewport:** resize to about 375 by 812 and 1280 by 800 (Playwright MCP `browser_resize`, `playwright-cli resize 375 812`, Chrome DevTools MCP `resize_page`). Check that nothing overflows horizontally (`document.documentElement.scrollWidth <= window.innerWidth`), that controls stay reachable, and that text is not clipped.
- **Keyboard only:** Tab through the flow from the top of the page. Every focused element is visible and in a sensible order; Enter and Space activate controls; Escape closes dialogs and returns focus to the control that opened them.

## Capture evidence

- Quote text first: the heading, the list entry, the message, the status code, the row.
- Take a screenshot for every visual or human-eye row and for every failure.
- Save screenshots and traces outside the working tree, for example in `"$RUN_DIR/evidence/"`, or in the path the profile names. In CI they are uploaded as artifacts. Reference them by path or artifact name.
- Use seeded data only, so screenshots hold no real personal data.

## Credentials

- Test accounts exist only in local or ephemeral environments. Their values come from environment variables named in the profile.
- Check that a variable is set without printing it, and print only the host of a URL variable, to compare with the allowed environments:
  ```sh
  test -n "${DATABASE_URL-}" && echo "DATABASE_URL set" || echo "DATABASE_URL unset"
  printf '%s\n' "$DATABASE_URL" | sed -E 's#^[^:]+://([^@/]*@)?([^:/?]+).*#\2#'
  ```
- Typing a password through a browser tool records it in the tool log. Use credentials that are worthless outside the local environment, and never type real personal credentials.
- When the tool can load a saved session (Playwright MCP `--storage-state`), sign in once with a script that reads the variables, and reuse the saved state.
- Never write a credential value into the report. Redact tokens, keys, cookies and connection strings from quoted logs and output.

## Tool trouble

A tool error is not a product failure. Re-probe the tool and retry once. If it still fails, mark the row `blocked` and quote the tool error. A row whose retry passes after a quoted tool error is `pass`; quote the error in the report. Any other failure followed by a pass on retry is `fail`.

Claude in Chrome stops on a JavaScript alert or confirm dialog, and pauses on login pages and CAPTCHAs for the user. In an unattended run, that makes the row `blocked`.

## Clean up

1. Stop every process you started. Package-manager scripts spawn children, so stop the process group, or the process listening on the port you started it on (`lsof -ti tcp:3000`), then confirm the port is free.
2. Stop only the containers you started: `docker compose -p <project> down`. Remove volumes only when you created them.
3. Close browser sessions (Playwright MCP `browser_close`, `playwright-cli close`).
4. Remove worktrees (`git worktree remove`), scratch scripts and cookie jars.
5. Confirm `git status` is clean and `HEAD` equals the recorded SHA.

Leave every process, container and file you did not create exactly as you found it.
