# Context and scope

Status: built

The plant keeper runs `sprig.py` in a terminal. It reads and writes one JSON file named by `--data`, `sprig.json` by default. Nothing else is involved: no network, no accounts, no background process.

Dates are local calendar dates, and `--today` overrides today's date for every command.
