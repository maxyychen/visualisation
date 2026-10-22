# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(8)
n = 400
t_relapse = rng.weibull(1.2, n) * 22          # years
t_death = rng.weibull(1.6, n) * 14
t_censor = rng.uniform(4, 10, n)
time = np.minimum.reduce([t_relapse, t_death, t_censor]).round(2)
cause = np.select([time == t_relapse.round(2), time == t_death.round(2)], [1, 2], default=0)
df = pd.DataFrame({"years": time, "cause": cause})   # 0 = censored, 1 = relapse, 2 = death
df["cause"].map({0: "censored", 1: "relapse", 2: "death w/o relapse"}).value_counts()

# %% plot
def aalen_johansen(t, c, causes=(1, 2)):
    """Cumulative incidence per cause plus 1-KM for cause 1 (treating others as censored)."""
    times = np.unique(t[c > 0])
    surv, km1 = 1.0, 1.0
    cif = {k: [0.0] for k in causes}
    naive = [0.0]
    for u in times:
        at_risk = (t >= u).sum()
        d = {k: ((t == u) & (c == k)).sum() for k in causes}
        for k in causes:
            cif[k].append(cif[k][-1] + surv * d[k] / at_risk)
        surv *= 1 - sum(d.values()) / at_risk
        km1 *= 1 - d[causes[0]] / at_risk
        naive.append(1 - km1)
    return np.r_[0, times], {k: np.array(v) for k, v in cif.items()}, np.array(naive)

t_grid, cif, naive = aalen_johansen(df["years"].values, df["cause"].values)
fig, ax = plt.subplots(figsize=(8.5, 5))
ax.step(t_grid, naive, where="post", color=GRAY, linewidth=2)
ax.step(t_grid, cif[1], where="post", color=PALETTE[0], linewidth=2.2)
ax.step(t_grid, cif[2], where="post", color=PALETTE[1], linewidth=2.2)
end = t_grid[-1]
labels = [  # (curve end value, text, style)
    (naive[-1], f"1 − KM for relapse {naive[-1]:.0%}\n(treats deaths as censored)", dict(color="#7a7974")),
    (cif[1][-1], f"Relapse {cif[1][-1]:.0%}", dict(color="#0b0b0b", fontweight="bold")),
    (cif[2][-1], f"Death without relapse {cif[2][-1]:.0%}", dict(color="#0b0b0b")),
]
labels.sort(key=lambda l: l[0])
ys = [l[0] for l in labels]
for i in range(1, len(ys)):                      # push labels apart so they never overlap
    ys[i] = max(ys[i], ys[i - 1] + 0.045)
for (yv, text, kw), yl in zip(labels, ys):
    ax.annotate(text, xy=(end, yv), xytext=(end + 0.35, yl), va="center", fontsize=9.5,
                arrowprops=dict(arrowstyle="-", color="#b8b7b1", linewidth=0.8), **kw)
ax.set_xlim(0, end + 4.2)
ax.set_ylim(0, max(naive.max(), 0.5) * 1.1)
ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
ax.set_xlabel("Years since surgery")
ax.set_ylabel("Cumulative incidence")
ax.set_title(f"Relapse with death as a competing risk (n = {len(df)})")
fig.tight_layout()
