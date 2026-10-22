# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
stages = pd.Series({"Leads": 2400, "Qualified": 1150, "Demo held": 640,
                    "Proposal sent": 410, "Closed-won": 230})
stages.to_frame("deals").assign(step_conversion=(stages / stages.shift()).round(2))

# %% plot
fig, ax = plt.subplots(figsize=(9, 5))
y = np.arange(len(stages))[::-1]
ax.barh(y, stages.values, left=-stages.values / 2, color=PALETTE[0], height=0.8)
for yi, (name, v), prev in zip(y, stages.items(), [None] + list(stages.values[:-1])):
    ax.text(0, yi, f"{v:,}", ha="center", va="center", color="white", fontweight="bold")
    ax.text(-stages.max() / 2 - 60, yi, name, ha="right", va="center", fontsize=10)
    if prev:
        ax.text(stages.max() / 2 + 60, yi, f"{v / prev:.0%} of previous", ha="left",
                va="center", fontsize=9, color="#52514e")
ax.set_xlim(-stages.max() / 2 - 500, stages.max() / 2 + 500)
ax.axis("off")
ax.set_title(f"Sales pipeline: {stages.iloc[-1] / stages.iloc[0]:.0%} of leads become customers")
fig.tight_layout()

# %% alt:plotly
import plotly.graph_objects as go
fig = go.Figure(go.Funnel(y=stages.index, x=stages.values, textinfo="value+percent previous",
                          marker=dict(color=PALETTE[0]), connector=dict(fillcolor="#e6e5e1")))
fig.update_layout(title=f"Sales pipeline: {stages.iloc[-1] / stages.iloc[0]:.0%} of leads become customers")
fig.show()
