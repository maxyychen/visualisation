"""
Monte Carlo Retirement Projection  -  family: Finance & investment

DESIGN PURPOSE
Simulates thousands of possible market paths for a portfolio with withdrawals,
then shows the spread of outcomes as a percentile fan and the probability that
the money lasts to each age. It replaces a single misleading 'expected' line
with a range and a probability.

WHEN TO USE
  - Retirement or endowment planning with regular withdrawals
  - Communicate the risk of running out of money rather than an average
    outcome
  - Compare plans (spending levels, allocations) by their probability of
    success

AVOID WHEN
  - Presenting the median path as a forecast
  - Hiding the return and inflation assumptions; results are only as good as
    these inputs
  - Drawing all simulated paths (spaghetti); show percentile bands and a few
    sample paths

ALTERNATIVES
  - Fan chart
  - Table of success probabilities by spending level

EXAMPLE
$1.5M at age 60, $70k/year inflation-adjusted withdrawals, real returns ~4.5%
± 11% a year, 5,000 simulated paths (illustrative; not financial advice).

NOTE: Educational examples with simulated or historical data. Not investment
advice; past performance does not predict future returns.

Run:  python monte_carlo_wealth.py
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
rng = np.random.default_rng(2025)
n_paths, years = 5000, 35
start_age, start_wealth, spending = 60, 1_500_000, 70_000      # real (today's) dollars
mu, sigma = 0.045, 0.11                                         # real annual return, volatility
log_ret = rng.normal(np.log1p(mu) - sigma ** 2 / 2, sigma, (n_paths, years))

wealth = np.empty((n_paths, years + 1))
wealth[:, 0] = start_wealth
for t in range(years):                       # withdraw at the start of each year, then grow
    wealth[:, t + 1] = np.maximum((wealth[:, t] - spending) * np.exp(log_ret[:, t]), 0)
ages = start_age + np.arange(years + 1)
bands = pd.DataFrame(np.percentile(wealth, [10, 25, 50, 75, 90], axis=0).T / 1e6, index=ages,
                     columns=["p10", "p25", "p50", "p75", "p90"])
p_lasting = pd.Series((wealth > 0).mean(axis=0), index=ages)
bands.iloc[::5].round(2)

# --- Plot --------------------------------------------------------------------
fig, (ax, axp) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [2, 1]})
for path in wealth[rng.choice(n_paths, 30, replace=False)]:
    ax.plot(ages, path / 1e6, color="#b8b7b1", linewidth=0.6, alpha=0.6)
ax.fill_between(ages, bands["p10"], bands["p90"], color="#b7d3f6", linewidth=0, label="10th–90th percentile")
ax.fill_between(ages, bands["p25"], bands["p75"], color="#6da7ec", linewidth=0, label="25th–75th percentile")
ax.plot(ages, bands["p50"], color="#104281", linewidth=2.4, label="Median")
ax.axhline(0, color="#52514e", linewidth=0.8)
ax.set_xlabel("Age")
ax.set_ylabel("Portfolio value ($M, today's dollars)")
ax.set_title("Range of outcomes (5,000 simulations)")
ax.legend(loc="upper left")

axp.plot(ages, p_lasting * 100, color=PALETTE[0], linewidth=2.4)
p95 = p_lasting.loc[95]
axp.scatter(95, p95 * 100, s=60, color=PALETTE[0], edgecolor="#fcfcfb", linewidth=2, zorder=3)
axp.annotate(f"{p95:.0%} chance the money\nlasts to age 95", (95, p95 * 100), xytext=(-10, -40),
             textcoords="offset points", ha="right", fontsize=9.5, fontweight="bold")
axp.set_ylim(0, 105)
axp.set_xlabel("Age")
axp.set_ylabel("Paths with money left (%)")
axp.set_title("Probability of success")
fig.suptitle(r"Retirement plan: \$1.5M at 60, spending \$70k/yr (illustrative)", x=0.01, ha="left",
             fontsize=13, fontweight="bold")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
