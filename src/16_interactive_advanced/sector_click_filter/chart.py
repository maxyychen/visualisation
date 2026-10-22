# %% setup
from vizlib.altair_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(12)
sectors = {  # (mean one-year return, typical volatility)
    "Technology": (0.18, 0.34), "Industrials": (0.08, 0.24), "Financials": (0.09, 0.26),
    "Consumer": (0.05, 0.25), "Health care": (0.04, 0.22), "Utilities": (0.02, 0.15),
    "Materials": (-0.04, 0.28), "Energy": (-0.08, 0.33)}
rows = []
for sector, (mu, vol) in sectors.items():
    for i in range(9):
        rows.append({"ticker": f"{sector[:3].upper()}{i + 1}", "sector": sector,
                     "ret": round(rng.normal(mu, 0.09), 4), "vol": round(abs(rng.normal(vol, 0.045)), 4)})
stocks = pd.DataFrame(rows)
stocks.groupby("sector")[["ret", "vol"]].mean().round(3).sort_values("ret", ascending=False)

# %% plot
pick = alt.selection_point(fields=["sector"], name="pick")
order = stocks.groupby("sector")["ret"].mean().sort_values(ascending=False).index.tolist()

bars = (alt.Chart(stocks).mark_bar(cornerRadiusEnd=4, height=22)
        .encode(y=alt.Y("sector:N", sort=order, title=None),
                x=alt.X("mean(ret):Q", title="Average 1-year return", axis=alt.Axis(format="%")),
                color=alt.condition("datum.mean_ret >= 0", alt.value(PALETTE[0]), alt.value(PALETTE[1])),
                opacity=alt.condition(pick, alt.value(1), alt.value(0.3)),
                tooltip=["sector:N", alt.Tooltip("mean(ret):Q", title="Avg return", format=".1%")])
        .transform_joinaggregate(mean_ret="mean(ret)", groupby=["sector"])
        .add_params(pick)
        .properties(width=250, height=330, title=alt.Title("Click a sector", fontSize=12)))

scatter = (alt.Chart(stocks).mark_circle(size=90, stroke="#fcfcfb", strokeWidth=1)
           .encode(x=alt.X("vol:Q", title="Volatility (1-year)", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 0.5])),
                   y=alt.Y("ret:Q", title="1-year return", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[-0.35, 0.45])),
                   color=alt.condition(pick, alt.value(PALETTE[0]), alt.value("#d0cfca")),
                   opacity=alt.condition(pick, alt.value(0.95), alt.value(0.5)),
                   order=alt.condition(pick, alt.value(1), alt.value(0)),
                   tooltip=["ticker:N", "sector:N", alt.Tooltip("ret:Q", format="+.1%"), alt.Tooltip("vol:Q", format=".0%")])
           .properties(width=440, height=330, title=alt.Title("Stocks: risk vs. return", fontSize=12)))
zero = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="#8f8e88").encode(y="y:Q")

chart = alt.hconcat(bars, scatter + zero, spacing=40).properties(
    title=alt.Title("From sector to stock: what drove each sector? (simulated)", subtitle=[
        "Click a bar to highlight its stocks; shift-click to add sectors; click empty space to reset.", " "]))
