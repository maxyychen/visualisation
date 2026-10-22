# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(21)
means = {"setosa": [5.0, 3.4, 1.5, 0.25], "versicolor": [5.9, 2.8, 4.3, 1.3],
         "virginica": [6.6, 3.0, 5.6, 2.0]}
sds = [0.35, 0.33, 0.3, 0.15]
rows = []
for sp, mu in means.items():
    x = rng.normal(mu, sds, (50, 4))
    rows.append(pd.DataFrame(x, columns=["sepal_length", "sepal_width",
                                         "petal_length", "petal_width"]).assign(species=sp))
df = pd.concat(rows, ignore_index=True)
df.head()

# %% plot
import seaborn as sns
g = sns.pairplot(df, hue="species", palette=PALETTE[:3], height=2, corner=True,
                 plot_kws=dict(s=18, alpha=0.7, edgecolor="#fcfcfb", linewidth=0.4),
                 diag_kws=dict(fill=True, alpha=0.35, linewidth=1.2))
g.figure.suptitle("Flower measurements by species", x=0.02, ha="left", weight="bold")
fig = g.figure

# %% real-data
import plotly.express as px
df = px.data.iris()[["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]]
df.head()

# %% alt:plotly
import plotly.express as px
fig = px.scatter_matrix(df, dimensions=["sepal_length", "sepal_width", "petal_length", "petal_width"],
                        color="species", color_discrete_sequence=PALETTE, opacity=0.7,
                        title="Flower measurements by species")
fig.update_traces(diagonal_visible=False, showupperhalf=False, marker=dict(size=5))
fig.update_layout(height=650)
fig.show()
