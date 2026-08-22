"""Perturbation operators for Iterated Local Search."""
from __future__ import annotations

import numpy as np


def double_bridge(tour: list[int], rng: np.random.Generator) -> list[int]:
    """Classic double-bridge (4-opt) kick: split into 4 segments, rewire A C B D."""
    n = len(tour)
    if n < 8:
        return list(tour)
    cuts = sorted(rng.choice(np.arange(1, n), size=4, replace=False).tolist())
    a, b, c, d = cuts
    return tour[:a] + tour[b:c] + tour[a:b] + tour[c:]


def random_reversals(tour: list[int], rng: np.random.Generator, k: int) -> list[int]:
    """k random segment reversals (worsening allowed) — 'random k-exchange'."""
    n = len(tour)
    t = list(tour)
    if n < 5:
        return t
    for _ in range(k):
        i = int(rng.integers(0, n))
        j = int(rng.integers(0, n))
        if i > j:
            i, j = j, i
        if j - i + 1 <= n:
            seg_len = j - i + 1
            if 2 * seg_len <= n or True:
                # simple slice reversal on linear representation (may cut closing edge;
                # still yields a valid permutation tour — any reversal of a cyclic
                # sequence is a tour)
                t[i : j + 1] = t[i : j + 1][::-1]
    return t


def random_relocations(tour: list[int], rng: np.random.Generator, k: int,
                       max_seg: int = 3) -> list[int]:
    """k random Or-opt-style relocations of short segments to random anchors."""
    n = len(tour)
    t = list(tour)
    if n < 6:
        return t
    for _ in range(k):
        L = int(rng.integers(1, max_seg + 1))
        L = min(L, n - 2)
        p = int(rng.integers(0, n - L + 1))
        seg = t[p : p + L]
        rest = t[:p] + t[p + L :]
        ia = int(rng.integers(0, len(rest)))
        t = rest[:ia] + seg + rest[ia:]
    return t


PERTURBATIONS = {
    "double_bridge": lambda tour, rng, s: double_bridge(tour, rng),
    "reversals": lambda tour, rng, s: random_reversals(tour, rng, s),
    "relocations": lambda tour, rng, s: random_relocations(tour, rng, s),
}


def perturb(tour: list[int], kind: str, strength: int,
            rng: np.random.Generator) -> list[int]:
    if kind == "none":
        return list(tour)
    return PERTURBATIONS[kind](tour, rng, int(strength))
