# Changelog

All notable changes to Operator Skills are recorded here. This project follows
[semantic versioning](https://semver.org).

Note on releases: `plugin.json` declares an explicit version, so it must be
incremented for installed users to receive updates. Pushing commits alone has
no effect — Claude Code sees an unchanged version string and retains its cached
copy. Bump the version in both `.claude-plugin/plugin.json` and
`.claude-plugin/marketplace.json` together.

## [1.1.0] — 2026-07-30

### Added
- Packaged as an installable Claude Code plugin with an accompanying
  marketplace manifest, reducing installation to two commands
- `media-transcriber` skill, including a runnable `transcribe.py` implementing
  a three-tier fallback: caption retrieval, audio extraction, then
  browser-playback loopback capture into local Whisper

### Changed
- Documentation rewritten to lead with the failure modes each skill corrects
  rather than a feature summary

## [1.0.0] — 2026-07-11

### Added
- Initial release: `youtube-research-miner`, `local-lead-finder`,
  `govcon-scout`
