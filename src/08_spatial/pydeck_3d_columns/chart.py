# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(12)
lat0, lon0 = 40.0, -75.0                     # a generic mid-latitude city; no basemap is used
km_lat, km_lon = 1 / 111.0, 1 / (111.0 * np.cos(np.radians(lat0)))
hot = [(0.0, 0.0, 1.2, 0.45), (3.5, 2.0, 0.5, 0.15), (-4.0, -2.5, 0.6, 0.12)]  # (x km, y km, spread, share)
xs, ys = [], []
n = 15000
for x, y, s, share in hot:
    k = int(n * share)
    xs.append(rng.normal(x, s, k))
    ys.append(rng.normal(y, s, k))
k = n - sum(int(n * h[3]) for h in hot)
xs.append(rng.uniform(-8, 8, k))
ys.append(rng.uniform(-6, 6, k))
x_km, y_km = np.concatenate(xs), np.concatenate(ys)
df = pd.DataFrame({"lon": lon0 + x_km * km_lon, "lat": lat0 + y_km * km_lat, "x_km": x_km, "y_km": y_km})
df.head()

# %% plot
# Static preview: the same aggregation idea on a 0.5 km square grid, drawn as 3-D bars
counts, xe, ye = np.histogram2d(df["x_km"], df["y_km"], bins=[32, 24], range=[[-8, 8], [-6, 6]])
X, Y = np.meshgrid(xe[:-1], ye[:-1], indexing="ij")
mask = counts.ravel() > 0
h = counts.ravel()[mask]
colors = plt.get_cmap(SEQ_CMAP)(0.25 + 0.75 * np.log1p(h) / np.log1p(h.max()))
fig = plt.figure(figsize=(9, 6.5))
ax = fig.add_subplot(projection="3d")
ax.bar3d(X.ravel()[mask], Y.ravel()[mask], 0, 0.45, 0.45, h, color=colors, shade=True,
         edgecolor="none")
ax.view_init(elev=38, azim=-60)
ax.set_xlabel("km east")
ax.set_ylabel("km north")
ax.set_zlabel("Pick-ups per cell")
ax.set_title("Ride pick-ups per 0.5 km cell (simulated): static preview of the 3-D map")
ax.xaxis.pane.set_alpha(0)
ax.yaxis.pane.set_alpha(0)
ax.zaxis.pane.set_alpha(0)

# %% html
import pydeck as pdk

blues = [[205, 226, 251], [158, 197, 244], [109, 167, 236], [57, 135, 229], [37, 106, 191], [16, 66, 129]]
layer = pdk.Layer(
    "HexagonLayer", data=df[["lon", "lat"]], get_position=["lon", "lat"],
    radius=300, elevation_scale=6, elevation_range=[0, 1000], extruded=True,
    coverage=0.9, pickable=True, color_range=blues,
)
view = pdk.ViewState(latitude=lat0, longitude=lon0, zoom=11.3, pitch=48, bearing=-25)
deck = pdk.Deck(layers=[layer], initial_view_state=view, map_style=None,
                tooltip={"text": "{elevationValue} pick-ups"})
html = deck.to_html(as_string=True)
