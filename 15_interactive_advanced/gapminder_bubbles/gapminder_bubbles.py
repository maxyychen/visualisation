"""
Animated Bubble Chart (Gapminder)  -  family: Interactive, animated & big data

DESIGN PURPOSE
An animated scatter of two measures, with bubble area for a third (population)
and color for a group, stepping through time. Hans Rosling made it famous to
show countries' wealth and health converging. Every country's path is visible
at once, which a static chart cannot show without clutter.

WHEN TO USE
  - Show how many entities move through a two-measure space over time (wealth
    vs. health, risk vs. return)
  - Tell a development or convergence story to a general audience
  - Explore a panel dataset interactively (hover, pause, scrub)

AVOID WHEN
  - Precise year-to-year comparisons are needed (use connected scatter for a
    few entities)
  - There are too few frames or entities for motion to matter
  - The medium is static print

ALTERNATIVES
  - Connected scatter (a few entities over time)
  - Small multiples of the scatter at key years
  - Bubble chart (one year)

EXAMPLE
Real data: Gapminder life expectancy, GDP per capita and population for 142
countries, 1952–2007, bundled offline with plotly (`px.data.gapminder()`).

Run:  python gapminder_bubbles.py
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
df = px.data.gapminder()
continents = ["Asia", "Europe", "Africa", "Americas", "Oceania"]
df.query("year == 2007").sort_values("pop", ascending=False).head()

# --- Plot --------------------------------------------------------------------
fig = px.scatter(
    df, x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="country",
    animation_frame="year", animation_group="country", log_x=True, size_max=55,
    range_x=[200, 60000], range_y=[25, 88],
    category_orders={"continent": continents}, color_discrete_sequence=PALETTE,
    labels={"gdpPercap": "GDP per capita (US$, log scale)", "lifeExp": "Life expectancy (years)",
            "continent": "Continent"},
    title="Wealth and health of nations, 1952–2007",
)
fig.update_traces(marker=dict(line=dict(width=0.6, color="#fcfcfb")))
fig.update_layout(height=600)
for frame in fig.frames:  # put the year in the title so every frame (and GIF still) is dated
    frame.layout = go.Layout(title_text=f"Wealth and health of nations, {frame.name}")
fig.update_layout(title_text="Wealth and health of nations, 1952")
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 400

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".html")
fig.write_html(out, include_plotlyjs="cdn", div_id="gapminder_bubbles")
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
