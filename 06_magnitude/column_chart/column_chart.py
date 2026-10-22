"""
Column Chart (vertical bar)  -  family: Magnitude

DESIGN PURPOSE
Vertical bars whose heights encode values on a common zero baseline. Aligned
length is the most accurately read visual encoding, which makes this the
default for comparing amounts.

WHEN TO USE
  - Compare values across a small number (≤ 12) of categories with short
    labels
  - Show counts or amounts per time period (months, quarters)

AVOID WHEN
  - Category labels are long (use horizontal bars)
  - The baseline is not zero (bar length would lie)
  - The data is a continuous trend with many points (use a line)

ALTERNATIVES
  - Horizontal bar chart
  - Dot plot
  - Lollipop chart

EXAMPLE
Quarterly revenue for two years (illustrative data), highlighting the latest
quarter.

Run:  python column_chart.py
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
df = pd.DataFrame({
    "quarter": ["Q1 23", "Q2 23", "Q3 23", "Q4 23", "Q1 24", "Q2 24", "Q3 24", "Q4 24"],
    "revenue_m": [4.2, 4.8, 5.1, 6.3, 5.0, 5.6, 6.1, 7.4],
})
df

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))
colors = [PALETTE[0] if i == len(df) - 1 else "#9ec5f4" for i in range(len(df))]
bars = ax.bar(df["quarter"], df["revenue_m"], color=colors, width=0.65)
ax.bar_label(bars, fmt="$%.1fM", padding=3, fontsize=9, color="#52514e")
ax.set_ylabel("Revenue ($M)")
ax.set_ylim(0, df["revenue_m"].max() * 1.15)
ax.grid(axis="x", visible=False)
ax.set_title("Quarterly revenue: Q4 2024 is a record")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
