# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
companies = ["Novacorp", "Helion", "Quanta", "Meridian", "Orbis", "Vantage", "Kestrel",
             "Lumen", "Tessel", "Zephyr"]
value_bn = [2900, 1700, 1100, 640, 420, 260, 150, 90, 55, 30]
df = pd.DataFrame({"company": companies, "value_bn": value_bn}).sort_values("value_bn", ascending=False)
df

# %% plot
fig, ax = plt.subplots(figsize=(10, 3.4))
r = np.sqrt(df["value_bn"].values / np.pi)         # area proportional to value
r = r / r.max() * 0.45
gaps = np.maximum(r[:-1] + r[1:] + 0.06, 0.6)      # keep small circles' labels apart
x = np.cumsum(np.r_[r[0], gaps])
for xi, ri, (_, row) in zip(x, r, df.iterrows()):
    ax.add_patch(plt.Circle((xi, 0), ri, color=PALETTE[0], alpha=0.85))
    label = f"{row['value_bn']:,.0f}"
    if ri > 0.15:                                  # value inside big circles, above small ones
        ax.text(xi, 0, label, ha="center", va="center", color="white", fontsize=10, weight="bold")
    else:
        ax.text(xi, ri + 0.04, label, ha="center", va="bottom", color="#0b0b0b", fontsize=9.5, weight="bold")
    ax.text(xi, -0.55, row["company"], ha="center", va="top", fontsize=9, color="#52514e")
ax.set_xlim(-0.05, x[-1] + max(r[-1], 0.3) + 0.05)
ax.set_ylim(-0.8, 0.5)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Largest companies in the index (market value, $bn)")
fig.tight_layout()
