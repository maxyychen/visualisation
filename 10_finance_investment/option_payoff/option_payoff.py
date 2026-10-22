"""
Option Payoff Diagrams  -  family: Finance & investment

DESIGN PURPOSE
Plots profit or loss at expiry against the underlying price for an option
strategy, with the premium paid or received included. Small multiples put
several strategies side by side, so their risk profiles (capped, unlimited,
range-bound) can be compared.

WHEN TO USE
  - Explain or compare option strategies (directional, hedging, volatility,
    income)
  - Show breakeven prices, maximum gain and maximum loss
  - Check a proposed structure before trading it

AVOID WHEN
  - Showing value before expiry (that needs a pricing model and
    time/volatility assumptions; plot Black–Scholes value curves instead)
  - Mixing strategies with very different scales on one shared y-axis

ALTERNATIVES
  - P&L table at selected prices
  - Value-before-expiry curves for several dates

EXAMPLE
Stock at $100. Premiums from Black–Scholes with 25% volatility, 3 months to
expiry and a 4% rate (illustrative; financing of the premium ignored).

NOTE: Educational examples with simulated or historical data. Not investment
advice; past performance does not predict future returns.

Run:  python option_payoff.py
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

from scipy.stats import norm

# --- Example data ------------------------------------------------------------
S0, T, r, sigma = 100.0, 0.25, 0.04, 0.25


def black_scholes(S, K, T, r, sigma, kind):
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if kind == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


ST = np.linspace(60, 140, 801)                       # price at expiry


def leg(kind, K, qty):                               # qty: +1 long, -1 short
    premium = black_scholes(S0, K, T, r, sigma, kind)
    payoff = np.maximum(ST - K, 0) if kind == "call" else np.maximum(K - ST, 0)
    return qty * (payoff - premium)


strategies = pd.DataFrame({
    "Long call (K=100)": leg("call", 100, 1),
    "Protective put (stock + put K=95)": (ST - S0) + leg("put", 95, 1),
    "Long straddle (call + put, K=100)": leg("call", 100, 1) + leg("put", 100, 1),
    "Iron condor (85/95/105/115)": leg("put", 85, 1) + leg("put", 95, -1) + leg("call", 105, -1) + leg("call", 115, 1),
}, index=pd.Index(ST, name="price_at_expiry"))
strategies.iloc[::100].round(2)

# --- Plot --------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(10.5, 7), sharex=True)
for ax, (name, pnl) in zip(axes.flat, strategies.items()):
    x, y = pnl.index.to_numpy(), pnl.to_numpy()
    ax.fill_between(x, y, 0, where=y >= 0, color=PALETTE[0], alpha=0.25, linewidth=0, interpolate=True)
    ax.fill_between(x, y, 0, where=y < 0, color=PALETTE[1], alpha=0.25, linewidth=0, interpolate=True)
    ax.plot(x, y, color="#0b0b0b", linewidth=1.8)
    ax.axhline(0, color="#52514e", linewidth=0.8)
    ax.axvline(S0, color="#a9a8a2", linewidth=1)
    cross = np.flatnonzero(np.diff(np.sign(y)) != 0)
    for i in cross:                                   # linear interpolation of breakevens
        be = x[i] - y[i] * (x[i + 1] - x[i]) / (y[i + 1] - y[i])
        ax.scatter(be, 0, s=36, color="#0b0b0b", zorder=3)
        ax.annotate(f"{be:.1f}", (be, 0), xytext=(0, -14), textcoords="offset points",
                    ha="center", fontsize=8.5, color="#0b0b0b",
                    bbox=dict(boxstyle="round,pad=0.15", fc="#fcfcfb", ec="none"))
    ax.set_title(name, fontsize=10.5)
    ax.grid(axis="x", visible=False)
for ax in axes[1]:
    ax.set_xlabel("Underlying price at expiry ($)")
for ax in axes[:, 0]:
    ax.set_ylabel("Profit / loss per share ($)")
fig.suptitle("Option strategies: profit at expiry (spot $100 = gray line; dots = breakevens)",
             x=0.01, ha="left", fontsize=13, fontweight="bold")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
