# AGENTS.md

Evaluation fixture for the `product-engineering` skills: a standard-library Python record service with a browser page. It is deliberately incomplete and is not production software. Identity is simulated: the `X-Principal` request header names the acting principal.

## Commands

- Tests: `python3 -m unittest discover -p 'test_*.py' -v`
- Start: `python3 app.py --port <free-port> --data <temporary-data-file>`, then open the loopback URL it prints. The data file is created with one record owned by `alice` when it does not exist.

## Conventions

- Timestamps are timezone-aware UTC values from `datetime.now(timezone.utc)`, serialized with `isoformat()`. Never call `datetime.utcnow()`: it returns a naive datetime and is deprecated since Python 3.12.
