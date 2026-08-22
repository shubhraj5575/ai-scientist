"""Designer agent: generates candidate configurations with pre-registered
hypotheses, guided by (a) literature priors, (b) bandit scores over
component choices learned from the experiment DB, (c) one-factor mutations
of the incumbent champion.

Candidate generation strategy per round (mix):
  * 2 one-factor mutations of champion (clean ablation signal)
  * 1 untried literature-prior combination
  * remaining slots: UCB1-guided sampling over component values
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass

import numpy as np

from .space import COMPONENT_SPACE, CHAMPION_SEED_CONFIG, canon, config_uid


@dataclass
class Candidate:
    uid: str
    config: dict
    family: str                 # mutation | prior | bandit
    hypothesis_uid: str = ""
    parent_uid: str = ""
    statement: str = ""
    rationale: str = ""
    expected_effect: str = ""
    prediction: str = ""


class ComponentBandit:
    """UCB1 over discrete component choices; reward = mean excess reduction
    vs campaign baseline observed for configs containing that choice."""

    def __init__(self):
        self.rewards: dict[tuple[str, str], list[float]] = {}
        self._total = 0

    def update(self, component: str, value: str, reward: float):
        self.rewards.setdefault((component, value), []).append(reward)
        self._total += 1

    def best_value(self, component: str, values: list) -> tuple[str, float]:
        """Pick value by UCB1 score. Returns (value, score)."""
        entries = []
        for v in values:
            rs = self.rewards.get((component, _key(v)), [])
            if rs:
                mean = sum(rs) / len(rs)
                bonus = math.sqrt(2 * math.log(max(self._total, 1)) / len(rs))
                entries.append((mean + bonus, v))
            else:
                entries.append((float("inf"), v))     # play each arm once first
        entries.sort(key=lambda e: (-e[0], str(e[1])))
        return entries[0][1], entries[0][0]

    def summary(self) -> dict:
        return {
            f"{c}={v}": {"n": len(rs), "mean_reward": round(sum(rs) / len(rs), 4)}
            for (c, v), rs in sorted(self.rewards.items())
        }


def _key(v) -> str:
    if isinstance(v, (list, tuple)):
        return ",".join(map(str, v))
    if v is None:
        return "none"
    return str(v)


def _fill_required_params(cfg: dict):
    """Ensure acceptance-specific parameters exist (drawn from grammar)."""
    acc = cfg.get("acceptance")
    rng = random.Random(hash(config_uid(cfg)) & 0xFFFFFFFF)
    if acc == "sa":
        cfg.setdefault("sa_T0_frac", rng.choice(COMPONENT_SPACE["sa_T0_frac"]))
        cfg.setdefault("sa_alpha", rng.choice(COMPONENT_SPACE["sa_alpha"]))
    elif acc == "lahc":
        cfg.setdefault("lahc_L", rng.choice(COMPONENT_SPACE["lahc_L"]))
    elif acc in ("threshold", "record_to_record"):
        cfg.setdefault("threshold_rel",
                       rng.choice(COMPONENT_SPACE["threshold_rel"]))
    if cfg.get("perturbation") is None:
        cfg.pop("perturb_strength", None)


class Designer:
    def __init__(self, seed: int = 20260822):
        self.rng = random.Random(seed)
        self.bandit = ComponentBandit()
        self.hyp_counter = 0
        self.candidate_counter = 0

    # ------------------------------------------------------------------
    def propose(self, champion_cfg: dict, tried_digests: set[str],
                k_new: int = 5) -> list[Candidate]:
        proposals: list[Candidate] = []

        # --- family 1: one-factor mutations of champion -------------------
        mutable = [k for k in COMPONENT_SPACE if k in champion_cfg or k in (
            "perturbation", "acceptance", "ls_operators", "nl_k")]
        self.rng.shuffle(mutable)
        mutations_done = 0
        for comp in mutable:
            if mutations_done >= 2:
                break
            vals = COMPONENT_SPACE[comp]
            current = champion_cfg.get(comp, None)
            alternatives = [v for v in vals if _key(v) != _key(current)]
            if not alternatives:
                continue
            new_val = self.rng.choice(alternatives)
            cfg = dict(champion_cfg)
            cfg[comp] = new_val
            _fill_required_params(cfg)
            uid = config_uid(cfg)
            if uid in tried_digests or any(p.uid == uid for p in proposals):
                continue
            mutations_done += 1
            proposals.append(self._wrap(
                cfg, family="mutation",
                statement=f"Changing {comp} from {_key(current)} to "
                          f"{_key(new_val)} improves mean quality at fixed budget.",
                rationale="Single-factor ablation isolates the component effect "
                          "while holding all other choices at champion settings.",
                expected_effect=f"Direction unknown a priori; detectable effect "
                                f">=0.3pp mean excess difference.",
                prediction="Paired Wilcoxon on single-factor diff: "
                           "p<0.05 after Holm within batch."))

        # --- family 2: untried literature priors --------------------------
        prior_pool = [
            {"construction": "greedy", "ls_operators": ("two_opt", "or_opt"),
             "nl_k": None, "perturbation": "double_bridge",
             "perturb_base": "current", "acceptance": "better"},
            {"construction": "nn", "ls_operators": ("or_opt1", "two_opt"),
             "nl_k": 40, "perturbation": "double_bridge",
             "perturb_base": "best", "acceptance": "record_to_record",
             "threshold_rel": 0.005},
            {"construction": "cheapest_ins", "ls_operators": ("two_opt",),
             "nl_k": None, "perturbation": "reversals",
             "perturb_strength": 4, "perturb_base": "current",
             "acceptance": "threshold", "threshold_rel": 0.005},
        ]
        for pcfg in prior_pool:
            if len(proposals) >= k_new:
                break
            uid = config_uid(pcfg)
            if uid in tried_digests or any(p.uid == uid for p in proposals):
                continue
            proposals.append(self._wrap(
                pcfg, family="prior",
                statement="Literature-prior combination beats champion.",
                rationale="Combination recommended by curated ILS literature; "
                          "not yet evaluated under our protocol/budget.",
                expected_effect=">=0 pp; test of external validity of priors "
                                "under equal-budget rules.",
                prediction="Significant paired difference either direction; "
                           "sign recorded as evidence about prior transfer."))

        # --- family 3: combo of empirically-winning arms -------------------
        winners = {}
        for comp in ("construction", "ls_operators", "nl_k", "perturbation",
                     "acceptance", "perturb_base"):
            entries = []
            for v in COMPONENT_SPACE[comp]:
                rs = self.bandit.rewards.get((comp, _key(v)), [])
                if len(rs) >= 2:
                    entries.append((sum(rs) / len(rs), v))
            if entries:
                entries.sort(key=lambda e: -e[0])
                if entries[0][0] > 0:      # only arms with net-positive reward
                    winners[comp] = entries[0][1]
        if winners and len(winners) >= 2:
            cfg = dict(champion_cfg)
            cfg.update(winners)
            _fill_required_params(cfg)
            uid = config_uid(cfg)
            if uid not in tried_digests and \
                    not any(p.uid == uid for p in proposals):
                proposals.append(self._wrap(
                    cfg, family="combo",
                    statement="Combining components whose arms show "
                              f"net-positive rewards ({winners}) beats champion.",
                    rationale="Greedy assembly of individually-positive arms; "
                              "tests additivity of component effects.",
                    expected_effect=">= sum of individual effects if additive.",
                    prediction="Significant improvement vs champion; failure "
                               "would indicate negative interaction."))

        # --- family 4: bandit-guided combinations -------------------------
        while len(proposals) < k_new:
            cfg = dict(champion_cfg)
            comps = ["ls_operators", "nl_k", "perturbation", "acceptance",
                     "perturb_base"]
            for comp in comps:
                val, _score = self.bandit.best_value(comp, COMPONENT_SPACE[comp])
                cfg[comp] = val
                if comp == "perturbation" and val is None:
                    cfg.pop("perturb_strength", None)
            _fill_required_params(cfg)
            uid = config_uid(cfg)
            if uid in tried_digests or any(p.uid == uid for p in proposals):
                # random perturbation of one slot to escape collisions
                comp = self.rng.choice(comps)
                cfg[comp] = self.rng.choice(COMPONENT_SPACE[comp])
                _fill_required_params(cfg)
                uid = config_uid(cfg)
                if uid in tried_digests or any(p.uid == uid for p in proposals):
                    continue
            proposals.append(self._wrap(
                cfg, family="bandit",
                statement="Bandit-selected component combination matches or "
                          "beats champion.",
                rationale=f"UCB1 over accumulated rewards; current arms: "
                          f"{ {c: _key(cfg.get(c)) for c in comps} }",
                expected_effect="Exploitation step; small positive drift "
                                "expected if bandit estimates are stable.",
                prediction="No regression vs champion beyond noise."))

        self.candidate_counter += len(proposals)
        return proposals[:k_new]

    # ------------------------------------------------------------------
    def _wrap(self, cfg: dict, family: str, statement: str, rationale: str,
              expected_effect: str, prediction: str) -> Candidate:
        self.hyp_counter += 1
        hyp_uid = f"H-{self.hyp_counter:04d}"
        return Candidate(
            uid=config_uid(cfg), config=canon(cfg), family=family,
            hypothesis_uid=hyp_uid, statement=statement, rationale=rationale,
            expected_effect=expected_effect, prediction=prediction,
        )
