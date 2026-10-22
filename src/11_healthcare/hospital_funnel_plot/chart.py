# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from vizlib.health import funnel_limits

# %% data
rng = np.random.default_rng(2005)
k = 120
discharges = np.round(np.exp(rng.normal(7.0, 0.8, k))).astype(int).clip(80, 12000)
true_rate = np.full(k, 0.14)
by_size = np.argsort(-discharges)
true_rate[by_size[[1, 4]]] = 0.175      # two large hospitals truly readmit more
true_rate[by_size[6]] = 0.11            # one truly readmits less
readmitted = rng.binomial(discharges, true_rate)
df = pd.DataFrame({"hospital": [f"H{i:03d}" for i in range(1, k + 1)], "discharges": discharges,
                   "readmitted": readmitted})
df["rate"] = df["readmitted"] / df["discharges"]
target = df["readmitted"].sum() / df["discharges"].sum()
lo998, hi998 = funnel_limits(target, df["discharges"], level=0.998)
df["outside"] = np.where(df["rate"] > hi998, "high", np.where(df["rate"] < lo998, "low", ""))
df[df["outside"] != ""]

# %% plot
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.4), gridspec_kw={"width_ratios": [1.8, 1]})
n_grid = np.unique(np.geomspace(60, 13000, 300).astype(int))
for level, shade, label in ((0.998, "#e9e8e4", "99.8% limits"), (0.95, "#dcdbd6", "95% limits")):
    lo, hi = funnel_limits(target, n_grid, level=level)
    a1.fill_between(n_grid, lo, hi, color=shade, linewidth=0, label=label, step="mid")
a1.axhline(target, color="#52514e", linewidth=1)
a1.text(13000, target, f" pooled {target:.1%}", va="center", fontsize=8.5, color="#52514e")
inside = df["outside"] == ""
a1.scatter(df.loc[inside, "discharges"], df.loc[inside, "rate"], s=22, color="#8f8e88", edgecolor="#fcfcfb",
           linewidth=0.8, zorder=3, label="Within expected variation")
for kind, color, label in (("high", PALETTE[1], "Above 99.8% limit"), ("low", PALETTE[0], "Below 99.8% limit")):
    sel = df["outside"] == kind
    a1.scatter(df.loc[sel, "discharges"], df.loc[sel, "rate"], s=60, color=color, edgecolor="#fcfcfb",
               linewidth=1.2, zorder=4, label=label)
high = df[df["outside"] == "high"].sort_values("rate", ascending=False)
for i, r in enumerate(high.itertuples()):     # alternate above-left / below-right so close pairs don't collide
    up = i % 2 == 0
    a1.annotate(f"{r.hospital}  {r.rate:.1%}", (r.discharges, r.rate), xytext=(-8 if up else 8, 9 if up else -9),
                textcoords="offset points", fontsize=8.5, va="center", ha="right" if up else "left")
for r in df[df["outside"] == "low"].itertuples():
    a1.annotate(f"{r.hospital}  {r.rate:.1%}", (r.discharges, r.rate), xytext=(8, 0),
                textcoords="offset points", fontsize=8.5, va="center")
a1.set_xscale("log")
a1.set_xlim(50, 40000)
a1.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
a1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
a1.set_xlabel("Discharges per year (log scale)")
a1.set_ylabel("30-day readmission rate")
a1.set_title("Funnel plot: small hospitals vary most by chance", fontsize=11)
a1.legend(loc="upper right", fontsize=8)

top = df.nlargest(10, "rate").iloc[::-1]
colors = np.where(top["outside"] == "high", PALETTE[1], "#c9c8c3")
a2.barh(top["hospital"], top["rate"], color=colors, height=0.7)
for y, r in enumerate(top.itertuples()):
    a2.text(r.rate + 0.002, y, f"{r.discharges:,} discharges" + ("  · above 99.8%" if r.outside == "high" else ""), va="center", fontsize=8, color="#52514e")
a2.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
a2.set_xlim(0, top["rate"].max() * 1.75)
a2.set_title("✗ A naive 'worst 10' league table\n(orange = really outside the funnel)", fontsize=11)
a2.grid(axis="y", visible=False)
fig.suptitle("Which hospitals really readmit more patients? (simulated)", x=0.01, ha="left",
             fontweight="bold", fontsize=13)
fig.tight_layout()
