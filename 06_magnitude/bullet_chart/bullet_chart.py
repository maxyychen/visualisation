"""
Bullet Chart  -  family: Magnitude

DESIGN PURPOSE
Stephen Few's compact replacement for gauges. A bar shows the actual value, a
tick marks the target, and shaded bands mark qualitative ranges (poor, ok,
good), all in a small strip.

WHEN TO USE
  - Show KPI performance against target and qualitative thresholds in
    dashboards
  - Fit many metrics into little space (stack them vertically)

AVOID WHEN
  - There is no target or benchmark
  - The audience is unfamiliar with it and has no legend to explain it

ALTERNATIVES
  - KPI stat tile
  - Bar with reference line

EXAMPLE
Five quarterly KPIs versus target, each with poor/satisfactory/good ranges.

Run:  python bullet_chart.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Library style: categorical colors in fixed order, recessive axes, hairline grid.
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
           "#e87ba4", "#008300", "#6250d6", "#e34948"]
SEQ_CMAP = "Blues"      # sequential: one hue, light -> dark
DIV_CMAP = "RdBu_r"     # diverging: two opposite hues, neutral midpoint
GRAY = "#b8b7b1"        # de-emphasised marks
plt.rcParams.update({
    "figure.figsize": (8, 4.8), "figure.dpi": 110, "figure.facecolor": "#fcfcfb",
    "axes.facecolor": "#fcfcfb", "axes.edgecolor": "#c9c8c3", "axes.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#e6e5e1", "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.prop_cycle": plt.cycler(color=PALETTE),
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.labelcolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#52514e",
    "text.color": "#0b0b0b", "font.size": 10, "lines.linewidth": 2,
    "legend.frameon": False,
})

# --- Example data ------------------------------------------------------------
df = pd.DataFrame([
    ("Revenue ($M)", 270, 250, [150, 225, 300]),
    ("Profit (%)", 22.5, 26, [20, 25, 30]),
    ("Avg. order ($)", 320, 550, [350, 500, 600]),
    ("New customers", 1650, 2100, [1400, 2000, 2500]),
    ("Satisfaction (1–5)", 4.5, 4.2, [3.5, 4.25, 5]),
], columns=["kpi", "actual", "target", "ranges"])
df

# --- Plot --------------------------------------------------------------------
fig, axes = plt.subplots(len(df), 1, figsize=(8, 4.5))
band_colors = ["#d6d5d0", "#e6e5e1", "#f3f2ef"]
for ax, (_, r) in zip(axes, df.iterrows()):
    prev = 0
    for upper, c in zip(r["ranges"], band_colors):
        ax.barh(0, upper - prev, left=prev, color=c, height=1)
        prev = upper
    ax.barh(0, r["actual"], color=PALETTE[0] if r["actual"] >= r["target"] else PALETTE[1],
            height=0.35)
    ax.vlines(r["target"], -0.35, 0.35, color="#0b0b0b", linewidth=2.5)
    ax.set_xlim(0, r["ranges"][-1])
    ax.set_yticks([0], [r["kpi"]])
    ax.grid(False)
    ax.tick_params(axis="x", labelsize=8)
    for s in ["left", "bottom"]:
        ax.spines[s].set_visible(False)
fig.suptitle("KPI scorecard (bar = actual, tick = target; orange = below target)",
             x=0.02, ha="left", fontweight="bold")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
