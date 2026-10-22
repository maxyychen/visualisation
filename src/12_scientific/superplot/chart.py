# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from scipy import stats

# %% data
rng = np.random.default_rng(2020)
markets = ["Market 1", "Market 2", "Market 3", "Market 4"]
baseline = [52, 44, 58, 48]   # markets differ in level
lift = [6.0, -0.5, 4.5, 1.0]  # ...and in how much the new price changes spend
rows = []
for mkt, base, d in zip(markets, baseline, lift):
    for cond, shift in (("Control", 0.0), ("New pricing", d)):
        rows.append(pd.DataFrame({"market": mkt, "condition": cond,
                                  "spend": rng.normal(base + shift, 12, 1000).clip(0)}))
df = pd.concat(rows, ignore_index=True)
conditions = ["Control", "New pricing"]
rep = df.groupby(["market", "condition"])["spend"].mean().unstack()[conditions]
rep.round(1)

# %% plot
naive_p = stats.ttest_ind(*(df.loc[df["condition"] == c, "spend"] for c in conditions)).pvalue
paired_p = stats.ttest_rel(rep[conditions[1]], rep[conditions[0]]).pvalue
markers = ["o", "s", "^", "D"]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.2), gridspec_kw={"width_ratios": [1, 1.7]})

# The conventional chart: every customer counted as an independent n
m = df.groupby("condition")["spend"].agg(["mean", "sem"]).loc[conditions]
a1.bar(range(2), m["mean"], yerr=m["sem"], color=GRAY, width=0.6, capsize=6)
a1.set_xticks(range(2), conditions)
a1.set_ylim(0, 75)
a1.set_ylabel("Monthly spend ($)")
p_text = f"p = {naive_p:.4f}" if naive_p >= 1e-4 else "p < 0.0001"
a1.set_title(f"✗ n = {len(df) // 2} per arm\nmean ± SEM, {p_text}", fontsize=11)
a1.grid(axis="x", visible=False)

# The SuperPlot: customers colored by market, market means as big markers, test on market means
xr = np.random.default_rng(1)
for i, (mkt, mk) in enumerate(zip(markets, markers)):
    for x, cond in enumerate(conditions):
        vals = df.loc[(df["market"] == mkt) & (df["condition"] == cond), "spend"]
        a2.scatter(x + xr.uniform(-0.28, 0.28, len(vals)), vals, s=4, color=PALETTE[i], alpha=0.18,
                   marker=mk, linewidths=0)
    a2.plot([0, 1], rep.loc[mkt, conditions], color=PALETTE[i], linewidth=1.5, zorder=4)
    a2.scatter([0, 1], rep.loc[mkt, conditions], s=120, color=PALETTE[i], marker=mk,
               edgecolor="#0b0b0b", linewidth=1.2, zorder=5, label=mkt)
grand = rep.mean()
a2.hlines(grand.values, np.arange(2) - 0.38, np.arange(2) + 0.38, color="#0b0b0b", linewidth=2.2, zorder=6)
a2.set_xticks(range(2), conditions)
a2.set_xlim(-0.6, 1.6)
a2.set_ylabel("Monthly spend ($)")
a2.set_title(f"✓ SuperPlot: n = {len(markets)} markets\npaired t-test on market means, p = {paired_p:.2f}",
             fontsize=11)
a2.legend(loc="upper left", ncol=4, fontsize=8, markerscale=0.7, bbox_to_anchor=(0, 1.0))
a2.set_ylim(0, 125)
a2.grid(axis="x", visible=False)
a2.text(1.42, grand.iloc[1], "mean of\nmarket means", fontsize=8, va="center", color="#52514e")

fig.suptitle("Pricing test: the same data, analysed at the wrong and the right level (simulated)",
             x=0.01, ha="left", fontweight="bold", fontsize=13)
fig.tight_layout()
