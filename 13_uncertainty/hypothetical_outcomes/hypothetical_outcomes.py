"""
Hypothetical Outcome Plot (HOP)  -  family: Uncertainty

DESIGN PURPOSE
Animates uncertainty instead of summarizing it. Each frame shows one plausible
outcome drawn from the distribution, so viewers experience how often one
option beats another rather than reading overlapping error bars. Hullman et
al. (2015) found HOPs improve judgements of the probability that A > B.

WHEN TO USE
  - Answer "how often is A better than B?" when the uncertainty intervals
    overlap
  - Communicate model uncertainty to non-experts in an interactive or
    presentation setting
  - Show that a "winner" by average is not a guaranteed winner

AVOID WHEN
  - The output is printed or static (it needs animation; use gradient
    intervals or half-eye instead)
  - Readers need precise interval values
  - The animation would run too fast to follow (under ~300 ms per frame)

ALTERNATIVES
  - Half-eye plot (static)
  - Quantile dotplot
  - Bar chart with intervals plus a stated probability that A > B

REFERENCE
  - Hullman, J., Resnick, P. & Adar, E. (2015). Hypothetical outcome plots
    outperform error bars and violin plots for inferences about reliability of
    variable ordering. PLOS ONE 10(11), e0142444.
    https://doi.org/10.1371/journal.pone.0142444

EXAMPLE
Days to recovery under two treatments, with uncertain averages (Treatment A ~
N(10, 1.6) and Treatment B ~ N(11.5, 1.6) days). Each frame is one draw;
synthetic data.

Run:  python hypothetical_outcomes.py
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
rng = np.random.default_rng(4)
n_frames = 40
draws = pd.DataFrame({
    "A": rng.normal(10, 1.6, n_frames),
    "B": rng.normal(11.5, 1.6, n_frames),
})
p_b_slower = (draws["B"] > draws["A"]).mean()
print(f"B slower than A in {p_b_slower:.0%} of draws")
draws.head().round(1)

# --- Plot --------------------------------------------------------------------
labels = ["Treatment A", "Treatment B"]
colors = [PALETTE[0], PALETTE[1]]

def frame_data(i):
    vals = draws.iloc[i][["A", "B"]].values
    return [go.Bar(x=labels, y=vals, marker_color=colors, width=0.5,
                   text=[f"{v:.1f} d" for v in vals], textposition="outside",
                   hovertemplate="%{x}: %{y:.1f} days<extra></extra>")]

def frame_note(i):
    a, b = draws.iloc[i][["A", "B"]]
    who = "A recovers faster" if a < b else "B recovers faster"
    return [dict(text=f"Outcome {i + 1} of {n_frames}: {who}", x=0.5, y=1.02, xref="paper",
                 yref="paper", showarrow=False, font=dict(size=14, color="#52514e"))]

frames = [go.Frame(data=frame_data(i), name=str(i), layout=dict(annotations=frame_note(i)))
          for i in range(n_frames)]
fig = go.Figure(data=frame_data(0), frames=frames)
fig.update_layout(
    title=f"Days to recovery: one plausible outcome per frame (B slower in {p_b_slower:.0%} of draws)",
    yaxis=dict(range=[0, 17], title="Days to recovery"),
    annotations=frame_note(0), showlegend=False, height=520,
    updatemenus=[dict(type="buttons", x=0, y=-0.12, xanchor="left", direction="left", buttons=[
        dict(label="▶ Play", method="animate",
             args=[None, dict(frame=dict(duration=450, redraw=True), transition=dict(duration=0),
                              fromcurrent=True)]),
        dict(label="❚❚ Pause", method="animate",
             args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]),
    ])],
    sliders=[dict(x=0.18, y=-0.08, len=0.8, currentvalue=dict(prefix="Outcome "),
                  steps=[dict(label=str(i + 1), method="animate",
                              args=[[str(i)], dict(frame=dict(duration=0, redraw=True), mode="immediate")])
                         for i in range(n_frames)])],
)

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".html")
fig.write_html(out, include_plotlyjs="cdn", div_id="hypothetical_outcomes")
try:  # static preview; needs kaleido + a local Chrome
    fig.write_image(out.with_suffix(".png"), width=1000, height=620, scale=1.5)
except Exception:
    pass
print(f"saved {out}")
if "--no-show" not in sys.argv:
    fig.show()
