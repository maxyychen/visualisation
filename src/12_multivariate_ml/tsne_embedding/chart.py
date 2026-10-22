# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from sklearn.datasets import load_breast_cancer
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

# %% data
bc = load_breast_cancer(as_frame=True)
Z = StandardScaler().fit_transform(bc.data)
emb = TSNE(n_components=2, perplexity=30, init="pca", random_state=0).fit_transform(Z)
df = pd.DataFrame(emb, columns=["dim1", "dim2"])
df["diagnosis"] = bc.target.map({0: "Malignant", 1: "Benign"})
df["diagnosis"].value_counts()

# %% plot
fig, ax = plt.subplots(figsize=(7, 6))
for color, label in zip(PALETTE, ["Benign", "Malignant"]):
    g = df[df["diagnosis"] == label]
    ax.scatter(g["dim1"], g["dim2"], s=22, alpha=0.75, color=color,
               edgecolor="#fcfcfb", linewidth=0.5, label=f"{label} (n={len(g)})")
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
ax.set_xlabel("t-SNE 1 (no units)")
ax.set_ylabel("t-SNE 2 (no units)")
ax.set_title("Tumours cluster by diagnosis (t-SNE of 30 features)")
ax.legend(loc="best")
fig.tight_layout()
