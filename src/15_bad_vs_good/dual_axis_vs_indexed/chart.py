# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(21)
months = pd.date_range("2022-01", periods=36, freq="MS")
users_k = 10 * np.exp(np.linspace(0, np.log(3.0), 36)) * (1 + rng.normal(0, 0.02, 36))
revenue_m = 2.0 * np.exp(np.linspace(0, np.log(1.7), 36)) * (1 + rng.normal(0, 0.02, 36))
df = pd.DataFrame({"month": months, "users_k": users_k, "revenue_m": revenue_m})
df.head()

# %% plot
fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(12, 4.8))

# Misleading: two independent y-scales, chosen so the lines cross.
ax1.plot(df["month"], df["users_k"], color=PALETTE[0], label="Users (k)")
ax1.set_ylabel("Users (thousands)", color=PALETTE[0])
ax1.set_ylim(0, 60)
ax2 = ax1.twinx()
ax2.plot(df["month"], df["revenue_m"], color=PALETTE[1], label="Revenue ($M)")
ax2.set_ylabel("Revenue ($M)", color=PALETTE[1])
ax2.set_ylim(1.92, 3.57)
ax2.spines["right"].set_visible(True)
ax2.grid(False)
ax1.set_title("✗ Misleading: dual axis — the lines 'cross'", fontsize=11.5)
ax1.tick_params(axis="x", rotation=30)

# Better: one honest axis, both series indexed to 100 at the start.
idx = df[["users_k", "revenue_m"]] / df[["users_k", "revenue_m"]].iloc[0] * 100
for col, color, name in [("users_k", PALETTE[0], "Users"), ("revenue_m", PALETTE[1], "Revenue")]:
    ax3.plot(df["month"], idx[col], color=color)
    ax3.text(df["month"].iloc[-1] + pd.Timedelta(days=20), idx[col].iloc[-1],
             f"{name} {idx[col].iloc[-1]:.0f}", color="#0b0b0b", va="center", fontsize=9.5)
ax3.axhline(100, color="#52514e", linewidth=1)
ax3.set_ylabel("Index (Jan 2022 = 100)")
ax3.set_xlim(df["month"].iloc[0], df["month"].iloc[-1] + pd.Timedelta(days=200))
ax3.set_title("✓ Better: one axis, indexed to 100", fontsize=11.5)
ax3.tick_params(axis="x", rotation=30)
fig.tight_layout()
