"""
Scatter with Regression Line  -  family: Correlation

DESIGN PURPOSE
A scatter plot with a fitted trend line and its confidence band. The fit
summarises the relationship, the band shows how certain the estimate is, and
the raw points stay visible as evidence.

WHEN TO USE
  - Show the direction and strength of a roughly linear relationship
  - Report a correlation coefficient or slope alongside the data
  - Show model fit and the uncertainty around it

AVOID WHEN
  - The relationship is clearly non-linear (use LOWESS or a polynomial fit)
  - Readers might read the trend line as proof of causation
  - Outliers dominate the fit (check robust alternatives first)

ALTERNATIVES
  - LOWESS-smoothed scatter
  - Joint plot
  - Residual plot

EXAMPLE
Weekly advertising spend vs. sales for 80 weeks, with an OLS fit and 95%
confidence band.

Run:  python scatter_regression.py
      python scatter_regression.py --real-data   (real dataset: plotly.express.data.tips() — 244 restaurant bills and tips (Bryant & Smith 1995), bundled with plotly)

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
from scipy import stats
rng = np.random.default_rng(1)
spend = rng.uniform(5, 50, 80)
sales = 120 + 6.2 * spend + rng.normal(0, 40, 80)
df = pd.DataFrame({"ad_spend_k": spend, "sales_k": sales})
x, y = "ad_spend_k", "sales_k"
labels = dict(x="Advertising spend ($k / week)", y="Sales ($k / week)", title="Sales rise with advertising spend")
fit = stats.linregress(df[x], df[y])
print(f"slope={fit.slope:.2f}  r={fit.rvalue:.2f}  p={fit.pvalue:.1e}")

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.tips() — 244 restaurant bills and tips (Bryant & Smith 1995), bundled with plotly
    from scipy import stats
    import plotly.express as px
    df = px.data.tips()
    x, y = "total_bill", "tip"
    labels = dict(x="Total bill ($)", y="Tip ($)",
                  title="Tips rise with the size of the bill (244 restaurant bills)")
    fit = stats.linregress(df[x], df[y])
    print(f"slope={fit.slope:.2f}  r={fit.rvalue:.2f}  p={fit.pvalue:.1e}")

# --- Plot --------------------------------------------------------------------
import seaborn as sns
fig, ax = plt.subplots(figsize=(7.5, 5))
sns.regplot(data=df, x=x, y=y, ax=ax, ci=95, seed=0,
            scatter_kws=dict(s=30, alpha=0.6, color=PALETTE[0], edgecolor="#fcfcfb"),
            line_kws=dict(color=PALETTE[1], linewidth=2))
ax.text(0.03, 0.95, f"r = {fit.rvalue:.2f}\nn = {len(df)}", transform=ax.transAxes,
        va="top", fontsize=10, color="#52514e")
ax.set_xlabel(labels["x"])
ax.set_ylabel(labels["y"])
ax.set_title(labels["title"])
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
