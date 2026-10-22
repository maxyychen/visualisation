"""
Alluvial Diagram (Parallel Categories)  -  family: Flow

DESIGN PURPOSE
Several categorical dimensions are drawn as vertical axes with ribbons
connecting them. Each ribbon is the group of records sharing a combination of
categories. It shows how membership in one classification maps onto another,
or how groups change over time.

WHEN TO USE
  - Show how individuals move between categories over time (plan tier in 2024
    → 2025)
  - Explore associations among 2–4 categorical variables
  - Track cohort composition across stages

AVOID WHEN
  - Variables are continuous (use parallel coordinates)
  - Each dimension has many categories (ribbons become unreadable)

ALTERNATIVES
  - Sankey diagram
  - Mosaic/marimekko chart
  - Heatmap of a cross-tab

EXAMPLE
1,500 survey respondents: age group → preferred channel → satisfaction.

Run:  python alluvial.py
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
rng = np.random.default_rng(21)
n = 1500
age = rng.choice(["18–34", "35–54", "55+"], n, p=[0.35, 0.4, 0.25])
p_channel = {"18–34": [0.65, 0.25, 0.10], "35–54": [0.45, 0.35, 0.20], "55+": [0.2, 0.35, 0.45]}
channel = np.array([rng.choice(["App", "Web", "Phone"], p=p_channel[a]) for a in age])
p_sat = {"App": [0.6, 0.3, 0.1], "Web": [0.45, 0.4, 0.15], "Phone": [0.35, 0.35, 0.3]}
sat = np.array([rng.choice(["Satisfied", "Neutral", "Unsatisfied"], p=p_sat[c]) for c in channel])
df = pd.DataFrame({"Age": age, "Channel": channel, "Satisfaction": sat})
df.value_counts().head(8)

# --- Plot --------------------------------------------------------------------
color_idx = df["Channel"].map({"App": 0, "Web": 1, "Phone": 2})
fig = go.Figure(go.Parcats(
    dimensions=[
        dict(label="Age", values=df["Age"], categoryorder="array",
             categoryarray=["18–34", "35–54", "55+"]),
        dict(label="Channel", values=df["Channel"], categoryorder="array",
             categoryarray=["App", "Web", "Phone"]),
        dict(label="Satisfaction", values=df["Satisfaction"], categoryorder="array",
             categoryarray=["Satisfied", "Neutral", "Unsatisfied"]),
    ],
    line=dict(color=color_idx, colorscale=[[0, PALETTE[0]], [0.5, PALETTE[1]], [1, PALETTE[2]]],
              shape="hspline"),
    hoveron="color", arrangement="freeform",
))
fig.update_layout(title="Customer journey: age → channel → satisfaction (n = 1,500)",
                  width=900, height=520, margin=dict(t=70, l=60, r=60, b=30))

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
