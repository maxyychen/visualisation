# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(14)
dates = pd.date_range("2023-01", periods=30, freq="MS")
t = np.arange(30)
df = pd.DataFrame({
    "Users (k)": 12 + 0.9 * t + rng.normal(0, 0.5, 30),
    "Sessions (M)": 0.35 + 0.004 * t ** 1.6 + rng.normal(0, 0.01, 30),
    "Revenue ($M)": 2.1 + 0.03 * t + rng.normal(0, 0.05, 30),
}, index=dates)
indexed = df / df.iloc[0] * 100
labels = dict(y="Index (Jan 2023 = 100)",
              title="Growth since Jan 2023: one honest axis instead of three")
indexed.head()

# %% plot
fig, ax = plt.subplots(figsize=(9, 4.8))
span = indexed.index[-1] - indexed.index[0]
for i, col in enumerate(indexed.columns):
    ax.plot(indexed.index, indexed[col], color=PALETTE[i], label=col)
    ax.text(indexed.index[-1] + span * 0.012, indexed[col].iloc[-1],
            f"{col.split(' (')[0]} {indexed[col].iloc[-1]:.0f}", va="center", fontsize=9.5)
ax.axhline(100, color="#52514e", linewidth=1)
ax.set_xlim(indexed.index[0], indexed.index[-1] + span * 0.17)
ax.set_ylabel(labels["y"])
ax.set_title(labels["title"])
ax.legend(loc="upper left")
fig.tight_layout()

# %% real-data
import plotly.express as px
gm = px.data.gapminder().query("country == 'India'")
df = pd.DataFrame({"Population (M)": gm["pop"].values / 1e6,
                   "GDP per capita ($)": gm["gdpPercap"].values,
                   "Life expectancy (yrs)": gm["lifeExp"].values},
                  index=pd.to_datetime(gm["year"].astype(str)))
indexed = df / df.iloc[0] * 100
labels = dict(y="Index (1952 = 100)", title="India since 1952: three measures on one honest axis")
indexed.head()
