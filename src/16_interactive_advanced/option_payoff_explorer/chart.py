# %% setup
from vizlib.altair_style import *  # noqa: F401,F403  (inlined on build)

# %% data
spot, r = 100.0, 0.03  # underlying price today, risk-free rate
prices = pd.DataFrame({"S": np.round(np.linspace(50, 150, 201), 2)})
prices.head()

# %% plot
strike = alt.param(name="strike", value=100,
                   bind=alt.binding_range(min=70, max=130, step=1, name="Strike ($) "))
vol = alt.param(name="vol", value=0.25,
                bind=alt.binding_range(min=0.05, max=0.80, step=0.01, name="Implied volatility "))
days = alt.param(name="days", value=90,
                 bind=alt.binding_range(min=1, max=365, step=1, name="Days to expiry "))
kind = alt.param(name="kind", value="Call",
                 bind=alt.binding_radio(options=["Call", "Put"], name="Option "))

T = "(days / 365)"
xs = alt.Scale(domain=[50, 150])


def black_scholes(S):
    """Vega expression for the Black-Scholes value of the selected option at underlying price S."""
    d1 = f"((log({S} / strike) + ({r} + vol * vol / 2) * {T}) / (vol * sqrt({T})))"
    d2 = f"({d1} - vol * sqrt({T}))"
    call = f"({S} * cumulativeNormal({d1}) - strike * exp(-{r} * {T}) * cumulativeNormal({d2}))"
    put = f"({call} - {S} + strike * exp(-{r} * {T}))"  # put-call parity
    return f"(kind == 'Call' ? {call} : {put})"


premium = black_scholes(spot)
payoff = "(kind == 'Call' ? max(datum.S - strike, 0) : max(strike - datum.S, 0))"

curves = (
    alt.Chart(prices)
    .transform_calculate(premium=premium)
    .transform_calculate(expiry=f"{payoff} - datum.premium",
                         today=f"{black_scholes('datum.S')} - datum.premium")
    .transform_fold(["expiry", "today"], as_=["key", "pnl"])
    .transform_calculate(curve="datum.key == 'expiry' ? 'At expiry' : 'Today (Black-Scholes)'")
    .mark_line(strokeWidth=2.5)
    .encode(
        x=alt.X("S:Q", title="Underlying price ($)", scale=xs),
        y=alt.Y("pnl:Q", title="Profit / loss per share ($)"),
        color=alt.Color("curve:N", title=None,
                        scale=alt.Scale(domain=["At expiry", "Today (Black-Scholes)"],
                                        range=["#52514e", PALETTE[0]]),
                        legend=alt.Legend(orient="bottom", direction="horizontal")),
        tooltip=[alt.Tooltip("S:Q", title="Underlying"), "curve:N",
                 alt.Tooltip("pnl:Q", title="P&L", format="+.2f")],
    )
)
one_row = pd.DataFrame({"row": [0]})
zero = alt.Chart(one_row).mark_rule(color="#8f8e88").encode(y=alt.datum(0))
spot_rule = alt.Chart(one_row).mark_rule(color="#b8b7b1").encode(x=alt.X(datum=spot, scale=xs))
strike_rule = (alt.Chart(one_row).transform_calculate(k="strike")
               .mark_rule(color=PALETTE[1], strokeWidth=1.5).encode(x=alt.X("k:Q", scale=xs)))
strike_label = (alt.Chart(one_row).transform_calculate(k="strike", label="'Strike ' + strike")
                .mark_text(align="left", dx=5, color=PALETTE[1], fontSize=11)
                .encode(x=alt.X("k:Q", scale=xs), y=alt.value(12), text="label:N"))
readout = (
    alt.Chart(one_row)
    .transform_calculate(premium=premium)
    .transform_calculate(be="kind == 'Call' ? strike + datum.premium : strike - datum.premium")
    .transform_calculate(label="kind + ' premium today: $' + format(datum.premium, '.2f')"
                               " + '   ·   breakeven at expiry: $' + format(datum.be, '.2f')")
    .mark_text(align="left", fontSize=13, fontWeight="bold", color="#0b0b0b")
    .encode(x=alt.value(0), y=alt.value(-14), text="label:N")
)
chart = (
    alt.layer(zero, spot_rule, strike_rule, strike_label, curves, readout)
    .add_params(strike, vol, days, kind)
    .properties(width=640, height=380,
                title=alt.Title("Option P&L explorer", subtitle=[
                    "Long one option bought today with the underlying at $100 (r = 3%). Move the sliders below.", " "]))
)
