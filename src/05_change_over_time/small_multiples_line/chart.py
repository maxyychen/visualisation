# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(8)
weeks = np.arange(1, 53)
stores = [f"Store {c}" for c in "ABCDEFGHI"]
df = pd.DataFrame({s: 100 + rng.normal(0, 0.8) * weeks + 10 * np.sin(weeks / 8 + rng.uniform(0, 6))
                   + rng.normal(0, 3, 52).cumsum() / 2 for s in stores}, index=weeks)
df = df[df.iloc[-1].sort_values(ascending=False).index]
labels = dict(x="Week", y="Sales index", title="Weekly sales index by store (sorted by final value)")
df.iloc[:5, :5]

# %% plot
fig, axes = plt.subplots(3, 3, figsize=(10, 7), sharex=True, sharey=True)
for ax, col in zip(axes.flat, df.columns):
    for other in df.columns:
        ax.plot(df.index, df[other], color="#e3e2de", linewidth=0.8)
    ax.plot(df.index, df[col], color=PALETTE[0], linewidth=2)
    ax.set_title(f"{col}  ({df[col].iloc[-1]:.0f})", fontsize=10)
for ax in axes[-1]:
    ax.set_xlabel(labels["x"])
for ax in axes[:, 0]:
    ax.set_ylabel(labels["y"])
fig.suptitle(labels["title"], x=0.02, ha="left",
             fontweight="bold", fontsize=13)
fig.tight_layout()

# %% real-data
import plotly.express as px
countries = ["Japan", "Chile", "China", "Brazil", "India", "Iraq", "Rwanda", "South Africa", "Zimbabwe"]
gm = px.data.gapminder().query("country in @countries")
df = gm.pivot(index="year", columns="country", values="lifeExp").rename_axis(columns=None)
df = df[df.iloc[-1].sort_values(ascending=False).index]
labels = dict(x="Year", y="Life exp. (yrs)", title="Life expectancy 1952–2007 (sorted by 2007 value)")
df.iloc[:5, :5]
