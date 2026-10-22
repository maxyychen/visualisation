"""
ACF & PACF (Autocorrelation Plots)  -  family: Change over time

DESIGN PURPOSE
Shows how strongly a time series is correlated with its own past. The
autocorrelation function (ACF) shows the correlation at each lag; the partial
autocorrelation function (PACF) shows each lag's correlation after removing
the effect of shorter lags. Bars outside the confidence band reveal memory and
seasonality, and their pattern suggests which ARIMA-type model fits.

WHEN TO USE
  - Check for seasonality and its period (spikes at lags 7, 12, 52…)
  - Choose AR and MA orders before fitting a forecasting model
  - Test whether model residuals are white noise (no bars should cross the
    band)

AVOID WHEN
  - The series has a strong trend (difference or detrend it first, or every
    lag looks significant)
  - The audience is non-technical (show the seasonal pattern directly instead)

ALTERNATIVES
  - Seasonal cycle plot
  - STL decomposition
  - Lag scatter plot (y_t vs. y_t−k)

EXAMPLE
365 days of simulated website sessions (detrended): an AR(1) process with a
weekly pattern, as traffic dips every weekend.

Run:  python acf_pacf.py
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

from statsmodels.tsa.stattools import acf, pacf

# --- Example data ------------------------------------------------------------
rng = np.random.default_rng(9)
n = 365
dates = pd.date_range("2024-01-01", periods=n, freq="D")
weekly = np.array([0.4, 0.5, 0.5, 0.45, 0.3, -1.1, -1.05])      # Mon..Sun effect
x = np.zeros(n)
for t in range(1, n):
    x[t] = 0.55 * x[t - 1] + rng.normal(0, 0.6)
series = pd.Series(x + weekly[dates.dayofweek], index=dates, name="sessions (std. units)")
nlags = 28
series.head(8).round(2)

# --- Plot --------------------------------------------------------------------
fig = plt.figure(figsize=(11, 6.4))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.15], hspace=0.45, wspace=0.15)
ax0 = fig.add_subplot(gs[0, :])
ax0.plot(series.index, series, color=PALETTE[0], linewidth=1)
ax0.axhline(0, color="#52514e", linewidth=0.8)
ax0.set_title("The series: daily website sessions, detrended (simulated)", fontsize=11)

for k, (name, fn) in enumerate([("ACF: autocorrelation", acf), ("PACF: partial autocorrelation", pacf)]):
    ax = fig.add_subplot(gs[1, k], sharey=None)
    vals, ci = (fn(series, nlags=nlags, alpha=0.05) if fn is pacf
                else fn(series, nlags=nlags, alpha=0.05, fft=True))
    lags = np.arange(len(vals))
    band = ci[:, 1] - vals
    ax.fill_between(lags[1:], -band[1:], band[1:], color="#e4eefb", step="mid", linewidth=0,
                    label="95% band (no correlation)")
    ax.vlines(lags[1:], 0, vals[1:], color=PALETTE[0], linewidth=2)
    ax.scatter(lags[1:], vals[1:], color=PALETTE[0], s=14, zorder=3)
    ax.axhline(0, color="#52514e", linewidth=0.8)
    for s in (7, 14, 21, 28):
        ax.axvline(s, color="#e6e5e1", linewidth=3, zorder=0)
    ax.set_xticks([1, 7, 14, 21, 28])
    ax.set_xlabel("Lag (days)")
    ax.set_ylim(-0.6, 1)
    ax.set_title(name, fontsize=11)
    if k == 0:
        ax.legend(loc="upper right", fontsize=8)
fig.suptitle("Autocorrelation reveals memory and a weekly cycle", x=0.06, ha="left",
             fontsize=14, fontweight="bold")

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
