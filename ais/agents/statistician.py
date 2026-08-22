"""Statistician agent: paired analyses vs incumbent champion, Holm
correction across each batch, bootstrap CIs, effect sizes, and the
pre-registered champion-promotion decision rule.

DECISION RULE (fixed a priori — DECISIONS.md D4):
  promote candidate IFF (all of)
    1. Wilcoxon two-sided p < alpha after Holm correction within batch
    2. mean excess reduction >= min_effect_pp (practical significance)
    3. median runtime ratio <= max_runtime_ratio, UNLESS the effect is at
       least bigwin_factor * min_effect_pp, in which case up to
       max_runtime_ratio_bigwin is tolerated.
Ties on quality favour the FASTER solver; if both criteria fail the
champion is retained.
"""
from __future__ import annotations

import numpy as np

from ..config import DEFAULT_PROTOCOL as P
from ..stats import analyse_paired, holm_bonferroni


class Statistician:
    def __init__(self, db):
        self.db = db

    def analyse_batch(self, batch_id: str, candidates: list[dict],
                      baseline_uid: str,
                      suites: tuple[str, ...] = ("exact", "medium"),
                      runtime_guard: bool = True) -> list[dict]:
        """Paired analysis of each candidate vs baseline over shared pairs."""
        base_ex, base_rt, _ = self.db.excess_lookup(baseline_uid)
        results = []
        for cand in candidates:
            uid = cand["uid"]
            cand_ex, cand_rt, _ = self.db.excess_lookup(uid)
            keys = sorted(set(cand_ex) & set(base_ex))
            keys = [k for k in keys if k[0].rsplit("_n", 1)[-1].split("_")[0].isdigit()
                    and _suite_of(k[0]) in suites]
            if not keys:
                continue
            cand_vals = {k: cand_ex[k] for k in keys}
            base_vals = {k: base_ex[k] for k in keys}
            stats = analyse_paired(cand_vals, base_vals,
                                   bootstrap_B=P.bootstrap_B)
            rt_ratios = [cand_rt[k] / max(base_rt[k], 1e-9) for k in keys
                         if k in cand_rt and k in base_rt]
            med_rt = float(np.median(rt_ratios)) if rt_ratios else float("nan")
            results.append({
                "batch_id": batch_id,
                "candidate_uid": uid,
                "baseline_uid": baseline_uid,
                **stats,
                "median_runtime_ratio": med_rt,
                "suites": sorted({_suite_of(k[0]) for k in keys}),
            })

        # Holm correction within this batch
        pvals = [r["wilcoxon_p"] for r in results]
        rejects = holm_bonferroni(pvals, alpha=P.alpha)
        for r, rej in zip(results, rejects):
            r["holm_reject"] = rej

        for r in results:
            r["decision"] = self._decide(r)
        return results

    def _decide(self, r: dict) -> str:
        sig = r["holm_reject"]
        effect_ok = r["mean_delta_pp"] >= P.min_effect_pp
        big_win = r["mean_delta_pp"] >= P.bigwin_factor * P.min_effect_pp
        rt = r["median_runtime_ratio"]
        rt_cap = P.max_runtime_ratio_bigwin if big_win else P.max_runtime_ratio
        rt_ok = (not np.isfinite(rt)) or rt <= rt_cap
        if sig and effect_ok and rt_ok:
            return "promote"
        if sig and effect_ok:
            return f"reject_on_runtime(ratio={rt:.2f}>cap={rt_cap:.2f})"
        if sig:
            return "significant_but_not_practical"
        if effect_ok:
            return "practical_but_not_significant"
        return "no_change"

    def record(self, batch_id: str, analyses: list[dict]):
        for r in analyses:
            self.db.add_analysis(
                batch_id=r["batch_id"], candidate_uid=r["candidate_uid"],
                baseline_uid=r["baseline_uid"], n_pairs=r["n_pairs"],
                cand_mean=r["cand_mean"], base_mean=r["base_mean"],
                mean_delta_pp=r["mean_delta_pp"], ci_lo=r["ci_lo"],
                ci_hi=r["ci_hi"], cohens_dz=r["cohens_dz"], t_stat=r["t_stat"],
                ttest_p=r["ttest_p"], wilcoxon_z=r["wilcoxon_z"],
                wilcoxon_p=r["wilcoxon_p"], holm_reject=r["holm_reject"],
                win_rate=r["win_rate"],
                median_runtime_ratio=r["median_runtime_ratio"],
                decision=r["decision"],
                endpoint={"suites": r.get("suites", [])},
            )


def _suite_of(instance_name: str) -> str:
    kind = instance_name.split("_")[0]
    n = int(instance_name.split("_n")[1].split("_")[0])
    if kind == "uniform" and n <= 14:
        return "exact"
    if kind == "uniform":
        return "medium"
    return "structured"
