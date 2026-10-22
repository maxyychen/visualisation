# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from scipy import stats

# %% data
rng = np.random.default_rng(6)
groups = ["Placebo", "10 mg", "20 mg", "40 mg"]
true_mean = [3, 18, 27, 33]
df = pd.concat([pd.DataFrame({"group": g, "ldl_reduction_pct": rng.normal(m, 11, rng.integers(22, 30))})
                for g, m in zip(groups, true_mean)], ignore_index=True)
summary = df.groupby("group", sort=False)["ldl_reduction_pct"].agg(["mean", "std", "count"])
summary["ci95"] = stats.t.ppf(0.975, summary["count"] - 1) * summary["std"] / np.sqrt(summary["count"])
summary.round(2)

# %% plot
fig, ax = plt.subplots(figsize=(7.5, 5))
for i, g in enumerate(groups):
    vals = df.loc[df.group == g, "ldl_reduction_pct"]
    ax.scatter(i + rng.uniform(-0.18, 0.18, len(vals)), vals, s=14, color=GRAY, alpha=0.6, linewidth=0)
ax.errorbar(range(len(groups)), summary["mean"], yerr=summary["ci95"], fmt="o", color=PALETTE[0],
            markersize=9, capsize=6, elinewidth=2, capthick=2, markeredgecolor="#fcfcfb", zorder=3)
for i, (m, n) in enumerate(zip(summary["mean"], summary["count"])):
    ax.text(i + 0.25, m, f"{m:.1f}%", va="center", fontsize=9, color="#0b0b0b")
ax.set_xticks(range(len(groups)), [f"{g}\n(n={n})" for g, n in zip(groups, summary["count"])])
ax.axhline(0, color="#52514e", linewidth=0.8)
ax.grid(axis="x", visible=False)
ax.set_ylabel("LDL reduction at week 12 (%)")
ax.set_title("Mean LDL reduction by dose (dot = mean, bar = 95% CI)")
fig.tight_layout()
