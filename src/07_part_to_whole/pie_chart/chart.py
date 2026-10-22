# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
raw = pd.Series({"Organic search": 41, "Direct": 24, "Social": 14, "Referral": 11,
                 "Email": 6, "Paid": 2.5, "Affiliates": 1.5})
# Keep at most 5 named slices; fold the tail into "Other"
top = raw.nlargest(4)
s = pd.concat([top, pd.Series({"Other": raw.drop(top.index).sum()})])
s

# %% plot
fig, ax = plt.subplots(figsize=(6.5, 6.5))
colors = PALETTE[:len(s) - 1] + [GRAY]
wedges, _ = ax.pie(s.values, colors=colors, startangle=90, counterclock=False,
                   wedgeprops=dict(edgecolor="#fcfcfb", linewidth=2))
for w, (name, v) in zip(wedges, s.items()):
    ang = np.deg2rad((w.theta1 + w.theta2) / 2)
    x, y = np.cos(ang), np.sin(ang)
    ax.annotate(f"{name}\n{v:.0f}%", xy=(0.98 * x, 0.98 * y), xytext=(1.25 * x, 1.2 * y),
                ha="center", va="center", fontsize=10,
                arrowprops=dict(arrowstyle="-", color="#b8b7b1", linewidth=0.8))
ax.set_title("Website traffic by source")
ax.axis("equal")
fig.tight_layout()

# %% alt:plotly
import plotly.express as px
fig = px.pie(names=s.index, values=s.values, color_discrete_sequence=PALETTE[:len(s) - 1] + ["#b8b7b1"],
             title="Website traffic by source")
fig.update_traces(sort=False, direction="clockwise", textinfo="label+percent",
                  marker=dict(line=dict(color="#fcfcfb", width=2)))
fig.update_layout(showlegend=False)
fig.show()
