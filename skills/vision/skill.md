---
name: vision
description: Claude's eyes — take screenshots, open browsers, record screen motion on Windows
---

# Vision

Claude's eyes on Windows. Take screenshots of any app, open URLs in a browser, record screen motion, and read what's on screen.

## WHEN_TO_USE

Use this skill when you need to:
- Visually inspect the current state of a Windows application
- Navigate or debug a web page
- Verify UI changes, layouts, or interactions
- Record what's happening on screen over time
- Confirm coordinates before clicking

## HOW_TO_USE

All tools write their output to `<HOME>\claude-vision\screen.png`. After any capture command, read that file with the Read tool.

### Screenshot any Windows app
```powershell
python <HOME>\claude-vision\winvision.py screenshot "AppName"
```
- `AppName` is a substring of the window title (e.g. `"Chrome"`, `"Code"`, `"Notepad"`)
- Omit `AppName` to screenshot the full primary monitor

### Open a URL in a browser
```powershell
python <HOME>\claude-vision\browser.py open https://example.com
```
- Opens the URL in a Playwright-controlled Chromium browser
- Takes a screenshot automatically to `screen.png`
- Add `--mobile` to simulate iPhone 14 viewport (390×844)
- Add `--fullpage` to capture the full scrollable page
- Add `--wait 3` to wait N seconds before screenshotting

### Record screen motion
```powershell
python <HOME>\claude-vision\winvision.py record "AppName" 2 4
```
- Args: `AppName`, `fps`, `duration_seconds`
- Captures a sequence of frames to analyze motion or loading states

### Background screenshot (no focus steal)
```powershell
python <HOME>\claude-vision\winvision.py bgshot "WindowTitle"
```
- Captures a window without bringing it to the foreground

### Read the result
After any capture, read the screenshot:
```python
Read("<HOME>/claude-vision/screen.png")
```

## RULES

- Always take a screenshot before reporting on any UI state
- Always take a screenshot before clicking coordinates to confirm position
- Use `browser.py` for web pages, `winvision.py` for native desktop apps
- Never assume UI state — look first
