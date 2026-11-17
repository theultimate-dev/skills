# Changelog

All notable changes to the `software-architecture` plugin are documented in this file. Changes to the marketplace and the repository around it are in the [root changelog](../../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this plugin adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are tagged `software-architecture--vX.Y.Z`.

## [Unreleased]

### Added

- `drawing-architecture-views` skill: draws one question about your system as one view, a Markdown file with a Mermaid diagram and tables that tie every element and relationship to evidence, and keeps the index of views and studies. It explains the architecture to a named audience with a short guide to the views that already exist. It builds `architecture.html`, one page that shows every view and study with pan, zoom, light and dark, and any two views side by side, so nobody installs a tool to read your architecture. A bundled bash script rebuilds the page from the Markdown files, the page reports which views drew, and its Save button makes a copy that opens with no network, for sending to someone outside.

[Unreleased]: https://github.com/theultimate-dev/skills/commits/main/skills/software-architecture
