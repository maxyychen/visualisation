"""
vizlib.finance: portfolio performance metrics and a one-page performance report.

Conventions
-----------
* ``returns`` are *simple* periodic returns (0.01 = +1%) in a pandas Series with a
  DatetimeIndex. Use :func:`to_returns` to convert prices.
* Annualisation uses ``periods_per_year`` (252 daily, 52 weekly, 12 monthly). When
  omitted it is inferred from the index spacing.
* Risk-free rate ``rf`` is an annual rate and is converted to the return frequency.

Quick use
---------
>>> from vizlib.finance import to_returns, summary_stats, tear_sheet
>>> r = to_returns(prices)                 # prices: pd.Series
>>> summary_stats(r, benchmark=to_returns(index_prices))
>>> fig = tear_sheet(r, benchmark=to_returns(index_prices), title="My fund")

Command line (CSV with a date column and one or more price columns):
    python -m vizlib.finance prices.csv --price Fund --benchmark Index -o report.png

Educational code, not investment advice.
"""
from __future__ import annotations

import argparse
from typing import Optional

import numpy as np
import pandas as pd

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# --------------------------------------------------------------------------- basics
def to_returns(prices: pd.Series | pd.DataFrame, log: bool = False):
    """Periodic returns from a price series; the first (undefined) period is dropped."""
    prices = prices.astype(float)
    r = np.log(prices / prices.shift(1)) if log else prices.pct_change(fill_method=None)
    return r.iloc[1:]


def infer_periods_per_year(index: pd.Index) -> int:
    """252 for daily, 52 weekly, 12 monthly, 4 quarterly, 1 annual (from the median gap)."""
    if len(index) < 3 or not isinstance(index, pd.DatetimeIndex):
        return 252
    days = float(np.median(np.diff(index.values).astype("timedelta64[D]").astype(float)))
    for limit, ppy in ((4, 252), (10, 52), (45, 12), (120, 4)):
        if days <= limit:
            return ppy
    return 1


def _ppy(returns, periods_per_year):
    return periods_per_year or infer_periods_per_year(returns.index)


def growth_of(returns: pd.Series, start: float = 1.0) -> pd.Series:
    """Value of `start` invested at the beginning, compounding the returns."""
    return start * (1 + returns).cumprod()


def drawdown(returns: pd.Series) -> pd.Series:
    """Fractional decline from the running peak (0 at a new high, -0.25 = 25% below peak)."""
    wealth = growth_of(returns)
    peak = np.maximum(wealth.cummax(), 1.0)  # the starting value counts as a peak
    return wealth / peak - 1


def max_drawdown(returns: pd.Series) -> float:
    return float(drawdown(returns).min())


def drawdown_periods(returns: pd.Series, top: int = 5) -> pd.DataFrame:
    """The `top` worst drawdowns: peak date, trough date, recovery date (NaT if ongoing), depth."""
    dd = drawdown(returns)
    out, in_dd, start = [], False, None
    for t, v in dd.items():
        if v < 0 and not in_dd:
            in_dd, start = True, t
        elif v == 0 and in_dd:
            seg = dd[start:t]
            out.append((start, seg.idxmin(), t, seg.min()))
            in_dd = False
    if in_dd:
        seg = dd[start:]
        out.append((start, seg.idxmin(), pd.NaT, seg.min()))
    df = pd.DataFrame(out, columns=["start", "trough", "recovery", "depth"])
    return df.sort_values("depth").head(top).reset_index(drop=True)


# --------------------------------------------------------------------------- metrics
def total_return(returns: pd.Series) -> float:
    return float((1 + returns).prod() - 1)


def cagr(returns: pd.Series, periods_per_year: Optional[int] = None) -> float:
    """Compound annual growth rate."""
    years = len(returns) / _ppy(returns, periods_per_year)
    return float((1 + total_return(returns)) ** (1 / years) - 1)


def annual_volatility(returns: pd.Series, periods_per_year: Optional[int] = None) -> float:
    return float(returns.std(ddof=1) * np.sqrt(_ppy(returns, periods_per_year)))


def _excess(returns, rf, ppy):
    return returns - ((1 + rf) ** (1 / ppy) - 1)


def sharpe(returns: pd.Series, rf: float = 0.0, periods_per_year: Optional[int] = None) -> float:
    """Annualised Sharpe ratio: mean excess return / volatility, scaled by sqrt(periods)."""
    ppy = _ppy(returns, periods_per_year)
    ex = _excess(returns, rf, ppy)
    return float(ex.mean() / ex.std(ddof=1) * np.sqrt(ppy))


def sortino(returns: pd.Series, rf: float = 0.0, periods_per_year: Optional[int] = None) -> float:
    """Like Sharpe, but only downside deviation (returns below the risk-free rate) counts as risk."""
    ppy = _ppy(returns, periods_per_year)
    ex = _excess(returns, rf, ppy)
    downside = np.sqrt((np.minimum(ex, 0) ** 2).mean())
    return float(ex.mean() / downside * np.sqrt(ppy))


def calmar(returns: pd.Series, periods_per_year: Optional[int] = None) -> float:
    """CAGR divided by the absolute maximum drawdown."""
    return float(cagr(returns, periods_per_year) / abs(max_drawdown(returns)))


def var_historical(returns: pd.Series, level: float = 0.95) -> float:
    """Historical Value-at-Risk: the (1-level) quantile of returns (a negative number = loss)."""
    return float(np.quantile(returns.dropna(), 1 - level))


def cvar_historical(returns: pd.Series, level: float = 0.95) -> float:
    """Conditional VaR / expected shortfall: mean return in the worst (1-level) tail."""
    v = var_historical(returns, level)
    return float(returns[returns <= v].mean())


def beta(returns: pd.Series, benchmark: pd.Series) -> float:
    r, b = returns.align(benchmark, join="inner")
    return float(np.cov(r, b, ddof=1)[0, 1] / b.var(ddof=1))


def alpha(returns: pd.Series, benchmark: pd.Series, rf: float = 0.0,
          periods_per_year: Optional[int] = None) -> float:
    """Annualised Jensen's alpha (CAPM), using arithmetic mean excess returns."""
    r, b = returns.align(benchmark, join="inner")
    ppy = _ppy(r, periods_per_year)
    er, eb = _excess(r, rf, ppy), _excess(b, rf, ppy)
    return float((er.mean() - beta(r, b) * eb.mean()) * ppy)


def tracking_error(returns, benchmark, periods_per_year=None) -> float:
    r, b = returns.align(benchmark, join="inner")
    return float((r - b).std(ddof=1) * np.sqrt(_ppy(r, periods_per_year)))


def information_ratio(returns, benchmark, periods_per_year=None) -> float:
    r, b = returns.align(benchmark, join="inner")
    ppy = _ppy(r, periods_per_year)
    active = r - b
    return float(active.mean() / active.std(ddof=1) * np.sqrt(ppy))


def rolling_volatility(returns, window, periods_per_year=None) -> pd.Series:
    return returns.rolling(window).std(ddof=1) * np.sqrt(_ppy(returns, periods_per_year))


def rolling_sharpe(returns, window, rf=0.0, periods_per_year=None) -> pd.Series:
    ppy = _ppy(returns, periods_per_year)
    ex = _excess(returns, rf, ppy)
    return ex.rolling(window).mean() / ex.rolling(window).std(ddof=1) * np.sqrt(ppy)


def period_returns(returns: pd.Series, freq: str = "ME") -> pd.Series:
    """Compound returns into calendar periods ('ME' month-end, 'YE' year-end, 'QE' quarter-end)."""
    return (1 + returns).resample(freq).prod(min_count=1) - 1  # empty periods stay NaN


def monthly_returns_table(returns: pd.Series) -> pd.DataFrame:
    """Year x month table of compounded monthly returns, plus a compounded 'Year' column."""
    m = period_returns(returns, "ME")
    table = (m.to_frame("r").assign(year=m.index.year, month=m.index.month)
             .pivot(index="year", columns="month", values="r")
             .reindex(columns=range(1, 13)))
    table.columns = MONTHS
    table["Year"] = (1 + table[MONTHS].fillna(0)).prod(axis=1) - 1
    return table


def summary_stats(returns: pd.Series, benchmark: Optional[pd.Series] = None, rf: float = 0.0,
                  periods_per_year: Optional[int] = None) -> pd.DataFrame:
    """Key statistics as a tidy table (one column per series)."""
    def stats(r):
        return {
            "Total return": total_return(r), "CAGR": cagr(r, periods_per_year),
            "Volatility (ann.)": annual_volatility(r, periods_per_year),
            "Sharpe": sharpe(r, rf, periods_per_year), "Sortino": sortino(r, rf, periods_per_year),
            "Max drawdown": max_drawdown(r), "Calmar": calmar(r, periods_per_year),
            "VaR 95% (1 period)": var_historical(r), "CVaR 95% (1 period)": cvar_historical(r),
            "Best period": float(r.max()), "Worst period": float(r.min()),
            "% positive periods": float((r > 0).mean()),
        }
    cols = {returns.name or "Strategy": stats(returns)}
    if benchmark is not None:
        r, b = returns.align(benchmark, join="inner")
        cols[benchmark.name or "Benchmark"] = stats(b)
        rel = {"Beta": beta(r, b), "Alpha (ann.)": alpha(r, b, rf, periods_per_year),
               "Tracking error": tracking_error(r, b, periods_per_year),
               "Information ratio": information_ratio(r, b, periods_per_year)}
        for k, v in rel.items():
            cols[returns.name or "Strategy"][k] = v
            cols[benchmark.name or "Benchmark"][k] = np.nan
    return pd.DataFrame(cols)


# --------------------------------------------------------------------------- formatting
def fmt_pct(x: float, digits: int = 1, sign: bool = False) -> str:
    return "–" if pd.isna(x) else f"{x:{'+' if sign else ''}.{digits}%}"


def fmt_money(x: float, currency: str = "$") -> str:
    """$1.23B / $45.6M / $7.8k / $950"""
    if pd.isna(x):
        return "–"
    sign, x = ("-" if x < 0 else ""), abs(x)
    for div, suffix in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "k")):
        if x >= div:
            return f"{sign}{currency}{x / div:.3g}{suffix}"
    return f"{sign}{currency}{x:,.0f}"


def fmt_bps(x: float) -> str:
    return "–" if pd.isna(x) else f"{x * 1e4:+.0f} bps"


def percent_axis(ax, axis: str = "y", digits: int = 0):
    from matplotlib.ticker import PercentFormatter
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(PercentFormatter(1.0, decimals=digits))


# --------------------------------------------------------------------------- report
def tear_sheet(returns: pd.Series, benchmark: Optional[pd.Series] = None, title: str = "Performance report",
               rf: float = 0.0, periods_per_year: Optional[int] = None):
    """One-page performance report as a matplotlib Figure.

    Panels: headline statistics, growth of $1 (log scale) vs. benchmark, drawdown,
    rolling volatility, rolling Sharpe, monthly-returns calendar and annual returns.
    """
    import matplotlib.pyplot as plt
    from matplotlib.colors import TwoSlopeNorm
    from vizlib.mpl_style import PALETTE  # noqa: F401  (also applies the library style)

    ppy = _ppy(returns, periods_per_year)
    name = returns.name or "Strategy"
    bname = (benchmark.name or "Benchmark") if benchmark is not None else None
    if benchmark is not None:
        returns, benchmark = returns.align(benchmark, join="inner")
    window = {252: 126, 52: 26, 12: 12}.get(ppy, max(ppy // 2, 3))
    blue, orange, gray, ink2 = PALETTE[0], PALETTE[1], "#8f8e88", "#52514e"

    fig = plt.figure(figsize=(11, 13.5))
    gs = fig.add_gridspec(5, 2, height_ratios=[0.45, 1.5, 0.9, 0.9, 1.6], hspace=0.6, wspace=0.18,
                          top=0.925, bottom=0.07, left=0.08, right=0.92)
    fig.suptitle(f"{title}\n", x=0.06, ha="left", fontsize=17, fontweight="bold", y=0.985)
    start, end = returns.index[0], returns.index[-1]
    fig.text(0.06, 0.952, f"{name}{' vs. ' + bname if bname else ''} · {start:%b %Y} – {end:%b %Y} · "
             f"{len(returns):,} periods · rf = {rf:.1%}", color=ink2, fontsize=10)

    # 1. KPI strip
    kpi = fig.add_subplot(gs[0, :])
    kpi.axis("off")
    tiles = [("CAGR", fmt_pct(cagr(returns, ppy))), ("Volatility", fmt_pct(annual_volatility(returns, ppy))),
             ("Sharpe", f"{sharpe(returns, rf, ppy):.2f}"), ("Max drawdown", fmt_pct(max_drawdown(returns))),
             ("Calmar", f"{calmar(returns, ppy):.2f}")]
    if benchmark is not None:
        tiles.append(("Beta", f"{beta(returns, benchmark):.2f}"))
    for i, (label, value) in enumerate(tiles):
        x = i / len(tiles)
        kpi.text(x, 0.85, label, transform=kpi.transAxes, color=ink2, fontsize=10)
        kpi.text(x, 0.15, value, transform=kpi.transAxes, fontsize=21, fontweight="bold")
        if benchmark is not None and label in ("CAGR", "Volatility", "Sharpe", "Max drawdown", "Calmar"):
            f = {"CAGR": lambda r: fmt_pct(cagr(r, ppy)), "Volatility": lambda r: fmt_pct(annual_volatility(r, ppy)),
                 "Sharpe": lambda r: f"{sharpe(r, rf, ppy):.2f}", "Max drawdown": lambda r: fmt_pct(max_drawdown(r)),
                 "Calmar": lambda r: f"{calmar(r, ppy):.2f}"}[label]
            kpi.text(x, -0.25, f"benchmark {f(benchmark)}", transform=kpi.transAxes, color=gray, fontsize=9)

    # 2. Growth of $1
    ax = fig.add_subplot(gs[1, :])
    g = growth_of(returns)
    if benchmark is not None:
        gb = growth_of(benchmark)
        ax.plot(gb.index, gb, color=gray, linewidth=1.5, label=bname)
        ax.text(gb.index[-1], gb.iloc[-1], f"  {bname} {gb.iloc[-1]:.2f}", color=gray, va="center", fontsize=9)
    ax.plot(g.index, g, color=blue, label=name)
    ax.text(g.index[-1], g.iloc[-1], f"  {name} {g.iloc[-1]:.2f}", color=blue, va="center",
            fontsize=9, fontweight="bold")
    ax.set_yscale("log")
    lo, hi = ax.get_ylim()
    nice = np.array([b * 10.0 ** e for e in range(-2, 4) for b in (1, 1.5, 2, 3, 5, 7.5)])
    ticks = nice[(nice >= lo) & (nice <= hi)]
    if len(ticks) > 7:
        ticks = ticks[:: int(np.ceil(len(ticks) / 7))]
    ax.yaxis.set_major_locator(plt.FixedLocator(ticks))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:g}"))
    ax.yaxis.set_minor_locator(plt.NullLocator())
    ax.set_title("Growth of $1 (log scale)")
    ax.legend(loc="upper left")

    # 3. Drawdown
    ax = fig.add_subplot(gs[2, :])
    dd = drawdown(returns)
    if benchmark is not None:
        ax.plot(benchmark.index, drawdown(benchmark), color=gray, linewidth=1, label=bname)
    ax.fill_between(dd.index, dd, 0, color=orange, alpha=0.35, linewidth=0)
    ax.plot(dd.index, dd, color=orange, linewidth=1.2, label=name)
    ax.annotate(f"Max {fmt_pct(dd.min())}", (dd.idxmin(), dd.min()), xytext=(8, -2),
                textcoords="offset points", fontsize=9, color=ink2, va="top")
    percent_axis(ax)
    ax.set_title("Drawdown from previous peak")

    # 4. Rolling volatility / Sharpe (two panels, never a dual axis)
    for col, (label, series) in enumerate([
            (f"Rolling volatility ({window} periods, ann.)", rolling_volatility(returns, window, ppy)),
            (f"Rolling Sharpe ({window} periods)", rolling_sharpe(returns, window, rf, ppy))]):
        ax = fig.add_subplot(gs[3, col])
        ax.plot(series.index, series, color=blue, linewidth=1.5)
        if col == 0:
            percent_axis(ax)
        else:
            ax.axhline(0, color=ink2, linewidth=0.8)
        ax.set_title(label, fontsize=11)
        ax.tick_params(axis="x", labelsize=8)

    # 5. Monthly returns calendar + annual returns
    table = monthly_returns_table(returns)
    ax = fig.add_subplot(gs[4, 0])
    vals = table[MONTHS].values
    lim = np.nanmax(np.abs(vals)) or 0.01
    from matplotlib.colors import LinearSegmentedColormap
    gain_loss = LinearSegmentedColormap.from_list("gain_loss", [orange, "#f2f1ee", blue])
    ax.imshow(vals, cmap=gain_loss, norm=TwoSlopeNorm(0, -lim, lim), aspect="auto")
    for (i, j), v in np.ndenumerate(vals):
        if not np.isnan(v):
            ax.text(j, i, f"{v * 100:.1f}", ha="center", va="center", fontsize=7,
                    color="white" if abs(v) > 0.6 * lim else "#0b0b0b")
    ax.set_xticks(range(12), [m[0] for m in MONTHS])
    ax.set_yticks(range(len(table)), table.index)
    ax.grid(False)
    ax.set_title("Monthly returns (%)", fontsize=11)
    for s in ax.spines.values():
        s.set_visible(False)

    ax = fig.add_subplot(gs[4, 1])
    yr = table["Year"]
    y = np.arange(len(yr))
    h = 0.38 if benchmark is not None else 0.7
    ax.barh(y - (h / 2 if benchmark is not None else 0), yr.values, height=h,
            color=np.where(yr.values >= 0, blue, orange), label=name)
    if benchmark is not None:
        yb = monthly_returns_table(benchmark)["Year"].reindex(yr.index)
        ax.barh(y + h / 2, yb.values, height=h, color="#d0cfca", label=bname)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=8)
    ax.set_yticks(y, yr.index)
    ax.invert_yaxis()
    ax.axvline(0, color=ink2, linewidth=0.8)
    percent_axis(ax, "x")
    ax.grid(axis="y", visible=False)
    ax.set_title("Calendar-year returns", fontsize=11)

    fig.text(0.06, 0.012, "Past performance does not predict future returns. Educational example, not investment advice.",
             color=gray, fontsize=8)
    return fig


# --------------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description="One-page performance report from a CSV of prices.")
    ap.add_argument("csv")
    ap.add_argument("--date", default=None, help="date column (default: first column)")
    ap.add_argument("--price", required=True, help="price column of the strategy/fund")
    ap.add_argument("--benchmark", default=None, help="price column of the benchmark")
    ap.add_argument("--rf", type=float, default=0.0, help="annual risk-free rate, e.g. 0.03")
    ap.add_argument("--title", default="Performance report")
    ap.add_argument("-o", "--out", default="tear_sheet.png", help=".png, .pdf or .svg")
    a = ap.parse_args(argv)

    df = pd.read_csv(a.csv)
    date_col = a.date or df.columns[0]
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col).sort_index()
    r = to_returns(df[a.price]).rename(a.price)
    b = to_returns(df[a.benchmark]).rename(a.benchmark) if a.benchmark else None
    print(summary_stats(r, b, a.rf).to_string(float_format=lambda v: f"{v:,.4f}"))
    fig = tear_sheet(r, b, a.title, a.rf)
    fig.savefig(a.out, dpi=150, bbox_inches="tight")
    print(f"saved {a.out}")


if __name__ == "__main__":
    main()
