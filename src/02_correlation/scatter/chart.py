# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(42)
n = 150
height_f = rng.normal(163, 6.5, n)
height_m = rng.normal(177, 7, n)
df = pd.DataFrame({
    "height_cm": np.r_[height_f, height_m],
    "weight_kg": np.r_[0.62 * height_f - 40 + rng.normal(0, 6, n),
                       0.75 * height_m - 55 + rng.normal(0, 7, n)],
    "sex": ["Female"] * n + ["Male"] * n,
})
x, y, hue = "height_cm", "weight_kg", "sex"
labels = dict(x="Height (cm)", y="Weight (kg)", title="Height vs. weight of 300 adults")
df.head()

# %% plot
fig, ax = plt.subplots(figsize=(7.5, 5.5))
for color, (name, g) in zip(PALETTE, df.groupby(hue)):
    ax.scatter(g[x], g[y], s=28, alpha=0.65, color=color,
               edgecolor="#fcfcfb", linewidth=0.6, label=name)
ax.set_xlabel(labels["x"])
ax.set_ylabel(labels["y"])
ax.set_title(labels["title"])
ax.legend(title=None, loc="upper left")
fig.tight_layout()

# %% real-data
import plotly.express as px
df = px.data.tips()                     # 244 restaurant bills (Bryant & Smith, 1995)
x, y, hue = "total_bill", "tip", "sex"
labels = dict(x="Total bill ($)", y="Tip ($)", title="Tip vs. bill size, 244 restaurant bills")
df.head()

# %% alt:plotly
import plotly.express as px
fig = px.scatter(df, x=x, y=y, color=hue, opacity=0.7, color_discrete_sequence=PALETTE,
                 labels={x: labels["x"], y: labels["y"]}, title=labels["title"])
fig.update_traces(marker=dict(size=8, line=dict(color="#fcfcfb", width=0.6)))
fig.show()

# %% alt:altair
import altair as alt
chart = alt.Chart(df).mark_circle(size=40, opacity=0.65).encode(
    x=alt.X(x, title=labels["x"], scale=alt.Scale(zero=False)),
    y=alt.Y(y, title=labels["y"], scale=alt.Scale(zero=False)),
    color=alt.Color(hue, title=None),
    tooltip=[x, y, hue],
).properties(title=labels["title"], width=480, height=340).interactive()
chart
