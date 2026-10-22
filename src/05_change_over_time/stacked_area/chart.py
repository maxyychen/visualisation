# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
years = np.arange(2005, 2025)
t = years - 2005
df = pd.DataFrame({
    "Coal": 220 - 7.5 * t,
    "Gas": 110 + 3.0 * t,
    "Nuclear": np.full(len(t), 80.0) - 0.5 * t,
    "Wind": 2 + 0.25 * t ** 2,
    "Solar": 0.5 + 0.18 * t ** 2,
}, index=years).clip(lower=0)
df.tail()

# %% plot
fig, ax = plt.subplots(figsize=(9, 5))
ax.stackplot(df.index, df.T.values, labels=df.columns, colors=PALETTE[:5],
             edgecolor="#fcfcfb", linewidth=1)
ax.set_xlim(df.index[0], df.index[-1])
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.set_ylabel("Generation (TWh)")
ax.set_title("Electricity generation by source")
ax.legend(loc="upper left", ncol=5, bbox_to_anchor=(0, -0.08))
fig.tight_layout()

# %% alt:altair
import altair as alt
long = df.rename_axis("year").reset_index().melt(id_vars="year", var_name="source", value_name="twh")
chart = alt.Chart(long).mark_area().encode(
    x=alt.X("year:O", title=None, axis=alt.Axis(labelAngle=0, values=list(range(2006, 2025, 2)))),
    y=alt.Y("twh:Q", stack="zero", title="Generation (TWh)"),
    color=alt.Color("source:N", sort=list(df.columns), title=None),
    order=alt.Order("order:Q"),
    tooltip=["year", "source", alt.Tooltip("twh:Q", format=".0f")],
).transform_calculate(order=f"indexof({list(df.columns)}, datum.source)"
).properties(title="Electricity generation by source", width=540, height=300)
chart
