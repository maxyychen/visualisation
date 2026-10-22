# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = pd.DataFrame({"group": ["Teens 13–17", "Adults 18–34", "Adults 35–54", "Adults 55+"],
                   "hours": [7.5, 6.5, 5.0, 3.5]})
df

# %% plot
from matplotlib.patches import FancyBboxPatch
def phone(ax, x, y, frac=1.0, color=PALETTE[0]):
    w, h = 0.55, 0.85
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor="#e6e5e1", edgecolor="none"))
    ax.add_patch(FancyBboxPatch((x, y), w * frac, h,
                                boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor=color, edgecolor="none"))
    ax.add_patch(plt.Circle((x + w / 2, y + 0.1), 0.04, color="#fcfcfb"))
fig, ax = plt.subplots(figsize=(9, 4))
for row, (_, r) in enumerate(df.iloc[::-1].iterrows()):
    full, part = int(r["hours"]), r["hours"] % 1
    for k in range(full):
        phone(ax, k * 0.75, row * 1.2)
    if part:
        phone(ax, full * 0.75, row * 1.2, frac=part)
    ax.text(-0.3, row * 1.2 + 0.42, r["group"], ha="right", va="center", fontsize=10)
    ax.text(8 * 0.75 + 0.2, row * 1.2 + 0.42, f"{r['hours']:.1f} h", va="center",
            fontweight="bold")
ax.set_xlim(-3.2, 7.3)
ax.set_ylim(-0.3, len(df) * 1.2)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Daily screen time by age group (1 phone = 1 hour)")
fig.tight_layout()
