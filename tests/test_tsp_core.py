import numpy as np

from ais.domains.tsp.exact import brute_force_length, held_karp_length
from ais.domains.tsp.instance import generate


def test_held_karp_matches_brute_force():
    for n in (5, 6, 7):
        for seed in range(2):
            inst = generate("uniform", n, seed)
            assert abs(held_karp_length(inst) - brute_force_length(inst)) < 1e-9


def test_instance_determinism():
    a = generate("uniform", 50, 3)
    b = generate("uniform", 50, 3)
    assert np.array_equal(a.coords, b.coords)
    assert a.digest() == b.digest()


def test_clustered_and_grid_generators_valid():
    for kind in ("clustered", "grid"):
        inst = generate(kind, 40, 1)
        assert inst.coords.shape == (40, 2)
        assert np.isfinite(inst.coords).all()
