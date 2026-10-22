# %% setup
from vizlib.plotly_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(8)
quarters = pd.period_range("2000Q1", "2025Q4", freq="Q")
t = quarters.year + (quarters.quarter - 1) / 4
# Anchor points (year, %) for the policy rate (short end) and the 10-year yield (long end).
short_pts = [(2000, 6.3), (2001.5, 3.5), (2003, 1.0), (2004.5, 1.3), (2006.5, 5.2), (2007.5, 5.0),
             (2008.9, 0.1), (2015.9, 0.2), (2018.9, 2.4), (2019.6, 2.0), (2020.2, 0.1), (2022.0, 0.1),
             (2022.4, 1.6), (2022.8, 4.3), (2023.5, 5.3), (2024.6, 5.3), (2025.9, 4.0)]
long_pts = [(2000, 6.0), (2003, 4.0), (2006, 4.8), (2008, 3.8), (2012, 1.8), (2014, 2.5), (2016, 1.8),
            (2018, 2.9), (2020, 0.9), (2021.8, 1.5), (2022.8, 3.8), (2023, 4.1), (2024, 4.2), (2025.9, 4.4)]
short = np.interp(t, *zip(*short_pts)) + rng.normal(0, 0.05, len(t))
long = np.interp(t, *zip(*long_pts)) + rng.normal(0, 0.08, len(t))

maturities = ["1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
years_to_mat = np.array([1/12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
tau = 2.0
shape = (1 - np.exp(-years_to_mat / tau)) / (years_to_mat / tau)    # Nelson-Siegel slope loading
shape10 = (1 - np.exp(-10 / tau)) / (10 / tau)
curves = pd.DataFrame(
    [lng + (sht - lng) * (shape - shape10) / (1 - shape10) + 0.15 * (years_to_mat > 10) for sht, lng in zip(short, long)],
    index=quarters.strftime("%Y Q%q"), columns=maturities).clip(lower=0.02).round(2)
curves["10y-2y"] = curves["10Y"] - curves["2Y"]
curves = curves.iloc[3::4]                                # one frame per year: the year-end (Q4) curve
curves.index = curves.index.str[:4]
curves.iloc[::5]

# %% plot
TRAIL = 3  # previous years shown faintly
labels = list(curves.index)


def frame_traces(i):
    traces = []
    for k in range(TRAIL, 0, -1):  # always the same number of traces: full traces in every frame
        j = i - k
        y = curves.iloc[j][maturities] if j >= 0 else [None] * len(maturities)
        traces.append(go.Scatter(x=maturities, y=y, mode="lines", hoverinfo="skip",
                                 line=dict(color="#b8b7b1", width=1), opacity=0.25 + 0.15 * (TRAIL - k)))
    inverted = curves["10y-2y"].iloc[i] < 0
    traces.append(go.Scatter(x=maturities, y=curves.iloc[i][maturities], mode="lines+markers",
                             line=dict(color=PALETTE[1] if inverted else PALETTE[0], width=3),
                             marker=dict(size=7), hovertemplate="%{x}: %{y:.2f}%<extra></extra>"))
    return traces


def frame_title(i):
    spread = curves["10y-2y"].iloc[i]
    state = "INVERTED" if spread < 0 else "normal"
    return f"US Treasury curve (simulated), end of {labels[i]}  ·  10y–2y {spread:+.2f} pp  ·  {state}"


fig = go.Figure(
    data=frame_traces(0),
    frames=[go.Frame(data=frame_traces(i), name=labels[i], layout=dict(title_text=frame_title(i)))
            for i in range(len(curves))],
)
fig.update_layout(
    title_text=frame_title(0), showlegend=False, height=560,
    xaxis=dict(title="Maturity", type="category"),
    yaxis=dict(title="Yield (%)", range=[0, 7.2]),
    updatemenus=[dict(type="buttons", x=0, y=-0.12, xanchor="left", direction="left", buttons=[
        dict(label="▶ Play", method="animate",
             args=[None, dict(frame=dict(duration=450, redraw=False), fromcurrent=True, transition=dict(duration=0))]),
        dict(label="❚❚ Pause", method="animate",
             args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])])],
    sliders=[dict(x=0.17, y=-0.08, len=0.83, currentvalue=dict(visible=False),
                  steps=[dict(label=lab if int(lab) % 5 == 0 else "", method="animate",
                              args=[[lab], dict(mode="immediate", frame=dict(duration=0, redraw=False))])
                         for lab in labels])],
    margin=dict(b=110),
)
