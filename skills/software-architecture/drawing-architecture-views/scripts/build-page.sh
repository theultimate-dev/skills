#!/usr/bin/env bash
# build-page.sh: build or rebuild architecture.html from the Markdown files of an architecture folder.
#
# Makes the page hold exactly the Markdown files under the folder, one source block each, in a
# stable order (the index README.md first, then the standing views, then the studies), and sets
# the built stamp to today's date and the short commit of the repository that holds the folder.
# When the folder has no architecture.html yet, it starts from the template in this skill.
# It writes only architecture.html, through a temporary file moved into place.
#
# Needs: bash 3.2 or newer, awk, sed, find, sort, cut, date. Optional: git, for the commit.

set -u

usage() {
  cat <<'EOF'
Usage: bash build-page.sh <architecture folder>

Builds or rebuilds <architecture folder>/architecture.html from every .md file under the folder.
Prints one line per file placed and a final line with the count.

Exit codes: 0 built, 1 wrong arguments, a missing folder or template, a page without its
region markers or stamp line, no Markdown files, or a path the page cannot carry.
EOF
}

fail() { echo "build-page.sh: $1" >&2; exit 1; }

if [ $# -ne 1 ]; then usage >&2; exit 1; fi
case "$1" in -h|--help) usage; exit 0 ;; esac

[ -d "$1" ] || fail "no such folder: $1"
ARCH=$(cd -P "$1" && pwd) || fail "cannot open the folder: $1"
SCRIPTS=$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd) || fail "cannot find the script's own folder"
TEMPLATE="$(dirname "$SCRIPTS")/templates/architecture.html"
[ -f "$TEMPLATE" ] || fail "no template at $TEMPLATE; run the script from inside the drawing-architecture-views skill"

PAGE="$ARCH/architecture.html"
BEGIN='<!-- sources: begin -->'
END='<!-- sources: end -->'
if [ -f "$PAGE" ]; then SOURCE="$PAGE"; CREATED=0; else SOURCE="$TEMPLATE"; CREATED=1; fi

# The page must be a copy of the template: one begin line, one end line after it, one stamp line.
awk -v b="$BEGIN" -v e="$END" '
  $0 == b { nb++; lb = NR }
  $0 == e { ne++; le = NR }
  /^ *<p id="stamp">/ { ns++ }
  END { exit !(nb == 1 && ne == 1 && lb < le && ns == 1) }' "$SOURCE" ||
  fail "$SOURCE lacks its region lines ($BEGIN and $END, once each, in that order) or its stamp line; copy the template again"

# Every .md file under the folder, hidden folders skipped: index first, standing views, then studies.
LIST=$(cd "$ARCH" && find . -name '.?*' -prune -o -type f -name '*.md' -print |
  sed 's|^\./||' |
  awk '{ k = ($0 == "README.md") ? 0 : (index($0, "studies/") == 1 ? 2 : 1); print k "\t" $0 }' |
  LC_ALL=C sort | cut -f2-)
[ -n "$LIST" ] || fail "no Markdown files under $ARCH"

while IFS= read -r f; do
  case "$f" in
    *'"'* | *'<'* | *'>'* | *'&'* | *'\'*) fail "the page cannot carry this path, rename the file: $f" ;;
  esac
done <<EOF
$LIST
EOF

case "$LIST" in
  README.md | README.md"
"*) ;;
  *) echo "build-page.sh: warning: no README.md in $ARCH, so the page has no index" >&2 ;;
esac

DATE=$(date +%Y-%m-%d)
if ! command -v git >/dev/null 2>&1 || ! git -C "$ARCH" rev-parse --git-dir >/dev/null 2>&1; then
  COMMIT='no-git'
else
  COMMIT=$(git -C "$ARCH" rev-parse --verify -q --short HEAD) || COMMIT='uncommitted'
fi

TMP="$ARCH/.architecture.html.$$.tmp"
trap 'rm -f "$TMP"' EXIT
{
  awk -v b="$BEGIN" -v date="$DATE" -v commit="$COMMIT" '
    /^ *<p id="stamp">/ { sub(/<p id="stamp">.*<\/p>/, "<p id=\"stamp\">Built <time>" date "</time> from <code>" commit "</code></p>") }
    { print }
    $0 == b { exit }' "$SOURCE"
  while IFS= read -r f; do
    printf '<script type="text/markdown" data-path="%s">\n' "$f"
    # awk 1 ends the last line with a newline; sed applies the page's one escape.
    awk 1 "$ARCH/$f" | sed -E 's#<(\\*)(/[Ss][Cc][Rr][Ii][Pp][Tt]|!--)#<\\\1\2#g'
    printf '</script><!-- end %s -->\n' "$f"
  done <<EOF
$LIST
EOF
  awk -v e="$END" '$0 == e { on = 1 } on' "$SOURCE"
} >"$TMP" || fail "could not write $TMP"

mv -f "$TMP" "$PAGE" || fail "could not move the new page into place at $PAGE"
trap - EXIT

[ "$CREATED" = 1 ] && echo "copied the template to $PAGE"
COUNT=0
while IFS= read -r f; do
  echo "placed $f"
  COUNT=$((COUNT + 1))
done <<EOF
$LIST
EOF
echo "built $PAGE: $COUNT files, stamp $DATE from $COMMIT"
