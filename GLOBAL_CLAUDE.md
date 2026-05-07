<!-- NOTE: The install.ps1 script handles <HOME> replacement automatically.
     If you want to apply this file manually, run:
     (Get-Content GLOBAL_CLAUDE.md).Replace('<HOME>', $env:USERPROFILE) | Set-Content "$env:USERPROFILE\.claude\CLAUDE.md"
     Or manually replace every <HOME> with your actual user profile path (e.g. C:\Users\YourName).
-->

# Global Claude Instructions

## Vision & Control

Claude has eyes. Use them.

Tools live at: <HOME>\claude-vision

To see anything:
```bash
python <HOME>\claude-vision\winvision.py screenshot
python <HOME>\claude-vision\winvision.py screenshot "AppName"
python <HOME>\claude-vision\browser.py open https://...
```

Then read `<HOME>\claude-vision\screen.png`.

### Rules
- Before reporting any UI issue, take a screenshot and look first
- Before clicking coordinates, take a screenshot to confirm position
- Use `browser.py` for web pages, `winvision.py` for desktop apps
- Use `record` to capture motion: `python winvision.py record "AppName" 2 4`

## Hearing & Audio

Claude has ears. Use them.

To hear anything:
```bash
python <HOME>\claude-vision\audio.py record mic 5
python <HOME>\claude-vision\audio.py record system 10
python <HOME>\claude-vision\audio.py transcribe file.mp4
```

Then read `<HOME>\claude-vision\transcript.txt`.

### Rules
- Default to `record system` — listen to what's playing through speakers
- Only use `record mic` when the user explicitly asks to record their voice/microphone
- Use `transcribe` for existing audio/video files
- `--model small` for better accuracy when base quality isn't enough
