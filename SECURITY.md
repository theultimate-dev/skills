# Security

Skills in this repository are Markdown instructions. Installing one copies text into your agent's skills directory; nothing runs at install time. Your agent then follows the skill with your permissions, so read a skill before you install it, the same way you would read a script before piping it to a shell.

For reproducibility, install from a plugin's own release tag (`<category>--vX.Y.Z`) rather than `main`, and compare downloaded archives against the `checksums.txt` attached to that GitHub Release. A marketplace tag (`vX.Y.Z`) pins the whole catalog at one commit, which can include plugin changes not yet released; marketplace releases carry notes only.

## Reporting

Use GitHub's private vulnerability reporting on this repository for anything that could put users at risk, including a skill that behaves in a way its description does not announce. I answer within a few days. Please do not open a public issue for it.
