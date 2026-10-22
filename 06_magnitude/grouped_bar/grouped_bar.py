"""
Grouped (Clustered) Bar Chart  -  family: Magnitude

DESIGN PURPOSE
Places bars for several sub-groups side by side within each category. Sub-
groups can be compared within a category, and the same sub-group across
categories.

WHEN TO USE
  - Compare 2–4 sub-groups across a handful of categories (sales by region and
    year)
  - Individual values matter more than the category total

AVOID WHEN
  - There are more than ~4 sub-groups or ~8 categories (it becomes a barcode;
    use small multiples)
  - The total of each category is the main point (use stacked bars)

ALTERNATIVES
  - Dumbbell chart (2 sub-groups)
  - Small-multiple bar charts
  - Stacked bar

EXAMPLE
Sales by region for three consecutive years (illustrative data).

Run:  python grouped_bar.py
      python grouped_bar.py --real-data   (real dataset: plotly.express.data.medals_long() — 2018 Winter Olympics short-track medal counts, bundled with plotly)

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
df = pd.DataFrame({
    "region": ["North", "South", "East", "West", "Central"],
    "2022": [42, 35, 28, 50, 22],
    "2023": [48, 33, 34, 55, 25],
    "2024": [55, 31, 41, 57, 30],
}).set_index("region")
labels = dict(y="Sales ($M)", legend="Year", title="Sales by region and year")
df

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.medals_long() — 2018 Winter Olympics short-track medal counts, bundled with plotly
    import plotly.express as px
    m = px.data.medals_long()
    df = (m.pivot(index="nation", columns="medal", values="count")[["gold", "silver", "bronze"]]
            .rename(columns=str.title).rename_axis(index=None, columns=None))
    labels = dict(y="Medals", legend=None, title="2018 Winter Olympics short-track medals")
    df

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.8))
n = len(df.columns)
width = 0.8 / n
x = np.arange(len(df))
for i, col in enumerate(df.columns):
    ax.bar(x + (i - (n - 1) / 2) * width, df[col], width=width * 0.92,
           color=PALETTE[i], label=col)
ax.set_xticks(x, df.index)
ax.set_ylabel(labels["y"])
ax.grid(axis="x", visible=False)
ax.legend(title=labels["legend"], ncol=n, loc="upper left")
ax.set_ylim(0, df.values.max() * 1.3)
ax.set_title(labels["title"])
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
