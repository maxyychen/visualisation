# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve, average_precision_score

# %% data
X, y = make_classification(n_samples=6000, n_features=20, n_informative=6, weights=[0.92],
                           flip_y=0.02, random_state=1)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=1, stratify=y)
models = {"Logistic regression": LogisticRegression(max_iter=1000),
          "Random forest": RandomForestClassifier(n_estimators=300, random_state=1)}
scores = {name: m.fit(X_tr, y_tr).predict_proba(X_te)[:, 1] for name, m in models.items()}
df = pd.DataFrame({"y_true": y_te, **scores})
print(f"prevalence = {df.y_true.mean():.3f}")
df.head()

# %% plot
fig, ax = plt.subplots(figsize=(6.5, 6))
for i, name in enumerate(scores):
    p, r, _ = precision_recall_curve(df["y_true"], df[name])
    ap = average_precision_score(df["y_true"], df[name])
    ax.plot(r, p, color=PALETTE[i], label=f"{name} (AP = {ap:.3f})")
prev = df["y_true"].mean()
ax.axhline(prev, color=GRAY, linewidth=1, label=f"No skill (prevalence = {prev:.2f})")
ax.set_xlabel("Recall (sensitivity)"); ax.set_ylabel("Precision (PPV)")
ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
ax.set_title("Precision–recall curve, test set")
ax.legend(loc="lower left")
fig.tight_layout()

# %% real-data
from sklearn.datasets import load_breast_cancer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
bc = load_breast_cancer()
X, y = bc.data, 1 - bc.target                       # 1 = malignant
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=1, stratify=y)

models = {"Logistic regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
          "Random forest": RandomForestClassifier(n_estimators=300, random_state=1)}
scores = {name: m.fit(X_tr, y_tr).predict_proba(X_te)[:, 1] for name, m in models.items()}
df = pd.DataFrame({"y_true": y_te, **scores})
print(f"prevalence = {df.y_true.mean():.3f}")
df.head()
