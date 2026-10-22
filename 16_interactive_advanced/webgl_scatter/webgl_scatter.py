"""
WebGL Scatter (200k interactive points)  -  family: Interactive, animated & big data

DESIGN PURPOSE
An interactive scatter drawn on the GPU (WebGL) instead of as SVG elements, so
a browser can pan, zoom and hover over hundreds of thousands of points
smoothly. It keeps the individual point and its hover details, which density
images like datashader give up.

WHEN TO USE
  - Explore 50k to ~1M points interactively, zooming into dense regions
  - Points must stay individually inspectable (hover to see a trade, a
    customer, a sensor reading)
  - Share an exploratory view as a standalone HTML file

AVOID WHEN
  - Millions of points or more (the file gets heavy; aggregate with
    datashader)
  - Static print output (use a density plot)
  - Small data (normal SVG scatter is crisper)

ALTERNATIVES
  - Million-point scatter with datashader (static density)
  - Hexbin plot

EXAMPLE
200,000 simulated stock-day observations: daily return vs. trading volume
relative to its 20-day average, split by market-cap group (large, mid, small).

Run:  python webgl_scatter.py
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
rng = np.random.default_rng(31)
groups = {"Large cap": (100_000, 0.012), "Mid cap": (60_000, 0.018), "Small cap": (40_000, 0.026)}
frames = []
for name, (n, vol) in groups.items():
    rel_volume = rng.lognormal(0, 0.45, n)                       # volume / 20-day average
    ret = rng.standard_t(4, n) * vol * np.sqrt(rel_volume) / np.sqrt(2)
    frames.append(pd.DataFrame({"group": name, "rel_volume": rel_volume.astype("float32"),
                                "ret_pct": (100 * ret).astype("float32")}))
df = pd.concat(frames, ignore_index=True)
print(f"{len(df):,} points")
df.groupby("group")["ret_pct"].describe().round(2)

# --- Plot --------------------------------------------------------------------
fig = go.Figure()
# Widest group first so it sits underneath; colors stay tied to the group, not the draw order.
for i, (name, part) in reversed(list(enumerate(df.groupby("group", sort=False)))):
    fig.add_trace(go.Scattergl(
        x=part["rel_volume"].to_numpy(), y=part["ret_pct"].to_numpy(), mode="markers", name=name,
        marker=dict(size=3, color=PALETTE[i], opacity=0.35),
        hovertemplate=f"{name}<br>relative volume %{{x:.2f}}×<br>return %{{y:+.2f}}%<extra></extra>"))
fig.update_layout(
    title=f"Daily return vs. relative volume: {len(df):,} stock-days (WebGL)",
    xaxis=dict(title="Volume relative to 20-day average (log scale)", type="log"),
    yaxis=dict(title="Daily return (%)", range=[-15, 15]),
    legend=dict(itemsizing="constant", traceorder="reversed"), height=580,
)

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".html")
fig.write_html(out, include_plotlyjs="cdn", div_id="webgl_scatter")
try:  # static preview; needs kaleido + a local Chrome
    fig.write_image(out.with_suffix(".png"), width=1000, height=620, scale=1.5)
except Exception:
    pass
print(f"saved {out}")
if "--no-show" not in sys.argv:
    fig.show()
