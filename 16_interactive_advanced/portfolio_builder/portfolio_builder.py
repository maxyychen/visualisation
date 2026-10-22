"""
Portfolio Builder (weights → risk, return, drawdown)  -  family: Interactive, animated & big data

DESIGN PURPOSE
Sliders set the weights of four asset classes. The chart places the resulting
portfolio on the risk/return plane against the efficient frontier and the
individual assets, redraws its growth of $1, and reports return, volatility
and maximum drawdown, all recomputed in the browser from the monthly return
history. Readers learn diversification by doing it.

WHEN TO USE
  - Teach diversification and the efficient frontier interactively
  - Let a client or committee explore allocations before a formal optimisation
  - Show how adding a low-correlation asset (bonds, gold) changes risk and
    drawdown

AVOID WHEN
  - A recommendation document (show the chosen allocation and its statistics
    statically)
  - More than about five assets (sliders become unwieldy; use an optimiser and
    show results)
  - Readers might take historical or simulated statistics as forecasts

ALTERNATIVES
  - Efficient frontier (static)
  - Risk contribution chart
  - Allocation drift

EXAMPLE
Simulated monthly returns for 15 years of four asset classes (US equities,
international equities, bonds, gold) with realistic volatilities and
correlations. The frontier comes from 4,000 random long-only portfolios of the
same history.

Run:  python portfolio_builder.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import altair as alt

PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
           "#e87ba4", "#008300", "#6250d6", "#e34948"]


@alt.theme.register("vizlib", enable=True)
def vizlib_theme():
    return alt.theme.ThemeConfig({
        "config": {
            "background": "#fcfcfb",
            "view": {"stroke": None},
            "range": {"category": PALETTE},
            "font": "Helvetica, Arial, sans-serif",
            "title": {"anchor": "start", "fontSize": 14, "color": "#0b0b0b"},
            "axis": {"gridColor": "#e6e5e1", "domainColor": "#c9c8c3", "tickColor": "#c9c8c3",
                     "labelColor": "#52514e", "titleColor": "#52514e", "titleFontWeight": "normal"},
            "legend": {"labelColor": "#52514e", "titleColor": "#52514e"},
        }
    })

# --- Example data ------------------------------------------------------------
rng = np.random.default_rng(156)
assets = ["US equities", "Intl equities", "Bonds", "Gold"]
mu = np.array([0.085, 0.07, 0.03, 0.045]) / 12
sd = np.array([0.16, 0.18, 0.06, 0.15]) / np.sqrt(12)
corr = np.array([[1.0, 0.8, -0.1, 0.05], [0.8, 1.0, 0.0, 0.1], [-0.1, 0.0, 1.0, 0.25], [0.05, 0.1, 0.25, 1.0]])
R = rng.multivariate_normal(mu, np.outer(sd, sd) * corr, size=180)  # 15 years of monthly returns
monthly = pd.DataFrame(R, columns=["a1", "a2", "a3", "a4"]).assign(
    date=pd.date_range("2010-01-31", periods=180, freq="ME"))

# Annualised statistics of the same history, for the assets and the efficient frontier.
m, C = R.mean(0) * 12, np.cov(R.T) * 12
asset_pts = pd.DataFrame({"asset": assets, "ret": m, "risk": np.sqrt(np.diag(C))})
W = rng.dirichlet(np.full(4, 0.6), 4000)
cloud = pd.DataFrame({"ret": W @ m, "risk": np.sqrt(np.einsum("ij,jk,ik->i", W, C, W))})
cloud["bin"] = pd.cut(cloud["risk"], 30)
frontier = (cloud.loc[cloud.groupby("bin", observed=True)["ret"].idxmax(), ["risk", "ret"]]
            .sort_values("risk"))
frontier = frontier[frontier["ret"].cummax() == frontier["ret"]]  # keep the upper (efficient) edge
asset_pts.round(3)

# --- Plot --------------------------------------------------------------------
alt.data_transformers.disable_max_rows()
names = ["w1", "w2", "w3", "w4"]
defaults = [40, 20, 30, 10]
weights = [alt.param(name=n, value=v, bind=alt.binding_range(min=0, max=100, step=5, name=f"{a} weight "))
           for n, v, a in zip(names, defaults, assets)]
total = "max(w1 + w2 + w3 + w4, 1)"
port = alt.Chart(monthly).transform_calculate(
    rp=f"(w1 * datum.a1 + w2 * datum.a2 + w3 * datum.a3 + w4 * datum.a4) / {total}")

x = alt.X("risk:Q", title="Volatility (annualised)", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0.04, 0.2]))
y = alt.Y("ret:Q", title="Return (annualised)", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0.02, 0.1]))
plane = alt.layer(
    alt.Chart(cloud.drop(columns="bin")).mark_circle(size=8, color="#d0cfca", opacity=0.6).encode(x=x, y=y),
    alt.Chart(frontier).mark_line(color="#52514e", strokeWidth=2).encode(x=x, y=y),
    alt.Chart(asset_pts).mark_point(shape="diamond", filled=True, size=90, color="#52514e").encode(
        x=x, y=y, tooltip=["asset:N", alt.Tooltip("ret:Q", format=".1%"), alt.Tooltip("risk:Q", format=".1%")]),
    alt.Chart(asset_pts).mark_text(align="left", dx=8, fontSize=11, color="#52514e").encode(x=x, y=y, text="asset:N"),
    port.transform_aggregate(mean="mean(rp)", sd="stdev(rp)")
        .transform_calculate(ret="datum.mean * 12", risk="datum.sd * sqrt(12)")
        .mark_point(filled=True, size=260, color=PALETTE[0], stroke="#fcfcfb", strokeWidth=2, opacity=1)
        .encode(x=x, y=y, tooltip=[alt.Tooltip("ret:Q", title="Return", format=".1%"),
                                   alt.Tooltip("risk:Q", title="Volatility", format=".1%")]),
).properties(width=380, height=330, title=alt.Title("Risk vs. return", fontSize=12))

path = (port.transform_calculate(lr="log(1 + datum.rp)")
        .transform_window(cum="sum(lr)", frame=[None, 0], sort=[alt.SortField("date")])
        .transform_calculate(wealth="exp(datum.cum)")
        .transform_window(peak="max(wealth)", frame=[None, 0], sort=[alt.SortField("date")])
        .transform_calculate(dd="datum.wealth / max(datum.peak, 1) - 1"))
growth = path.mark_line(color=PALETTE[0], strokeWidth=2).encode(
    x=alt.X("date:T", title=None), y=alt.Y("wealth:Q", title="Growth of $1", scale=alt.Scale(type="log", domain=[0.8, 4]),
                 axis=alt.Axis(values=[1, 1.5, 2, 3, 4], format="$.1f")),
    tooltip=[alt.Tooltip("date:T", format="%b %Y"), alt.Tooltip("wealth:Q", format="$.2f")],
).properties(width=380, height=160, title=alt.Title("Growth of $1", fontSize=12))
drawdown = path.mark_area(color=PALETTE[1], opacity=0.45, line={"color": PALETTE[1], "strokeWidth": 1}).encode(
    x=alt.X("date:T", title=None), y=alt.Y("dd:Q", title="Drawdown", axis=alt.Axis(format="%"),
                                          scale=alt.Scale(domain=[-0.5, 0])),
).properties(width=380, height=110)

readout = (path.transform_aggregate(mean="mean(rp)", sd="stdev(rp)", mdd="min(dd)")
           .transform_calculate(label="'Return ' + format(datum.mean * 12, '.1%') + '/yr   ·   volatility '"
                                      " + format(datum.sd * sqrt(12), '.1%') + '   ·   max drawdown ' + format(datum.mdd, '.0%')")
           .mark_text(align="left", fontSize=14, fontWeight="bold").encode(x=alt.value(0), y=alt.value(0), text="label:N")
           .properties(width=780, height=10))
mix = (alt.Chart(pd.DataFrame({"row": [0]}))
       .transform_calculate(label=f"'Weights: US ' + format(w1 / {total}, '.0%') + ' · Intl ' + format(w2 / {total}, '.0%')"
                                  f" + ' · Bonds ' + format(w3 / {total}, '.0%') + ' · Gold ' + format(w4 / {total}, '.0%')")
       .mark_text(align="left", fontSize=12, color="#52514e").encode(x=alt.value(0), y=alt.value(0), text="label:N")
       .properties(width=780, height=10))

chart = (
    alt.vconcat(readout, mix, alt.hconcat(plane, alt.vconcat(growth, drawdown, spacing=8), spacing=40), spacing=14)
    .add_params(*weights)
    .properties(title=alt.Title("Portfolio builder: set the weights below (simulated history)", subtitle=[
        "Weights are normalised to 100%. Statistics recompute from 15 years of simulated monthly returns.", " "]))
)

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".html")
chart.save(out)
chart.save(out.with_suffix(".png"), scale_factor=2)  # static preview (vl-convert)
print(f"saved {out}")
if "--no-show" not in sys.argv:
    import webbrowser
    webbrowser.open(out.resolve().as_uri())
