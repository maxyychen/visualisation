# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.colors import to_rgb
from scipy import stats

# %% data
df = pd.DataFrame({
    "region": ["North", "South", "East", "West", "Coast", "Mountain"],
    "mean_growth": [4.2, 7.5, 3.1, 5.0, 6.4, 2.0],
    "sd": [0.8, 2.2, 1.5, 1.8, 1.0, 2.8],
}).sort_values("mean_growth")
df

# %% plot
fig, ax = plt.subplots(figsize=(8.5, 4.8))
xs = np.linspace(-6, 15, 600)
rgb = np.array(to_rgb(PALETTE[0]))
for i, r in enumerate(df.itertuples()):
    dens = stats.norm.pdf(xs, r.mean_growth, r.sd)
    alpha = dens / dens.max()
    img = np.zeros((1, len(xs), 4))
    img[0, :, :3] = rgb
    img[0, :, 3] = alpha * 0.95
    ax.imshow(img, extent=(xs[0], xs[-1], i - 0.32, i + 0.32), aspect="auto", interpolation="bilinear")
    ax.plot([r.mean_growth] * 2, [i - 0.36, i + 0.36], color="#0d366b", lw=2)
    ax.text(r.mean_growth, i + 0.42, f"{r.mean_growth:.1f}%", ha="center", va="bottom",
            fontsize=8.5, color="#52514e")
ax.axvline(0, color="#52514e", lw=1)
ax.set_yticks(range(len(df)), df["region"])
ax.set_ylim(-0.6, len(df) - 0.2)
ax.set_xlim(-6, 15)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Projected sales growth to 2030 (%)  (darker = more likely)")
ax.set_title("Mountain region could still shrink; others very likely grow")
fig.tight_layout()
