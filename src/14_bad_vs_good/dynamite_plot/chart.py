# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from scipy import stats

# %% data
rng = np.random.default_rng(30)
a = rng.normal(50, 8, 30)
b = np.concatenate([rng.normal(30, 5, 15), rng.normal(70, 5, 15)])
b = b - b.mean() + a.mean()   # force identical means
df = pd.DataFrame({"group": ["Treatment A"] * 30 + ["Treatment B"] * 30,
                   "value": np.concatenate([a, b])})
df.groupby("group")["value"].agg(["count", "mean", "std", "sem"]).round(1)

# %% plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
groups = ["Treatment A", "Treatment B"]
summary = df.groupby("group")["value"].agg(["mean", "sem", "count"]).loc[groups]

# Misleading: bar of means + SE whisker.
ax1.bar(groups, summary["mean"], yerr=summary["sem"], color=[PALETTE[0], PALETTE[1]],
        width=0.55, capsize=10, error_kw=dict(elinewidth=1.5, ecolor="#0b0b0b"))
ax1.set_ylabel("Biomarker level")
ax1.set_title("✗ Misleading: dynamite plot (mean ± SE)", fontsize=11.5)
ax1.grid(axis="x", visible=False)

# Better: every point + mean and 95% CI, n labeled.
for i, g in enumerate(groups):
    vals = df.loc[df["group"] == g, "value"].to_numpy()
    jitter = rng.uniform(-0.12, 0.12, len(vals))
    ax2.scatter(i + jitter, vals, s=28, color=PALETTE[i], alpha=0.75,
                edgecolor="#fcfcfb", linewidth=0.8, zorder=2)
    m = vals.mean()
    lo, hi = stats.t.interval(0.95, len(vals) - 1, loc=m, scale=stats.sem(vals))
    ax2.errorbar(i + 0.28, m, yerr=[[m - lo], [hi - m]], fmt="o", color="#0b0b0b",
                 capsize=5, markersize=6, linewidth=1.5, zorder=3)
    ax2.text(i + 0.36, m, f"mean {m:.0f}\n95% CI {lo:.0f}–{hi:.0f}", va="center", fontsize=8.5,
             color="#52514e")
ax2.set_xticks([0, 1], [f"{g}\n(n = {int(summary.loc[g, 'count'])})" for g in groups])
ax2.set_xlim(-0.5, 1.9)
ax2.set_title("✓ Better: all points + mean and 95% CI", fontsize=11.5)
ax2.grid(axis="x", visible=False)
fig.tight_layout()
