# The release workflow

`templates/release.yml` is a GitHub Actions workflow that turns a pushed `vX.Y.Z` tag into a GitHub Release whose notes are that version's section of `CHANGELOG.md`. It uses only `actions/checkout` and the `gh` CLI preinstalled on GitHub runners, so there is no third-party action to audit or keep updated.

`templates/release-components.yml` does the same for a repository whose components are versioned independently. It releases both root `vX.Y.Z` tags and component `name--vX.Y.Z` tags from the matching changelog. It adds a tag-parsing step, a checkout of the tag, a manual run with a `tag` input, a Latest policy, and an optional check, switched on with `ROOT_FOLLOWS_COMPONENTS`, that refuses a component tag the root release at the same commit does not list. `independent-versions.md` explains it, and `root-follows-components.md` the option. The steps below apply to both.

## What it does, in order

1. **Checks the tag shape.** `vMAJOR.MINOR.PATCH` with an optional `-prerelease` suffix. Anything else fails fast; `v1.2` or `release-1` never becomes a release.
2. **Checks out the full history.** `fetch-depth: 0`, because the next step needs `main`.
3. **Verifies the tag is on `main`.** Fetches `origin/main` explicitly (a tag-triggered checkout does not have it), resolves the tag to its commit (an annotated tag points at a tag object, not a commit), and requires `git merge-base --is-ancestor <commit> origin/main`. GitHub cannot filter tag pushes by branch, so this step is the only thing between a tag on a feature branch and a published release.
4. **Extracts the notes.** An `awk` program prints the lines between `## [X.Y.Z]` and the next `## ` heading, ignoring `## ` lines inside fenced code blocks. It matches the heading by prefix, not by regex, so the dots in the version are literal. An empty result fails the job: releasing a version with no changelog section is the mistake this workflow exists to prevent.
5. **Creates the release.** `gh release create vX.Y.Z --title vX.Y.Z --notes-file <notes> --verify-tag`, with `--prerelease` when the version contains a hyphen. If the release already exists, a re-run does nothing instead of failing.

Projects that ship files add a packaging step between 4 and 5 and pass the files to `gh release create`, uploading with `--clobber` on re-runs. The repository this skill comes from does that for per-skill archives and a `checksums.txt`.

## Installing it in a project

1. Copy `templates/release.yml` to `.github/workflows/release.yml`. Change nothing unless the default branch is not `main`; then replace `main` in the fetch and in the ancestry check.
2. Confirm the workflow token may write contents. The file declares `permissions: contents: write`, which is enough under default repository settings. If the organisation restricts `GITHUB_TOKEN` to read-only, an administrator grants write for this workflow.
3. Commit with `ci: release from tags` and a changelog entry under `Added`.
4. Cut the first release per `cutting-a-release.md`.

## Reading a failure

| Message | Cause | Fix |
|---|---|---|
| `Tag 'vX' is not vMAJOR.MINOR.PATCH` | Tag name shape | Delete the local tag and create it correctly. If it was pushed, leave it and create the right one |
| `Tag vX.Y.Z points at <sha>, which is not on main` | Tagged a branch commit, or pushed the tag before `main` | Push `main`, re-run the job. If the commit is not meant for `main`, that tag must not become a release; cut the release from `main` under the next version |
| `CHANGELOG.md has no entries under '## [X.Y.Z]'` | Changelog not released, or the heading does not match the tag (`v` prefix in the heading, wrong number) | Fix `CHANGELOG.md` on `main` and release the next patch version. Released tags are not moved |
| No run appears after a tag push | The push carried more than three tags, and GitHub created no event | Components template: `gh workflow run release.yml -f tag=TAG`. Push at most three tags at a time |
| `... does not exist at TAG. Is 'NAME' a component of this repository?` | The tag names an unknown component, or `COMPONENT_CHANGELOG` does not match the layout | Fix the path template on `main` and start the run by hand. A misnamed tag stays unreleased; tag the right component under its next version |
| `Tag '...' is neither vMAJOR.MINOR.PATCH nor NAME--vMAJOR.MINOR.PATCH` | Tag shape, components template | As for the tag shape above |
| `CHANGELOG.md section X.Y.Z does not link NAME--vX.Y.Z` | `ROOT_FOLLOWS_COMPONENTS` is on and the release commit did not release the root, or its section does not link the component with an inline link | A re-run reads the same commit and fails again. Leave the tag unreleased and release the component under its next version together with the root |
| `Resource not accessible by integration` | Token lacks `contents: write` | Repository or organisation Actions settings |
| `release not found` followed by upload errors | A re-run raced a partially created release | Re-run once more |

## Why not release-please, semantic-release, or a marketplace action

They work, and they also decide things for you: bot pull requests, notes generated from commit subjects, one more dependency with its own release cadence. This workflow keeps the human-written changelog as the source of truth and does one thing at tag time. If the project already runs one of those tools, read `bootstrapping.md` before replacing anything.
