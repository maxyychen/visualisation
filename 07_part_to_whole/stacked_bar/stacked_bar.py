"""
Stacked Bar Chart  -  family: Part-to-whole

DESIGN PURPOSE
Each bar is a total, divided into segments for its components. It shows the
total and its composition at once. The first segment and the total are easy to
compare across bars. Inner segments are harder to compare because they have no
common baseline.

WHEN TO USE
  - Compare totals across categories and show roughly what makes them up
  - Use few components (2–5), where the first segment is the most important
  - Show composition of counts or amounts, not percentages

AVOID WHEN
  - Readers must compare the middle segments precisely (use grouped bars or
    small multiples)
  - There are more than ~5 components
  - Only the shares matter, not the totals (use a 100% stacked bar)

ALTERNATIVES
  - Grouped bar chart
  - 100% stacked bar
  - Small-multiple bars

EXAMPLE
Quarterly revenue of a software company, split by sales channel.

Run:  python stacked_bar.py

The notebook also shows this chart built with: plotly, altair.
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
quarters = ["Q1", "Q2", "Q3", "Q4"]
df = pd.DataFrame({
    "Direct sales": [3200, 3500, 3350, 3800],
    "Partners":     [5400, 5600, 5900, 6100],
    "Online":       [1200, 1500, 1900, 2300],
}, index=quarters)
df

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
bottom = np.zeros(len(df))
for i, col in enumerate(df.columns):
    ax.bar(df.index, df[col], bottom=bottom, color=PALETTE[i], label=col,
           width=0.6, edgecolor="#fcfcfb", linewidth=2)
    bottom += df[col].values
for x, total in enumerate(bottom):
    ax.text(x, total + 150, f"${total / 1000:.1f}M", ha="center", fontsize=9, color="#52514e")
ax.set_ylabel("Revenue ($k)")
ax.set_title("Revenue by quarter and sales channel")
ax.grid(axis="x", visible=False)
ax.set_ylim(0, bottom.max() * 1.12)
ax.legend(ncol=3, loc="upper left")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
