# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = pd.DataFrame({"vendor": ["Vendor A", "Vendor B", "Vendor C", "Vendor D", "Vendor E"],
                   "share": [21.0, 19.0, 23.0, 17.5, 19.5]})
df

# %% plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), gridspec_kw={"width_ratios": [1, 1.15]})

# Misleading: near-equal slices, legend lookup, no order.
ax1.pie(df["share"], labels=None, colors=plt.get_cmap("tab10").colors[:5], startangle=90,
        wedgeprops=dict(edgecolor="white", linewidth=1))
ax1.legend(df["vendor"], loc="center left", bbox_to_anchor=(0.95, 0.5), fontsize=9)
ax1.set_title("✗ Misleading: pie of near-equal shares", fontsize=11.5)

# Better: sorted bar, one color, direct labels.
d = df.sort_values("share")
ax2.barh(d["vendor"], d["share"], color=PALETTE[0], height=0.65)
for y, v in enumerate(d["share"]):
    ax2.text(v + 0.3, y, f"{v:.1f}%", va="center", fontsize=9.5, color="#52514e")
ax2.set_xlim(0, 27)
ax2.set_xlabel("Market share (%)")
ax2.grid(axis="y", visible=False)
ax2.set_title("✓ Better: sorted bar — order and gaps are obvious", fontsize=11.5)
fig.tight_layout()
