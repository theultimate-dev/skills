# Contributing

This is a curated set: the skills I use myself, kept small on purpose. Fixes are welcome. New skills get added by decision, not by pull request volume.

- Bug or unclear instruction in a skill: open an issue or a small pull request.
- New skill or category: open an issue first. Say which problem it solves and which harnesses you use. If it fits, we shape it before writing it.
- Conventions live in [AGENTS.md](AGENTS.md): format rules, naming, categories, commits, changelog.
- Before a pull request: `python3 scripts/validate.py` passes, the changed plugin's `skills/<category>/CHANGELOG.md` has an entry under `[Unreleased]` (catalog, install and tooling changes go in the root `CHANGELOG.md`), and commit messages follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) with the description in the imperative mood.
