# %% setup
from vizlib.plotly_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = pd.DataFrame([
    ("Tokyo", 35.7, 139.7, 37.2), ("Delhi", 28.6, 77.2, 32.9), ("Shanghai", 31.2, 121.5, 29.2),
    ("Dhaka", 23.8, 90.4, 23.2), ("São Paulo", -23.6, -46.6, 22.6), ("Cairo", 30.0, 31.2, 22.2),
    ("Mexico City", 19.4, -99.1, 22.3), ("Beijing", 39.9, 116.4, 21.8), ("Mumbai", 19.1, 72.9, 21.3),
    ("Osaka", 34.7, 135.5, 19.0), ("New York", 40.7, -74.0, 18.9), ("Karachi", 24.9, 67.0, 17.2),
    ("Kinshasa", -4.3, 15.3, 17.0), ("Lagos", 6.5, 3.4, 15.9), ("Istanbul", 41.0, 29.0, 15.8),
    ("Buenos Aires", -34.6, -58.4, 15.5), ("Kolkata", 22.6, 88.4, 15.3), ("Manila", 14.6, 121.0, 14.7),
    ("Moscow", 55.8, 37.6, 12.7), ("Los Angeles", 34.1, -118.2, 12.5), ("Paris", 48.9, 2.35, 11.2),
    ("Jakarta", -6.2, 106.8, 11.2), ("London", 51.5, -0.13, 9.6), ("Lima", -12.0, -77.0, 11.0),
], columns=["city", "lat", "lon", "pop_m"]).sort_values("pop_m", ascending=False)
df.head()

# %% plot
fig = px.scatter_geo(df, lat="lat", lon="lon", size="pop_m", hover_name="city",
                     size_max=38, projection="natural earth",
                     title="Largest urban agglomerations (population, millions)")
fig.update_traces(marker=dict(color=PALETTE[0], opacity=0.7,
                              line=dict(color="#fcfcfb", width=1)))
fig.update_geos(showframe=False, landcolor="#eeeeea", coastlinecolor="#c9c8c3",
                showcountries=True, countrycolor="#dcdbd6", bgcolor="#fcfcfb")
fig.update_layout(margin=dict(l=10, r=10, t=50, b=10), height=480)
