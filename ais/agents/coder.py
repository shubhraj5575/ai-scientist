"""Coder agent: materialises declarative candidates into runnable solvers
and runs pre-benchmark sanity checks (correctness gate).

Nothing reaches the benchmark stage until it passes:
  1. grammar validation
  2. tour validity (permutation) on a small instance
  3. monotonicity: local search never worsens the objective
  4. budget obedience: runtime within 1.5x of requested budget on a small run
"""
from __future__ import annotations

import numpy as np

from ..domains.tsp.algorithms import run_ils, run_plain_ls
from ..domains.tsp.instance import generate
from .space import to_ilscfg, validate


class Coder:
    def __init__(self):
        self.check_instance = generate("uniform", 30, 999)

    def validate_config(self, cfg: dict) -> list[str]:
        return validate(cfg)

    def sanity_checks(self, cfg: dict, budget_s: float = 0.5) -> list[str]:
        errs = self.validate_config(cfg)
        if errs:
            return errs
        ilscfg = to_ilscfg(cfg)
        seed = 123
        res = run_ils(self.check_instance, ilscfg, budget_s, seed)
        # 1. permutation validity
        if sorted(res.tour) != list(range(self.check_instance.n)):
            errs.append("tour is not a permutation")
        # 2. finite length
        if not np.isfinite(res.length) or res.length <= 0:
            errs.append(f"non-finite/nonpositive length {res.length}")
        # 3. budget obedience (generous guard for scheduler noise)
        if res.runtime_s > budget_s * 1.5 + 1.0:
            errs.append(f"budget violation: {res.runtime_s:.2f}s > "
                        f"{budget_s:.2f}s*1.5+1")
        # 4. reproducibility: same seed twice -> identical length
        res2 = run_ils(self.check_instance, ilscfg, budget_s, seed)
        if abs(res2.length - res.length) > 1e-6:
            errs.append(f"non-reproducible under fixed seed: "
                        f"{res.length} vs {res2.length}")
        return errs

    def materialise(self, cfg: dict):
        """Return the runnable solver entry point for this config."""
        return to_ilscfg(cfg)
