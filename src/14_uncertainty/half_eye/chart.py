# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from scipy.stats import gaussian_kde

# %% data
rng = np.random.default_rng(21)
n = 4000
draws = pd.DataFrame({
    "Exercise programme": rng.normal(4.5, 1.6, n),
    "Salt reduction": rng.normal(3.2, 1.3, n),
    "App-based coaching": rng.gamma(1.6, 1.5, n) - 0.6,
    "Medication": rng.normal(9.0, 1.4, n),
})
summary = draws.quantile([0.025, 0.17, 0.5, 0.83, 0.975]).T.round(1)
summary.columns = ["2.5%", "17%", "median", "83%", "97.5%"]
order = summary["median"].sort_values().index
summary.loc[order]

# %% plot
fig, ax = plt.subplots(figsize=(8.5, 5.2))
xs = np.linspace(-4, 15, 500)
for i, name in enumerate(order):
    v = draws[name].values
    dens = gaussian_kde(v)(xs)
    dens = dens / dens.max() * 0.72
    ax.fill_between(xs, i, i + dens, color=PALETTE[0], alpha=0.35, linewidth=0)
    ax.plot(xs, i + dens, color=PALETTE[0], lw=1)
    lo95, lo66, med, hi66, hi95 = np.quantile(v, [0.025, 0.17, 0.5, 0.83, 0.975])
    ax.plot([lo95, hi95], [i, i], color="#0b0b0b", lw=1.3, solid_capstyle="round")
    ax.plot([lo66, hi66], [i, i], color="#0b0b0b", lw=4, solid_capstyle="round")
    ax.scatter([med], [i], s=55, color="#fcfcfb", edgecolor="#0b0b0b", linewidth=1.6, zorder=4)
ax.axvline(0, color="#52514e", lw=1)
ax.set_yticks(range(len(order)), order)
ax.set_ylim(-0.4, len(order) - 0.15)
ax.set_xlim(-4, 15)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Reduction in systolic blood pressure (mmHg)  (→ more benefit)")
ax.set_title("Estimated benefit of four interventions (posterior)")
ax.text(14.8, -0.32, "dot = median · thick = 66% · thin = 95% interval", ha="right",
        fontsize=8.5, color="#52514e")
fig.tight_layout()
