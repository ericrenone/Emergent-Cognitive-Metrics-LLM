#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Emergent Cognitive Metrics - LLM
Canonical simulation of LLM-inspired cognitive dynamics.
Fully self-contained, no external dependencies beyond Python standard library.

Author: Eric Ren
License: MIT
"""

import math
import random
import tkinter as tk
import sys

# ---------------- Configuration ----------------
class Config:
    STEPS = 150
    VOCAB_SIZE = 10
    DECAY = 0.91
    ALPHA_PENALTY = 0.4
    BG_COLOR = "#0F111A"
    ACCENT_BLUE = "#00E5FF"
    ACCENT_PINK = "#FF007F"
    ACCENT_GREEN = "#00FF9C"
    GRID_COLOR = "#1F2233"
    RANDOM_SEED = 42
    HEADLESS = "--cli" in sys.argv

# ---------------- Core Engine ----------------
class LLMCore:
    def __init__(self, config: Config):
        self.config = config
        random.seed(self.config.RANDOM_SEED)
        if self.config.STEPS < 2 or self.config.VOCAB_SIZE < 1:
            raise ValueError("STEPS >=2 and VOCAB_SIZE >=1 required")

        self.stream = self._generate_stochastic_stream()
        self.logic = []
        self.aesthetic = []
        self.understanding = []
        self.utility = []
        self._solve_dynamics()

    def _generate_stochastic_stream(self):
        """Power-law stochastic token stream (heavy-tailed)."""
        data = []
        for _ in range(self.config.STEPS):
            raw = [random.random() ** 4 for _ in range(self.config.VOCAB_SIZE)]
            norm = sum(raw) or 1e-10
            data.append([r / norm for r in raw])
        return data

    def _solve_dynamics(self):
        """Compute logic, aesthetic, understanding, utility."""
        l_state = a_state = 0.0
        for probs in self.stream:
            fidelity = max(probs)
            entropy = -sum(p * math.log(p + 1e-10) for p in probs)
            l_state = (l_state * self.config.DECAY) + (fidelity * 1.2)
            a_state = (a_state * self.config.DECAY) + (entropy * 0.8)
            synthesis = math.sqrt(l_state * a_state)
            util = fidelity - (self.config.ALPHA_PENALTY * entropy)
            self.logic.append(l_state)
            self.aesthetic.append(a_state)
            self.understanding.append(synthesis)
            self.utility.append(util)

# ---------------- Visualization ----------------
class Dashboard:
    def __init__(self, core: LLMCore):
        self.core = core
        self.config = core.config
        if self.config.HEADLESS:
            self.print_metrics()
        else:
            try:
                self.root = tk.Tk()
            except tk.TclError:
                print("Tkinter failed (headless?), fallback to CLI metrics")
                self.print_metrics()
                return
            self.root.title("Emergent Cognitive Metrics - LLM")
            self.root.geometry("1200x900")
            self.root.configure(bg=self.config.BG_COLOR)
            self.canvas = tk.Canvas(self.root, width=1150, height=850,
                                    bg=self.config.BG_COLOR, highlightthickness=0)
            self.canvas.pack(pady=20)
            self.render()
            self.root.mainloop()

    def print_metrics(self):
        print("Final Metrics:")
        print(f"Logic: {self.core.logic[-1]:.4f}")
        print(f"Aesthetic: {self.core.aesthetic[-1]:.4f}")
        print(f"Understanding: {self.core.understanding[-1]:.4f}")
        print(f"Utility: {self.core.utility[-1]:.4f}")

    def draw_axes(self, x, y, w, h, title):
        for i in range(5):
            offset = (i / 4) * h
            self.canvas.create_line(x, y + offset, x + w, y + offset,
                                    fill=self.config.GRID_COLOR, dash=(2, 4))
        self.canvas.create_text(x + w / 2, y - 25, text=title.upper(),
                                fill="white", font=("Arial", 11, "bold"))
        self.canvas.create_rectangle(x, y, x + w, y + h, outline=self.config.GRID_COLOR, width=1)

    def plot_series(self, x, y, w, h, data, color, label, fill=False):
        if not data: return
        d_max = max(data) or 1.0
        coords = []
        for i, val in enumerate(data):
            px = x + (i / (len(data) - 1)) * w
            py = y + h - (val / d_max) * h
            coords.extend([px, py])
        if fill:
            poly = [x, y + h] + coords + [x + w, y + h]
            self.canvas.create_polygon(poly, fill=color, stipple="gray25", outline="")
        self.canvas.create_line(coords, fill=color, width=2, smooth=True)
        self.canvas.create_text(x + w - 5, y + 15, text=label, fill=color, font=("Arial", 9), anchor="e")

    def draw_heatmap(self, x, y, w, h):
        self.draw_axes(x, y, w, h, "Stochastic Token Stream")
        cw, ch = w / self.config.STEPS, h / self.config.VOCAB_SIZE
        for i, probs in enumerate(self.core.stream):
            for j, p in enumerate(probs):
                val = int(p * 255)
                r = max(0, val - 128)
                g = val
                b = 255 - val // 2
                color = f'#{r:02x}{g:02x}{b:02x}'
                self.canvas.create_rectangle(x + i * cw, y + j * ch,
                                             x + (i + 1) * cw, y + (j + 1) * ch,
                                             fill=color, outline="")

    def draw_phase_space(self, x, y, w, h):
        self.draw_axes(x, y, w, h, "Phase Space (Logic vs Aesthetic)")
        l_max = max(self.core.logic) or 1.0
        a_max = max(self.core.aesthetic) or 1.0
        u_max = max(self.core.understanding) or 1.0
        for i in range(self.config.STEPS):
            px = x + (self.core.logic[i] / l_max) * w
            py = y + h - (self.core.aesthetic[i] / a_max) * h
            r = (self.core.understanding[i] / u_max) * 6 + 1
            self.canvas.create_oval(px - r, py - r, px + r, py + r, fill=self.config.ACCENT_BLUE, outline="")

    def render(self):
        w, h = 480, 240
        self.draw_axes(60, 60, w, h, "Petri Net Dynamics")
        self.plot_series(60, 60, w, h, self.core.logic, self.config.ACCENT_BLUE, "Logic")
        self.plot_series(60, 60, w, h, self.core.aesthetic, self.config.ACCENT_PINK, "Aesthetic")
        self.draw_axes(610, 60, w, h, "Emergent Understanding")
        self.plot_series(610, 60, w, h, self.core.understanding, self.config.ACCENT_GREEN, "Understanding", fill=True)
        self.draw_axes(60, 340, w, h, "Utility Optimization")
        self.plot_series(60, 340, w, h, self.core.utility, self.config.ACCENT_GREEN, "Utility")
        self.draw_heatmap(610, 340, w, h * 2)
        self.draw_phase_space(60, 620, w, h)

# ---------------- Main Execution ----------------
if __name__ == "__main__":
    config = Config()
    model = LLMCore(config)
    Dashboard(model)
