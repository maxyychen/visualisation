# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# %% data
wine = load_wine(as_frame=True)
X = wine.data
y = wine.target.map(lambda k: f"Cultivar {k}")
Z = StandardScaler().fit_transform(X)
pca = PCA(n_components=2).fit(Z)
scores = pca.transform(Z)
loadings = pd.DataFrame(pca.components_.T, index=X.columns, columns=["PC1", "PC2"])
loadings.round(2).sort_values("PC1")

# %% plot
fig, ax = plt.subplots(figsize=(8, 6.5))
for color, cls in zip(PALETTE, sorted(y.unique())):
    m = (y == cls).values
    ax.scatter(scores[m, 0], scores[m, 1], s=30, alpha=0.7, color=color,
               edgecolor="#fcfcfb", linewidth=0.6, label=cls)
scale = np.abs(scores).max() * 0.9
top = loadings.pow(2).sum(axis=1).nlargest(7).index
for name, (lx, ly) in loadings.iterrows():
    strong = name in top
    ax.annotate("", xy=(lx * scale, ly * scale), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#52514e" if strong else "#b8b7b1",
                                lw=1.2 if strong else 0.8))
    if strong:
        ax.text(lx * scale * 1.12, ly * scale * 1.12, name.replace("_", " "), fontsize=8.5,
                color="#0b0b0b", ha="center", va="center")
ev = pca.explained_variance_ratio_ * 100
ax.set_xlabel(f"PC1 ({ev[0]:.0f}% of variance)")
ax.set_ylabel(f"PC2 ({ev[1]:.0f}% of variance)")
ax.axhline(0, color="#c9c8c3", lw=0.8)
ax.axvline(0, color="#c9c8c3", lw=0.8)
ax.set_title("Wine cultivars separate along PC1, driven by phenolic compounds")
ax.legend(loc="upper right")
fig.tight_layout()
