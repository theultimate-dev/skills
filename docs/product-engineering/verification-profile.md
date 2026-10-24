# Verification profile

Confirmed: 2026-10-24 at commit 9982dc6
Re-check when these paths change: `scripts/validate.py`, `.github/workflows/`, `evaluations/`, the installed Chrome version

Names only. A secret value never appears in this file. Mark anything not yet confirmed by a run as `unconfirmed`, and anything designed but not built as `planned`.

## Stack

- Languages and frameworks: Markdown skills in the Agent Skills format; HTML templates with inline, non-module JavaScript; a Python 3 standard-library validator.
- Package manager: none for the skills. `uv` runs `scripts/render_visuals.py` only.
- Repository host: GitHub (`git@github.com:theultimate-dev/skills.git`).

## Commands

| Purpose | Command | Covers | Typical time | Baseline on 9982dc6 |
|---|---|---|---|---|
| Install | none | | | |
| Lint, typecheck, unit tests, build | none | | | |
| Repository invariants | `python3 scripts/validate.py` | Layout, frontmatter, self-containment including the parent-path ban, marketplace, decisions index, changelogs, README skill names | 0.14 s | pass: "0 errors, 0 warnings" |
| Whitespace | `git diff --check origin/main...HEAD` | Trailing whitespace and conflict markers in the diff | under 1 s | `unconfirmed` |
| Render category visuals | `uv run scripts/render_visuals.py <category>` | Category README images; needs Chrome and network access for fonts | | `unconfirmed`, not needed unless a category README changes |
| Verify entry point | none | The validator is the only check CI runs | | |

## CI

- Workflows: `.github/workflows/validate.yml` runs `python3 scripts/validate.py` on every push and pull request. `.github/workflows/release.yml` runs on `vX.Y.Z` and `<plugin>--vX.Y.Z` tags, or by hand with a tag.
- Required checks on pull requests to `main`: `validate`. The branch rules also block deletion and non-fast-forward pushes, and require a pull request with 0 approving reviews (`gh api repos/theultimate-dev/skills/rules/branches/main`, 2026-10-24).
- Deploys or releases on push to the base branch: no. Releases run only from tags.

## Run the app

There is no app. The product is a skill that an agent follows, plus copyable HTML templates that run in a browser. "Running" it means one of two things:

| Step | Command or value |
|---|---|
| Stage files | Copy the exact file set to `<scratchpad>/<run>/a/b/`, and put the filled-in check templates at `<scratchpad>/<run>/` |
| Start | `python3 -m http.server <port> --bind 127.0.0.1`, run from `<scratchpad>/<run>/` |
| URL | `http://127.0.0.1:<port>/` |
| Readiness | The first request returns 200 |
| Stop | Kill the server process, for example `pkill -f "http.server <port>"` |
| Agent trial | A fresh-context subagent (Sonnet or Haiku) gets the candidate skill's path in the worktree, a fixture project copied to the scratchpad, and a task. Its output files are read afterwards |

## Configuration and accounts

None.

## Verification tools

| Capability | Tool | Probe | Confirmed |
|---|---|---|---|
| Read a page's DOM after its timers run | Google Chrome 155 headless: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --virtual-time-budget=<ms> --dump-dom <url>` | A page that writes `PASS timer-ran` 1.5 s after load: the dump showed it in `#results` | 2026-10-24 |
| Screenshot a URL | The same binary: `--headless --window-size=<w>,<h> --screenshot=<path> <url>` | Wrote an 800×600 PNG | 2026-10-24 |
| Narrow viewport | A same-origin `<iframe>` of the target width, read over HTTP. Headless Chrome kept a minimum window width of 500 CSS px: `--window-size=320,800` gave `innerWidth` 500 | A 320 px frame reported `innerWidth` 320 and no horizontal scroll | 2026-10-24 |
| Open from disk | Headless Chrome on a `file://` URL | A page in `views/panel/` applied a stylesheet two folders up (`PASS shared-css 7px`) | 2026-10-24 |
| Serve files locally | `python3 -m http.server` (Python 3.13.2) | Served `/a/b/index.html` to headless Chrome | 2026-10-24 |
| Run an agent with fresh context | Subagent (Agent tool), Haiku or Sonnet | Read the candidate `SKILL.md` and returned its name and line count (41) | 2026-10-24 |
| Read screenshots | The agent's image-reading file tool | | `unconfirmed` |
| Drive a real browser interactively | none in this session. Playwright for Python exists only as a dependency of `scripts/render_visuals.py` | not probed | |

Another host or machine may expose different tools. Probe before use. A tool with the same capability may replace one listed here; the report names the tool actually used.

## Environments

| Environment | URL or host | Allowed for verification |
|---|---|---|
| Local | `127.0.0.1` servers, scratchpad folders, this worktree | yes |
| Ephemeral preview | none | no |
| Staging | none | no |
| Production | GitHub releases and tags of `theultimate-dev/skills`, the published marketplace, the `main` branch | never: verification creates no tag, release, push or merge |

## Default limits

- Data the agent may reset: only scratchpad folders it created.
- Outbound side effects: none. Fixtures use only local files and reserved `example.com` URLs that no check fetches.
- Load: none.
- Every server binds to `127.0.0.1` and is stopped when the check ends.

## Harness gaps

- No interactive browser-driving tool on this host. Accepted: the work item's checks run through headless DOM dumps and screenshots by design.
- No CI job runs browser checks. Template checks rerun by hand from `evaluations/product-design/`.
