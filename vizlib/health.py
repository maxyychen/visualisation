"""
vizlib.health: tested statistics behind the healthcare charts.

* Survival: Kaplan-Meier with Greenwood confidence bands, median survival, RMST.
* Quality improvement: run-chart rules, p- and u-chart limits, funnel-plot limits,
  VLAD and risk-adjusted Bernoulli CUSUM.
* Epidemiology: epidemic-curve binning, discretised serial interval, time-varying
  reproduction number (Cori et al. 2013).
* Patient level: reference-range flags.

Every function is plain numpy/pandas/scipy and has unit tests in tests/test_health.py.
Use de-identified data: executed notebooks store their outputs.

References
----------
Perla, Provost & Murray (2011) The run chart. BMJ Qual Saf 20:46-51.
Mohammed, Worthington & Woodall (2008) Plotting basic control charts. Qual Saf Health Care 17:137-145.
Spiegelhalter (2005) Funnel plots for comparing institutional performance. Stat Med 24:1185-1202.
Lovegrove et al. (1997) Variable life-adjusted display. Lancet 350:1128-1130.
Steiner, Cook & Farewell (2001) Risk-adjusted monitoring of binary surgical outcomes. Med Decis Making 21:163-169.
Cori, Ferguson, Fraser & Cauchemez (2013) Time-varying reproduction numbers. Am J Epidemiol 178:1505-1512.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


# --------------------------------------------------------------------------- survival
def kaplan_meier(time, event, alpha: float = 0.05) -> pd.DataFrame:
    """Kaplan-Meier estimate at each distinct event/censoring time.

    `event` is 1 for the event (death, relapse) and 0 for censored. The confidence band
    uses Greenwood's variance on the log(-log S) scale, which keeps it inside [0, 1].
    The table starts at time 0: survival is 1 unless events occur at time 0 itself, in which
    case the time-0 row already reflects them.
    """
    t = np.asarray(time, dtype=float)
    e = np.asarray(event, dtype=int)
    if t.shape != e.shape or t.size == 0:
        raise ValueError("time and event must be non-empty and the same length")
    rows, s, greenwood = [], 1.0, 0.0
    z = stats.norm.ppf(1 - alpha / 2)
    n_at_risk = t.size
    for u in np.unique(t):
        here = t == u
        d = int(e[here].sum())
        c = int(here.sum()) - d
        if d:
            s *= 1 - d / n_at_risk
            if n_at_risk > d:
                greenwood += d / (n_at_risk * (n_at_risk - d))
        se = s * np.sqrt(greenwood)
        if 0 < s < 1:
            log_se = np.sqrt(greenwood) / abs(np.log(s))
            lo, hi = s ** np.exp(z * log_se), s ** np.exp(-z * log_se)
        else:
            lo = hi = s
        rows.append((u, n_at_risk, d, c, s, se, lo, hi))
        n_at_risk -= d + c
    out = pd.DataFrame(rows, columns=["time", "at_risk", "events", "censored", "survival",
                                      "se", "ci_lower", "ci_upper"])
    if out["time"].iloc[0] > 0:  # add the starting point; keep real time-0 events if present
        start = pd.DataFrame([dict(time=0.0, at_risk=t.size, events=0, censored=0, survival=1.0,
                                   se=0.0, ci_lower=1.0, ci_upper=1.0)])
        out = pd.concat([start, out], ignore_index=True)
    return out


def survival_at(km: pd.DataFrame, times) -> np.ndarray:
    """Step-function lookup of S(t) from a kaplan_meier() table."""
    idx = np.searchsorted(km["time"].values, np.asarray(times, dtype=float), side="right") - 1
    return km["survival"].values[np.clip(idx, 0, None)]


def at_risk(time, times) -> np.ndarray:
    """Number still at risk (time >= t) at each of `times`, for a numbers-at-risk table."""
    t = np.sort(np.asarray(time, dtype=float))
    return t.size - np.searchsorted(t, np.asarray(times, dtype=float), side="left")


def median_survival(km: pd.DataFrame) -> float:
    """First time at which S(t) <= 0.5 (NaN if never reached)."""
    hit = km.loc[km["survival"] <= 0.5, "time"]
    return float(hit.iloc[0]) if len(hit) else float("nan")


def rmst(km: pd.DataFrame, tau: float) -> float:
    """Restricted mean survival time: area under the KM step curve from 0 to tau."""
    t = np.append(km["time"].values, np.inf)
    s = km["survival"].values
    area = 0.0
    for i in range(len(s)):
        lo, hi = t[i], min(t[i + 1], tau)
        if hi > lo:
            area += s[i] * (hi - lo)
        if t[i + 1] >= tau:
            break
    return float(area)


# --------------------------------------------------------------------------- quality improvement
def run_chart_signals(values, center: float | None = None, shift: int = 6, trend: int = 5) -> dict:
    """Run-chart rules (Perla, Provost & Murray 2011).

    * shift: >= `shift` consecutive points on one side of the median (points on it are skipped)
    * trend: >= `trend` consecutive points all going up or all going down (ties are skipped)
    * runs: number of runs about the median, flagged if outside the ~95% range expected by chance

    Returns indices of points in a shift or trend, the run count and its expected range.
    """
    y = np.asarray(values, dtype=float)
    med = float(np.median(y)) if center is None else float(center)
    side = np.sign(y - med)
    useful = np.flatnonzero(side != 0)

    shift_idx = set()
    start = 0
    for k in range(1, len(useful) + 1):
        if k == len(useful) or side[useful[k]] != side[useful[start]]:
            if k - start >= shift:
                shift_idx.update(useful[start:k].tolist())
            start = k

    trend_idx = set()
    keep = [0] + [i for i in range(1, len(y)) if y[i] != y[i - 1]]
    direction = np.sign(np.diff(y[keep]))
    start = 0
    for k in range(1, len(direction) + 1):
        if k == len(direction) or direction[k] != direction[start]:
            if k - start + 1 >= trend:
                trend_idx.update(keep[start:k + 1])
            start = k

    runs = 1 + int(np.sum(side[useful][1:] != side[useful][:-1])) if len(useful) else 0
    n1, n2 = int(np.sum(side > 0)), int(np.sum(side < 0))
    n = n1 + n2
    mean = 1 + 2 * n1 * n2 / n if n else 0.0
    var = 2 * n1 * n2 * (2 * n1 * n2 - n) / (n ** 2 * (n - 1)) if n > 1 else 0.0
    lo, hi = mean - 1.96 * np.sqrt(var), mean + 1.96 * np.sqrt(var)
    return {"median": med, "shift": sorted(shift_idx), "trend": sorted(trend_idx),
            "runs": runs, "runs_expected": (float(np.ceil(lo)), float(np.floor(hi))),
            "too_few_runs": bool(runs < lo), "too_many_runs": bool(runs > hi)}


def p_chart(events, n, sigma: float = 3.0) -> pd.DataFrame:
    """p-chart (proportions): centre p-bar and per-point limits p-bar +/- sigma*sqrt(p(1-p)/n_i)."""
    x, n = np.asarray(events, dtype=float), np.asarray(n, dtype=float)
    p = x / n
    pbar = x.sum() / n.sum()
    half = sigma * np.sqrt(pbar * (1 - pbar) / n)
    lcl, ucl = np.clip(pbar - half, 0, 1), np.clip(pbar + half, 0, 1)
    return pd.DataFrame({"p": p, "center": pbar, "lcl": lcl, "ucl": ucl,
                         "signal": (p > ucl) | (p < lcl)})


def u_chart(counts, exposure, sigma: float = 3.0) -> pd.DataFrame:
    """u-chart (rates, e.g. falls per 1,000 bed-days): u-bar +/- sigma*sqrt(u-bar/exposure_i)."""
    c, a = np.asarray(counts, dtype=float), np.asarray(exposure, dtype=float)
    u = c / a
    ubar = c.sum() / a.sum()
    half = sigma * np.sqrt(ubar / a)
    lcl, ucl = np.clip(ubar - half, 0, None), ubar + half
    return pd.DataFrame({"u": u, "center": ubar, "lcl": lcl, "ucl": ucl,
                         "signal": (u > ucl) | (u < lcl)})


def funnel_limits(target: float, n, level: float = 0.998, exact: bool = True):
    """Lower/upper funnel limits for a proportion with target `target` at sample sizes `n`.

    exact=True uses binomial quantiles with Spiegelhalter's (2005) interpolation, which
    matters for small n; exact=False is the normal approximation.
    """
    n = np.asarray(n, dtype=float)
    z = stats.norm.ppf(1 - (1 - level) / 2)
    if not exact:
        half = z * np.sqrt(target * (1 - target) / n)
        return np.clip(target - half, 0, 1), np.clip(target + half, 0, 1)

    def limit(prob):
        r = stats.binom.ppf(prob, n, target)
        below = stats.binom.cdf(r - 1, n, target)
        at = stats.binom.pmf(r, n, target)
        alpha = np.where(at > 0, (prob - below) / np.where(at > 0, at, 1), 0)
        return np.clip((r - 1 + alpha) / n, 0, 1)

    return limit((1 - level) / 2), limit(1 - (1 - level) / 2)


def vlad(observed, expected_risk) -> np.ndarray:
    """Variable life-adjusted display: cumulative (expected - observed) deaths.

    Rising = fewer deaths than the case mix predicts ("statistical lives saved").
    """
    o = np.asarray(observed, dtype=float)
    p = np.asarray(expected_risk, dtype=float)
    return np.cumsum(p - o)


def ra_cusum(observed, expected_risk, odds_ratio: float = 2.0, h: float | None = None,
             reset: bool = True) -> np.ndarray:
    """Risk-adjusted Bernoulli CUSUM (Steiner et al.) testing for odds of death multiplied by
    `odds_ratio`. Each patient adds log(R / (1 - p + R p)) if they die and
    log(1 / (1 - p + R p)) if they survive; the chart is floored at 0. With `h` and
    reset=True the chart restarts at 0 after crossing the threshold.
    """
    y = np.asarray(observed, dtype=float)
    p = np.asarray(expected_risk, dtype=float)
    denom = 1 - p + odds_ratio * p
    w = np.where(y == 1, np.log(odds_ratio / denom), np.log(1 / denom))
    out, s = np.empty_like(w), 0.0
    for i, wi in enumerate(w):
        s = max(0.0, s + wi)
        out[i] = s
        if h is not None and reset and s > h:
            s = 0.0
    return out


# --------------------------------------------------------------------------- epidemiology
def epicurve(onset_dates, freq: str = "D", start=None, end=None) -> pd.Series:
    """Counts of cases per period (zero-filled), indexed by period start."""
    d = pd.to_datetime(pd.Series(onset_dates))
    counts = d.dt.to_period(freq).value_counts().sort_index()
    lo = pd.Period(start, freq) if start is not None else counts.index.min()
    hi = pd.Period(end, freq) if end is not None else counts.index.max()
    full = pd.period_range(lo, hi, freq=freq)
    return counts.reindex(full, fill_value=0).rename("cases").set_axis(full.to_timestamp())


def discretised_serial_interval(mean: float, sd: float, max_days: int = 30) -> np.ndarray:
    """Gamma serial-interval distribution discretised to days 1..max_days (sums to 1)."""
    shape, scale = (mean / sd) ** 2, sd ** 2 / mean
    edges = np.arange(0, max_days + 1) + 0.5
    edges[0] = 0
    w = np.diff(stats.gamma.cdf(edges, shape, scale=scale))
    return w / w.sum()


def estimate_rt(incidence, serial_interval, window: int = 7, prior_shape: float = 1.0,
                prior_scale: float = 5.0, level: float = 0.95) -> pd.DataFrame:
    """Time-varying reproduction number (Cori et al. 2013).

    `serial_interval[k-1]` is the probability that the serial interval is k days. For each
    day t (from `window` on), the posterior of R over days t-window+1..t is
    Gamma(a + sum I_s, 1 / (1/b + sum Lambda_s)), with Lambda_s = sum_k I_{s-k} w_k.
    """
    inc = pd.Series(incidence, dtype=float)
    i = inc.values
    w = np.asarray(serial_interval, dtype=float)
    lam = np.array([np.dot(i[max(0, s - len(w)):s][::-1], w[:min(s, len(w))]) for s in range(len(i))])
    rows = []
    for t in range(window, len(i)):
        s = slice(t - window + 1, t + 1)
        shape = prior_shape + i[s].sum()
        scale = 1 / (1 / prior_scale + lam[s].sum())
        lo, hi = stats.gamma.ppf([(1 - level) / 2, 1 - (1 - level) / 2], shape, scale=scale)
        rows.append((inc.index[t], shape * scale, lo, hi))
    return pd.DataFrame(rows, columns=["date", "rt", "lower", "upper"]).set_index("date")


# --------------------------------------------------------------------------- patient level
def reference_flags(values, low: float, high: float) -> np.ndarray:
    """'L', 'H' or '' for each value against a reference range [low, high]."""
    v = np.asarray(values, dtype=float)
    return np.where(v < low, "L", np.where(v > high, "H", ""))
