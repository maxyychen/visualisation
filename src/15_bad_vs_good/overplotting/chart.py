# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.colors import LogNorm

# %% data
rng = np.random.default_rng(12)
n_main, n_sub = 57_000, 3_000
main = rng.multivariate_normal([5, 5], [[1.6, 1.1], [1.1, 1.6]], n_main)
sub = rng.multivariate_normal([7.6, 7.0], [[0.08, 0.0], [0.0, 0.08]], n_sub)
df = pd.DataFrame(np.vstack([main, sub]), columns=["marker_a", "marker_b"])
df.describe().round(2)

# %% plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)

# Misleading: 60k opaque markers.
ax1.scatter(df["marker_a"], df["marker_b"], s=14, color=PALETTE[0])
ax1.set_title("✗ Misleading: 60,000 opaque dots = one blob", fontsize=11.5)
ax1.set_xlabel("Marker A"); ax1.set_ylabel("Marker B")

# Better: hexbin with a log color scale.
hb = ax2.hexbin(df["marker_a"], df["marker_b"], gridsize=60, cmap=SEQ_CMAP, norm=LogNorm(), mincnt=1)
fig.colorbar(hb, ax=ax2, label="Patients per bin (log scale)")
ax2.annotate("Hidden subgroup\n(n = 3,000)", xy=(7.6, 7.0), xytext=(8.6, 3.2), fontsize=9.5,
             arrowprops=dict(arrowstyle="-", color="#52514e", lw=1), color="#0b0b0b")
ax2.set_title("✓ Better: hexbin + log color reveals structure", fontsize=11.5)
ax2.set_xlabel("Marker A")
ax2.grid(False)
fig.tight_layout()
