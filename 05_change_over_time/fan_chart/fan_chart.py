"""
Fan Chart (forecast uncertainty)  -  family: Change over time

DESIGN PURPOSE
Shows observed history followed by a forecast drawn as nested bands of
uncertainty that widen over time. It shows the best guess together with honest
uncertainty about it.

WHEN TO USE
  - Show forecasts or projections with confidence or prediction intervals
  - Show that uncertainty grows with the forecast horizon
  - Present model outputs to decision-makers (inflation, demand, epidemics)

AVOID WHEN
  - The intervals have no statistical basis (they would imply false precision)
  - The audience will read the central line as a promise

ALTERNATIVES
  - Line with a single confidence band
  - Spaghetti plot of scenarios

EXAMPLE
Monthly demand (synthetic): 4 years of history plus a 12-month forecast with
50/80/95% intervals.

Run:  python fan_chart.py
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
rng = np.random.default_rng(9)
hist_dates = pd.date_range("2021-01", periods=48, freq="MS")
hist = 200 + 2 * np.arange(48) + 15 * np.sin(np.arange(48) * 2 * np.pi / 12) + rng.normal(0, 6, 48)
fc_dates = pd.date_range(hist_dates[-1], periods=13, freq="MS")
h = np.arange(13)
center = hist[-1] + 2 * h + 15 * (np.sin((48 + h - 1) * 2 * np.pi / 12) - np.sin(47 * 2 * np.pi / 12))
sd = 4.2 * np.sqrt(h)          # zero at the last observation, growing with the horizon
bands = {lvl: (center - stats.norm.ppf(0.5 + lvl / 2) * sd, center + stats.norm.ppf(0.5 + lvl / 2) * sd)
         for lvl in (0.5, 0.8, 0.95)}
forecast = pd.DataFrame({"date": fc_dates, "center": center, "sd": sd})
forecast.head()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(hist_dates, hist, color="#0b0b0b", linewidth=1.5, label="Observed")
for lvl, alpha in [(0.95, 0.15), (0.8, 0.25), (0.5, 0.4)]:
    lo, hi = bands[lvl]
    ax.fill_between(fc_dates, lo, hi, color=PALETTE[0], alpha=alpha, linewidth=0,
                    label=f"{int(lvl * 100)}% interval")
ax.plot(fc_dates, center, color=PALETTE[0], linewidth=2, label="Forecast")
ax.axvline(hist_dates[-1], color="#52514e", linewidth=1)
ax.text(hist_dates[-1], ax.get_ylim()[1], "  forecast →", va="top", color="#52514e")
ax.set_ylabel("Units (k)")
ax.set_title("Monthly demand with 12-month forecast")
ax.legend(loc="upper left", ncol=2)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
