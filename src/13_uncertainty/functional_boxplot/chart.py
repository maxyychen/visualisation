# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from statsmodels.graphics.functional import banddepth

# %% data
rng = np.random.default_rng(2011)
n_paths, months = 300, 120
log_r = rng.normal(0.006, 0.042, (n_paths, months))
paths = 100 * np.exp(np.cumsum(log_r, axis=1))
paths = np.hstack([np.full((n_paths, 1), 100.0), paths])
t = np.arange(months + 1) / 12
depth = banddepth(paths, method="MBD")
pd.Series(depth).describe().round(3)

# %% plot
rank = np.argsort(-depth)                    # most central first
median = paths[rank[0]]
central = paths[rank[: n_paths // 2]]        # the 50% deepest curves
c_lo, c_hi = central.min(0), central.max(0)
w_lo, w_hi = c_lo - 1.5 * (c_hi - c_lo), c_hi + 1.5 * (c_hi - c_lo)
outlier = ((paths < w_lo) | (paths > w_hi)).any(1)
w_lo = np.maximum(w_lo, paths[~outlier].min(0))  # whiskers end at the most extreme non-outlier curve
w_hi = np.minimum(w_hi, paths[~outlier].max(0))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.2), sharey=True)
m, s = paths.mean(0), paths.std(0)
a1.plot(t, paths[:60].T, color="#c9c8c3", linewidth=0.5, alpha=0.6)
a1.fill_between(t, m - 2 * s, m + 2 * s, color=PALETTE[0], alpha=0.18, linewidth=0)
a1.plot(t, m, color=PALETTE[0])
a1.set_title("✗ Mean ± 2 SD: symmetric, no outlier paths", fontsize=11)
a1.set_ylabel("Portfolio value ($, start = 100)")

a2.fill_between(t, w_lo, w_hi, color=PALETTE[0], alpha=0.14, linewidth=0, label="Whisker envelope")
a2.fill_between(t, c_lo, c_hi, color=PALETTE[0], alpha=0.38, linewidth=0, label="50% central region")
for k, i in enumerate(np.where(outlier)[0]):
    a2.plot(t, paths[i], color=PALETTE[1], linewidth=1, alpha=0.85, label="Outlier curve" if k == 0 else None)
a2.plot(t, median, color="#0b0b0b", linewidth=2, label="Median curve (deepest)")
a2.set_title(f"✓ Functional boxplot: {outlier.sum()} outlier paths flagged", fontsize=11)
a2.legend(loc="upper left", fontsize=8.5)
for ax in (a1, a2):
    ax.set_xlabel("Years")
    ax.axhline(100, color="#52514e", linewidth=0.8)

fig.suptitle(f"{n_paths} simulated 10-year portfolio paths: two ways to summarise them", x=0.01,
             ha="left", fontweight="bold", fontsize=13)
fig.tight_layout()
