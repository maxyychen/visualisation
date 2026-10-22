"""
Joint Plot (Scatter + Marginals)  -  family: Correlation

DESIGN PURPOSE
A scatter plot with the marginal distribution of each variable drawn along its
axis. The joint relationship and both individual distributions show together.

WHEN TO USE
  - Show both the relationship and each variable's skew or outliers
  - Explore two key variables in detail

AVOID WHEN
  - There are more than two or three groups (marginals get crowded)
  - Space is tight (dashboard tiles)

ALTERNATIVES
  - Scatter plot
  - Hexbin with marginal histograms

EXAMPLE
House size vs. sale price for 400 homes (synthetic, right-skewed prices).

Run:  python joint_plot.py
      python joint_plot.py --real-data   (real dataset: plotly.express.data.gapminder() — Gapminder 2007, bundled with plotly)

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
rng = np.random.default_rng(17)
size = rng.gamma(9, 18, 400)                                 # m²
price = np.exp(10.8 + 0.0062 * size + rng.normal(0, 0.22, 400)) / 1000   # $k
df = pd.DataFrame({"size_m2": size, "price_k": price})
x, y = "size_m2", "price_k"
labels = dict(x="Living area (m²)", y="Sale price ($k)", title="House size vs. price")
df.describe().round(0)

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.gapminder() — Gapminder 2007, bundled with plotly
    import plotly.express as px
    df = px.data.gapminder().query("year == 2007")
    x, y = "gdpPercap", "lifeExp"
    labels = dict(x="GDP per capita (USD)", y="Life expectancy (years)",
                  title="Income vs. life expectancy, 142 countries (2007)")
    df[[x, y]].describe().round(0)

# --- Plot --------------------------------------------------------------------
import seaborn as sns
g = sns.jointplot(data=df, x=x, y=y, height=6, color=PALETTE[0],
                  joint_kws=dict(s=22, alpha=0.6, edgecolor="#fcfcfb", linewidth=0.5),
                  marginal_kws=dict(bins=30, edgecolor="#fcfcfb", linewidth=0.5))
g.set_axis_labels(labels["x"], labels["y"])
g.figure.suptitle(labels["title"], x=0.02, ha="left", weight="bold")
g.figure.tight_layout()
fig = g.figure

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
