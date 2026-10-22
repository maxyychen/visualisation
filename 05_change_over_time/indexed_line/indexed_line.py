"""
Indexed Line Chart (rebased to 100)  -  family: Change over time

DESIGN PURPOSE
Divides each series by its value at a common start date and multiplies by 100,
so all series start at 100 and show relative growth. It is the honest
replacement for a dual-axis chart when series have very different units or
scales.

WHEN TO USE
  - Compare growth of series with very different magnitudes (a small-cap vs.
    an index)
  - You are tempted to use a second y-axis. Index instead, so there is one
    honest scale
  - Show performance since an event (rebased at the event date)

AVOID WHEN
  - Absolute levels matter more than relative change
  - The base period is unusual (spike or trough), which distorts every later
    value

ALTERNATIVES
  - Two separate charts stacked vertically
  - Small multiples

EXAMPLE
Users (thousands) and sessions (millions) of a product: different scales,
compared by growth.

Run:  python indexed_line.py
      python indexed_line.py --real-data   (real dataset: plotly.express.data.gapminder() — Gapminder life expectancy, GDP and population 1952–2007, bundled with plotly)
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
rng = np.random.default_rng(14)
dates = pd.date_range("2023-01", periods=30, freq="MS")
t = np.arange(30)
df = pd.DataFrame({
    "Users (k)": 12 + 0.9 * t + rng.normal(0, 0.5, 30),
    "Sessions (M)": 0.35 + 0.004 * t ** 1.6 + rng.normal(0, 0.01, 30),
    "Revenue ($M)": 2.1 + 0.03 * t + rng.normal(0, 0.05, 30),
}, index=dates)
indexed = df / df.iloc[0] * 100
labels = dict(y="Index (Jan 2023 = 100)",
              title="Growth since Jan 2023: one honest axis instead of three")
indexed.head()

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.gapminder() — Gapminder life expectancy, GDP and population 1952–2007, bundled with plotly
    import plotly.express as px
    gm = px.data.gapminder().query("country == 'India'")
    df = pd.DataFrame({"Population (M)": gm["pop"].values / 1e6,
                       "GDP per capita ($)": gm["gdpPercap"].values,
                       "Life expectancy (yrs)": gm["lifeExp"].values},
                      index=pd.to_datetime(gm["year"].astype(str)))
    indexed = df / df.iloc[0] * 100
    labels = dict(y="Index (1952 = 100)", title="India since 1952: three measures on one honest axis")
    indexed.head()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.8))
span = indexed.index[-1] - indexed.index[0]
for i, col in enumerate(indexed.columns):
    ax.plot(indexed.index, indexed[col], color=PALETTE[i], label=col)
    ax.text(indexed.index[-1] + span * 0.012, indexed[col].iloc[-1],
            f"{col.split(' (')[0]} {indexed[col].iloc[-1]:.0f}", va="center", fontsize=9.5)
ax.axhline(100, color="#52514e", linewidth=1)
ax.set_xlim(indexed.index[0], indexed.index[-1] + span * 0.17)
ax.set_ylabel(labels["y"])
ax.set_title(labels["title"])
ax.legend(loc="upper left")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
