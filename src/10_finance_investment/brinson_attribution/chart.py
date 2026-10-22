# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
sectors = ["Technology", "Financials", "Health care", "Industrials", "Energy", "Consumer"]
df = pd.DataFrame({
    "w_p": [0.32, 0.12, 0.14, 0.14, 0.10, 0.18],    # portfolio weights
    "w_b": [0.25, 0.16, 0.13, 0.15, 0.08, 0.23],    # benchmark weights
    "r_p": [0.245, 0.098, 0.071, 0.132, 0.012, 0.085],   # portfolio sector returns
    "r_b": [0.228, 0.104, 0.052, 0.118, 0.061, 0.079],   # benchmark sector returns
}, index=sectors)
df

# %% plot
R_b, R_p = (df.w_b * df.r_b).sum(), (df.w_p * df.r_p).sum()
df["allocation"] = (df.w_p - df.w_b) * (df.r_b - R_b)
df["selection"] = df.w_b * (df.r_p - df.r_b)
df["interaction"] = (df.w_p - df.w_b) * (df.r_p - df.r_b)
effects = df[["allocation", "selection", "interaction"]].sum()
assert np.isclose(effects.sum(), R_p - R_b)

fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), gridspec_kw={"width_ratios": [1, 1.25]})
steps = [("Benchmark", R_b, "total"), ("Allocation", effects["allocation"], "fx"),
         ("Selection", effects["selection"], "fx"), ("Interaction", effects["interaction"], "fx"),
         ("Portfolio", R_p, "total")]
level = 0
for i, (lab, v, kind) in enumerate(steps):
    if kind == "total":
        ax.bar(i, v, color="#52514e", width=0.6)
        ax.text(i, v + 0.001, f"{v:.2%}", ha="center", va="bottom", fontsize=9, weight="bold")
        level = v
    else:
        ax.bar(i, v, bottom=level, color=PALETTE[0] if v >= 0 else PALETTE[1], width=0.6)
        ax.text(i, max(level, level + v) + 0.001, f"{v * 1e4:+.0f} bp", ha="center", va="bottom", fontsize=9)
        level += v
ax.set_xticks(range(len(steps)), [s[0] for s in steps])
lo = min(R_b, R_p) * 0.9
ax.set_ylim(lo, max(R_b, R_p) * 1.04)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.1%}"))
ax.set_title(f"Excess return {(R_p - R_b) * 1e4:+.0f} bp, decomposed")
ax.text(0.0, -0.13, "Axis does not start at zero: bars here show changes, not totals.",
        transform=ax.transAxes, fontsize=8, color="#7a7974")
ax.grid(axis="x", visible=False)

by = df[["allocation", "selection"]] * 1e4
y = np.arange(len(by))
ax2.barh(y + 0.19, by["allocation"], height=0.36, color=PALETTE[0], label="Allocation")
ax2.barh(y - 0.19, by["selection"], height=0.36, color=PALETTE[2], label="Selection")
ax2.axvline(0, color="#52514e", linewidth=1)
ax2.set_yticks(y, by.index)
ax2.invert_yaxis()
ax2.set_xlabel("Effect (basis points)")
ax2.set_title("By sector")
ax2.legend(loc="lower right")
ax2.grid(axis="y", visible=False)
fig.tight_layout()
