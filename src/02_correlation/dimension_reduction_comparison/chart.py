# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
import os
os.environ["NUMBA_NUM_THREADS"] = "1"  # PaCMAP/UMAP use numba; single-threaded avoids a macOS crash
os.environ["OMP_NUM_THREADS"] = "1"
from scipy.spatial.distance import pdist
from scipy.stats import spearmanr
from sklearn.datasets import load_digits
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors
import umap
import pacmap

# %% data
digits = load_digits()
X = (digits.data / 16).astype("float32")
labels = digits.target
embeddings = {
    "t-SNE": TSNE(n_components=2, perplexity=30, init="pca", random_state=0).fit_transform(X),
    "UMAP": umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=0).fit_transform(X),
    "PaCMAP": pacmap.PaCMAP(n_components=2, random_state=0, apply_pca=False).fit_transform(X),
}
{name: e.shape for name, e in embeddings.items()}

# %% plot
def local_score(high, low, k=10):
    nn_h = NearestNeighbors(n_neighbors=k + 1).fit(high).kneighbors(high, return_distance=False)[:, 1:]
    nn_l = NearestNeighbors(n_neighbors=k + 1).fit(low).kneighbors(low, return_distance=False)[:, 1:]
    return np.mean([len(set(a) & set(b)) / k for a, b in zip(nn_h, nn_l)])

def global_score(high, low, y):
    ch = np.array([high[y == c].mean(0) for c in range(10)])
    cl = np.array([low[y == c].mean(0) for c in range(10)])
    return spearmanr(pdist(ch), pdist(cl)).statistic

colors = PALETTE + ["#8f8e88", "#3f3e3b"]
fig, axes = plt.subplots(1, 3, figsize=(15, 5.4))
for ax, (name, emb) in zip(axes, embeddings.items()):
    for c in range(10):
        pts = emb[labels == c]
        ax.scatter(pts[:, 0], pts[:, 1], s=5, color=colors[c], alpha=0.7, linewidth=0)
        cx, cy = np.median(pts, axis=0)
        ax.text(cx, cy, str(c), ha="center", va="center", fontsize=13, fontweight="bold", color="#0b0b0b",
                bbox=dict(boxstyle="circle,pad=0.2", facecolor="#fcfcfb", edgecolor=colors[c], linewidth=1.5))
    ax.set_title(f"{name}\nlocal {local_score(X, emb):.2f} · global {global_score(X, emb, labels):.2f}",
                 loc="center", fontsize=12)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
fig.suptitle("Same digits, three embeddings: local = neighbours kept, global = cluster arrangement kept (1 = best)",
             x=0.01, ha="left", fontsize=12, fontweight="bold")
fig.tight_layout()
