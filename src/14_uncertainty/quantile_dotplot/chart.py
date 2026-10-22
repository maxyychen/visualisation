# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.patches import Circle
from scipy import stats

# %% data
n_dots = 20
dist = stats.lognorm(s=0.35, scale=11)          # median ~11 minutes
q = dist.ppf((np.arange(n_dots) + 0.5) / n_dots)  # one dot per 5% of probability
threshold = 9
df = pd.DataFrame({"minutes": q.round(1), "bin": np.floor(q).astype(int)})  # bin b = [b, b+1) minutes
print(f"P(arrival ≤ {threshold} min) ≈ {dist.cdf(threshold):.0%}")
df.T

# %% plot
fig, ax = plt.subplots(figsize=(9, 3.8))
r = 0.45
counts = {}
for b in df["bin"]:
    k = counts.get(b, 0)
    counts[b] = k + 1
    color = PALETTE[0] if b < threshold else "#b8b7b1"
    ax.add_patch(Circle((b + 0.5, r + 2 * r * k + 0.02), r, color=color, linewidth=0))
n_before = int((df["bin"] < threshold).sum())
ax.axvline(threshold, color="#52514e", lw=1)
ax.text(threshold + 0.1, 4.6, f"{n_before} of {n_dots} dots\n≈ {n_before / n_dots:.0%} chance\nby {threshold} min",
        fontsize=9.5, color="#0b0b0b", va="top")
ax.set_xlim(df["bin"].min() - 1.5, df["bin"].max() + 2.5)
ax.set_ylim(0, 5)
ax.set_aspect("equal")
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.grid(False)
ax.set_xticks(range(df["bin"].min() - 1, df["bin"].max() + 3, 2))
ax.set_xlabel("Minutes until the bus arrives (each dot = 5% chance)")
ax.set_title("When will my bus arrive?")
fig.tight_layout()
