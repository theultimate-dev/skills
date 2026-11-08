---
name: framing-prototype-ideas
description: "Frames a prototype idea before any bet exists: checks what the prototype context and code already settle, compares two or three options, recommends one with a signal for removing it after a try, and gives a verdict of shape, park or stop in a one-page dated research note. Use when the user says I have an idea, should we try X, think this through, research this before we build it, or is this worth a bet. Not for shaping the bet (shaping-prototype-bets) or choosing the technical approach to an agreed spec (brainstorming-solutions)."
license: MIT
---

# Framing prototype ideas

A prototype is a place to try ideas and keep or remove them cheaply. Framing is the step before the first try: it decides whether an idea earns a bet at all. It reads what the prototype already knows, researches what it does not, compares a few ways to deliver the value, recommends one, and says plainly whether to shape it, park it or stop. A stop costs a page; a bet that should never have been shaped costs a day and a revert. The product of this skill is one dated research note and an updated research index. It writes nothing else, and it has no gate: the verdict is advice the person can overrule.

[The prototype profile](references/prototype-profile.md) defines the context folder, its statuses and the reading order. This skill follows its "Frame an idea" row.

## Modes

| Situation | What to do |
|---|---|
| A new idea | Frame it: steps 1 to 8 |
| The context already settles it | Stop early at step 2: a short note, verdict `stop`, `park` or `shape` as the record says |
| A parked idea, asked about again | Read its note, check whether the condition it named now holds, and frame again from that evidence in a new note |
| An idea with a `shape` note and no bet | Check that the note's material assumptions still hold against the current context and code. When they do, do not frame again: hand the note to `shaping-prototype-bets`. When one changed, frame again from that evidence in a new note |

## Inputs

- The person's idea in their words. Quote it in the note, with the date.
- The prototype's context folder (`context/` by default). When none exists, offer `structuring-prototype-context` first. If the person wants to frame before that, work from the code and the docs, write nothing, and return the note as Markdown for them to place later.
- The code the idea would touch.

## Frame an idea

1. **Read in the framing order.** Open the files in the profile's "Frame an idea" row, in that order: `product/overview.md`, `product/requirements/README.md`, `decisions/README.md`, `architecture/ecosystem.md`, `notes.md`, `research/README.md`. Open a capability file, a decision or a note only when an index row points at it. Then read the code the idea would touch.
2. **Check what already settles the idea.** Look for each of these before researching anything, because a settled question needs a citation, not an investigation.

   | Found | Means |
   |---|---|
   | An accepted decision that rules the idea out | Stop early. Cite the record. Reopening it is a decision for the person, taken with `decision-records`, not a framing outcome |
   | A dropped requirement with a reason that still holds | Stop early. Cite the row and the reason. When the reason no longer holds, continue and say what changed |
   | A built requirement that already covers it | Nothing to frame. Point to the row |
   | An open risk or question the idea waits on | Verdict `park`, naming the item |
   | An earlier framing note, or the lesson of a removed bet | Read it. A `shape` note without a bet goes to shaping once its material assumptions are checked against the current context and code (see Modes); a `park` note whose condition now holds is reopened; a `stop` note stands unless there is new evidence |

   An early stop ends with a short note: Idea, the settling record in Evidence, and the Verdict. The same question will come back, and the research index is where it will be found.
3. **Pin down the problem.** State who is stuck, on what, and what it costs them today. Ask only what the code and the context cannot answer, in one message, each question with a recommended default. A solution in the person's words is a clue to the problem, not the problem.
4. **Research.** Cite paths for every claim about the code. Use primary sources (official documentation, standards, source code) for what the platform or a service can do, and record each with its URL, the date retrieved and the version. Keep apart what the code shows, what a source claims and what you infer. Research only the questions that change which option wins. When the harness has subagents, send independent questions to separate ones in fresh contexts and merge their findings yourself.
5. **Compare two or three options.** They must differ in what the person gets or how it is built, not in library brand. One may be a smaller try or no code at all. For each, write the value, an appetite estimate on the profile's scale (`½ day`, `1 day`, `2 days`; anything larger is "over 2 days", with what to cut or split), the risks that matter and what exposes them early, and the reversibility. Run the strawman check: name the situation in which each option is the best choice, and drop any option for which there is none. With one sensible option, say so and say why the others fail; never invent alternatives to fill the table.
6. **Recommend, and name the removal signal.** Recommend one option, with reasons tied to the problem, the evidence and the appetite. Name the condition under which another would win. Then write "Remove if": what the person would see, within days of trying it, that says the idea was not worth keeping. Shaping turns it into the bet's keep-or-remove signal.
7. **Give the verdict.**

   | Verdict | When | The note says |
   |---|---|---|
   | `shape` | The problem is real, one option fits two days or less, and nothing blocks it | Which option to shape, and the questions shaping still has to settle |
   | `park` | Worth doing, but something must change first | The condition that reopens it |
   | `stop` | The context or the evidence settles against it, or the cheapest option still costs more than the idea is worth | What settled it, so nobody frames it again without new evidence |

8. **Write the note and the index.** Fill [the framing note template](templates/framing-note.md) and save it as `research/YYYY-MM-DD-slug.md` with `Bet: not yet`. Rebuild `research/README.md` from the notes' header lines with [the folder index template](templates/folder-index.md), one row per note with its date, title, verdict and bet; the index is derived, never hand-edited. Report as Hand back says. Another bet may be open: research notes, `notes.md` rows and derived indexes may change at any time, so the note and the index are written either way, while the files an open bet's Context pack and Architecture › Relies on name stay untouched. Open questions and risks the work surfaced go in the note; offer to add them to `notes.md`, and add them only when the person agrees.

## Example

Quill is a single-user web app that tracks daily writing streaks. The person says: "Quill should nudge me at 8pm if I haven't written." Framing reads `context/` and finds decision 0003, which keeps Quill free of accounts and servers beyond the web app, and `STK-04` (email reminders), dropped on 2026-10-02 because the reminder arrived after the day's writing window. It does not stop there: the dropped row's reason concerns timing, and the idea is an in-browser nudge. The note then records the problem (the streak breaks on days the person forgets, `src/streaks/rollover.ts`), the browser's notification support from the platform documentation (URL, retrieved date, version), and three options: an in-page banner when the app is open (½ day, easy to revert), a notification raised by the open page at 8pm (½ day, easy: needs a permission prompt, and fires only while a Quill tab is open, because the platform documentation does not establish a scheduled delivery that survives a closed page without a server), and a calendar file export (½ day, easy, reliable at 8pm but outside the app). It recommends the open-page notification, states in the Evidence and the Verdict that evenings with no tab open get no nudge, gives "Remove if: I dismiss the nudge on most evenings for a week, or most missed evenings pass with no tab open to show it", and ends with verdict `shape`, leaving the delivery limit for shaping to confirm.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| Framing an idea the decisions or dropped requirements already answer | Check them first and cite the record |
| A problem that is the solution reworded: "add reminders" | Who is stuck, on what, with what cost today |
| Options that differ only by library | Vary what the person gets or how it is built |
| An appetite estimate that fits only if nothing goes wrong | Estimate with the rabbit holes in; "over 2 days" is an honest answer |
| A recommendation by taste: "cleaner", "more modern" | Tie each reason to the problem, the evidence or the appetite |
| Sources without dates, or code claims without paths | Record URL, retrieval date, version; cite paths |
| "Remove if" as a feeling: "it doesn't seem useful" | A sign the person can observe within days |
| Verdict `shape` for an idea with an unanswered blocking question | `park`, naming the question |

## Hand back

Report the verdict in one sentence, the recommended option, the removal signal, the note's path and the research index update, and the next step by verdict:

- `shape`: `shaping-prototype-bets`, with the note's path. Offer to start it; the person decides.
- `park`: the condition that reopens the idea, and where it is recorded.
- `stop`: the reason, and that the note stays as evidence.

Commit nothing unless the person asks; context commits are the person's call, kept separate from code commits as the profile describes. Without file access, return the note as Markdown and say that no file was written.

## When a sibling skill is missing

Name the missing skill in one line and carry on with what is small.

- `structuring-prototype-context` missing, or no context folder: frame from the code and the docs that exist, return the note as Markdown, and say that the research index was not updated.
- `shaping-prototype-bets` missing: the `shape` verdict and the note stand; say that shaping needs the skill and nothing else is written.
- `decision-records` missing: when the idea would reopen an accepted decision, name the record and leave the reopening to the person.

## References

| Read | When |
|---|---|
| [the prototype profile](references/prototype-profile.md) | The context folder, statuses, reading order, house rules |
| [the framing note template](templates/framing-note.md) | Writing the note |
| [the folder index template](templates/folder-index.md) | Rebuilding `research/README.md` |
