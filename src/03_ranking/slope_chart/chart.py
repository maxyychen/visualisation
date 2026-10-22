# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
brands = ["Atlas", "Borealis", "Cirrus", "Delta", "Echo", "Flux", "Gamma", "Helix"]
y2019 = [21.0, 18.5, 14.0, 11.0, 9.5, 8.0, 6.0, 4.5]
y2024 = [19.5, 12.0, 17.5, 6.5, 13.5, 8.5, 9.5, 3.5]
df = pd.DataFrame({"brand": brands, "2019": y2019, "2024": y2024})
start, end = "2019", "2024"
title = "Smartphone market share (%), 2019 → 2024"
df["change"] = df[end] - df[start]
df

# %% plot
from matplotlib import patheffects
fig, ax = plt.subplots(figsize=(6.5, 6.5))
for _, r in df.iterrows():
    color = PALETTE[0] if r["change"] > 0 else PALETTE[1] if r["change"] < -2 else GRAY
    ax.plot([0, 1], [r[start], r[end]], color=color, marker="o", markersize=7,
            markeredgecolor="#fcfcfb", markeredgewidth=1.5)
    ax.text(-0.04, r[start], f"{r['brand']} {r[start]:.1f}", ha="right", va="center", fontsize=9)
    ax.text(1.04, r[end], f"{r[end]:.1f} {r['brand']}", ha="left", va="center", fontsize=9)
ax.set_xlim(-0.55, 1.55)
ax.set_xticks([0, 1], [start, end], fontsize=11, weight="bold")
ax.yaxis.set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_visible(False)
ax.grid(False)
ax.set_title(title)
fig.tight_layout()

# %% real-data
import plotly.express as px
countries = ["Japan", "China", "Iraq", "India", "Zimbabwe", "Nigeria"]
gm = px.data.gapminder().query("year in [1987, 2007] and country in @countries")
df = (gm.pivot(index="country", columns="year", values="lifeExp")
        .rename(columns=str).rename_axis(columns=None).reset_index().rename(columns={"country": "brand"}))
start, end = "1987", "2007"
title = "Life expectancy (years), 1987 → 2007"
df["change"] = df[end] - df[start]
df

# %% alt:altair
import altair as alt
long = df.melt(id_vars=["brand", "change"], value_vars=[start, end], var_name="year", value_name="value")
long["direction"] = np.where(long["change"] > 0, "Up", np.where(long["change"] < -2, "Down", "Flat"))
base = alt.Chart(long).encode(
    x=alt.X("year:N", title=None, axis=alt.Axis(labelAngle=0)),
    y=alt.Y("value:Q", title=None, scale=alt.Scale(zero=False)),
    color=alt.Color("direction:N", scale=alt.Scale(domain=["Up", "Down", "Flat"],
                                                   range=[PALETTE[0], PALETTE[1], "#b8b7b1"]), title=None),
    detail="brand:N")
chart = (base.mark_line(point=True) + base.mark_text(dx=8, align="left").encode(text="brand:N")
         .transform_filter(alt.datum.year == end)).properties(title=title, width=300, height=420)
chart
