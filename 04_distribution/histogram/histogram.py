"""
Histogram  -  family: Distribution

DESIGN PURPOSE
Bins one numeric variable into intervals and draws a bar for the count in
each. It is the standard way to see a distribution's shape, centre, spread,
skew and gaps.

WHEN TO USE
  - Show the shape of one numeric variable (normal, skewed, bimodal)
  - Find outliers, gaps and impossible values during data cleaning
  - Communicate a distribution to a general audience

AVOID WHEN
  - There are fewer than ~30 values (use a strip or dot plot)
  - Comparing more than two or three groups (overlapping bars become
    unreadable)

ALTERNATIVES
  - KDE density curve
  - Box plot
  - ECDF

EXAMPLE
Delivery times (minutes) for 2,000 food orders, right-skewed (synthetic).

Run:  python histogram.py

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
rng = np.random.default_rng(5)
df = pd.DataFrame({"minutes": rng.gamma(4.5, 7, 2000) + 8})
df["minutes"].describe().round(1)

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.8))
ax.hist(df["minutes"], bins=40, color=PALETTE[0], edgecolor="#fcfcfb", linewidth=0.8)
med = df["minutes"].median()
ax.axvline(med, color="#0b0b0b", linewidth=1.2)
ax.text(med + 1, ax.get_ylim()[1] * 0.92, f"median {med:.0f} min", fontsize=9)
ax.set_xlabel("Delivery time (minutes)")
ax.set_ylabel("Orders")
ax.set_title("Distribution of delivery times")
ax.grid(axis="x", visible=False)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
