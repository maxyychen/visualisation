"""
Scatter Plot  -  family: Correlation

DESIGN PURPOSE
Each observation is a dot placed by two numeric variables. It is the basic
chart for relationships: the direction, strength, shape (linear or curved),
clusters and outliers all show at once.

WHEN TO USE
  - Show whether two numeric variables move together
  - Find clusters, gaps and outliers in two-dimensional data
  - Explore data before fitting a model

AVOID WHEN
  - There are tens of thousands of points and heavy overplotting (use hexbin
    or 2-D density)
  - One variable is time (use a line chart)
  - Readers need exact values (use a table)

ALTERNATIVES
  - Hexbin plot
  - 2-D density contour
  - Bubble chart (adds a third variable)

EXAMPLE
Height and weight of 300 adults, split by sex (synthetic data).

Run:  python scatter.py
      python scatter.py --real-data   (real dataset: plotly.express.data.tips() — restaurant tipping data (Bryant & Smith 1995), bundled with plotly)

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
rng = np.random.default_rng(42)
n = 150
height_f = rng.normal(163, 6.5, n)
height_m = rng.normal(177, 7, n)
df = pd.DataFrame({
    "height_cm": np.r_[height_f, height_m],
    "weight_kg": np.r_[0.62 * height_f - 40 + rng.normal(0, 6, n),
                       0.75 * height_m - 55 + rng.normal(0, 7, n)],
    "sex": ["Female"] * n + ["Male"] * n,
})
x, y, hue = "height_cm", "weight_kg", "sex"
labels = dict(x="Height (cm)", y="Weight (kg)", title="Height vs. weight of 300 adults")
df.head()

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.tips() — restaurant tipping data (Bryant & Smith 1995), bundled with plotly
    import plotly.express as px
    df = px.data.tips()                     # 244 restaurant bills (Bryant & Smith, 1995)
    x, y, hue = "total_bill", "tip", "sex"
    labels = dict(x="Total bill ($)", y="Tip ($)", title="Tip vs. bill size, 244 restaurant bills")
    df.head()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 5.5))
for color, (name, g) in zip(PALETTE, df.groupby(hue)):
    ax.scatter(g[x], g[y], s=28, alpha=0.65, color=color,
               edgecolor="#fcfcfb", linewidth=0.6, label=name)
ax.set_xlabel(labels["x"])
ax.set_ylabel(labels["y"])
ax.set_title(labels["title"])
ax.legend(title=None, loc="upper left")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
