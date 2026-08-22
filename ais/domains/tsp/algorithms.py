"""Configurable Iterated Local Search solver.

The solver is assembled from declarative components (see space.py):
    construction -> local search -> [perturb -> local search -> accept]*
This module contains no candidate-specific logic; every knob comes from the
config so that benchmark results are directly attributable to components.
"""
from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field

import numpy as np

from .construction import CONSTRUCTIONS
from .instance import Instance
from .localsearch import TourState, run_local_search
from .perturb import perturb


@dataclass
class ILSConfig:
    construction: str = "nn"
    ls_operators: tuple[str, ...] = ("two_opt",)
    nl_k: int | None = 16              # neighbour list size; None = full
    perturbation: str = "double_bridge"
    perturb_strength: int = 1          # semantic depends on operator
    perturb_base: str = "current"      # 'current' | 'best'
    acceptance: str = "better"         # see ACCEPTORS
    sa_T0_frac: float = 0.02           # T0 = frac * initial tour length
    sa_alpha: float = 0.95             # geometric cooling per kick
    lahc_L: int = 50
    threshold_rel: float = 0.001       # threshold acceptance / record-to-record delta
    restart_stagnation: int = 0        # 0 = never restart; else kicks w/o best-improve


@dataclass
class SolverResult:
    tour: list[int]
    length: float
    runtime_s: float
    n_kicks: int
    ls_moves: int
    n_restarts: int
    converged_initial: bool
    config_digest: str
    meta: dict = field(default_factory=dict)


def _make_acceptor(cfg: ILSConfig, init_len: float):
    """Returns f(new_len, cur_len, best_len, rng) -> bool."""
    kind = cfg.acceptance
    if kind == "better":
        def accept(new, cur, best, rng):
            return new < cur - 1e-9
        return accept
    if kind == "better_eq":
        def accept(new, cur, best, rng):
            return new <= cur + 1e-9
        return accept
    if kind == "threshold":
        th = cfg.threshold_rel
        def accept(new, cur, best, rng):
            return new <= cur * (1 + th) + 1e-9
        return accept
    if kind == "record_to_record":
        th = cfg.threshold_rel
        def accept(new, cur, best, rng):
            return new < best * (1 + th) + 1e-9
        return accept
    if kind == "sa":
        state = {"T": max(1e-9, cfg.sa_T0_frac * init_len)}
        alpha = cfg.sa_alpha

        def accept(new, cur, best, rng):
            delta = new - cur
            T = state["T"]
            ok = delta <= 1e-9 or (T > 1e-12 and rng.random() < float(np.exp(-delta / T)))
            state["T"] *= alpha          # geometric cooling per kick
            return ok
        return accept
    if kind == "lahc":
        L = max(1, cfg.lahc_L)
        hist = deque([init_len] * L, maxlen=L)

        def accept(new, cur, best, rng):
            ok = new <= hist[0] + 1e-9
            hist.append(cur)             # classic LAHC appends previous objective
            return ok
        return accept
    raise ValueError(f"unknown acceptance {kind!r}")


def run_ils(inst: Instance, cfg: ILSConfig, budget_s: float,
            seed: int) -> SolverResult:
    rng = np.random.default_rng(seed)
    t_end = time.perf_counter() + budget_s

    # --- construction -------------------------------------------------------
    t0 = time.perf_counter()
    start_tour = CONSTRUCTIONS[cfg.construction](inst, rng)
    st = TourState(inst, start_tour, nl_k=cfg.nl_k)
    run_local_search(st, cfg.ls_operators)
    converged_initial = time.perf_counter() >= t_end

    cur = st.copy_tour()
    cur_len = inst.tour_length(cur)
    best, best_len = list(cur), cur_len
    accept_fn = _make_acceptor(cfg, cur_len)

    kicks = 0
    restarts = 0
    since_improve = 0

    while time.perf_counter() < t_end:
        base = cur if cfg.perturb_base == "current" else best
        cand = perturb(base, cfg.perturbation, cfg.perturb_strength, rng)
        st2 = TourState(inst, cand, nl_k=cfg.nl_k)
        run_local_search(st2, cfg.ls_operators)
        new_len = st2.length()
        kicks += 1

        if accept_fn(new_len, cur_len, best_len, rng):
            cur = st2.copy_tour()
            cur_len = new_len
        if new_len < best_len - 1e-9:
            best, best_len = st2.copy_tour(), new_len
            since_improve = 0
        else:
            since_improve += 1

        if cfg.restart_stagnation and since_improve >= cfg.restart_stagnation:
            fresh_tour = CONSTRUCTIONS[cfg.construction](inst, rng)
            st3 = TourState(inst, fresh_tour, nl_k=cfg.nl_k)
            run_local_search(st3, cfg.ls_operators)
            cur, cur_len = st3.copy_tour(), st3.length()
            if cfg.acceptance == "sa":
                # reheat handled implicitly by fresh acceptor state is not
                # accessible here; documented as a known limitation (D8)
                pass
            restarts += 1
            since_improve = 0

    return SolverResult(
        tour=best,
        length=best_len,
        runtime_s=time.perf_counter() - t0,
        n_kicks=kicks,
        ls_moves=int(st.moves),
        n_restarts=restarts,
        converged_initial=converged_initial,
        config_digest="",
        meta={},
    )


def run_plain_ls(inst: Instance, construction: str, operators: tuple[str, ...],
                 nl_k: int | None, seed: int,
                 budget_s: float | None = None) -> SolverResult:
    """Single construction + local search to convergence (baseline mode)."""
    from .construction import CONSTRUCTIONS as C
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed)
    tour = C[construction](inst, rng)
    st = TourState(inst, tour, nl_k=nl_k)
    run_local_search(st, operators)
    return SolverResult(
        tour=st.copy_tour(), length=st.length(),
        runtime_s=time.perf_counter() - t0, n_kicks=0, ls_moves=int(st.moves),
        n_restarts=0, converged_initial=True, config_digest="", meta={},
    )
