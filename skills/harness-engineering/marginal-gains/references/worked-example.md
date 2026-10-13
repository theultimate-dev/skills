# Worked example

A sample session, the reasoning, the reply, and the ledger entry. Use it to calibrate length and specificity, not as a list of suggestions to look for. Harness details stay generic here; a real run shows settings in the syntax of the user's harness, read from its settings file.

## The session

A user and an agent spend an afternoon on a documentation site. The ledger's goals are 1. help readers find answers in the docs, 2. spend less of the user's attention supervising the agent. Its one earlier run proposed G1, which the user declined, and G2, which added a line to the project's AGENTS.md: "Run `pnpm check` before reporting a change as done." Its watchlist holds `×1 agent ran npm instead of pnpm`.

What happened:

1. The agent ran `npm test`. The user: "we use pnpm here." Later the agent ran `npm run build`, and the user corrected it again.
2. The agent wrote two changelog entries from their commit subjects, and the user rewrote both: "write it for the reader: what can they do now?" The project's AGENTS.md already says "Changelog entries are written for users, not from the commit subject", near the end of a long file.
3. The session shows the user approving the `pnpm lint` permission prompt six times.
4. Before reporting, the agent ran `pnpm check` (G2). It caught a broken link, which was fixed before the user saw it.
5. The agent read eleven files to find where the site's navigation is defined.

## The reasoning

Grading: G2's check is "the agent runs `pnpm check` before reporting". It did, and it caught a real defect. G2 held, first time; it is checked again next session.

Candidates, by root cause:

| Candidate | F | C | R | Score | Notes |
|---|---|---|---|---|---|
| The changelog rule exists and is not working | 2 | 2 | 3 | 12 | Two entries rewritten; the changelog is what readers see, the first goal |
| The package manager is not stated | 2 | 1 | 2 | 4 | Twice this session and once on the watchlist; rises to F 3 next time |
| `pnpm lint` is always approved | 2 | 1 | 2 | 4 | One-minute fix |
| No map to the navigation config | 1 | 1 | 2 | 2 | First time; goes on the watchlist |

The pnpm and lint candidates tie at 4. Both serve goal 2 and take a minute; neither is a removal. The pnpm one has the longer history, so it goes second and the lint permission third. Either one satisfies the five-minute rule. The navigation map goes on the watchlist.

The changelog rule is already written down, so rewording it more forcefully is not the fix. Moving it to where the agent reads it while writing the entry, with a contrasting example, is the lightest change that should hold. If it slips, the next step is a step in the procedure the agent follows to write release notes. Wording cannot be checked mechanically, so a check is not an option here.

Before writing G5, the agent reads `package.json`: the `lint` script is `eslint .`, which changes no files.

## The reply

**Since last time:** G2 held (pnpm check caught a broken link before review)

### G3 · Put the changelog rule where the entry gets written, with an example

5 min · serves goal 1: readers · score 2×2×3 = 12

- **Evidence:** "write it for the reader: what can they do now?", after two entries were rewritten; the rule already sits at `AGENTS.md:88`, in Conventions, the file's last section.
- **Change:** `AGENTS.md` (project, shared: every contributor's agent reads it), move the line from Conventions into Commits and changelogs, and add an example:

  ```diff
  - Changelog entries are written for users, not from the commit subject.
  + Write each changelog entry for the reader, saying what they can do now. Not "fix(nav): handle empty groups", but "Empty navigation groups no longer break the sidebar."
  ```

- **Why it ranks:** every release passes through it, each miss costs a rewrite, and the changelog is what readers see.
- **Check:** the next changelog entry needs no rewrite.

### G4 · State the package manager in the project instructions

1 min · serves goal 2: less supervision · score 2×1×2 = 4

- **Evidence:** `npm test` and `npm run build`, both corrected; on the watchlist since the last run.
- **Change:** `AGENTS.md` (project, shared), Commands:

  ```diff
  + Use pnpm for every package command, such as `pnpm test` and `pnpm build`.
  ```

- **Why it ranks:** every session that builds or tests passes through it, three times so far.
- **Check:** no npm command in the next session.

### G5 · Allow `pnpm lint` without a prompt

1 min · serves goal 2: less supervision · score 2×1×2 = 4

- **Evidence:** the `pnpm lint` prompt approved six times this session.
- **Change:** the user's permission settings for this project (project, private), an allow rule for exactly `pnpm lint`, no wildcard. The `lint` script is `eslint .`, so it changes no files.
- **Why it ranks:** six interruptions per session for a command that is always approved.
- **Check:** no lint permission prompt next session.

**Watchlist:** no map to the navigation config ×1

Which should I apply? Reply with IDs, or decline or defer by ID.

## The ledger entry

Written before the reply was sent. The user then applied G3 and G4 and deferred G5, so the run was updated to:

| ID | Suggestion | Where | Evidence | Score | Effort | Status | Check | Outcome |
|---|---|---|---|---|---|---|---|---|
| G3 | Put the changelog rule where the entry gets written, with an example | AGENTS.md, Commits and changelogs | two entries rewritten · ×1 | 2×2×3 | 5 min | applied | next entry needs no rewrite | open |
| G4 | State the package manager | AGENTS.md, Commands | npm test, npm run build corrected · ×2 | 2×1×2 | 1 min | applied | no npm command | open |
| G5 | Allow `pnpm lint` without a prompt | permission settings, project | 6 approvals · ×1 | 2×1×2 | 1 min | deferred | no lint prompt | — |

G2's row in the earlier run now reads `held` with the date, and the watchlist gains `×1 no map to the navigation config`.

## A card that fails

### Gx · Improve AGENTS.md so the agent follows conventions better

This card has no pointer, so it is generic advice. Its change names no line and no text, so the user has to do the work. It has no check, so the next run cannot grade it. And "improve" is a redesign with no first step. Each of these alone is enough to drop it.
