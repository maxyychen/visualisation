# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
drivers = pd.DataFrame({
    "step": ["FY2024", "Price", "Volume", "Mix", "FX", "Acquisitions", "FY2025"],
    "value_m": [400, 45, 70, -25, -35, 60, np.nan],
})
drivers.loc[drivers.index[-1], "value_m"] = drivers["value_m"].iloc[:-1].sum()
drivers

# %% plot
vals = drivers["value_m"].to_numpy()
is_total = np.zeros(len(vals), bool)
is_total[[0, -1]] = True
running = np.r_[0, np.cumsum(vals[:-1])]
bottom = np.where(is_total, 0, np.where(vals >= 0, running, running + vals))
height = np.where(is_total, vals, np.abs(vals))
colors = np.where(is_total, "#7a7974", np.where(vals >= 0, PALETTE[0], PALETTE[1]))

fig, ax = plt.subplots(figsize=(9.5, 5.5))
x = np.arange(len(vals))
ax.bar(x, height, bottom=bottom, color=colors, width=0.62)
for i in range(len(vals) - 1):                    # connectors at the running total
    level = vals[0] if i == 0 else running[i] + vals[i]
    ax.plot([i + 0.31, i + 0.69], [level, level], color="#a9a8a2", linewidth=1)
for xi, v, b, h, tot in zip(x, vals, bottom, height, is_total):
    label = f"${v:,.0f}m" if tot else f"{v:+,.0f}"
    ax.text(xi, b + h + 6, label, ha="center", va="bottom", fontsize=10,
            fontweight="bold" if tot else "normal")
ax.set_xticks(x, drivers["step"])
ax.set_ylim(0, vals.max() * 1.15)
ax.set_ylabel("Revenue ($m)")
ax.grid(axis="x", visible=False)
ax.set_title("Revenue bridge FY2024 → FY2025: volume and M&A drove +29% (illustrative)")
fig.tight_layout()
