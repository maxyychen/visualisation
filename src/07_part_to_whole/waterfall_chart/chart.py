# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
steps = pd.Series({"Revenue": 480, "Cost of goods": -190, "Salaries": -120,
                   "Marketing": -45, "R&D": -38, "Other income": 12, "Tax": -24})
steps

# %% plot
cum = steps.cumsum()
starts = cum - steps
labels = list(steps.index) + ["Net profit"]
fig, ax = plt.subplots(figsize=(10, 5))
for i, (name, v) in enumerate(steps.items()):
    if i == 0:
        color, bottom, h = "#52514e", 0, v
    else:
        color = PALETTE[0] if v >= 0 else PALETTE[1]
        bottom, h = min(starts.iloc[i], cum.iloc[i]), abs(v)
    ax.bar(i, h, bottom=bottom, color=color, width=0.65)
    ax.text(i, bottom + h + 6, f"{v:+,}" if i else f"{v:,}", ha="center", fontsize=9,
            color="#52514e")
    ax.plot([i + 0.33, i + 0.67], [cum.iloc[i]] * 2, color="#b8b7b1", linewidth=1)
net = cum.iloc[-1]
ax.bar(len(steps), net, color="#52514e", width=0.65)
ax.text(len(steps), net + 6, f"{net:,}", ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(range(len(labels)), labels, rotation=20)
ax.set_ylabel("$M")
ax.set_title("From revenue to net profit, FY2025")
ax.grid(axis="x", visible=False)
fig.tight_layout()
