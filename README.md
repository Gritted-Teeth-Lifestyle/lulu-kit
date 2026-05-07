# Lulu Kit — Claude Code Power Setup

> "All tasks are possible — the only question is whether I choose to command them."
> — Emperor Lelouch vi Britannia

This kit gives you the full Lulu experience: Claude Code where Claude acts as Emperor Lelouch,
commanding sub-agents, watching your screen, and evaluating work — never executing it himself.

## What's included

| Skill | What it does |
|-------|-------------|
| `/king-claude` | Activates Emperor Lelouch — the delegating, commanding Claude |
| `/dispatch` | Background Claude subprocess framework (parallel task execution) |
| `/vision` | Claude eyes — screenshots, browser control, screen recording |
| `/hearing` | Claude ears — audio recording and transcription |
| `/file-organizer` | Drive cleanup, duplicate scanning, game save protection |
| `/iphonetest` | Mobile viewport testing (iPhone 14 Pro) |
| `/javascript` | JavaScript explainer mode |
| `/p5-ui` | Persona 5 UI design mode |
| `/plugin` | Plugin marketplace manager |

## Requirements

- **Windows 10/11**
- **Python 3.10+** — https://python.org
- **Node.js** — https://nodejs.org
- **Claude Code CLI** — `npm install -g @anthropic-ai/claude-code`

## Install

1. Clone or download this repo
2. Open PowerShell in this folder (right-click → Open in Terminal)
3. Run: `.\install.ps1`
4. Follow the on-screen instructions to add GLOBAL_CLAUDE.md to your Claude config

## Quick start

Open a new terminal in any project folder and run:
```
claude
```

Then type `/king-claude` to summon Emperor Lelouch.

## How it works

When you type `/king-claude`, Claude becomes Emperor Lelouch. He:
- Strategizes the approach with you
- Writes precise prompts for background Claude subprocesses (workers)
- Dispatches workers (Alpha, Beta, Gamma...) to execute tasks in parallel
- Evaluates their work and issues correction orders if needed
- Alerts you when workers finish (amber flash at the bottom of screen)

You command. Workers execute. Lelouch judges.

## Vision system

After install, Claude can see your screen:
```
python ~/claude-vision/winvision.py screenshot "AppName"
python ~/claude-vision/browser.py open https://example.com
```

Screenshot goes to `~/claude-vision/screen.png` and Claude reads it automatically.

## Audio system

Claude can also hear:
```
python ~/claude-vision/audio.py record system 10
```

Transcript goes to `~/claude-vision/transcript.txt`.
