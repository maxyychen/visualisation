# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(8)
n = 40
gdp = np.exp(rng.uniform(np.log(800), np.log(80000), n))
life = 48 + 7.5 * np.log10(gdp) + rng.normal(0, 2.5, n)
pop = np.exp(rng.normal(3, 1.3, n))          # millions
region = rng.choice(["Asia", "Africa", "Europe"], n, p=[0.4, 0.35, 0.25])
df = pd.DataFrame({"country": [f"C{i:02d}" for i in range(n)], "gdp_pc": gdp,
                   "life_exp": life, "pop_m": pop, "region": region})
df = df.sort_values("pop_m", ascending=False)   # big bubbles drawn first
df.head()

# %% plot
fig, ax = plt.subplots(figsize=(8.5, 5.5))
size = lambda p: p * 4                         # area proportional to population
for color, reg in zip(PALETTE, ["Asia", "Africa", "Europe"]):
    g = df[df["region"] == reg]
    ax.scatter(g["gdp_pc"], g["life_exp"], s=size(g["pop_m"]), color=color,
               alpha=0.65, edgecolor="#fcfcfb", linewidth=1, label=reg)
ax.set_xscale("log")
ax.set_xlabel("GDP per capita (USD, log scale)")
ax.set_ylabel("Life expectancy (years)")
ax.set_title("Wealth and health of nations")
leg1 = ax.legend(loc="upper left", markerscale=0.4)
ax.add_artist(leg1)
for p in [10, 50, 200]:
    ax.scatter([], [], s=size(p), color="#d0cfca", label=f"{p}M")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[3:], labels[3:], loc="lower right", title="Population",
          labelspacing=1.6, borderpad=1.2)
fig.tight_layout()

# %% real-data
import plotly.express as px
gm = px.data.gapminder().query("year == 2007 and continent in ['Asia', 'Africa', 'Europe']")
df = pd.DataFrame({"country": gm["country"], "gdp_pc": gm["gdpPercap"], "life_exp": gm["lifeExp"],
                   "pop_m": gm["pop"] / 1e6, "region": gm["continent"]})
df = df.sort_values("pop_m", ascending=False)
df.head()

# %% alt:plotly
import plotly.express as px
fig = px.scatter(df, x="gdp_pc", y="life_exp", size="pop_m", color="region", hover_name="country",
                 log_x=True, size_max=45, color_discrete_sequence=PALETTE,
                 category_orders={"region": ["Asia", "Africa", "Europe"]},
                 labels={"gdp_pc": "GDP per capita (USD, log scale)", "life_exp": "Life expectancy (years)",
                         "pop_m": "Population (M)", "region": "Region"},
                 title="Wealth and health of nations")
fig.update_traces(marker=dict(opacity=0.7, line=dict(color="#fcfcfb", width=1)))
fig.show()
