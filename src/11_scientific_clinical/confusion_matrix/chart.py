# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from sklearn.metrics import confusion_matrix

# %% data
rng = np.random.default_rng(10)
classes = ["Luminal A", "Luminal B", "HER2-enriched", "Basal-like"]
# row = true class; probabilities of each predicted class
P = np.array([[0.86, 0.11, 0.02, 0.01],
              [0.18, 0.72, 0.08, 0.02],
              [0.03, 0.09, 0.84, 0.04],
              [0.01, 0.02, 0.05, 0.92]])
n = [240, 150, 90, 120]
y_true = np.repeat(np.arange(4), n)
y_pred = np.concatenate([rng.choice(4, size=k, p=P[i]) for i, k in enumerate(n)])
cm = confusion_matrix(y_true, y_pred)
model_name = "Subtype classifier"
pd.DataFrame(cm, index=[f"true {c}" for c in classes], columns=[f"pred {c}" for c in classes])

# %% plot
pct = cm / cm.sum(axis=1, keepdims=True)
fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(pct, cmap=SEQ_CMAP, vmin=0, vmax=1)
for i in range(len(classes)):
    for j in range(len(classes)):
        ax.text(j, i, f"{cm[i, j]}\n{pct[i, j]:.0%}", ha="center", va="center", fontsize=10,
                color="white" if pct[i, j] > 0.55 else "#0b0b0b")
ax.set_xticks(range(len(classes)), classes, rotation=20); ax.set_yticks(range(len(classes)), classes)
ax.set_xlabel("Predicted class"); ax.set_ylabel("True class")
ax.grid(False)
for s in ax.spines.values():
    s.set_visible(False)
cb = fig.colorbar(im, ax=ax, shrink=0.8, format=lambda v, _: f"{v:.0%}")
cb.set_label("Row % (recall)"); cb.outline.set_visible(False)
ax.set_title(f"{model_name}, accuracy {np.trace(cm) / cm.sum():.1%}")
fig.tight_layout()

# %% real-data
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
bc = load_breast_cancer()
X_tr, X_te, y_tr, y_te = train_test_split(bc.data, bc.target, test_size=0.4, random_state=0,
                                          stratify=bc.target)
clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_tr, y_tr)
classes = ["Malignant", "Benign"]                   # target 0 = malignant, 1 = benign
y_true, y_pred = y_te, clf.predict(X_te)
cm = confusion_matrix(y_true, y_pred)
model_name = "Breast-cancer classifier (logistic regression)"
pd.DataFrame(cm, index=[f"true {c}" for c in classes], columns=[f"pred {c}" for c in classes])
