<p align="center">
  <img src=".github/assets/logo.jpg" alt="Operator Skills" width="140">
</p>

<h1 align="center">Operator Skills</h1>

<p align="center">
  Engineering-grade skills for Claude Code: research, lead generation,<br>and product construction.<br>
  <a href="https://opforge.gumroad.com/l/operator-skills-free">Download as zip</a> ·
  <a href="https://opforge.gumroad.com/l/operator-stack">Full 11-skill stack</a> ·
  <a href="#install">Install</a>
</p>

<p align="center">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg">
  <img alt="Skills: 4" src="https://img.shields.io/badge/skills-4-38bdf8.svg">
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-ready-a78bfa.svg">
</p>

---


Four MIT-licensed skills for [Claude Code](https://claude.com/claude-code), each
derived from a pipeline in active use rather than composed speculatively. Every
procedure documented here has been executed against live systems: the lead
finder against OpenStreetMap's Overpass endpoint at roughly 300 records per
metro, the research miner across 100-video channel archives, the contract scout
against USAspending's award API.

What these files encode is not capability but **failure modes**. Calling the
APIs is the easy part. The cost is in discovering that auto-generated caption
tracks are emitted as rolling cues that triple your token count under naive
parsing; that OpenStreetMap's absent-website attribute is a false positive on
franchise locations; that SAM.gov answers an unprovisioned key with a 404
rather than a 401. Each skill carries the correction inline, with the reasoning
intact.

## The skills

| Skill | What Claude learns to do |
|---|---|
| **[media-transcriber](skills/media-transcriber/SKILL.md)** | Transcribe any audible source — YouTube, TikTok, local files, or authenticated Instagram/Facebook content with no caption track. Three-tier pipeline: caption retrieval, audio extraction, then browser-playback loopback capture into local Whisper. Ships a runnable `transcribe.py`. |
| **[youtube-research-miner](skills/youtube-research-miner/SKILL.md)** | Transcribe and mine a single video or an entire channel without the YouTube API. Correct cue-level VTT deduplication, channel-scale distillation, and claim extraction. |
| **[local-lead-finder](skills/local-lead-finder/SKILL.md)** | Identify businesses with no web presence in any municipality via OpenStreetMap. Opportunity scoring, franchise filtering, and contact enrichment. No API keys required. |
| **[govcon-scout](skills/govcon-scout/SKILL.md)** | Query federal procurement: award data by NAICS category, contract value, and state via USAspending, plus open solicitations via SAM.gov. |

<a name="install"></a>

## Install

**As a plugin (recommended)** — inside Claude Code:

```
/plugin marketplace add z0157/claude-operator-skills
/plugin install operator-skills@opforge
```

All four skills install together. Subsequent releases arrive via `/plugin update`.

**Or copy the files manually**, if you'd rather not add a marketplace:

```bash
git clone https://github.com/z0157/claude-operator-skills
cp -r claude-operator-skills/skills/* ~/.claude/skills/   # all projects
```

In either case, invoke them in natural language — "find businesses without
websites in Boise", "transcribe this channel and extract every revenue claim"
— and Claude Code resolves the appropriate skill automatically.

## Why these are different

Most published skills are prompt text with no executable substance behind
them. These document the specific defects that make each task non-obvious:
the cue-level dedupe required to parse rolling caption tracks correctly, the
franchise denylist that removes false positives from OpenStreetMap's
missing-website signal, the authentication behaviour that makes SAM.gov's
demonstration key appear to be a routing error. That is the difference between
a skill that demonstrates well and one that survives contact with production
data.

## The full Operator Stack (11 skills)

The paid stack adds the production layer — the skills that convert research
and lead data into shippable artefacts and billable output:

- **client-site-builder** — self-contained single-file websites for local businesses, themed per industry with schema.org LocalBusiness markup, verified at desktop and mobile breakpoints
- **cold-outreach-drafter** — proof-of-work outreach sequences with CAN-SPAM and TCPA constraints enforced at the template level
- **pdf-product-factory** — typeset PDF deliverables (forms, bundles, workbooks) rendered from HTML/CSS at catalogue scale
- **spreadsheet-tool-builder** — Excel instruments whose formulas are verified against parallel Python computation before shipping
- **stripe-no-sdk** — payments, subscriptions and payment links over plain REST, no SDK dependency
- **micro-dashboard** — single-file Flask and SQLite control panels for arbitrary pipelines
- **niche-demand-scout** — quantify demand prior to construction: score niches against live query data and derive listing copy

**→ [Get the full Operator Stack — $39](https://opforge.gumroad.com/l/operator-stack)**
· instant download · free updates · commercial license.

The four skills above are also packaged as a [downloadable archive](https://opforge.gumroad.com/l/operator-skills-free)
on a pay-what-you-want basis, $0 included — identical to this repository, with
release notifications.

## License

The four skills in this repository are MIT licensed, including for commercial use.
