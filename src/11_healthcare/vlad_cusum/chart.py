# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from vizlib.health import vlad, ra_cusum

# %% data
rng = np.random.default_rng(1998)
n, change = 600, 400
logit = -3.1 + 0.8 * rng.normal(size=n) + 0.6 * rng.normal(size=n)   # pre-operative risk model
risk = 1 / (1 + np.exp(-logit))
odds = risk / (1 - risk)
true_odds = np.where(np.arange(n) >= change, odds * 2.5, odds)       # deterioration from op 400
died = (rng.random(n) < true_odds / (1 + true_odds)).astype(int)
h = 4.5
df = pd.DataFrame({"operation": np.arange(1, n + 1), "predicted_risk": risk.round(3), "died": died})
df["vlad"] = vlad(df["died"], df["predicted_risk"])
df["cusum"] = ra_cusum(df["died"], df["predicted_risk"], odds_ratio=2.0, h=h)
signals = df.index[df["cusum"] > h]
df.groupby(df["operation"] > change)[["died", "predicted_risk"]].sum().round(1)

# %% plot
fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [1.2, 1]})
x = df["operation"]
a1.plot(x, df["vlad"], color=PALETTE[0], linewidth=1.5)
a1.axhline(0, color="#52514e", linewidth=1)
a1.set_ylabel("Expected − observed deaths\n(\"statistical lives saved\")")
a1.set_title("VLAD: cumulative expected minus observed deaths", fontsize=11)
a1.text(8, a1.get_ylim()[1], "above 0: fewer deaths than the case mix predicts", fontsize=8.5,
        color="#52514e", va="top")
a2.plot(x, df["cusum"], color=PALETTE[0], linewidth=1.5)
a2.axhline(h, color="#b8b7b1", linewidth=1.2)
a2.text(8, h + 0.15, f"threshold h = {h}", fontsize=8.5, color="#52514e", va="bottom")
a2.scatter(x[signals], df["cusum"][signals], s=80, color=PALETTE[1], edgecolor="#fcfcfb", linewidth=1.5,
           zorder=4)
for i in signals:
    a2.annotate(f"signal: op {x[i]}", (x[i], df['cusum'][i]), xytext=(6, 4), textcoords="offset points",
                fontsize=8.5)
a2.set_ylim(0, h + 1.5)
a2.set_ylabel("Risk-adjusted CUSUM\n(evidence of doubled odds)")
a2.set_xlabel("Consecutive operation")
a2.set_title("Risk-adjusted Bernoulli CUSUM (odds ratio 2), reset after each signal", fontsize=11)
for ax in (a1, a2):
    ax.axvline(change, color="#52514e", linewidth=1)
a1.annotate("true odds of death ×2.5\nfrom here (simulated)", (change, a1.get_ylim()[0]), xytext=(6, 6),
            textcoords="offset points", fontsize=8.5, va="bottom")
fig.suptitle("Monitoring 600 cardiac operations, adjusted for each patient's risk (simulated)", x=0.01,
             ha="left", fontweight="bold", fontsize=13)
fig.tight_layout()
