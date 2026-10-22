# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, learning_curve
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

# %% data
X, y = load_breast_cancer(return_X_y=True)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
models = {
    "Logistic regression": make_pipeline(StandardScaler(), LogisticRegression(C=0.5, max_iter=5000)),
    "Decision tree (unpruned)": DecisionTreeClassifier(random_state=0),
}
curves = {}
for name, m in models.items():
    sizes, tr, va = learning_curve(m, X, y, cv=cv, train_sizes=np.linspace(0.1, 1, 8), scoring="accuracy")
    curves[name] = (sizes, tr, va)
pd.DataFrame({name: c[2].mean(axis=1) for name, c in curves.items()}, index=sizes).round(3)

# %% plot
fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), sharey=True)
for ax, (name, (sizes, tr, va)) in zip(axes, curves.items()):
    for scores, color, label in [(tr, PALETTE[0], "Training"), (va, PALETTE[1], "Cross-validation")]:
        mu, sd = scores.mean(axis=1), scores.std(axis=1)
        ax.fill_between(sizes, mu - sd, mu + sd, color=color, alpha=0.18, linewidth=0)
        ax.plot(sizes, mu, color=color, marker="o", markersize=5, label=label)
    ax.set_title(name, fontsize=11.5)
    ax.set_xlabel("Training examples")
axes[0].set_ylabel("Accuracy (higher is better)")
axes[0].set_ylim(0.85, 1.01)
axes[0].legend(loc="lower right")
fig.suptitle("The tree overfits; logistic regression has converged",
             x=0.02, ha="left", fontsize=13, fontweight="bold")
fig.tight_layout()
