# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(14)
df = pd.concat([
    pd.DataFrame({"score": rng.normal(68, 9, 300), "method": "Lecture"}),
    pd.DataFrame({"score": rng.normal(74, 7, 300), "method": "Flipped"}),
    pd.DataFrame({"score": np.r_[rng.normal(60, 6, 150), rng.normal(82, 6, 150)],
                  "method": "Self-paced"}),
], ignore_index=True)
x, hue, order = "score", "method", ["Lecture", "Flipped", "Self-paced"]
labels = dict(x="Exam score", title="Exam score distribution by teaching method")
df.groupby(hue)[x].describe().round(1)

# %% plot
import seaborn as sns
fig, ax = plt.subplots(figsize=(8, 4.8))
sns.kdeplot(data=df, x=x, hue=hue, hue_order=order,
            palette=PALETTE[:len(order)], fill=True, alpha=0.2, linewidth=2, common_norm=False, ax=ax)
ax.set_xlabel(labels["x"])
ax.set_ylabel("Density")
ax.set_title(labels["title"])
ax.get_legend().set_title(None)
fig.tight_layout()

# %% real-data
import plotly.express as px
df = px.data.iris()
x, hue, order = "sepal_length", "species", ["setosa", "versicolor", "virginica"]
labels = dict(x="Sepal length (cm)", title="Sepal length by iris species (Fisher, 1936)")
df.groupby(hue)[x].describe().round(1)

# %% alt:altair
import altair as alt
chart = alt.Chart(df).transform_density(
    x, groupby=[hue], as_=[x, "density"], steps=200,
).mark_area(opacity=0.25, line=dict(strokeWidth=2)).encode(
    x=alt.X(f"{x}:Q", title=labels["x"]),
    y=alt.Y("density:Q", title="Density", stack=None),
    color=alt.Color(f"{hue}:N", sort=order, title=None),
).properties(title=labels["title"], width=520, height=300)
chart
