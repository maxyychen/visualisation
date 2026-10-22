"""
Stress-Test Tornado Chart  -  family: Finance & investment

DESIGN PURPOSE
For each risk factor, a horizontal bar runs from the portfolio's P&L under a
downside shock to its P&L under an upside shock. Bars are sorted by total
range, so the widest (most important) sensitivities sit at the top and the
chart narrows like a tornado. It ranks which assumptions matter most.

WHEN TO USE
  - Rank the sensitivity of a portfolio, valuation or budget to individual
    assumptions
  - Communicate scenario or stress-test results to non-specialists
  - Decide which inputs deserve more research or hedging

AVOID WHEN
  - Factors interact strongly (one-at-a-time shocks mislead; use joint
    scenarios)
  - Shocks are not comparable in likelihood (state the shock size for each
    bar)

ALTERNATIVES
  - Scenario table with joint shocks
  - DCF / two-way sensitivity table
  - Waterfall from base case to stressed case

EXAMPLE
Simulated one-at-a-time shocks to a $100 million multi-asset portfolio (P&L in
millions). Not investment advice.

NOTE: Educational examples with simulated or historical data. Not investment
advice; past performance does not predict future returns.

Run:  python stress_test_tornado.py
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
df = pd.DataFrame({
    "factor":   ["Equity markets", "Interest rates", "Credit spreads", "USD exchange rate",
                 "Oil price", "Inflation", "Equity volatility", "Real estate"],
    "down_shock": ["−20%", "+100 bp", "+150 bp", "USD +10%", "−30%", "+2 pp", "VIX +15", "−15%"],
    "up_shock":   ["+20%", "−100 bp", "−75 bp", "USD −10%", "+30%", "−1 pp", "VIX −5", "+15%"],
    "down_pnl": [-11.8, -4.6, -3.9, -2.4, -1.1, -1.6, -2.9, -1.4],   # P&L, $ millions
    "up_pnl":   [10.9, 4.1, 1.8, 2.2, 0.9, 0.7, 0.8, 1.3],
})
df["range"] = df["up_pnl"] - df["down_pnl"]
df = df.sort_values("range").reset_index(drop=True)
df

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
y = np.arange(len(df))
ax.barh(y, df["down_pnl"], color=PALETTE[1], height=0.65, label="Downside shock")
ax.barh(y, df["up_pnl"], color=PALETTE[0], height=0.65, label="Upside shock")
for yi, row in df.iterrows():
    ax.text(row["down_pnl"] - 0.25, yi, f"{row['down_shock']}  {row['down_pnl']:+.1f}", ha="right",
            va="center", fontsize=8.5, color="#52514e")
    ax.text(row["up_pnl"] + 0.25, yi, f"{row['up_pnl']:+.1f}  {row['up_shock']}", ha="left",
            va="center", fontsize=8.5, color="#52514e")
ax.axvline(0, color="#52514e", linewidth=1)
ax.set_yticks(y, df["factor"])
lim = df[["down_pnl", "up_pnl"]].abs().max().max() * 1.55
ax.set_xlim(-lim, lim)
ax.set_xlabel("Portfolio P&L vs. base case ($ millions)")
ax.set_title("Stress test: which shocks move the portfolio most")
ax.grid(axis="y", visible=False)
ax.legend(loc="lower right")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
