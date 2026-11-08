<!-- The block the person reads before Gate 2. Fill every bracket, delete the lines that do not apply, and delete this comment. Write it at the end state as the last block of the bet's Build log (a `###` heading inside `## Build log`), so it survives the working folder, and point the person to it in the report. Plain steps, no jargon from the build. -->

### Try it: bet [NN], [the outcome, in a few words]

Built at commit `[head SHA]` on branch `[branch]`, [date]. Appetite [½ day | 1 day | 2 days] in total, [time used] so far. [After a repair: Repaired at this commit on [date]: the person's request in one line. Replace the earlier block, which described an older head.]

#### Before you start

- [What must exist: a running service, seed data, a configuration value by name, a browser. `none` when nothing]
- [Which commit to have checked out, and whether the working tree is clean]

#### Start the build

1. [Command, from which folder]
2. [Address or window to open, and the signal that it is ready]
3. [How to stop it]

#### What to look at

<!-- One step per check marked person's eye, in the bet's order. Say what to do, what to look for, and what good looks like in the person's terms. -->

**[C3 ([ABC-01])]: [the check as the bet states it]**


- Do: [the steps, with concrete values]
- Look for: [what the person should see, feel or find]
- Good looks like: [the result that matches the bet's intent]
- Not right: [what would make this check fail in your eyes]

#### Already proven

<!-- So the person does not repeat it. One line per check that passed, with how. -->

- [C1 ([ABC-01])]: [method], [one line of observed evidence]

#### Cut or not proven

<!-- Checks that were cut under the appetite, blocked, or only inferred; each with the reason. `none` when there are none. -->

- [C2 ([ABC-01])]: [cut | blocked | inferred], [reason]

#### Keep or remove

- Signal: [the bet's Keep or remove signal, copied]
- If removed: [what removing leaves behind, copied from the bet]

When you have decided, say keep or remove, with your reason in your own words. `closing-prototype-bets` records it.
