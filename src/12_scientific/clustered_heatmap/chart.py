# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
import seaborn as sns
from matplotlib.patches import Patch

# %% data
rng = np.random.default_rng(3)
group = np.array(["Tumour"] * 8 + ["Normal"] * 8)
rng.shuffle(group)
expr = rng.normal(0, 1, (40, 16))
is_t = group == "Tumour"
expr[:12, is_t] += 2.2      # module up in tumour
expr[12:22, is_t] -= 1.8    # module down in tumour
expr[22:30] += np.linspace(-1, 1, 16)  # gradient module
genes = [f"G{i:02d}" for i in range(40)]
df = pd.DataFrame(expr + 8, index=genes, columns=[f"S{i:02d}" for i in range(16)])
group_palette = {"Tumour": PALETTE[1], "Normal": PALETTE[0]}
title = "Clustered expression heatmap"
df.iloc[:5, :6]

# %% plot
group_colors = pd.Series(group, index=df.columns).map(group_palette)
g = sns.clustermap(df, z_score=0, cmap=DIV_CMAP, center=0, vmin=-2.5, vmax=2.5, method="average",
                   metric="correlation", col_colors=group_colors, figsize=(8, 9),
                   dendrogram_ratio=(0.15, 0.12), cbar_pos=(0.02, 0.84, 0.03, 0.12),
                   yticklabels=True, tree_kws=dict(linewidths=0.8, colors="#52514e"))
g.ax_heatmap.tick_params(axis="y", labelsize=7)
g.ax_cbar.set_title("z-score", fontsize=9)
g.ax_heatmap.legend(handles=[Patch(color=c, label=k) for k, c in group_palette.items()],
                    loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=2)
g.figure.suptitle(title, x=0.55, y=1.01, fontweight="bold")
fig = g.figure

# %% real-data
from sklearn.datasets import load_breast_cancer
bc = load_breast_cancer(as_frame=True)
rng = np.random.default_rng(3)
target = bc.target.values
idx = np.r_[rng.choice(np.where(target == 0)[0], 20, replace=False),
            rng.choice(np.where(target == 1)[0], 20, replace=False)]
rng.shuffle(idx)
feats = [c for c in bc.feature_names if c.startswith("mean ")]      # 10 nucleus features
df = bc.data.loc[idx, feats].T
df.columns = [f"P{i:02d}" for i in range(len(idx))]
group = np.where(target[idx] == 0, "Malignant", "Benign")
group_palette = {"Malignant": PALETTE[1], "Benign": PALETTE[0]}
title = "Breast tumours clustered by nucleus features"
df.iloc[:5, :6]
