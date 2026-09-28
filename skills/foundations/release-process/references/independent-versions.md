# Independent versions

Some repositories hold several things that users install or depend on separately: packages in a monorepo, plugins in a marketplace, services with their own clients. If they change at different speeds, one repository version bumps every component whenever any of them changes, and one changelog mixes notes for different audiences. Independent versions give each component its own SemVer version, changelog, tags, and GitHub Release.

## When to use it

Use it when users install, pin, or depend on components one by one, and a release of one component is noise to users of another. Stay with one version (the rest of this skill) when the repository ships as one thing, or its components always change together.

If the repository already runs changesets or release-please in manifest mode, keep that tool (see `bootstrapping.md`). This mode is the hand-written equivalent.

## Layout and tags

| Stream | Changelog | Tag | GitHub Release |
|---|---|---|---|
| A component | `CHANGELOG.md` in the component's directory | `api--v1.2.0` | `api v1.2.0`, with the component's files |
| The repository itself (optional) | `CHANGELOG.md` at the root | `v2.1.0` | `v2.1.0`, marked Latest |

- The component name is kebab-case and matches the name users know: the package name, the plugin name.
- `--v` separates name and version. Kebab-case names never contain `--`, so `api-gateway--v1.2.0` parses one way only. It is also the tag form Claude Code uses for plugin releases and plugin dependency ranges.
- Keep `@` and `/` out of tags. Some installers split a ref at `@`, and `/` makes refs ambiguous in URL paths.
- The root changelog, when there is one, logs what belongs to no single component: the catalog (components added, renamed, removed), install instructions, shared tooling. A repository without that audience can skip it and publish component tags only.

## Declare it in AGENTS.md

Nobody should have to guess. Under a "Release" heading in `AGENTS.md` or `CONTRIBUTING.md`, write down:
- the components, and the changelog path as a template such as `packages/{component}/CHANGELOG.md`;
- the version files of each component, for example `packages/api/package.json` or that component's entry in a plugin manifest, and those of the root;
- the two tag forms.

## Logging a change

- A change inside a component gets an entry in that component's `[Unreleased]`.
- A change to the catalog or to shared tooling gets an entry in the root changelog.
- A change that spans several components gets an entry in each, written for each component's users.

Link references use the component's own tags. Before the component's first release, `[Unreleased]` points at the commits under its path, `https://github.com/OWNER/REPO/commits/main/packages/api`. After releases:

```markdown
[Unreleased]: https://github.com/OWNER/REPO/compare/api--v1.2.0...HEAD
[1.2.0]: https://github.com/OWNER/REPO/compare/api--v1.1.0...api--v1.2.0
[1.1.0]: https://github.com/OWNER/REPO/releases/tag/api--v1.1.0
```

## Cutting a component release

Follow `cutting-a-release.md`. These steps differ:

1. **Preflight.** The component's `[Unreleased]` has entries, and its new tag exists neither locally nor on the remote.
2. **Previous tag and commits.** Limit both to the component. Without `--match`, `git describe` returns the nearest tag of any component. Without the path, the log lists other components' commits.
   ```bash
   prev="$(git describe --tags --match 'api--v*' --abbrev=0 2>/dev/null || true)"
   git log --pretty='%s' ${prev:+"$prev..HEAD"} -- packages/api
   ```
3. **Version.** Same rules, applied to that component's commits and entries.
4. **Changelog and version files.** Release that component's changelog only, and bump that component's version files only.
5. **Commit and tag.** Commit `chore(release): api v1.3.0`, then create the annotated tag `api--v1.3.0` with the message `api v1.3.0`.

## Releasing several streams at once

One release commit may release several components, and the root with them. Release each changelog and bump each version file. Commit once, for example `chore(release): api v1.3.0, web v0.9.1`, and create one annotated tag per stream on that commit.

GitHub starts no workflow run when one push carries more than three tags. Push `main` first, then push the tags by name, at most three per push:

```bash
git push origin main
git push origin api--v1.3.0 web--v0.9.1 v2.1.0
```

Do not use `git push --tags` or `--follow-tags` here. If a run is still missing, start it for that tag: `gh workflow run release.yml -f tag=api--v1.3.0`.

## The workflow

`templates/release-components.yml` releases both tag forms. Install it at `.github/workflows/release.yml` and set two values:
- `ROOT_CHANGELOG`: the root changelog, `CHANGELOG.md` by default.
- `COMPONENT_CHANGELOG`: the path template. `{component}` is replaced by the name in the tag.

Compared with `templates/release.yml`, it:
- parses the tag by the `--v` separator (a component) or a leading `v` (the root), validates the name and the version, and passes only the parsed values to later steps;
- checks out the tag itself, so a manual run behaves like a push;
- fails when the component has no changelog at the tag;
- titles releases `api v1.3.0`;
- marks root releases Latest and component releases not, so the repository's latest-release link stays on the root rather than on whichever component released last. Until the first root release is published, no release is marked Latest, and GitHub shows the release with the newest tag date, often a component; the first root release takes the link back. A repository without root releases can remove `--latest=false` and let GitHub choose;
- accepts a manual run with a `tag` input, for pushes GitHub did not act on.

Project checks go after the notes step. The most useful one checks that the version files at the tag declare `$VERSION` for `$COMPONENT`, because a forgotten bump can leave users without the update. Packaging writes into `dist/`, and the release step attaches everything there.

## Renaming or removing a component

- **Renaming.** The component starts a new changelog under its new name. Its first entry says which component it continues and links the old changelog at the old component's last tag. Old tags stay. Log the rename in the root changelog as a breaking change, and use the ecosystem's rename mechanism: a `renames` entry in a Claude Code marketplace, or a deprecation notice on the old package.
- **Removing.** Log the removal in the root changelog as a breaking change. If users need a final word, release one last version of the component first.

## Migrating from one version

1. Create each component's changelog. Move each `[Unreleased]` entry to the component it describes. Released sections stay in the root changelog, which continues as the repository's changelog.
2. Choose each component's first version. Continue the repository's current version so existing pins keep their meaning, or start at `0.1.0` if nothing was released yet.
3. Declare the components in `AGENTS.md`, install the components workflow, and record the switch as a decision.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| No workflow run after pushing tags | More than three tags in one push | Start each run with `gh workflow run release.yml -f tag=TAG`. Push at most three tags next time |
| Version chosen from the wrong commits | `git describe` without `--match`, or `git log` without the path | `--match 'api--v*'` and `-- packages/api` |
| Empty release notes for a component | The section went into the root changelog, or the tag names the wrong component | Release the component's own changelog, and make the tag name match the path template |
| Users never see a component release | Its version file was not bumped | Check the version files against the tag in the workflow |
| The latest-release link shows a component | No root release has been published yet, so GitHub falls back to the newest tag date | Publish the root release; it is marked Latest and later component releases leave it there |
| The latest-release link moves to each new component release | Component releases were marked Latest | Pass `--latest=false` on component releases, as the template does |
