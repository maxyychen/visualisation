"""
Flow Map (origin–destination)  -  family: Spatial

DESIGN PURPOSE
Draws lines between origins and destinations on a map, with line width (or
opacity) encoding the volume of movement. It combines geography with flow.

WHEN TO USE
  - Show movement between places (flights, migration, trade, capital flows)
  - Show hub-and-spoke networks where geography matters

AVOID WHEN
  - There are many crossing routes (it becomes a hairball; aggregate, or use a
    chord diagram or matrix)
  - The geography is irrelevant to the story (use a Sankey diagram)

ALTERNATIVES
  - Sankey diagram
  - Chord diagram
  - Origin–destination matrix heatmap

EXAMPLE
Weekly passengers (thousands, illustrative) on routes out of a Taipei hub
airport.

Run:  python flow_map.py
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
hub = ("Taipei", 25.08, 121.23)
df = pd.DataFrame([
    ("Tokyo", 35.55, 139.78, 62), ("Seoul", 37.46, 126.44, 41), ("Hong Kong", 22.31, 113.91, 55),
    ("Singapore", 1.36, 103.99, 30), ("Bangkok", 13.69, 100.75, 34), ("Manila", 14.51, 121.02, 22),
    ("Los Angeles", 33.94, -118.41, 18), ("San Francisco", 37.62, -122.38, 14),
    ("Vancouver", 49.19, -123.18, 9), ("London", 51.47, -0.45, 8), ("Amsterdam", 52.31, 4.76, 6),
    ("Sydney", -33.94, 151.18, 11), ("Dubai", 25.25, 55.36, 7),
], columns=["dest", "lat", "lon", "pax_k"])
df.head()

# --- Plot --------------------------------------------------------------------
fig = go.Figure()
for _, r in df.iterrows():
    fig.add_trace(go.Scattergeo(
        lon=[hub[2], r.lon], lat=[hub[1], r.lat], mode="lines",
        line=dict(width=0.6 + r.pax_k / 6, color=PALETTE[0]), opacity=0.65,
        hoverinfo="text", text=f"{hub[0]} → {r.dest}: {r.pax_k}k pax/week", showlegend=False))
fig.add_trace(go.Scattergeo(
    lon=df.lon, lat=df.lat, text=df.dest, mode="markers+text", textposition="top center",
    marker=dict(size=6, color=PALETTE[0], line=dict(color="#fcfcfb", width=1)),
    textfont=dict(size=10, color="#52514e"), showlegend=False, hoverinfo="skip"))
fig.add_trace(go.Scattergeo(lon=[hub[2]], lat=[hub[1]], text=[hub[0]], mode="markers+text",
                            textposition="bottom center", marker=dict(size=11, color=PALETTE[1]),
                            showlegend=False))
fig.update_geos(projection_type="natural earth", projection_rotation=dict(lon=150),
                showframe=False, landcolor="#eeeeea", coastlinecolor="#c9c8c3",
                bgcolor="#fcfcfb", showcountries=False)
fig.update_layout(title="Weekly passengers from Taipei hub (thousands, illustrative)",
                  margin=dict(l=10, r=10, t=50, b=10), height=500)

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
