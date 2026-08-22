"""Exact TSP solver: Held-Karp dynamic programming (reference values only).

Scope: n <= 16 (memory 2^n * n float64 = 1 MB at n=16; time is the limit).
We need only the optimal LENGTH (no tour reconstruction) for use as a
reference value in quality metrics.
"""
from __future__ import annotations

import numpy as np

from .instance import Instance


def held_karp_length(inst: Instance) -> float:
    """Optimal tour length for inst via subset DP over tours rooted at city 0."""
    if inst.n > 18:
        raise ValueError("held_karp limited to n<=18")
    D = inst.D
    n = inst.n
    m = 1 << n
    INF = np.inf
    dp = np.full((m, n), INF, dtype=np.float64)
    dp[1, 0] = 0.0

    # Iterate subsets containing city 0 in increasing numeric order.
    # Numeric order guarantees S ^ (1<<j) < S when j not in S, so dp is ready.
    for S in range(1, m):
        if not (S & 1):
            continue
        row = dp[S]
        for j in range(n):
            v = row[j]
            if v == INF:
                continue
            Dj = D[j]
            free = (~S) & (m - 1)
            while free:
                k_bit = free & (-free)
                k = k_bit.bit_length() - 1
                cand = v + Dj[k]
                S2 = S | k_bit
                if cand < dp[S2, k]:
                    dp[S2, k] = cand
                free ^= k_bit
    # close the tour: cheapest final city j -> start city 0
    last_row = dp[m - 1]
    D0 = D[0]
    return float(min(last_row[j] + D0[j] for j in range(n)))


def brute_force_length(inst: Instance) -> float:
    """Exhaustive optimum by permutation enumeration (n <= 9, for testing)."""
    import itertools
    n = inst.n
    assert n <= 9
    D = inst.D
    best = np.inf
    others = range(1, n)
    for perm in itertools.permutations(others):
        tour = (0,) + perm
        L = sum(D[tour[i], tour[(i + 1) % n]] for i in range(n))
        if L < best:
            best = L
    return float(best)
