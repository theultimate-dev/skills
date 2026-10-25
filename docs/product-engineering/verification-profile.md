# Verification profile

Confirmed: 2026-10-24 at commit f401cae
Re-check when these paths change: `scripts/validate.py`, `.github/workflows/`, `evaluations/`, the installed Chrome version

Names only. A secret value never appears in this file. Mark anything not yet confirmed by a run as `unconfirmed`, and anything designed but not built as `planned`.

## Stack

- Languages and frameworks: Markdown skills in the Agent Skills format; HTML templates with inline, non-module JavaScript; a Python 3 standard-library validator.
- Package manager: none for the skills. `uv` runs `scripts/render_visuals.py` only.
- Repository host: GitHub (`git@github.com:theultimate-dev/skills.git`).

## Commands

| Purpose | Command | Covers | Typical time | Baseline on f401cae |
|---|---|---|---|---|
| Install | none | | | |
| Lint, typecheck, unit tests, build | none | | | |
| Repository invariants | `python3 scripts/validate.py` | Layout, frontmatter, self-containment including the parent-path ban, marketplace, decisions index, changelogs, README skill names | 0.11 s | pass: "0 errors, 0 warnings" |
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
| Agent trial | A fresh-context subagent (Opus, Sonnet or Haiku, chosen by the task) gets only `<scratchpad>/<run>/`: the candidate skill staged there with `git archive <sha> <skill dir>`, outside any checkout; a fixture copied to `project/`; and a task that allows only absolute paths under `<run>`. Its output files are read afterwards, and its transcript is scanned (see "Verification tools") |

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
| Run an agent with fresh context | Subagent (Agent tool), Opus, Sonnet or Haiku | Read the candidate `SKILL.md` and returned its name and line count (41) | 2026-10-24 |
| Scan a subagent's tool calls | `python3 -I evaluations/product-design/scan_transcript.py <transcript> <run>`, where the transcript is the subagent's `agent-<id>.jsonl` in the session's `subagents/` folder | A synthetic transcript with a `Read` of the main checkout's `AGENTS.md`, a relative-path `Bash` call, a `Skill` call, a `cd` to `<run>/../..` and a Python heredoc that opens an outside file printed five lines and exited 1. One confined to the run folder, with a `cd` into `<run>/project` and a `cat` heredoc that writes `/etc` as text, printed `CLEAN`. A third, with `cat > /tmp/x; python3 - <<'E'` opening `/etc/hosts` and `cat <<'EOF' > /tmp/y`, printed all three paths and exited 1. `wc -l </etc/hosts` printed its path, and a Python heredoc that writes `</div></fieldset>` markup printed `CLEAN`. Each of these was flagged: a `Read` of `<run>/skill/../../…/AGENTS.md`, the same climb in an absolute and in a relative `cat`, `$HOME`, `${HOME}` and `~` paths, a later `cd ..`, a `cat` heredoc piped into `python3 -` or read inside `$( )`, climbs from `$PWD/..` and `$(pwd)/..`, a later bare `cd`, `cd -`, `cd -P /etc`, `cd $d`, a `cd` to a backtick or to `$(dirname "$PWD")`, `pushd "$HOME"`, `popd`, `$OLDPWD`, `${PWD%/*/*}`, `${PWD/run/}`, `${PWD%run}`, `${PWD%"${PWD##*/}"}`, `dirname` in a Python one-liner, `cd '../..'`, `cd '-'`, `pushd '../..'`, `find / -name SKILL.md`, `ls /`, `cat //etc/hosts`, and calls to a connector or any tool outside the file and shell tools. A `cat ../skill/SKILL.md` run from `<run>/project`, a later `cd project`, `cd 'project'` or `pushd project`, `$PWD/project/README.md`, `${f%.md}`, `sed 's/ (x)//g'`, `http://` in a `grep` pattern, and a `cat` heredoc that writes a Markdown link to `../skill/`, `b / 2`, or `cd -` and `$OLDPWD` as text, printed `CLEAN` | 2026-10-25 |
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
- A subagent's shell starts in the main checkout, and the host loads the installed product-design plugin at its released text. Accepted: trials stage the candidate outside any checkout and void any run whose transcript reaches outside it. A subagent still receives the session's project instructions, which hold none of the skill text under test.
