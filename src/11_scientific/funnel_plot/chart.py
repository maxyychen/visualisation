# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(2005)
n = 150
te = 0.05  # annual tracking error: alpha's year-to-year noise
years = np.round(rng.gamma(2.2, 3.0, n).clip(1, 25), 1)
order = np.argsort(-years)
true_alpha = np.zeros(n)
true_alpha[order[[0, 2]]] = 0.045   # two genuinely skilled, long-running funds
true_alpha[order[4]] = -0.045       # one that consistently destroys value
alpha = true_alpha + rng.normal(0, te / np.sqrt(years))
df = pd.DataFrame({"fund": [f"Fund {i:03d}" for i in range(1, n + 1)], "years": years, "alpha": alpha})
se = te / np.sqrt(df["years"])
df["z"] = df["alpha"] / se
df.sort_values("z").iloc[[0, 1, -2, -1]].round(3)

# %% plot
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.4), gridspec_kw={"width_ratios": [1.8, 1]})
t = np.linspace(0.8, df["years"].max() + 1, 300)
for z, shade, label in ((3.09, "#e9e8e4", "99.8% limits"), (1.96, "#dcdbd6", "95% limits")):
    a1.fill_between(t, -z * te / np.sqrt(t), z * te / np.sqrt(t), color=shade, linewidth=0, label=label)
a1.axhline(0, color="#52514e", linewidth=1)
out_hi, out_lo = df["z"] > 3.09, df["z"] < -3.09
inside = ~(out_hi | out_lo)
a1.scatter(df.loc[inside, "years"], df.loc[inside, "alpha"], s=22, color="#8f8e88", edgecolor="#fcfcfb",
           linewidth=0.8, label="Consistent with zero alpha", zorder=3)
a1.scatter(df.loc[out_hi, "years"], df.loc[out_hi, "alpha"], s=55, color=PALETTE[0], edgecolor="#fcfcfb",
           linewidth=1.2, label="Above 99.8% limit", zorder=4)
a1.scatter(df.loc[out_lo, "years"], df.loc[out_lo, "alpha"], s=55, color=PALETTE[1], edgecolor="#fcfcfb",
           linewidth=1.2, label="Below 99.8% limit", zorder=4)
for r in df[~inside].itertuples():
    a1.annotate(f"{r.fund}\n{r.alpha:+.1%}, {r.years:.0f} yrs", (r.years, r.alpha), xytext=(8, 0),
                textcoords="offset points", fontsize=8, va="center")
a1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:+.0%}"))
a1.set_xlabel("Track record (years)")
a1.set_ylabel("Annualised alpha vs. benchmark")
a1.set_title("Funnel plot: extremes on the left are mostly noise", fontsize=11)
a1.legend(loc="upper right", fontsize=8)
a1.set_xlim(0, df["years"].max() + 4)

top = df.nlargest(10, "alpha").iloc[::-1]
colors = np.where(top["z"] > 3.09, PALETTE[0], "#c9c8c3")
a2.barh(top["fund"], top["alpha"], color=colors, height=0.7)
for y, r in enumerate(top.itertuples()):
    a2.text(r.alpha + 0.002, y, f"{r.years:.1f} yrs", va="center", fontsize=8, color="#52514e")
a2.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:+.0%}"))
a2.set_xlim(0, top["alpha"].max() * 1.3)
a2.set_title("✗ A naive top-10 league table\n(blue = outside the funnel)", fontsize=11)
a2.grid(axis="y", visible=False)

fig.suptitle("150 funds: which alphas are skill and which are luck? (simulated)", x=0.01, ha="left",
             fontweight="bold", fontsize=13)
fig.tight_layout()
