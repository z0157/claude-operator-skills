<p align="center">
  <img src=".github/assets/logo.jpg" alt="Operator Skills" width="140">
</p>

<h1 align="center">Operator Skills</h1>

<p align="center">
  Claude Code skills for building things that make money.<br>
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


Four free, production-grade skills for [Claude Code](https://claude.com/claude-code) —
distilled from real working pipelines, not voice-dumped guesses. Every pattern in
these files has actually run: the lead finder has pulled 300+ real businesses per
city, the research miner has processed 100-video channels, the govcon scout has
queried real federal award data.

## The skills

| Skill | What Claude learns to do |
|---|---|
| **[media-transcriber](skills/media-transcriber/SKILL.md)** | Transcribe **anything audible** — YouTube, TikTok, local files, or login-walled Instagram/FB with no captions. 3-tier pipeline (captions → audio download → browser-playback loopback recording) + local Whisper. Ships a runnable `transcribe.py`. |
| **[youtube-research-miner](skills/youtube-research-miner/SKILL.md)** | Transcribe & mine any YouTube video or entire channel — no API. Correct VTT dedupe (the part everyone gets wrong), channel-scale distillation, claim extraction. |
| **[local-lead-finder](skills/local-lead-finder/SKILL.md)** | Find businesses with **no website** in any city, free (OpenStreetMap). Opportunity scoring, chain/franchise filtering, phone/address enrichment. |
| **[govcon-scout](skills/govcon-scout/SKILL.md)** | Research what the U.S. government buys and who wins — real award data by category/size/state (USAspending, no key) + live bid opportunities (SAM.gov). |

<a name="install"></a>

## Install

Drop any skill folder into your skills directory:

```bash
# personal (all projects)
git clone https://github.com/z0157/claude-operator-skills
cp -r claude-operator-skills/skills/* ~/.claude/skills/

# or per-project
cp -r claude-operator-skills/skills/* .claude/skills/
```

Then just ask Claude Code naturally — "find businesses without websites in
Boise", "transcribe this channel and find every revenue claim" — and it uses
the skill.

## Why these are different

Most skills for sale are prompts wearing a trench coat. These encode the
**gotchas that cost hours**: why auto-caption VTTs duplicate every line and the
exact dedupe that fixes it; why OSM "no website" false-positives on franchises
and the denylist that filters them; why SAM.gov's DEMO_KEY 404s and what
actually works. That's the difference between a skill that demos well and one
that ships.

## The full Operator Stack (11 skills)

The paid stack adds the **build-and-sell layer** — the skills that turn leads
and research into products and revenue:

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
