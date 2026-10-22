"""
Dumbbell Chart (connected dot plot)  -  family: Magnitude

DESIGN PURPOSE
Two dots per category joined by a line: before and after, or group A and group
B. The line's length shows the gap and its direction shows which value is
larger. It is far cleaner than paired bars.

WHEN TO USE
  - Compare two values per category (2015 vs. 2025, men vs. women, target vs.
    actual)
  - The size of the gap is the story
  - Values don't start at zero, so bars would be misleading

AVOID WHEN
  - There are more than two values per category (use a dot plot with several
    markers)

ALTERNATIVES
  - Grouped bar chart
  - Slope chart
  - Arrow chart

EXAMPLE
Life expectancy at birth in 2000 vs. 2022 for ten countries (approximate
values).

Run:  python dumbbell.py
      python dumbbell.py --real-data   (real dataset: plotly.express.data.gapminder() — Gapminder life expectancy, GDP and population 1952–2007, bundled with plotly)

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

# --- Example data ------------------------------------------------------------
df = pd.DataFrame({
    "country": ["Japan", "Taiwan", "Germany", "USA", "China", "Brazil",
                "India", "Russia", "South Africa", "Nigeria"],
    "y2000": [81.2, 76.5, 78.0, 76.8, 71.4, 70.1, 62.7, 65.3, 55.9, 46.3],
    "y2022": [84.0, 79.8, 80.7, 77.5, 78.6, 73.4, 67.7, 70.1, 61.5, 53.6],
})
start, end = "y2000", "y2022"
title = "Life expectancy rose everywhere, but gaps remain"
df["gain"] = df[end] - df[start]
df = df.sort_values(end).reset_index(drop=True)
df

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.gapminder() — Gapminder life expectancy, GDP and population 1952–2007, bundled with plotly
    import plotly.express as px
    countries = ["Japan", "Taiwan", "Germany", "United States", "China", "Brazil",
                 "India", "Bangladesh", "South Africa", "Zimbabwe"]
    gm = px.data.gapminder().query("year in [1982, 2007] and country in @countries")
    df = (gm.pivot(index="country", columns="year", values="lifeExp")
            .rename(columns=lambda yr: f"y{yr}").rename_axis(columns=None).reset_index())
    start, end = "y1982", "y2007"
    title = "Life expectancy 1982 → 2007: most gained, southern Africa fell back"
    df["gain"] = df[end] - df[start]
    df = df.sort_values(end).reset_index(drop=True)
    df

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5.5))
ax.hlines(df.index, df[start], df[end], color="#c9c8c3", linewidth=3)
ax.scatter(df[start], df.index, color=PALETTE[1], s=70, zorder=3, label=start[1:],
           edgecolor="#fcfcfb", linewidth=1.5)
ax.scatter(df[end], df.index, color=PALETTE[0], s=70, zorder=3, label=end[1:],
           edgecolor="#fcfcfb", linewidth=1.5)
for i, r in df.iterrows():
    ax.text(max(r[start], r[end]) + 0.7, i, f"{r['gain']:+.1f}", va="center", fontsize=8.5, color="#52514e")
ax.set_yticks(df.index, df["country"])
ax.set_xlabel("Life expectancy at birth (years)")
ax.grid(axis="y", visible=False)
ax.legend(loc="upper left", ncol=2)
ax.set_title(title)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
