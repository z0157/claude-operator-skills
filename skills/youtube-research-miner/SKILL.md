---
name: youtube-research-miner
description: Transcribe and mine YouTube videos or entire channels without the YouTube API. Use when the user wants a video transcribed, a channel's content analyzed, quotes/claims extracted, or dozens of transcripts distilled into findings. Works with yt-dlp captions — no API keys, no Whisper needed when captions exist.
---

# YouTube Research Miner

Turn any YouTube video or channel into clean, searchable research material. The
core insight: **YouTube already generates caption tracks for almost everything** —
so transcription is a fetch-and-parse problem, not a speech-to-text problem.
A 100-video channel can be fully mined in minutes for $0.

## When to reach for this
- "Transcribe this video" / "what does this video say?"
- "Analyze every video on this channel and find X"
- Extracting claims, numbers, tools, or quotes from talking-head content
- Building a corpus from a creator's catalog for comparison or synthesis

## Step 1 — Metadata first (cheap, instant)

```bash
yt-dlp --skip-download --print "%(title)s ||| %(uploader)s ||| %(duration_string)s ||| %(view_count)s views" "URL"
```

For a channel, list videos without downloading anything:

```bash
yt-dlp --flat-playlist --print "%(id)s ||| %(duration_string)s ||| %(title)s" \
  "https://www.youtube.com/@CHANNEL/videos" --playlist-end 100 > videolist.txt
```

## Step 2 — Pull captions (not video)

```bash
yt-dlp --skip-download --write-auto-sub --write-sub --sub-lang en --sub-format vtt \
  -o "subs/%(id)s.%(ext)s" "URL"
```

- `--skip-download` = only the ~50-500KB caption file, never the video.
- Request **both** `--write-sub` (manual captions, cleaner) and `--write-auto-sub`.
- Bulk channel pull: add `--ignore-errors --playlist-end 100` and point at the
  channel /videos URL. Expect a few videos to have no captions — skip them.

## Step 3 — Parse the VTT correctly (the part everyone gets wrong)

There are TWO caption formats and they need different parsing:

**Auto-generated captions are "rolling"**: every cue repeats the previous line
plus types out the new one with inline timing tags. Naive parsing gives you
every line 2-3x. The fix: keep ONLY the line inside each cue that contains
inline `<c>` timing tags — that's the genuinely new text.

**Manual captions** are plain cues — just strip tags and join.

```python
import re, html

def parse_vtt(path):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    is_auto = "<c>" in raw          # rolling auto-subs marker
    out = []
    for block in raw.split("\n\n"):
        if "-->" not in block:
            continue
        m = re.search(r"(\d\d):(\d\d):(\d\d)\.\d\d\d --> ", block)
        if not m:
            continue
        ts = f"{int(m.group(1))*60+int(m.group(2)):02d}:{m.group(3)}"  # mm:ss
        if is_auto:
            line = next((l for l in block.split("\n")
                         if "<c>" in l or re.search(r"<\d\d:\d\d:\d\d", l)), None)
            if line is None:
                continue
            text = line
        else:
            text = " ".join(l for l in block.split("\n")[1:] if "-->" not in l)
        text = re.sub(r"<[^>]+>", "", text)
        text = html.unescape(text).replace("\xa0", " ")
        text = re.sub(r"\s+", " ", text).strip()
        if text and (not out or out[-1][1] != text):   # drop consecutive dupes
            out.append((ts, text))
    return out
```

Sanity checks after parsing: word count should be roughly 130-160 words per
minute of runtime. If it's ~2x that, you parsed rolling captions naively.

## Step 4 — Present it usefully

For a single video, group lines into ~30-second timestamped paragraphs — far
more readable than caption-line fragments:

```python
def paragraphs(lines, gap=30):
    secs = lambda ts: int(ts[:2])*60 + int(ts[3:])
    paras, cur, anchor, last = [], [], None, -999
    for ts, t in lines:
        if anchor is None:
            anchor, last = ts, secs(ts)
        cur.append(t)
        if secs(ts) - last >= gap:
            paras.append((anchor, " ".join(cur))); cur, anchor = [], None
    if cur: paras.append((anchor or lines[0][0], " ".join(cur)))
    return paras
```

## Step 5 — Mine at channel scale

For N videos, don't read every transcript top to bottom. Distill first:

1. Parse all VTTs to flat text.
2. Regex-tag each transcript for what you're hunting: money figures
   (`\$[\d,]+`), tool names, claims, topic keywords.
3. Score/rank videos by signal density, then deep-read only the top hits.
4. For deep reads, pull **keyword-context windows** instead of full text:

```python
def context(text, term, win=200, max_hits=4):
    hits, low = [], text.lower()
    for m in re.finditer(re.escape(term.lower()), low):
        s = text[max(0, m.start()-win): m.start()+win].strip()
        if not any(s[:60] in h for h in hits):
            hits.append(s)
        if len(hits) >= max_hits: break
    return hits
```

This "distill → rank → context-window" pattern keeps a 100-video analysis
inside a single context window.

## Gotchas
- No captions at all → fall back to `yt-dlp -x --audio-format mp3` + Whisper.
- yt-dlp warns when >90 days old and YouTube breaks it regularly: `pip install -U yt-dlp` fixes most extraction failures.
- Auto-captions lack punctuation-perfect accuracy; never quote them as verbatim without flagging.
- Sponsor segments and self-promo read like content — check mid-video claims against who benefits.
