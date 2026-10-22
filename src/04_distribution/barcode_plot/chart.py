# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(41)
dates = ["Jan 2020", "Apr 2020", "Jan 2022"]
centers = [3.6, 13.0, 4.2]
spreads = [0.8, 3.5, 1.0]
df = pd.concat([pd.DataFrame({"date": d, "state": [f"S{i:02d}" for i in range(50)],
                              "rate": rng.normal(c, s, 50).clip(1.5)})
                for d, c, s in zip(dates, centers, spreads)], ignore_index=True)
focus = "S07"
df[df["state"] == focus]

# %% plot
fig, ax = plt.subplots(figsize=(9, 3.6))
for y, d in enumerate(dates):
    g = df[df["date"] == d]
    ax.vlines(g["rate"], y - 0.3, y + 0.3, color=GRAY, linewidth=1.5)
    f = g[g["state"] == focus]["rate"].iloc[0]
    ax.vlines(f, y - 0.38, y + 0.38, color=PALETTE[1], linewidth=3)
    if y == 0:
        ax.text(f, y + 0.45, focus, ha="center", fontsize=9, color="#0b0b0b", weight="bold")
ax.set_yticks(range(len(dates)), dates)
ax.invert_yaxis()
ax.set_xlabel("Unemployment rate (%)")
ax.set_title(f"State unemployment rates ({focus} highlighted)")
ax.grid(axis="y", visible=False)
fig.tight_layout()
