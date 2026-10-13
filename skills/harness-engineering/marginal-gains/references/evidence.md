# Evidence

A suggestion is only as good as the moment in the session it points to. Read the session as a log of friction and wins, not as a story, and collect pointers before forming any opinion about the harness.

## Signals

| Signal | What it looks like | Usual root cause | Where the fix usually lives |
|---|---|---|---|
| Correction | "No, use X"; "that's not what I asked"; the user rewrites the agent's output | A fact or a default the agent lacked | Instruction line; prompt habit |
| Restated instruction | The user says something an instruction file already says, or says the same thing twice | A rule that is not working: buried, vague, contradicted, or in a file too long to hold attention | Move the rule to where it is read at the right moment, or add an example; a firmer mechanism once a fix to it has slipped |
| Denied or interrupted call | The user rejects a tool call or stops a run | The agent acting outside the scope the user expects | Instruction line on scope; permission rule |
| Approved every time | The session shows the same permission prompt approved again and again, or the user says so. When the harness does not show the agent which calls needed approval, do not infer approvals from repeated calls | A missing allow rule | Permission rule, narrowed to the exact command |
| Failure and retry | A command fails, then succeeds after a change; a check fails on its first run | A missing environment fact, a wrong command, a convention the agent did not know | Instruction line with the right command; a clearer check message |
| Answerable question | The agent asks what the repository or harness files already answer | The answer is hard to find, or exists only in the user's head | A pointer in the instruction file to where it lives; the fact itself if it lives nowhere |
| Rediscovery | Many reads to find a convention; the same exploration a past session did (the watchlist shows it) | No map for this part of the work | One pointer line; a memory entry; a reference in a skill |
| Skill miss | The fitting skill was not used, the wrong one triggered, or a step was skipped | A description too vague or too broad; an unclear or buried step | Skill description or body |
| Manual step | The user pastes output, runs a command, or copies a file for the agent | Missing tool access or permission | Permission rule; tool configuration; a small script |
| Loop | The agent retries an approach that keeps failing | No stop rule, or a diagnostic that says too little | Instruction line on when to stop and ask; a check that reports the cause |
| Win | A prompt that worked first time, a review that caught a real bug, a shortcut that saved minutes | A good move that happened by luck | Write it down: a skill step, a saved prompt, an instruction line |

Corrections and restated instructions are the strongest signals: the user paid for them with attention, and they recur until something changes. Wins are the most often missed: a run that only looks for friction never turns good luck into routine.

## Pointers

A pointer lets the user find the moment in seconds. Keep it short and specific:

- A turn: `"the changelog entry is for users, not the commit subject"`
- A tool call: `git push origin main, denied`
- A file: `AGENTS.md:41`, `skills/x/SKILL.md:12-18`
- A commit: `4e9ffdd`
- A count the session shows: `approved "npm run lint" 6 times`

Quote a phrase, not a paragraph. Paraphrase when the words carry anything sensitive.

## What is not evidence

- Task content that will not recur: a one-off migration, a typo in the user's prompt.
- A single cheap slip with no pattern behind it. At most it goes on the watchlist, where a second occurrence makes it a candidate.
- Provider outages, rate limits, and model behavior no harness change can reach. Record one only when a harness change works around it.
- Product decisions: what to build belongs to the product, not to the harness.
- Advice from general best practice with no moment in this session behind it.

## Partial evidence

Long sessions get compacted. When earlier turns survive only as a summary, use it, add what the session changed on disk (commits, diffs, written files), and say in the reply that the evidence is partial. A restated instruction is easy to lose in a summary, so look for the same rule appearing both in a harness file and in the user's words.
