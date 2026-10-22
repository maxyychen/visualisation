# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = pd.DataFrame({
    "date": pd.to_datetime(["2019-01-01", "2019-08-01", "2019-10-30", "2020-03-03", "2020-03-15",
                            "2022-03-16", "2022-05-04", "2022-06-15", "2022-07-27", "2022-09-21",
                            "2022-11-02", "2022-12-14", "2023-02-01", "2023-03-22", "2023-05-03",
                            "2023-07-26", "2024-09-18", "2024-11-07", "2024-12-18", "2025-06-30"]),
    "rate": [2.50, 2.25, 1.75, 1.25, 0.25, 0.50, 1.00, 1.75, 2.50, 3.25,
             4.00, 4.50, 4.75, 5.00, 5.25, 5.50, 5.00, 4.75, 4.50, 4.50],
})
df.head()

# %% plot
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.step(df["date"], df["rate"], where="post", color=PALETTE[0])
ax.fill_between(df["date"], df["rate"], step="post", color=PALETTE[0], alpha=0.12)
ax.set_ylim(0, 6)
ax.set_ylabel("Policy rate (%)")
ax.set_title("Policy rate decisions")
ax.annotate("Emergency cuts", xy=(pd.Timestamp("2020-03-15"), 0.25),
            xytext=(pd.Timestamp("2020-06-01"), 2.0), color="#52514e",
            arrowprops=dict(arrowstyle="->", color="#52514e"))
fig.tight_layout()
