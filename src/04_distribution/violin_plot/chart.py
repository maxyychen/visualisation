# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(31)
groups = {"13–17": 6.5, "18–29": 5.5, "30–49": 4.2, "50–64": 3.4, "65+": 3.0}
rows = []
for g, mu in groups.items():
    rows.append(pd.DataFrame({"age": g, "day": "Weekday", "hours": rng.gamma(mu * 2, 0.5, 300)}))
    rows.append(pd.DataFrame({"age": g, "day": "Weekend", "hours": rng.gamma(mu * 2.6, 0.5, 300)}))
df = pd.concat(rows, ignore_index=True)
x, y, hue = "age", "hours", "day"
labels = dict(x="Age group", y="Screen time (hours / day)", title="Daily screen time by age group")
df.groupby(["age", "day"])["hours"].median().unstack().round(1)

# %% plot
import seaborn as sns
fig, ax = plt.subplots(figsize=(9, 5))
sns.violinplot(data=df, x=x, y=y, hue=hue, split=True, inner="quart",
               palette=PALETTE[:2], linewidth=1, cut=0, density_norm="width", ax=ax)
ax.set_xlabel(labels["x"])
ax.set_ylabel(labels["y"])
ax.set_title(labels["title"])
ax.legend(title=None, loc="upper right")
ax.grid(axis="x", visible=False)
fig.tight_layout()

# %% real-data
import plotly.express as px
df = px.data.tips()
df["day"] = pd.Categorical(df["day"], ["Thur", "Fri", "Sat", "Sun"])   # calendar order
x, y, hue = "day", "total_bill", "sex"
labels = dict(x="Day", y="Total bill ($)", title="Restaurant bills by day and sex")
df.groupby([x, hue], observed=True)[y].median().unstack().round(1)

# %% alt:plotly
import plotly.graph_objects as go
fig = go.Figure()
for color, side, (name, g) in zip(PALETTE, ["negative", "positive"], df.groupby(hue, observed=True)):
    fig.add_trace(go.Violin(x=g[x], y=g[y], name=str(name), side=side, line_color=color,
                            fillcolor=color, opacity=0.75, meanline_visible=True, points=False))
fig.update_layout(violinmode="overlay", violingap=0.1, title=labels["title"],
                  xaxis_title=labels["x"], yaxis_title=labels["y"])
fig.show()
