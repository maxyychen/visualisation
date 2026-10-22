# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(12)
visits = np.array([0, 3, 6, 9, 12, 18, 24])
rows = []
for arm, slope_mu in [("Placebo", -0.55), ("Treatment", -0.12)]:
    for i in range(40):
        pid = f"{arm[0]}{i:02d}"
        base = rng.normal(62, 9)
        slope = rng.normal(slope_mu, 0.25)
        if arm == "Treatment" and i == 7:
            slope = -0.9                                     # an atypical decliner to highlight
        last = rng.choice([12, 18, 24, 24, 24, 24])          # dropout
        for v in visits[visits <= last]:
            if v > 0 and rng.random() < 0.08:                # missed visit
                continue
            month = v + rng.normal(0, 0.4) if v else 0
            rows.append({"arm": arm, "patient": pid, "month": month, "visit": v,
                         "egfr": base + slope * month + rng.normal(0, 2.5)})
df = pd.DataFrame(rows)
df.head()

# %% plot
highlight = "T07"
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True)
for ax, (arm, g) in zip(axes, df.groupby("arm")):
    for pid, p in g.groupby("patient"):
        if pid != highlight:
            ax.plot(p["month"], p["egfr"], color=GRAY, linewidth=0.8, alpha=0.7)
    summary = g.groupby("visit")["egfr"].agg(["mean", "std", "count"])
    ci = 1.96 * summary["std"] / np.sqrt(summary["count"])
    ax.fill_between(summary.index, summary["mean"] - ci, summary["mean"] + ci, color=PALETTE[0], alpha=0.2, linewidth=0)
    ax.plot(summary.index, summary["mean"], color=PALETTE[0], linewidth=3, marker="o", markersize=5,
            markeredgecolor="#fcfcfb", markeredgewidth=1.2)
    ax.text(24.4, summary["mean"].iloc[-1], f"Mean\n{summary['mean'].iloc[-1]:.0f}", color="#0b0b0b",
            fontsize=9, va="center", fontweight="bold")
    if highlight in set(g["patient"]):
        p = g[g["patient"] == highlight]
        ax.plot(p["month"], p["egfr"], color=PALETTE[1], linewidth=2)
        ax.text(p["month"].iloc[-1] + 0.4, p["egfr"].iloc[-1], f"Patient {highlight}", color="#0b0b0b",
                fontsize=9, va="center")
    ax.set_title(f"{arm} (n = {g['patient'].nunique()})")
    ax.set_xticks(visits)
    ax.set_xlim(-0.5, 28.5)
    ax.set_xlabel("Months since baseline")
axes[0].set_ylabel("eGFR (mL/min/1.73 m²)")
fig.suptitle("Kidney function trajectories: individuals (gray) and arm mean ± 95% CI (blue)",
             x=0.01, ha="left", fontsize=13, fontweight="bold")
fig.tight_layout()
