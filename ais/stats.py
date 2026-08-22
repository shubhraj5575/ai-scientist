"""Statistical utilities (self-contained; no scipy dependency).

Implements:
  * paired t-test (p-value via regularised incomplete beta)
  * Wilcoxon signed-rank test (normal approximation w/ tie correction)
  * percentile bootstrap CI for a mean
  * Holm-Bonferroni step-down correction
  * Cohen's dz effect size for paired designs

All functions operate on paired difference vectors d = x - y where x is the
candidate metric and y the baseline metric on shared (instance, seed) pairs.
"""
from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------------------
# special functions
# ---------------------------------------------------------------------------

def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction for incomplete beta (Numerical Recipes 3rd ed. 6.4)."""
    MAXIT, EPS, FPMIN = 200, 3e-16, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < EPS:
            break
    return h


def betainc_reg(a: float, b: float, x: float) -> float:
    """Regularised incomplete beta I_x(a,b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    ln_bt = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log(1.0 - x))
    bt = math.exp(ln_bt)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_sf_two_sided(t: float, df: int) -> float:
    """Two-sided p-value for |t| with df dof."""
    if df <= 0:
        return float("nan")
    x = df / (df + t * t)
    return betainc_reg(df / 2.0, 0.5, x)


def norm_sf_two_sided(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


# ---------------------------------------------------------------------------
# descriptive
# ---------------------------------------------------------------------------

def mean_ci_bootstrap(x: np.ndarray, B: int = 10_000, seed: int = 0,
                      level: float = 0.95) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    n = len(x)
    idx = rng.integers(0, n, size=(B, n))
    means = x[idx].mean(axis=1)
    lo_q = (1 - level) / 2 * 100
    hi_q = (1 + level) / 2 * 100
    return tuple(np.percentile(means, [lo_q, hi_q]))  # type: ignore


# ---------------------------------------------------------------------------
# tests on paired differences
# ---------------------------------------------------------------------------

def paired_ttest(d: np.ndarray) -> tuple[float, float]:
    """Returns (t_stat, two_sided_p)."""
    d = np.asarray(d, dtype=float)
    n = len(d)
    sd = d.std(ddof=1)
    if sd == 0:
        return (0.0, 1.0 if d.mean() == 0 else 0.0)
    t = d.mean() / (sd / math.sqrt(n))
    return float(t), t_sf_two_sided(abs(t), n - 1)


def wilcoxon_signed_rank(d: np.ndarray) -> tuple[float, float]:
    """Wilcoxon signed-rank, normal approximation with tie/zero handling.

    Returns (z_stat, two_sided_p). Drops exact zeros (Pratt convention).
    """
    d = np.asarray(d, dtype=float)
    d = d[np.abs(d) > 1e-12]
    n = len(d)
    if n == 0:
        return 0.0, 1.0
    ranks = _midranks(np.abs(d))
    w_plus = ranks[d > 0].sum()
    mu = n * (n + 1) / 4.0
    # tie correction
    _, counts = np.unique(np.abs(d), return_counts=True)
    tie_term = (counts * (counts ** 2 - 1)).sum() / 48.0
    var = n * (n + 1) * (2 * n + 1) / 24.0 - tie_term
    if var <= 0:
        return 0.0, 1.0
    z = (w_plus - mu) / math.sqrt(var)
    if z > 0:  # continuity correction toward mean
        z -= 0.5 / math.sqrt(var)
    else:
        z += 0.5 / math.sqrt(var)
    return float(z), norm_sf_two_sided(z)


def _midranks(x: np.ndarray) -> np.ndarray:
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(len(x), dtype=float)
    sx = x[order]
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and sx[j + 1] == sx[i]:
            j += 1
        ranks[order[i : j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return ranks


def cohens_dz(d: np.ndarray) -> float:
    d = np.asarray(d, dtype=float)
    sd = d.std(ddof=1)
    return float(d.mean() / sd) if sd > 0 else float("inf") * float(np.sign(d.mean()))


# ---------------------------------------------------------------------------
# multiple comparisons
# ---------------------------------------------------------------------------

def holm_bonferroni(pvals: list[float], alpha: float = 0.05) -> list[bool]:
    """Step-down Holm. Returns list of reject-decisions aligned with input."""
    m = len(pvals)
    if m == 0:
        return []
    order = sorted(range(m), key=lambda i: pvals[i])
    rejected = [False] * m
    for rank, idx in enumerate(order):
        thresh = alpha / (m - rank)
        if pvals[idx] <= thresh:
            rejected[idx] = True
        else:
            break
    return rejected


# ---------------------------------------------------------------------------
# high-level analysis of a batch vs baseline
# ---------------------------------------------------------------------------

def analyse_paired(candidate_vals: dict, baseline_vals: dict,
                   bootstrap_B: int = 10_000) -> dict:
    """candidate/baseline vals: {(instance_name, seed): excess_pct}.

    Returns summary statistics + test results on paired differences.
    Positive mean_delta_pp means candidate has LOWER excess than baseline.
    """
    keys = sorted(set(candidate_vals) & set(baseline_vals))
    assert keys, "no overlapping (instance, seed) pairs"
    cand = np.array([candidate_vals[k] for k in keys])
    base = np.array([baseline_vals[k] for k in keys])
    d = base - cand          # positive => candidate better
    t, tp = paired_ttest(d)
    z, wp = wilcoxon_signed_rank(d)
    ci_lo, ci_hi = mean_ci_bootstrap(d, B=bootstrap_B)
    return {
        "n_pairs": len(keys),
        "pairs": keys,
        "cand_mean": float(cand.mean()),
        "base_mean": float(base.mean()),
        "mean_delta_pp": float(d.mean()),
        "ci_lo": float(ci_lo),
        "ci_hi": float(ci_hi),
        "cohens_dz": cohens_dz(d),
        "t_stat": t,
        "ttest_p": tp,
        "wilcoxon_z": z,
        "wilcoxon_p": wp,
        "win_rate": float((d > 0).mean()),
    }
