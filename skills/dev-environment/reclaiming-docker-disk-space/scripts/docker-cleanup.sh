#!/usr/bin/env bash
# docker-cleanup.sh: remove unused Docker data older than a given age.
#
# Removes, when older than the age and not used by any container:
#   - stopped containers, unused networks, unused images, build cache
#   - anonymous volumes (the ones Docker names with a 64-character hex id)
# Never removes: anything a container uses, and named volumes. Unused named
# volumes are listed so a person can decide.
#
# Needs: bash 3.2 or newer, the docker CLI, a reachable Docker daemon.
# Optional: colima, to hand freed space back to the host after the cleanup.

set -u

AGE="24h"
DRY_RUN=0
TRIM=1

usage() {
  cat <<'EOF'
Usage: docker-cleanup.sh [--older-than <age>] [--dry-run] [--no-trim]

  --older-than <age>  Remove only what is older than this. A whole number
                      followed by h (hours) or d (days). Default: 24h.
  --dry-run           Remove nothing. Show disk usage, the commands a real
                      run would execute, and every volume it would remove.
  --no-trim           Skip handing freed space back to the host (Colima only).
  -h, --help          Show this help.

Exit codes: 0 done, 1 wrong arguments or Docker not reachable,
2 some volumes could not be removed.
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --older-than)
      [ $# -ge 2 ] || { echo "error: --older-than needs a value" >&2; exit 1; }
      AGE="$2"; shift 2 ;;
    --older-than=*) AGE="${1#*=}"; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    --no-trim) TRIM=0; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ "$AGE" =~ ^([0-9]+)h$ ]]; then
  HOURS=$((10#${BASH_REMATCH[1]}))
elif [[ "$AGE" =~ ^([0-9]+)d$ ]]; then
  HOURS=$((10#${BASH_REMATCH[1]} * 24))
else
  echo "error: --older-than takes a whole number followed by h or d, for example 24h or 7d" >&2
  exit 1
fi
if [ "$HOURS" -lt 1 ]; then
  echo "error: --older-than must be at least 1h" >&2
  exit 1
fi

command -v docker >/dev/null 2>&1 || { echo "error: the docker CLI is not on PATH" >&2; exit 1; }
docker info >/dev/null 2>&1 || { echo "error: the Docker daemon is not reachable" >&2; exit 1; }

CUTOFF=$(( $(date +%s) - HOURS * 3600 ))

# RFC 3339 timestamp, as `docker volume inspect` prints it, to Unix seconds.
# Prints nothing when the timestamp does not parse. Pure arithmetic, because
# BSD date and GNU date parse dates with different flags.
to_epoch() {
  local re='^([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})(\.[0-9]+)?(Z|([+-])([0-9]{2}):([0-9]{2}))$'
  [[ "$1" =~ $re ]] || return 0
  local y=$((10#${BASH_REMATCH[1]})) m=$((10#${BASH_REMATCH[2]})) d=$((10#${BASH_REMATCH[3]}))
  local hh=$((10#${BASH_REMATCH[4]})) mi=$((10#${BASH_REMATCH[5]})) ss=$((10#${BASH_REMATCH[6]}))
  local offset=0
  if [ "${BASH_REMATCH[8]}" != "Z" ]; then
    offset=$(( 10#${BASH_REMATCH[10]} * 3600 + 10#${BASH_REMATCH[11]} * 60 ))
    [ "${BASH_REMATCH[9]}" = "-" ] && offset=$(( -offset ))
  fi
  # Days since 1970-01-01 for a Gregorian date.
  [ "$m" -le 2 ] && y=$((y - 1))
  local era=$((y / 400))
  local yoe=$((y - era * 400))
  local mp=$(( m > 2 ? m - 3 : m + 9 ))
  local doy=$(( (153 * mp + 2) / 5 + d - 1 ))
  local doe=$(( yoe * 365 + yoe / 4 - yoe / 100 + doy ))
  local days=$(( era * 146097 + doe - 719468 ))
  echo $(( days * 86400 + hh * 3600 + mi * 60 + ss - offset ))
}

section() { printf '\n== %s ==\n' "$1"; }

# Colima keeps Docker's data on a disk image that only shrinks when trimmed.
COLIMA_PROFILE=""
context=$(docker context show 2>/dev/null || true)
if command -v colima >/dev/null 2>&1; then
  case "$context" in
    colima) COLIMA_PROFILE="default" ;;
    colima-*) COLIMA_PROFILE="${context#colima-}" ;;
  esac
fi

data_disk() {
  [ -n "$COLIMA_PROFILE" ] || return 0
  colima ssh --profile "$COLIMA_PROFILE" -- df -h /var/lib/docker 2>/dev/null
}

if [ "$DRY_RUN" -eq 1 ]; then
  section "Dry run: nothing is removed. Age limit: older than ${HOURS}h"
else
  section "Removing unused Docker data older than ${HOURS}h"
fi

if [ -n "$COLIMA_PROFILE" ]; then
  section "Data disk before (Colima profile: $COLIMA_PROFILE)"
  data_disk
fi

if [ "$DRY_RUN" -eq 1 ]; then
  section "Disk usage by type (this can take minutes when there are many volumes)"
  docker system df
fi

# --- Containers, networks, images, build cache -------------------------------

section "Stopped containers, unused networks, unused images, build cache"
if [ "$DRY_RUN" -eq 1 ]; then
  echo "A real run executes:"
  echo "  docker system prune -a -f --filter until=${HOURS}h"
  echo "  docker builder prune -a -f --filter until=${HOURS}h"
  echo "Docker has no dry run for prune, so the exact list is not known in advance."
  stopped=$(docker ps -aq -f status=exited -f status=created -f status=dead | wc -l | tr -d ' ')
  echo "Stopped containers right now, of any age: $stopped"
else
  docker system prune -a -f --filter "until=${HOURS}h" | grep -E '^Total reclaimed space' \
    | sed 's/^/system prune:  /'
  docker builder prune -a -f --filter "until=${HOURS}h" | grep -E '^Total' \
    | sed 's/^/builder prune: /'
fi

# --- Volumes ------------------------------------------------------------------

section "Volumes"
unused=$(docker volume ls -q -f dangling=true)
old_anonymous=""
old_count=0
young_count=0
unknown_count=0
named=""

if [ -n "$unused" ]; then
  # One inspect call for all of them: "<name> <created>" per line.
  # shellcheck disable=SC2086
  listing=$(docker volume inspect -f '{{.Name}} {{.CreatedAt}}' $unused 2>/dev/null)
  while read -r name created; do
    [ -n "$name" ] || continue
    if [[ "$name" =~ ^[0-9a-f]{64}$ ]]; then
      epoch=$(to_epoch "$created")
      if [ -z "$epoch" ]; then
        unknown_count=$((unknown_count + 1))
      elif [ "$epoch" -lt "$CUTOFF" ]; then
        old_anonymous="${old_anonymous}${name} ${created}"$'\n'
        old_count=$((old_count + 1))
      else
        young_count=$((young_count + 1))
      fi
    else
      named="${named}${name} ${created}"$'\n'
    fi
  done <<EOF
$listing
EOF
fi

failed=0
if [ "$old_count" -eq 0 ]; then
  echo "Unused anonymous volumes older than ${HOURS}h: none"
elif [ "$DRY_RUN" -eq 1 ]; then
  echo "Unused anonymous volumes older than ${HOURS}h, which a real run removes: $old_count"
  printf '%s' "$old_anonymous" | sed 's/^/  /'
else
  echo "Removing $old_count unused anonymous volumes older than ${HOURS}h..."
  removed=0
  while read -r name _; do
    [ -n "$name" ] || continue
    if docker volume rm "$name" >/dev/null 2>&1; then
      removed=$((removed + 1))
    else
      failed=$((failed + 1))
      echo "  could not remove $name (a container may have started using it)"
    fi
  done <<EOF
$old_anonymous
EOF
  echo "Removed: $removed. Failed: $failed."
fi
echo "Unused anonymous volumes kept because they are newer: $young_count"
[ "$unknown_count" -gt 0 ] && echo "Unused anonymous volumes kept because their age is unknown: $unknown_count"

if [ -n "$named" ]; then
  echo
  echo "Unused NAMED volumes, never removed by this script (name, created):"
  printf '%s' "$named" | sed 's/^/  /'
  echo "They usually hold data someone chose to keep, such as a database."
  echo "Remove one by name once its owner agrees: docker volume rm <name>"
fi

# --- Hand the space back, report ----------------------------------------------

if [ "$DRY_RUN" -eq 0 ]; then
  if [ -n "$COLIMA_PROFILE" ] && [ "$TRIM" -eq 1 ]; then
    section "Handing freed space back to the host (fstrim)"
    colima ssh --profile "$COLIMA_PROFILE" -- sudo fstrim -a -v 2>&1 | sed 's/^/  /'
  fi
  if [ -n "$COLIMA_PROFILE" ]; then
    section "Data disk after"
    data_disk
  fi
  section "Disk usage by type after"
  docker system df
fi

[ "$failed" -gt 0 ] && exit 2
exit 0
