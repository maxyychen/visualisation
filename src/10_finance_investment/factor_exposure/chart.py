# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
import statsmodels.api as sm

# %% data
rng = np.random.default_rng(3)
n = 252 * 5
factors = pd.DataFrame({
    "Market": rng.standard_t(4, n) * 0.0095 / np.sqrt(2) + 0.0003,
    "Size (SMB)": rng.normal(0, 0.005, n),
    "Value (HML)": rng.normal(0, 0.005, n),
    "Momentum": rng.normal(0, 0.007, n),
    "Quality": rng.normal(0, 0.004, n),
})
true_beta = np.array([1.05, 0.05, 0.35, 0.12, -0.02])
fund = pd.Series(0.00002 + factors.values @ true_beta + rng.normal(0, 0.006, n), name="fund_excess")
fund.head()

# %% plot
model = sm.OLS(fund, sm.add_constant(factors)).fit()
ci = model.conf_int(0.05)
coef = model.params.drop("const")
ci = ci.drop("const")
order = coef.index[::-1]
y = np.arange(len(order))
ref = pd.Series(0.0, index=coef.index)
ref["Market"] = 1.0
signif = (ci[0] > ref) | (ci[1] < ref)

fig, ax = plt.subplots(figsize=(8.5, 4.6))
for yi, f in zip(y, order):
    color = PALETTE[0] if signif[f] else GRAY
    ax.hlines(yi, ci.loc[f, 0], ci.loc[f, 1], color=color, linewidth=2)
    ax.scatter(coef[f], yi, s=70, color=color, zorder=3, edgecolor="#fcfcfb", linewidth=1.5)
    ax.text(ci.loc[f, 1] + 0.02, yi, f"{coef[f]:.2f}", va="center", fontsize=9, color="#52514e")
ax.axvline(0, color="#52514e", linewidth=1)
ax.axvline(1, color="#c9c8c3", linewidth=1)
ax.text(1, len(order) - 0.45, "β = 1", ha="center", fontsize=8, color="#7a7974")
ax.set_yticks(y, order)
ax.set_xlabel("Estimated exposure (beta), 95% CI")
alpha_ann = model.params["const"] * 252
a_lo, a_hi = model.conf_int().loc["const"] * 252
ax.set_title("Factor exposures of the fund")
ax.text(0, -0.2, f"Alpha {alpha_ann:+.1%}/yr (95% CI {a_lo:+.1%} to {a_hi:+.1%})   ·   R² = {model.rsquared:.2f}"
        "   ·   Market beta tested against 1, others against 0", transform=ax.transAxes, fontsize=8.5,
        color="#52514e")
ax.grid(axis="y", visible=False)
ax.set_ylim(-0.6, len(order) - 0.2)
fig.tight_layout()
