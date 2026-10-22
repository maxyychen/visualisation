# %% setup
from vizlib.plotly_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(4)
n_frames = 40
draws = pd.DataFrame({
    "A": rng.normal(10, 1.6, n_frames),
    "B": rng.normal(11.5, 1.6, n_frames),
})
p_b_slower = (draws["B"] > draws["A"]).mean()
print(f"B slower than A in {p_b_slower:.0%} of draws")
draws.head().round(1)

# %% plot
labels = ["Treatment A", "Treatment B"]
colors = [PALETTE[0], PALETTE[1]]

def frame_data(i):
    vals = draws.iloc[i][["A", "B"]].values
    return [go.Bar(x=labels, y=vals, marker_color=colors, width=0.5,
                   text=[f"{v:.1f} d" for v in vals], textposition="outside",
                   hovertemplate="%{x}: %{y:.1f} days<extra></extra>")]

def frame_note(i):
    a, b = draws.iloc[i][["A", "B"]]
    who = "A recovers faster" if a < b else "B recovers faster"
    return [dict(text=f"Outcome {i + 1} of {n_frames}: {who}", x=0.5, y=1.02, xref="paper",
                 yref="paper", showarrow=False, font=dict(size=14, color="#52514e"))]

frames = [go.Frame(data=frame_data(i), name=str(i), layout=dict(annotations=frame_note(i)))
          for i in range(n_frames)]
fig = go.Figure(data=frame_data(0), frames=frames)
fig.update_layout(
    title=f"Days to recovery: one plausible outcome per frame (B slower in {p_b_slower:.0%} of draws)",
    yaxis=dict(range=[0, 17], title="Days to recovery"),
    annotations=frame_note(0), showlegend=False, height=520,
    updatemenus=[dict(type="buttons", x=0, y=-0.12, xanchor="left", direction="left", buttons=[
        dict(label="▶ Play", method="animate",
             args=[None, dict(frame=dict(duration=450, redraw=True), transition=dict(duration=0),
                              fromcurrent=True)]),
        dict(label="❚❚ Pause", method="animate",
             args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]),
    ])],
    sliders=[dict(x=0.18, y=-0.08, len=0.8, currentvalue=dict(prefix="Outcome "),
                  steps=[dict(label=str(i + 1), method="animate",
                              args=[[str(i)], dict(frame=dict(duration=0, redraw=True), mode="immediate")])
                         for i in range(n_frames)])],
)
