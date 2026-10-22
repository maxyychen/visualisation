"""
Retirement Planner (Monte Carlo what-if)  -  family: Interactive, animated & big data

DESIGN PURPOSE
An interactive Monte Carlo fan chart. Sliders set expected return, volatility
and annual spending; the fan shows the range of portfolio values from 65 to
95, and a side panel shows the probability that the money lasts. Uncertainty
is the message: readers see the spread of outcomes and how fast success falls
as spending rises, instead of one optimistic projection.

WHEN TO USE
  - Financial planning conversations about a sustainable withdrawal rate
  - Show how sensitive an outcome is to assumptions (return, volatility,
    spending)
  - Replace a single straight-line projection with a range of plausible
    outcomes

AVOID WHEN
  - The audience reads the median as a promise (label the fan and state the
    probability)
  - Assumptions are unknown or contested (show a static scenario comparison
    instead)
  - Precise tax or fee modelling is needed (this simulator ignores both)

ALTERNATIVES
  - Monte Carlo wealth fan (static, in Finance & investment)
  - Fan chart (forecast uncertainty)
  - Quantile dot plot (single outcome)

EXAMPLE
Simulated: a $1.5M portfolio at age 65, withdrawing a fixed nominal amount
each year to 95, with 2,000 random return paths for each of 210 slider
combinations (normal annual returns, no tax or fees). Illustrative only, not
financial advice.

Run:  python retirement_planner.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import altair as alt

PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
           "#e87ba4", "#008300", "#6250d6", "#e34948"]


@alt.theme.register("vizlib", enable=True)
def vizlib_theme():
    return alt.theme.ThemeConfig({
        "config": {
            "background": "#fcfcfb",
            "view": {"stroke": None},
            "range": {"category": PALETTE},
            "font": "Helvetica, Arial, sans-serif",
            "title": {"anchor": "start", "fontSize": 14, "color": "#0b0b0b"},
            "axis": {"gridColor": "#e6e5e1", "domainColor": "#c9c8c3", "tickColor": "#c9c8c3",
                     "labelColor": "#52514e", "titleColor": "#52514e", "titleFontWeight": "normal"},
            "legend": {"labelColor": "#52514e", "titleColor": "#52514e"},
        }
    })

# --- Example data ------------------------------------------------------------
# Precompute the Monte Carlo on a grid of slider values (the browser only filters it).
rng = np.random.default_rng(7)
start_age, years, n_paths, start = 65, 30, 2000, 1_500_000
z = rng.standard_normal((n_paths, years))  # common random numbers for every grid point
fan_rows, success_rows = [], []
for ret in range(2, 9):                      # expected annual return, %
    for vol in (6, 9, 12, 15, 18):           # annual volatility, %
        growth = 1 + ret / 100 + vol / 100 * z
        for spend in range(40, 100, 10):     # annual withdrawal, $k
            wealth = np.full(n_paths, float(start))
            path = [wealth]
            for t in range(years):
                wealth = np.maximum(wealth * growth[:, t] - spend * 1000, 0)
                path.append(wealth)
            q = np.percentile(np.array(path), [10, 25, 50, 75, 90], axis=1) / 1e6
            for t in range(years + 1):
                fan_rows.append((ret, vol, spend, start_age + t, *q[:, t]))
            success_rows.append((ret, vol, spend, float((wealth > 0).mean())))
fan = pd.DataFrame(fan_rows, columns=["ret", "vol", "spend", "age", "p10", "p25", "p50", "p75", "p90"]).round(4)
success = pd.DataFrame(success_rows, columns=["ret", "vol", "spend", "success"])
success.query("ret == 5 and vol == 12")

# --- Plot --------------------------------------------------------------------
alt.data_transformers.disable_max_rows()
ret = alt.param(name="ret", value=5, bind=alt.binding_range(min=2, max=8, step=1, name="Expected return (%/yr) "))
vol = alt.param(name="vol", value=12, bind=alt.binding_range(min=6, max=18, step=3, name="Volatility (%/yr) "))
spend = alt.param(name="spend", value=70, bind=alt.binding_range(min=40, max=90, step=10, name="Spending ($k/yr) "))
chosen = "datum.ret == ret && datum.vol == vol && datum.spend == spend"
same_market = "datum.ret == ret && datum.vol == vol"

x = alt.X("age:Q", title="Age", scale=alt.Scale(domain=[65, 95]))
band = alt.Chart(fan).transform_filter(chosen)
fan_chart = alt.layer(
    band.mark_area(color=PALETTE[0], opacity=0.15).encode(x=x, y=alt.Y("p10:Q", title="Portfolio value ($M)"), y2="p90"),
    band.mark_area(color=PALETTE[0], opacity=0.3).encode(x=x, y="p25:Q", y2="p75"),
    band.mark_line(color=PALETTE[0], strokeWidth=2.5).encode(
        x=x, y="p50:Q", tooltip=["age:Q", alt.Tooltip("p50:Q", title="Median ($M)", format=".2f")]),
    alt.Chart(success).transform_filter(chosen)
    .transform_calculate(label="'Probability the money lasts to 95: ' + format(datum.success, '.0%')")
    .mark_text(align="left", fontSize=15, fontWeight="bold").encode(x=alt.value(0), y=alt.value(-14), text="label:N"),
).properties(width=470, height=320)

line = alt.Chart(success).transform_filter(same_market).encode(
    x=alt.X("spend:Q", title="Annual spending ($k)", scale=alt.Scale(domain=[35, 95])),
    y=alt.Y("success:Q", title="Probability of success", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 1])))
success_chart = alt.layer(
    line.mark_line(color="#8f8e88"),
    line.mark_point(filled=True, opacity=1, stroke="#fcfcfb", strokeWidth=1.5).encode(
        size=alt.condition("datum.spend == spend", alt.value(220), alt.value(50)),
        color=alt.condition("datum.spend == spend", alt.value(PALETTE[0]), alt.value("#8f8e88")),
        tooltip=["spend:Q", alt.Tooltip("success:Q", format=".0%")]),
).properties(width=230, height=320, title=alt.Title("Success vs. spending", fontSize=12))

chart = (
    alt.hconcat(fan_chart, success_chart, spacing=40)
    .add_params(ret, vol, spend)
    .properties(title=alt.Title("Retirement planner: $1.5M at 65, spending to 95 (simulated)", subtitle=[
        "Bands: middle 50% and 80% of 2,000 simulated paths; line: median. Move the sliders below.", " "]))
)

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".html")
chart.save(out)
chart.save(out.with_suffix(".png"), scale_factor=2)  # static preview (vl-convert)
print(f"saved {out}")
if "--no-show" not in sys.argv:
    import webbrowser
    webbrowser.open(out.resolve().as_uri())
