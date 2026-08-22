import numpy as np

from ais.domains.tsp.algorithms import run_ils, run_plain_ls
from ais.domains.tsp.construction import CONSTRUCTIONS
from ais.domains.tsp.exact import held_karp_length
from ais.domains.tsp.instance import generate
from ais.domains.tsp.localsearch import TourState, run_local_search
from ais.domains.tsp.perturb import double_bridge


def _valid(tour, n):
    return sorted(tour) == list(range(n))


def test_constructions_produce_valid_tours():
    inst = generate("uniform", 25, 0)
    rng = np.random.default_rng(0)
    for name, fn in CONSTRUCTIONS.items():
        t = fn(inst, rng)
        assert _valid(t, inst.n), name


def test_local_search_never_worsens_and_converges():
    inst = generate("uniform", 40, 2)
    rng = np.random.default_rng(1)
    for ops in (("two_opt",), ("or_opt",), ("two_opt", "or_opt")):
        st = TourState(inst, CONSTRUCTIONS["random"](inst, rng), nl_k=16)
        l0 = st.length()
        run_local_search(st, ops)
        assert st.length() <= l0 + 1e-9
        assert _valid(st.tour, inst.n)


def test_two_opt_local_optimum_is_real():
    """After convergence, full O(n^2) scan finds no improving 2-move."""
    inst = generate("uniform", 30, 5)
    rng = np.random.default_rng(7)
    st = TourState(inst, CONSTRUCTIONS["random"](inst, rng), nl_k=None)
    from ais.domains.tsp.localsearch import two_opt
    two_opt(st)
    D, tour, n = st.Dl, st.tour, st.n
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            a, b_, c, d = tour[i - 1], tour[i], tour[j], tour[(j + 1) % n]
            assert D[a][b_] + D[c][d] - D[a][c] - D[b_][d] <= 1e-9


def test_double_bridge_preserves_permutation():
    rng = np.random.default_rng(3)
    t = list(range(50))
    rng.shuffle(t)
    t2 = double_bridge(t, rng)
    assert sorted(t2) == sorted(t) and t2 != t


def test_ils_beats_single_ls_at_fixed_budget():
    inst = generate("uniform", 60, 4)
    cfg_plain = dict(construction="nn", ls_operators=("two_opt",),
                     nl_k=None, perturbation="none")
    cfg_ils = dict(construction="nn", ls_operators=("two_opt",),
                   nl_k=None, perturbation="double_bridge",
                   acceptance="better")
    r_plain = run_plain_ls(inst, "nn", ("two_opt",), None, seed=0)
    r_ils = run_ils(inst, type(cfg_ils, ()), 1.5, seed=0) if False else None
    from ais.domains.tsp.algorithms import ILSConfig
    r_ils = run_ils(inst, ILSConfig(**{
        k: v for k, v in cfg_ils.items() if k != "perturbation"} |
        {"perturbation": "double_bridge"}), 1.5, seed=0)
    assert r_ils.length < r_plain.length


def test_small_instance_ils_reaches_optimum_often():
    inst = generate("uniform", 10, 1)
    opt = held_karp_length(inst)
    from ais.domains.tsp.algorithms import ILSConfig
    hits = 0
    trials = 3
    for s in range(trials):
        r = run_ils(inst, ILSConfig(), 1.0, seed=s)
        if abs(r.length - opt) < 1e-6:
            hits += 1
    assert hits >= 1
