#!/usr/bin/env bash
# Builds a throwaway plugin marketplace for the release-process scenarios.
# Usage: release-process-fixture.sh WORK [base|root-minor|catch-up|no-root]
#   WORK/repo    the workspace the executing agent gets, with main pushed to WORK/origin.git
#   WORK/grade   grader data the agent must not see: pushes.log, one line per ref, numbered by push
set -euo pipefail

work="${1:?usage: $0 WORK [base|root-minor|catch-up|no-root]}"
variant="${2:-base}"
skills="$(cd "$(dirname "$0")/../.." && pwd)"
template="$skills/skills/foundations/release-process/templates/release-components.yml"

mkdir -p "$work/grade"
git init -q --bare -b main "$work/origin.git"
mkdir "$work/repo"
cd "$work/repo"
git init -q -b main
git remote add origin "$work/origin.git"

url="https://github.com/acme/plugins"
alpha=0.1.0

component() {
  local name="$1" unreleased="$2" released="${3:-}"
  local latest="${4:-0.1.0}"
  mkdir -p "plugins/$name"
  {
    printf '# Changelog\n\nAll notable changes to the `%s` plugin are documented in this file.\n\n' "$name"
    printf '## [Unreleased]\n\n%s\n' "$unreleased"
    [ -n "$released" ] && printf '%s\n' "$released"
    printf '## [0.1.0] - 2026-09-01\n\n### Added\n\n- The `%s` plugin.\n\n' "$name"
    printf '[Unreleased]: %s/compare/%s--v%s...HEAD\n' "$url" "$name" "$latest"
    [ "$latest" != 0.1.0 ] && printf '[%s]: %s/compare/%s--v0.1.0...%s--v%s\n' "$latest" "$url" "$name" "$name" "$latest"
    printf '[0.1.0]: %s/releases/tag/%s--v0.1.0\n' "$url" "$name"
  } > "plugins/$name/CHANGELOG.md"
}

root_unreleased=""
alpha_released=""
if [ "$variant" = root-minor ]; then
  root_unreleased=$'### Added\n\n- The marketplace can be installed from a release archive as well as from the repository.\n'
fi
if [ "$variant" = catch-up ]; then
  # alpha 0.1.1 went out on its own, before the project adopted the option; the root lists it under [Unreleased].
  alpha=0.1.1
  alpha_released=$'## [0.1.1] - 2026-09-10\n\n### Fixed\n\n- `lint-prose` no longer flags headings as sentences.\n'
  root_unreleased="### Changed

- Components released with this version:
  - \`alpha\` [0.1.1]($url/releases/tag/alpha--v0.1.1): \`lint-prose\` no longer flags headings as sentences.
"
fi

component alpha $'### Fixed\n\n- `lint-prose` accepts British spelling.\n' "$alpha_released" "$alpha"
component beta $'### Added\n\n- A `draft-pr` skill that opens a draft pull request from the current branch.\n'
component gamma $'### Fixed\n\n- `triage` reads labels case-insensitively.\n'

cat > CHANGELOG.md <<EOF
# Changelog

All notable changes to the \`acme\` marketplace are documented in this file: the plugin catalog, and every plugin release, with a link to its notes.

## [Unreleased]

$root_unreleased
## [0.1.0] - 2026-09-01

### Added

- Marketplace with three plugins: \`alpha\`, \`beta\` and \`gamma\`.

[Unreleased]: $url/compare/v0.1.0...HEAD
[0.1.0]: $url/releases/tag/v0.1.0
EOF

mkdir -p .claude-plugin
cat > .claude-plugin/marketplace.json <<EOF
{
  "name": "acme",
  "owner": { "name": "Acme" },
  "metadata": { "version": "0.1.0" },
  "plugins": [
    { "name": "alpha", "source": "./plugins/alpha", "version": "$alpha" },
    { "name": "beta", "source": "./plugins/beta", "version": "0.1.0" },
    { "name": "gamma", "source": "./plugins/gamma", "version": "0.1.0" }
  ]
}
EOF

follows="Every plugin release is also a marketplace release, in the same release commit; the marketplace section lists the plugins released under Changed."
[ "$variant" = no-root ] && follows="The marketplace is released only for its own changes."
cat > AGENTS.md <<EOF
# AGENTS.md

## Release

Plugins and the marketplace are versioned independently.

| Stream | Changelog | Version file | Tag |
|---|---|---|---|
| A plugin | \`plugins/{component}/CHANGELOG.md\` | its entry's \`version\` in \`.claude-plugin/marketplace.json\` | \`<plugin>--vX.Y.Z\` |
| The marketplace | \`CHANGELOG.md\` | \`metadata.version\` in \`.claude-plugin/marketplace.json\` | \`vX.Y.Z\` |

$follows

There is no CI in this repository; the checks run on release tags only. Never push more than three tags at once.
EOF

mkdir -p .github/workflows
sed -e 's|"packages/{component}/CHANGELOG.md"|"plugins/{component}/CHANGELOG.md"|' \
    -e "s|ROOT_FOLLOWS_COMPONENTS: \"false\"|ROOT_FOLLOWS_COMPONENTS: \"$([ "$variant" = no-root ] && echo false || echo true)\"|" \
    "$template" > .github/workflows/release.yml

git add -A
git -c user.name=Fixture -c user.email=fixture@example.com commit -qm "chore: fixture baseline"
for tag in v0.1.0 alpha--v0.1.0 beta--v0.1.0 gamma--v0.1.0; do
  git -c user.name=Fixture -c user.email=fixture@example.com tag -a "$tag" -m "$tag"
done
if [ "$variant" = catch-up ]; then
  git -c user.name=Fixture -c user.email=fixture@example.com tag -a alpha--v0.1.1 -m "alpha v0.1.1"
fi
git push -q origin main --tags

# Record every later push for the grader, outside the workspace: "<push number> <remote ref>".
cat > "$work/origin.git/hooks/pre-receive" <<EOF
#!/usr/bin/env bash
n=\$(( \$(cat "$work/grade/push-count" 2>/dev/null || echo 0) + 1 ))
echo "\$n" > "$work/grade/push-count"
while read -r _ _ ref; do echo "\$n \$ref" >> "$work/grade/pushes.log"; done
EOF
chmod +x "$work/origin.git/hooks/pre-receive"
echo "Fixture '$variant' ready: $work/repo (grader data in $work/grade)"
