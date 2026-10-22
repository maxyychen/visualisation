# %% setup
from vizlib.altair_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(5)
n = 756  # three years of trading days
day = np.arange(n)
daily_vol = np.where((day > 300) & (day < 430), 0.026, 0.010)  # a turbulent stretch
ret = rng.normal(0.0004, daily_vol)
prices = pd.DataFrame({"date": pd.bdate_range("2022-01-03", periods=n),
                       "price": (100 * np.cumprod(1 + ret)).round(2), "ret": ret.round(5)})
prices.head()

# %% plot
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
