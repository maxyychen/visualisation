# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(17)
size = rng.gamma(9, 18, 400)                                 # m²
price = np.exp(10.8 + 0.0062 * size + rng.normal(0, 0.22, 400)) / 1000   # $k
df = pd.DataFrame({"size_m2": size, "price_k": price})
x, y = "size_m2", "price_k"
labels = dict(x="Living area (m²)", y="Sale price ($k)", title="House size vs. price")
df.describe().round(0)

# %% plot
import seaborn as sns
g = sns.jointplot(data=df, x=x, y=y, height=6, color=PALETTE[0],
                  joint_kws=dict(s=22, alpha=0.6, edgecolor="#fcfcfb", linewidth=0.5),
                  marginal_kws=dict(bins=30, edgecolor="#fcfcfb", linewidth=0.5))
g.set_axis_labels(labels["x"], labels["y"])
g.figure.suptitle(labels["title"], x=0.02, ha="left", weight="bold")
g.figure.tight_layout()
fig = g.figure

# %% real-data
import plotly.express as px
df = px.data.gapminder().query("year == 2007")
x, y = "gdpPercap", "lifeExp"
labels = dict(x="GDP per capita (USD)", y="Life expectancy (years)",
              title="Income vs. life expectancy, 142 countries (2007)")
df[[x, y]].describe().round(0)

# %% alt:plotly
import plotly.express as px
fig = px.scatter(df, x=x, y=y, marginal_x="histogram", marginal_y="histogram", opacity=0.6,
                 color_discrete_sequence=PALETTE, labels={x: labels["x"], y: labels["y"]},
                 title=labels["title"])
fig.update_layout(height=560)
fig.show()
