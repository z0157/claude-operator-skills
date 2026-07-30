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
| **[media-transcriber](skills/media-transcriber/SKILL.md)** | Transcribe **anything audible** — YouTube, TikTok, local files, or login-walled Instagram/FB with no captions. 3-tier pipeline (captions → audio download → browser-playback loopback recording) + local Whisper. Ships a runnable `transcribe.py`. |
| **[youtube-research-miner](skills/youtube-research-miner/SKILL.md)** | Transcribe & mine any YouTube video or entire channel — no API. Correct VTT dedupe (the part everyone gets wrong), channel-scale distillation, claim extraction. |
| **[local-lead-finder](skills/local-lead-finder/SKILL.md)** | Find businesses with **no website** in any city, free (OpenStreetMap). Opportunity scoring, chain/franchise filtering, phone/address enrichment. |
| **[govcon-scout](skills/govcon-scout/SKILL.md)** | Research what the U.S. government buys and who wins — real award data by category/size/state (USAspending, no key) + live bid opportunities (SAM.gov). |

<a name="install"></a>

## Install

**As a plugin (recommended)** — inside Claude Code:

```
/plugin marketplace add z0157/claude-operator-skills
/plugin install operator-skills@opforge
```

That's it. You get all four skills, and `/plugin update` pulls new ones as
they land.

**Or copy the files manually**, if you'd rather not add a marketplace:

```bash
git clone https://github.com/z0157/claude-operator-skills
cp -r claude-operator-skills/skills/* ~/.claude/skills/   # all projects
```

Either way, just ask Claude Code naturally — "find businesses without websites
in Boise", "transcribe this channel and find every revenue claim" — and it
loads the right skill on its own.

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

- **client-site-builder** — polished single-file websites for local businesses (themed by industry, schema.org, mobile-verified)
- **cold-outreach-drafter** — "I already built you something" outreach with CAN-SPAM/TCPA rails baked in
- **pdf-product-factory** — sellable PDF products (forms, bundles, workbooks) from HTML/CSS at catalog scale
- **spreadsheet-tool-builder** — Excel calculators with verified formulas (the anti-slop moat)
- **stripe-no-sdk** — payments, subscriptions & payment links in plain REST
- **micro-dashboard** — one-file Flask + SQLite control panels for any pipeline
- **niche-demand-scout** — validate demand *before* building; score niches, write listing copy

**→ [Get the full Operator Stack — $34](https://opforge.gumroad.com/l/operator-stack)**
· instant download · free updates · commercial license.

Prefer to try first? **[Grab these 4 free skills as a zip](https://opforge.gumroad.com/l/operator-skills-free)**
(pay what you want, $0 works) — same files as this repo, and you'll hear about
new skills when they land.

## License

Free skills: MIT — use them anywhere, including commercially.
