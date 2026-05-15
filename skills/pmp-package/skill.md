---
name: pmp-package
description: Build a full Proles Consulting PMP package for a client engagement — 13 DTIC markdown docs, a print-ready HTML business case, and a dark-theme online pitch deck. Use when Pinko needs a project management package for a new or existing client.
---

# PMP Package Builder — Proles Consulting

Builds a complete DTIC-framework project management package dispatched via Alpha sub. Outputs: 13 markdown docs + HTML business case + 10-slide pitch deck.

## Framework
DTIC AL/EQ-HBK-61-2 (1996 U.S. Air Force Armstrong Laboratory). Key mappings:
- TIP = Project Charter
- TTP = Technology Transition Plan (handoff)
- GCE = Budget/Cost Estimate
- CDRL = Deliverables list
- Case File = Project Index (doc 00)

## Output Structure (always 13 + 2 files)
```
C:\Users\Pinko\Documents\PMP Projects\[Client Name]\
  00_Project_Index.md
  01_Business_Case.md
  02_Project_Charter.md
  03_Scope_Statement.md
  04_WBS.md
  05_WBS_Dictionary.md
  06_Statement_of_Work.md
  07_Risk_Register.md
  08_Communications_Plan.md
  09_Project_Schedule_Milestones.md
  10_Budget_Cost_Estimate.md
  11_Team_RACI.md
  12_Technology_Transition_Plan.md
  [REF]_Business_Case.html         ← print-ready, PDF via Chrome print
C:\Users\Pinko\claudesandbox\proles-consulting\
  [slug]-pitch.html                ← 10-slide dark pitch deck
```

## Completed Projects

### Heisenberg Ammo LLC (WCO-HAL-2026-001) — 2026-05-13
- **Client:** Gabriel Hillman | (832) 444-6651 | gabriel_hillman@heisenbergammollc.com
- **Scope:** Warehouse cleaning & organization, ammunition facility, Sugar Land TX
- **Special compliance:** OSHA 29 CFR 1910.109 + NFPA 495 — static-free equipment, Proles crew never touches ammo
- **Files:** `C:\Users\Pinko\Documents\PMP Projects\Warehouse Cleanup\`
- **Pitch:** `prolesconsulting.com/warehouse-pitch.html` (deploy via `railway up`)
- **Budget range:** $16,500 – $31,086
- **Gmail draft:** sent to amthuku@gmail.com with all file paths (draft ID r7408145396941254852)

### Inspired Options Inc — IOI Website (INS-WEB-2026-001) — 2026-04-16
- Folder: `C:\Users\Pinko\Documents\PMP Projects\Inspired Options Inc Website\`
- Full DTIC set + DOCX conversions + business case PDF

## Brand Colors (all packages)
`--crimson:#8B1A1A | --navy:#1B2F45 | --teal:#1A7A6A | --amber:#B8720A | --paper:#FAFAFA`

## HTML Business Case — Key CSS Rules
```css
/* EXACT — do not change */
@media print {
  .page { box-shadow:none!important; margin:0!important; padding:0!important; }
  .cover-page { page-break-after:always; padding:0.75in 0.85in!important; }
  @page { size:letter portrait; margin:0.75in 0.85in; }
}
/* Cover: display:flex flex-direction:column min-height:11in */
/* Content: NO min-height — flows naturally */
/* Padding shorthand on child class ZEROS inherited left/right — use padding-top/bottom only */
```

## Pitch Deck Engine
- `.slide` fixed-position, `.slide.active` visible, `.reveal` animates in on click
- Space/Click = next reveal or next slide | ArrowLeft = previous | ESC = prolesconsulting.com
- 6px crimson left bar on every slide (`::before`)
- Gold progress bar top, slide counter bottom-right
- Proles logo bottom-left: `images/proles-consulting-logo.svg` filtered white

## Dispatch Pattern
Always send via Alpha sub (`alpha_runner.ps1` piping task via stdin to `claude --dangerously-skip-permissions --print`).
Task file: `C:\Users\Pinko\claude-vision\tasks\alpha_task.txt`
Log: `C:\Users\Pinko\claude-vision\logs\alpha_log.txt`
Status: `C:\Users\Pinko\claude-vision\tasks\alpha_status.txt` (writes "COMPLETE" or "FAIL: reason")

Poll with `.NET` `Directory.GetFiles()` — `Get-ChildItem` sometimes returns nothing on this machine.

## After Completion
1. Verify file count in Warehouse Cleanup folder
2. Create Gmail draft via MCP `mcp__claude_ai_Gmail__create_draft` with file paths + budget table
3. Note: pitch deck needs `railway up` from `claudesandbox\proles-consulting\` to go live
4. Update `project_pmp_projects.md` memory with new project entry
