# Claude Hearing — audio.py Toolkit

Claude has ears. `audio.py` lives at `<HOME>\claude-vision\audio.py` alongside the vision tools.

## Quick reference

```bash
# Listen to what's playing through speakers (DEFAULT)
python <HOME>\claude-vision\audio.py record system 10

# Record from microphone (only when user explicitly asks)
python <HOME>\claude-vision\audio.py record mic 5

# Shorthand — no source specified → system loopback
python <HOME>\claude-vision\audio.py record 30

# Transcribe an existing audio/video file
python <HOME>\claude-vision\audio.py transcribe file.mp4

# Analyze sound and extract FM synthesis parameters
python <HOME>\claude-vision\audio.py analyze

# Higher quality transcription
python <HOME>\claude-vision\audio.py record system 10 --model small

# List all available audio devices
python <HOME>\claude-vision\audio.py devices
```

## Output files (always in `<HOME>\claude-vision\`)

| File | Contents |
|------|----------|
| `transcript.txt` | Speech transcription with timestamp + source metadata |
| `last_recording.wav` | Raw audio (16kHz mono) |
| `analysis.json` | Pitch, spectral features, envelope, sound type, FM params |

## Behavioral rules

- **Always default to system loopback** — `record system` unless mic is explicitly requested
- After recording, read `transcript.txt` for speech; read `analysis.json` for sound analysis
- Use `--model small` when transcription quality matters (slower but more accurate)
- `analyze` runs on `last_recording.wav` — record first, then analyze

## analyze command — FM synthesis output

`analysis.json` includes an `fm_params` block for importing into a soundboard:

```json
{
  "sound_type": "tonal|mixed|noisy|percussive",
  "pitch_hz": 440.0,
  "note_name": "A4",
  "brightness": 1200.0,
  "fm_params": {
    "carrier_hz": 440.0,
    "mod_ratio": 2.0,
    "mod_depth": 150.0,
    "duration": 1.0,
    "vol": 0.5
  }
}
```

## Dependencies

```bash
pip install sounddevice SoundCard openai-whisper librosa numpy scipy
```
