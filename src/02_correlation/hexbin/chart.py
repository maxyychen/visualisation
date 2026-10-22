# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(0)
n = 50_000
distance = rng.gamma(2.0, 1.6, n)
fare = 3 + 2.4 * distance + rng.normal(0, 1.2 + 0.25 * distance, n)
df = pd.DataFrame({"distance_km": distance, "fare_usd": fare}).query("fare_usd > 2")
df.describe().round(1)

# %% plot
fig, ax = plt.subplots(figsize=(8, 5.5))
hb = ax.hexbin(df["distance_km"], df["fare_usd"], gridsize=45, cmap=SEQ_CMAP,
               bins="log", mincnt=1, linewidths=0.2, edgecolors="#fcfcfb")
ax.set_xlim(0, 16); ax.set_ylim(0, 55)
ax.grid(False)
fig.colorbar(hb, ax=ax, label="Trips (log scale)")
ax.set_xlabel("Trip distance (km)")
ax.set_ylabel("Fare (USD)")
ax.set_title("50,000 taxi trips: distance vs. fare")
fig.tight_layout()
