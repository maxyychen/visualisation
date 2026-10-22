"""
Ordered Column Chart  -  family: Ranking

DESIGN PURPOSE
Vertical bars sorted by value. It works like the ordered bar chart, but suits
short labels and layouts that are wider than they are tall.

WHEN TO USE
  - Rank a handful of categories with short names
  - Fit a ranking into a wide slide or dashboard slot

AVOID WHEN
  - Labels are long (they must be rotated, so use horizontal bars)
  - The categories are time periods (keep them in time order instead of
    sorting by value)

ALTERNATIVES
  - Ordered bar chart
  - Lollipop chart

EXAMPLE
Number of medals won by the top 10 teams at a fictional games.

Run:  python ordered_column.py
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
teams = ["USA", "CHN", "JPN", "GBR", "AUS", "FRA", "NED", "KOR", "ITA", "GER"]
medals = [113, 91, 58, 65, 46, 64, 34, 32, 40, 33]
df = pd.DataFrame({"team": teams, "medals": medals}).sort_values("medals", ascending=False)
df

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 4.5))
ax.bar(df["team"], df["medals"], color=PALETTE[0], width=0.7)
for x, v in enumerate(df["medals"]):
    ax.text(x, v + 1.5, str(v), ha="center", fontsize=9, color="#52514e")
ax.set_ylabel("Total medals")
ax.set_title("Medal table: top 10 teams")
ax.grid(axis="x", visible=False)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
