# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(4)
years = np.arange(2004, 2024)
t = np.linspace(0, 3 * np.pi, len(years))
unemployment = 6 + 2.2 * np.sin(t) + rng.normal(0, 0.3, len(years))
inflation = 2.5 + 1.8 * np.cos(t) + rng.normal(0, 0.3, len(years))
df = pd.DataFrame({"year": years, "unemployment": unemployment, "inflation": inflation})
df.head()

# %% plot
fig, ax = plt.subplots(figsize=(7.5, 5.5))
x, y = df["unemployment"].values, df["inflation"].values
for i in range(len(df) - 1):
    ax.annotate("", xy=(x[i + 1], y[i + 1]), xytext=(x[i], y[i]),
                arrowprops=dict(arrowstyle="-|>", color=PALETTE[0], lw=1.4,
                                alpha=0.35 + 0.65 * i / len(df), shrinkA=4, shrinkB=4))
ax.scatter(x, y, s=36, color=PALETTE[0], edgecolor="#fcfcfb", linewidth=1.5, zorder=3)
for i in [0, 5, 10, 15, len(df) - 1]:
    ax.annotate(str(df["year"].iloc[i]), (x[i], y[i]), xytext=(6, 6),
                textcoords="offset points", fontsize=9, color="#52514e")
ax.set_xlabel("Unemployment rate (%)")
ax.set_ylabel("Inflation rate (%)")
ax.set_title("Unemployment vs. inflation, 2004–2023")
fig.tight_layout()
