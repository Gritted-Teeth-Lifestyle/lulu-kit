"""
audio.py — Windows audio capture + transcription tool for Claude
================================================================
Gives Claude hearing — record from mic or system audio, then transcribe.
Works alongside winvision.py and browser.py in the claude-vision toolkit.

COMMANDS:
  record [seconds]                  Record system audio / loopback (default: 10s)
  record mic [seconds]              Record from microphone (only when explicitly asked)
  record system [seconds]           Record system audio / loopback
  transcribe [file]                 Transcribe an existing audio/video file
  analyze [file]                    Analyze sound: pitch, timbre, envelope -- outputs analysis.json
                                    (also generates FM synthesis params for soundboard import)
  devices                           List available audio input/output devices

OPTIONS:
  --model base|small|medium|large   Whisper model quality (default: base)
                                    base=fast/good, small=better, medium=best

OUTPUT:
  transcript.txt   — full transcript with timestamp + source metadata
  last_recording.wav — raw audio from the most recent record command

EXAMPLES:
  python audio.py record mic 5
  python audio.py record mic 10 --model small
  python audio.py record system 30
  python audio.py transcribe my_video.mp4
  python audio.py analyze last_recording.wav
  python audio.py analyze                     -- analyzes last_recording.wav
  python audio.py devices

INSTALL (one-time):
  pip install sounddevice SoundCard openai-whisper librosa
"""

import os
import sys
import time
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPT_PATH = os.path.join(_HERE, "transcript.txt")
RECORDING_PATH  = os.path.join(_HERE, "last_recording.wav")
ANALYSIS_PATH   = os.path.join(_HERE, "analysis.json")

DEFAULT_MIC_SECONDS    = 5
DEFAULT_SYSTEM_SECONDS = 10
SAMPLE_RATE            = 16000   # Whisper native sample rate
DEFAULT_MODEL          = "base"

# ── Audio I/O ──────────────────────────────────────────────────────────────────

def _save_wav(data, samplerate):
    """Save a numpy float array as 16-bit WAV at RECORDING_PATH."""
    from scipy.io import wavfile

    if data.ndim > 1:
        data = data.mean(axis=1)          # stereo → mono
    data = data.astype(np.float32)

    peak = np.abs(data).max()
    if peak > 0:
        data = data / peak * 0.95         # normalize, leave headroom

    # scipy expects int16 or float32; float32 is fine
    wavfile.write(RECORDING_PATH, samplerate, data)
    size_kb = os.path.getsize(RECORDING_PATH) // 1024
    print(f"  Saved recording: {RECORDING_PATH}  ({size_kb} KB)")


def record_mic(seconds=DEFAULT_MIC_SECONDS, model=DEFAULT_MODEL):
    """Record from the default microphone input."""
    try:
        import sounddevice as sd
    except ImportError:
        _die_install("sounddevice", "pip install sounddevice")

    device_info = sd.query_devices(kind='input')
    print(f"Recording {seconds}s from mic: {device_info['name']}")
    print("  Listening now — speak clearly ...")

    data = sd.rec(
        int(seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32',
        blocking=True,
    )
    print(f"  Done.  {len(data)} samples @ {SAMPLE_RATE} Hz")

    _save_wav(data.flatten(), SAMPLE_RATE)
    return _transcribe_and_save(RECORDING_PATH, model, source="mic", seconds=seconds)


def record_system(seconds=DEFAULT_SYSTEM_SECONDS, model=DEFAULT_MODEL):
    """
    Record system audio via WASAPI loopback — captures whatever is playing
    through the default speaker (games, video, music, calls, etc.).
    """
    try:
        import soundcard as sc
    except ImportError:
        _die_install("SoundCard", "pip install SoundCard")

    speaker = sc.default_speaker()
    print(f"Recording {seconds}s of system audio from: {speaker.name}")
    print("  Capturing loopback — play something now ...")

    try:
        with sc.get_microphone(id=str(speaker.name), include_loopback=True) as loopback:
            data = loopback.record(samplerate=SAMPLE_RATE, numframes=int(SAMPLE_RATE * seconds))
    except Exception as e:
        print(f"ERROR: Loopback capture failed: {e}")
        print("  Make sure your audio driver supports WASAPI loopback.")
        print("  Try: python audio.py devices  to see available devices.")
        sys.exit(1)

    print(f"  Done.  shape={data.shape}")
    _save_wav(data, SAMPLE_RATE)
    return _transcribe_and_save(RECORDING_PATH, model, source="system", seconds=seconds)


# ── Transcription ──────────────────────────────────────────────────────────────

def _load_whisper(model_name):
    """Import and load whisper model, with friendly install hint."""
    try:
        import whisper
    except ImportError:
        _die_install("openai-whisper", "pip install openai-whisper")
    print(f"Loading Whisper '{model_name}' model (first run downloads ~{_model_size(model_name)}) ...")
    return whisper.load_model(model_name)


def _model_size(name):
    sizes = {"tiny": "75 MB", "base": "145 MB", "small": "460 MB",
             "medium": "1.5 GB", "large": "3 GB"}
    return sizes.get(name, "unknown size")


def transcribe_file(filepath, model=DEFAULT_MODEL):
    """Transcribe an existing audio or video file."""
    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)
    return _transcribe_and_save(filepath, model, source=filepath)


def _transcribe_and_save(wav_path, model_name, source="", seconds=None):
    """Run Whisper on wav_path, write transcript.txt, print result."""
    m = _load_whisper(model_name)
    print(f"Transcribing {os.path.basename(wav_path)} ...")
    result = m.transcribe(wav_path, fp16=False)
    text = result["text"].strip()

    _write_transcript(text, source=source, seconds=seconds)
    return text


def _write_transcript(text, source="", seconds=None):
    """Save transcript to transcript.txt with metadata header."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    meta_parts = [f"[{timestamp}]"]
    if source:
        meta_parts.append(f"source={source}")
    if seconds is not None:
        meta_parts.append(f"duration={seconds}s")
    header = "  ".join(meta_parts)

    content = f"{header}\n{text}\n"
    with open(TRANSCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    bar = "-" * 48
    print(f"\nTranscript:\n{bar}\n{text}\n{bar}")
    print(f"Saved: {TRANSCRIPT_PATH}")


# ── Sound Analysis ────────────────────────────────────────────────────────────

def analyze(filepath=None):
    """
    Analyze a sound file: extract pitch, timbre, envelope, spectral character.
    Outputs analysis.json with FM synthesis params the soundboard can import.
    Defaults to last_recording.wav if no file given.
    """
    import json

    try:
        import librosa
        import librosa.effects
    except ImportError:
        _die_install("librosa", "pip install librosa")

    filepath = filepath or RECORDING_PATH
    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        print(f"  Record something first: python audio.py record system 10")
        sys.exit(1)

    print(f"Analyzing: {os.path.basename(filepath)} ...")

    y, sr = librosa.load(filepath, sr=None, mono=True)
    duration = float(librosa.get_duration(y=y, sr=sr))

    # ── Pitch (fundamental frequency) ─────────────────────────────────────────
    segment = y[:int(sr * min(4.0, duration))]
    try:
        f0, voiced_flag, _ = librosa.pyin(
            segment,
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7'),
            sr=sr
        )
        voiced_f0 = f0[voiced_flag & ~np.isnan(f0)] if f0 is not None else np.array([])
        fundamental = float(np.median(voiced_f0)) if len(voiced_f0) > 3 else 0.0
    except Exception:
        fundamental = 0.0

    # ── Spectral features ──────────────────────────────────────────────────────
    centroid   = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
    flatness   = float(np.mean(librosa.feature.spectral_flatness(y=y)))
    zcr        = float(np.mean(librosa.feature.zero_crossing_rate(y)))
    rms_frames = librosa.feature.rms(y=y, hop_length=512)[0]
    rms_mean   = float(np.mean(rms_frames))

    # ── Envelope ──────────────────────────────────────────────────────────────
    peak_frame = int(np.argmax(rms_frames))
    attack_ms  = peak_frame * 512 / sr * 1000
    peak_val   = rms_frames[peak_frame]
    tail       = rms_frames[peak_frame:]
    decay_idx  = np.where(tail < peak_val * 0.1)[0]
    decay_ms   = float(decay_idx[0] * 512 / sr * 1000) if len(decay_idx) > 0 else duration * 1000

    # ── Harmonic vs percussive ─────────────────────────────────────────────────
    y_harm, y_perc = librosa.effects.hpss(y)
    h_e  = float(np.mean(y_harm ** 2))
    p_e  = float(np.mean(y_perc ** 2))
    harmonic_ratio = h_e / (h_e + p_e + 1e-10)

    # ── Sound type ────────────────────────────────────────────────────────────
    if harmonic_ratio > 0.7 and fundamental > 20:
        sound_type = "tonal"
    elif harmonic_ratio > 0.4:
        sound_type = "mixed"
    elif zcr > 0.15:
        sound_type = "noisy"
    else:
        sound_type = "percussive"

    # ── Note name ─────────────────────────────────────────────────────────────
    note_name = ""
    if fundamental > 20:
        midi = 12 * np.log2(fundamental / 440.0) + 69
        names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        note_name = f"{names[int(round(midi)) % 12]}{int(round(midi)) // 12 - 1}"

    # ── FM synthesis approximation ────────────────────────────────────────────
    carrier_hz = fundamental if fundamental > 20 else centroid
    if harmonic_ratio > 0.7:
        mod_ratio = 1.0
    elif harmonic_ratio > 0.4:
        mod_ratio = 1.8
    else:
        mod_ratio = 3.14
    mod_freq  = carrier_hz * mod_ratio
    mod_depth = int(max(80, min(1400, centroid / max(carrier_hz, 1) * 300)))
    vol       = round(min(0.85, rms_mean * 12), 2)
    sb_dur    = round(min(2.0, duration), 3)
    attack_s  = round(min(0.12, attack_ms / 1000), 4)
    release_s = round(min(0.6,  decay_ms  / 1000), 4)

    analysis = {
        "source_file":        os.path.basename(filepath),
        "duration_s":         round(duration, 3),
        "fundamental_hz":     round(fundamental, 2),
        "note":               note_name,
        "spectral_centroid_hz": round(centroid, 1),
        "spectral_flatness":  round(flatness, 5),
        "zero_crossing_rate": round(zcr, 5),
        "rms":                round(rms_mean, 5),
        "attack_ms":          round(attack_ms, 1),
        "decay_ms":           round(min(decay_ms, duration * 1000), 1),
        "harmonic_ratio":     round(harmonic_ratio, 3),
        "sound_type":         sound_type,
        "fm_params": {
            "carrier_hz":  round(carrier_hz, 1),
            "mod_ratio":   round(mod_ratio, 2),
            "mod_freq":    round(mod_freq, 1),
            "mod_depth":   mod_depth,
            "duration":    sb_dur,
            "attack_s":    attack_s,
            "release_s":   release_s,
            "vol":         vol,
        }
    }

    with open(ANALYSIS_PATH, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2)

    bar = "-" * 48
    print(f"\n{bar}")
    print(f"  File:      {os.path.basename(filepath)}")
    print(f"  Type:      {sound_type}")
    print(f"  Pitch:     {fundamental:.1f} Hz  ({note_name or 'unpitched'})")
    print(f"  Brightness:{centroid:.0f} Hz  (spectral centroid)")
    print(f"  Harmonic:  {harmonic_ratio:.0%}")
    print(f"  Attack:    {attack_ms:.1f} ms")
    print(f"  Decay:     {min(decay_ms, duration*1000):.1f} ms")
    print(f"")
    print(f"  FM Params → soundboard:")
    print(f"    carrier={carrier_hz:.0f}Hz  mod_ratio={mod_ratio:.2f}")
    print(f"    mod_depth={mod_depth}  dur={sb_dur}s  vol={vol}")
    print(f"{bar}")
    print(f"\nSaved: {ANALYSIS_PATH}")
    print(f"Import this into the soundboard with File → Import Analysis JSON")

    return analysis


# ── Device listing ─────────────────────────────────────────────────────────────

def list_devices():
    """Print available input devices (mic) and loopback devices (system)."""
    # --- sounddevice inputs ---
    try:
        import sounddevice as sd
        print("=== Microphone / Input devices (sounddevice) ===")
        default_in = sd.default.device[0]
        for i, d in enumerate(sd.query_devices()):
            if d['max_input_channels'] > 0:
                tag = "  <-- default" if i == default_in else ""
                print(f"  [{i:2d}] {d['name']}  ({d['max_input_channels']}ch){tag}")
    except ImportError:
        print("  sounddevice not installed — pip install sounddevice")

    # --- soundcard loopback ---
    try:
        import soundcard as sc
        print("\n=== System audio / Loopback devices (SoundCard) ===")
        default_spk = sc.default_speaker()
        for spk in sc.all_speakers():
            tag = "  <-- default (used by 'record system')" if spk.name == default_spk.name else ""
            print(f"  {spk.name}{tag}")
    except ImportError:
        print("\n  SoundCard not installed — pip install SoundCard")


# ── Helpers ────────────────────────────────────────────────────────────────────

def _is_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def _die_install(package, command):
    print(f"ERROR: {package} not installed.")
    print(f"  Run: {command}")
    sys.exit(1)


def _parse_model(args):
    """Pull --model <name> from args list, return (remaining_args, model_name)."""
    model = DEFAULT_MODEL
    clean = []
    i = 0
    while i < len(args):
        if args[i] == "--model" and i + 1 < len(args):
            model = args[i + 1]
            i += 2
        else:
            clean.append(args[i])
            i += 1
    return clean, model


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()
    rest, model = _parse_model(sys.argv[2:])

    if cmd == "record":
        # Default to system audio — mic only when explicitly requested
        source = rest[0].lower() if rest else "system"
        seconds_arg = rest[1] if len(rest) > 1 else (rest[0] if rest and _is_number(rest[0]) else None)

        if source == "mic":
            secs = float(rest[1]) if len(rest) > 1 else DEFAULT_MIC_SECONDS
            record_mic(seconds=secs, model=model)
        elif source in ("system", "sys", "loopback"):
            secs = float(rest[1]) if len(rest) > 1 else DEFAULT_SYSTEM_SECONDS
            record_system(seconds=secs, model=model)
        elif _is_number(source):
            # e.g. `audio.py record 30` — plain seconds, default to system
            record_system(seconds=float(source), model=model)
        else:
            print(f"Unknown source '{source}'. Use 'mic' or 'system'.")
            sys.exit(1)

    elif cmd == "transcribe":
        if not rest:
            print("Usage: audio.py transcribe <file>")
            sys.exit(1)
        transcribe_file(rest[0], model=model)

    elif cmd == "analyze":
        filepath = rest[0] if rest else None
        analyze(filepath)

    elif cmd == "devices":
        list_devices()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
