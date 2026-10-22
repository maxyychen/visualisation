"""
Choropleth Map (world)  -  family: Spatial

DESIGN PURPOSE
Fills each region with a color that encodes a statistic. Geographic clusters
and regional gradients (the north–south divide, a hot spot) become visible at
a glance.

WHEN TO USE
  - Show a rate, ratio or index (life expectancy, % vaccinated) across
    countries or regions
  - Reveal spatial clusters and gradients
  - Show data that is already aggregated to administrative units

AVOID WHEN
  - Values are raw counts, because big regions dominate visually (normalize to
    per-capita or use a bubble map)
  - Small but important regions would be invisible (use a tile grid map)
  - Readers need to compare exact values (use a sorted bar chart)

ALTERNATIVES
  - Tile grid map
  - Bubble map
  - Sorted bar chart

EXAMPLE
Life expectancy at birth by country in 2007 (Gapminder dataset, bundled with
plotly).

Run:  python choropleth_world.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
           "#e87ba4", "#008300", "#6250d6", "#e34948"]
pio.templates["vizlib"] = go.layout.Template(layout=dict(
    colorway=PALETTE, font=dict(family="Helvetica, Arial, sans-serif", size=13, color="#0b0b0b"),
    paper_bgcolor="#fcfcfb", plot_bgcolor="#fcfcfb", title=dict(x=0.02, xanchor="left"),
    xaxis=dict(gridcolor="#e6e5e1", linecolor="#c9c8c3", zeroline=False),
    yaxis=dict(gridcolor="#e6e5e1", linecolor="#c9c8c3", zeroline=False),
))
pio.templates.default = "plotly_white+vizlib"

# --- Example data ------------------------------------------------------------
df = px.data.gapminder().query("year == 2007")
df[["country", "continent", "iso_alpha", "lifeExp"]].head()

# --- Plot --------------------------------------------------------------------
fig = px.choropleth(df, locations="iso_alpha", color="lifeExp", hover_name="country",
                    color_continuous_scale="Blues", range_color=(40, 85),
                    labels={"lifeExp": "Life exp. (yrs)"},
                    title="Life expectancy at birth, 2007")
fig.update_geos(showframe=False, showcoastlines=False, projection_type="natural earth",
                bgcolor="#fcfcfb", landcolor="#eeeeea")
fig.update_layout(margin=dict(l=10, r=10, t=50, b=10), height=480)

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".html")
fig.write_html(out, include_plotlyjs="cdn")
try:  # static preview; needs kaleido + a local Chrome
    fig.write_image(out.with_suffix(".png"), width=1000, height=620, scale=1.5)
except Exception:
    pass
print(f"saved {out}")
if "--no-show" not in sys.argv:
    fig.show()
