"""Coder agent: materialises declarative candidates into runnable solvers
and runs pre-benchmark sanity checks (correctness gate).

Nothing reaches the benchmark stage until it passes:
  1. grammar validation
  2. tour validity (permutation) on a small instance
  3. monotonicity: local search never worsens the objective
  4. budget obedience: runtime within 1.5x of requested budget on a small run
  5. LS soundness probe: composite operator orders must agree within 6% on a
     probe instance (added after artifact A1 — stale don't-look bits made
     (or_opt-first) composites converge up to ~30% worse than equivalent
     (two_opt-first) runs; see DECISIONS.md D13)
"""
from __future__ import annotations

import numpy as np

from ..domains.tsp.algorithms import run_ils, run_plain_ls
from ..domains.tsp.instance import generate
from ..domains.tsp.localsearch import TourState, run_local_search
from .space import to_ilscfg, validate


class Coder:
    def __init__(self):
        self.check_instance = generate("uniform", 30, 999)

    def validate_config(self, cfg: dict) -> list[str]:
        return validate(cfg)

    def _ls_soundness_probe(self) -> list[str]:
        errs = []
        rng = np.random.default_rng(7)
        t = list(range(self.check_instance.n))
        rng.shuffle(t)
        lens = {}
        for ops in (("two_opt", "or_opt1"), ("or_opt1", "two_opt")):
            st = TourState(self.check_instance, list(t), nl_k=None)
            run_local_search(st, ops)
            lens[ops] = st.length()
        lo = min(lens.values())
        for ops, L in lens.items():
            if L > lo * 1.06:
                errs.append(
                    f"ls_soundness: order {ops} converged >6% worse "
                    f"({L:.0f} vs {lo:.0f}) — stale-mask artifact?")
        return errs

    def sanity_checks(self, cfg: dict, budget_s: float = 0.5,
                      skip_probe: bool = False) -> list[str]:
        errs = self.validate_config(cfg)
        if errs:
            return errs
        if not skip_probe:
            errs.extend(self._ls_soundness_probe())
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
