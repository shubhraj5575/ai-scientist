"""Construction heuristics: produce an initial tour (no guarantee of quality)."""
from __future__ import annotations

import numpy as np

from .instance import Instance


def nearest_neighbor(inst: Instance, start: int = 0) -> list[int]:
    """Classic nearest-neighbour tour. O(n^2) with matrix, O(n * k) w/ kNN lists."""
    n = inst.n
    D = inst.D
    visited = np.zeros(n, dtype=bool)
    tour = [start]
    visited[start] = True
    cur = start
    for _ in range(n - 1):
        row = D[cur].copy()
        row[visited] = np.inf
        nxt = int(np.argmin(row))
        tour.append(nxt)
        visited[nxt] = True
        cur = nxt
    return tour


def random_tour(inst: Instance, rng: np.random.Generator) -> list[int]:
    t = np.arange(inst.n)
    rng.shuffle(t)
    return t.tolist()


def greedy_edge(inst: Instance) -> list[int]:
    """Kruskal-style: add cheapest edges keeping degrees<=2, no premature cycle.

    O(n^2 log n); produces the classic 'greedy' baseline tour.
    """
    n = inst.n
    if n < 4:
        return random_tour(inst, np.random.default_rng(0))
    iu, ju = np.triu_indices(n, k=1)
    w = inst.D[iu, ju]
    order = np.argsort(w, kind="stable")
    deg = np.zeros(n, dtype=np.int8)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    adj: dict[int, list[int]] = {}
    edges_needed = n  # closing edge included
    for e in order:
        a, b = int(iu[e]), int(ju[e])
        if deg[a] >= 2 or deg[b] >= 2:
            continue
        ra, rb = find(a), find(b)
        if ra != rb or edges_needed == 1:
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
            deg[a] += 1
            deg[b] += 1
            parent[ra] = rb
            edges_needed -= 1
            if edges_needed == 0:
                break

    # walk the degree-2 graph from node 0
    tour = [0]
    prev = None
    cur = 0
    while True:
        nbrs = adj[cur]
        nxt = nbrs[0] if nbrs[0] != prev else nbrs[1]
        if nxt == 0:
            break
        tour.append(nxt)
        prev, cur = cur, nxt
        if len(tour) == n:
            break
    return tour


def cheapest_insertion(inst: Instance, rng: np.random.Generator) -> list[int]:
    """Start from 2 cities, repeatedly insert city with min insertion cost. O(n^3/6) vectorised."""
    n = inst.n
    D = inst.D
    perm = rng.permutation(n)
    tour = [int(perm[0]), int(perm[1])]
    remaining = set(int(c) for c in perm[2:])
    while remaining:
        rem = np.fromiter(remaining, dtype=np.int64)
        t = np.array(tour)
        nxt = np.roll(t, -1)
        # cost[c, p]: inserting c between t[p] and nxt[p]
        base = D[t, nxt]
        cost = D[t][:, rem] + D[nxt][:, rem] - base[:, None]   # (m, |rem|)
        best_pos, best_c = np.unravel_index(np.argmin(cost), cost.shape)
        c = int(rem[best_c])
        p = int(best_pos)
        tour.insert(p + 1, c)
        remaining.discard(c)
    return tour


CONSTRUCTIONS = {
    "nn": lambda inst, rng: nearest_neighbor(inst),
    "greedy": lambda inst, rng: greedy_edge(inst),
    "random": lambda inst, rng: random_tour(inst, rng),
    "cheapest_ins": lambda inst, rng: cheapest_insertion(inst, rng),
}
