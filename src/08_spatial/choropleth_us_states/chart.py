# %% setup
from vizlib.plotly_style import *  # noqa: F401,F403  (inlined on build)

# %% data
STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN",
          "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",
          "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT",
          "VT", "VA", "WA", "WV", "WI", "WY"]

rng = np.random.default_rng(8)
south = {"TX", "OK", "GA", "FL", "MS", "AL", "SC", "NC", "TN", "AR", "LA", "NM", "AZ", "NV", "WY"}
rate = [rng.normal(11.5 if s in south else 6.5, 1.6) for s in STATES]
df = pd.DataFrame({"state": STATES, "uninsured_pct": np.clip(rate, 2.5, 18).round(1)})
df.head()

# %% plot
fig = px.choropleth(df, locations="state", locationmode="USA-states", scope="usa",
                    color="uninsured_pct", color_continuous_scale="Blues",
                    labels={"uninsured_pct": "Uninsured (%)"},
                    title="Uninsured rate by state (illustrative data)")
fig.update_traces(marker_line_color="#fcfcfb", marker_line_width=1)
fig.update_layout(margin=dict(l=10, r=10, t=50, b=10), height=460, geo_bgcolor="#fcfcfb")
