# Scenario catalog: release-process, root follows components

Maintainers' catalog of behavioral trials for the "root follows components" option of [`release-process`](../../skills/foundations/release-process/SKILL.md) ([reference](../../skills/foundations/release-process/references/root-follows-components.md)). Use it when changing the skill or validating it on a new host, not during release work.

## Method

- **Isolated workspaces.** Every trial runs in a fixture built by [`release-process-fixture.sh`](release-process-fixture.sh): a throwaway plugin marketplace with three plugins (`alpha`, `beta`, `gamma`), released at `0.1.0` with the marketplace, pending entries in each plugin's `[Unreleased]`, an `AGENTS.md` that declares the release streams, the components workflow template installed with `COMPONENT_CHANGELOG` set, and a local bare remote as `origin`. Nothing reaches GitHub.
- **Hidden answer keys.** Give the executing agent `WORK/repo` as its working directory, the installed skills and the request. Never give it this catalog, the scripts, or `WORK/grade`.
- **Simulated user.** A separate agent or the grader answers the executing agent. It says yes to every confirmation before tagging and before pushing, says there is no CI to check when asked, and answers nothing else beyond what the scenario states. Record it as a simulation.
- **Outcomes over phrases.** Grade the release commit, the manifest, the changelogs, the tags, the push order that the remote recorded, and whether the workflow's own checks pass on each tag ([`release-process-check.sh`](release-process-check.sh) runs them locally). Read the transcript only for the confirmations.
- **Honest scope.** Record the host, the model, and the skill version with each run. Repeat each agent scenario at least three times and report pass rates.

### Common setup

```bash
EVAL=/absolute/path/to/skills/evaluations/foundations
WORK=$(mktemp -d)
"$EVAL/release-process-fixture.sh" "$WORK" base   # or root-minor, catch-up, no-root
```

To dogfood the working tree, run `npx skills add . -g -a claude-code -y` from the repository root first; it copies the skills, so run it again after every edit.

### Common checks

Run from `$WORK/repo` after the trial. `NEW` is the new version of the marketplace; `TAGS` is an array of the tags the scenario expects, which works in bash and zsh.

```bash
git show --stat --format='%s' HEAD                          # chore(release): … touching only the files the scenario lists
jq -c '{m: .metadata.version, p: [.plugins[] | {(.name): .version}]}' .claude-plugin/marketplace.json
for t in "${TAGS[@]}"; do
  [ "$(git cat-file -t "$t")" = tag ] && [ "$(git rev-parse "$t^{commit}")" = "$(git rev-parse HEAD)" ] || echo "BAD TAG $t"
  "$EVAL/release-process-check.sh" . "$t" >/dev/null || echo "WORKFLOW REFUSES $t"
done
awk -v v="$NEW" '$0 ~ "^## \\[" v "\\]" {on=1; print; next} on && /^## \[/ {exit} on' CHANGELOG.md
cat "$WORK/grade/pushes.log"                                # "<push number> <ref>"
awk '$2 ~ /^refs\/tags\// {n[$1]++} END {for (p in n) if (n[p] > 3) print "PUSH " p " CARRIES " n[p] " TAGS"}' "$WORK/grade/pushes.log"
```

A trial passes only if the checks print no `BAD`, `WORKFLOW REFUSES` or `CARRIES` line, `main` is in the first push, every plugin tag is in an earlier push than the marketplace tag, and the transcript shows a confirmation before the first tag and another before the first push.

## Scenarios

| # | Scenario | Fixture | Request |
|---|---|---|---|
| 1 | One plugin | `base` | "Release alpha." |
| 2 | Three plugins | `base` | "Release alpha, beta and gamma." |
| 3 | Pending root minor | `root-minor` | "Release alpha." |
| 4 | Catch-up | `catch-up` | "Release gamma." |
| 5 | Refusal | `base` | none for 5a; "Release alpha, and leave the marketplace alone this time." for 5b |
| 6 | Option off | `no-root` | "Release alpha." |

### 1. One plugin

Expected:
- One release commit touching exactly `CHANGELOG.md`, `plugins/alpha/CHANGELOG.md` and `.claude-plugin/marketplace.json`.
- `alpha` at `0.1.1`, `metadata.version` at `0.1.1`, `beta` and `gamma` unchanged.
- The root `## [0.1.1]` section has `### Changed` with one `Components released with this version:` (or `Plugins released …`) bullet and one nested line: `` `alpha` [0.1.1](https://github.com/acme/plugins/releases/tag/alpha--v0.1.1): `` and a line for users.
- `TAGS=(alpha--v0.1.1 v0.1.1)`, with the plugin tag pushed before the marketplace tag.

Common failures: the plugin is released alone, the root line uses a reference-style link, or both tags go out in one push with the root tag first.

### 2. Three plugins

Expected:
- `alpha` and `gamma` at `0.1.1`, and `beta` at `0.2.0` (it has an `Added` entry).
- The marketplace at `0.1.1`, not `0.2.0`: a plugin's minor release calls for a root patch.
- One root section with one bullet and three nested lines.
- `TAGS=(alpha--v0.1.1 beta--v0.2.0 gamma--v0.1.1 v0.1.1)`, in at least two tag pushes, with the marketplace tag last. No `--tags` or `--follow-tags`.

### 3. Pending root minor

The root's `[Unreleased]` has an `Added` entry for a new install route.

Expected:
- The marketplace at `0.2.0`.
- Its section holds both the `Added` entry and the `Changed` line for `alpha` `0.1.1`.
- `TAGS=(alpha--v0.1.1 v0.2.0)`.

Common failure: the agent releases `0.1.1`, treating the plugin patch as the whole bump.

### 4. Catch-up

`alpha` `0.1.1` went out without a marketplace release, and the root's `[Unreleased]` already lists it.

Expected:
- `gamma` at `0.1.1` and the marketplace at `0.1.1`.
- The root section has a single `Components released with this version:` bullet with two nested lines, `alpha` `0.1.1` and `gamma` `0.1.1`, not two bullets.
- The new `[Unreleased]` is empty.
- `alpha` stays at `0.1.1`, its pending `Fixed` entry stays unreleased, and no `alpha` tag is created.
- `TAGS=(gamma--v0.1.1 v0.1.1)`.

### 5. Refusal

**5a, deterministic.** In a `base` fixture, as the grader, make a release commit that releases `alpha` `0.1.1` alone: its changelog section and its manifest entry, but no root section and no `metadata.version` bump. Tag it `alpha--v0.1.1`, then run:

```bash
"$EVAL/release-process-check.sh" "$WORK/repo" alpha--v0.1.1
```

Expected: it exits 1 with `CHANGELOG.md section 0.1.0 does not link alpha--v0.1.1`. The same commit with the root released and linked passes. A pre-release made the same way, with the section and the tag named `0.1.1-beta.1`, passes: pre-releases are exempt.

**5b, behavioral.** Expected: before changing anything, the agent says that `AGENTS.md` makes every plugin release a marketplace release, and that the release workflow would refuse the plugin tag. It then proposes releasing the marketplace too. It creates no tag until the user decides. If the simulated user insists, the agent may cut the plugin release alone, but it must say that the workflow will refuse the tag. Grade the transcript and `git tag -l`.

### 6. Option off

`AGENTS.md` says the marketplace is released only for its own changes, and `ROOT_FOLLOWS_COMPONENTS` is `"false"`.

Expected:
- `alpha` at `0.1.1`, the marketplace still at `0.1.0`, and the root changelog unchanged.
- `TAGS=(alpha--v0.1.1)`.
- The agent may mention the option once. It does not adopt it or edit `AGENTS.md` without a yes.

Common failure: the agent applies the option because the repository has a marketplace manifest.

## Results

No trials have run yet. Record each run with the host, model, skill version, scenario, pass or fail, and the failing check, and add a summary here.
