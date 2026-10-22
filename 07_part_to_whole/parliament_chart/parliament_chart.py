"""
Parliament (Semicircle) Chart  -  family: Part-to-whole

DESIGN PURPOSE
Seats drawn as dots arranged in semicircular rows and colored by party. Each
dot is a countable unit, so the chart shows composition and whether a majority
threshold is crossed.

WHEN TO USE
  - Show seat allocation in a legislature or committee
  - Show any whole made of discrete units where reaching a threshold (50%)
    matters

AVOID WHEN
  - The units are not discrete or the counts are very large (thousands)
  - There are many small parties (fold them into 'Other')

ALTERNATIVES
  - Waffle chart
  - Single stacked bar with a majority line

EXAMPLE
Seats in a 120-seat parliament after a (fictional) election.

Run:  python parliament_chart.py
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
seats = pd.Series({"Party A": 52, "Party B": 38, "Party C": 14, "Party D": 8, "Other": 8})
assert seats.sum() == 120
seats

# --- Plot --------------------------------------------------------------------
n_rows, total = 6, seats.sum()
radii = np.linspace(1.0, 2.0, n_rows)
per_row = np.round(radii / radii.sum() * total).astype(int)
per_row[-1] += total - per_row.sum()
pts = []
for r, n in zip(radii, per_row):
    for a in np.linspace(np.pi, 0, n):
        pts.append((a, r * np.cos(a), r * np.sin(a)))
pts.sort(key=lambda p: -p[0])           # fill left to right by angle
colors = PALETTE[:len(seats) - 1] + [GRAY]
seat_colors = np.repeat(colors, seats.values)
fig, ax = plt.subplots(figsize=(9, 5))
xs, ys = [p[1] for p in pts], [p[2] for p in pts]
ax.scatter(xs, ys, c=seat_colors, s=95, edgecolor="#fcfcfb", linewidth=1.5)
ax.text(0, 0.15, f"{total} seats\nmajority = {total // 2 + 1}", ha="center",
        fontsize=12, fontweight="bold")
ax.set_aspect("equal")
ax.axis("off")
handles = [plt.Line2D([], [], marker="o", ls="", color=c, markersize=9) for c in colors]
ax.legend(handles, [f"{k} ({v})" for k, v in seats.items()], ncol=5,
          loc="upper center", bbox_to_anchor=(0.5, 0.02))
ax.set_title("Parliament seat allocation")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
