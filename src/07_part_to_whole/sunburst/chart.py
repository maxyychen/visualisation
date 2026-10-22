# %% setup
from vizlib.plotly_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rows = [
    ("Asia", "Japan", "Online", 42), ("Asia", "Japan", "Retail", 30),
    ("Asia", "Taiwan", "Online", 25), ("Asia", "Taiwan", "Retail", 18),
    ("Asia", "India", "Online", 20), ("Asia", "India", "Retail", 12),
    ("Europe", "Germany", "Online", 33), ("Europe", "Germany", "Retail", 27),
    ("Europe", "France", "Online", 21), ("Europe", "France", "Retail", 19),
    ("Europe", "UK", "Online", 26), ("Europe", "UK", "Retail", 14),
    ("Americas", "USA", "Online", 60), ("Americas", "USA", "Retail", 45),
    ("Americas", "Brazil", "Online", 14), ("Americas", "Brazil", "Retail", 10),
]
df = pd.DataFrame(rows, columns=["region", "country", "channel", "sales_m"])
df.head()

# %% plot
fig = px.sunburst(df, path=["region", "country", "channel"], values="sales_m",
                  color="region", color_discrete_sequence=PALETTE,
                  title="Sales by region, country and channel ($M)")
fig.update_traces(marker=dict(line=dict(color="#fcfcfb", width=2)),
                  insidetextorientation="radial")
fig.update_layout(width=700, height=650, margin=dict(t=60, l=10, r=10, b=10))
