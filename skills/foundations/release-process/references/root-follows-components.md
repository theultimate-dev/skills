# Root follows components

An option of independent versions (`independent-versions.md`). Every component release is also a root release, so the root release, the one GitHub marks Latest and `releases/latest` opens, always names the newest component versions and links to their releases.

## When it fits

In a catalog repository the root rarely changes: a component added, renamed or removed. The components change weekly. Without this option the root is released only for its own changes, and Latest shows an old version that says nothing about the current components.

It fits:
- Claude Code and Copilot CLI plugin marketplaces: `.claude-plugin/marketplace.json` with a `metadata.version` and a `version` per plugin.
- Skill catalogs shipped as plugins.
- Any catalog-with-components repository whose root release is the entry point visitors land on.

It does not fit a monorepo whose root release has no audience of its own, or whose root is a product with its own release rhythm. There, tying the two adds noise. It is an option, not a default: suggest it when the repository has a marketplace manifest and marks its root releases Latest, and let the user decide.

## The rule

- Every component release is also a root release, in the same release commit.
- One root release per release commit, however many components it releases.
- A root release without component releases stays possible.
- Component pre-releases (a hyphen in the version) are exempt. A root release for every beta would put pre-release notes on Latest.

## The bump

The root bump is the highest one its changes call for, with patch as the minimum. A component release calls for a patch, whatever its own bump: a breaking change inside a component does not break the catalog, and the component's version already says so. The root's own unreleased entries that call for a minor or major bump raise it, and they ship in the same release, because the root tag covers all of `main` at that commit.

## The entry

The root section lists the components under `### Changed`, written in the release commit, since the lines only exist once the component versions are chosen:

```markdown
## [2.4.1] - 2026-10-02

### Changed

- Components released with this version:
  - `api` [1.3.0](https://github.com/OWNER/REPO/releases/tag/api--v1.3.0): list endpoints accept a `since` filter.
  - `web` [0.9.1](https://github.com/OWNER/REPO/releases/tag/web--v0.9.1): the settings page saves on slow connections.
```

- One nested line per component: the name in backticks, the new version linked to the component's release page, one line for users on what the release gives them. The full notes stay in the component's own release.
- A marketplace may say `Plugins released with this version:`. Pick one wording and keep it.
- Use inline links. The notes extraction stops at link-reference lines such as `[1.3.0]: https://…`, so a reference-style link never reaches the release notes, and the workflow check cannot see it.

## Catch-up

A component release that went out without a root release, because the option was off or the release was cut by hand, is listed under the root's `[Unreleased]`, in the same `Components released with this version:` form, and ships with the next root release. Components whose first release shipped with the root's first release are exempt, because that root release introduced them.

## Tag order

Push `main`, then the component tags, then the root tag, by name and at most three per push. The root notes then never link to a component release that does not exist yet. Three components and the root take two pushes:

```bash
git push origin main
git push origin api--v1.3.0 web--v0.9.1 cli--v0.4.0
git push origin v2.4.1
```

## Declare it

Add one line to the "Release" section of `AGENTS.md`, for example: "Every component release is also a root release, in the same release commit; the root section lists the components released under Changed." Without that line, the next agent follows the plain independent-versions mode.

## The workflow check

In `templates/release-components.yml`, set `ROOT_FOLLOWS_COMPONENTS: "true"`. For a component tag that is not a pre-release, the step "Check the root release lists the component":
1. reads the root version at the tag from the newest `## [X.Y.Z]` heading of `ROOT_CHANGELOG`;
2. extracts that section;
3. refuses the tag unless the section links, outside fenced code, `…/releases/tag/<name>--vX.Y.Z`.

A component tag cut without a root release in the same commit fails, because the newest root section at that commit is an older one that cannot link the new tag. A repository whose root version lives in a manifest can read it there instead, as the comment in the step shows for `metadata.version` in `.claude-plugin/marketplace.json`.

## A local check

The workflow check is the hard gate, but it runs only at tag time. A project with its own validator adds two rules, so a missing line shows up before anyone tags:
- Every component release dated after `SINCE` is linked from the root changelog.
- Every such link names a release the component's changelog has.

`SINCE` defaults to the root's first release, which exempts the components' first releases. A project that adopts the option later sets it to the adoption date, so its history needs no backfill. Releases dated on `SINCE` itself are exempt. A standard-library sketch to adapt:

````python
import re
from pathlib import Path

ROOT = Path("CHANGELOG.md")
COMPONENT = "packages/{component}/CHANGELOG.md"  # the path template from AGENTS.md
COMPONENTS = ["api", "web"]                      # or discover them from the layout
SINCE = None                                     # "YYYY-MM-DD" when adopted later; None means the root's first release

HEADING = re.compile(r"^## \[(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)\] - (\d{4}-\d{2}-\d{2})")
LINK = re.compile(r"\]\([^)\s]*/releases/tag/([a-z0-9]+(?:-[a-z0-9]+)*)--v(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)\)")


def lines(path):
    """Yield (number, line) outside fenced code blocks."""
    fenced = False
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if line.strip().startswith(("```", "~~~")):
            fenced = not fenced
        elif not fenced:
            yield number, line


def releases(path):
    """Map each released version of a changelog to its date."""
    return {m[1]: m[2] for _, line in lines(path) if (m := HEADING.match(line))}


def check():
    errors, linked = [], set()
    released = {c: releases(Path(COMPONENT.format(component=c))) for c in COMPONENTS}
    for number, line in lines(ROOT):
        for component, version in LINK.findall(line):
            if version not in released.get(component, {}):
                errors.append(f"{ROOT}:{number}: links {component}--v{version}, which is not released")
            linked.add((component, version))
    since = SINCE or min(releases(ROOT).values(), default=None)
    for component, versions in released.items():
        for version, date in versions.items():
            if since and date > since and "-" not in version and (component, version) not in linked:
                errors.append(f"{ROOT}: does not link the {component} {version} release of {date}")
    return errors
````

## For marketplaces

- A plugin updates when its own `version` changes. `metadata.version` does not trigger updates, so a root patch release costs users nothing; its value is the visible release and a meaningful `#vX.Y.Z` pin.
- A root tag pin pins the whole catalog at that commit, including other plugins' unreleased work that was merged before it. Users who want one plugin as released pin its `<name>--vX.Y.Z` tag instead.
- Until the first root release is published, no release is marked Latest, and GitHub shows the one with the newest tag date, often a plugin. The first root release takes the link back.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `… does not link NAME--vX.Y.Z` in the workflow | The component was released without a root release in the same commit | The check reads the changelog at the tag, so a re-run fails again. Leave the tag unreleased and release the component under its next version, with a root release in the same commit |
| The root notes link to a release page that 404s | The root tag was pushed before the component tags, or a component run did not start | Push the component tags; start a missing run with `gh workflow run release.yml -f tag=TAG` |
| The local check reports an unlinked release | A release was cut by hand, or before the option was declared | List it under the root's `[Unreleased]`, or move `SINCE` to the adoption date |
| The check refuses a tag whose line is in the root section | The line uses a reference-style link | As for the refusal above, and write the line with an inline link next time; released sections stay as they are |
| Latest names a component | No root release has been published yet | Publish the root release |
