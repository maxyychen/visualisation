# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from sklearn.datasets import load_diabetes
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.inspection import PartialDependenceDisplay

# %% data
diab = load_diabetes(as_frame=True)
X, y = diab.data, diab.target
model = GradientBoostingRegressor(n_estimators=300, max_depth=2, learning_rate=0.05,
                                  random_state=0).fit(X, y)
print(f"R² on training data: {model.score(X, y):.2f}")
X.describe().loc[["mean", "std"], ["bmi", "s5"]].round(3)

# %% plot
fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), sharey=True)
PartialDependenceDisplay.from_estimator(
    model, X, ["bmi", "s5"], kind="both", subsample=80, random_state=0, ax=axes,
    ice_lines_kw={"color": "#b8b7b1", "alpha": 0.35, "linewidth": 0.7},
    pd_line_kw={"color": PALETTE[0], "linewidth": 2.5, "linestyle": "-"})
for ax, name in zip(axes, ["BMI (standardized)", "s5: log serum triglycerides (standardized)"]):
    ax.set_xlabel(name)
    ax.grid(True, color="#e6e5e1", linewidth=0.6)
    leg = ax.get_legend()
    if leg:
        leg.remove()
axes[0].set_ylabel("Predicted disease progression")
axes[1].set_ylabel("")
fig.suptitle("Progression rises sharply above average BMI and triglycerides",
             x=0.02, ha="left", fontsize=13, fontweight="bold")
fig.text(0.02, 0.005, "Gray: individual patients (ICE)   Blue: average effect (partial dependence)",
         fontsize=9, color="#52514e")
fig.tight_layout(rect=(0, 0.03, 1, 1))
