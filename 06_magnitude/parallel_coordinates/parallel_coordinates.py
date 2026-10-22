"""
Parallel Coordinates  -  family: Magnitude

DESIGN PURPOSE
Each variable gets a vertical axis and each observation is a line crossing
every axis. Patterns, clusters and trade-offs across many dimensions become
visible.

WHEN TO USE
  - Explore multivariate data (4–12 numeric variables) for clusters and trade-
    offs
  - Compare groups on many attributes at once
  - Use interactive filtering (brushing) of high-dimensional records

AVOID WHEN
  - General audiences (the chart takes explanation)
  - Thousands of lines would overplot (sample, aggregate, or use alpha)

ALTERNATIVES
  - Radar chart (few entities)
  - Scatterplot matrix
  - Heatmap

EXAMPLE
Specs of 60 cars from three classes (synthetic): engine size, power, weight,
mpg, price.

Run:  python parallel_coordinates.py
      python parallel_coordinates.py --real-data   (real dataset: plotly.express.data.iris() — Fisher's (1936) iris measurements, bundled with plotly)

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
rng = np.random.default_rng(10)
classes = {"Compact": (1.4, 110, 1250, 42, 22), "SUV": (2.5, 200, 1900, 28, 45),
           "Sports": (3.5, 380, 1500, 22, 90)}
rows = []
for cls, (eng, hp, kg, mpg, price) in classes.items():
    for _ in range(20):
        rows.append([cls, eng * rng.normal(1, .12), hp * rng.normal(1, .12),
                     kg * rng.normal(1, .07), mpg * rng.normal(1, .1), price * rng.normal(1, .15)])
df = pd.DataFrame(rows, columns=["class", "Engine (L)", "Power (hp)", "Weight (kg)",
                                 "MPG", "Price ($k)"])
title = "Car classes across five specifications"
df.head()

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.iris() — Fisher's (1936) iris measurements, bundled with plotly
    import plotly.express as px
    iris = px.data.iris()
    df = pd.DataFrame({"class": iris["species"],
                       "Sepal length (cm)": iris["sepal_length"], "Sepal width (cm)": iris["sepal_width"],
                       "Petal length (cm)": iris["petal_length"], "Petal width (cm)": iris["petal_width"]})
    title = "Iris species across four measurements (Fisher, 1936)"
    df.head()

# --- Plot --------------------------------------------------------------------
cols = df.columns[1:]
norm = (df[cols] - df[cols].min()) / (df[cols].max() - df[cols].min())
fig, ax = plt.subplots(figsize=(10, 5))
for i, (cls, g) in enumerate(norm.groupby(df["class"])):
    for _, row in g.iterrows():
        ax.plot(range(len(cols)), row.values, color=PALETTE[i], alpha=0.45, linewidth=1)
    ax.plot([], [], color=PALETTE[i], label=cls, linewidth=2)
for j, c in enumerate(cols):
    ax.axvline(j, color="#8c8b86", linewidth=1)
    ax.text(j, 1.03, f"{df[c].max():.3g}", ha="center", fontsize=8, color="#52514e")
    ax.text(j, -0.06, f"{df[c].min():.3g}", ha="center", fontsize=8, color="#52514e")
ax.set_xticks(range(len(cols)), cols)
ax.set_yticks([])
ax.grid(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_visible(False)
ax.set_ylim(-0.1, 1.08)
ax.legend(loc="upper center", ncol=3, bbox_to_anchor=(0.5, -0.08))
ax.set_title(title)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
