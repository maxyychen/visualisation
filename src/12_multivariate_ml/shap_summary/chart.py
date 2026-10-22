# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.colors import LinearSegmentedColormap
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# %% data
bc = load_breast_cancer(as_frame=True)
X = pd.DataFrame(StandardScaler().fit_transform(bc.data), columns=bc.data.columns)
y = 1 - bc.target                      # 1 = malignant
model = LogisticRegression(C=0.1, max_iter=5000).fit(X, y)
# Exact SHAP values for a linear model (log-odds scale): coef * (x - mean)
shap = pd.DataFrame(model.coef_[0] * (X - X.mean()).values, columns=X.columns)
order = shap.abs().mean().sort_values(ascending=False).index[:10]
shap.abs().mean()[order].round(2)

# %% plot
cmap = LinearSegmentedColormap.from_list("feat", ["#cde2fb", "#2a78d6", "#0d366b"])
fig, ax = plt.subplots(figsize=(8.5, 6))
rng = np.random.default_rng(0)
for row, feat in enumerate(order[::-1]):
    v = shap[feat].values
    # beeswarm-style jitter: spread points vertically in proportion to local density
    bins = np.round(v / 0.08)
    offs = np.zeros_like(v)
    for b in np.unique(bins):
        idx = np.where(bins == b)[0]
        k = len(idx)
        offs[idx] = (np.arange(k) - (k - 1) / 2) * min(0.035, 0.8 / max(k, 1))
    offs += rng.uniform(-0.01, 0.01, len(v))
    fv = X[feat].rank(pct=True).values
    sc = ax.scatter(v, row + offs, c=fv, cmap=cmap, s=9, alpha=0.9, linewidth=0, vmin=0, vmax=1)
ax.axvline(0, color="#52514e", lw=1)
ax.set_yticks(range(len(order)), [f.capitalize() for f in order[::-1]])
ax.grid(axis="y", visible=False)
ax.set_xlabel("Contribution to log-odds of malignancy  (← benign | malignant →)")
ax.set_title("What drives the malignancy model (top 10 features)")
cb = fig.colorbar(sc, ax=ax, pad=0.02, ticks=[0, 1], aspect=30)
cb.ax.set_yticklabels(["Low", "High"])
cb.set_label("Feature value (percentile)", color="#52514e")
cb.outline.set_visible(False)
fig.tight_layout()
