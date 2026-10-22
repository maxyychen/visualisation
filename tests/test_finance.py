"""Unit tests for vizlib.finance, against hand-computed values."""
import numpy as np
import pandas as pd
import pytest

import matplotlib
matplotlib.use("Agg")

from vizlib import finance as fin


def series(values, freq="B", start="2020-01-01", name=None):
    return pd.Series(values, index=pd.date_range(start, periods=len(values), freq=freq), name=name, dtype=float)


def test_to_returns_simple_and_log():
    p = series([100, 110, 99])
    assert fin.to_returns(p).tolist() == pytest.approx([0.10, -0.10])
    assert fin.to_returns(p, log=True).tolist() == pytest.approx([np.log(1.1), np.log(0.9)])


def test_drawdown_and_max_drawdown():
    r = fin.to_returns(series([100, 120, 90, 130]))
    assert fin.drawdown(r).tolist() == pytest.approx([0.0, -0.25, 0.0])
    assert fin.max_drawdown(r) == pytest.approx(-0.25)


def test_drawdown_counts_initial_value_as_peak():
    r = fin.to_returns(series([100, 80, 100]))
    assert fin.drawdown(r).tolist() == pytest.approx([-0.20, 0.0])


def test_drawdown_periods_finds_recovery_and_ongoing():
    r = fin.to_returns(series([100, 120, 90, 130, 117]))
    periods = fin.drawdown_periods(r)
    assert periods.loc[0, "depth"] == pytest.approx(-0.25)
    assert pd.notna(periods.loc[0, "recovery"])
    assert pd.isna(periods.loc[1, "recovery"]) and periods.loc[1, "depth"] == pytest.approx(-0.10)


def test_cagr_doubling_over_two_years():
    n = 504  # 2 years of trading days
    r = series(np.full(n, 2 ** (1 / n) - 1))
    assert fin.total_return(r) == pytest.approx(1.0)
    assert fin.cagr(r, 252) == pytest.approx(np.sqrt(2) - 1)


def test_volatility_and_sharpe():
    r = series([0.01, -0.01] * 50)
    sd = np.std(r, ddof=1)
    assert fin.annual_volatility(r, 252) == pytest.approx(sd * np.sqrt(252))
    r2 = r + 0.001
    assert fin.sharpe(r2, 0.0, 252) == pytest.approx(0.001 / sd * np.sqrt(252))


def test_sortino_ignores_upside():
    r = series([0.02, -0.01, 0.02, -0.01])
    downside = np.sqrt(np.mean(np.minimum(r, 0) ** 2))
    assert fin.sortino(r, 0.0, 252) == pytest.approx(r.mean() / downside * np.sqrt(252))


def test_risk_free_rate_is_deannualised():
    r = series(np.full(252, 0.0002) + np.tile([0.001, -0.001], 126))
    daily_rf = 1.05 ** (1 / 252) - 1
    expected = (r - daily_rf).mean() / (r - daily_rf).std(ddof=1) * np.sqrt(252)
    assert fin.sharpe(r, 0.05, 252) == pytest.approx(expected)


def test_var_and_cvar():
    r = series(np.linspace(-0.05, 0.04, 10))
    assert fin.var_historical(r, 0.9) == pytest.approx(np.quantile(r, 0.1))
    assert fin.cvar_historical(r, 0.9) <= fin.var_historical(r, 0.9)
    assert fin.cvar_historical(r, 0.9) == pytest.approx(-0.05)


def test_beta_alpha_tracking():
    rng = np.random.default_rng(0)
    b = series(rng.normal(0.0005, 0.01, 500))
    r = 2 * b + 0.0001
    assert fin.beta(r, b) == pytest.approx(2.0)
    assert fin.alpha(r, b, 0.0, 252) == pytest.approx(0.0001 * 252)
    assert fin.tracking_error(b, b, 252) == pytest.approx(0.0)


def test_monthly_table_compounds_within_month_and_year():
    idx = pd.to_datetime(["2021-01-05", "2021-01-20", "2021-02-10", "2022-03-01"])
    r = pd.Series([0.10, 0.10, -0.05, 0.02], index=idx)
    t = fin.monthly_returns_table(r)
    assert t.loc[2021, "Jan"] == pytest.approx(0.21)
    assert t.loc[2021, "Feb"] == pytest.approx(-0.05)
    assert np.isnan(t.loc[2021, "Mar"])
    assert t.loc[2021, "Year"] == pytest.approx(1.21 * 0.95 - 1)
    assert t.loc[2022, "Year"] == pytest.approx(0.02)


@pytest.mark.parametrize("freq,expected", [("B", 252), ("W-FRI", 52), ("ME", 12), ("QE", 4), ("YE", 1)])
def test_infer_periods_per_year(freq, expected):
    idx = pd.date_range("2020-01-01", periods=30, freq=freq)
    assert fin.infer_periods_per_year(idx) == expected


def test_formatting():
    assert fin.fmt_money(1_234_000) == "$1.23M"
    assert fin.fmt_money(-950) == "-$950"
    assert fin.fmt_pct(0.1234, 1, sign=True) == "+12.3%"
    assert fin.fmt_bps(0.0025) == "+25 bps"


def test_summary_stats_shape():
    rng = np.random.default_rng(1)
    r = series(rng.normal(0.0004, 0.01, 600), name="Fund")
    b = series(rng.normal(0.0003, 0.009, 600), name="Index")
    s = fin.summary_stats(r, b)
    assert list(s.columns) == ["Fund", "Index"]
    assert {"Sharpe", "Max drawdown", "Beta", "Information ratio"} <= set(s.index)


@pytest.mark.parametrize("with_benchmark", [False, True])
def test_tear_sheet_renders(with_benchmark):
    rng = np.random.default_rng(2)
    r = series(rng.normal(0.0004, 0.01, 800), name="Fund")
    b = series(rng.normal(0.0003, 0.009, 800), name="Index") if with_benchmark else None
    fig = fin.tear_sheet(r, b)
    assert len(fig.axes) >= 6


def test_cli(tmp_path):
    rng = np.random.default_rng(3)
    idx = pd.date_range("2021-01-01", periods=300, freq="B")
    df = pd.DataFrame({"Date": idx, "Fund": 100 * np.cumprod(1 + rng.normal(0.0005, 0.01, 300)),
                       "Index": 100 * np.cumprod(1 + rng.normal(0.0003, 0.009, 300))})
    csv = tmp_path / "prices.csv"
    df.to_csv(csv, index=False)
    out = tmp_path / "report.png"
    fin.main([str(csv), "--price", "Fund", "--benchmark", "Index", "-o", str(out)])
    assert out.exists() and out.stat().st_size > 10_000
