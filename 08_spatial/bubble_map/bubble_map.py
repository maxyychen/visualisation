"""
Bubble Map (proportional symbols)  -  family: Spatial

DESIGN PURPOSE
Places a circle at each location with area proportional to a quantity. Unlike
a choropleth, the symbol size, not the region size, carries the value, so raw
counts are safe to show.

WHEN TO USE
  - Show counts or totals at point locations (city population, store revenue,
    case counts)
  - Show values whose locations do not match administrative boundaries

AVOID WHEN
  - Points are so dense that circles overlap into a blob (aggregate, or use a
    hexbin or density map)
  - The value is a rate (a choropleth is more natural)

ALTERNATIVES
  - Choropleth (for rates)
  - Dot density map
  - Sorted bar chart

EXAMPLE
Approximate population of the world's largest urban agglomerations (millions,
illustrative).

Run:  python bubble_map.py
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
df = pd.DataFrame([
    ("Tokyo", 35.7, 139.7, 37.2), ("Delhi", 28.6, 77.2, 32.9), ("Shanghai", 31.2, 121.5, 29.2),
    ("Dhaka", 23.8, 90.4, 23.2), ("São Paulo", -23.6, -46.6, 22.6), ("Cairo", 30.0, 31.2, 22.2),
    ("Mexico City", 19.4, -99.1, 22.3), ("Beijing", 39.9, 116.4, 21.8), ("Mumbai", 19.1, 72.9, 21.3),
    ("Osaka", 34.7, 135.5, 19.0), ("New York", 40.7, -74.0, 18.9), ("Karachi", 24.9, 67.0, 17.2),
    ("Kinshasa", -4.3, 15.3, 17.0), ("Lagos", 6.5, 3.4, 15.9), ("Istanbul", 41.0, 29.0, 15.8),
    ("Buenos Aires", -34.6, -58.4, 15.5), ("Kolkata", 22.6, 88.4, 15.3), ("Manila", 14.6, 121.0, 14.7),
    ("Moscow", 55.8, 37.6, 12.7), ("Los Angeles", 34.1, -118.2, 12.5), ("Paris", 48.9, 2.35, 11.2),
    ("Jakarta", -6.2, 106.8, 11.2), ("London", 51.5, -0.13, 9.6), ("Lima", -12.0, -77.0, 11.0),
], columns=["city", "lat", "lon", "pop_m"]).sort_values("pop_m", ascending=False)
df.head()

# --- Plot --------------------------------------------------------------------
fig = px.scatter_geo(df, lat="lat", lon="lon", size="pop_m", hover_name="city",
                     size_max=38, projection="natural earth",
                     title="Largest urban agglomerations (population, millions)")
fig.update_traces(marker=dict(color=PALETTE[0], opacity=0.7,
                              line=dict(color="#fcfcfb", width=1)))
fig.update_geos(showframe=False, landcolor="#eeeeea", coastlinecolor="#c9c8c3",
                showcountries=True, countrycolor="#dcdbd6", bgcolor="#fcfcfb")
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
