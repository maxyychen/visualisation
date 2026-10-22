"""
Rolling Return, Volatility and Sharpe  -  family: Finance & investment

DESIGN PURPOSE
Three stacked panels sharing one time axis: trailing 12-month return,
annualised volatility and Sharpe ratio, each for the fund and its benchmark. A
single full-period number hides regime changes; rolling windows show whether
performance and risk were stable or came from one lucky stretch.

WHEN TO USE
  - Check whether a strategy's edge is persistent or concentrated in one
    period
  - Show how risk (volatility) changes across market regimes
  - Monitor a live fund against its benchmark over time

AVOID WHEN
  - Histories shorter than about three window lengths (the lines are mostly
    noise)
  - Mixing metrics with different units on a dual y-axis (use stacked panels,
    as here)

ALTERNATIVES
  - Full-period metrics table
  - Rolling excess return only
  - Monthly returns heatmap

EXAMPLE
Simulated daily returns of a fund and benchmark, 2015–2024, with a
252-trading-day window and a 2% risk-free rate. Simple returns; volatility =
std × √252. Not investment advice.

NOTE: Educational examples with simulated or historical data. Not investment
advice; past performance does not predict future returns.

Run:  python rolling_metrics.py
      python rolling_metrics.py --real-data   (real dataset: plotly.express.data.stocks() — weekly AMZN vs an equal-weight 6-stock tech basket, 2018–2019, 26-week window)
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

from matplotlib.ticker import PercentFormatter

# --- Example data ------------------------------------------------------------
rng = np.random.default_rng(21)
dates = pd.bdate_range("2015-01-01", "2024-12-31")
n = len(dates)
mkt = 0.00045 + rng.standard_t(4, n) * 0.0095 / np.sqrt(2)
mkt[(dates >= "2020-02-20") & (dates <= "2020-03-23")] -= 0.012
mkt[(dates >= "2022-01-01") & (dates <= "2022-10-15")] -= 0.0011
fund = 0.00024 + 0.9 * mkt + rng.normal(0, 0.004, n)
rets = pd.DataFrame({"Fund": fund, "Benchmark": mkt}, index=dates)  # simple daily returns
freq, window, rf = 252, 252, 0.02   # obs/year, rolling window, annual risk-free rate
rets.head()

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.stocks() — weekly AMZN vs an equal-weight 6-stock tech basket, 2018–2019, 26-week window
    import plotly.express as px
    stocks = px.data.stocks().set_index("date")
    stocks.index = pd.to_datetime(stocks.index)
    weekly = stocks.pct_change().dropna()
    rets = pd.DataFrame({"AMZN": weekly["AMZN"], "Tech basket": weekly.mean(axis=1)})
    freq, window, rf = 52, 26, 0.02
    rets.head()

# --- Plot --------------------------------------------------------------------
roll_ret = (1 + rets).rolling(window).apply(np.prod, raw=True) ** (freq / window) - 1
roll_vol = rets.rolling(window).std() * np.sqrt(freq)
roll_sharpe = (rets.rolling(window).mean() * freq - rf) / roll_vol
fund_name, bench_name = rets.columns[:2]

fig, axes = plt.subplots(3, 1, figsize=(9, 7.5), sharex=True)
panels = [(roll_ret, "Return (annualised)", True), (roll_vol, "Volatility (annualised)", True),
          (roll_sharpe, "Sharpe ratio", False)]
for ax, (data, label, pct) in zip(axes, panels):
    ax.plot(data.index, data[bench_name], color=GRAY, linewidth=1.5, label=bench_name)
    ax.plot(data.index, data[fund_name], color=PALETTE[0], linewidth=1.8, label=fund_name)
    if label != "Volatility (annualised)":
        ax.axhline(0, color="#52514e", linewidth=0.9)
    if pct:
        ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_ylabel(label)
axes[0].set_title(f"Rolling {window}-period metrics: {fund_name} vs. {bench_name}")
axes[0].legend(loc="upper left", ncol=2)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
