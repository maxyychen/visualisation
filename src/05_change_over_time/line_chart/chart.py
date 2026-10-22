# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(1)
dates = pd.date_range("2022-01", periods=36, freq="MS")
t = np.arange(36)
df = pd.DataFrame({
    "date": dates,
    "App A": 120 + 4.0 * t + rng.normal(0, 6, 36),
    "App B": 180 + 1.2 * t + 15 * np.sin(t / 3) + rng.normal(0, 6, 36),
    "App C": 60 + 0.15 * t ** 2 + rng.normal(0, 5, 36),
}).set_index("date")
labels = dict(y="Monthly active users (k)", title="Monthly active users by app")
df.head()

# %% plot
fig, ax = plt.subplots(figsize=(9, 4.8))
for i, col in enumerate(df.columns):
    ax.plot(df.index, df[col], color=PALETTE[i], label=col)
    ax.text(df.index[-1] + pd.Timedelta(days=12), df[col].iloc[-1], col,
            color="#0b0b0b", va="center", fontsize=10)
ax.set_ylabel(labels["y"])
ax.set_title(labels["title"])
ax.set_xlim(df.index[0], df.index[-1] + (df.index[-1] - df.index[0]) * 0.09)
ax.legend(loc="upper left")
fig.tight_layout()

# %% real-data
import plotly.express as px
df = (px.data.stocks().assign(date=lambda d: pd.to_datetime(d["date"]))
        .set_index("date")[["GOOG", "AAPL", "AMZN"]])
labels = dict(y="Share price (1 Jan 2018 = 1)", title="Weekly share prices, 2018–2019")
df.head()

# %% alt:plotly
import plotly.express as px
long = df.reset_index().melt(id_vars=df.index.name or "index", var_name="series", value_name="value")
fig = px.line(long, x=long.columns[0], y="value", color="series", color_discrete_sequence=PALETTE,
              labels={"value": labels["y"], long.columns[0]: ""}, title=labels["title"])
fig.update_layout(hovermode="x unified")
fig.show()

# %% alt:altair
import altair as alt
long = df.reset_index().melt(id_vars=df.index.name or "index", var_name="series", value_name="value")
xcol = long.columns[0]
hover = alt.selection_point(fields=[xcol], nearest=True, on="pointerover", empty=False)
lines = alt.Chart(long).mark_line(strokeWidth=2).encode(
    x=alt.X(f"{xcol}:T", title=None), y=alt.Y("value:Q", title=labels["y"]),
    color=alt.Color("series:N", title=None))
rule = alt.Chart(long).mark_rule(color="#b8b7b1").encode(
    x=f"{xcol}:T", opacity=alt.condition(hover, alt.value(1), alt.value(0)),
    tooltip=[alt.Tooltip(f"{xcol}:T"), "series:N", alt.Tooltip("value:Q", format=".2f")]).add_params(hover)
chart = (lines + rule).properties(title=labels["title"], width=560, height=300)
chart
