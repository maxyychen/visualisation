"""
Stacked Area Chart  -  family: Change over time

DESIGN PURPOSE
Stacks several series on top of each other over time. The top edge shows the
total, and each band shows how much one component contributes.

WHEN TO USE
  - Show how a total changes over time and which components drive it
  - Show a few (2–6) parts with a meaningful sum (energy mix, revenue by
    segment)

AVOID WHEN
  - Readers need precise values for the middle layers (only the bottom layer
    has a flat baseline)
  - Components are not parts of a sum
  - There are many layers or layers that cross a lot

ALTERNATIVES
  - Small-multiple area charts
  - 100% stacked area (when shares matter more than totals)
  - Line chart

EXAMPLE
Electricity generation mix (TWh) by source over 20 years, synthetic data.

Run:  python stacked_area.py

The notebook also shows this chart built with: altair.
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
years = np.arange(2005, 2025)
t = years - 2005
df = pd.DataFrame({
    "Coal": 220 - 7.5 * t,
    "Gas": 110 + 3.0 * t,
    "Nuclear": np.full(len(t), 80.0) - 0.5 * t,
    "Wind": 2 + 0.25 * t ** 2,
    "Solar": 0.5 + 0.18 * t ** 2,
}, index=years).clip(lower=0)
df.tail()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
ax.stackplot(df.index, df.T.values, labels=df.columns, colors=PALETTE[:5],
             edgecolor="#fcfcfb", linewidth=1)
ax.set_xlim(df.index[0], df.index[-1])
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.set_ylabel("Generation (TWh)")
ax.set_title("Electricity generation by source")
ax.legend(loc="upper left", ncol=5, bbox_to_anchor=(0, -0.08))
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
