"""
Correlation Matrix Heatmap  -  family: Correlation

DESIGN PURPOSE
A grid that colors each cell by the correlation coefficient between a pair of
variables. Strong positive and negative relationships across many variables
stand out in one view.

WHEN TO USE
  - Screen many numeric variables for pairwise relationships
  - Spot multicollinearity before regression modelling
  - Summarise a feature set in a report

AVOID WHEN
  - Relationships are non-linear (Pearson r can miss them; check scatter
    plots)
  - There are more than ~25 variables (cluster or filter first)

ALTERNATIVES
  - Pair plot
  - Clustered heatmap with dendrogram

EXAMPLE
Correlations between the monthly returns of eight asset classes over 15 years
(synthetic, factor-model data).

Run:  python correlation_heatmap.py
      python correlation_heatmap.py --real-data   (real dataset: plotly.express.data.stocks() — weekly prices of six large US tech stocks, 2018–2019, bundled with plotly)

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
n = 180  # months
equity, rates, infl = rng.normal(0, 1, (3, n))  # common risk factors
assets = {
    "US equities":   0.9 * equity + 0.3 * rng.normal(size=n),
    "Intl equities": 0.8 * equity + 0.5 * rng.normal(size=n),
    "EM equities":   0.7 * equity + 0.7 * rng.normal(size=n),
    "REITs":         0.6 * equity - 0.3 * rates + 0.6 * rng.normal(size=n),
    "High yield":    0.5 * equity - 0.2 * rates + 0.6 * rng.normal(size=n),
    "US Treasuries": -0.3 * equity - 0.9 * rates + 0.3 * rng.normal(size=n),
    "Gold":          -0.1 * equity + 0.5 * infl + 0.8 * rng.normal(size=n),
    "Commodities":   0.3 * equity + 0.7 * infl + 0.6 * rng.normal(size=n),
}
df = pd.DataFrame(assets)
title = "Correlation of monthly returns across asset classes"
corr = df.corr().round(2)
corr

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.stocks() — weekly prices of six large US tech stocks, 2018–2019, bundled with plotly
    import plotly.express as px
    prices = px.data.stocks().set_index("date")
    df = prices.pct_change().dropna()          # weekly returns
    df.columns = [c.upper() for c in df.columns]
    title = "Correlation of weekly returns, six tech stocks (2018-2019)"
    corr = df.corr().round(2)
    corr

# --- Plot --------------------------------------------------------------------
import seaborn as sns
mask = np.triu(np.ones_like(corr, dtype=bool))
# drop the all-masked first row / last column of the lower triangle
tri, tri_mask = corr.iloc[1:, :-1], mask[1:, :-1]
fig, ax = plt.subplots(figsize=(7.5, 6.2))
sns.heatmap(tri, mask=tri_mask, cmap=DIV_CMAP, vmin=-1, vmax=1, center=0, annot=True,
            fmt=".2f", annot_kws=dict(size=9), linewidths=2, linecolor="#fcfcfb",
            square=True, cbar_kws=dict(shrink=0.75, label="Pearson r"), ax=ax)
ax.grid(False)
ax.set_title(title)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
