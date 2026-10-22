# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
import statsmodels.api as sm
from scipy import stats
from sklearn.datasets import load_diabetes
from statsmodels.nonparametric.smoothers_lowess import lowess

# %% data
diab = load_diabetes(as_frame=True)
X = sm.add_constant(diab.data)
fit = sm.OLS(diab.target, X).fit()
infl = fit.get_influence()
d = pd.DataFrame({
    "fitted": fit.fittedvalues, "resid": fit.resid,
    "std_resid": infl.resid_studentized_internal,
    "leverage": infl.hat_matrix_diag, "cooks": infl.cooks_distance[0],
})
print(f"R² = {fit.rsquared:.2f}, n = {int(fit.nobs)}, p = {int(fit.df_model)}")
d.sort_values("cooks", ascending=False).head().round(3)

# %% plot
def trend(ax, x, y):
    sm_ = lowess(y, x, frac=0.6)
    ax.plot(sm_[:, 0], sm_[:, 1], color=PALETTE[1], lw=2)

pt = dict(s=14, alpha=0.55, color=PALETTE[0], linewidth=0)
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
ax = axes[0, 0]
ax.scatter(d["fitted"], d["resid"], **pt); trend(ax, d["fitted"], d["resid"])
ax.axhline(0, color="#52514e", lw=1)
ax.set(title="Residuals vs fitted", xlabel="Fitted value", ylabel="Residual")
ax = axes[0, 1]
(osm, osr), (slope, icpt, _) = stats.probplot(d["std_resid"], dist="norm")
ax.scatter(osm, osr, **pt)
ax.plot(osm, slope * osm + icpt, color=PALETTE[1], lw=2)
ax.set(title="Normal Q-Q", xlabel="Theoretical quantile", ylabel="Standardized residual")
ax = axes[1, 0]
sl = np.sqrt(np.abs(d["std_resid"]))
ax.scatter(d["fitted"], sl, **pt); trend(ax, d["fitted"], sl)
ax.set(title="Scale-location", xlabel="Fitted value", ylabel="√|standardized residual|")
ax = axes[1, 1]
ax.scatter(d["leverage"], d["std_resid"], **pt); trend(ax, d["leverage"], d["std_resid"])
ax.axhline(0, color="#52514e", lw=1)
p = int(fit.df_model) + 1
hx = np.linspace(d["leverage"].min() * 0.9, d["leverage"].max() * 1.1, 100)
hy = np.sqrt(0.5 * p * (1 - hx) / hx)          # Cook's distance = 0.5 contour
ax.plot(hx, hy, color="#b8b7b1", lw=1)
ax.plot(hx, -hy, color="#b8b7b1", lw=1)
ax.set_ylim(-4, 4)
note = ("Cook's D 0.5 contour is beyond the plotted range:\nno single point is highly influential"
        if hy.min() > 4 else "gray curves: Cook's D = 0.5")
ax.text(0.98, 0.97, note, transform=ax.transAxes, ha="right", va="top", fontsize=8, color="#52514e")
for i in d["cooks"].nlargest(3).index:
    ax.annotate(str(i), (d.at[i, "leverage"], d.at[i, "std_resid"]), xytext=(4, 2),
                textcoords="offset points", fontsize=8, color="#52514e")
ax.set(title="Residuals vs leverage", xlabel="Leverage", ylabel="Standardized residual")
fig.suptitle("OLS diagnostics: disease progression ~ 10 baseline variables",
             x=0.02, ha="left", fontsize=13, fontweight="bold")
fig.tight_layout()
