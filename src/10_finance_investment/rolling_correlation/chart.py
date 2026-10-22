# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(5)
dates = pd.bdate_range("2015-01-01", "2024-12-31")
n = len(dates)
# Time-varying correlation with equities: bonds -0.35 until 2021, then +0.45; gold drifts around +0.05.
rho_bond = np.where(dates < "2021-10-01", -0.35, 0.45) + 0.15 * np.sin(np.arange(n) / 90)
rho_gold = 0.05 + 0.2 * np.sin(np.arange(n) / 260 + 1)
z_eq, z_b, z_g = rng.standard_normal((3, n))
eq = 0.010 * z_eq
bonds = 0.004 * (rho_bond * z_eq + np.sqrt(1 - rho_bond**2) * z_b)
gold = 0.009 * (rho_gold * z_eq + np.sqrt(1 - rho_gold**2) * z_g)
rets = pd.DataFrame({"Equities": eq, "Gov. bonds": bonds, "Gold": gold}, index=dates)
window = 63
rets.head()

# %% plot
base = rets.columns[0]
fig, ax = plt.subplots(figsize=(9, 4.8))
for i, col in enumerate(rets.columns[1:]):
    rc = rets[base].rolling(window).corr(rets[col])
    ax.plot(rc.index, rc, color=PALETTE[i], linewidth=1.6, label=f"{col} vs {base.lower()}")
    ax.annotate(col, (rc.index[-1], rc.iloc[-1]), xytext=(6, 0), textcoords="offset points",
                va="center", fontsize=9, color=PALETTE[i])
ax.axhline(0, color="#52514e", linewidth=1)
ax.set_ylim(-1, 1)
ax.set_ylabel(f"{window}-day correlation of daily returns")
ax.set_title(f"Correlation with {base.lower()} is not constant")
ax.legend(loc="lower left")
ax.margins(x=0.01)
fig.tight_layout()
