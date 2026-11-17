# Changelog

All notable changes to the `software-architecture` plugin are documented in this file. Changes to the marketplace and the repository around it are in the [root changelog](../../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this plugin adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are tagged `software-architecture--vX.Y.Z`.

## [Unreleased]

### Added

- `drawing-architecture-views` skill: draws one question about your system as one view, a Markdown file with a Mermaid diagram and tables that tie every element and relationship to evidence, and keeps the index of views and studies. It explains the architecture to a named audience with a short guide to the views that already exist. It builds `architecture.html`, one page that shows every view and study with pan, zoom, light and dark, and any two views side by side, so nobody installs a tool to read your architecture. A bundled bash script rebuilds the page from the Markdown files, the page reports which views drew, and its Save button makes a copy that opens with no network, for sending to someone outside.
- `recovering-built-architecture` skill: answers "what is really there?" for an application nobody has drawn. It reads manifests, entry points, configuration, infrastructure files and schema, and writes context and container views in which every element and relationship cites the file that proves it, with a date and commit. It keeps apart what the code shows, what only deployment configuration says and what only the running system could confirm, describes a part by what its code does when its name says otherwise, and lists the blind spots with what would settle each.
- `evaluating-architecture-risks` skill: takes a critical look at a problem, a design or a proposal before a consequential change. It restates the question without the solution you named, picks three to five measurable scenarios, and traces each through the views element by element. Then it looks for what the scenarios miss: single points of failure, each dependency slow or down, sensitive data crossing a trust boundary, and a short premortem. You get a dated risk review: a verdict per scenario, risks ranked and pinned to elements with cause and evidence, the trade-offs, and the next check for each top risk. It says so when the problem needs no architecture change.
- `exploring-architecture-options` skill: answers "what are our options?" for a choice about the system as a whole, including a system that does not exist yet. It checks what the code and the decision log already settle, then sketches two or three options that differ in kind, one of them the smallest change that could work, each as a view at the same level. It traces the same scenarios through each and gives you a matrix with a sentence per cell instead of scores, a recommendation, and what would reverse it. You pick in your own words; the study records the pick and offers a decision record, and until you pick it says the choice is waiting.

[Unreleased]: https://github.com/theultimate-dev/skills/commits/main/skills/software-architecture
