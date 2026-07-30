#!/usr/bin/env python3
"""transcribe.py — one command to transcribe any media URL or file.

Usage:
  python transcribe.py <url>              # YouTube/TikTok/etc: captions if they
                                          # exist, else download audio + Whisper
  python transcribe.py <file.mp4|.wav>    # local file -> Whisper
  python transcribe.py --record 60        # record system audio (loopback) for N
                                          # seconds (play the media now!) -> Whisper
Options:
  --lang en        force language (default: auto-detect)
  --model medium   whisper model (tiny/base/small/medium/large-v3)

Output: <name>_transcript.txt (timestamped) + summary line. Prints transcript.

Pipeline logic:
 1. URL with captions  -> yt-dlp caption pull + VTT dedupe (fast, free)
 2. URL without        -> yt-dlp audio download -> faster-whisper (GPU if avail)
 3. Login-walled (IG)  -> --record: play it in your browser, loopback-record
                          system output, then Whisper. Works for ANYTHING audible.
"""
import argparse, html, os, re, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows cp1252 console


# ---------- VTT parsing (handles rolling auto-subs AND manual captions) ----------
def parse_vtt(path):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    is_auto = "<c>" in raw
    out = []
    for block in raw.split("\n\n"):
        if "-->" not in block:
            continue
        m = re.search(r"(\d\d):(\d\d):(\d\d)\.\d\d\d --> ", block)
        if not m:
            continue
        ts = f"{int(m.group(1))*60+int(m.group(2)):02d}:{m.group(3)}"
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
        if text and (not out or out[-1][1] != text):
            out.append((ts, text))
    return out


def try_captions(url, workdir):
    """Attempt caption download; return transcript lines or None."""
    out = Path(workdir) / "cap"
    r = subprocess.run(
        ["yt-dlp", "--skip-download", "--write-auto-sub", "--write-sub",
         "--sub-lang", "en", "--sub-format", "vtt", "--no-warnings",
         "-o", f"{out}.%(ext)s", url],
        capture_output=True, text=True, timeout=180)
    vtts = list(Path(workdir).glob("cap*.vtt"))
    if not vtts:
        return None
    lines = parse_vtt(vtts[0])
    return lines or None


def download_audio(url, workdir):
    """Download best audio; return path or None."""
    out = Path(workdir) / "audio.%(ext)s"
    r = subprocess.run(
        ["yt-dlp", "-x", "--audio-format", "wav", "--no-warnings",
         "-o", str(out), url],
        capture_output=True, text=True, timeout=600)
    wavs = list(Path(workdir).glob("audio*.wav"))
    return str(wavs[0]) if wavs else None


def record_loopback(seconds):
    """Record system audio output (WASAPI loopback). Returns wav path."""
    import numpy as np
    import soundcard as sc
    import wave
    SR = 48000
    spk = sc.default_speaker()
    mic = sc.get_microphone(spk.name, include_loopback=True)
    print(f"● recording system output ({spk.name}) for {seconds}s — play it now!",
          flush=True)
    frames = []
    with mic.recorder(samplerate=SR, channels=2) as rec:
        for _ in range(seconds):
            frames.append(rec.record(numframes=SR))
    data = np.concatenate(frames).mean(axis=1)
    peak = float(abs(data).max())
    pcm = (data.clip(-1, 1) * 32767).astype("int16")
    path = "recording.wav"
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"  saved ({'audio ok' if peak > 0.01 else 'WARNING: near-silent'} — peak {peak:.3f})")
    return path


def whisper_transcribe(wav, model_size, lang):
    from faster_whisper import WhisperModel
    try:
        model = WhisperModel(model_size, device="cuda", compute_type="float16")
    except Exception:
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(wav, vad_filter=True, language=lang)
    lines = [(f"{int(s.start//60):02d}:{int(s.start%60):02d}", s.text.strip())
             for s in segments]
    return lines, info.language


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="URL or media file")
    ap.add_argument("--record", type=int, metavar="SECONDS",
                    help="record system audio instead (play the media while it runs)")
    ap.add_argument("--lang", default=None)
    ap.add_argument("--model", default="medium")
    a = ap.parse_args()

    name, lines, detected = "transcript", None, ""

    if a.record:
        wav = record_loopback(a.record)
        lines, detected = whisper_transcribe(wav, a.model, a.lang)
        name = "recording"
    elif a.target and os.path.exists(a.target):
        lines, detected = whisper_transcribe(a.target, a.model, a.lang)
        name = Path(a.target).stem
    elif a.target:
        with tempfile.TemporaryDirectory() as td:
            print("→ trying captions (fast, free)...")
            lines = try_captions(a.target, td)
            if lines:
                print("  captions found.")
            else:
                print("→ no captions; downloading audio for Whisper...")
                wav = download_audio(a.target, td)
                if wav:
                    lines, detected = whisper_transcribe(wav, a.model, a.lang)
                else:
                    sys.exit(
                        "Could not download (login-walled?).\n"
                        "Fallback: open it in your browser, then run:\n"
                        "  python transcribe.py --record 70\n"
                        "and press play.")
            m = re.search(r"[?&]v=([\w-]+)|/([A-Za-z0-9_-]{8,})/?$", a.target)
            name = next((g for g in (m.groups() if m else []) if g), "transcript")
    else:
        ap.print_help(); sys.exit(1)

    out = Path(f"{name}_transcript.txt")
    text = "\n".join(f"[{ts}] {t}" for ts, t in lines)
    out.write_text(text, encoding="utf-8")
    words = sum(len(t.split()) for _, t in lines)
    print(f"\n{'='*60}\n{out}  ({len(lines)} lines, {words} words"
          + (f", lang={detected}" if detected else "") + f")\n{'='*60}")
    print(text[:3000] + ("\n... [truncated — see file]" if len(text) > 3000 else ""))


if __name__ == "__main__":
    main()
