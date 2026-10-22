# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.calibration import calibration_curve

# %% data
X, y = make_classification(n_samples=8000, n_features=20, n_informative=2, n_redundant=10,
                           random_state=2)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.5, random_state=2)
models = {"Logistic regression": LogisticRegression(max_iter=1000), "Naive Bayes": GaussianNB()}
probs = {name: m.fit(X_tr, y_tr).predict_proba(X_te)[:, 1] for name, m in models.items()}
df = pd.DataFrame({"y_true": y_te, **probs})
df.head()

# %% plot
fig, (ax, axh) = plt.subplots(2, 1, figsize=(6.5, 7.5), height_ratios=[3, 1], sharex=True)
ax.plot([0, 1], [0, 1], color=GRAY, linewidth=1, label="Perfectly calibrated")
bins = np.linspace(0, 1, 21)
for i, name in enumerate(probs):
    frac_pos, mean_pred = calibration_curve(df["y_true"], df[name], n_bins=10)
    ax.plot(mean_pred, frac_pos, "o-", color=PALETTE[i], markersize=6, label=name,
            markeredgecolor="#fcfcfb", markeredgewidth=1.2)
    axh.hist(df[name], bins=bins, histtype="step", color=PALETTE[i], linewidth=1.8)
ax.set_ylabel("Observed fraction of positives")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_title("Calibration plot")
ax.legend(loc="upper left")
axh.set_xlabel("Mean predicted probability"); axh.set_ylabel("Count")
fig.tight_layout()

