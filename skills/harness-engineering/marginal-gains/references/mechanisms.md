# Mechanisms

Every fix lives somewhere in the harness. Choose the lightest mechanism that will hold, at the narrowest scope that covers every occurrence. Lighter mechanisms cost little and bend; heavier ones hold every time and cost more to build and to change.

## The ladder

From lightest to firmest:

| Step | Mechanism | Use when | Cost |
|---|---|---|---|
| 1 | Prompt habit: how the user asks, or a saved prompt | Only the user has the fact, and it matters at the start of one kind of task | Nothing loaded; depends on the user remembering |
| 2 | Memory entry | A fact needed in some sessions, specific to the user or a project, where the harness keeps memory | Small; recall depends on the harness |
| 3 | Instruction line | A fact or rule needed in most sessions of that scope that the agent cannot infer from the files | Loads in every session of that scope, so it must earn its place |
| 4 | Skill edit | A recurring procedure went wrong: wrong trigger, missing step, buried step | Loads only when the skill runs |
| 5 | New skill or sub-agent | A recurring procedure has no home | The most to write; the first step is usually a skeleton, or a watchlist line until it recurs |
| 6 | Control: hook, permission rule, setting | A written rule was broken anyway; a rule must never fail; an action should always or never run; a permission is always granted | Runs every time without the model's judgment; harness-specific syntax |
| 7 | Check: validator, test, lint, CI | The mistake shows in the output and can be detected mechanically | Catches it for every agent and every contributor, not only this user |

The ladder orders mechanisms by how firmly they hold. A firmer step helps only when it fits the root cause: a skill step fixes a mistake made while following that skill, not a rule unrelated to any skill. Steps 6 and 7 hold whether or not the model remembers. Prefer a check over a control when both fit: a check works in every harness and for every contributor. When the harness in use lacks a mechanism, such as hooks, take the next step it has.

## Escalate a slipped fix

A suggestion that slipped returns on a firmer step that fits the root cause: text that loads at the moment the mistake happens, such as a skill step instead of an instruction line, or a control or a check when the mistake can be blocked or detected. Skip steps that do not fit. Rewording the same rule more forcefully is not an escalation; capitals and "always" make models over-apply a rule without making them remember it. When the same root cause has slipped twice, go to a control or a check, or say that none can catch it and leave it on the watchlist.

## Remove before adding

Every instruction line loads in every session of its scope and competes for attention with every other line. A removal is a real gain, and often the cheapest one:

- A line that a check or a control now enforces can go.
- A line that restates what the repository shows, such as the language or the framework, can go.
- Two files that say the same thing keep it in one place.
- A line the user contradicted in this session gets fixed or removed, never left to contradict the next session.
- A skill whose description overlaps another's gets a sharper boundary, so the right one triggers.

When an addition and a removal tie on score, goal, and effort, propose the removal.

## Choose the scope

| Scope | Reaches | Choose when |
|---|---|---|
| User level | Every session of this user, in every project | The occurrences span projects, or the fact is about the user |
| Project, private | This user in this project | The fact is about the project but should not be shared |
| Project, shared | Every contributor's agent in this project | The fact is true for anyone working here |
| Published | Readers and clients who install or read it: a public skill, a template, documentation | The fix belongs in something the user ships to others |

Shared and published scopes reach other people, so the card says so. Their changes ship through the project's normal review and release path, not straight from the session.

## Write the change

- Read the target file first, place the change next to the related rules, and match the file's style and terms.
- One instruction per line, stated as what to do, with the reason in a clause when it is not obvious.
- Show the change as a diff or as the exact text to insert, with the file and the section.
- For controls, give the setting in the syntax of the harness the user is running, read from its settings file, and say what it allows or blocks.
- Narrow an allow rule to the exact command, after reading what that command runs. Commands that push, publish, deploy, delete outside the working tree, or spend money stay behind a prompt however often they were approved.
- Name the scope on the card: user, project private, project shared, or published.
- Keep the change small enough to read in a minute and apply in fifteen. A change that needs a design discussion is not a marginal gain; put its first step on the card.
