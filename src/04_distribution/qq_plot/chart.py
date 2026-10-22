# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
from scipy import stats
rng = np.random.default_rng(43)
samples = {
    "Normal": rng.normal(0, 1, 200),
    "Right-skewed (lognormal)": rng.lognormal(0, 0.6, 200),
    "Heavy-tailed (t, df=3)": rng.standard_t(3, 200),
}
{k: round(stats.skew(v), 2) for k, v in samples.items()}

# %% plot
fig, axes = plt.subplots(1, 3, figsize=(11, 4))
for ax, (name, x) in zip(axes, samples.items()):
    (osm, osr), (slope, intercept, r) = stats.probplot(x, dist="norm")
    ax.scatter(osm, osr, s=14, color=PALETTE[0], alpha=0.7, edgecolor="none")
    ax.plot(osm, slope * osm + intercept, color=PALETTE[1], linewidth=1.5)
    ax.set_title(name, fontsize=11)
    ax.set_xlabel("Theoretical quantiles")
axes[0].set_ylabel("Sample quantiles")
fig.suptitle("Q-Q plots against the normal distribution", x=0.01, ha="left", weight="bold")
fig.tight_layout()
