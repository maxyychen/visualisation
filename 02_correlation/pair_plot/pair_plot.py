"""
Pair Plot (Scatter-plot Matrix)  -  family: Correlation

DESIGN PURPOSE
A grid of scatter plots for every pair of variables, with each variable's
distribution on the diagonal. It is a standard first look at a multivariate
dataset.

WHEN TO USE
  - Explore relationships among 3–6 numeric variables at once
  - Check how well groups separate across features (classification problems)
  - Find non-linear relationships that a correlation matrix would miss

AVOID WHEN
  - There are more than ~6 variables (the panels get tiny)
  - The audience is non-technical (too dense for presentation)

ALTERNATIVES
  - Correlation heatmap
  - Parallel coordinates

EXAMPLE
Four flower measurements for three species (synthetic, iris-like).

Run:  python pair_plot.py
      python pair_plot.py --real-data   (real dataset: plotly.express.data.iris() — Fisher's (1936) iris measurements, bundled with plotly)

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
rng = np.random.default_rng(21)
means = {"setosa": [5.0, 3.4, 1.5, 0.25], "versicolor": [5.9, 2.8, 4.3, 1.3],
         "virginica": [6.6, 3.0, 5.6, 2.0]}
sds = [0.35, 0.33, 0.3, 0.15]
rows = []
for sp, mu in means.items():
    x = rng.normal(mu, sds, (50, 4))
    rows.append(pd.DataFrame(x, columns=["sepal_length", "sepal_width",
                                         "petal_length", "petal_width"]).assign(species=sp))
df = pd.concat(rows, ignore_index=True)
df.head()

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.iris() — Fisher's (1936) iris measurements, bundled with plotly
    import plotly.express as px
    df = px.data.iris()[["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]]
    df.head()

# --- Plot --------------------------------------------------------------------
import seaborn as sns
g = sns.pairplot(df, hue="species", palette=PALETTE[:3], height=2, corner=True,
                 plot_kws=dict(s=18, alpha=0.7, edgecolor="#fcfcfb", linewidth=0.4),
                 diag_kws=dict(fill=True, alpha=0.35, linewidth=1.2))
g.figure.suptitle("Flower measurements by species", x=0.02, ha="left", weight="bold")
fig = g.figure

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
