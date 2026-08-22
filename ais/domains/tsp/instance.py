"""TSP instances: representation, deterministic generators, distance matrices.

Design notes
------------
* Instances are generated from (kind, n, seed) so they are perfectly
  reproducible; the digest of the coordinate array is stored in the DB.
* Distance matrix is materialised for n <= 1500 and computed on the fly
  above that (memory guard).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Iterator, Literal

import numpy as np

from ...utils import stable_digest

InstanceKind = Literal["uniform", "clustered", "grid"]

MAX_MATRIX_N = 1500


def _dist_matrix(coords: np.ndarray) -> np.ndarray:
    diff = coords[:, None, :] - coords[None, :, :]
    return np.sqrt((diff * diff).sum(-1))


@dataclass(eq=False)
class Instance:
    name: str
    kind: str
    n: int
    seed: int
    coords: np.ndarray            # (n, 2) float64
    params: dict = field(default_factory=dict)
    _D: np.ndarray | None = field(default=None, repr=False)
    _Dlist: list | None = field(default=None, repr=False)
    _nl_cache: dict = field(default_factory=dict, repr=False)

    def __post_init__(self):
        if self.n <= MAX_MATRIX_N:
            self._D = _dist_matrix(self.coords)

    # -- distances ---------------------------------------------------------
    @property
    def D(self) -> np.ndarray:
        """Full distance matrix (materialises lazily if needed)."""
        if self._D is None:
            self._D = _dist_matrix(self.coords)
        return self._D

    def d_list(self) -> list:
        """Cached python-list view of D (fast scalar access in hot loops)."""
        if self._Dlist is None:
            self._Dlist = self.D.tolist()
        return self._Dlist

    def d(self, i: int, j: int) -> float:
        if self._D is not None:
            return float(self._D[i, j])
        diff = self.coords[i] - self.coords[j]
        return math.sqrt(float(diff @ diff))

    def dist_many(self, i: int, js: np.ndarray) -> np.ndarray:
        c = self.coords[i]
        diff = self.coords[js] - c
        return np.sqrt((diff * diff).sum(-1))

    def k_nearest(self, k: int) -> np.ndarray:
        """(n, k) array of each city's k nearest neighbours, excluding itself."""
        Dm = self.D
        order = np.argsort(Dm, axis=1)[:, 1 : k + 1]
        return order.astype(np.int32)

    def k_nearest_lists(self, k: int | None) -> list:
        """Cached python-list neighbour lists for hot loops (k=None -> full)."""
        kk = self.n - 1 if k is None else min(k, self.n - 1)
        if kk not in self._nl_cache:
            arr = self.k_nearest(kk) if kk >= 0 else np.zeros((self.n, 0), np.int32)
            self._nl_cache[kk] = [row.tolist() for row in arr]
        return self._nl_cache[kk]

    # -- tours ---------------------------------------------------------------
    def tour_length(self, tour: np.ndarray | list[int]) -> float:
        t = np.asarray(tour, dtype=np.int64)
        if self._D is not None:
            idx = self._D[t, np.roll(t, -1)]
        else:
            nxt = np.roll(t, -1)
            diff = self.coords[t] - self.coords[nxt]
            idx = np.sqrt((diff * diff).sum(-1))
        return float(idx.sum())

    # -- identity ------------------------------------------------------------
    def digest(self) -> str:
        return stable_digest({"coords": self.coords, "kind": self.kind,
                              "seed": self.seed, "params": self.params})


# ---------------------------------------------------------------------------
# Generators (deterministic given kind/n/seed)
# ---------------------------------------------------------------------------

def generate(kind: str, n: int, seed: int) -> Instance:
    rng = np.random.default_rng(seed)
    if kind == "uniform":
        coords = rng.uniform(0.0, 1000.0, size=(n, 2))
        params = {"box": 1000}
    elif kind == "clustered":
        k = max(2, n // 25)
        centers = rng.uniform(0, 1000, size=(k, 2))
        assign = rng.integers(0, k, size=n)
        spread = 60.0 + 40 * ((seed % 3) == 0)   # seed-dependent tightness mix
        coords = centers[assign] + rng.normal(0, spread, size=(n, 2))
        params = {"k": int(k), "spread": spread, "box": 1000}
    elif kind == "grid":
        side = math.isqrt(n - 1) + 1
        xs = np.linspace(0, 1000, side)
        base = np.array([(x, y) for y in xs for x in xs])[:n]
        coords = base + rng.uniform(-8, 8, size=base.shape)
        params = {"side": int(side), "jitter": 8, "box": 1000}
    else:
        raise ValueError(f"unknown instance kind {kind!r}")
    return Instance(
        name=f"{kind}_n{n}_s{seed}", kind=kind, n=int(n), seed=int(seed),
        coords=np.ascontiguousarray(coords, dtype=np.float64), params=params,
    )


def suite(kind_ns_seeds: list[tuple[str, list[int], list[int]]]) -> list[Instance]:
    out: list[Instance] = []
    for kind, ns, seeds in kind_ns_seeds:
        for n in ns:
            for s in seeds:
                out.append(generate(kind, n, s))
    return out


@lru_cache(maxsize=256)
def get_instance(kind: str, n: int, seed: int) -> Instance:
    """Cached accessor — instances are immutable once built."""
    return generate(kind, int(n), int(seed))


# Round coordinates to TSPLIB-style integers? No: we keep full float precision
# to avoid EUC_2D rounding ambiguity; documented in DECISIONS.md D7.
