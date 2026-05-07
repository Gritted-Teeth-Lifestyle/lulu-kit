---
name: dispatch
description: Launch, monitor, and coordinate background Claude CLI subprocesses for parallel task execution
---

# Dispatch

The worker-dispatch framework. Launch named Claude subprocesses in the background, monitor them via log files, and coordinate parallel task execution — all from a single orchestrating Claude session.

## WHEN_TO_USE

Use this skill when you need to:
- Run multiple independent Claude tasks in parallel
- Offload a long-running task without blocking the current session
- Coordinate a multi-agent workflow (Alpha does X while Beta does Y)
- Monitor background workers and fire alerts when they finish

## HOW_TO_USE

### Worker naming convention
Name workers after the NATO/Greek alphabet in order:
`Alpha, Beta, Gamma, Delta, Epsilon, Zeta, Eta`

### Step 1 — Write a task file
```python
import os
task_dir = r"<HOME>\claude-vision\tasks"
os.makedirs(task_dir, exist_ok=True)

task = """Your full task prompt here.
Be specific. The worker has no conversation context.
End with: Write COMPLETE to <HOME>\\claude-vision\\tasks\\alpha_status.txt when done.
"""

with open(os.path.join(task_dir, "alpha_task.txt"), "w") as f:
    f.write(task)
```

### Step 2 — Launch the worker
```python
import subprocess, os

log_path = r"<HOME>\claude-vision\tasks\alpha_log.txt"
task_path = r"<HOME>\claude-vision\tasks\alpha_task.txt"
task_text = open(task_path).read()

with open(log_path, "w") as log_file:
    proc = subprocess.Popen(
        ['claude', '--dangerously-skip-permissions', '--print', task_text],
        cwd=r"<HOME>\claude-vision",
        stdout=log_file,
        stderr=log_file,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
print(f"Alpha launched (PID {proc.pid})")
```

### Step 3 — Open a monitor window (upper monitor)
To watch a worker log on the monitor above the main display (y = -1440 to y = 0):
```powershell
# Open log in Windows Terminal positioned on upper monitor
wt --pos 0,-1440 --size 220,50 powershell -NoExit -Command "Get-Content '<HOME>\claude-vision\tasks\alpha_log.txt' -Wait"
```

### Step 4 — Poll for completion
```python
import time, os

status_path = r"<HOME>\claude-vision\tasks\alpha_status.txt"

while True:
    if os.path.exists(status_path):
        status = open(status_path).read().strip()
        if "COMPLETE" in status:
            print("Alpha: COMPLETE")
            break
        elif "FAIL" in status:
            print("Alpha: FAILED")
            break
    time.sleep(5)
```

### Step 5 — Fire alert when done
```python
import subprocess
subprocess.run(['python', r'<HOME>\claude-vision\alert.py', 'Alpha complete'])
```

## STANDARD LAUNCH BOILERPLATE

Full copy-paste launch pattern for a named worker:

```python
import subprocess, os, time

WORKER = "alpha"
TASK_DIR = r"<HOME>\claude-vision\tasks"
os.makedirs(TASK_DIR, exist_ok=True)

task = f"""[Your task here]

When complete, write 'COMPLETE' to {TASK_DIR}\\{WORKER}_status.txt
If you fail, write 'FAIL: <reason>' to the same file.
"""

task_path = os.path.join(TASK_DIR, f"{WORKER}_task.txt")
log_path = os.path.join(TASK_DIR, f"{WORKER}_log.txt")
status_path = os.path.join(TASK_DIR, f"{WORKER}_status.txt")

with open(task_path, "w") as f:
    f.write(task)

with open(log_path, "w") as log_file:
    proc = subprocess.Popen(
        ['claude', '--dangerously-skip-permissions', '--print', task],
        cwd=r"<HOME>\claude-vision",
        stdout=log_file,
        stderr=log_file,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

print(f"{WORKER.capitalize()} launched — PID {proc.pid}")
print(f"Log: {log_path}")

# Poll for completion
while True:
    if os.path.exists(status_path):
        result = open(status_path).read().strip()
        print(f"{WORKER.capitalize()}: {result}")
        break
    time.sleep(5)
```

## RULES

- Always give workers a self-contained task — they have no conversation context
- Always include a status-file write instruction at the end of every task
- Use `CREATE_NO_WINDOW` to keep background processes invisible
- Monitor logs via `Get-Content -Wait` on the upper monitor (y=-1440)
- Name workers in order: Alpha first, then Beta, Gamma, etc.
- Fire `alert.py` when workers complete so you're notified
