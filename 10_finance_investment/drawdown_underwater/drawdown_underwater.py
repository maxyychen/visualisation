"""
Drawdown (Underwater) Chart  -  family: Finance & investment

DESIGN PURPOSE
Plots, for every date, how far an investment sits below its previous peak. The
area hangs "underwater" from a zero line, so the depth, length and frequency
of losses become visible. A cumulative-return chart hides these, because
recoveries quickly paint over the dips.

WHEN TO USE
  - Show the pain an investor would have experienced, not just the end result
  - Compare maximum drawdown and time-to-recovery between strategies
  - Pair with a cumulative-return chart in a performance report

AVOID WHEN
  - The series never falls meaningfully below its peak (the chart is empty)
  - Very short histories, where one dip dominates

ALTERNATIVES
  - Cumulative return chart with peaks marked
  - Table of the five worst drawdowns (depth, start, trough, recovery)

EXAMPLE
Simulated daily prices for a fund, 2015–2024, with a sharp 2020-style crash
and a slower 2022-style bear market. Not investment advice.

NOTE: Educational examples with simulated or historical data. Not investment
advice; past performance does not predict future returns.

Run:  python drawdown_underwater.py
      python drawdown_underwater.py --real-data   (real dataset: plotly.express.data.stocks() — weekly NFLX, 2018–2019)
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

from matplotlib.ticker import PercentFormatter, LogLocator, FuncFormatter

# --- Example data ------------------------------------------------------------
rng = np.random.default_rng(21)
dates = pd.bdate_range("2015-01-01", "2024-12-31")
n = len(dates)
r = 0.00045 + rng.standard_t(4, n) * 0.0095 / np.sqrt(2)
r[(dates >= "2020-02-20") & (dates <= "2020-03-23")] -= 0.012
r[(dates >= "2022-01-01") & (dates <= "2022-10-15")] -= 0.0011
price = pd.Series(100 * np.cumprod(1 + r), index=dates, name="Fund")
price.tail()

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.stocks() — weekly NFLX, 2018–2019
    import plotly.express as px
    stocks = px.data.stocks().set_index("date")
    price = pd.Series(100 * stocks["NFLX"].values, index=pd.to_datetime(stocks.index), name="NFLX")
    price.tail()

# --- Plot --------------------------------------------------------------------
drawdown = price / price.cummax() - 1
trough = drawdown.idxmin()
peak = price.loc[:trough].idxmax()
recovered = price.loc[trough:][price.loc[trough:] >= price.loc[peak]]
recovery = recovered.index[0] if len(recovered) else None

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True,
                               gridspec_kw={"height_ratios": [1.3, 1]})
ax1.plot(price.index, price, color=PALETTE[0])
ax1.set_yscale("log")
ax1.yaxis.set_major_locator(LogLocator(base=10, subs=[1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 7]))
ax1.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax1.yaxis.set_minor_formatter(FuncFormatter(lambda v, _: ""))
ax1.set_ylabel("Price (log scale)")
ax1.set_title(f"{price.name}: price and drawdown from previous peak")
ax1.axvspan(peak, recovery or price.index[-1], color=PALETTE[1], alpha=0.08, linewidth=0)

ax2.fill_between(drawdown.index, drawdown, 0, color=PALETTE[1], alpha=0.85, linewidth=0)
ax2.axhline(0, color="#52514e", linewidth=1)
ax2.yaxis.set_major_formatter(PercentFormatter(1.0))
ax2.set_ylabel("Drawdown")
rec_text = f"recovered {recovery:%b %Y}" if recovery is not None else "not yet recovered"
ax2.annotate(f"Max drawdown {drawdown.min():.1%}\npeak {peak:%b %Y} → trough {trough:%b %Y}, {rec_text}",
             (trough, drawdown.min()), xytext=(14, 4), textcoords="offset points", fontsize=9,
             va="bottom", color="#0b0b0b")
ax2.set_ylim(drawdown.min() * 1.25, 0.02)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
