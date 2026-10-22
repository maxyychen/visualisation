"""
Sunburst Chart  -  family: Part-to-whole

DESIGN PURPOSE
Concentric rings that show a hierarchy. The center is the root and each ring
outward is one level deeper. Each arc's angle is proportional to its value. In
the interactive version, clicking a segment zooms into that branch.

WHEN TO USE
  - Show part-to-whole across 2–4 levels of hierarchy
  - Exploring how a total breaks down (budget → department → line item)
  - Interactive contexts where users can drill down

AVOID WHEN
  - Precise comparison is needed (outer arcs are distorted by radius)
  - The hierarchy is deeper than ~4 levels or very unbalanced
  - Static print with many small segments

ALTERNATIVES
  - Treemap
  - Icicle chart
  - Indented table

EXAMPLE
Global sales by region → country → channel (synthetic).

Run:  python sunburst.py
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
rows = [
    ("Asia", "Japan", "Online", 42), ("Asia", "Japan", "Retail", 30),
    ("Asia", "Taiwan", "Online", 25), ("Asia", "Taiwan", "Retail", 18),
    ("Asia", "India", "Online", 20), ("Asia", "India", "Retail", 12),
    ("Europe", "Germany", "Online", 33), ("Europe", "Germany", "Retail", 27),
    ("Europe", "France", "Online", 21), ("Europe", "France", "Retail", 19),
    ("Europe", "UK", "Online", 26), ("Europe", "UK", "Retail", 14),
    ("Americas", "USA", "Online", 60), ("Americas", "USA", "Retail", 45),
    ("Americas", "Brazil", "Online", 14), ("Americas", "Brazil", "Retail", 10),
]
df = pd.DataFrame(rows, columns=["region", "country", "channel", "sales_m"])
df.head()

# --- Plot --------------------------------------------------------------------
fig = px.sunburst(df, path=["region", "country", "channel"], values="sales_m",
                  color="region", color_discrete_sequence=PALETTE,
                  title="Sales by region, country and channel ($M)")
fig.update_traces(marker=dict(line=dict(color="#fcfcfb", width=2)),
                  insidetextorientation="radial")
fig.update_layout(width=700, height=650, margin=dict(t=60, l=10, r=10, b=10))

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".html")
fig.write_html(out, include_plotlyjs="cdn", div_id="sunburst")
try:  # static preview; needs kaleido + a local Chrome
    fig.write_image(out.with_suffix(".png"), width=1000, height=620, scale=1.5)
except Exception:
    pass
print(f"saved {out}")
if "--no-show" not in sys.argv:
    fig.show()
