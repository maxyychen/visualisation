# %% setup
from vizlib.plotly_style import *  # noqa: F401,F403  (inlined on build)
from plotly.subplots import make_subplots

# %% data
moneyness = np.linspace(0.70, 1.30, 25)                     # strike / spot
expiry = np.array([1/52, 2/52, 1/12, 2/12, 3/12, 6/12, 9/12, 1.0, 1.5, 2.0])
K, T = np.meshgrid(moneyness, expiry)
x = np.log(K)
atm = 0.16 + 0.025 * np.log1p(4 * T)                          # term structure
skew = -0.32 / np.sqrt(T + 0.15) * x                          # downside skew, fading with expiry
smile = 0.9 / (T + 0.25) * x**2                                # curvature, strongest short-dated
iv = 100 * (atm + skew * 0.35 + smile * 0.35)
expiry_labels = ["1W", "2W", "1M", "2M", "3M", "6M", "9M", "1Y", "18M", "2Y"]
surface = pd.DataFrame(iv.round(1), index=expiry_labels, columns=(100 * moneyness).round().astype(int))
surface.iloc[:, ::4]

# %% plot
fig = make_subplots(rows=1, cols=2, column_widths=[0.58, 0.42], horizontal_spacing=0.06,
                    specs=[[{"type": "surface"}, {"type": "heatmap"}]],
                    subplot_titles=("Rotate me: shape", "Read me: values (%)"))
fig.add_trace(go.Surface(
    x=100 * moneyness, y=np.arange(len(expiry)), z=iv, coloraxis="coloraxis",
    contours=dict(z=dict(show=True, project_z=True, usecolormap=True, width=1)),
    hovertemplate="strike %{x:.0f}% · expiry %{customdata}<br>IV %{z:.1f}%<extra></extra>",
    customdata=np.tile(np.array(expiry_labels)[:, None], (1, len(moneyness)))), row=1, col=1)
fig.add_trace(go.Heatmap(
    x=100 * moneyness, y=expiry_labels, z=iv, coloraxis="coloraxis",
    hovertemplate="strike %{x:.0f}% · expiry %{y}<br>IV %{z:.1f}%<extra></extra>"), row=1, col=2)
fig.update_layout(
    title="Implied volatility surface (simulated equity index)", height=560,
    coloraxis=dict(colorscale="Blues", colorbar=dict(title="IV (%)", x=1.02)),
    scene=dict(xaxis_title="Strike (% of spot)", zaxis_title="IV (%)",
               yaxis=dict(title="Expiry", tickvals=list(range(len(expiry))), ticktext=expiry_labels),
               camera=dict(eye=dict(x=-1.6, y=-1.5, z=0.9))),
    margin=dict(l=10, r=10, t=80, b=40),
)
fig.update_xaxes(title_text="Strike (% of spot)", row=1, col=2)
fig.update_yaxes(title_text="Expiry", row=1, col=2)
