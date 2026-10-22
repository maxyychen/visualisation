# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.animation import FuncAnimation

# %% data
rng = np.random.default_rng(21)
years = np.arange(2005, 2025)
companies = {  # name: (2005 market cap $bn, mean annual growth)
    "Meridian Oil": (450, -0.01), "Globex Industrial": (380, 0.03), "Kestrel Bank": (300, 0.04),
    "Delta Retail": (260, 0.05), "Nova Telecom": (240, 0.02), "Evergreen Pharma": (220, 0.06),
    "Apex Systems": (200, 0.09), "Blue Harbor Insurance": (180, 0.05), "Cobalt Energy": (160, 0.03),
    "Juniper Motors": (120, 0.08), "Lumen Media": (110, 0.04), "Fintrex Payments": (60, 0.15),
    "Northwind Logistics": (90, 0.06), "Helix Semis": (40, 0.22), "Ionix Cloud": (15, 0.30),
}
start = np.array([v[0] for v in companies.values()])
growth = np.array([v[1] for v in companies.values()])
shocks = rng.normal(0, 0.12, (len(years), len(companies)))
shocks[years == 2008] -= 0.40           # financial crisis
shocks[years == 2020] -= 0.10           # pandemic dip
log_cap = np.log(start) + np.cumsum(np.vstack([np.zeros(len(companies)), (growth + shocks)[1:]]), axis=0)
df = pd.DataFrame(np.exp(log_cap), index=years, columns=list(companies)).round(1)

# Interpolate two in-between frames per year so bars glide.
steps = 2
df.index = df.index.astype(float)
frames = df.reindex(np.linspace(years[0], years[-1], (len(years) - 1) * steps + 1)).interpolate("index")
df.tail(3).T.sort_values(2024.0, ascending=False).head(10)

# %% plot
# Fixed color per entity: the 8 largest at the end get the categorical hues, everyone else gray.
leaders = df.iloc[-1].sort_values(ascending=False).index[:8]
colors = {name: GRAY for name in df.columns} | {name: PALETTE[i] for i, name in enumerate(leaders)}

fig, ax = plt.subplots(figsize=(8.5, 5.2))


def draw(i):
    ax.clear()
    row = frames.iloc[i].sort_values().tail(10)
    ax.barh(range(10), row.values, color=[colors[n] for n in row.index], height=0.78)
    for y, (name, value) in enumerate(row.items()):
        ax.text(value, y, f"  {name}  ${value:,.0f}bn", va="center", fontsize=9, color="#0b0b0b")
    ax.set_xlim(0, row.max() * 1.45)
    ax.set_yticks([])
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Market capitalisation (US$ bn) · axis rescales each frame")
    ax.set_title("Ten largest companies by market cap (simulated)")
    ax.text(0.97, 0.06, f"{int(frames.index[i])}", transform=ax.transAxes, ha="right",
            fontsize=40, fontweight="bold", color="#d0cfca")


anim = FuncAnimation(fig, draw, frames=len(frames), interval=170)
draw(len(frames) - 1)  # the static preview shows the final year
fig.tight_layout()
