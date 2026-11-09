Started: 2026-11-04 09:00 · Finished: 2026-11-04 15:30 · Base: @@BASE@@ · Head: @@HEAD@@ · Branch: @@BRANCH@@
Approved 2026-11-03 at @@PIN@@: @@AUTONOMY@@
Working time used: 5h 40m, waits excluded, as of 2026-11-04 15:30
Code commits, oldest first:
@@A@@ feat: snooze a plant while away
context: @@M@@ docs(context): log progress on bet 04
@@B@@ feat: limit a snooze to 14 days
Review: independent in a fresh context, 1 round

| Check | Result | Evidence |
|---|---|---|
| C1 (WAT-07) | pass | observed: `python3 -m unittest test_snooze.SnoozeTest.test_snooze_hides_until_the_last_day`, ran 1, OK, at @@HEADS@@ |
| C2 (WAT-08) | pass | observed: run printed `snooze: days must be between 1 and 14`, exit status 2, at @@HEADS@@ |
| C3 (WAT-02) | pass | observed: `python3 -m unittest test_snooze.SnoozeTest.test_water_clears_the_snooze`, ran 1, OK, at @@HEADS@@ |
| ~ C4 (WAT-09) | cut | out of appetite: the `snoozed until` text in `list` was cut first; WAT-09 has no other check |
| C5 (WAT-07) | person's eye | listed in the Try it block |

Findings: no findings. Checked: the diff from the base, each check above
Cuts: ~ C4 (WAT-09), the `snoozed until` text in `list`, cut to stay inside the appetite
Decisions taken: none

### Try it: bet 04, snooze a plant while away

Built at commit `@@HEAD@@` on branch `@@BRANCH@@`, 2026-11-04. Appetite 1 day in total, 5h 40m so far.

#### Before you start

- none

#### Start the build

1. `python3 sprig.py add fern --every 7`
2. `python3 sprig.py snooze fern --days 3`
3. Nothing to stop; each command exits.

#### What to look at

**C5 (WAT-07): The snooze reads as one obvious step before a trip**

- Do: snooze a plant before your next trip.
- Look for: one command, and a due list that stays quiet.
- Good looks like: you did not need the help text.
- Not right: you had to look up the option name.

#### Already proven

- C1 (WAT-07): test, ran and passed.
- C2 (WAT-08): run and observe, status 2 and the message seen.
- C3 (WAT-02): test, ran and passed.

#### Cut or not proven

- C4 (WAT-09): cut, out of appetite.

#### Keep or remove

- Signal: after the next trip the plant keeper snoozed the plants they meant to, and the due list stayed quiet until they were home.
- If removed: the code commits are reverted, WAT-07, WAT-08 and WAT-09 are recorded as dropped, the planned snooze window concept is deleted, and WAT-02 stays as it was.

When you have decided, say keep or remove, with your reason in your own words. `closing-prototype-bets` records it.
