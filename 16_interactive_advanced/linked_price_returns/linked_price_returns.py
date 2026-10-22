"""
Linked Price & Returns (brush to select a window)  -  family: Interactive, animated & big data

DESIGN PURPOSE
Two linked views of one price history. Dragging across the price chart selects
a time window, and the histogram of daily returns and the summary statistics
update to show only that window, against the full-period distribution in gray.
The reader asks "what was risk like during that episode?" by pointing at it.

WHEN TO USE
  - Compare return distributions across calm and turbulent periods
  - Explore a long price history before choosing the window for a formal
    analysis
  - Show non-specialists that volatility changes over time

AVOID WHEN
  - Static reports (pick the windows yourself and show small multiples)
  - Very short histories, where a selected window has too few returns for a
    meaningful histogram

ALTERNATIVES
  - Rolling volatility chart
  - Return distribution with VaR (static)

EXAMPLE
Simulated daily prices over three years with a turbulent stretch in the
middle, where daily volatility more than doubles.

Run:  python linked_price_returns.py
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
rng = np.random.default_rng(5)
n = 756  # three years of trading days
day = np.arange(n)
daily_vol = np.where((day > 300) & (day < 430), 0.026, 0.010)  # a turbulent stretch
ret = rng.normal(0.0004, daily_vol)
prices = pd.DataFrame({"date": pd.bdate_range("2022-01-03", periods=n),
                       "price": (100 * np.cumprod(1 + ret)).round(2), "ret": ret.round(5)})
prices.head()

# --- Plot --------------------------------------------------------------------
alt.data_transformers.disable_max_rows()
window = alt.selection_interval(encodings=["x"], name="window")

price_chart = (alt.Chart(prices).mark_line(color=PALETTE[0], strokeWidth=1.5)
               .encode(x=alt.X("date:T", title=None), y=alt.Y("price:Q", title="Price ($)", scale=alt.Scale(zero=False)),
                       tooltip=[alt.Tooltip("date:T"), alt.Tooltip("price:Q", format="$.2f")])
               .add_params(window)
               .properties(width=720, height=220, title=alt.Title("Drag across the price chart to select a window", fontSize=12)))

bins = alt.Bin(extent=[-0.08, 0.08], step=0.004)
hx = alt.X("ret:Q", bin=bins, title="Daily return", axis=alt.Axis(format="%"))
hist = alt.layer(
    alt.Chart(prices).mark_bar(color="#d0cfca").encode(x=hx, y=alt.Y("count():Q", title="Days")),
    alt.Chart(prices).transform_filter(window).mark_bar(color=PALETTE[0]).encode(
        x=hx, y="count():Q", tooltip=[alt.Tooltip("count():Q", title="Days in window")]),
).properties(width=720, height=200, title=alt.Title("Daily returns: selected window (blue) vs. full period (gray)", fontSize=12))

stats = (alt.Chart(prices).transform_filter(window)
         .transform_calculate(lr="log(1 + datum.ret)")
         .transform_aggregate(n="count()", lr="sum(lr)", sd="stdev(ret)", worst="min(ret)", start="min(date)", end="max(date)")
         .transform_calculate(label="timeFormat(datum.start, '%b %d %Y') + ' – ' + timeFormat(datum.end, '%b %d %Y')"
                                    " + '  ·  ' + datum.n + ' days  ·  return ' + format(exp(datum.lr) - 1, '+.1%')"
                                    " + '  ·  volatility ' + format(datum.sd * sqrt(252), '.0%') + ' a year'"
                                    " + '  ·  worst day ' + format(datum.worst, '.1%')")
         .mark_text(align="left", fontSize=14, fontWeight="bold")
         .encode(x=alt.value(0), y=alt.value(0), text="label:N")
         .properties(width=720, height=12))

chart = alt.vconcat(price_chart, stats, hist, spacing=18).properties(
    title=alt.Title("Linked views: how risky was that period? (simulated prices)", subtitle=[" "]))

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".html")
chart.save(out)
chart.save(out.with_suffix(".png"), scale_factor=2)  # static preview (vl-convert)
print(f"saved {out}")
if "--no-show" not in sys.argv:
    import webbrowser
    webbrowser.open(out.resolve().as_uri())
