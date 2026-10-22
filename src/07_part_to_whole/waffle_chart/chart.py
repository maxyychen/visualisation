# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
s = pd.Series({"Cash & deposits": 40, "Stocks & funds": 45, "Bonds & other": 15})
assert s.sum() == 100
s

# %% plot
fig, ax = plt.subplots(figsize=(7, 5.6))
cells = np.repeat(np.arange(len(s)), s.values)
for k, cat in enumerate(cells):
    col, row = k // 10, k % 10          # fill column by column, bottom to top
    ax.add_patch(plt.Rectangle((col, row), 0.88, 0.88, color=PALETTE[cat]))
ax.set_xlim(-0.2, 10)
ax.set_ylim(-0.2, 10)
ax.set_aspect("equal")
ax.axis("off")
handles = [plt.Rectangle((0, 0), 1, 1, color=PALETTE[i]) for i in range(len(s))]
ax.legend(handles, [f"{k}: ${v}" for k, v in s.items()], loc="center left",
          bbox_to_anchor=(1.0, 0.5), fontsize=10)
ax.set_title("Household financial assets, per $100")
fig.tight_layout()
