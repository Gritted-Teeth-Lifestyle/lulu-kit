# Video Translator Skill

Operational guide for the video translation + subtitle burning web app.

## Project Location
`C:\Users\Pinko\claudesandbox\video-translator\`

## Live URL
`https://video-translator-production-8218.up.railway.app`

## Railway IDs
| Field | Value |
|---|---|
| Project | `490faaad-d074-4f0a-a50e-e30248d486a4` |
| Service | `b241ffa2-7524-4446-8e64-ef9919f9b28a` |
| Environment | `56890ce6-34fb-4430-ac93-e463e471b058` |
| API Token | from `C:\Users\Pinko\.railway\config.json` → `user.accessToken` |

## Architecture
```
main.py       — FastAPI routes: POST /translate, GET /status/{id}, GET /download/{id}, GET /srt/{id}
processor.py  — Background thread: whisper transcription → Google translate → ffmpeg drawtext burn
index.html    — P5 UI: URL/Upload tabs, language selectors, progress bar, download button
Dockerfile    — python:3.11-slim + ffmpeg + fonts-dejavu-core
requirements.txt — fastapi uvicorn[standard] faster-whisper deep-translator yt-dlp python-multipart imageio-ffmpeg
```

## Key Technical Rules
1. **Subtitle burning = drawtext filter** — Never use `subtitles` (libass) filter; use `drawtext` with explicit fontfile path
2. **Font path on Linux**: `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` (installed via fonts-dejavu-core)
3. **RAM limit**: Railway free tier = 512MB. Keep faster-whisper at `tiny` int8 model. Always `del model; gc.collect()` after transcription
4. **Whisper translate**: For English target, use `task="translate"` — don't run Google Translate on top
5. **Special char escaping** in drawtext text: replace `\` → `\\`, `'` → `'` (curly), `:` → `\:`, `%` → `\%`

## Triggering a Railway Redeploy via API
```python
import requests
token = open(r'C:\Users\Pinko\.railway\config.json').read()
# parse JSON and get user.accessToken
# Then:
mutation = 'mutation { serviceInstanceRedeploy(serviceId: "b241ffa2-...", environmentId: "56890ce6-...") }'
requests.post('https://backboard.railway.app/graphql/v2',
    headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'},
    json={'query': mutation})
```

## Switching to Dockerfile Mode
Railway defaults to Railpack and silently ignores the Dockerfile. Fix:
```python
mutation = '''mutation { serviceInstanceUpdate(serviceId: "...", environmentId: "...", input: { dockerfilePath: "Dockerfile" }) }'''
```
Then trigger redeploy.

## Verifying a New Build is Live
Check for a route that only exists in the new code:
```python
requests.get('https://video-translator-production-8218.up.railway.app/srt/test').json()
# Old build: {"detail":"Not Found"}
# New build: {"error":"SRT not found"}
```

## Test Script
`python test_clean.py` — uploads solid-blue video with Spanish audio, polls status, downloads output, extracts frame to `C:\Users\Pinko\claude-vision\clean_frame.png`

## GitHub Repo
`kamipinko/video-translator` — push to master triggers Railway redeploy (once Dockerfile mode is configured)
