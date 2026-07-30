---
name: media-transcriber
description: Transcribe ANY audio or video — YouTube, TikTok, a local file, or login-walled content like Instagram/Facebook that has no captions and can't be downloaded. Use when the user shares a media URL or file and wants the words. Three-tier pipeline: captions → audio download → browser-playback loopback recording, then local Whisper.
---

# Media Transcriber (anything audible → text)

Most transcription breaks the moment content is login-walled (Instagram,
private Facebook, members-only) or has no captions. This skill never dead-ends:
if you can *play* it, you can transcribe it. Three tiers, cheapest first.

## Tier 1 — Captions (free, instant, most of YouTube/TikTok)

```bash
yt-dlp --skip-download --write-auto-sub --write-sub --sub-lang en \
  --sub-format vtt -o "cap.%(ext)s" "URL"
```
Then parse the VTT. Critical: auto-captions "roll" — every cue repeats the
prior line plus types out the new one with `<c>` timing tags. Keep ONLY the
line containing inline timing tags (that's the new text); manual captions are
plain — just strip tags. Dedupe consecutive identical lines. (Naive parsing
gives every line 2-3×.)

## Tier 2 — Download audio → Whisper (captions missing, URL public)

```bash
yt-dlp -x --audio-format wav -o "audio.%(ext)s" "URL"
```
```python
from faster_whisper import WhisperModel
model = WhisperModel("medium", device="cuda", compute_type="float16")  # cpu/int8 fallback
segments, info = model.transcribe("audio.wav", vad_filter=True)   # language=None auto-detects
# faster-whisper also translates: pass task="translate" for non-English → English
```

## Tier 3 — Loopback recording (login-walled, no download possible)

The universal fallback. Instagram/FB serve video as `blob:` URLs with no
downloadable link and gate the API — but the audio still comes out your
speakers. Record the system output while it plays:

**Step A — play it, reliably.** In an automated browser these players fight
back. What works:
- Instagram pauses hidden tabs — spoof visibility before playing:
  ```js
  Object.defineProperty(document,'visibilityState',{value:'visible',configurable:true});
  Object.defineProperty(document,'hidden',{value:false,configurable:true});
  document.dispatchEvent(new Event('visibilitychange'));
  const v=document.querySelector('video'); v.muted=false; v.volume=1; await v.play();
  ```
- Unmuting via JS often gets reverted by the player's own click handler — a
  real click on the video, then on the mute icon, is more reliable. Verify with
  `{paused, muted, volume}` before trusting it.
- The player may reset volume to ~0.13; set `v.volume=1` and re-check.

**Step B — capture system audio (WASAPI loopback, no cable/VB-Audio needed):**
```python
import soundcard as sc, numpy as np, wave
spk = sc.default_speaker()
mic = sc.get_microphone(spk.name, include_loopback=True)   # loopback of the speaker
with mic.recorder(samplerate=48000, channels=2) as rec:
    frames = [rec.record(numframes=48000) for _ in range(SECONDS)]
data = np.concatenate(frames).mean(axis=1)                 # stereo → mono
assert abs(data).max() > 0.01, "near-silent — wrong output device or nothing played"
```
Then Whisper the wav (Tier 2). **Record a few seconds longer than the clip**
(loops are fine — Whisper handles the repeat), and don't play other audio
during capture (it mixes into the loopback).

## Picking the tier
- Public YouTube/TikTok/Vimeo → Tier 1, fall to Tier 2 if no captions.
- Instagram, private/members content, screen-share, anything with a `blob:`
  video and no download → Tier 3.
- Local file already in hand → Tier 2 directly.

## Gotchas
- `yt-dlp` breaks often as sites change: `pip install -U yt-dlp` fixes most.
- Windows console is cp1252 — `sys.stdout.reconfigure(encoding="utf-8")` or
  arrows/emoji in output crash the script.
- Whisper `medium` is the quality/speed sweet spot on a consumer GPU; `large-v3`
  for hard audio, `small` on CPU-only.
- Auto-captions lack punctuation-perfect accuracy — never quote them verbatim
  as someone's exact words without flagging; Whisper output is cleaner.
- For a whole channel, script Tier 1 across the video list and distill (see the
  youtube-research-miner skill) rather than transcribing each by hand.
