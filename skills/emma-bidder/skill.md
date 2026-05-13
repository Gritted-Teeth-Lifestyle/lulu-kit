---
name: emma-bidder
description: Manage, fix, and deploy the eMMA Bid Automator on Railway. Use when submitting bids on eMaryland Marketplace Advantage (eMMA), updating company data, fixing automation issues, or deploying updates.
---

# eMMA Bid Automator

Flask + Playwright app with two tabs:
- **Tab 1 — eMMA Maryland:** Auto-fills Maryland eMMA solicitation forms, creates Gmail drafts for review
- **Tab 2 — SAM.gov Federal:** Searches federal opportunities, finds subcontractors, creates outreach email drafts

## LIVE URL
`https://emma-bidder-production.up.railway.app`

## Files
- **Local:** `C:\Users\Pinko\claudesandbox\emma-bidder\`
- **GitHub:** `github.com/kamipinko/emma-bidder` (private)
- **Key files:** `app.py`, `bidder.py`, `gmail_client.py`, `sam_client.py`, `sam_outreach.py`, `emma_outreach.py`, `company_data.py`, `naics_infer.py`, `naics_wbs.py`

## Company Data (Proles L.L.C)
- Address: 6610 Eastern Parkway, Baltimore, MD 21214
- Email: amthuku@gmail.com
- DUNS: 392985621
- Plumbing sub: AT Plumbing and Gas Fitting

## Railway Environment Variables
- `EMMA_USERNAME` = amthuku@gmail.com
- `EMMA_PASSWORD` = L0v3@lway5em@
- `GMAIL_TOKEN_JSON` = base64-encoded token.json
- `GMAIL_USER` / `GMAIL_TO` = amthuku@gmail.com
- `SAM_API_KEY` = SAM.gov API key (get free at api.sam.gov)
- Source token: `C:\Users\Pinko\claudesandbox\emma-bidder\token.json`

## Routes
| Route | Method | Description |
|---|---|---|
| `/` | GET | Main UI (two tabs) |
| `/bid` | POST | Run eMMA Playwright automation |
| `/sam/search` | GET | Search SAM.gov opportunities (?q=&naics=&state=&limit=) |
| `/sam/opportunity` | GET | Fetch single opportunity by URL (?url=) |
| `/sam/contractors` | GET | Search contractors (?naics=&state=&limit=) |
| `/sam/outreach` | POST | Create SAM outreach Gmail drafts |
| `/emma/contractors` | POST | Search contractors for eMMA project (defaults state=MD) |
| `/emma/outreach` | POST | Create eMMA outreach Gmail drafts |
| `/health` | GET | Returns "OK" |

## eMMA Tab Flow
1. User pastes eMMA solicitation URL
2. Playwright logs in → navigates → fills all visible form fields via `FIELD_MAP` in `bidder.py`
3. Screenshots every step
4. Creates Gmail DRAFT to amthuku@gmail.com — subject: `[eMMA BID READY] <Project Title>`
5. User reviews draft + screenshots, then manually submits on eMMA

## SAM.gov Tab Flow
1. User enters keywords/NAICS to search federal opportunities
2. User selects an opportunity → contractors are found via triple-layer search
3. User clicks "Draft Outreach" → Gmail drafts created for each contractor with email

## Contractor Search — Triple-Layer (`sam_client.py`)
**Layer 1:** SAM Entity API + NAICS + state=MD (local first)
**Layer 2:** SAM Entity API + NAICS, national (if Layer 1 < 5 results)
**Layer 3:** USASpending.gov historical award winners (if Layers 1+2 < 5 results)

Deduplication via UEI. API: `GET https://api.sam.gov/entity-information/v3/entities`

**Three bugs fixed 2026-05-13:**
1. Removed `purposeOfRegistrationCode: "Z2"` (Z2 = Grants Only, excluded all contractors)
2. `pointsOfContact` is a list, not a dict — parser handles both shapes
3. Added `physicalAddressStateOrProvinceCode=MD` for Layer 1

## Outreach Email Voice (Thuku style)
Both `sam_outreach.py` and `emma_outreach.py` use the invariant sign-off:
```
If there are any questions do not hesitate to call or email me,
Thank you and have a wonderful day!

Very Respectfully,
-- 
//SIGNED//
ALEXANDER THUKU
Cell: 434/429.9296
Email: athuku@tulane.edu
amthuku@gmail.com
```
Greeting: `Hi [Name],` — Opener: `Hope you're doing well. Just reaching out regarding...`

## Deploy
```powershell
cd C:\Users\Pinko\claudesandbox\emma-bidder
git add <files>
git commit -m "..."
git push
railway up --ci
```
Railway uses Dockerfile builder (set in railway.toml). Build takes ~5-10 min due to Playwright/Chromium.

## Common Issues

**Gmail draft fails (`invalid_grant`):**
Token expired. Fix:
1. `cd C:\Users\Pinko\claudesandbox\emma-bidder`
2. `python reauth.py` — browser opens, sign in as amthuku@gmail.com
3. New `token.json` written locally
4. `$b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("token.json"))`
5. `railway variables set GMAIL_TOKEN_JSON=$b64`
6. `railway up --ci`

**Healthcheck fails after deploy:**
Check Railway build logs for Python `SyntaxError: invalid character`. The Edit tool sometimes inserts smart quotes (U+2018/U+2019) in f-strings. Fix:
```powershell
$c = Get-Content sam_outreach.py -Raw
$c = $c -replace [char]0x2018,"'" -replace [char]0x2019,"'"
Set-Content sam_outreach.py $c
python -m py_compile sam_outreach.py  # verify clean
```

**Login fails:** eMMA may have updated selectors. Check `bidder.py` `EMMA_LOGIN_URL` and username/password selector lists.

**Field not filled:** Add field's label text to `FIELD_MAP` in `bidder.py`.

**No contractors found:** Check SAM_API_KEY is set in Railway. Verify NAICS code is valid. Layer 3 (USASpending) requires no key and always returns results.
