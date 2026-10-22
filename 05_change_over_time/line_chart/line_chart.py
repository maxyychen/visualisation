"""
Line Chart  -  family: Change over time

DESIGN PURPOSE
The standard way to show a continuous series over time. Points joined by a
line put the reader's attention on the trend, its direction, speed and turning
points, more than on any single value.

WHEN TO USE
  - Show a trend in a continuous measure over regular time intervals
  - Compare a few series (up to ~4) on the same scale
  - Make peaks, troughs and turning points visible

AVOID WHEN
  - The data are discrete categories with no order (use a bar chart)
  - There are only 2–3 time points (use a slope chart or bars)
  - More than ~5 series would overlap into spaghetti (use small multiples or
    highlighting)

ALTERNATIVES
  - Highlighted line chart
  - Small-multiple lines
  - Area chart

EXAMPLE
Monthly active users of three apps over three years, synthetic data.

Run:  python line_chart.py
      python line_chart.py --real-data   (real dataset: plotly.express.data.stocks() — weekly closing prices of large tech stocks 2018–2019 (normalised), bundled with plotly)

The notebook also shows this chart built with: plotly, altair.
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
rng = np.random.default_rng(1)
dates = pd.date_range("2022-01", periods=36, freq="MS")
t = np.arange(36)
df = pd.DataFrame({
    "date": dates,
    "App A": 120 + 4.0 * t + rng.normal(0, 6, 36),
    "App B": 180 + 1.2 * t + 15 * np.sin(t / 3) + rng.normal(0, 6, 36),
    "App C": 60 + 0.15 * t ** 2 + rng.normal(0, 5, 36),
}).set_index("date")
labels = dict(y="Monthly active users (k)", title="Monthly active users by app")
df.head()

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.stocks() — weekly closing prices of large tech stocks 2018–2019 (normalised), bundled with plotly
    import plotly.express as px
    df = (px.data.stocks().assign(date=lambda d: pd.to_datetime(d["date"]))
            .set_index("date")[["GOOG", "AAPL", "AMZN"]])
    labels = dict(y="Share price (1 Jan 2018 = 1)", title="Weekly share prices, 2018–2019")
    df.head()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.8))
for i, col in enumerate(df.columns):
    ax.plot(df.index, df[col], color=PALETTE[i], label=col)
    ax.text(df.index[-1] + pd.Timedelta(days=12), df[col].iloc[-1], col,
            color="#0b0b0b", va="center", fontsize=10)
ax.set_ylabel(labels["y"])
ax.set_title(labels["title"])
ax.set_xlim(df.index[0], df.index[-1] + (df.index[-1] - df.index[0]) * 0.09)
ax.legend(loc="upper left")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
