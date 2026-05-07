---
name: file-organizer
description: File and folder organization commands for PC drives. Covers duplicate scanning, cross-drive cleanup, folder restructuring, and game save safety rules.
user-invocable: true
triggers: ["organize drives", "clean drives", "file cleanup", "duplicate scan", "organize files", "drive cleanup"]
---

# File Organization Command Guide

## Drives Reference

| Drive | Label | Primary Use |
|-------|-------|-------------|
| C:\   | System | User profile — skip AppData |
| D:\   | Drive D | Storage |
| E:\   | Drive E | Storage |
| F:\   | Drive F | Storage |
| G:\   | Drive G | Archive |

---

## Phase 1 — Duplicate Scan Command

**Subordinate:** Epsilon  
**Task file:** `<HOME>\claude-vision\tasks\Epsilon_task.txt`  
**Log:** `<HOME>\claude-vision\logs\Epsilon_log.txt`  
**Output:** `dup_all_drives.json` + `dup_all_summary.txt` in logs folder  

### Key parameters
- Min file size: **5MB** (skip smaller — too many false positives)
- Hash: **MD5** full file
- Cross-drive: YES — same MD5 on different drives = duplicate
- Scan C: user profile only (skip AppData, Windows, Program Files)
- Result: two lists — `main` (safe to clean) and `saves` (manual review only)

### Launch pattern
```python
import subprocess

task = open(r"<HOME>\claude-vision\tasks\Epsilon_task.txt").read()
log_path = r"<HOME>\claude-vision\logs\Epsilon_log.txt"
with open(log_path, "w") as f:
    f.write("=== EPSILON STARTING ===\n")

proc = subprocess.Popen(
    ["claude", "--dangerously-skip-permissions", "--print", task],
    cwd=r"<HOME>\claudesandbox",
    stdout=open(log_path, "a"),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.CREATE_NO_WINDOW
)
print(f"Epsilon launched | PID {proc.pid}")
```

### Read results
```python
import json
report = json.load(open(r"<HOME>\claude-vision\logs\dup_all_drives.json"))
main = report["main"]   # safe to clean
saves = report["saves"] # manual review only
print(f"Main: {len(main)} groups | Saves: {len(saves)} groups")
```

---

## Phase 2 — Folder Structure Survey Command

**Subordinate:** Zeta  
**Task file:** `<HOME>\claude-vision\tasks\Zeta_task.txt`  
**Log:** `<HOME>\claude-vision\logs\Zeta_log.txt`  
**Output:** `drive_structure.txt` (raw map) + full analysis in Zeta_log

Run Zeta in parallel with Epsilon — it's read-only and fast.

### Zeta produces
1. Current folder map (3 levels deep, all drives)
2. Problems: duplicate folder names, bad casing, vague names, loose root files
3. Proposed clean hierarchy (see standard below)
4. Move plan with game save flags

---

## Phase 3 — Cleanup Execution Command

Only dispatch after reviewing Phase 1 + 2 reports. Send one subordinate per drive to avoid conflicts.

**Never auto-execute.** Always present the move plan for user approval first.

### Move script pattern (safe — moves to a staging folder, not delete)
```python
import os, shutil, json

REPORT = r"<HOME>\claude-vision\logs\dup_all_drives.json"
STAGING = r"E:\DUPLICATES_TO_REVIEW"  # staging — review and delete manually

report = json.load(open(REPORT))
moved = 0
errors = []

os.makedirs(STAGING, exist_ok=True)

for group in report["main"]:
    for path in group["move"]:
        try:
            rel = os.path.relpath(path, os.path.splitdrive(path)[0] + "\\")
            dest = os.path.join(STAGING, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.move(path, dest)
            moved += 1
        except Exception as e:
            errors.append(f"{path}: {e}")

print(f"Moved {moved} files to {STAGING}")
if errors:
    print(f"Errors: {len(errors)}")
    for e in errors[:10]:
        print(f"  {e}")
```

**DO NOT use `shutil.rmtree` or `os.remove` directly on duplicates** — always move to staging first. Review staging and delete manually.

---

## Standard Folder Hierarchy

Apply to whichever drive has the content. Keep gaming consolidated to fewest drives possible.

```
Gaming/
  roms/
    xbox/
    ps2/
    ps3/
    ps4/
    psp/
    3ds/
    pc/
  saves/              ← GAME SAVES — always flag, never auto-move
    (platform)/
  emulators/          ← emulator binaries + configs
  screenshots/

Media/
  videos/
    personal/
    cooking/
    projects/
  music/
  photos/

Projects/
  (project-name)/

Archive/
  (year)/

Documents/
  work/
  school/
  contracts/

Personal/
  family/
  (person-name)/
```

### Naming conventions
- PascalCase for top-level: `Gaming`, `Media`, `Projects`, `Archive`
- lowercase for sub-content: `roms`, `saves`, `videos`, `music`
- Hyphens not spaces: `project-name` not `Project Name`
- No version numbers in folder names unless it's software

---

## Game Save Safety Rules

**These are the highest-priority rules. Non-negotiable.**

### What counts as a game save (never auto-move)
- Any path containing: `\Saves\`, `\SaveData\`, `\save_data\`, `\userdata\`, `\SaveGames\`
- Emulator save paths: `rpcs3\dev_hdd0\home`, `xenia\content`, `xemu` + (`hdd` or `saves`)
- Extensions in game directories: `.sav`, `.mcr`, `.vmp`, `.srm`, `.state`, `.sl2`, `.dss`
- Entire `<HOME>\AppData\` — never touch
- `<HOME>\Documents\My Games\` — flag only, no auto-move

### What is NOT a save (safe to reorganize)
- ROM files: `.iso`, `.7z`, `.zip`, `.nsp`, `.xci`, `.bin` (unless inside a saves folder)
- Emulator binaries and configs (the exe, not the save folder)
- Screenshots from emulators
- DLC packages

### Command instruction for saves
When writing a task that involves game areas:
> "Flag any path matching save markers as [GAME SAVE — MANUAL REVIEW]. Do not include in the auto-move list. Do not move them. List them separately."

---

## Subordinate Naming Convention for Drive Ops

| Subordinate | Role |
|-------------|------|
| Epsilon | Scanner — duplicate detection, structure survey |
| Zeta | Planner — org scheme, move plan |
| Eta | Executor E: — moves on E: drive only |
| Theta | Executor F: — moves on F: drive only |
| Iota | Executor G: — moves on G: drive only |
| Kappa | Executor D: — moves on D: drive only |

One executor per drive. Lelouch reviews the plan before dispatching any executor.

---

## Completion Signals to Watch For

- Epsilon done: `grep -q "EPSILON COMPLETE" Epsilon_log.txt`
- Zeta done: `grep -q "ZETA COMPLETE" Zeta_log.txt`
- Any executor done: `grep -q "COMPLETE" NAME_log.txt`

Monitor loop:
```bash
until grep -q "COMPLETE" "<HOME>/claude-vision/logs/Epsilon_log.txt"; do sleep 30; done && echo "Epsilon done"
```
