#!/usr/bin/env python3
"""Validate this skills repository against its own invariants.

Run `python3 scripts/validate.py [repo-root]`. Violations print as
`path:line: message`, warnings carry a `warning:` prefix, and any error exits 1.

Layout: `SKILL.md` only at `skills/<category>/<skill>/SKILL.md`, kebab-case
  directory names of at most 64 characters, every category holding at least one
  skill directory, its `CHANGELOG.md`, and nothing else.
Frontmatter: `---` at byte 0, a closing `---`, and between them plain
  `key: value` lines carrying exactly name, description and license; `name`
  matches the directory and is unique repository-wide, `description` is
  non-empty, at most 1024 characters and free of angle brackets, `license` is
  `MIT`.
Self-containment: relative links resolve inside the skill (links inside fenced
  code blocks are literal examples, so they are not followed), no file mentions
  `../` or a harness path even in a fence, `SKILL.md` is at most 500 lines
  (warning past 250).
Marketplace: one plugin per category, each with `source` `"./"`, `strict` false,
  a `skills` array matching the directories on disk, and a `version` equal to the
  newest released version in `skills/<category>/CHANGELOG.md`; `metadata.version`
  equal to the newest released version in the root `CHANGELOG.md`; `0.0.0` before
  a first release. `renames`, when present, maps former names only.
Decisions: `decisions/README.md` links every `NNNN-kebab-title.md` record,
  record numbers are unique, every record carries a `- Status:` line.
Changelogs: the root one (tags `vX.Y.Z`) and one per category (tags
  `<category>--vX.Y.Z`), each with `## [Unreleased]` plus version headings in
  strictly descending order. The first version links to its tag's release page,
  every later one to a compare from the version below it, and `[Unreleased]` to
  a compare from the newest tag to `HEAD`, or to a `commits/` page before a
  first release. Every plugin release also releases the marketplace, so the root
  changelog links each plugin release dated after the root's first release
  (`.../releases/tag/<category>--vX.Y.Z`), and every such link names a release
  that the plugin's changelog has.
Hygiene: `AGENTS.md` has no unbackticked `@path` import, `README.md` names every
  skill.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FIELD_RE = re.compile(r"^([a-z][a-z0-9-]*): (.+)$")
LINK_RE = re.compile(r"\]\(([^)\s]+)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
AT_IMPORT_RE = re.compile(r"@[A-Za-z0-9_./-]*\.md")
HEADING_RE = re.compile(r"^## \[(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)\] - (\d{4}-\d{2}-\d{2})( \[YANKED\])?$")
LINK_REF_RE = re.compile(r"^\[([^\]]+)\]:\s+(\S+)\s*$")
PLUGIN_RELEASE_LINK_RE = re.compile(
    r"\]\([^)\s]*/releases/tag/([a-z0-9]+(?:-[a-z0-9]+)*)--v(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)\)")
DECISION_RE = re.compile(r"^(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
STATUS_RE = re.compile(r"^- Status: (proposed|accepted|deprecated|superseded)\b")

REQUIRED_KEYS = {"name", "description", "license"}
EXTERNAL = ("http://", "https://", "mailto:")
BANNED = ("../", "~/.claude", ".claude/skills", "${CLAUDE_SKILL_DIR}", "CLAUDE_PLUGIN_ROOT")
MAX_NAME, MAX_DESCRIPTION, MAX_LINES, WARN_LINES = 64, 1024, 500, 250
EXTRA_KEYS_NOTE = ("only name, description and license are allowed here; spec fields such as compatibility,"
                   " metadata and allowed-tools, and Claude-only fields, are not permitted")
FIELD_NOTE = ("frontmatter line is not a plain 'key: value' pair (block scalars, list items, comments,"
              " continuation lines, blank lines and tabs are not allowed)")


class Report:
    """Collects every violation so one run reports all of them."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.messages: list[str] = []
        self.errors = 0
        self.warnings = 0

    def error(self, path, message: str, line: int | None = None) -> None:
        self.messages.append(self._format(path, line, message))
        self.errors += 1

    def warn(self, path, message: str, line: int | None = None) -> None:
        self.messages.append(self._format(path, line, "warning: " + message))
        self.warnings += 1

    def _format(self, path, line: int | None, message: str) -> str:
        where = self.relative(path)
        return f"{where}:{line}: {message}" if line is not None else f"{where}: {message}"

    def relative(self, path) -> str:
        try:
            return Path(path).relative_to(self.root).as_posix()
        except ValueError:
            return Path(path).as_posix()

    def finish(self) -> int:
        for message in self.messages:
            print(message)
        print(f"{self.errors} error{plural(self.errors)}, {self.warnings} warning{plural(self.warnings)}")
        return 1 if self.errors else 0


def plural(number: int) -> str:
    return "" if number == 1 else "s"


def read_text(path: Path) -> str | None:
    """Return the file as UTF-8 text, or None when it cannot be read or decoded."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def read_required(path: Path, report: Report, what: str) -> str | None:
    """Read a file the repository must have, reporting a missing or undecodable one."""
    if not path.is_file():
        report.error(path, f"{what} is missing")
        return None
    text = read_text(path)
    if text is None:
        report.error(path, "is not valid UTF-8")
    return text


def strip_quotes(value: str) -> str:
    for quote in ('"', "'"):
        if len(value) >= 2 and value.startswith(quote) and value.endswith(quote):
            return value[1:-1]
    return value


def check_layout(root: Path, report: Report) -> dict[str, dict[str, Path]]:
    """Validate the skills tree and return {category: {skill: directory}}."""
    for skill_md in sorted(root.rglob("SKILL.md")):
        parts = skill_md.relative_to(root).parts
        if ".git" not in parts and (len(parts) != 4 or parts[0] != "skills"):
            report.error(skill_md, "SKILL.md belongs only at skills/<category>/<skill>/SKILL.md")
    skills_root = root / "skills"
    if not skills_root.is_dir():
        report.error(skills_root, "skills/ directory is missing")
        return {}
    categories: dict[str, dict[str, Path]] = {}
    for category_dir in sorted(entry for entry in skills_root.iterdir() if entry.is_dir()):
        check_name(category_dir, "category", report)
        skills: dict[str, Path] = {}
        for entry in sorted(category_dir.iterdir()):
            if not entry.is_dir():
                if entry.name != "CHANGELOG.md":
                    report.error(entry, "a category directory holds only skill directories and CHANGELOG.md")
                continue
            check_name(entry, "skill", report)
            if not (entry / "SKILL.md").is_file():
                report.error(entry, "skill directory has no SKILL.md")
            skills[entry.name] = entry
        if not skills:
            report.error(category_dir, "category contains no skill directory")
        categories[category_dir.name] = skills
    if not categories:
        report.error(skills_root, "skills/ contains no category directory")
    return categories


def check_name(path: Path, kind: str, report: Report) -> None:
    if not KEBAB_RE.match(path.name):
        report.error(path, f"{kind} directory name {path.name!r} is not kebab-case")
    if len(path.name) > MAX_NAME:
        report.error(path, f"{kind} directory name is {len(path.name)} characters, maximum is {MAX_NAME}")


def check_skill(skill_dir: Path, report: Report, seen: dict[str, str]) -> None:
    skill_md = skill_dir / "SKILL.md"
    if skill_md.is_file():
        check_frontmatter(skill_md, skill_dir, report, seen)
        lines = len((read_text(skill_md) or "").splitlines())
        if lines > MAX_LINES:
            report.error(skill_md, f"SKILL.md is {lines} lines, maximum is {MAX_LINES}")
        elif lines > WARN_LINES:
            report.warn(skill_md, f"SKILL.md is {lines} lines; move depth into references/ before {MAX_LINES}")
    check_self_containment(skill_dir, report)


def parse_frontmatter(skill_md: Path, report: Report) -> dict[str, str] | None:
    """Parse the restricted `key: value` frontmatter, or report why it cannot be parsed."""
    try:
        opening = skill_md.read_bytes()[:4]
    except OSError:
        opening = b""
    if opening != b"---\n":
        report.error(skill_md, "must begin at byte 0 with a '---' line ending in a newline", line=1)
        return None
    text = read_text(skill_md)
    if text is None:
        report.error(skill_md, "is not valid UTF-8")
        return None
    lines = text.split("\n")
    closing = next((index for index in range(1, len(lines)) if lines[index] == "---"), None)
    if closing is None:
        report.error(skill_md, "frontmatter has no closing '---' line")
        return None
    fields: dict[str, str] = {}
    for index in range(1, closing):
        match = FIELD_RE.match(lines[index])
        if match is None:
            report.error(skill_md, FIELD_NOTE, line=index + 1)
            continue
        if match.group(1) in fields:
            report.error(skill_md, f"duplicate frontmatter key {match.group(1)!r}", line=index + 1)
        fields[match.group(1)] = strip_quotes(match.group(2))
    return fields


def check_frontmatter(skill_md: Path, skill_dir: Path, report: Report, seen: dict[str, str]) -> None:
    fields = parse_frontmatter(skill_md, report)
    if fields is None:
        return
    for missing in sorted(REQUIRED_KEYS - set(fields)):
        report.error(skill_md, f"frontmatter is missing the {missing!r} key")
    extra = sorted(set(fields) - REQUIRED_KEYS)
    if extra:
        report.error(skill_md, f"unsupported frontmatter keys {', '.join(repr(k) for k in extra)}: {EXTRA_KEYS_NOTE}")
    check_name_field(skill_md, skill_dir, fields.get("name"), report, seen)
    description = fields.get("description")
    if description is not None:
        if not description.strip():
            report.error(skill_md, "description is empty")
        if len(description) > MAX_DESCRIPTION:
            report.error(skill_md, f"description is {len(description)} characters, maximum is {MAX_DESCRIPTION}")
        if "<" in description or ">" in description:
            report.error(skill_md, "description must not contain '<' or '>'")
    if fields.get("license") not in (None, "MIT"):
        report.error(skill_md, f"license is {fields['license']!r}, expected 'MIT'")


def check_name_field(skill_md: Path, skill_dir: Path, name, report: Report, seen: dict[str, str]) -> None:
    if name is None:
        return
    if name != skill_dir.name:
        report.error(skill_md, f"name {name!r} does not match directory name {skill_dir.name!r}")
    if not KEBAB_RE.match(name):
        report.error(skill_md, f"name {name!r} is not kebab-case")
    if len(name) > MAX_NAME:
        report.error(skill_md, f"name is {len(name)} characters, maximum is {MAX_NAME}")
    if name in seen:
        report.error(skill_md, f"name {name!r} is already used by {seen[name]}")
    else:
        seen[name] = report.relative(skill_dir)


def check_self_containment(skill_dir: Path, report: Report) -> None:
    skill_root = skill_dir.resolve()
    for path in sorted(entry for entry in skill_dir.rglob("*") if entry.is_file()):
        text = read_text(path)
        if text is None:
            continue
        fenced = False
        for number, line in enumerate(text.splitlines(), 1):
            for banned in BANNED:
                if banned in line:
                    report.error(path, f"a skill must not reference {banned!r}", line=number)
            if line.strip().startswith(("```", "~~~")):
                fenced = not fenced
            elif not fenced and path.suffix == ".md":
                check_links(path, skill_root, line, number, report)


def check_links(path: Path, skill_root: Path, line: str, number: int, report: Report) -> None:
    for target in LINK_RE.findall(line):
        if target.startswith(EXTERNAL) or target.startswith("#"):
            continue
        cleaned = target.split("#", 1)[0]
        if not cleaned:
            continue
        destination = path.parent / cleaned
        if not destination.resolve().is_relative_to(skill_root):
            report.error(path, f"link target {target!r} points outside the skill directory", line=number)
        elif not destination.exists():
            report.error(path, f"link target {target!r} does not exist", line=number)


def check_marketplace(root: Path, categories: dict[str, dict[str, Path]], version: str | None,
                      plugin_versions: dict[str, str | None], report: Report) -> None:
    path = root / ".claude-plugin" / "marketplace.json"
    text = read_required(path, report, "marketplace manifest")
    if text is None:
        return
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        report.error(path, f"invalid JSON: {error.msg}", line=error.lineno)
        return
    if not isinstance(data, dict):
        report.error(path, "the top level must be a JSON object")
        return
    if not isinstance(data.get("name"), str) or not KEBAB_RE.match(data.get("name") or ""):
        report.error(path, "'name' must be a kebab-case string")
    owner = data.get("owner")
    if not isinstance(owner, dict) or not isinstance(owner.get("name"), str):
        report.error(path, "'owner' must be an object with a string 'name'")
    metadata = data.get("metadata")
    if not isinstance(metadata, dict) or "version" not in metadata:
        report.error(path, "'metadata' must be an object carrying the marketplace 'version'")
    else:
        check_version(path, metadata["version"], version or "0.0.0", "metadata.version", "CHANGELOG.md", report)
    plugins = data.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        report.error(path, "'plugins' must be a non-empty array")
        return
    named: set[str] = set()
    for index, plugin in enumerate(plugins):
        if not isinstance(plugin, dict) or not isinstance(plugin.get("name"), str):
            report.error(path, f"plugins[{index}] must be an object with a string 'name'")
            continue
        if plugin["name"] in named:
            report.error(path, f"duplicate plugin name {plugin['name']!r}")
        named.add(plugin["name"])
        check_plugin(root, path, plugin, categories, plugin_versions.get(plugin["name"]) or "0.0.0", report)
    for missing in sorted(set(categories) - named):
        report.error(path, f"category {missing!r} has no plugin entry")
    for extra in sorted(named - set(categories)):
        report.error(path, f"plugin {extra!r} has no matching category directory under skills/")
    check_renames(path, data.get("renames"), named, report)


def check_plugin(root: Path, path: Path, plugin: dict, categories: dict, version: str, report: Report) -> None:
    name = plugin["name"]
    if plugin.get("source") != "./":
        report.error(path, f"plugin {name!r}: 'source' must be \"./\"")
    if plugin.get("strict") is not False:
        report.error(path, f"plugin {name!r}: 'strict' must be false")
    if "version" not in plugin:
        report.error(path, f"plugin {name!r}: 'version' is missing")
    else:
        check_version(path, plugin["version"], version, f"plugin {name!r} version",
                      f"skills/{name}/CHANGELOG.md", report)
    listed = plugin.get("skills")
    if not isinstance(listed, list) or not listed:
        report.error(path, f"plugin {name!r}: 'skills' must be a non-empty array")
        return
    found: set[str] = set()
    for entry in listed:
        skill = check_skill_entry(root, path, name, entry, report)
        if skill is None:
            continue
        if skill in found:
            report.error(path, f"plugin {name!r} lists skill {skill!r} twice")
        found.add(skill)
    for missing in sorted(set(categories.get(name, {})) - found):
        report.error(path, f"plugin {name!r} does not list skill {missing!r} that exists on disk")


def check_skill_entry(root: Path, path: Path, plugin: str, entry, report: Report) -> str | None:
    """Validate one `skills[]` path and return the skill directory name it points at."""
    if not isinstance(entry, str) or not entry.startswith("./"):
        report.error(path, f"plugin {plugin!r}: skill entry {entry!r} must be a string starting with './'")
        return None
    parts = Path(entry[2:]).parts
    if len(parts) != 3 or parts[0] != "skills" or parts[1] != plugin:
        report.error(path, f"plugin {plugin!r}: skill entry {entry!r} must be under ./skills/{plugin}/")
        return None
    directory = root / Path(*parts)
    if not directory.is_dir():
        report.error(path, f"plugin {plugin!r}: skill entry {entry!r} is not a directory")
        return None
    if not (directory / "SKILL.md").is_file():
        report.error(path, f"plugin {plugin!r}: skill entry {entry!r} has no SKILL.md")
        return None
    return parts[2]


def check_renames(path: Path, renames, plugins: set[str], report: Report) -> None:
    """Validate the optional `renames` map: former names to a current name, a later former name, or null."""
    if renames is None:
        return
    if not isinstance(renames, dict):
        report.error(path, "'renames' must be an object mapping former plugin names to a name or null")
        return
    for former, current in renames.items():
        if former in plugins:
            report.error(path, f"renames: {former!r} is still a plugin in 'plugins'")
        if current is not None and (not isinstance(current, str) or (current not in plugins and current not in renames)):
            report.error(path, f"renames: {former!r} must map to a plugin in 'plugins', another former name, or null")


def check_version(path: Path, value, expected: str, label: str, source: str, report: Report) -> None:
    if not isinstance(value, str):
        report.error(path, f"{label} must be a string")
    elif value != expected:
        report.error(path, f"{label} is {value!r}, expected {expected!r} from {source}")


def check_changelog(path: Path, prefix: str, report: Report) -> list[tuple[str, str]]:
    """Validate one changelog whose tags are `<prefix>X.Y.Z` and return its releases as (version, date), newest first."""
    text = read_required(path, report, "changelog")
    if text is None:
        return []
    headings: list[tuple[str, int]] = []
    dates: dict[str, str] = {}
    references: dict[str, tuple[str, int]] = {}
    unreleased = False
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(("```", "~~~")):
            fenced = not fenced
        elif fenced:
            continue
        elif line == "## [Unreleased]":
            unreleased = True
        elif line.startswith("## "):
            match = HEADING_RE.match(line)
            if match is None:
                report.error(path, f"heading {line!r} is not '## [x.y.z] - YYYY-MM-DD'", line=number)
            else:
                headings.append((match.group(1), number))
                dates.setdefault(match.group(1), match.group(2))
        elif reference := LINK_REF_RE.match(line):
            references[reference.group(1)] = (reference.group(2), number)
    if not unreleased:
        report.error(path, "no '## [Unreleased]' heading")
    check_versions(path, headings, references, prefix, report)
    newest = headings[0][0] if headings else None
    check_unreleased_link(path, references, prefix, newest, report)
    return [(version, dates[version]) for version, _ in headings]


def check_versions(path: Path, headings: list, references: dict, prefix: str, report: Report) -> None:
    seen: set[str] = set()
    for index, (version, number) in enumerate(headings):
        if version in seen:
            report.error(path, f"version {version} appears more than once", line=number)
        seen.add(version)
        older = headings[index + 1][0] if index + 1 < len(headings) else None
        check_version_link(path, references, version, older, prefix, number, report)
    for (newer, _), (older, number) in zip(headings, headings[1:]):
        if semver_key(newer) <= semver_key(older):
            report.error(path, f"version {older} must sort below {newer} above it; releases go newest first", line=number)


def check_version_link(path: Path, references: dict, version: str, older: str | None, prefix: str,
                       number: int, report: Report) -> None:
    """The first release links to its tag's release page; every later one compares against the release below."""
    if version not in references:
        report.error(path, f"version {version} has no '[{version}]: <url>' link reference", line=number)
        return
    url, line = references[version]
    tag = prefix + version
    expected = f"/compare/{prefix}{older}...{tag}" if older else f"/releases/tag/{tag}"
    if not url.endswith(expected):
        report.error(path, f"the [{version}] link must end with '{expected}'", line=line)


def check_unreleased_link(path: Path, references: dict, prefix: str, newest: str | None, report: Report) -> None:
    if "Unreleased" not in references:
        report.error(path, "no '[Unreleased]: <url>' link reference definition")
        return
    url, number = references["Unreleased"]
    if newest is None:
        if "/commits/" not in url:
            report.error(path, "before the first release, the [Unreleased] link must be a 'commits/' URL", line=number)
    elif not url.endswith(f"/compare/{prefix}{newest}...HEAD"):
        report.error(path, f"the [Unreleased] link must end with '/compare/{prefix}{newest}...HEAD'", line=number)


def check_plugin_releases_listed(root: Path, releases: list[tuple[str, str]],
                                 plugin_releases: dict[str, list[tuple[str, str]]], report: Report) -> None:
    """Every plugin release also releases the marketplace, whose changelog links it.

    The plugins' first releases shipped with the marketplace's first release, which introduced them,
    so only plugin releases dated after it must be linked.
    """
    path = root / "CHANGELOG.md"
    text = read_text(path)
    if text is None:
        return
    listed: set[tuple[str, str]] = set()
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced:
            continue
        for match in PLUGIN_RELEASE_LINK_RE.finditer(line):
            plugin, version = match.groups()
            if version not in dict(plugin_releases.get(plugin, [])):
                report.error(path, f"links {plugin}--v{version}, which skills/{plugin}/CHANGELOG.md has not released",
                             line=number)
            listed.add((plugin, version))
    if not releases:
        return
    first = releases[-1][1]
    for plugin in sorted(plugin_releases):
        for version, date in plugin_releases[plugin]:
            if date > first and (plugin, version) not in listed:
                report.error(path, f"does not link the {plugin} {version} release of {date}; every plugin release"
                                   " also releases the marketplace, whose section lists the plugin under Changed")


def semver_key(version: str) -> tuple:
    """Order versions numerically, ranking a pre-release below its own release."""
    core, _, pre = version.partition("-")
    major, minor, patch = (int(part) for part in core.split("."))
    return (major, minor, patch, 0 if pre else 1, pre)


def check_decisions(root: Path, report: Report) -> None:
    directory = root / "decisions"
    index = directory / "README.md"
    records: list[Path] = []
    numbers: dict[str, str] = {}
    for record in sorted(directory.glob("*.md")) if directory.is_dir() else []:
        if record.name == "README.md":
            continue
        match = DECISION_RE.match(record.name)
        if match is None:
            report.error(record, "decision records must be named NNNN-kebab-title.md")
            continue
        records.append(record)
        if match.group(1) in numbers:
            report.error(record, f"decision number {match.group(1)} is already used by {numbers[match.group(1)]}")
        numbers.setdefault(match.group(1), record.name)
        check_status(record, report)
    text = read_required(index, report, "decisions/README.md")
    if text is None:
        return
    linked = index_links(index, directory, text, report)
    for record in records:
        if record.name not in linked:
            report.error(record, "decision record is not linked from decisions/README.md")


def index_links(index: Path, directory: Path, text: str, report: Report) -> set[str]:
    """Report unresolvable links in the decision index and return the targets it names."""
    linked: set[str] = set()
    for number, line in enumerate(text.splitlines(), 1):
        for target in LINK_RE.findall(line):
            if target.startswith(EXTERNAL) or target.startswith("#"):
                continue
            cleaned = target.split("#", 1)[0].removeprefix("./")
            if not cleaned:
                continue
            linked.add(cleaned)
            if not (directory / cleaned).exists():
                report.error(index, f"link target {target!r} does not exist", line=number)
    return linked


def check_status(record: Path, report: Report) -> None:
    wrong = None
    for number, line in enumerate((read_text(record) or "").splitlines(), 1):
        if STATUS_RE.match(line):
            return
        if line.startswith("- Status:") and wrong is None:
            wrong = (line, number)
    if wrong is None:
        report.error(record, "no '- Status: proposed|accepted|deprecated|superseded' line")
    else:
        report.error(record, f"{wrong[0]!r} is not proposed, accepted, deprecated or superseded", line=wrong[1])


def check_agents(root: Path, report: Report) -> None:
    path = root / "AGENTS.md"
    text = read_required(path, report, "AGENTS.md")
    if text is None:
        return
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(("```", "~~~")):
            fenced = not fenced
        elif fenced:
            continue
        elif line.startswith("@"):
            report.error(path, "line starts with '@'; AGENTS.md must not import other files", line=number)
        elif AT_IMPORT_RE.search(INLINE_CODE_RE.sub(" ", line)):
            report.error(path, "unbackticked '@path' import; wrap the path in backticks or use a link", line=number)


def check_readme(root: Path, categories: dict[str, dict[str, Path]], report: Report) -> None:
    path = root / "README.md"
    text = read_required(path, report, "README.md")
    if text is None:
        return
    for category in sorted(categories):
        for skill in sorted(categories[category]):
            if skill not in text:
                report.error(path, f"README.md does not mention the skill {skill!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate.py",
        description="Check this skills repository against the invariants in AGENTS.md.",
        epilog="Prints one 'path:line: message' per violation, then a summary. Exits 1 on any error;"
               " warnings are printed but do not fail the run.")
    parser.add_argument("root", nargs="?", default=".", help="repository root (default: the working directory)")
    root = Path(parser.parse_args(argv).root).resolve()
    if not root.is_dir():
        print(f"{root}: not a directory", file=sys.stderr)
        return 2
    report = Report(root)
    categories = check_layout(root, report)
    seen: dict[str, str] = {}
    for category in sorted(categories):
        for skill in sorted(categories[category]):
            check_skill(categories[category][skill], report, seen)
    releases = check_changelog(root / "CHANGELOG.md", "v", report)
    plugin_releases = {category: check_changelog(root / "skills" / category / "CHANGELOG.md", f"{category}--v", report)
                       for category in sorted(categories)}
    check_marketplace(root, categories, releases[0][0] if releases else None,
                      {category: versions[0][0] if versions else None for category, versions in plugin_releases.items()},
                      report)
    check_plugin_releases_listed(root, releases, plugin_releases, report)
    check_decisions(root, report)
    check_agents(root, report)
    check_readme(root, categories, report)
    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
