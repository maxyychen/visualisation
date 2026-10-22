"""
Violin Plot  -  family: Distribution

DESIGN PURPOSE
A mirrored density curve for each group, often with a mini box plot inside. It
keeps a box plot's compact group comparison while showing the full shape of
each distribution.

WHEN TO USE
  - Compare distributions across groups when the shape matters (bimodality,
    skew)
  - Show large samples per group

AVOID WHEN
  - There are small samples (under ~30 per group)
  - The audience is non-technical (box plots or histograms are more familiar)

ALTERNATIVES
  - Box plot
  - Raincloud plot
  - Ridgeline plot

EXAMPLE
Daily screen time (hours) by age group, with a split by weekday vs. weekend.

Run:  python violin_plot.py
      python violin_plot.py --real-data   (real dataset: plotly.express.data.tips() — restaurant tipping data (Bryant & Smith 1995), bundled with plotly)

The notebook also shows this chart built with: plotly.
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
rng = np.random.default_rng(31)
groups = {"13–17": 6.5, "18–29": 5.5, "30–49": 4.2, "50–64": 3.4, "65+": 3.0}
rows = []
for g, mu in groups.items():
    rows.append(pd.DataFrame({"age": g, "day": "Weekday", "hours": rng.gamma(mu * 2, 0.5, 300)}))
    rows.append(pd.DataFrame({"age": g, "day": "Weekend", "hours": rng.gamma(mu * 2.6, 0.5, 300)}))
df = pd.concat(rows, ignore_index=True)
x, y, hue = "age", "hours", "day"
labels = dict(x="Age group", y="Screen time (hours / day)", title="Daily screen time by age group")
df.groupby(["age", "day"])["hours"].median().unstack().round(1)

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.tips() — restaurant tipping data (Bryant & Smith 1995), bundled with plotly
    import plotly.express as px
    df = px.data.tips()
    df["day"] = pd.Categorical(df["day"], ["Thur", "Fri", "Sat", "Sun"])   # calendar order
    x, y, hue = "day", "total_bill", "sex"
    labels = dict(x="Day", y="Total bill ($)", title="Restaurant bills by day and sex")
    df.groupby([x, hue], observed=True)[y].median().unstack().round(1)

# --- Plot --------------------------------------------------------------------
import seaborn as sns
fig, ax = plt.subplots(figsize=(9, 5))
sns.violinplot(data=df, x=x, y=y, hue=hue, split=True, inner="quart",
               palette=PALETTE[:2], linewidth=1, cut=0, density_norm="width", ax=ax)
ax.set_xlabel(labels["x"])
ax.set_ylabel(labels["y"])
ax.set_title(labels["title"])
ax.legend(title=None, loc="upper right")
ax.grid(axis="x", visible=False)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
