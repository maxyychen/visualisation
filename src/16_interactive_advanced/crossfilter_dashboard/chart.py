# %% setup
from vizlib.altair_style import *  # noqa: F401,F403  (inlined on build)

# %% data
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

# %% plot
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
