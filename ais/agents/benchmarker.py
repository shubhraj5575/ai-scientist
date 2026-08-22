"""Benchmark engineer: executes the measurement protocol and records
every run with full provenance into the experiment database.

Protocol (pre-registered, see DECISIONS.md D4):
  * instances: exact suite (n<=14, optimal known), medium suite
    (n in {50,100,200}), structured suite (clustered/grid n=100)
  * seeds 0..9 per instance; budgets fixed per suite
  * quality = 100 * (length - reference) / reference   [% excess]
    reference = exact optimum where known, else internal best-known-so-far
    (BKS) which is updated whenever any run finds a shorter tour; BKS rows
    are always labelled and never treated as proven optima.
"""
from __future__ import annotations

import json

from ..config import DEFAULT_BUDGETS as BUDGETS
from ..config import EXACT_NS, MEDIUM_NS, SEEDS, STRUCTURED_N, GIT_REMOTE
from ..domains.tsp.instance import Instance, generate, get_instance
from ..domains.tsp.algorithms import ILSConfig, run_ils
from ..utils import env_snapshot, git_commit, now_iso, peak_rss_mb
from .. import config as cfg_mod

PROJECT_ROOT = cfg_mod.PROJECT_ROOT


class BenchmarkEngineer:
    def __init__(self, db):
        self.db = db
        self.git = git_commit(PROJECT_ROOT)
        self.instance_names: dict[str, int] = {}

    # -- instance registry ---------------------------------------------------
    def ensure_instances(self) -> dict[str, int]:
        """Register all protocol instances; returns name->id map."""
        names: dict[str, int] = {}
        specs: list[tuple[str, int, int]] = []
        for n in EXACT_NS:
            for s in SEEDS[:5]:
                specs.append(("uniform", n, s))
        for n in MEDIUM_NS:
            for s in SEEDS:
                specs.append(("uniform", n, s))
        for s in SEEDS:
            specs.append(("clustered", STRUCTURED_N, s))
            specs.append(("grid", STRUCTURED_N, s))
        for kind, n, seed in specs:
            inst = get_instance(kind, n, seed)
            iid = self.db.upsert_instance(inst)
            names[inst.name] = iid
        self.instance_names = names
        return names

    def set_exact_references(self, instance_names: list[str]):
        from ..domains.tsp.exact import held_karp_length
        for name in instance_names:
            kind, n_s, s_s = name.split("_")
            n = int(n_s[1:])
            if n > 16:
                continue
            inst = get_instance(kind, n, int(s_s[1:]))
            iid = self.db.upsert_instance(inst)
            row = self.db.one(
                "SELECT value FROM reference_vals WHERE instance_id=? AND kind='exact'",
                (iid,))
            if not row:
                val = held_karp_length(inst)
                self.db.set_reference(iid, "exact", val, "held_karp",
                                      "verified vs brute force n<=8")
                print(f"  exact ref {name}: {val:.2f}")

    def bks(self, instance_name: str) -> float | None:
        iid = self._iid(instance_name)
        row = self.db.one(
            "SELECT value FROM reference_vals WHERE instance_id=? AND kind='bks'",
            (iid,))
        return float(row["value"]) if row else None

    def update_bks_if_better(self, inst: Instance, length: float,
                             provenance: str):
        iid = self.db.upsert_instance(inst)
        cur = self.bks(inst.name)
        if cur is None or length < cur - 1e-9:
            self.db.set_reference(iid, "bks", length, "best_of_all_runs",
                                  provenance)
            return True
        return False

    def _iid(self, name: str) -> int:
        row = self.db.one("SELECT id FROM instances WHERE name=?", (name,))
        if not row:
            raise LookupError(name)
        return int(row["id"])

    # -- execution -------------------------------------------------------------
    def benchmark_candidate(self, batch_id: str, candidate_uid: str,
                            cfg: dict, suites: list[str],
                            seeds_map: dict[str, list[int]],
                            budget_map: dict[str, float],
                            verbose: bool = False) -> int:
        """Run candidate over suites with per-suite seed lists. Returns #runs."""
        ilscfg = _to_ilscfg(cfg)
        env = env_snapshot({"git_commit": self.git})
        if not self.instance_names:
            # lazy reload from DB (new session after a previous registration)
            rows = self.db.query("SELECT id, name FROM instances")
            self.instance_names = {r["name"]: int(r["id"]) for r in rows}
        count = 0
        for suite_name in suites:
            budget = budget_map[suite_name]
            seeds = seeds_map[suite_name]
            for inst_name, iid in sorted(self.instance_names.items()):
                if not _in_suite(suite_name, inst_name):
                    continue
                inst = get_instance(*_parse_name(inst_name))
                ref_val, ref_kind = None, None
                try:
                    ref_val, ref_kind = self.db.get_reference(iid)
                except LookupError:
                    pass
                for seed in seeds:
                    res = run_ils(inst, ilscfg, budget, seed)
                    excess = 0.0
                    if ref_val is not None:
                        excess = 100.0 * (res.length - ref_val) / ref_val
                    elif ref_kind is None:
                        excess = float("nan")   # no reference yet -> flagged later
                    self.update_bks_if_better(
                        inst, res.length, f"{candidate_uid}@{batch_id}")
                    self.db.add_run(
                        batch_id=batch_id, candidate_uid=candidate_uid,
                        instance_id=iid, seed=seed, budget_s=budget,
                        length=res.length, excess_pct=excess,
                        runtime_s=res.runtime_s, kicks=res.n_kicks,
                        ls_moves=res.ls_moves, restarts=res.n_restarts,
                        peak_rss_mb=peak_rss_mb(), git_commit=self.git,
                        env=env)
                    count += 1
                    if verbose:
                        print(f"    {inst_name} s{seed}: len={res.length:.1f} "
                              f"excess={excess:.2f}% rt={res.runtime_s:.2f}s")
        if count == 0 and suites:
            raise RuntimeError(
                f"benchmark_candidate produced 0 runs (suites={suites}) — "
                f"instance registry empty or suite filter matched nothing")
        return count


def _to_ilscfg(cfg: dict) -> ILSConfig:
    from .space import to_ilscfg
    return to_ilscfg(cfg)


def _parse_name(name: str) -> tuple[str, int, int]:
    kind, ns, ss = name.split("_")
    return kind, int(ns[1:]), int(ss[1:])


def _in_suite(suite: str, inst_name: str) -> bool:
    kind, n, _ = _parse_name(inst_name)
    if suite == "exact":
        return kind == "uniform" and n <= 14
    if suite == "medium":
        return kind == "uniform" and n >= 50
    if suite == "structured":
        return kind in ("clustered", "grid")
    if suite == "scale":
        return n >= 500
    raise ValueError(suite)


DEFAULT_SUITE_BUDGETS = {
    "exact": BUDGETS.exact_suite,
    "medium": BUDGETS.medium,
    "structured": BUDGETS.structured,
    "scale": BUDGETS.scale,
}
