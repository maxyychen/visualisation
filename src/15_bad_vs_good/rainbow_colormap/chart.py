# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
x, y = np.meshgrid(np.linspace(-3, 3, 300), np.linspace(-2, 2, 200))
z = np.exp(-((x + 0.8) ** 2 + y ** 2)) + 0.7 * np.exp(-((x - 1.3) ** 2 + (y - 0.4) ** 2) / 0.6)


def lightness(cmap, n=256):
    """CIE L* (0 = black, 100 = white) of each color in a colormap."""
    rgb = plt.get_cmap(cmap)(np.linspace(0, 1, n))[:, :3]
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    Y = lin @ np.array([0.2126, 0.7152, 0.0722])
    f = np.where(Y > (6 / 29) ** 3, np.cbrt(Y), Y / (3 * (6 / 29) ** 2) + 4 / 29)
    return 116 * f - 16


pd.Series({"field min": z.min(), "field max": z.max()}).round(3)

# %% plot
fig = plt.figure(figsize=(12, 5.6))
gs = fig.add_gridspec(2, 2, height_ratios=[4, 1.1], hspace=0.45)
for col, (cmap, title) in enumerate([("jet", "✗ Misleading: rainbow (jet) invents bands"),
                                     (SEQ_CMAP, "✓ Better: one-hue sequential")]):
    ax = fig.add_subplot(gs[0, col])
    im = ax.imshow(z, cmap=cmap, origin="lower", extent=(-3, 3, -2, 2), aspect="auto")
    ax.set_title(title, fontsize=11.5)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02, label="Concentration")
    lax = fig.add_subplot(gs[1, col])
    L = lightness(cmap)
    lax.scatter(np.linspace(0, 1, 256), L, c=np.linspace(0, 1, 256), cmap=cmap, s=8)
    lax.set_ylim(0, 100); lax.set_xlim(0, 1)
    lax.set_ylabel("Lightness L*", fontsize=9)
    lax.set_xlabel("colormap position (low → high value)", fontsize=9)
    lax.tick_params(labelsize=8)
