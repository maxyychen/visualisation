"""
Highlight Table (heat-shaded table)  -  family: Magnitude

DESIGN PURPOSE
A table of numbers with each cell shaded by its value. Readers can look up
exact values and still see high and low cells at a glance, which makes it a
bridge between a table and a heatmap.

WHEN TO USE
  - Readers need exact numbers and patterns (finance reports, cross-tabs)
  - Compare values across two categorical dimensions (product × month)

AVOID WHEN
  - The table is huge (use a pure heatmap)
  - Rows have very different scales (shade per row or normalise first)

ALTERNATIVES
  - Heatmap
  - Grouped bar chart

EXAMPLE
Units sold by product and month.

Run:  python highlight_table.py
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
rng = np.random.default_rng(23)
products = ["Laptops", "Tablets", "Phones", "Monitors", "Headsets", "Keyboards"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
base = np.array([120, 80, 300, 90, 150, 60])[:, None]
season = np.array([0.9, 0.85, 1.0, 1.05, 1.1, 1.25])[None, :]
df = pd.DataFrame((base * season * rng.uniform(0.85, 1.15, (6, 6))).round().astype(int),
                  index=products, columns=months)
df

# --- Plot --------------------------------------------------------------------
import seaborn as sns
fig, ax = plt.subplots(figsize=(8, 4.5))
sns.heatmap(df, annot=True, fmt="d", cmap=SEQ_CMAP, linewidths=2, linecolor="#fcfcfb",
            cbar_kws={"label": "Units sold", "shrink": 0.8}, ax=ax, annot_kws={"fontsize": 10})
ax.set_xlabel(""); ax.set_ylabel("")
ax.tick_params(length=0)
ax.set_title("Units sold by product and month")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
