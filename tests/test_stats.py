import numpy as np

from ais.stats import (analyse_paired, cohens_dz, holm_bonferroni,
                       mean_ci_bootstrap, paired_ttest, wilcoxon_signed_rank)


def test_paired_ttest_detects_shift():
    rng = np.random.default_rng(0)
    x = rng.normal(10, 1, 40)
    y = x - 1.0 + rng.normal(0, .2, 40)   # candidate better by ~1 with noise
    t, p = paired_ttest(x - y)
    assert p < 0.001


def test_wilcoxon_symmetric_null_not_significant():
    rng = np.random.default_rng(1)
    d = rng.normal(0, 1, 50)
    z, p = wilcoxon_signed_rank(d)
    assert p > 0.05


def test_wilcoxon_detects_consistent_improvement():
    d = np.array([0.5, 0.7, 0.3, 0.9, 0.4, 0.6, 0.8, 0.2, 1.1, 0.5])
    z, p = wilcoxon_signed_rank(d)
    assert p < 0.01


def test_bootstrap_ci_covers_mean():
    rng = np.random.default_rng(2)
    d = rng.normal(2.0, 3.0, 200)
    lo, hi = mean_ci_bootstrap(d, B=4000, seed=0)
    assert lo < 2.0 < hi


def test_holm_correction_conservative_vs_raw():
    pvals = [0.001, 0.03, 0.04, 0.20]
    rej = holm_bonferroni(pvals, alpha=0.05)
    raw = [p < 0.05 for p in pvals]
    assert all(not (r and not w) for r, w in zip(rej, raw))
    # step-down: reject smallest at alpha/m; stop at first non-rejection
    assert rej == [True, False, False, False]


def test_analyse_paired_end_to_end():
    rng = np.random.default_rng(5)
    keys = [(f"inst_{i}", s) for i in range(6) for s in range(8)]
    base = {k: rng.normal(8, 1) for k in keys}
    cand = {k: base[k] - 0.5 + rng.normal(0, .3) for k in keys}
    out = analyse_paired(cand, base)
    assert out["n_pairs"] == len(keys)
    assert out["mean_delta_pp"] > 0.25
    assert out["wilcoxon_p"] < 0.01
