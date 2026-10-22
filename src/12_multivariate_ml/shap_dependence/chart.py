# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.colors import LinearSegmentedColormap
from sklearn.linear_model import LogisticRegression

# %% data
rng = np.random.default_rng(17)
n = 3000
df = pd.DataFrame({
    "utilization": rng.beta(2, 3, n) * 100,                  # % of credit limit used
    "income": np.exp(rng.normal(np.log(60), 0.45, n)),       # $k per year
    "dti": rng.uniform(5, 45, n),                            # debt-to-income, %
})
z = (df - df.mean()) / df.std()
true_logit = -2.2 + 1.0 * z["utilization"] - 0.6 * z["income"] + 0.5 * z["dti"] \
    - 0.6 * z["utilization"] * z["income"]
df["default"] = rng.random(n) < 1 / (1 + np.exp(-true_logit))

# Fit: main effects on standardized features + one interaction column
X = z.assign(util_x_income=z["utilization"] * z["income"])
model = LogisticRegression(C=100, max_iter=2000).fit(X, df["default"])
b = dict(zip(X.columns, model.coef_[0]))
mu = z.mean()

# Exact interventional SHAP values on the log-odds scale (closed form for this model)
shap = pd.DataFrame({
    f: b[f] * (z[f] - mu[f]) for f in ["utilization", "income", "dti"]})
shap["utilization"] += 0.5 * b["util_x_income"] * (z["utilization"] - mu["utilization"]) * (z["income"] + mu["income"])
shap["income"] += 0.5 * b["util_x_income"] * (z["income"] - mu["income"]) * (z["utilization"] + mu["utilization"])
pd.Series(b).round(2)

# %% plot
cmap = LinearSegmentedColormap.from_list("income", ["#cde2fb", "#2a78d6", "#0d366b"])
order = np.argsort(rng.random(n))                          # random draw order: no color sits on top
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True)
for ax, feat, label in [(axes[0], "utilization", "Credit utilization (%)"),
                        (axes[1], "dti", "Debt-to-income (%)")]:
    sc = ax.scatter(df[feat].values[order], shap[feat].values[order], c=df["income"].values[order],
                    cmap=cmap, s=9, alpha=0.8, linewidth=0, norm=plt.matplotlib.colors.LogNorm(25, 160))
    ax.axhline(0, color="#52514e", linewidth=0.8)
    ax.set_xlabel(label)
    # rug of the feature's distribution
    ax.plot(df[feat], np.full(n, -2.9), "|", color="#b8b7b1",
            markersize=6, alpha=0.15)
axes[0].set_ylabel("SHAP contribution to log-odds of default")
axes[0].set_title("Utilization: effect depends on income")
axes[1].set_title("Debt-to-income: no interaction")
axes[0].set_ylim(-3, 4)
cb = fig.colorbar(sc, ax=axes, pad=0.02, shrink=0.9)
cb.set_label("Income ($k, color = interacting feature)")
cb.outline.set_visible(False)
cb.ax.minorticks_off()
cb.set_ticks([30, 50, 80, 120])
cb.set_ticklabels(["30", "50", "80", "120"])
