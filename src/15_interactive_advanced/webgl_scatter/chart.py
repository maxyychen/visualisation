# %% setup
from vizlib.plotly_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(31)
groups = {"Large cap": (100_000, 0.012), "Mid cap": (60_000, 0.018), "Small cap": (40_000, 0.026)}
frames = []
for name, (n, vol) in groups.items():
    rel_volume = rng.lognormal(0, 0.45, n)                       # volume / 20-day average
    ret = rng.standard_t(4, n) * vol * np.sqrt(rel_volume) / np.sqrt(2)
    frames.append(pd.DataFrame({"group": name, "rel_volume": rel_volume.astype("float32"),
                                "ret_pct": (100 * ret).astype("float32")}))
df = pd.concat(frames, ignore_index=True)
print(f"{len(df):,} points")
df.groupby("group")["ret_pct"].describe().round(2)

# %% plot
fig = go.Figure()
# Widest group first so it sits underneath; colors stay tied to the group, not the draw order.
for i, (name, part) in reversed(list(enumerate(df.groupby("group", sort=False)))):
    fig.add_trace(go.Scattergl(
        x=part["rel_volume"].to_numpy(), y=part["ret_pct"].to_numpy(), mode="markers", name=name,
        marker=dict(size=3, color=PALETTE[i], opacity=0.35),
        hovertemplate=f"{name}<br>relative volume %{{x:.2f}}×<br>return %{{y:+.2f}}%<extra></extra>"))
fig.update_layout(
    title=f"Daily return vs. relative volume: {len(df):,} stock-days (WebGL)",
    xaxis=dict(title="Volume relative to 20-day average (log scale)", type="log"),
    yaxis=dict(title="Daily return (%)", range=[-15, 15]),
    legend=dict(itemsizing="constant", traceorder="reversed"), height=580,
)
