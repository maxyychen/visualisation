"""
Sankey Diagram  -  family: Flow

DESIGN PURPOSE
Nodes joined by bands whose width is proportional to the quantity flowing
between them. It shows where a quantity comes from, where it goes, and where
it is lost or split, and the total is conserved along the way.

WHEN TO USE
  - Show energy, money, or material flowing through a system
  - Show how a population moves through stages (lead → trial → paid plan)
  - Show the main paths and losses in a multi-step process

AVOID WHEN
  - Flows form cycles or have many back-links (use a chord diagram or network)
  - There are too many nodes, giving a 'spaghetti' tangle (aggregate first)
  - Only one stage transition with one source (use a bar chart)

ALTERNATIVES
  - Alluvial diagram
  - Funnel chart
  - Chord diagram

EXAMPLE
Customer journey: 1,000 new sign-ups → first-week engagement → plan after 30
days.

Run:  python sankey.py
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
nodes = ["Sign-ups", "Activated", "Browsed only", "Bounced",
         "Pro plan", "Basic plan", "Free tier", "Churned", "Win-back email"]
links = pd.DataFrame([
    ("Sign-ups", "Activated", 380), ("Sign-ups", "Browsed only", 520), ("Sign-ups", "Bounced", 100),
    ("Activated", "Pro plan", 210), ("Activated", "Basic plan", 150), ("Activated", "Free tier", 20),
    ("Browsed only", "Free tier", 140), ("Browsed only", "Churned", 380),
    ("Bounced", "Win-back email", 100),
], columns=["source", "target", "users"])
links

# --- Plot --------------------------------------------------------------------
idx = {n: i for i, n in enumerate(nodes)}
node_colors = ["#52514e", PALETTE[1], PALETTE[0], PALETTE[3],
               "#b8b7b1", "#b8b7b1", "#b8b7b1", "#b8b7b1", "#b8b7b1"]
def rgba(hex_, a):
    h = hex_.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})"
link_colors = [rgba(node_colors[idx[t]] if s == "Sign-ups" else node_colors[idx[s]], 0.45)
               for s, t in zip(links["source"], links["target"])]
fig = go.Figure(go.Sankey(
    node=dict(label=nodes, color=node_colors, pad=18, thickness=16,
              line=dict(color="#fcfcfb", width=1)),
    link=dict(source=links["source"].map(idx), target=links["target"].map(idx),
              value=links["users"], color=link_colors),
))
fig.update_layout(title="Customer journey from sign-up to plan (n = 1,000)",
                  width=900, height=520, margin=dict(t=60, l=20, r=20, b=20))

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
