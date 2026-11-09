# Watering (WAT)

Recording waterings and working out which plants are due.

| ID | Requirement | Status | Notes |
|---|---|---|---|
| WAT-01 | `water NAME` records today as the last watering | built | |
| WAT-02 | `due` lists every plant whose next watering date is today or earlier | built | |
| WAT-03 | The next watering date is the last watering plus the interval | built | |
| WAT-04 | `water` on an unknown plant exits with status 3 | built | |
| WAT-05 | Sprig emails a reminder when a plant is due | dropped | 2026-10-20, bet 02 removed: a reminder needs a mail server and an account, which decision 0003 rules out |
