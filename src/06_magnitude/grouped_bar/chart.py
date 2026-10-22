# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = pd.DataFrame({
    "region": ["North", "South", "East", "West", "Central"],
    "2022": [42, 35, 28, 50, 22],
    "2023": [48, 33, 34, 55, 25],
    "2024": [55, 31, 41, 57, 30],
}).set_index("region")
labels = dict(y="Sales ($M)", legend="Year", title="Sales by region and year")
df

# %% plot
fig, ax = plt.subplots(figsize=(9, 4.8))
n = len(df.columns)
width = 0.8 / n
x = np.arange(len(df))
for i, col in enumerate(df.columns):
    ax.bar(x + (i - (n - 1) / 2) * width, df[col], width=width * 0.92,
           color=PALETTE[i], label=col)
ax.set_xticks(x, df.index)
ax.set_ylabel(labels["y"])
ax.grid(axis="x", visible=False)
ax.legend(title=labels["legend"], ncol=n, loc="upper left")
ax.set_ylim(0, df.values.max() * 1.3)
ax.set_title(labels["title"])
fig.tight_layout()

# %% real-data
import plotly.express as px
m = px.data.medals_long()
df = (m.pivot(index="nation", columns="medal", values="count")[["gold", "silver", "bronze"]]
        .rename(columns=str.title).rename_axis(index=None, columns=None))
labels = dict(y="Medals", legend=None, title="2018 Winter Olympics short-track medals")
df

# %% alt:plotly
import plotly.express as px
long = df.rename_axis("group").reset_index().melt(id_vars="group", var_name="series", value_name="value")
fig = px.bar(long, x="group", y="value", color="series", barmode="group",
             color_discrete_sequence=PALETTE, title=labels["title"],
             labels={"group": "", "value": labels["y"], "series": labels["legend"] or ""})
fig.show()

# %% alt:altair
import altair as alt
long = df.rename_axis("group").reset_index().melt(id_vars="group", var_name="series", value_name="value")
chart = alt.Chart(long).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
    x=alt.X("group:N", title=None, sort=list(df.index), axis=alt.Axis(labelAngle=0)),
    xOffset=alt.XOffset("series:N", sort=list(df.columns)),
    y=alt.Y("value:Q", title=labels["y"]),
    color=alt.Color("series:N", title=labels["legend"], sort=list(df.columns)),
    tooltip=["group", "series", "value"],
).properties(title=labels["title"], width=480, height=300)
chart
