# %% setup
from vizlib.plotly_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = px.data.gapminder().query("year == 2007")
df[["country", "continent", "iso_alpha", "lifeExp"]].head()

# %% plot
fig = px.choropleth(df, locations="iso_alpha", color="lifeExp", hover_name="country",
                    color_continuous_scale="Blues", range_color=(40, 85),
                    labels={"lifeExp": "Life exp. (yrs)"},
                    title="Life expectancy at birth, 2007")
fig.update_geos(showframe=False, showcoastlines=False, projection_type="natural earth",
                bgcolor="#fcfcfb", landcolor="#eeeeea")
fig.update_layout(margin=dict(l=10, r=10, t=50, b=10), height=480)
