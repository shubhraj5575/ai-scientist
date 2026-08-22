"""Global configuration and paths for the AI Scientist system.

All experiment-relevant constants live here so that runs are reproducible
and the provenance of every number in reports can be traced to code.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
DB_PATH = RESULTS_DIR / "experiments.db"
DOCS_DIR = PROJECT_ROOT  # top-level docs (README.md etc.)

for _d in (DATA_DIR, RESULTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)


@dataclass
class StatsProtocol:
    """Pre-registered decision protocol for champion promotion.

    These thresholds are fixed BEFORE batches are analysed (see DECISIONS.md D4)
    to avoid post-hoc rationalisation of noise.
    """
    seeds_full: int = 10            # seeds per instance for full benchmark
    seeds_pilot: int = 3            # seeds per instance for pilot screening
    alpha: float = 0.05             # family-wise significance level (Holm corrected)
    min_effect_pp: float = 0.30     # practical significance: mean excess reduction >= 0.30 pp
    max_runtime_ratio: float = 1.25 # allowed median runtime ratio vs incumbent
    max_runtime_ratio_bigwin: float = 2.0  # if effect >= bigwin_factor*min_effect_pp
    bigwin_factor: float = 3.0
    bootstrap_B: int = 10_000


@dataclass
class BenchmarkBudgets:
    """Wall-clock budgets per run type (seconds).

    Sized so one FULL candidate evaluation (exact+medium suites, all seeds)
    costs ~13-15 min: exact 20inst x10seeds x1.5s + medium 30inst x6seeds x3s.
    Ranking stability under reduced budgets is itself tested empirically
    (see EXPERIMENTS.md 'budget sensitivity' check).
    """
    exact_suite: float = 1.5
    medium: float = 3.0
    structured: float = 3.0
    scale: float = 15.0
    bks_bootstrap: float = 10.0


DEFAULT_PROTOCOL = StatsProtocol()
DEFAULT_BUDGETS = BenchmarkBudgets()

# Instance suite definitions -------------------------------------------------
EXACT_NS = [8, 10, 12, 14]
MEDIUM_NS = [50, 100, 200]
SCALE_NS = [500, 1000]
STRUCTURED_N = 100
SEEDS = tuple(range(10))          # global seed set S = {0..9}
SEEDS_EXACT = tuple(range(10))    # cheap runs -> all seeds
SEEDS_MEDIUM = tuple(range(6))    # expensive runs -> 6 paired seeds

GIT_REMOTE = "https://github.com/shubhraj5575/ai-scientist"
