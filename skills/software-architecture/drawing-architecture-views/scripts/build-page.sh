#!/usr/bin/env bash
# build-page.sh: build or rebuild architecture.html from the Markdown files of an architecture folder.
#
# Makes the page hold exactly the Markdown files under the folder, one source block each, in a
# stable order (the index README.md first, then the standing views, then the studies), and sets
# the built stamp to today's date and the short commit of the repository that holds the folder.
# When the folder has no architecture.html yet, it starts from the template in this skill.
# It writes only architecture.html, through a temporary file that is moved into place once the
# whole page is written. Every failure stops it with exit code 1 and leaves the page as it was.
#
# Needs: bash 3.2 or newer, awk, find, sort, cut, date. Optional: git, for the commit.

set -u

usage() {
  cat <<'EOF'
Usage: bash build-page.sh <architecture folder>

Builds or rebuilds <architecture folder>/architecture.html from every .md file under the folder.
Prints one line per file placed and a final line with the count.

Exit codes: 0 built, 1 wrong arguments, a missing folder or template, a file or folder that
cannot be read or written, a page without its region markers or stamp line, no Markdown files,
or a path the page cannot carry. On exit code 1 the page is as it was before the run.
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
if [ -e "$PAGE" ] || [ -L "$PAGE" ]; then
  [ -f "$PAGE" ] || fail "$PAGE is not a regular file; move it aside and run the script again"
  SOURCE="$PAGE"; CREATED=0
else
  SOURCE="$TEMPLATE"; CREATED=1
fi
[ -r "$SOURCE" ] || fail "cannot read $SOURCE; give it read permission and run the script again"

# shape FILE [BLOCKS]: one begin line, one end line after it, one stamp line; with BLOCKS, exactly
# that many closing marker lines between the region lines. Exit 1 when the shape is wrong, 2 when
# awk cannot read FILE.
shape() {
  awk -v b="$BEGIN" -v e="$END" -v want="${2:--1}" '
    $0 == b { nb++; lb = NR }
    $0 == e { ne++; le = NR }
    /^ *<p id="stamp">/ { ns++ }
    nb == 1 && ne == 0 && index($0, "</script><!-- end ") == 1 { n++ }
    END { exit !(nb == 1 && ne == 1 && lb < le && ns == 1 && (want < 0 || n == want)) }' "$1"
}

# The page must be a copy of the template.
shape "$SOURCE"
case $? in
  0) ;;
  1) fail "$SOURCE lacks its region lines ($BEGIN and $END, once each, in that order) or its stamp line; copy the template again" ;;
  *) fail "could not read $SOURCE" ;;
esac

# Every .md file under the folder, hidden folders skipped: index first, standing views, then studies.
# Each step runs on its own, so a failing find or sort stops the build instead of shortening the list.
FOUND=$(cd "$ARCH" && find . -name '.?*' -prune -o -type f -name '*.md' -print) ||
  fail "could not list the Markdown files under $ARCH; find names the folder it could not read above"
[ -n "$FOUND" ] || fail "no Markdown files under $ARCH"
KEYED=$(printf '%s\n' "$FOUND" |
  awk '{ sub(/^\.\//, ""); k = ($0 == "README.md") ? 0 : (index($0, "studies/") == 1 ? 2 : 1); print k "\t" $0 }') ||
  fail "could not order the list of Markdown files under $ARCH"
SORTED=$(printf '%s\n' "$KEYED" | LC_ALL=C sort) || fail "could not sort the list of Markdown files under $ARCH"
LIST=$(printf '%s\n' "$SORTED" | cut -f2-) || fail "could not cut the sort keys from the list of Markdown files under $ARCH"
[ -n "$LIST" ] || fail "no Markdown files under $ARCH"

# Every path must fit a marker line and every file must be readable, before anything is written.
COUNT=0
while IFS= read -r f; do
  case "$f" in
    *'"'* | *'<'* | *'>'* | *'&'* | *'\'*) fail "the page cannot carry this path, rename the file: $f" ;;
  esac
  [ -r "$ARCH/$f" ] || fail "cannot read $ARCH/$f; give it read permission or move it out of the folder, then run the script again"
  COUNT=$((COUNT + 1))
done <<EOF
$LIST
EOF

case "$LIST" in
  README.md | README.md"
"*) ;;
  *) echo "build-page.sh: warning: no README.md in $ARCH, so the page has no index" >&2 ;;
esac

DATE=$(date +%Y-%m-%d) || fail "could not read today's date"
if ! command -v git >/dev/null 2>&1 || ! git -C "$ARCH" rev-parse --git-dir >/dev/null 2>&1; then
  COMMIT='no-git'
else
  COMMIT=$(git -C "$ARCH" rev-parse --verify -q --short HEAD) || COMMIT='uncommitted'
fi

# The temporary file is created only if no file has its name, and removed on every exit before
# the move, including an interrupted run.
TMP="$ARCH/.architecture.html.$$.tmp"
MADE=0
trap 'if [ "$MADE" = 1 ]; then rm -f "$TMP"; fi' EXIT
(set -C; : >"$TMP") || fail "could not create the temporary file $TMP; check that $ARCH is writable"
MADE=1

# Each step that reads or writes is checked on its own; fail exits from inside the group.
{
  awk -v b="$BEGIN" -v date="$DATE" -v commit="$COMMIT" '
    /^ *<p id="stamp">/ { sub(/<p id="stamp">.*<\/p>/, "<p id=\"stamp\">Built <time>" date "</time> from <code>" commit "</code></p>") }
    { print }
    $0 == b { exit }' "$SOURCE" || fail "could not copy the head of $SOURCE into $TMP"
  while IFS= read -r f; do
    printf '<script type="text/markdown" data-path="%s">\n' "$f" || fail "could not write $TMP"
    # Copies the file, ends its last line with a newline, and applies the page's one escape:
    # a backslash after the < of every </script (any case) and <!--, after any backslashes there.
    LC_ALL=C awk '{
        out = ""; s = $0
        while (match(s, /<\\*(\/[Ss][Cc][Rr][Ii][Pp][Tt]|!--)/)) {
          out = out substr(s, 1, RSTART) "\\" substr(s, RSTART + 1, RLENGTH - 1)
          s = substr(s, RSTART + RLENGTH)
        }
        print out s
      }' "$ARCH/$f" || fail "could not read $ARCH/$f or write it into $TMP"
    printf '</script><!-- end %s -->\n' "$f" || fail "could not write $TMP"
  done <<EOF
$LIST
EOF
  awk -v e="$END" '$0 == e { on = 1 } on' "$SOURCE" || fail "could not copy the tail of $SOURCE into $TMP"
} >"$TMP" || fail "could not write $TMP"

shape "$TMP" "$COUNT" || fail "the new page in $TMP came out incomplete, so the page was left as it was"

mv -f "$TMP" "$PAGE" || fail "could not move the new page into place at $PAGE"
MADE=0
trap - EXIT

[ "$CREATED" = 1 ] && echo "copied the template to $PAGE"
while IFS= read -r f; do
  echo "placed $f"
done <<EOF
$LIST
EOF
echo "built $PAGE: $COUNT files, stamp $DATE from $COMMIT"
