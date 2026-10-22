"""
Icicle Chart  -  family: Part-to-whole

DESIGN PURPOSE
A rectangular, linear version of the sunburst. Each hierarchy level is a row
(or column), and each child sits directly under its parent with a width
proportional to its value. Straight edges are easier to compare than arcs, and
long labels fit better.

WHEN TO USE
  - Show hierarchical part-to-whole where labels are long
  - Show file-system sizes, cost breakdowns, or org structures
  - Need accurate comparison at every level of a hierarchy

AVOID WHEN
  - The hierarchy has only one level (use a bar or treemap)
  - There are hundreds of leaves (use a treemap)

ALTERNATIVES
  - Sunburst
  - Treemap
  - Flame graph (performance profiling)

EXAMPLE
Disk usage of a project folder by directory and file type.

Run:  python icicle.py
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
    ("project", "data", "raw", 820), ("project", "data", "processed", 310),
    ("project", "models", "checkpoints", 540), ("project", "models", "exports", 120),
    ("project", "notebooks", "outputs", 95), ("project", "notebooks", "ipynb", 40),
    ("project", "src", "python", 12), ("project", "src", "tests", 6),
    ("project", "docs", "images", 55), ("project", "docs", "markdown", 3),
]
df = pd.DataFrame(rows, columns=["root", "folder", "sub", "size_mb"])
df.head()

# --- Plot --------------------------------------------------------------------
fig = px.icicle(df, path=[px.Constant("project"), "folder", "sub"], values="size_mb", color="folder",
                color_discrete_sequence=PALETTE, title="Disk usage by folder (MB)")
fig.update_traces(root_color="#d0cfca", tiling=dict(orientation="v"),
                  marker=dict(line=dict(color="#fcfcfb", width=2)))
fig.update_layout(width=850, height=500, margin=dict(t=60, l=10, r=10, b=10))

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".html")
fig.write_html(out, include_plotlyjs="cdn", div_id="icicle")
try:  # static preview; needs kaleido + a local Chrome
    fig.write_image(out.with_suffix(".png"), width=1000, height=620, scale=1.5)
except Exception:
    pass
print(f"saved {out}")
if "--no-show" not in sys.argv:
    fig.show()
