#!/usr/bin/env bash
# Runs the release workflow's own checks for one tag, locally, without GitHub.
# Usage: release-process-check.sh REPO TAG
# Executes the steps "Parse the tag", "Extract release notes" and, when its condition holds,
# "Check the root release lists the component" from REPO/.github/workflows/release.yml, in a
# temporary checkout of TAG, and exits with the first failing step's status. Needs Ruby or PyYAML.
set -euo pipefail

repo="$(cd "${1:?usage: $0 REPO TAG}" && pwd)"
tag="${2:?usage: $0 REPO TAG}"
tmp="$(mktemp -d)"
trap 'git -C "$repo" worktree remove --force "$tmp/tree" >/dev/null 2>&1 || true; rm -rf "$tmp"' EXIT

workflow="$repo/.github/workflows/release.yml"
steps=("Parse the tag" "Extract release notes" "Check the root release lists the component")
extract() {
  if ruby -ryaml -e '' 2>/dev/null; then
    ruby -ryaml -e '
      job = YAML.load_file(ARGV[0])["jobs"]["release"]
      job["env"].each { |k, v| puts "#{k}=#{v}" if v.is_a?(String) && !v.include?("${{") } if ARGV[1] == "env"
      step = job["steps"].find { |s| s["name"] == ARGV[1] }
      if step then File.write(ARGV[2], step["run"]); File.write(ARGV[2] + ".if", step["if"].to_s) end
    ' "$workflow" "$@"
  else
    python3 - "$workflow" "$@" <<'PY'
import sys, yaml
job = yaml.safe_load(open(sys.argv[1]))["jobs"]["release"]
if sys.argv[2] == "env":
    for k, v in job["env"].items():
        if isinstance(v, str) and "${{" not in v:
            print(f"{k}={v}")
for step in job["steps"]:
    if step.get("name") == sys.argv[2]:
        open(sys.argv[3], "w").write(step["run"])
        open(sys.argv[3] + ".if", "w").write(step.get("if", ""))
PY
  fi
}

git -C "$repo" worktree add -q --detach "$tmp/tree" "refs/tags/$tag"
export TAG="$tag" RUNNER_TEMP="$tmp" GITHUB_ENV="$tmp/github-env"
: > "$GITHUB_ENV"
while IFS='=' read -r key value; do export "$key=$value"; done < <(extract env)

for i in "${!steps[@]}"; do
  extract "${steps[$i]}" "$tmp/step$i.sh"
  [ -f "$tmp/step$i.sh" ] || { echo "no step '${steps[$i]}' in $workflow"; exit 2; }
  while IFS='=' read -r key value; do export "$key=$value"; done < "$GITHUB_ENV"
  # Only the root check has a condition: a component tag, with ROOT_FOLLOWS_COMPONENTS on.
  condition="$(cat "$tmp/step$i.sh.if")"
  if [ -n "$condition" ] && ! { [ -n "$COMPONENT" ] && [ "${ROOT_FOLLOWS_COMPONENTS:-}" = true ]; }; then
    echo "skip: ${steps[$i]}"; continue
  fi
  echo "run:  ${steps[$i]}"
  ( cd "$tmp/tree" && bash -e "$tmp/step$i.sh" )
done
echo "pass: $tag"
