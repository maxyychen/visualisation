"""
Monthly Returns Heatmap (Calendar Table)  -  family: Finance & investment

DESIGN PURPOSE
A year × month grid in which every cell is one month's return, colored on a
diverging scale centered at zero, with the full-year return in a separate
column. It is the standard compact view in fund factsheets: you can read exact
numbers and also spot streaks, seasonality and bad years at a glance.

WHEN TO USE
  - Summarise a multi-year monthly track record on one page
  - Look for streaks of losses, seasonality or a change in behavior after a
    given date
  - Give readers exact monthly figures alongside the pattern

AVOID WHEN
  - Fewer than about two years of history (use a bar chart of monthly returns)
  - Comparing two funds (use annual returns bars or a difference heatmap)

ALTERNATIVES
  - Annual returns bar chart
  - Column chart of monthly returns
  - Distribution of monthly returns (histogram)

EXAMPLE
Simulated monthly returns for a fund, 2015–2024 (compounded from daily
returns). Not investment advice.

NOTE: Educational examples with simulated or historical data. Not investment
advice; past performance does not predict future returns.

Run:  python monthly_returns_heatmap.py
      python monthly_returns_heatmap.py --real-data   (real dataset: plotly.express.data.stocks() — MSFT weekly prices resampled to month-end, 2018–2019)
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

from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

# --- Example data ------------------------------------------------------------
rng = np.random.default_rng(21)
dates = pd.bdate_range("2015-01-01", "2024-12-31")
n = len(dates)
r = 0.00045 + rng.standard_t(4, n) * 0.0095 / np.sqrt(2)
r[(dates >= "2020-02-20") & (dates <= "2020-03-23")] -= 0.012
r[(dates >= "2022-01-01") & (dates <= "2022-10-15")] -= 0.0011
daily = pd.Series(r, index=dates)
monthly = (1 + daily).resample("ME").prod() - 1   # simple monthly returns
name = "Fund"
monthly.tail()

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.stocks() — MSFT weekly prices resampled to month-end, 2018–2019
    import plotly.express as px
    stocks = px.data.stocks().set_index("date")
    px_m = pd.Series(stocks["MSFT"].values, index=pd.to_datetime(stocks.index)).resample("ME").last()
    monthly = px_m.pct_change().dropna()
    name = "MSFT"
    monthly.tail()

# --- Plot --------------------------------------------------------------------
table = pd.DataFrame({"year": monthly.index.year, "month": monthly.index.month, "r": monthly.values})
grid = table.pivot(index="year", columns="month", values="r").reindex(columns=range(1, 13))
annual = table.groupby("year")["r"].apply(lambda x: (1 + x).prod() - 1)

cmap = LinearSegmentedColormap.from_list("loss_gain", ["#b3471c", "#eb6834", "#f2f1ee", "#2a78d6", "#1c5cab"])
lim = np.nanmax(np.abs(grid.values))
fig, (ax, axy) = plt.subplots(1, 2, figsize=(11, 0.5 * len(grid) + 1.6), sharey=True,
                              gridspec_kw={"width_ratios": [12, 1.4], "wspace": 0.04})
ax.imshow(grid.values, cmap=cmap, norm=TwoSlopeNorm(0, -lim, lim), aspect="auto")
alim = np.abs(annual.values).max()
axy.imshow(annual.values[:, None], cmap=cmap, norm=TwoSlopeNorm(0, -alim, alim), aspect="auto")

def label(axis, values, scale):
    for (i, j), v in np.ndenumerate(values):
        if not np.isnan(v):
            axis.text(j, i, f"{v:+.1%}", ha="center", va="center", fontsize=8,
                      color="white" if abs(v) > 0.6 * scale else "#0b0b0b")

label(ax, grid.values, lim)
label(axy, annual.values[:, None], alim)
ax.set_xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
ax.set_yticks(range(len(grid)), grid.index)
axy.set_xticks([0], ["Year"])
for a in (ax, axy):
    a.grid(False)
    a.tick_params(length=0)
    for s in a.spines.values():
        s.set_visible(False)
    a.xaxis.tick_top()
ax.set_title(f"{name}: monthly returns", pad=28)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
