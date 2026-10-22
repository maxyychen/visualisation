# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from scipy import stats

# %% data
rng = np.random.default_rng(23)
n, rho, nu = 2500, 0.45, 3
z = rng.multivariate_normal([0, 0], [[1, rho], [rho, 1]], n)
w = rng.chisquare(nu, n) / nu
u = stats.t.cdf(z / np.sqrt(w)[:, None], nu)                 # t-copula uniforms
rets = pd.DataFrame({"Index A": stats.t.ppf(u[:, 0], 4) * 0.009,
                     "Index B": stats.t.ppf(u[:, 1], 4) * 0.011})
rets.describe().round(4)

# %% plot
a, b = rets.columns
ua = rets[a].rank() / (len(rets) + 1)
ub = rets[b].rank() / (len(rets) + 1)
tau = stats.kendalltau(rets[a], rets[b]).statistic
rho_g = np.sin(np.pi * tau / 2)                              # Gaussian copula with the same Kendall tau
qs = np.linspace(0.01, 0.20, 20)
empirical = [((ua <= q) & (ub <= q)).sum() / (ua <= q).sum() for q in qs]
mvn = stats.multivariate_normal([0, 0], [[1, rho_g], [rho_g, 1]])
gaussian = [mvn.cdf([stats.norm.ppf(q)] * 2) / q for q in qs]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5), gridspec_kw={"wspace": 0.25})
qa, qb = rets[a].quantile(0.05), rets[b].quantile(0.05)
crash = (rets[a] <= qa) & (rets[b] <= qb)
ax1.scatter(rets.loc[~crash, a], rets.loc[~crash, b], s=6, color="#b8b7b1", alpha=0.6, linewidth=0)
ax1.scatter(rets.loc[crash, a], rets.loc[crash, b], s=16, color=PALETTE[1], edgecolor="#fcfcfb",
            linewidth=0.6, label=f"Both in worst 5% ({crash.sum()} days)")
ax1.axvline(qa, color="#52514e", linewidth=0.8)
ax1.axhline(qb, color="#52514e", linewidth=0.8)
for ax_, fmt in ((ax1.xaxis, None), (ax1.yaxis, None)):
    ax_.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
ax1.set_xlabel(f"{a} daily return")
ax1.set_ylabel(f"{b} daily return")
ax1.set_title(f"Daily returns (Kendall τ = {tau:.2f})", fontsize=11)
ax1.legend(loc="upper left", fontsize=9)

ax2.plot(qs, empirical, color=PALETTE[0], marker="o", markersize=4, label="Data (empirical)")
ax2.plot(qs, gaussian, color="#8f8e88", label="Gaussian model, same correlation")
ax2.plot(qs, qs, color="#d0cfca", linewidth=1, label="Independent")
ax2.set_xticks([0.01, 0.05, 0.10, 0.15, 0.20])
ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
ax2.set_xlabel("Tail threshold q (worst q of days)")
ax2.set_ylabel(f"P({b} in worst q | {a} in worst q)")
ax2.set_title("Lower-tail dependence", fontsize=11)
ax2.set_ylim(0, None)
ax2.legend(loc="lower right", fontsize=9)
fig.suptitle("Do they crash together? More often than correlation suggests (simulated)", x=0.06,
             ha="left", fontsize=14, fontweight="bold")
