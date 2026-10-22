# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, roc_auc_score

# %% data
X, y = make_classification(n_samples=3000, n_features=20, n_informative=6, weights=[0.7],
                           flip_y=0.05, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=0, stratify=y)
models = {"Logistic regression": LogisticRegression(max_iter=1000),
          "Random forest": RandomForestClassifier(n_estimators=300, random_state=0)}
scores = {name: m.fit(X_tr, y_tr).predict_proba(X_te)[:, 1] for name, m in models.items()}
df = pd.DataFrame({"y_true": y_te, **scores})
df.head()

# %% plot
fig, ax = plt.subplots(figsize=(6, 6))
for i, name in enumerate(scores):
    fpr, tpr, _ = roc_curve(df["y_true"], df[name])
    ax.plot(fpr, tpr, color=PALETTE[i], label=f"{name} (AUC = {roc_auc_score(df['y_true'], df[name]):.3f})")
ax.plot([0, 1], [0, 1], color=GRAY, linewidth=1, label="Chance (AUC = 0.5)")
ax.set_xlabel("False positive rate (1 − specificity)")
ax.set_ylabel("True positive rate (sensitivity)")
ax.set_xlim(0, 1); ax.set_ylim(0, 1.01); ax.set_aspect("equal")
ax.set_title("ROC curve, test set")
ax.legend(loc="lower right")
fig.tight_layout()

# %% real-data
from sklearn.datasets import load_breast_cancer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
bc = load_breast_cancer()
X, y = bc.data, 1 - bc.target                       # 1 = malignant
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=0, stratify=y)

models = {"Logistic regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
          "Random forest": RandomForestClassifier(n_estimators=300, random_state=0)}
scores = {name: m.fit(X_tr, y_tr).predict_proba(X_te)[:, 1] for name, m in models.items()}
df = pd.DataFrame({"y_true": y_te, **scores})
df.head()
