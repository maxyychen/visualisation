# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(2025)
n_paths, years = 5000, 35
start_age, start_wealth, spending = 60, 1_500_000, 70_000      # real (today's) dollars
mu, sigma = 0.045, 0.11                                         # real annual return, volatility
log_ret = rng.normal(np.log1p(mu) - sigma ** 2 / 2, sigma, (n_paths, years))

wealth = np.empty((n_paths, years + 1))
wealth[:, 0] = start_wealth
for t in range(years):                       # withdraw at the start of each year, then grow
    wealth[:, t + 1] = np.maximum((wealth[:, t] - spending) * np.exp(log_ret[:, t]), 0)
ages = start_age + np.arange(years + 1)
bands = pd.DataFrame(np.percentile(wealth, [10, 25, 50, 75, 90], axis=0).T / 1e6, index=ages,
                     columns=["p10", "p25", "p50", "p75", "p90"])
p_lasting = pd.Series((wealth > 0).mean(axis=0), index=ages)
bands.iloc[::5].round(2)

# %% plot
fig, (ax, axp) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [2, 1]})
for path in wealth[rng.choice(n_paths, 30, replace=False)]:
    ax.plot(ages, path / 1e6, color="#b8b7b1", linewidth=0.6, alpha=0.6)
ax.fill_between(ages, bands["p10"], bands["p90"], color="#b7d3f6", linewidth=0, label="10th–90th percentile")
ax.fill_between(ages, bands["p25"], bands["p75"], color="#6da7ec", linewidth=0, label="25th–75th percentile")
ax.plot(ages, bands["p50"], color="#104281", linewidth=2.4, label="Median")
ax.axhline(0, color="#52514e", linewidth=0.8)
ax.set_xlabel("Age")
ax.set_ylabel("Portfolio value ($M, today's dollars)")
ax.set_title("Range of outcomes (5,000 simulations)")
ax.legend(loc="upper left")

axp.plot(ages, p_lasting * 100, color=PALETTE[0], linewidth=2.4)
p95 = p_lasting.loc[95]
axp.scatter(95, p95 * 100, s=60, color=PALETTE[0], edgecolor="#fcfcfb", linewidth=2, zorder=3)
axp.annotate(f"{p95:.0%} chance the money\nlasts to age 95", (95, p95 * 100), xytext=(-10, -40),
             textcoords="offset points", ha="right", fontsize=9.5, fontweight="bold")
axp.set_ylim(0, 105)
axp.set_xlabel("Age")
axp.set_ylabel("Paths with money left (%)")
axp.set_title("Probability of success")
fig.suptitle(r"Retirement plan: \$1.5M at 60, spending \$70k/yr (illustrative)", x=0.01, ha="left",
             fontsize=13, fontweight="bold")
fig.tight_layout()
