"""
Crossfilter Dashboard (every view filters the others)  -  family: Interactive, animated & big data

DESIGN PURPOSE
Three coordinated views of one sales table: by region, by product and by
month. Clicking a region or product, or brushing a range of months, filters
the other two views, while gray bars keep the unfiltered totals for context. A
headline states the filtered total and its share. Many-dimensional questions
get answered without writing a single group-by.

WHEN TO USE
  - Exploratory analysis of a cube (region × product × time) by business users
  - Find which combination drives a change ("is the Q4 jump all Phones in the
    West?")
  - Replace a stack of pivot tables with one interactive page

AVOID WHEN
  - A one-message presentation (state the finding with one static chart)
  - More than four or five dimensions (the page becomes a puzzle; use a BI
    tool)
  - Readers on paper or static slides

ALTERNATIVES
  - Small multiples
  - Highlight table (region × product)
  - Stacked area by product

EXAMPLE
Simulated monthly sales ($k) for four regions and five product lines over two
years, with seasonality, growth and a strong Q4 for Phones in the West.

Run:  python crossfilter_dashboard.py
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
rng = np.random.default_rng(31)
regions = {"North": 1.0, "South": 0.8, "East": 1.15, "West": 1.3}
products = {"Laptops": 120, "Phones": 160, "Tablets": 60, "Accessories": 45, "Services": 70}
months = pd.date_range("2023-01-01", periods=24, freq="MS")
rows = []
for region, rw in regions.items():
    for product, base in products.items():
        for i, m in enumerate(months):
            season = 1 + 0.25 * (m.month in (11, 12)) + 0.08 * np.sin(2 * np.pi * m.month / 12)
            boost = 1.6 if (region == "West" and product == "Phones" and m.month in (11, 12)) else 1.0
            sales = base * rw * season * boost * (1 + 0.01 * i) * rng.lognormal(0, 0.08)
            rows.append({"region": region, "product": product, "month": m, "sales": round(sales, 1)})
sales = pd.DataFrame(rows)
sales.pivot_table(index="product", columns="region", values="sales", aggfunc="sum").round(0)

# --- Plot --------------------------------------------------------------------
region_pick = alt.selection_point(fields=["region"], name="region_pick")
product_pick = alt.selection_point(fields=["product"], name="product_pick")
months_brush = alt.selection_interval(encodings=["x"], name="months_brush")
base = alt.Chart(sales)
region_order, product_order = list(regions), list(products)


def bar_view(field, order, own, others, title):
    y = alt.Y(f"{field}:N", sort=order, title=None)
    x = alt.X("sum(sales):Q", title="Sales ($k)")
    back = base.mark_bar(color="#e3e2de", height=20, cornerRadiusEnd=3).encode(y=y, x=x)
    front = base.mark_bar(color=PALETTE[0], height=20, cornerRadiusEnd=3).encode(
        y=y, x=x, opacity=alt.condition(own, alt.value(1), alt.value(0.35)),
        tooltip=[f"{field}:N", alt.Tooltip("sum(sales):Q", title="Filtered sales ($k)", format=",.0f")])
    for sel in others:
        front = front.transform_filter(sel)
    return alt.layer(back, front.add_params(own)).properties(
        width=300, height=170, title=alt.Title(title, fontSize=12))


region_view = bar_view("region", region_order, region_pick, [product_pick, months_brush], "By region (click)")
product_view = bar_view("product", product_order, product_pick, [region_pick, months_brush], "By product (click)")

x = alt.X("yearmonth(month):T", title=None)
y = alt.Y("sum(sales):Q", title="Sales ($k)")
month_view = alt.layer(
    base.mark_bar(color="#e3e2de").encode(x=x, y=y).add_params(months_brush),
    base.transform_filter(region_pick).transform_filter(product_pick).mark_bar(color=PALETTE[0]).encode(
        x=x, y=y, tooltip=[alt.Tooltip("yearmonth(month):T", title="Month"),
                           alt.Tooltip("sum(sales):Q", title="Filtered sales ($k)", format=",.0f")]),
).properties(width=690, height=180, title=alt.Title("By month (drag to brush a range)", fontSize=12))

headline = (base.transform_joinaggregate(total="sum(sales)")
            .transform_filter(region_pick).transform_filter(product_pick).transform_filter(months_brush)
            .transform_aggregate(selected="sum(sales)", total="max(total)")
            .transform_calculate(label="'Selected sales: $' + format(datum.selected / 1000, ',.2f') + 'M  ·  '"
                                       " + format(datum.selected / datum.total, '.0%') + ' of the two-year total'")
            .mark_text(align="left", fontSize=15, fontWeight="bold")
            .encode(x=alt.value(0), y=alt.value(0), text="label:N")
            .properties(width=690, height=12))

chart = alt.vconcat(headline, alt.hconcat(region_view, product_view, spacing=60), month_view, spacing=22).properties(
    title=alt.Title("Sales crossfilter: every view filters the others (simulated)", subtitle=[
        "Click bars (shift-click for several) and brush months; double-click a view to clear it.", " "]))

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".html")
chart.save(out)
chart.save(out.with_suffix(".png"), scale_factor=2)  # static preview (vl-convert)
print(f"saved {out}")
if "--no-show" not in sys.argv:
    import webbrowser
    webbrowser.open(out.resolve().as_uri())
