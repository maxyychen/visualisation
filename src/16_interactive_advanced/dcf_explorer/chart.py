# %% setup
from vizlib.altair_style import *  # noqa: F401,F403  (inlined on build)

# %% data
base_revenue, shares, net_debt, price = 1000.0, 100.0, 300.0, 36.0  # $m, millions, $m, $
plan = pd.DataFrame({"year": [1, 2, 3, 4, 5], "growth": [0.12, 0.10, 0.08, 0.06, 0.05]})
plan["revenue"] = (base_revenue * np.cumprod(1 + plan["growth"])).round(1)
plan

# %% plot
wacc = alt.param(name="wacc", value=0.09, bind=alt.binding_range(min=0.06, max=0.14, step=0.0025, name="WACC "))
tg = alt.param(name="tg", value=0.025, bind=alt.binding_range(min=0.0, max=0.04, step=0.0025, name="Terminal growth "))
margin = alt.param(name="margin", value=0.18, bind=alt.binding_range(min=0.10, max=0.30, step=0.01, name="FCF margin "))

flows = (alt.Chart(plan)
         .transform_calculate(fcf="datum.revenue * margin")
         .transform_calculate(pv="datum.fcf / pow(1 + wacc, datum.year)",
                              tv_pv="datum.year == 5 ? datum.fcf * (1 + tg) / (wacc - tg) / pow(1 + wacc, 5) : 0"))

value = (flows
         .transform_aggregate(pv_sum="sum(pv)", tv="sum(tv_pv)")
         .transform_calculate(ok="wacc > tg + 0.005")
         .transform_calculate(per_share=f"datum.ok ? (datum.pv_sum + datum.tv - {net_debt}) / {shares} : null",
                              tv_share="datum.tv / (datum.pv_sum + datum.tv)")
         .transform_calculate(upside=f"datum.per_share / {price} - 1",
                              label=f"datum.ok ? 'Implied value $' + format(datum.per_share, '.2f') + ' vs. price ${price:.0f}  →  '"
                                    " + format(datum.per_share / " + str(price) + " - 1, '+.0%')"
                                    " + '   ·   terminal value = ' + format(datum.tv_share, '.0%') + ' of enterprise value'"
                                    " : 'WACC must exceed terminal growth'"))
xv = alt.X("per_share:Q", title="Value per share ($)", scale=alt.Scale(domain=[0, 100]))
value_chart = alt.layer(
    value.mark_bar(height=26, cornerRadiusEnd=4).encode(
        x=xv, color=alt.condition("datum.upside >= 0", alt.value(PALETTE[0]), alt.value(PALETTE[1])),
        tooltip=[alt.Tooltip("per_share:Q", format="$.2f"), alt.Tooltip("upside:Q", format="+.0%")]),
    alt.Chart(pd.DataFrame({"p": [price]})).mark_rule(color="#0b0b0b", strokeWidth=2).encode(
        x=alt.X("p:Q", scale=alt.Scale(domain=[0, 100]))),
    alt.Chart(pd.DataFrame({"p": [price]})).mark_text(align="left", dx=4, dy=-24, fontSize=11).encode(
        x=alt.X("p:Q", scale=alt.Scale(domain=[0, 100])), text=alt.value(f"Price ${price:.0f}")),
    value.mark_text(align="left", fontSize=14, fontWeight="bold").encode(
        x=alt.value(0), y=alt.value(-30), text="label:N"),
).properties(width=640, height=50)

bars = (flows
        .transform_fold(["fcf", "pv"], as_=["kind", "amount"])
        .transform_calculate(kind="datum.kind == 'fcf' ? 'Free cash flow' : 'Present value'")
        .mark_bar(cornerRadiusEnd=3)
        .encode(x=alt.X("year:O", title="Forecast year", axis=alt.Axis(labelAngle=0)),
                xOffset=alt.XOffset("kind:N", sort=["Free cash flow", "Present value"]),
                y=alt.Y("amount:Q", title="$ millions", scale=alt.Scale(domain=[0, 500])),
                color=alt.Color("kind:N", title=None, sort=["Free cash flow", "Present value"],
                                scale=alt.Scale(range=["#b8b7b1", PALETTE[0]]),
                                legend=alt.Legend(orient="top", direction="horizontal")),
                tooltip=["year:O", "kind:N", alt.Tooltip("amount:Q", format=",.0f")])
        .properties(width=640, height=230))

chart = (
    alt.vconcat(value_chart, bars, spacing=30)
    .resolve_scale(color="independent")
    .resolve_legend(color="independent")
    .add_params(wacc, tg, margin)
    .properties(title=alt.Title("DCF explorer: what is the company worth per share?", subtitle=[
        "Illustrative five-year DCF with a Gordon-growth terminal value. Move the sliders below.", " ", " "]))
)
