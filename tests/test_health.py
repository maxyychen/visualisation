"""Unit tests for vizlib.health, against hand-computed values and lifelines."""
import numpy as np
import pandas as pd
import pytest

from vizlib import health as h


# --------------------------------------------------------------------------- survival
TIME = [1, 2, 2, 3, 4]
EVENT = [1, 1, 0, 1, 0]


def test_kaplan_meier_hand_example():
    km = h.kaplan_meier(TIME, EVENT)
    assert km["time"].tolist() == [0, 1, 2, 3, 4]
    assert km["survival"].tolist() == pytest.approx([1.0, 0.8, 0.6, 0.3, 0.3])
    assert km["at_risk"].tolist() == [5, 5, 4, 2, 1]
    # Greenwood: S(1)^2 * 1/(5*4)
    assert km.loc[1, "se"] == pytest.approx(0.8 * np.sqrt(1 / 20))
    assert (km["ci_lower"] <= km["survival"]).all() and (km["survival"] <= km["ci_upper"]).all()


def test_kaplan_meier_matches_lifelines():
    lifelines = pytest.importorskip("lifelines")
    rng = np.random.default_rng(0)
    t = np.round(rng.exponential(10, 200), 1)
    e = (rng.random(200) < 0.7).astype(int)
    km = h.kaplan_meier(t, e)
    ref = lifelines.KaplanMeierFitter().fit(t, e)
    ours = h.survival_at(km, ref.survival_function_.index.values)
    assert ours == pytest.approx(ref.survival_function_.iloc[:, 0].values)
    ci = ref.confidence_interval_survival_function_
    ours_ci = km.set_index("time").reindex(ref.survival_function_.index.values)["ci_lower"].values
    assert ours_ci == pytest.approx(ci.iloc[:, 0].values, abs=1e-6)


def test_median_rmst_and_at_risk():
    km = h.kaplan_meier(TIME, EVENT)
    assert h.median_survival(km) == 3
    assert h.rmst(km, 3) == pytest.approx(1 + 0.8 + 0.6)
    assert h.rmst(km, 2.5) == pytest.approx(1 + 0.8 + 0.6 * 0.5)
    assert h.at_risk(TIME, [0, 2, 3.5, 5]).tolist() == [5, 4, 1, 0]


def test_kaplan_meier_keeps_events_at_time_zero():
    km = h.kaplan_meier([0, 1, 2, 3], [1, 1, 0, 1])
    assert km["time"].iloc[0] == 0 and km["survival"].iloc[0] == pytest.approx(0.75)


def test_median_not_reached():
    km = h.kaplan_meier([1, 2, 3], [1, 0, 0])
    assert np.isnan(h.median_survival(km))


# --------------------------------------------------------------------------- quality improvement
def test_run_chart_shift_and_trend():
    y = [5, 5, 4, 5, 4, 5, 9, 9, 9, 9, 9, 9, 5, 1, 2, 3, 4, 6]
    sig = h.run_chart_signals(y, center=5)
    assert sig["shift"] == [6, 7, 8, 9, 10, 11]            # six points above the median
    assert sig["trend"] == [13, 14, 15, 16, 17]             # five points rising in a row


def test_run_chart_points_on_median_do_not_break_shift():
    y = [6, 6, 5, 6, 6, 6, 6, 1]
    assert h.run_chart_signals(y, center=5)["shift"] == [0, 1, 3, 4, 5, 6]


def test_run_chart_random_data_has_expected_runs():
    rng = np.random.default_rng(1)
    sig = h.run_chart_signals(rng.normal(size=40))
    lo, hi = sig["runs_expected"]
    assert lo <= sig["runs"] <= hi and not sig["too_few_runs"]


def test_p_chart_limits():
    out = h.p_chart([100, 200, 300], [1000, 1000, 1000])
    assert out["center"].iloc[0] == pytest.approx(0.2)
    half = 3 * np.sqrt(0.2 * 0.8 / 1000)
    assert out["ucl"].iloc[0] == pytest.approx(0.2 + half)
    assert out["signal"].tolist() == [True, False, True]


def test_u_chart_limits():
    out = h.u_chart([4, 6], [1000, 1000])
    assert out["center"].iloc[0] == pytest.approx(0.005)
    assert out["ucl"].iloc[0] == pytest.approx(0.005 + 3 * np.sqrt(0.005 / 1000))
    assert (out["lcl"] >= 0).all()


def test_funnel_limits_narrow_with_n_and_match_normal_for_large_n():
    lo, hi = h.funnel_limits(0.1, [20, 200, 20000], level=0.95)
    assert np.all(np.diff(hi) < 0) and np.all(np.diff(lo) > 0)
    nlo, nhi = h.funnel_limits(0.1, 20000, level=0.95, exact=False)
    assert hi[-1] == pytest.approx(nhi, abs=5e-4) and lo[-1] == pytest.approx(nlo, abs=5e-4)


def test_vlad():
    assert h.vlad([0, 1, 0], [0.1, 0.2, 0.3]).tolist() == pytest.approx([0.1, -0.7, -0.4])


def test_ra_cusum_weights_and_floor():
    # odds ratio 1 => no evidence either way
    assert h.ra_cusum([1, 0, 1], [0.2, 0.2, 0.2], odds_ratio=1.0).tolist() == [0, 0, 0]
    out = h.ra_cusum([1, 0], [0.1, 0.1], odds_ratio=2.0)
    w_death = np.log(2 / (1 - 0.1 + 0.2))
    assert out[0] == pytest.approx(w_death)
    assert out[1] == pytest.approx(max(0, w_death + np.log(1 / 1.1)))


def test_ra_cusum_signals_on_doubled_risk_and_resets():
    rng = np.random.default_rng(2)
    p = rng.uniform(0.02, 0.2, 2000)
    bad = (rng.random(2000) < np.clip(2.5 * p, 0, 1)).astype(int)
    good = (rng.random(2000) < p).astype(int)
    assert h.ra_cusum(bad, p).max() > h.ra_cusum(good, p).max()
    max_step = np.log(2 / (1 - p + 2 * p)).max()          # largest single-death increment
    assert h.ra_cusum(bad, p, h=4.5).max() <= 4.5 + max_step + 1e-9


# --------------------------------------------------------------------------- epidemiology
def test_epicurve_zero_fills():
    s = h.epicurve(["2024-01-01", "2024-01-01", "2024-01-03"])
    assert s.tolist() == [2, 0, 1]
    assert s.index[0] == pd.Timestamp("2024-01-01")


def test_serial_interval_sums_to_one():
    w = h.discretised_serial_interval(5.0, 2.0, 30)
    assert w.sum() == pytest.approx(1.0) and len(w) == 30
    assert np.argmax(w) + 1 in (4, 5)


@pytest.mark.parametrize("growth", [1.0, 1.1, 0.9])
def test_estimate_rt_recovers_growth_with_one_day_serial_interval(growth):
    inc = 1e6 * growth ** np.arange(60)   # large counts so the Gamma(1, 5) prior is negligible
    rt = h.estimate_rt(inc, [1.0], window=7)
    assert rt["rt"].iloc[-1] == pytest.approx(growth, rel=0.01)
    assert (rt["lower"] <= rt["rt"]).all() and (rt["rt"] <= rt["upper"]).all()


def test_reference_flags():
    assert h.reference_flags([3.0, 4.5, 6.0], 3.5, 5.0).tolist() == ["L", "", "H"]
