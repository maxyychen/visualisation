"""
Bubble Chart  -  family: Correlation

DESIGN PURPOSE
A scatter plot whose marker area encodes a third numeric variable. Three
measures fit in one view, with the size channel adding emphasis.

WHEN TO USE
  - Show three numeric variables at once (x, y, and size)
  - Show entities whose size or weight matters (population, revenue)
  - Tell a 'Gapminder-style' story about countries or companies

AVOID WHEN
  - Precise comparison of the third variable matters (area is judged poorly)
  - There are many bubbles that overlap heavily
  - Sizes span several orders of magnitude without scaling

ALTERNATIVES
  - Scatter plot with color for a third variable
  - Small multiples

EXAMPLE
GDP per capita vs. life expectancy for 40 fictional countries; bubble area =
population.

Run:  python bubble.py
      python bubble.py --real-data   (real dataset: plotly.express.data.gapminder() — Gapminder 2007 (Asia, Africa, Europe), bundled with plotly)

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
rng = np.random.default_rng(8)
n = 40
gdp = np.exp(rng.uniform(np.log(800), np.log(80000), n))
life = 48 + 7.5 * np.log10(gdp) + rng.normal(0, 2.5, n)
pop = np.exp(rng.normal(3, 1.3, n))          # millions
region = rng.choice(["Asia", "Africa", "Europe"], n, p=[0.4, 0.35, 0.25])
df = pd.DataFrame({"country": [f"C{i:02d}" for i in range(n)], "gdp_pc": gdp,
                   "life_exp": life, "pop_m": pop, "region": region})
df = df.sort_values("pop_m", ascending=False)   # big bubbles drawn first
df.head()

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.gapminder() — Gapminder 2007 (Asia, Africa, Europe), bundled with plotly
    import plotly.express as px
    gm = px.data.gapminder().query("year == 2007 and continent in ['Asia', 'Africa', 'Europe']")
    df = pd.DataFrame({"country": gm["country"], "gdp_pc": gm["gdpPercap"], "life_exp": gm["lifeExp"],
                       "pop_m": gm["pop"] / 1e6, "region": gm["continent"]})
    df = df.sort_values("pop_m", ascending=False)
    df.head()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5.5))
size = lambda p: p * 4                         # area proportional to population
for color, reg in zip(PALETTE, ["Asia", "Africa", "Europe"]):
    g = df[df["region"] == reg]
    ax.scatter(g["gdp_pc"], g["life_exp"], s=size(g["pop_m"]), color=color,
               alpha=0.65, edgecolor="#fcfcfb", linewidth=1, label=reg)
ax.set_xscale("log")
ax.set_xlabel("GDP per capita (USD, log scale)")
ax.set_ylabel("Life expectancy (years)")
ax.set_title("Wealth and health of nations")
leg1 = ax.legend(loc="upper left", markerscale=0.4)
ax.add_artist(leg1)
for p in [10, 50, 200]:
    ax.scatter([], [], s=size(p), color="#d0cfca", label=f"{p}M")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[3:], labels[3:], loc="lower right", title="Population",
          labelspacing=1.6, borderpad=1.2)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
