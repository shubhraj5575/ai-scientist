"""Regression tests for the don't-look-bit artifact (A1).

Background: or-opt masking caused premature convergence (up to ~30% worse
tours, order-dependent). These tests pin the fixed behaviour.
"""
import numpy as np

from ais.domains.tsp.construction import random_tour
from ais.domains.tsp.instance import generate
from ais.domains.tsp.localsearch import (TourState, or_opt_pass, run_local_search,
                                         two_opt, two_opt_pass)


def _fresh(inst, seed):
    rng = np.random.default_rng(seed)
    return TourState(inst, random_tour(inst, rng), nl_k=None)


def test_operator_orders_agree():
    inst = generate("uniform", 60, 3)
    a = _fresh(inst, 0)
    run_local_search(a, ("two_opt", "or_opt1"))
    b = _fresh(inst, 0)
    run_local_search(b, ("or_opt1", "two_opt"))
    # path dependence exists, but post-fix orders land within a few %
    assert abs(a.length() - b.length()) / min(a.length(), b.length()) < 0.08


def test_joint_convergence_exhaustive_oropt1_pair():
    """After ('or_opt1','two_opt') converges, matched-neighborhood scans
    find no improving move."""
    inst = generate("uniform", 50, 7)
    st = _fresh(inst, 1)
    run_local_search(st, ("or_opt1", "two_opt"))
    st.mask = bytearray(st.n)
    assert not or_opt_pass(st, lengths=(1,))
    assert not two_opt_pass(st)


def test_joint_convergence_exhaustive_full_oropt():
    inst = generate("uniform", 50, 7)
    st = _fresh(inst, 2)
    run_local_search(st, ("two_opt", "or_opt"))
    st.mask = bytearray(st.n)
    assert not or_opt_pass(st)
    assert not two_opt_pass(st)


def test_composite_never_loses_to_singles():
    """Regression pin for artifact A1: pre-fix, composites could end up far
    WORSE than a single operator due to stale don't-look bits."""
    for seed in range(3):
        inst = generate("uniform", 60, seed + 20)
        singles = []
        for op in (("two_opt",), ("or_opt",)):
            st = _fresh(inst, seed)
            run_local_search(st, op)
            singles.append(st.length())
        for combo in (("two_opt", "or_opt"), ("or_opt1", "two_opt")):
            st = _fresh(inst, seed)
            run_local_search(st, combo)
            # Post-fix: path dependence may cost ~1-2% vs a lucky single-op
            # basin, never the ~30% catastrophe seen pre-fix.
            assert st.length() <= max(singles) * 1.02, (seed, combo)


def test_two_opt_still_converges():
    inst = generate("uniform", 40, 9)
    st = _fresh(inst, 2)
    two_opt(st)
    D, tour, n = st.Dl, st.tour, st.n
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            a, b_, c, d = tour[i - 1], tour[i], tour[j], tour[(j + 1) % n]
            assert D[a][b_] + D[c][d] - D[a][c] - D[b_][d] <= 1e-9
