"""
Venn Diagram  -  family: Part-to-whole

DESIGN PURPOSE
Overlapping circles that show how two or three sets share members. Each region
is labeled with its count, so readers see the size of every combination,
including what is unique and what is shared.

WHEN TO USE
  - Show overlap between 2–3 groups (customers holding products A, B, C)
  - Compare gene lists, customer segments, or feature sets

AVOID WHEN
  - There are more than 3 sets (use an UpSet plot)
  - Exact area proportionality is expected (it is only approximate for 3 sets)

ALTERNATIVES
  - UpSet plot
  - Euler diagram
  - Grouped bar of intersections

EXAMPLE
Product holdings of 1,000 retail-bank customers (simulated): checking account,
credit card, brokerage account.

Run:  python venn_diagram.py
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

from matplotlib_venn import venn3

# --- Example data ------------------------------------------------------------
# region sizes in the order: (100, 010, 110, 001, 101, 011, 111)
subsets = {"Checking only": 210, "Card only": 90, "Checking∩Card": 70, "Brokerage only": 160,
           "Checking∩Brokerage": 95, "Card∩Brokerage": 55, "All three": 40}
subsets

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 6))
v = venn3(subsets=tuple(subsets.values()),
          set_labels=("Checking", "Credit card", "Brokerage"),
          set_colors=PALETTE[:3], alpha=0.55, ax=ax)
for patch in v.patches:
    if patch is not None:
        patch.set_edgecolor("#fcfcfb")
        patch.set_linewidth(2)
for t in v.subset_labels:
    if t is not None:
        t.set_fontsize(10)
n_none = 1000 - sum(subsets.values())        # customers holding none of the three
ax.set_title(f"Which bank products do customers hold? (n = 1,000; {n_none} hold none)")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
