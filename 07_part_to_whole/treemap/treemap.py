"""
Treemap  -  family: Part-to-whole

DESIGN PURPOSE
Nested rectangles whose areas are proportional to values. It fits a large
number of parts (and optionally a hierarchy) into a small space, and the
biggest contributors stand out.

WHEN TO USE
  - Show part-to-whole with many categories (10–50+) where a pie would fail
  - Show hierarchical data (sector → company), coloring by the parent
  - Find the dominant contributors in a long tail

AVOID WHEN
  - Precise comparison of similar values is needed (areas are hard to compare)
  - Values can be negative
  - There are very few categories (use a bar chart)

ALTERNATIVES
  - Sunburst (hierarchy)
  - Bar chart
  - Icicle chart

EXAMPLE
A $268M equity portfolio (fictional holdings), grouped into four sectors.

Run:  python treemap.py

The notebook also shows this chart built with: plotly.
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

import squarify

# --- Example data ------------------------------------------------------------
df = pd.DataFrame({
    "division": ["Technology"] * 5 + ["Financials"] * 3 + ["Healthcare"] * 3 + ["Energy"] * 2,
    "holding": ["Software Co", "Chipmaker", "Cloud Co", "Hardware Co", "Payments Co",
             "Big Bank", "Insurer", "Asset Mgr",
             "Pharma Co", "MedTech Co", "Biotech Co",
             "Oil Major", "Pipeline Co"],
    "value_m": [58, 44, 30, 26, 14, 22, 12, 6, 18, 15, 11, 7, 5],
}).sort_values(["division", "value_m"], ascending=[True, False])
df

# --- Plot --------------------------------------------------------------------
divisions = ["Technology", "Financials", "Healthcare", "Energy"]
cmap = dict(zip(divisions, PALETTE))
W, H = 100, 60
totals = df.groupby("division")["value_m"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
# level 1: one rectangle per sector; level 2: holdings squarified inside their sector
sector_rects = squarify.squarify(squarify.normalize_sizes(totals.values, W, H), 0, 0, W, H)
for div, sr in zip(totals.index, sector_rects):
    g = df[df["division"] == div].sort_values("value_m", ascending=False)
    rects = squarify.squarify(squarify.normalize_sizes(g["value_m"].values, sr["dx"], sr["dy"]),
                              sr["x"], sr["y"], sr["dx"], sr["dy"])
    for (_, row), r in zip(g.iterrows(), rects):
        ax.add_patch(plt.Rectangle((r["x"], r["y"]), r["dx"], r["dy"], facecolor=cmap[div],
                                   edgecolor="#fcfcfb", linewidth=1.5))
        if row["value_m"] >= 10:
            ax.text(r["x"] + r["dx"] / 2, r["y"] + r["dy"] / 2, f"{row['holding']}\n${row['value_m']}M",
                    ha="center", va="center", color="white", fontsize=9.5, fontweight="bold")
    ax.add_patch(plt.Rectangle((sr["x"], sr["y"]), sr["dx"], sr["dy"], fill=False,
                               edgecolor="#fcfcfb", linewidth=5))   # thick gap between sectors
ax.set_xlim(0, W); ax.set_ylim(0, H)
ax.axis("off")
handles = [plt.Rectangle((0, 0), 1, 1, color=cmap[d]) for d in divisions]
ax.legend(handles, [f"{d} (${totals[d]}M)" for d in divisions], ncol=4, loc="upper center",
          bbox_to_anchor=(0.5, -0.01))
ax.set_title(f"Equity portfolio by sector and holding (total ${df['value_m'].sum()}M)")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
