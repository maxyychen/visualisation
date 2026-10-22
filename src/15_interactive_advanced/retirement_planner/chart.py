# %% setup
from vizlib.altair_style import *  # noqa: F401,F403  (inlined on build)

# %% data
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

# %% plot
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
