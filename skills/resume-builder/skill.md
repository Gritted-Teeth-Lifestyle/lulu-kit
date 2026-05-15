---
name: resume-builder
description: Manage, fix, and deploy the Proles Consulting Resume Builder on Railway. Use when updating the resume base data, fixing generation, adding features, or deploying changes.
---

# Resume Builder — Proles Consulting

Express.js app that generates tailored PM resumes and cover letters using Claude API, with LinkedIn Easy Apply automation.

**Live URL:** https://www.prolesconsulting.com/resume
**Local:** C:\Users\Pinko\claudesandbox\proles-consulting\
**GitHub:** proles-consulting repo
**Key files:** server.js, resume.html

## Stack
- Express.js server with Anthropic SDK
- Playwright (stealth plugin) for scraping + LinkedIn automation
- P5 UI (Bebas Neue + Space Mono, gold/crimson/black)

## API Routes
- `POST /api/resume/scrape` — axios first, Playwright stealth fallback for Cloudflare-protected boards
- `POST /api/resume/generate` — calls claude-opus-4-7, returns `{resume, coverLetter}`
- `POST /api/resume/docx` — generates Word doc from resume JSON (mammoth + docx packages)
- `POST /api/resume/pdf` — Playwright renders resume HTML → PDF buffer
- `POST /api/linkedin/save-session` — saves LinkedIn cookies JSON to linkedin-session.json
- `GET /api/linkedin/session-status` — checks if session file exists
- `POST /api/linkedin/apply` — Playwright fills LinkedIn Easy Apply form, pauses for review
- `POST /api/linkedin/submit` — confirms and submits the paused application
- `GET /resume` — serves resume.html

## Features
- **Bookmarklet** (⬡ GRAB JD) — drag to Chrome bar, click on any job page to pre-fill JD via ?jd= param
- **DOWNLOAD DOCX** — exports resume as formatted Word document
- **APPLY TO LINKEDIN** — modal: paste cookies once, enter job URL, Playwright fills Easy Apply, screenshot review before submit

## BASE_RESUME
Stored as `const BASE_RESUME` in server.js. Full employment history for Alexander Thuku.
Master source: `C:\Users\Pinko\Documents\Alexander_Thuku_Updated_Resume.docx`

## Deploy
```
cd C:\Users\Pinko\claudesandbox\proles-consulting
git add -A
git commit -m "..."
railway up --detach
railway logs --tail 15
```
Build takes 2-3 min (Playwright + Chromium ~150MB).
`ANTHROPIC_API_KEY` must be set in Railway → proles-consulting service → Variables.

## Env Vars (Railway)
- `ANTHROPIC_API_KEY` — required for generation

## Notes
- `linkedin-session.json` and `tmp_resume.pdf` are gitignored
- Bare domain prolesconsulting.com (no www) has DNS redirect pending via Namecheap
