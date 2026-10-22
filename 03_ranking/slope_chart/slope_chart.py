"""
Slope Chart  -  family: Ranking

DESIGN PURPOSE
Joins each item's value at two points in time (or two conditions) with a
straight line. The slope shows the direction and size of change, and crossing
lines show changes in rank.

WHEN TO USE
  - Compare rankings or values between exactly two time points or conditions
  - Highlight which items rose and which fell

AVOID WHEN
  - There are more than two time points (use a bump or line chart)
  - There are too many items, so lines and labels collide (~15 max)

ALTERNATIVES
  - Dumbbell chart
  - Bump chart
  - Grouped bar chart

EXAMPLE
Market share (%) of 8 smartphone brands in 2019 vs. 2024 (synthetic).

Run:  python slope_chart.py
      python slope_chart.py --real-data   (real dataset: plotly.express.data.gapminder() — Gapminder life expectancy, GDP and population 1952–2007, bundled with plotly)

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
brands = ["Atlas", "Borealis", "Cirrus", "Delta", "Echo", "Flux", "Gamma", "Helix"]
y2019 = [21.0, 18.5, 14.0, 11.0, 9.5, 8.0, 6.0, 4.5]
y2024 = [19.5, 12.0, 17.5, 6.5, 13.5, 8.5, 9.5, 3.5]
df = pd.DataFrame({"brand": brands, "2019": y2019, "2024": y2024})
start, end = "2019", "2024"
title = "Smartphone market share (%), 2019 → 2024"
df["change"] = df[end] - df[start]
df

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.gapminder() — Gapminder life expectancy, GDP and population 1952–2007, bundled with plotly
    import plotly.express as px
    countries = ["Japan", "China", "Iraq", "India", "Zimbabwe", "Nigeria"]
    gm = px.data.gapminder().query("year in [1987, 2007] and country in @countries")
    df = (gm.pivot(index="country", columns="year", values="lifeExp")
            .rename(columns=str).rename_axis(columns=None).reset_index().rename(columns={"country": "brand"}))
    start, end = "1987", "2007"
    title = "Life expectancy (years), 1987 → 2007"
    df["change"] = df[end] - df[start]
    df

# --- Plot --------------------------------------------------------------------
from matplotlib import patheffects
fig, ax = plt.subplots(figsize=(6.5, 6.5))
for _, r in df.iterrows():
    color = PALETTE[0] if r["change"] > 0 else PALETTE[1] if r["change"] < -2 else GRAY
    ax.plot([0, 1], [r[start], r[end]], color=color, marker="o", markersize=7,
            markeredgecolor="#fcfcfb", markeredgewidth=1.5)
    ax.text(-0.04, r[start], f"{r['brand']} {r[start]:.1f}", ha="right", va="center", fontsize=9)
    ax.text(1.04, r[end], f"{r[end]:.1f} {r['brand']}", ha="left", va="center", fontsize=9)
ax.set_xlim(-0.55, 1.55)
ax.set_xticks([0, 1], [start, end], fontsize=11, weight="bold")
ax.yaxis.set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_visible(False)
ax.grid(False)
ax.set_title(title)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
