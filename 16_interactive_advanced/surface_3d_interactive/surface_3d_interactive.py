"""
Interactive 3-D Surface (implied volatility)  -  family: Interactive, animated & big data

DESIGN PURPOSE
A rotatable 3-D surface of a measure over two continuous inputs, here implied
volatility over strike and expiry, shown next to a 2-D heatmap of the same
grid. The surface gives the overall shape (skew, smile, term structure) at a
glance, and the heatmap is where values are actually read.

WHEN TO USE
  - Show the shape of a function of two variables: volatility surfaces,
    yield/term surfaces, loss landscapes, response surfaces
  - The reader can rotate and hover (interactive HTML, notebook)
  - Shape matters more than exact values

AVOID WHEN
  - Static images and print: a fixed 3-D view hides parts of the surface and
    distorts heights (use a heatmap or contour plot)
  - Comparing precise values (perspective makes heights unreadable)
  - Bars or pies in 3-D: never

ALTERNATIVES
  - Heatmap or contour plot (precise and static)
  - Small multiples of 2-D slices (e.g. smiles by expiry)

EXAMPLE
Simulated equity-index implied volatility for strikes at 70–130% of spot and
expiries of 1 week to 2 years: downside skew, a smile at short expiries, and
an upward-sloping term structure.

Run:  python surface_3d_interactive.py
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

from plotly.subplots import make_subplots

# --- Example data ------------------------------------------------------------
moneyness = np.linspace(0.70, 1.30, 25)                     # strike / spot
expiry = np.array([1/52, 2/52, 1/12, 2/12, 3/12, 6/12, 9/12, 1.0, 1.5, 2.0])
K, T = np.meshgrid(moneyness, expiry)
x = np.log(K)
atm = 0.16 + 0.025 * np.log1p(4 * T)                          # term structure
skew = -0.32 / np.sqrt(T + 0.15) * x                          # downside skew, fading with expiry
smile = 0.9 / (T + 0.25) * x**2                                # curvature, strongest short-dated
iv = 100 * (atm + skew * 0.35 + smile * 0.35)
expiry_labels = ["1W", "2W", "1M", "2M", "3M", "6M", "9M", "1Y", "18M", "2Y"]
surface = pd.DataFrame(iv.round(1), index=expiry_labels, columns=(100 * moneyness).round().astype(int))
surface.iloc[:, ::4]

# --- Plot --------------------------------------------------------------------
fig = make_subplots(rows=1, cols=2, column_widths=[0.58, 0.42], horizontal_spacing=0.06,
                    specs=[[{"type": "surface"}, {"type": "heatmap"}]],
                    subplot_titles=("Rotate me: shape", "Read me: values (%)"))
fig.add_trace(go.Surface(
    x=100 * moneyness, y=np.arange(len(expiry)), z=iv, coloraxis="coloraxis",
    contours=dict(z=dict(show=True, project_z=True, usecolormap=True, width=1)),
    hovertemplate="strike %{x:.0f}% · expiry %{customdata}<br>IV %{z:.1f}%<extra></extra>",
    customdata=np.tile(np.array(expiry_labels)[:, None], (1, len(moneyness)))), row=1, col=1)
fig.add_trace(go.Heatmap(
    x=100 * moneyness, y=expiry_labels, z=iv, coloraxis="coloraxis",
    hovertemplate="strike %{x:.0f}% · expiry %{y}<br>IV %{z:.1f}%<extra></extra>"), row=1, col=2)
fig.update_layout(
    title="Implied volatility surface (simulated equity index)", height=560,
    coloraxis=dict(colorscale="Blues", colorbar=dict(title="IV (%)", x=1.02)),
    scene=dict(xaxis_title="Strike (% of spot)", zaxis_title="IV (%)",
               yaxis=dict(title="Expiry", tickvals=list(range(len(expiry))), ticktext=expiry_labels),
               camera=dict(eye=dict(x=-1.6, y=-1.5, z=0.9))),
    margin=dict(l=10, r=10, t=80, b=40),
)
fig.update_xaxes(title_text="Strike (% of spot)", row=1, col=2)
fig.update_yaxes(title_text="Expiry", row=1, col=2)

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".html")
fig.write_html(out, include_plotlyjs="cdn", div_id="surface_3d_interactive")
try:  # static preview; needs kaleido + a local Chrome
    fig.write_image(out.with_suffix(".png"), width=1000, height=620, scale=1.5)
except Exception:
    pass
print(f"saved {out}")
if "--no-show" not in sys.argv:
    fig.show()
