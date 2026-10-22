# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = pd.DataFrame({
    "country": ["Japan", "Taiwan", "Germany", "USA", "China", "Brazil",
                "India", "Russia", "South Africa", "Nigeria"],
    "y2000": [81.2, 76.5, 78.0, 76.8, 71.4, 70.1, 62.7, 65.3, 55.9, 46.3],
    "y2022": [84.0, 79.8, 80.7, 77.5, 78.6, 73.4, 67.7, 70.1, 61.5, 53.6],
})
start, end = "y2000", "y2022"
title = "Life expectancy rose everywhere, but gaps remain"
df["gain"] = df[end] - df[start]
df = df.sort_values(end).reset_index(drop=True)
df

# %% plot
fig, ax = plt.subplots(figsize=(8, 5.5))
ax.hlines(df.index, df[start], df[end], color="#c9c8c3", linewidth=3)
ax.scatter(df[start], df.index, color=PALETTE[1], s=70, zorder=3, label=start[1:],
           edgecolor="#fcfcfb", linewidth=1.5)
ax.scatter(df[end], df.index, color=PALETTE[0], s=70, zorder=3, label=end[1:],
           edgecolor="#fcfcfb", linewidth=1.5)
for i, r in df.iterrows():
    ax.text(max(r[start], r[end]) + 0.7, i, f"{r['gain']:+.1f}", va="center", fontsize=8.5, color="#52514e")
ax.set_yticks(df.index, df["country"])
ax.set_xlabel("Life expectancy at birth (years)")
ax.grid(axis="y", visible=False)
ax.legend(loc="upper left", ncol=2)
ax.set_title(title)
fig.tight_layout()

# %% real-data
import plotly.express as px
countries = ["Japan", "Taiwan", "Germany", "United States", "China", "Brazil",
             "India", "Bangladesh", "South Africa", "Zimbabwe"]
gm = px.data.gapminder().query("year in [1982, 2007] and country in @countries")
df = (gm.pivot(index="country", columns="year", values="lifeExp")
        .rename(columns=lambda yr: f"y{yr}").rename_axis(columns=None).reset_index())
start, end = "y1982", "y2007"
title = "Life expectancy 1982 → 2007: most gained, southern Africa fell back"
df["gain"] = df[end] - df[start]
df = df.sort_values(end).reset_index(drop=True)
df

# %% alt:plotly
import plotly.graph_objects as go
fig = go.Figure()
for _, r in df.iterrows():
    fig.add_trace(go.Scatter(x=[r[start], r[end]], y=[r["country"]] * 2, mode="lines",
                             line=dict(color="#c9c8c3", width=3), showlegend=False, hoverinfo="skip"))
fig.add_trace(go.Scatter(x=df[start], y=df["country"], mode="markers", name=start[1:],
                         marker=dict(color=PALETTE[1], size=11, line=dict(color="#fcfcfb", width=1.5))))
fig.add_trace(go.Scatter(x=df[end], y=df["country"], mode="markers", name=end[1:],
                         marker=dict(color=PALETTE[0], size=11, line=dict(color="#fcfcfb", width=1.5))))
fig.update_layout(title=title, xaxis_title="Life expectancy at birth (years)", height=480,
                  legend=dict(orientation="h", y=1.08, x=0))
fig.show()
