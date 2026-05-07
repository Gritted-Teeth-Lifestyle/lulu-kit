"""
alert.py — Lelouch attention system
Subtle amber flash strip at the bottom of the main screen.
Usage: python alert.py "Message here"
"""
import sys
import time
import tkinter as tk

msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Lelouch needs your attention"

# Flash a thin amber strip at the bottom of the primary monitor
root = tk.Tk()
root.overrideredirect(True)          # no title bar
root.attributes('-topmost', True)
root.attributes('-alpha', 0.0)       # start invisible

# Primary monitor: 3840 wide, bottom strip 6px tall
SCREEN_W = 3840
STRIP_H = 6
root.geometry(f"{SCREEN_W}x{STRIP_H}+0+{root.winfo_screenheight() - STRIP_H}")

# Amber color matching IOI brand
frame = tk.Frame(root, bg='#D4820A')
frame.pack(fill='both', expand=True)

# Optional label — tiny, right-aligned, only visible on brighter flashes
label = tk.Label(frame, text=msg, bg='#D4820A', fg='#FFF8E7',
                 font=('Share Tech Mono', 8), anchor='e', padx=8)
label.pack(fill='x')

FLASHES = 4
FADE_STEPS = 12
PEAK_ALPHA = 0.55   # subtle — not blinding

def flash_cycle(n=0):
    if n >= FLASHES * 2:
        root.destroy()
        return
    # Even = fade in, odd = fade out
    target = PEAK_ALPHA if n % 2 == 0 else 0.0
    current = root.attributes('-alpha')
    step = (target - current) / FADE_STEPS

    def fade(step_n=0, alpha=current):
        if step_n >= FADE_STEPS:
            root.attributes('-alpha', target)
            root.after(60, lambda: flash_cycle(n + 1))
            return
        alpha = max(0.0, min(PEAK_ALPHA, alpha + step))
        root.attributes('-alpha', alpha)
        root.after(18, lambda: fade(step_n + 1, alpha))

    fade()

root.after(50, flash_cycle)
root.mainloop()
