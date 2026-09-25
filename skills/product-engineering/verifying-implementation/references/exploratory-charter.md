# Exploratory charter

The contract checks what was agreed. The exploratory pass looks for what nobody wrote down. It is timeboxed and aimed at the surfaces this slice touches.

## Contents

- Run the pass
- Web UI
- API
- CLI
- Background job
- Data and migrations
- Record the notes

## Run the pass

1. Set the timebox before starting: about 10 minutes for a small change, 20 to 30 for a feature slice. Stop when it runs out.
2. Pick the surfaces the diff touches. Skip the sections below that do not apply.
3. Within each surface, start with the items closest to the changed code, then widen.
4. Use the same tools, accounts and environment as the contract. The allowed environments and destructive limits still apply.
5. Classify each finding:
   - Inside the slice's scope: a `fail` on the criterion it breaks, or on the nearest one, with a repro.
   - Outside scope and present on the base: a follow-up in the report. Do not fix it here.
   - A question the spec does not answer: an open question in the report, never an assumed answer.

## Web UI

**States**
- Empty: no records at all; the empty state explains what to do next.
- Loading: slow the network; a loading indicator appears and the layout does not jump.
- Error: make the request fail; an error message appears, the user's input survives, and a retry works.
- Long and unusual content: a 300-character title, emoji, non-Latin script, text without spaces.
- Many records: pagination or scrolling past the first page.

**Input**
- A required field left empty, and one holding only spaces.
- The maximum length, and one character more.
- Markup and script text such as `<b>x</b>` or `<script>`: shown as plain text, never executed.
- A double click on submit: exactly one record results.
- Pasted text with leading and trailing whitespace.

**Access**
- A second user cannot see or change the first user's records, through lists or through a direct URL.
- Signed out: protected pages redirect to sign-in, and return to the page afterwards when the app supports it.

**Navigation**
- Refresh in the middle of a flow.
- Back and forward after submitting: no duplicate submission, no stale screen presented as current.
- A deep link opened in a new tab.
- Two tabs editing the same record.

**Layout and input modes**
- About 375 px wide: no horizontal scroll, every control reachable, no clipped text.
- About 1280 px wide.
- Keyboard only: visible focus in a sensible order, Enter and Space activate, Escape closes dialogs and returns focus.

**Signals**
- No new console errors or warnings.
- No unexpected 4xx or 5xx responses, and no failed requests.

## API

- No credentials, invalid credentials, expired credentials: 401.
- Another user's resource: 403 or 404, with no content leaked in the body or headers.
- Invalid input: 400 or 422, with a field-level message in the project's error format.
- Wrong method or content type.
- A repeated request, where retries are expected: no duplicate effect.
- Pagination limits: zero, the maximum, beyond the maximum, a cursor past the end.
- Unknown fields in the payload: ignored or rejected, as the project does elsewhere.
- A large payload.
- No stack traces, SQL or internal paths in any error response.

## CLI

- No arguments, and `--help`: usage on stdout, exit 0 for help.
- An unknown flag, or a missing required argument: a message on stderr and a nonzero exit code.
- A missing file, an unreadable file, an empty file, a very large file.
- A path with spaces.
- Output piped to another program: no color codes or progress bars in the data.
- Interrupted with Ctrl-C: no partial output file left looking complete.
- Run twice: the second run behaves as documented, whether that is idempotent, refusing, or overwriting.

## Background job

- Triggered once, the job runs once and its effect is visible in the store or the log.
- Triggered twice for the same input: no duplicate effect.
- A dependency fails: the job retries with backoff, then lands in the failure path the project uses, and the failure is visible.
- A malformed message: handled without blocking the queue.
- Scheduled jobs: the time zone and the boundary (midnight, month end) behave as specified.
- The app restarts while a job runs: the job is resumed or retried, not lost.

## Data and migrations

- Migrate a database holding realistic existing rows, seeded at the base SHA as the procedure's migration row does, not only an empty one.
- Records created before the change still display and still work.
- Rollback, when the project supports it, leaves data intact.
- The previous release's code, if still deployed during rollout, can read what the new code writes.

## Record the notes

One line per probe, in the report's exploratory notes: what was tried, then what was observed.

- Empty title, submit: "Title is required" next to the field; no request sent.
- 375 px wide: the task list fits; the "Add" button stays visible.

Close with what the timebox covered and what it left out, so a reader knows where nobody has looked.
