# %% setup
from vizlib.plotly_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = px.data.gapminder()
continents = ["Asia", "Europe", "Africa", "Americas", "Oceania"]
df.query("year == 2007").sort_values("pop", ascending=False).head()

# %% plot
fig = px.scatter(
    df, x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="country",
    animation_frame="year", animation_group="country", log_x=True, size_max=55,
    range_x=[200, 60000], range_y=[25, 88],
    category_orders={"continent": continents}, color_discrete_sequence=PALETTE,
    labels={"gdpPercap": "GDP per capita (US$, log scale)", "lifeExp": "Life expectancy (years)",
            "continent": "Continent"},
    title="Wealth and health of nations, 1952–2007",
)
fig.update_traces(marker=dict(line=dict(width=0.6, color="#fcfcfb")))
fig.update_layout(height=600)
for frame in fig.frames:  # put the year in the title so every frame (and GIF still) is dated
    frame.layout = go.Layout(title_text=f"Wealth and health of nations, {frame.name}")
fig.update_layout(title_text="Wealth and health of nations, 1952")
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 400
