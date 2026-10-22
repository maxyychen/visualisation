# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(12)
weeks = np.arange(52)
genres = ["Pop", "Rock", "Hip-hop", "Electronic", "Jazz", "Classical"]
def bump(center, width, height):
    return height * np.exp(-((weeks - center) / width) ** 2)
df = pd.DataFrame({g: bump(rng.uniform(5, 47), rng.uniform(6, 14), rng.uniform(20, 60))
                   + rng.uniform(5, 15) for g in genres}, index=weeks)
df.head()

# %% plot
from scipy.ndimage import gaussian_filter1d
smooth = df.apply(lambda s: gaussian_filter1d(s, 1.5))
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.stackplot(smooth.index, smooth.T.values, baseline="wiggle", labels=smooth.columns,
             colors=PALETTE[:6], edgecolor="#fcfcfb", linewidth=0.8)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Week of year")
ax.set_xlim(0, 51)
ax.set_title("Listening by genre over the year")
ax.legend(loc="upper left", ncol=6, bbox_to_anchor=(0, -0.15))
fig.tight_layout()
