"""
Waffle Chart  -  family: Part-to-whole

DESIGN PURPOSE
A 10 × 10 grid of squares, each worth 1% (or one unit). Squares are colored by
category. Counting squares is more accurate than judging angles, and the 'n
out of 100' framing is easy for any audience.

WHEN TO USE
  - Communicate a few percentages to a general audience ('23 in every 100
    customers')
  - A pie-chart alternative that supports more accurate reading
  - Show progress toward a goal

AVOID WHEN
  - Values need precision finer than 1%
  - There are more than ~5 categories

ALTERNATIVES
  - Pie chart
  - Single 100% stacked bar
  - Pictogram (isotype)

EXAMPLE
How a typical household's financial assets are split, per $100 (illustrative).

Run:  python waffle_chart.py
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
s = pd.Series({"Cash & deposits": 40, "Stocks & funds": 45, "Bonds & other": 15})
assert s.sum() == 100
s

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5.6))
cells = np.repeat(np.arange(len(s)), s.values)
for k, cat in enumerate(cells):
    col, row = k // 10, k % 10          # fill column by column, bottom to top
    ax.add_patch(plt.Rectangle((col, row), 0.88, 0.88, color=PALETTE[cat]))
ax.set_xlim(-0.2, 10)
ax.set_ylim(-0.2, 10)
ax.set_aspect("equal")
ax.axis("off")
handles = [plt.Rectangle((0, 0), 1, 1, color=PALETTE[i]) for i in range(len(s))]
ax.legend(handles, [f"{k}: ${v}" for k, v in s.items()], loc="center left",
          bbox_to_anchor=(1.0, 0.5), fontsize=10)
ax.set_title("Household financial assets, per $100")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
