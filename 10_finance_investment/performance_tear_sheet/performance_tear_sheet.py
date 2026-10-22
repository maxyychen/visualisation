"""
Performance Tear Sheet (one-page report)  -  family: Finance & investment

DESIGN PURPOSE
A one-page report that combines the charts and statistics an investor checks
first: headline metrics, growth of $1 against a benchmark, drawdowns, rolling
risk, a monthly-returns calendar and calendar-year returns. Return, risk and
consistency read together, so no single flattering number tells the story
alone.

WHEN TO USE
  - Summarise a fund, strategy, or portfolio's track record on one page
  - Compare a strategy with its benchmark across return, risk and consistency
  - Produce a repeatable monthly or quarterly performance report from a price
    file

AVOID WHEN
  - The history is short (under ~2 years); rolling and calendar panels become
    noise
  - The audience needs one message (show the single relevant chart instead)
  - Returns are not time-weighted (cash flows distort them; compute TWR first)

ALTERNATIVES
  - Cumulative return vs. benchmark (just the growth line)
  - Drawdown (underwater) chart
  - Monthly returns heatmap

EXAMPLE
Simulated daily returns for a fund and its benchmark index over seven years,
including a sharp crash and a slow bear market. The report comes from the
reusable `vizlib.finance.tear_sheet()` function.

NOTE: Educational examples with simulated or historical data. Not investment
advice; past performance does not predict future returns.

Run:  python performance_tear_sheet.py
      python performance_tear_sheet.py --real-data   (real dataset: plotly.express.data.stocks (weekly prices 2018–2019, AAPL vs. equal-weight of six tech stocks))
"""
import sys
from pathlib import Path

# This example uses the reusable vizlib package from this repository
# (or `pip install -e .` at the repo root).
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

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

from vizlib.finance import tear_sheet, summary_stats

# --- Example data ------------------------------------------------------------
rng = np.random.default_rng(41)
dates = pd.bdate_range("2018-01-01", "2024-12-31")
n = len(dates)
# Market: calm drift, a sharp crash (~day 560) and a slow bear market (~day 1200).
market = rng.standard_t(4, n) * 0.007 + 0.0005
market[555:575] -= 0.010
market[1180:1380] -= 0.0008
# Fund: beta 0.85 to the market plus a small, noisy alpha.
fund = 0.85 * market + rng.normal(0.00012, 0.004, n)
returns = pd.Series(fund, index=dates, name="Fund")
benchmark = pd.Series(market, index=dates, name="Index")
title = "Global Equity Fund: performance report (simulated)"
summary_stats(returns, benchmark).style.format("{:.3f}")

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.stocks (weekly prices 2018–2019, AAPL vs. equal-weight of six tech stocks)
    import plotly.express as px

    stocks = px.data.stocks().assign(date=lambda d: pd.to_datetime(d["date"])).set_index("date")
    returns = stocks["AAPL"].pct_change().dropna().rename("AAPL")
    benchmark = stocks.pct_change().dropna().mean(axis=1).rename("Equal-weight tech")
    title = "AAPL vs. equal-weight big tech, weekly 2018–2019"
    summary_stats(returns, benchmark).style.format("{:.3f}")

# --- Plot --------------------------------------------------------------------
fig = tear_sheet(returns, benchmark, title=title, rf=0.02)

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
