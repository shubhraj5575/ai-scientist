"""Research Director: orchestrates the autonomous experimental loop.

Loop per batch:
    propose -> sanity gate -> benchmark -> analyse -> critique
    -> promote (if pre-registered rule satisfied) -> log -> commit

Phases:
    0 setup        : instances + exact references
    1 bks          : bootstrap internal best-known solutions
    2 baselines    : plain LS vs seed ILS; initial champion promotion
    3 ofat         : one-factor ablations around champion
    4 explore      : designer rounds w/ pilot screening + bandit guidance
    5 scale        : scaling study n in {500, 1000} (descriptive)
    6 robust       : structured-suite robustness analysis
"""
from __future__ import annotations

import json
import subprocess
import time

import numpy as np

from .. import config as C
from ..db import ExperimentDB
from ..utils import git_commit, now_iso
from .benchmarker import BenchmarkEngineer, DEFAULT_SUITE_BUDGETS
from .coder import Coder
from .critic import Critic
from .designer import Designer
from .researcher import ResearchNote, Researcher
from .space import BASELINE_CONFIG, CHAMPION_SEED_CONFIG, config_uid
from .statistician import Statistician

PROJECT_ROOT = C.PROJECT_ROOT

SEEDS_MAP_DEFAULT = {
    "exact": list(C.SEEDS_EXACT),
    "medium": list(C.SEEDS_MEDIUM),
    "structured": list(C.SEEDS_MEDIUM),
    "scale": [0, 1, 2],
}


def _suite_prefix(instance_name: str) -> str:
    kind = instance_name.split("_")[0]
    n = int(instance_name.split("_n")[1].split("_")[0])
    if kind == "uniform":
        return "exact" if n <= 14 else "medium"
    return "structured" if n < 500 else "scale"


def budgets_for(*suites: str) -> dict[str, float]:
    b = {"exact": C.DEFAULT_BUDGETS.exact_suite,
         "medium": C.DEFAULT_BUDGETS.medium,
         "structured": C.DEFAULT_BUDGETS.structured,
         "scale": C.DEFAULT_BUDGETS.scale}
    return {s: b[s] for s in suites}


class Director:
    def __init__(self):
        self.db = ExperimentDB()
        self.git = git_commit(PROJECT_ROOT)
        self.researcher = Researcher()
        self.designer = Designer()
        self.coder = Coder()
        self.bench = BenchmarkEngineer(self.db)
        self.stat = Statistician(self.db)
        self.critic = Critic(self.db)
        self.champion_uid: str | None = None
        self.champion_cfg: dict = dict(CHAMPION_SEED_CONFIG)
        self.t_start = time.time()
        self._load_champion()

    # ------------------------------------------------------------------ meta
    def _load_champion(self):
        row = self.db.one("SELECT value FROM meta WHERE key='champion'")
        if row:
            obj = json.loads(row["value"])
            self.champion_uid = obj["uid"]
            self.champion_cfg = obj["config"]

    def _save_champion(self):
        self.db.execute(
            "INSERT OR REPLACE INTO meta VALUES ('champion', ?)",
            (json.dumps({"uid": self.champion_uid,
                         "config": self.champion_cfg}),))

    def remaining_s(self, budget_h: float) -> float:
        return budget_h * 3600 - (time.time() - self.t_start)

    # ------------------------------------------------------------------ docs
    def log(self, msg: str):
        line = f"- **{now_iso()}** {msg}"
        print(line)
        path = PROJECT_ROOT / "OVERNIGHT_LOG.md"
        with open(path, "a") as f:
            f.write(line + "\n")

    def commit_push(self, msg: str):
        try:
            subprocess.run(["git", "add", "-A"], cwd=PROJECT_ROOT, check=True,
                           capture_output=True)
            r = subprocess.run(["git", "commit", "-m", msg], cwd=PROJECT_ROOT,
                               capture_output=True, text=True)
            if r.returncode != 0 and "nothing to commit" not in r.stdout:
                print("git commit:", r.stdout[-300:], r.stderr[-300:])
            subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_ROOT,
                           capture_output=True, timeout=120)
            self.git = git_commit(PROJECT_ROOT)
            self.db.execute(
                "INSERT OR REPLACE INTO meta VALUES ('last_git_commit',?)",
                (self.git,))
        except Exception as e:      # offline / auth loss must not kill science
            print(f"[git] skipped: {e}")

    # ------------------------------------------------------------- benchmark
    def _register(self, cand) -> str:
        self.db.add_hypothesis(
            cand.hypothesis_uid, cand.statement, cand.rationale,
            cand.expected_effect, cand.prediction,
            literature_basis="see researcher notes")
        self.db.add_candidate(
            uid=cand.uid, family=cand.family, config=cand.config,
            hypothesis_uid=cand.hypothesis_uid, parent_uid=self.champion_uid or "",
            code_version="v1", git_commit=self.git)
        return cand.uid

    def _sanity_gate(self, cand) -> bool:
        errs = self.coder.sanity_checks(cand.config, budget_s=1.0)
        if errs:
            self.db.set_candidate_status(cand.uid, "rejected")
            self.db.add_critique("gate", cand.uid, "blocking",
                                 "sanity: " + "; ".join(errs))
            return False
        return True

    def run_batch(self, batch_id: str, candidates: list, suites: list[str],
                  seeds_map: dict[str, list[int]],
                  budgets: dict[str, float],
                  pilot_first: bool = False) -> list[dict]:
        accepted: list[dict] = []
        for cand in candidates:
            if not self._sanity_gate(cand):
                continue
            self._register(cand)
            ok = True
            if pilot_first:
                pilot_budgets = {s: max(1.0, budgets[s] * 0.4) for s in suites}
                self.bench.benchmark_candidate(
                    batch_id + "-pilot", cand.uid, cand.config,
                    suites=suites[:1],
                    seeds_map={suites[0]: seeds_map[suites[0]][:3]},
                    budget_map=pilot_budgets)
                pilot_rows = self.db.query(
                    """SELECT excess_pct FROM runs WHERE candidate_uid=? AND
                       batch_id=?""", (cand.uid, batch_id + "-pilot"))
                pilot_ex = [r["excess_pct"] for r in pilot_rows
                            if r["excess_pct"] is not None
                            and np.isfinite(r["excess_pct"])]
                # screening rule: keep if within 3pp of champion mean
                champ_ex, _, _ = self.db.excess_lookup(self.champion_uid)
                champ_keys = [k for k in champ_ex
                              if k[0].rsplit("_n", 1)[-1].split("_")[0]
                              .isdigit() and _suite_prefix(k[0]) == suites[0]]
                champ_mean = (float(np.mean([champ_ex[k] for k in champ_keys]))
                              if champ_keys else None)
                keep = (not pilot_ex or champ_mean is None
                        or float(np.mean(pilot_ex)) <= champ_mean + 3.0)
                if not keep:
                    self.db.set_candidate_status(cand.uid, "rejected")
                    self.db.add_critique(
                        batch_id, cand.uid, "info",
                        f"pilot_screened_out mean="
                        f"{float(np.mean(pilot_ex)):.2f} vs champ "
                        f"{champ_mean:.2f}")
                    ok = False
            if ok:
                n = self.bench.benchmark_candidate(
                    batch_id, cand.uid, cand.config, suites=suites,
                    seeds_map=seeds_map, budget_map=budgets)
                self.db.set_candidate_status(cand.uid, "benchmarked")
                accepted.append({"uid": cand.uid, "config": cand.config,
                                 "n_runs": n})
        return accepted

    def analyse_and_promote(self, batch_id: str, accepted: list[dict],
                            suites: tuple[str, ...],
                            baseline_uid: str | None = None) -> list[dict]:
        analyses = self.stat.analyse_batch(
            batch_id, accepted, baseline_uid or self.champion_uid,
            suites=suites)
        if not analyses:
            self.log(f"batch {batch_id}: nothing analysable "
                     f"(no baseline or no shared pairs)")
            return []
        self.stat.record(batch_id, analyses)
        findings = self.critic.review_batch(
            batch_id, [a["uid"] for a in accepted], len(C.SEEDS), analyses)

        promoted = None
        promotable = [a for a in analyses if a["decision"] == "promote"]
        if promotable:
            best = max(promotable, key=lambda a: a["mean_delta_pp"])
            promoted = best
            cfg = next(a["config"] for a in accepted
                       if a["uid"] == best["candidate_uid"])
            self.champion_uid = best["candidate_uid"]
            self.champion_cfg = cfg
            self._save_champion()
            self.db.set_candidate_status(best["candidate_uid"], "promoted")
            self.db.decision("champion_promotion", {
                "batch": batch_id, "uid": best["candidate_uid"],
                "delta_pp": best["mean_delta_pp"],
                "ci": [best["ci_lo"], best["ci_hi"]],
                "p_wilcoxon": best["wilcoxon_p"], "dz": best["cohens_dz"]})
            self.researcher.add_finding(ResearchNote(
                topic=f"promotion@{batch_id}",
                claim=f"{best['candidate_uid']} beats prior champion by "
                      f"{best['mean_delta_pp']:.2f}pp mean excess "
                      f"(95% CI [{best['ci_lo']:.2f},{best['ci_hi']:.2f}], "
                      f"Wilcoxon p={best['wilcoxon_p']:.2g}, "
                      f"win rate {best['win_rate']:.2f}).",
                evidence_class="OUR_FINDING",
                source=f"this project: analyses.batch_id={batch_id}",
                design_prior=None))
        # bandit update with observed deltas (reward = improvement vs champion)
        for a in analyses:
            reward = a["mean_delta_pp"]
            cfg = next((x["config"] for x in accepted
                        if x["uid"] == a["candidate_uid"]), None)
            if cfg is None:
                continue
            for comp in ("construction", "ls_operators", "nl_k",
                         "perturbation", "acceptance", "perturb_base"):
                if comp in cfg and cfg[comp] is not None:
                    from .designer import _key
                    self.designer.bandit.update(comp, _key(cfg[comp]), reward)
        self.log(
            f"batch {batch_id}: {len(analyses)} analysed, "
            f"{len(findings)} critiques, "
            f"promotions={[p['candidate_uid'] for p in ([promoted] if promoted else [])]}")
        for a in analyses:
            self.log(
                f"  {a['candidate_uid']} ({a.get('suites')}): "
                f"Δ={a['mean_delta_pp']:+.2f}pp "
                f"CI[{a['ci_lo']:+.2f},{a['ci_hi']:+.2f}] "
                f"pW={a['wilcoxon_p']:.3g} dz={a['cohens_dz']:.2f} "
                f"rt×{a['median_runtime_ratio']:.2f} → {a['decision']}")
        return analyses

    # ---------------------------------------------------------------- phases
    def phase_setup(self):
        names = self.bench.ensure_instances()
        exact_names = [n for n in names if "_n8_" in n or "_n10_" in n
                       or "_n12_" in n or "_n14_" in n]
        self.bench.set_exact_references(exact_names)
        self.db.decision("phase", {"name": "setup",
                                   "instances": len(names)})
        self.log(f"setup complete: {len(names)} instances registered")

    def phase_bks_bootstrap(self, budget_s: float = 15.0, seeds=(0, 1)):
        """Establish initial BKS references on medium+structured instances."""
        batch = "bks_bootstrap"
        seed_champ = dict(CHAMPION_SEED_CONFIG)
        uid = config_uid(seed_champ)
        cand = self.designer._wrap(
            seed_champ, family="prior",
            statement="Seed ILS configuration (double-bridge kick + "
                      "better-acceptance) establishes reference tours.",
            rationale="Classic ILS template used to bootstrap BKS.",
            expected_effect="n/a (bootstrap)", prediction="n/a")
        cand.uid = uid
        self.db.add_candidate(uid=uid, family="seed", config=cand.config,
                              hypothesis_uid=None, parent_uid="",
                              code_version="v1", git_commit=self.git)
        suites = ["medium", "structured"]
        budget_map = {"medium": budget_s, "structured": budget_s,
                      "exact": budget_s, "scale": budget_s}
        seeds_map = {s: list(seeds) for s in suites}
        n = self.bench.benchmark_candidate(
            batch, uid, cand.config, suites=suites, seeds_map=seeds_map,
            budget_map=budget_map)
        self.db.decision("phase", {"name": "bks_bootstrap", "runs": n,
                                   "budget_per_run": budget_s})
        self.log(f"BKS bootstrap done ({n} runs @ {budget_s}s)")

    def phase_baselines(self):
        """Benchmark plain LS baseline and seed ILS under full protocol."""
        batch = "phase_baselines"
        cands = []
        base_c = dict(BASELINE_CONFIG)
        cands.append(self.designer._wrap(
            base_c, family="prior",
            statement="Plain NN construction + full-scan 2-opt to convergence "
                      "is the classical baseline.",
            rationale="Croes/Lin baseline without any metaheuristic wrapper.",
            expected_effect="Reference point only.",
            prediction="Dominated by any working ILS variant at equal budget."))
        cands.append(self.designer._wrap(
            dict(CHAMPION_SEED_CONFIG), family="prior",
            statement="Basic ILS (NN + 2-opt + double-bridge kick, better-"
                      "acceptance) improves over plain LS at fixed budget.",
            rationale="Martin/Otto/Felten-style iterated local search.",
            expected_effect="+2..15pp mean excess reduction vs plain LS.",
            prediction="Wilcoxon p<0.05, positive delta across suites."))
        accepted = []
        for cand in cands:
            if self._sanity_gate(cand):
                self._register(cand)
                n = self.bench.benchmark_candidate(
                    batch, cand.uid, cand.config,
                    suites=["exact", "medium"], seeds_map=SEEDS_MAP_DEFAULT,
                    budget_map=budgets_for("exact", "medium"))
                self.db.set_candidate_status(cand.uid, "benchmarked")
                accepted.append({"uid": cand.uid, "config": cand.config,
                                 "n_runs": n})
        analyses = self.stat.analyse_batch(batch, accepted, accepted[0]["uid"],
                                           suites=("exact", "medium"))
        # initial champion = whichever baseline has lower mean excess
        self.stat.record(batch, analyses)
        best_init = min(zip(accepted, analyses),
                        key=lambda pair: pair[1]["cand_mean"])
        self.champion_uid = best_init[0]["uid"]
        self.champion_cfg = best_init[0]["config"]
        self._save_champion()
        self.db.set_candidate_status(self.champion_uid, "promoted")
        self.db.decision("phase", {
            "name": "baselines",
            "champion": self.champion_uid,
            "plain_ls_mean_excess": analyses[0]["cand_mean"],
            "ils_mean_excess": analyses[-1]["cand_mean"],
            "ils_delta_pp_vs_plain": analyses[-1]["mean_delta_pp"],
            "p_wilcoxon": analyses[-1]["wilcoxon_p"]})
        self.log(
            f"baselines: plainLS={analyses[0]['cand_mean']:.2f}% "
            f"ILS={analyses[-1]['cand_mean']:.2f}% "
            f"Δ={analyses[-1]['mean_delta_pp']:+.2f}pp "
            f"p={analyses[-1]['wilcoxon_p']:.2g} "
            f"→ champion={self.champion_uid}")
        return analyses

    def phase_ofat(self, k_new: int = 5):
        batch = f"phase_ofat_{now_iso()}"
        tried = {r["uid"] for r in self.db.query("SELECT uid FROM candidates")}
        props = self.designer.propose(self.champion_cfg, tried, k_new=k_new)
        accepted = self.run_batch(
            batch, props, ["exact", "medium"], SEEDS_MAP_DEFAULT,
            budgets_for("exact", "medium"))
        return self.analyse_and_promote(batch, accepted,
                                        ("exact", "medium"))

    def phase_explore_round(self, k_new: int = 6):
        batch = f"explore_{now_iso()}"
        tried = {r["uid"] for r in self.db.query("SELECT uid FROM candidates")}
        props = self.designer.propose(self.champion_cfg, tried, k_new=k_new)
        accepted = self.run_batch(
            batch, props, ["medium"],
            {**SEEDS_MAP_DEFAULT, "medium": list(C.SEEDS_MEDIUM)},
            budgets_for("medium"), pilot_first=True)
        return self.analyse_and_promote(batch, accepted, ("medium",))

    def phase_scale(self, alts: list[dict] | None = None):
        """Scaling study: champion vs alternates at n>=500. Descriptive."""
        batch = f"scale_{now_iso()}"
        tried = {r["uid"] for r in self.db.query("SELECT uid FROM candidates")}
        if alts is None:
            rows = self.db.query(
                """SELECT DISTINCT candidate_uid FROM runs
                   WHERE instance_id IN (SELECT id FROM instances WHERE n>=50)
                   GROUP BY candidate_uid""")
            alts = [{"uid": r["candidate_uid"]} for r in rows][:3]
        uids = [self.champion_uid] + [a["uid"] for a in alts]
        uids = [u for i, u in enumerate(uids) if u and u not in uids[:i]]
        out = {}
        for uid in uids:
            row = self.db.one("SELECT config_json FROM candidates WHERE uid=?",
                              (uid,))
            if not row:
                continue
            cfg = json.loads(row["config_json"])
            n = self.bench.benchmark_candidate(
                batch, uid, cfg, ["scale"], seeds_map={"scale": [0, 1, 2]},
                budget_map={"scale": C.DEFAULT_BUDGETS.scale})
            out[uid] = n
        # descriptive comparison (no promotion from scale suite)
        ex_champ, rt_c, _ = self.db.excess_lookup(self.champion_uid)
        scale_pairs_c = {k: v for k, v in ex_champ.items()
                         if int(k[0].split("_n")[1].split("_")[0]) >= 500}
        summary = {}
        for uid in out:
            if uid == self.champion_uid:
                continue
            ex_a, rt_a, _ = self.db.excess_lookup(uid)
            pairs = {k: v for k, v in ex_a.items()
                     if k in scale_pairs_c}
            if pairs:
                d = np.mean([scale_pairs_c[k] - v for k, v in pairs.items()])
                summary[uid] = {"mean_delta_pp_vs_champ": round(float(d), 3),
                                "n_pairs": len(pairs)}
        self.db.decision("phase", {"name": "scale", "summary": summary})
        self.log(f"scale study: {summary}")
        return summary

    def phase_robustness(self):
        """Champion vs strongest challenger on clustered/grid distributions."""
        batch = f"robust_{now_iso()}"
        row = self.db.one(
            """SELECT candidate_uid, AVG(mean_delta_pp) AS md FROM analyses
               WHERE decision='promote' OR holm_reject=1
               GROUP BY candidate_uid ORDER BY md DESC LIMIT 2""")
        challengers = []
        if row and row["candidate_uid"] != self.champion_uid:
            crow = self.db.one("SELECT config_json FROM candidates WHERE uid=?",
                               (row["candidate_uid"],))
            challengers.append(json.loads(crow["config_json"]))
        if not challengers:
            challengers = [dict(CHAMPION_SEED_CONFIG)]
        cands = []
        for i, cfg in enumerate(challengers):
            cands.append(self.designer._wrap(
                cfg, family="robustness_probe",
                statement=f"Challenger {i} generalises to structured "
                          f"distributions.",
                rationale="Rankings can flip across distributions; direct test.",
                expected_effect="unknown", prediction="descriptive"))
        accepted = self.run_batch(
            batch, cands, ["structured"], SEEDS_MAP_DEFAULT,
            budgets_for("structured"))
        return self.analyse_and_promote(batch, accepted, ("structured",))
