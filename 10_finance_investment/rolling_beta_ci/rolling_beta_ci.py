"""
Rolling Beta with Confidence Band  -  family: Finance & investment

DESIGN PURPOSE
Estimates a stock's or fund's beta to the market over a moving window with a
rolling regression, and draws a 95% confidence band around each estimate.
Market exposure is not fixed, and a one-year estimate is noisy. The band shows
which wiggles are real shifts in exposure and which are estimation error.

WHEN TO USE
  - Monitor whether a fund's market exposure is drifting from its mandate
  - Check if a stock became more or less defensive after a business change
  - Show why a single "beta = 1.2" number can mislead

AVOID WHEN
  - The window is too short for the return frequency (wide bands, little
    information)
  - The relationship is clearly non-linear (options-like payoffs); beta
    summarises it poorly

ALTERNATIVES
  - Rolling correlation
  - Scatter of stock vs. market returns for two sub-periods

EXAMPLE
Simulated daily returns for a stock whose true beta moves from 0.8 to 1.4 and
back to about 1.0, regressed on market returns over a rolling 252-day window
with statsmodels RollingOLS. The real-data variant uses weekly 2018–2019
prices with a 52-week window. Not investment advice.

NOTE: Educational examples with simulated or historical data. Not investment
advice; past performance does not predict future returns.

Run:  python rolling_beta_ci.py
      python rolling_beta_ci.py --real-data   (real dataset: plotly.express.data.stocks (weekly 2018–2019; AAPL vs. equal-weight of six tech stocks))
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

from statsmodels.regression.rolling import RollingOLS
import statsmodels.api as sm

# --- Example data ------------------------------------------------------------
rng = np.random.default_rng(17)
dates = pd.bdate_range("2016-01-01", "2024-12-31")
n = len(dates)
true_beta = pd.Series(np.interp(np.arange(n), [0, 700, 1400, 1800, n - 1], [0.8, 0.8, 1.4, 1.0, 1.0]), index=dates)
market = rng.normal(0.0004, 0.010, n)
stock = 0.0001 + true_beta.values * market + rng.normal(0, 0.012, n)
rets = pd.DataFrame({"stock": stock, "market": market}, index=dates)
window = 252
label = "Stock"
title = "Rolling 1-year beta: market exposure is not constant (simulated)"
rets.head()

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.stocks (weekly 2018–2019; AAPL vs. equal-weight of six tech stocks)
    import plotly.express as px

    stocks = px.data.stocks().assign(date=lambda d: pd.to_datetime(d["date"])).set_index("date")
    weekly = stocks.pct_change().dropna()
    rets = pd.DataFrame({"stock": weekly["AAPL"], "market": weekly.mean(axis=1)})
    window = 52
    label = "AAPL"
    true_beta = None
    title = "AAPL rolling 52-week beta vs. equal-weight big tech"
    rets.head()

# --- Plot --------------------------------------------------------------------
res = RollingOLS(rets["stock"], sm.add_constant(rets["market"]), window=window).fit()
beta = res.params["market"]
se = res.bse["market"]
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.fill_between(beta.index, beta - 1.96 * se, beta + 1.96 * se, color=PALETTE[0], alpha=0.2,
                linewidth=0, label="95% confidence band")
ax.plot(beta.index, beta, color=PALETTE[0], label=f"{label}: estimated beta")
if true_beta is not None:
    ax.plot(true_beta.index, true_beta, color="#8f8e88", linewidth=1, label="True beta (simulation)")
ax.axhline(1, color="#52514e", linewidth=0.9)
ax.text(beta.dropna().index[0], 1.01, "β = 1 (moves with the market)", fontsize=8, color="#52514e", va="bottom")
ax.set_ylabel(f"Beta ({window}-period window)")
ax.set_title(title)
ax.legend(loc="upper left", fontsize=9)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
