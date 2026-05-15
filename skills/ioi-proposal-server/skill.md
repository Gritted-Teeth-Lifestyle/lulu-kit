---
name: ioi-proposal-server
description: Manage, fix, and deploy the IOI Digitalization Outreach Proposal Server on Railway. Use when making changes to proposals, email drafts, demo pages, client-site branding, phone numbers, or deploying updates.
---

# IOI Proposal Server — Digitalization Outreach

Flask server that generates personalized proposals, Gmail drafts, and demo websites for Proles HHC outreach to 50 SDAT-verified Maryland DDA/home health agencies.

## LIVE URL
`https://ioi-proposal-server-production.up.railway.app`

## Files
- **Local:** `C:\Users\Pinko\claudesandbox\proposal-server-deploy\app.py`
- **GitHub:** `kamipinko/ioi-proposal-server` (branch: `main`)
- **Templates:** `proposal-server-deploy\static\ioi_templates\` (index.html, services.html, about.html, contact.html, style.css)

**Always read `app.py` fresh before editing — it is 2100+ lines and changes every session.**

## Deploy
Push to `main` → Railway auto-deploys in ~2 minutes. **BUT Railway auto-deploy frequently stalls.** If the live site serves old code after a push, force it:

```powershell
cd "C:\Users\Pinko\claudesandbox\proposal-server-deploy"
railway up
```

Then poll until live: `until curl -sf <url> | grep -q "signal text"; do sleep 15; done`

```powershell
cd "C:\Users\Pinko\claudesandbox\proposal-server-deploy"
git add app.py
git commit -m "Your message"
git push
```

## Routes
| Route | What it does |
|-------|-------------|
| `/` | Dashboard — P5-styled table of all 50 agencies with modal |
| `/proposal/<n>` | Branded proposal HTML for agency n |
| `/email/<n>` | Email template preview page |
| `/generate-draft/<n>` | Creates Gmail draft (HTML + plain text + PDF attachment) |
| `/book/<n>` | Compact booking card (date/time dropdowns, Meet/Zoom) |
| `/overview/<n>` | **One-page executive overview** — stat boxes, gaps, 3-phase delivery, financials, ROI (auto-generated per agency) |
| `/demo/<n>` | **Primary demo page** — custom-built, no IOI templates, fully clean |
| `/client-site/<n>/` | IOI-template site personalized for agency n (secondary) |
| `/client-site/<n>/services` | Personalized services page |
| `/client-site/<n>/about` | Personalized about page |
| `/client-site/<n>/contact` | Personalized contact page |

**Rule:** Proposal and email links always point to `/demo/<n>` — NOT `/client-site/<n>/`.

## Key Constants
```python
COMPANY     = 'Proles Home Healthcare Consultants'
COMPANY_URL = 'www.prolesconsulting.com'
GMAIL_USER  = 'amthuku@gmail.com'
RAILWAY_URL = 'https://ioi-proposal-server-production.up.railway.app'
```
Contact phone: **(434) 429-9296** — Alex Thuku

## Railway Env Vars
```
GMAIL_CLIENT_ID     = <set in Railway — Google OAuth client ID>
GMAIL_CLIENT_SECRET = <set in Railway — Google OAuth client secret>
GMAIL_REFRESH_TOKEN = <set in Railway — Google OAuth refresh token>
GMAIL_USER          = amthuku@gmail.com
```

## build_client_site() — Branding Scrub Rules
The IOI templates contain Inspired Options Inc branding. `build_client_site()` scrubs all of it:

```python
# Agency identity
h = h.replace('Inspired Options Inc', name)
h = h.replace('Inspired Options Care', name)
h = h.replace('Inspired Options', name)

# Person names (IOI staff → generic team)
h = h.replace('Dr. Patricia Ametepi', 'Dr. Angela Brooks')
h = h.replace('Dr. Ametepi', 'Dr. Brooks')
h = h.replace('Marcus Johnson, LCSW', 'James Carter, LCSW')
h = h.replace('Marcus Johnson', 'James Carter')
h = h.replace('Tamara Reeves, RN', 'Patricia Moore, RN')
h = h.replace('Tamara Reeves', 'Patricia Moore')
h = h.replace('David Williams', 'Robert Davis')

# Domain + contact
h = h.replace('inspiredoptionscare.com', f'{slugify(name)}.com')
h = h.replace('https://www.instagram.com/InspiredOptionsCare', '#')

# Team grid — use REGEX not exact string (whitespace mismatch kills exact match)
h = re.sub(r'<div class="team-grid">.*?</div>\s*</div>\s*</div>\s*</section>',
           NEW_TEAM_GRID + '</div></section>', h, flags=re.DOTALL)
```

**Critical lesson:** Never use exact-string replacement for the team-grid — whitespace between the hardcoded string and the actual file will differ. Always use `re.sub()` with `re.DOTALL`.

## Generic Team (randomuser.me photos)
| Name | Role | Photo |
|------|------|-------|
| Dr. Angela Brooks | Founder & Executive Director | randomuser.me/api/portraits/women/44.jpg |
| James Carter, LCSW | Director of Clinical Services | randomuser.me/api/portraits/men/32.jpg |
| Patricia Moore, RN | Care Coordination Supervisor | randomuser.me/api/portraits/women/68.jpg |
| Robert Davis | Compliance & Training Manager | randomuser.me/api/portraits/men/75.jpg |

## PDF Generation — WeasyPrint
WeasyPrint cannot resolve CSS vars (`var(--gold)` etc.).
Fix: `build_proposal_for_pdf()` runs `_CSS_VAR_MAP` string replacements before passing HTML to WeasyPrint.

**Python version critical:** Railway defaults to Python 3.13. WeasyPrint's libgobject cannot load on 3.13. `nixpacks.toml` must pin:
```toml
[variables]
NIXPACKS_PYTHON_VERSION = "3.12"
```
This is already in place as of 2026-05-03 (commit `6c19795`). If WeasyPrint breaks again after a rebuild, this is why.

## build_demo() — Full P5 Demo Page (rebuilt 2026-05-03)
`build_demo()` at ~line 949 in app.py generates a complete agency-specific website. Sections in order:
1. Fixed gold demo banner + VIEW PROPOSAL link
2. Sticky nav: Services | About | Who We Serve | Careers | **Contact Us** (gold clip-path button)
3. Hero: full-viewport, diagonal clip-path, red accent stripes, stat cards (Licensed / Serving {city} / OHCQ Compliant)
4. Accent bar (red→gold gradient)
5. OUR MISSION — two-col: mission text + gold blockquote card
6. Accent bar
7. WHAT WE OFFER — services grid (from `demo_services()`)
8. WHY {AGENCY} — 3 numbered commitment cards
9. WHO WE SERVE — client group chips
10. Accent bar
11. CAREERS — banner strip
12. GET IN TOUCH — contact: phone (gold, large), email, gold CTA button
13. Footer

## Agency Data
`static/agencies.json` — 50 entries. Fields: `num, name, type, city, county, zip, phone, email, sdat_status`

## Common Fix Patterns

### Phone number update
```python
# In app.py — replace_all=true for each format
(443) 374-2931  →  (434) 429-9296
443-374-2931    →  434-429-9296
+14433742931    →  +14344299296
```

### Link target change (e.g., client-site → demo)
Search for all occurrences of `/client-site/{n}/` in `build_proposal()`, `build_email_html()`, `build_email_text()` and replace with `/demo/{n}`.

### Dispatch sub for template changes
Use the dispatch skill with Alpha. The worker needs to:
1. Read all 4 template files
2. Find all IOI references
3. Add replacements to `build_client_site()`
4. Commit + push

## build_overview(agency, n) — One-Page Executive Overview (added 2026-05-08)
Auto-generates a print-ready one-pager for any of the 50 agencies. Same structural DNA as the Animet-Overview.html. Uses P5 colors, Arial fonts (no Google Fonts — WeasyPrint compatible). Functions needed: `build_overview(agency, n)` + `/overview/<n>` Flask route.

Sections in order:
1. Header (name, city, Proles logo, confidential meta)
2. 4 stat boxes: 65% search online · 3 Wks launch · 50+ MD agencies · $1,800 investment
3. Snapshot bar: agency / city / type / service
4. Two-col: Capability Gaps (all NONE, red badge) + Cost of Inaction (~$62K/yr)
5. 3-col Phase cards: Audit & Brand (Wks 1–2) → Build & Launch (Wks 2–4) → SEO & Optimize (Days 30–60)
6. Financial tables: Investment $1,800 vs. Year 1 Return $13,200
7. 4 metric boxes: 7.3× ROI · 3 Wks · 60 Days SEO · $11,400 net benefit
8. 3-col Success Targets: Website / Local SEO {city} / Client Growth
9. Closing recommendation box

Email strip: added to `build_email_html()` before footer — stat grid + 3 bullets + link to `/overview/<n>`.

## Design System
P5 / Persona 5 aesthetic throughout:
- Colors: `#111111` bg, `#ECAA27` gold, `#8a0a0a` red, `#f5f0e8` cream text
- Clip-path diagonal buttons: `polygon(8px 0%, 100% 0%, calc(100% - 8px) 100%, 0% 100%)`
- Monospace section labels with letter-spacing
- Arial fonts only (no Google Fonts — WeasyPrint compatibility)
