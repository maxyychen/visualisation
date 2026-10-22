# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib_venn import venn3

# %% data
# region sizes in the order: (100, 010, 110, 001, 101, 011, 111)
subsets = {"Checking only": 210, "Card only": 90, "Checking∩Card": 70, "Brokerage only": 160,
           "Checking∩Brokerage": 95, "Card∩Brokerage": 55, "All three": 40}
subsets

# %% plot
fig, ax = plt.subplots(figsize=(7, 6))
v = venn3(subsets=tuple(subsets.values()),
          set_labels=("Checking", "Credit card", "Brokerage"),
          set_colors=PALETTE[:3], alpha=0.55, ax=ax)
for patch in v.patches:
    if patch is not None:
        patch.set_edgecolor("#fcfcfb")
        patch.set_linewidth(2)
for t in v.subset_labels:
    if t is not None:
        t.set_fontsize(10)
n_none = 1000 - sum(subsets.values())        # customers holding none of the three
ax.set_title(f"Which bank products do customers hold? (n = 1,000; {n_none} hold none)")
fig.tight_layout()
