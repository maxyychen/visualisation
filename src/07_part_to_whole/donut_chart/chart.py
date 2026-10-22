# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
s = pd.Series({"Current": 1050, "30–89 days late": 112, "90+ days late": 48, "Defaulted": 30})
s

# %% plot
fig, ax = plt.subplots(figsize=(6.5, 6))
# ordered severity: one neutral hue for 'Current', then light -> dark orange for worsening arrears
colors = [PALETTE[0], "#f5b38f", PALETTE[1], "#a8401a"]
wedges, _ = ax.pie(s.values, colors=colors, startangle=90, counterclock=False,
                   wedgeprops=dict(width=0.32, edgecolor="#fcfcfb", linewidth=2))
ax.text(0, 0.08, f"{s['Current'] / s.sum():.0%}", ha="center", va="center",
        fontsize=30, fontweight="bold")
ax.text(0, -0.17, "current", ha="center", va="center", fontsize=11, color="#52514e")
ax.legend(wedges, [f"{k}  ({v:,})" for k, v in s.items()], loc="center left",
          bbox_to_anchor=(0.95, 0.5))
ax.set_title(f"Loan book by repayment status, n = {s.sum():,} loans")
ax.axis("equal")
fig.tight_layout()
