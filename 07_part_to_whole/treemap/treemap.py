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
A $268M equity portfolio, holdings grouped into four sectors.

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
             "Oil Major", "Utility Co"],
    "value_m": [58, 44, 30, 26, 14, 22, 12, 6, 18, 15, 11, 7, 5],
}).sort_values(["division", "value_m"], ascending=[True, False])
df

# --- Plot --------------------------------------------------------------------
divisions = ["Technology", "Financials", "Healthcare", "Energy"]
cmap = dict(zip(divisions, PALETTE))
df = df.sort_values("value_m", ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
labels = [f"{d}\n${v}M" if v >= 10 else "" for d, v in zip(df["holding"], df["value_m"])]
squarify.plot(sizes=df["value_m"], label=labels, color=[cmap[d] for d in df["division"]],
              ax=ax, pad=False, edgecolor="#fcfcfb", linewidth=2,
              text_kwargs=dict(color="white", fontsize=9.5, fontweight="bold"))
ax.axis("off")
handles = [plt.Rectangle((0, 0), 1, 1, color=cmap[d]) for d in divisions]
ax.legend(handles, divisions, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.01))
ax.set_title(f"Equity portfolio by sector and holding (total ${df['value_m'].sum()}M)")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
