"""Candidate space: declarative grammar of solver configurations.

Every candidate is a JSON-serialisable dict validated against this module.
The Designer samples from this space; the Coder materialises it into an
ILSConfig. Keeping candidates declarative makes ablations clean, configs
hashable, and results attributable to specific components.
"""
from __future__ import annotations

from dataclasses import asdict

from ..domains.tsp.algorithms import ILSConfig

COMPONENT_SPACE = {
    "construction": ["nn", "greedy", "cheapest_ins", "random"],
    "ls_operators": [
        ("two_opt",),
        ("two_opt", "or_opt"),
        ("two_opt", "or_opt1"),
        ("or_opt1", "two_opt"),
    ],
    "nl_k": [None, 8, 16, 40],
    "perturbation": [None, "double_bridge", "reversals", "relocations"],
    "perturb_strength": [1, 2, 4],
    "perturb_base": ["current", "best"],
    "acceptance": ["better", "threshold", "record_to_record", "sa", "lahc"],
    "sa_T0_frac": [0.005, 0.02, 0.05],
    "sa_alpha": [0.90, 0.97],
    "lahc_L": [25, 100],
    "threshold_rel": [0.0005, 0.005],
    "restart_stagnation": [0, 200],
}

BASELINE_CONFIG = {
    "construction": "nn",
    "ls_operators": ("two_opt",),
    "nl_k": None,
    "perturbation": None,
    "acceptance": "better",
}

CHAMPION_SEED_CONFIG = {
    # classic ILS starting point (Lourenço/Martin/Stützle template):
    # double-bridge kick + better-acceptance, full-scan 2-opt
    "construction": "nn",
    "ls_operators": ("two_opt",),
    "nl_k": None,
    "perturbation": "double_bridge",
    "perturb_strength": 1,
    "perturb_base": "current",
    "acceptance": "better",
}


def validate(cfg: dict) -> list[str]:
    """Return a list of violations (empty = valid)."""
    errs = []
    for key in cfg:
        if key not in COMPONENT_SPACE:
            errs.append(f"unknown component {key!r}")
            continue
        val = _canon(cfg[key])
        allowed = [_canon(v) for v in COMPONENT_SPACE[key]]
        if val not in allowed:
            errs.append(f"{key}={val!r} not in {allowed}")
    # cross-field constraints
    if cfg.get("perturbation") in (None, "double_bridge") and \
            cfg.get("perturb_strength") not in (None, 1) and \
            cfg.get("perturbation") is None:
        errs.append("strength set without perturbation")
    if cfg.get("acceptance") == "sa" and "sa_T0_frac" not in cfg:
        errs.append("sa requires sa_T0_frac")
    return errs


def _canon(v):
    if isinstance(v, list) and all(isinstance(x, str) for x in v):
        return tuple(v)
    return v


def to_ilscfg(cfg: dict) -> ILSConfig:
    kw = {}
    mapping = {
        "construction": "construction",
        "ls_operators": "ls_operators",
        "nl_k": "nl_k",
        "perturbation": "perturbation",
        "perturb_strength": "perturb_strength",
        "perturb_base": "perturb_base",
        "acceptance": "acceptance",
        "sa_T0_frac": "sa_T0_frac",
        "sa_alpha": "sa_alpha",
        "lahc_L": "lahc_L",
        "threshold_rel": "threshold_rel",
        "restart_stagnation": "restart_stagnation",
    }
    for k, field in mapping.items():
        if k in cfg and cfg[k] is not None:
            v = cfg[k]
            if k == "ls_operators" and isinstance(v, list):
                v = tuple(v)
            kw[field] = v
    return ILSConfig(**kw)


def canon(cfg: dict) -> dict:
    """Canonical JSON-safe form (tuples -> lists, sorted keys downstream)."""
    out = {}
    for k, v in cfg.items():
        if isinstance(v, tuple):
            out[k] = list(v)
        else:
            out[k] = v
    return out


def config_uid(cfg: dict) -> str:
    import hashlib
    blob = repr(sorted(canon(cfg).items(), key=lambda kv: kv[0])).encode()
    return "C-" + hashlib.sha1(blob).hexdigest()[:10]
