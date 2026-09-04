# Cutting a release

Every step is a shell command or a file edit. Show the plan to the user before the first command that changes anything, and stop for explicit confirmation before creating the tag and again before pushing it.

## 1. Preflight

```bash
git switch main
git status --porcelain              # must print nothing
git fetch origin --tags
git status -sb | head -1            # "## main...origin/main" with no ahead or behind
git describe --tags --abbrev=0      # the previous tag, if any
```

Then check three more things: CI is green on the head commit (`gh run list --branch main --limit 1`, or the Actions page); `## [Unreleased]` in `CHANGELOG.md` has at least one entry; the version you intend has no tag yet (`git tag -l vX.Y.Z` and `git ls-remote --tags origin vX.Y.Z` both print nothing).

If anything fails here, fix it first. Do not release from a branch, from a dirty tree, or over a red build.

## 2. Choose the version

List the commits since the previous tag and scan the types:

```bash
git log "$(git describe --tags --abbrev=0)..HEAD" --pretty='%s' 
git log "$(git describe --tags --abbrev=0)..HEAD" --pretty='%b' | grep -n 'BREAKING CHANGE' || true
```

- Any `!` after the type or any `BREAKING CHANGE:` footer: major.
- Otherwise any `feat`: minor.
- Otherwise: patch.
- Before `1.0.0`, SemVer permits breaking changes in a minor bump. Apply that only if the project says so; otherwise use the rule above.

Cross-check with the `[Unreleased]` entries: `Removed` or a breaking `Changed` should mean major; only `Fixed` should mean patch. If the commits and the changelog disagree, an entry is probably missing. Fix that before releasing.

Propose the version to the user with the reason in one line.

## 3. Release the changelog

Edit `CHANGELOG.md`:

1. Insert a new `## [Unreleased]` heading above the current one, followed by a blank line.
2. Rename the old `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, today's date in ISO form.
3. Update the link references at the bottom:
   - `[Unreleased]: https://github.com/OWNER/REPO/compare/vX.Y.Z...HEAD`
   - a new line `[X.Y.Z]: https://github.com/OWNER/REPO/compare/vPREV...vX.Y.Z`. For the first release there is no previous tag; use `https://github.com/OWNER/REPO/releases/tag/vX.Y.Z`.

Read the released section once as a stranger. It becomes the GitHub Release notes verbatim.

## 4. Bump version files

Set every declared version file to `X.Y.Z`. The list lives in the project's `AGENTS.md` or `CONTRIBUTING.md`; typical entries are `package.json` and its lockfile (`npm version --no-git-tag-version X.Y.Z` does both), `pyproject.toml`, `Cargo.toml`, a plugin or marketplace manifest, `version.txt`. If the project declares no list, ask the user which files carry the version and suggest writing the list into `AGENTS.md` so the next release does not have to ask.

## 5. Commit and tag

```bash
git add CHANGELOG.md            # plus every version file you changed
git commit -m "chore(release): vX.Y.Z"
git tag -a vX.Y.Z -m "vX.Y.Z"
git show --stat HEAD            # exactly the changelog and the version files
git log --oneline -1 vX.Y.Z     # the tag points at the release commit
```

Stop here. Show the user the commit and the tag and ask for confirmation to push.

## 6. Push, then watch

```bash
git push origin main
git push origin vX.Y.Z
gh run watch                    # or open the Actions page; the Release workflow runs on the tag
gh release view vX.Y.Z          # notes match the changelog section; assets present if the project builds any
```

Push `main` before the tag. The workflow checks that the tagged commit is on `main`; if the tag arrives first, that check fails, and you re-run the job after `main` lands. Report the release URL to the user.

## Rollback

- **Before pushing:** `git tag -d vX.Y.Z`, then `git reset --soft HEAD~1` to undo the release commit. Fix, redo.
- **Tag pushed, release wrong:** do not delete or move the tag. Mark the version `[YANKED]` in the changelog with a one-line reason, fix the problem, release `X.Y.Z+1`. Mark the bad GitHub Release as a pre-release or say "yanked" in its title so nobody picks it as latest.
- **Workflow failed:** read the job log. The usual causes are the tag not being on `main`, no matching `## [X.Y.Z]` section, or a token without `contents: write`. Fix the cause and re-run the job from the Actions page on the same tag; creating the release is idempotent.
