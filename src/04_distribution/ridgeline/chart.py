# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(13)
groups = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
means = 15 + 11 * np.sin((np.arange(12) - 3.5) / 12 * 2 * np.pi)
df = pd.concat([pd.DataFrame({"group": m, "value": rng.normal(mu, 3 + abs(mu - 15) * 0.1, 31)})
                for m, mu in zip(groups, means)], ignore_index=True)
labels = dict(x="Daily maximum temperature (°C)", title="Daily highs by month")
df.groupby("group", sort=False)["value"].mean().round(1)

# %% plot
from scipy.stats import gaussian_kde
fig, ax = plt.subplots(figsize=(8, 7))
pad = np.ptp(df["value"]) * 0.2
xs = np.linspace(df["value"].min() - pad, df["value"].max() + pad, 300)
cmap = plt.get_cmap(SEQ_CMAP)
spacing = 1.0
for i, m in enumerate(groups):
    vals = df.loc[df["group"] == m, "value"]
    dens = gaussian_kde(vals, bw_method=0.6)(xs)
    dens = dens / dens.max() * 1.35
    base = (len(groups) - 1 - i) * spacing
    color = cmap(0.3 + 0.6 * (vals.mean() - df["value"].min()) / np.ptp(df["value"]))
    ax.fill_between(xs, base, base + dens, color=color, alpha=0.9, zorder=i, linewidth=0)
    ax.plot(xs, base + dens, color="#fcfcfb", linewidth=1.5, zorder=i)
    ax.text(xs[0] - pad * 0.06, base + 0.1, m, fontsize=9.5, color="#52514e", ha="right")
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.grid(False)
ax.set_xlabel(labels["x"])
ax.set_title(labels["title"])
fig.tight_layout()

# %% real-data
import plotly.express as px
gm = px.data.gapminder()
groups = [str(y) for y in sorted(gm["year"].unique())]
df = pd.DataFrame({"group": gm["year"].astype(str), "value": gm["lifeExp"]})
labels = dict(x="Life expectancy at birth (years), 142 countries",
              title="The world's life-expectancy distribution, 1952–2007")
df.groupby("group", sort=False)["value"].mean().round(1)
