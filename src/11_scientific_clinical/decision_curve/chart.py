# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# %% data
X, y = make_classification(n_samples=3000, n_features=8, n_informative=5, weights=[0.8],
                           class_sep=0.8, random_state=4)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=4, stratify=y)
p_full = LogisticRegression(max_iter=1000).fit(X_tr, y_tr).predict_proba(X_te)[:, 1]
p_reduced = LogisticRegression(max_iter=1000).fit(X_tr[:, :2], y_tr).predict_proba(X_te[:, :2])[:, 1]
print(f"test n = {len(y_te)}, prevalence = {y_te.mean():.1%}")

# %% plot
def net_benefit(y, p, thresholds):
    n = len(y)
    out = []
    for pt in thresholds:
        treat = p >= pt
        tp = (treat & (y == 1)).sum() / n
        fp = (treat & (y == 0)).sum() / n
        out.append(tp - fp * pt / (1 - pt))
    return np.array(out)

th = np.linspace(0.01, 0.6, 120)
prev = y_te.mean()
nb_all = prev - (1 - prev) * th / (1 - th)
fig, ax = plt.subplots(figsize=(8.5, 5))
ax.plot(th, nb_all, color=GRAY, linewidth=1.6, label="Treat all")
ax.axhline(0, color="#52514e", linewidth=1.2, label="Treat none")
ax.plot(th, net_benefit(y_te, p_full, th), color=PALETTE[0], label="Full model (8 predictors)")
ax.plot(th, net_benefit(y_te, p_reduced, th), color=PALETTE[1], label="Reduced model (2 predictors)")
ax.set_ylim(-0.05, prev + 0.03)
ax.set_xlim(0, 0.6)
ax.xaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
ax.set_xlabel("Threshold probability (risk at which you would biopsy)")
ax.set_ylabel("Net benefit")
ax.set_title("Decision curve: is the model worth using?")
ax.legend(loc="upper right")
fig.tight_layout()
