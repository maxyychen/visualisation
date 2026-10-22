# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import squareform

# %% data
rng = np.random.default_rng(8)
groups = ["Growth", "Value", "Dividend", "Small cap"]
n = 40
group = rng.permutation(np.repeat(np.arange(4), n // 4))       # strategy of each fund (hidden in ID order)
base = np.where(group[:, None] == group[None, :], 0.45, 0.06)  # same strategy -> large overlap
overlap = np.clip(base + rng.normal(0, 0.07, (n, n)), 0, 1)
overlap = np.triu(overlap, 1)
overlap = overlap + overlap.T                                  # symmetric, zero diagonal
overlap[overlap < 0.08] = 0                                    # tiny overlaps -> no link
funds = [f"F{i:02d}" for i in range(n)]
A = pd.DataFrame(overlap, index=funds, columns=funds)
A.iloc[:6, :6].round(2)

# %% plot
# Reorder by average-linkage clustering on distance = 1 - overlap
D = 1 - A.values
np.fill_diagonal(D, 0)
order = leaves_list(linkage(squareform(D), method="average"))
B = A.iloc[order, order]

fig, axes = plt.subplots(1, 2, figsize=(12, 6.2))
for ax, M, title in [(axes[0], A, "Fund ID order: structure is hidden"),
                     (axes[1], B, "Clustered order: four strategy blocks appear")]:
    im = ax.imshow(M.values, cmap=SEQ_CMAP, vmin=0, vmax=0.7, interpolation="nearest")
    ax.set_xticks(range(n), M.columns, rotation=90, fontsize=5.5)
    ax.set_yticks(range(n), M.index, fontsize=5.5)
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, fontsize=11)
# Outline the clusters on the reordered matrix and name them on the margin
g_sorted = group[order]
start = 0
for i in range(1, n + 1):
    if i == n or g_sorted[i] != g_sorted[start]:
        axes[1].add_patch(plt.Rectangle((start - 0.5, start - 0.5), i - start, i - start,
                                        fill=False, edgecolor="#0b0b0b", linewidth=1.2))
        axes[1].text(n + 0.5, (start + i - 1) / 2, groups[g_sorted[start]], va="center",
                     fontsize=9, color="#52514e")
        start = i
cb = fig.colorbar(im, ax=axes, shrink=0.75, pad=0.09)
cb.set_label("Portfolio overlap (share of holdings in common)")
cb.outline.set_visible(False)
fig.suptitle("Portfolio overlap between 40 funds (simulated)", x=0.02, ha="left",
             fontsize=13, fontweight="bold")
