# Scripted checks

## When a scripted check is required

A prototype breaks most often in its small state machines: a panel that opens and closes, a timer, focus that should return to its control, an ARIA state that should follow the UI. Exercise every stateful interaction the prototype demonstrates.

- **A browser-driving tool is available**, one that clicks, types and reads the page: drive each interaction with it, and record the check as `Driven: <name>`.
- **No browser-driving tool can exercise the interaction**, for example when the only browser is a headless one that loads a URL and dumps the DOM or takes a screenshot: a scripted check is required for each stateful interaction. Write it in the interaction harness, `templates/interaction-harness.html`, and record it as `Scripted: <name>`.

A screenshot shows a state; it does not exercise the behavior that leads to it. A click that also reaches a click-outside handler can open a panel and close it again within the same click, and every screenshot taken afterwards looks like a panel that never opened.

## The interaction harness

The harness loads the prototype in a same-origin frame served over local HTTP, runs the checks you write against it, and writes the results into the page.

- **Why HTTP and a frame.** Most browsers treat each `file://` document as an opaque origin, so a page opened from disk cannot reach into a frame's document ([MDN, Same-origin policy: File origins](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy#file_origins)). Served from one local server, the harness and the prototype share an origin, and the harness can dispatch events into the prototype and read its DOM.
- **Stage it.** Stage the prototype as [Serve files locally](interaction-and-verification.md#serve-files-locally) describes, with the harness at the staging root. Set the page and the frame size at the top of the harness or in the URL: `interaction-harness.html?page=a/b/index.html&width=1024&height=768`.
- **Write the checks** in the checks block at the end of the harness, or in a classic script at the staging root named in the URL with `?checks=<file>`. Each check is `check('<name>', async helpers => { … })`. It starts from a fresh load of the page and passes unless a step throws. An error the page throws during the check fails it too.
- **Dispatch events.** `click(target)` sends pointer and mouse down, moves focus as a pointer would, then sends pointer and mouse up and `click`. `press(key, target)` sends key down and key up to the target, or to the focused element. The events reach the prototype's handlers, and a click runs its activation, such as following a link. A synthetic key runs no browser default action: Enter does not activate a button and Tab does not move focus. Check a keyboard path through its handler, such as Escape closing a panel, and drive real Tab order with a browser-driving tool or by hand.
- **Let timers run.** `wait(ms)` lets the page's timers run for that long, and `until(condition, detail)` polls until a condition holds or fails after a timeout. A headless DOM dump must give the page enough time: its time budget, such as Chrome's `--virtual-time-budget`, must exceed the waits of all checks together.
- **Assert.** `assert(condition, detail)` fails the check with its detail. Read DOM state with `$`, `$$`, `visible(target)` and `style(target, property)`, focus with `focused()`, and ARIA and other attributes with `attr(target, name)`. `record(target, attribute)` collects every value an attribute takes, including a value that lasts only inside one event, which is how a check tells "opened, then closed on the same click" from "never opened". Start it before the action and read the values after it: `const states = record('#panel', 'hidden'); click('#toggle'); states.values()` lists every value of `hidden`, the current one last.
- **Navigate.** `const next = loaded(); click('a.next'); await next;` follows a link and waits for the new page. `load(path)` loads another page in the frame.
- **Read the results** from `#results` in the page or a DOM dump: one `PASS <name>` or `FAIL <name>: <detail>` line per check, then `DONE <passed>/<total>`.

Write the failing case first when you can: run a check against the version with the defect, or with the behavior removed, and confirm it fails for the right reason before it passes.

## Narrow viewports

A headless browser may keep a minimum window width; headless Chrome, for example, has kept 500 CSS pixels when asked for 320. Inspect a narrow layout in a frame of the exact width instead: set the harness's `width`, then measure inside the frame, for example that `page().document.documentElement.scrollWidth` is no larger than the frame's width.

## Long pages in slices

A full-page screenshot of a long page is too tall to read, and cropping it afterwards loses the scale. Inspect a long page in slices of one fixed frame height instead, with `templates/page-slices.html`:

1. Stage the page with `page-slices.html` at the staging root.
2. Open `page-slices.html?src=a/b/<page>&width=<w>&height=<h>&offset=0`. The frame of the given size sits in the top-left corner, scrolled to the offset, and `#results` reads `PASS scrolled 0`. Its `data-offsets` attribute lists the offsets that cover the page from top to bottom; the last slice overlaps the one before it when the height does not divide the page.
3. For each offset, screenshot the URL with a browser window of exactly `<w>` by `<h>`, and check that `#results` reads `PASS scrolled <offset>`. A `FAIL` says where the page stopped scrolling.

Inspect the slices in order, and record the frame size and the offsets in the notes.

## Name the checks

Name each check by the outcome it observes, in words a reviewer understands without reading the code: "panel closes on Escape and focus returns to its control", not "test 3". Copy each name into the verification table of the prototype notes as it appears in the results, prefixed with `Scripted:` or `Driven:`, with its result and the conditions it ran under: the browser, the frame size and the time budget.
