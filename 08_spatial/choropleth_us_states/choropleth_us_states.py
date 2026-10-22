"""
Choropleth Map (US states)  -  family: Spatial

DESIGN PURPOSE
A choropleth at the sub-national level, using built-in US state shapes keyed
by two-letter postal codes. It works for any state-level KPI.

WHEN TO USE
  - Show a state-level rate or index for a US audience
  - Show regional patterns (South vs. Northeast, coastal vs. interior)

AVOID WHEN
  - Small states such as RI, DE and DC matter to the story (they are nearly
    invisible; use a tile grid map)
  - Values are totals that scale with population

ALTERNATIVES
  - Tile grid map
  - Sorted bar chart

EXAMPLE
Illustrative (synthetic) uninsured rate (%) by state, with a South-to-North
gradient.

Run:  python choropleth_us_states.py
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
STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN",
          "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",
          "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT",
          "VT", "VA", "WA", "WV", "WI", "WY"]

rng = np.random.default_rng(8)
south = {"TX", "OK", "GA", "FL", "MS", "AL", "SC", "NC", "TN", "AR", "LA", "NM", "AZ", "NV", "WY"}
rate = [rng.normal(11.5 if s in south else 6.5, 1.6) for s in STATES]
df = pd.DataFrame({"state": STATES, "uninsured_pct": np.clip(rate, 2.5, 18).round(1)})
df.head()

# --- Plot --------------------------------------------------------------------
fig = px.choropleth(df, locations="state", locationmode="USA-states", scope="usa",
                    color="uninsured_pct", color_continuous_scale="Blues",
                    labels={"uninsured_pct": "Uninsured (%)"},
                    title="Uninsured rate by state (illustrative data)")
fig.update_traces(marker_line_color="#fcfcfb", marker_line_width=1)
fig.update_layout(margin=dict(l=10, r=10, t=50, b=10), height=460, geo_bgcolor="#fcfcfb")

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".html")
fig.write_html(out, include_plotlyjs="cdn", div_id="choropleth_us_states")
try:  # static preview; needs kaleido + a local Chrome
    fig.write_image(out.with_suffix(".png"), width=1000, height=620, scale=1.5)
except Exception:
    pass
print(f"saved {out}")
if "--no-show" not in sys.argv:
    fig.show()
