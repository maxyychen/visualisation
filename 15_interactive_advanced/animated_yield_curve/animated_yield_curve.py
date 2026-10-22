"""
Animated Yield Curve (2000–2025)  -  family: Interactive, animated & big data

DESIGN PURPOSE
Plays the government bond yield curve through time, one frame per year, with a
faint trail of the previous three years' curves. The curve's shape (upward
sloping, flat or inverted) is the message, and watching it twist, shift and
invert shows rate cycles more intuitively than any single snapshot.

WHEN TO USE
  - Explain rate cycles: easing, tightening, and curve inversions before
    recessions
  - Teach how the short end follows the central bank while the long end
    follows growth and inflation expectations
  - Present the history of a term structure (yields, futures, swap curves)

AVOID WHEN
  - Readers need to compare two specific dates precisely (overlay those two
    curves statically)
  - The medium is print (use the yield curve history heatmap instead)

ALTERNATIVES
  - Yield curve history heatmap (maturity × time)
  - Static overlay of a few chosen dates
  - 10y–2y spread line chart

EXAMPLE
Simulated year-end US-Treasury-like curves (1 month to 30 years) for
2000–2025. Short and long anchors follow the broad shape of the real cycle
(2001–03 easing, 2006–07 inversion, zero rates 2009–15 and 2020–21, the
2022–24 inversion), but the values are illustrative.

Run:  python animated_yield_curve.py
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
rng = np.random.default_rng(8)
quarters = pd.period_range("2000Q1", "2025Q4", freq="Q")
t = quarters.year + (quarters.quarter - 1) / 4
# Anchor points (year, %) for the policy rate (short end) and the 10-year yield (long end).
short_pts = [(2000, 6.3), (2001.5, 3.5), (2003, 1.0), (2004.5, 1.3), (2006.5, 5.2), (2007.5, 5.0),
             (2008.9, 0.1), (2015.9, 0.2), (2018.9, 2.4), (2019.6, 2.0), (2020.2, 0.1), (2022.0, 0.1),
             (2022.5, 1.6), (2023.5, 5.3), (2024.6, 5.3), (2025.9, 4.0)]
long_pts = [(2000, 6.0), (2003, 4.0), (2006, 4.8), (2008, 3.8), (2012, 1.8), (2014, 2.5), (2016, 1.8),
            (2018, 2.9), (2020, 0.9), (2021, 1.5), (2022, 3.6), (2023, 4.1), (2024, 4.2), (2025.9, 4.4)]
short = np.interp(t, *zip(*short_pts)) + rng.normal(0, 0.05, len(t))
long = np.interp(t, *zip(*long_pts)) + rng.normal(0, 0.08, len(t))

maturities = ["1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
years_to_mat = np.array([1/12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
tau = 2.0
shape = (1 - np.exp(-years_to_mat / tau)) / (years_to_mat / tau)    # Nelson-Siegel slope loading
shape10 = (1 - np.exp(-10 / tau)) / (10 / tau)
curves = pd.DataFrame(
    [lng + (sht - lng) * (shape - shape10) / (1 - shape10) + 0.15 * (years_to_mat > 10) for sht, lng in zip(short, long)],
    index=quarters.strftime("%Y Q%q"), columns=maturities).clip(lower=0.02).round(2)
curves["10y-2y"] = curves["10Y"] - curves["2Y"]
curves = curves.iloc[3::4]                                # one frame per year: the year-end (Q4) curve
curves.index = curves.index.str[:4]
curves.iloc[::5]

# --- Plot --------------------------------------------------------------------
TRAIL = 3  # previous years shown faintly
labels = list(curves.index)


def frame_traces(i):
    traces = []
    for k in range(TRAIL, 0, -1):  # always the same number of traces: full traces in every frame
        j = i - k
        y = curves.iloc[j][maturities] if j >= 0 else [None] * len(maturities)
        traces.append(go.Scatter(x=maturities, y=y, mode="lines", hoverinfo="skip",
                                 line=dict(color="#b8b7b1", width=1), opacity=0.25 + 0.15 * (TRAIL - k)))
    inverted = curves["10y-2y"].iloc[i] < 0
    traces.append(go.Scatter(x=maturities, y=curves.iloc[i][maturities], mode="lines+markers",
                             line=dict(color=PALETTE[1] if inverted else PALETTE[0], width=3),
                             marker=dict(size=7), hovertemplate="%{x}: %{y:.2f}%<extra></extra>"))
    return traces


def frame_title(i):
    spread = curves["10y-2y"].iloc[i]
    state = "INVERTED" if spread < 0 else "normal"
    return f"US Treasury curve (simulated), end of {labels[i]}  ·  10y–2y {spread:+.2f} pp  ·  {state}"


fig = go.Figure(
    data=frame_traces(0),
    frames=[go.Frame(data=frame_traces(i), name=labels[i], layout=dict(title_text=frame_title(i)))
            for i in range(len(curves))],
)
fig.update_layout(
    title_text=frame_title(0), showlegend=False, height=560,
    xaxis=dict(title="Maturity", type="category"),
    yaxis=dict(title="Yield (%)", range=[0, 7.2]),
    updatemenus=[dict(type="buttons", x=0, y=-0.12, xanchor="left", direction="left", buttons=[
        dict(label="▶ Play", method="animate",
             args=[None, dict(frame=dict(duration=450, redraw=False), fromcurrent=True, transition=dict(duration=0))]),
        dict(label="❚❚ Pause", method="animate",
             args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])])],
    sliders=[dict(x=0.17, y=-0.08, len=0.83, currentvalue=dict(visible=False),
                  steps=[dict(label=lab if int(lab) % 5 == 0 else "", method="animate",
                              args=[[lab], dict(mode="immediate", frame=dict(duration=0, redraw=False))])
                         for lab in labels])],
    margin=dict(b=110),
)

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".html")
fig.write_html(out, include_plotlyjs="cdn", div_id="animated_yield_curve")
try:  # static preview; needs kaleido + a local Chrome
    fig.write_image(out.with_suffix(".png"), width=1000, height=620, scale=1.5)
except Exception:
    pass
try:  # animated: also write a GIF preview from the frames (kaleido + Pillow)
    import io
    from PIL import Image
    still = go.Figure(fig)
    still.layout.updatemenus, still.layout.sliders = (), ()  # no play controls in a GIF
    step = max(1, len(fig.frames) // 40)
    images = []
    for frame in fig.frames[::step]:
        still.update(data=list(frame.data), layout=frame.layout)
        png = still.to_image(format="png", width=900, height=560)
        images.append(Image.open(io.BytesIO(png)).convert("P", palette=Image.ADAPTIVE))
    images[0].save(out.with_suffix(".gif"), save_all=True, append_images=images[1:],
                   duration=int(1000 / 6), loop=0)
except Exception as exc:
    print(f"GIF preview skipped: {exc}")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    fig.show()
