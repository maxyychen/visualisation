# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(5)
months = pd.period_range("2023-01", periods=24, freq="M")
df = pd.DataFrame({"month": months.strftime("%b %y"),
                   "net_cash_k": (rng.normal(4, 12, 24)).round(1)})
df.head()

# %% plot
fig, ax = plt.subplots(figsize=(10, 4.5))
colors = np.where(df["net_cash_k"] >= 0, PALETTE[0], PALETTE[1])
ax.bar(df["month"], df["net_cash_k"], color=colors, width=0.75)
ax.axhline(0, color="#52514e", linewidth=1)
ax.set_ylabel("Net cash flow ($k)")
ax.set_title("Monthly net cash flow")
ax.tick_params(axis="x", rotation=60)
ax.grid(axis="x", visible=False)
fig.tight_layout()
