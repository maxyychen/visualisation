# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

# %% data
wine = load_wine(as_frame=True)
X_tr, X_te, y_tr, y_te = train_test_split(wine.data, wine.target, test_size=0.35,
                                          stratify=wine.target, random_state=1)
rf = RandomForestClassifier(n_estimators=300, max_features=2, random_state=0).fit(X_tr, y_tr)
print(f"Test accuracy: {rf.score(X_te, y_te):.3f}")
res = permutation_importance(rf, X_te, y_te, n_repeats=30, random_state=0)
imp = pd.DataFrame(res.importances.T, columns=X_te.columns)
order = imp.median().sort_values().index
imp[order[::-1]].median().round(3)

# %% plot
fig, ax = plt.subplots(figsize=(8, 5.8))
ax.boxplot([imp[c] for c in order], vert=False, widths=0.6, patch_artist=True,
           boxprops=dict(facecolor="#9ec5f4", edgecolor=PALETTE[0]),
           medianprops=dict(color="#0d366b", linewidth=2),
           whiskerprops=dict(color=PALETTE[0]), capprops=dict(color=PALETTE[0]),
           flierprops=dict(marker="o", markersize=3, markerfacecolor=PALETTE[0], markeredgecolor="none"))
ax.set_yticks(range(1, len(order) + 1), [c.replace("_", " ") for c in order])
ax.axvline(0, color="#52514e", lw=1)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Drop in test accuracy when the feature is shuffled")
ax.set_title("A handful of features carry the forest; most add nothing")
fig.tight_layout()
