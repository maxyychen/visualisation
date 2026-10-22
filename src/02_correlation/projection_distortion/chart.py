# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import Ellipse
from scipy.spatial.distance import pdist
from sklearn.datasets import load_digits
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors

# %% data
digits = load_digits()
X = digits.data / 16
labels = digits.target
emb = TSNE(n_components=2, perplexity=30, init="pca", random_state=0).fit_transform(X)
pd.DataFrame(emb, columns=["tsne1", "tsne2"]).describe().round(1)

# %% plot
G, k = 12, 25                                  # grid resolution, neighbours per local fit
lo, hi = emb.min(0), emb.max(0)
cell = (hi - lo).max() / (G - 1)
gx, gy = np.meshgrid(np.linspace(lo[0], hi[0], G), np.linspace(lo[1], hi[1], G))
centers = np.c_[gx.ravel(), gy.ravel()]
dist, idx = NearestNeighbors(n_neighbors=k).fit(emb).kneighbors(centers)

glyphs = []
for c, d, nb in zip(centers, dist, idx):
    if d.max() > 0.9 * cell:                   # too few points nearby: skip empty regions
        continue
    U = emb[nb] - emb[nb].mean(0)              # 2-D offsets
    V = X[nb] - X[nb].mean(0)                  # high-D offsets
    M, *_ = np.linalg.lstsq(U, V, rcond=None)  # local linear map 2-D -> high-D (2 x 64)
    evals, evecs = np.linalg.eigh(M @ M.T)     # metric tensor: high-D length per unit 2-D length
    ratio = pdist(X[nb]).mean() / pdist(emb[nb]).mean()
    glyphs.append((c, np.sqrt(np.maximum(evals, 1e-12)), evecs, ratio))

ratios = np.array([g[3] for g in glyphs])
scales = np.array([g[1].mean() for g in glyphs])
log_ratio = np.log2(ratios / np.median(ratios))
cmap = LinearSegmentedColormap.from_list("stretch", [PALETTE[0], "#d9d8d3", PALETTE[1]])
lim = np.abs(log_ratio).max()
norm = TwoSlopeNorm(0, -lim, lim)

fig, ax = plt.subplots(figsize=(9, 8))
ax.scatter(emb[:, 0], emb[:, 1], s=4, color="#b8b7b1", alpha=0.6, linewidth=0)
base = 0.36 * cell
for (c, s, vecs, _), lr in zip(glyphs, log_ratio):
    semi = np.clip(base * np.median(scales) / s, 0.25 * base, 1.6 * base)  # image of a fixed high-D ball
    angle = np.degrees(np.arctan2(vecs[1, 0], vecs[0, 0]))
    ax.add_patch(Ellipse(c, 2 * semi[0], 2 * semi[1], angle=angle, facecolor=cmap(norm(lr)),
                         edgecolor="#fcfcfb", linewidth=1, alpha=0.9))
for d in range(10):
    cx, cy = np.median(emb[labels == d], axis=0)
    ax.text(cx, cy, str(d), ha="center", va="center", fontsize=15, fontweight="bold", color="#0b0b0b")
sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
cb = fig.colorbar(sm, ax=ax, shrink=0.7, pad=0.02)
cb.set_label("log2 high-D / 2-D neighbour distance (vs. map median)\n← stretched in the map · compressed in the map →")
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
ax.set_aspect("equal")
ax.set_title("Where t-SNE distorts the digits: ellipse = image of a small high-D ball")
fig.tight_layout()
