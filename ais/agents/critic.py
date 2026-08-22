"""Critic agent: adversarial review of batches before decisions are taken.

Checks:
  * protocol completeness (all planned seeds/instances present)
  * runtime sanity (no run wildly exceeding budget; flag >1.5x)
  * variance anomalies (seed spread explodes vs baseline -> possible
    nondeterminism or budget truncation effects)
  * reference integrity (NaN excesses, missing references)
  * failure recording: for rejected candidates, writes a structured
    'why it failed' note consumed by the Designer's bandit.
"""
from __future__ import annotations

import numpy as np


class Critic:
    def __init__(self, db):
        self.db = db

    def review_batch(self, batch_id: str, candidate_uids: list[str],
                     planned_seeds: int, analyses: list[dict]) -> list[str]:
        findings: list[str] = []
        for uid in candidate_uids:
            rows = self.db.query(
                """SELECT r.*, i.name AS iname FROM runs r
                   JOIN instances i ON i.id=r.instance_id
                   WHERE r.batch_id=? AND r.candidate_uid=?""",
                (batch_id, uid))
            if not rows:
                self.db.add_critique(batch_id, uid, "blocking",
                                     "no runs recorded")
                continue

            # completeness per instance
            by_inst: dict[str, list] = {}
            for r in rows:
                by_inst.setdefault(r["iname"], []).append(r)
            for iname, rs in sorted(by_inst.items()):
                if len(rs) != planned_seeds:
                    findings.append(
                        f"{uid}: {iname} has {len(rs)}/{planned_seeds} seeds")
                over = [r["runtime_s"] / r["budget_s"] for r in rs]
                if max(over) > 1.5:
                    findings.append(
                        f"{uid}: {iname} budget overrun "
                        f"{max(over):.2f}x")
            # nan excesses
            nans = [r for r in rows if not np.isfinite(r["excess_pct"])]
            if nans:
                findings.append(f"{uid}: {len(nans)} runs without reference")

            # seed-spread anomaly vs baseline on shared instances
            a = next((x for x in analyses if x["candidate_uid"] == uid), None)
            if a and a["n_pairs"] >= 8:
                spread_note = (
                    f"{uid}: win_rate={a['win_rate']:.2f}, "
                    f"dz={a['cohens_dz']:.2f}")
                if abs(a["cohens_dz"]) < 0.15 and a["holm_reject"]:
                    findings.append(
                        f"{spread_note} -- significant p but tiny effect; "
                        f"verify practical relevance")
            # record failure rationale for the designer
            if a and a["decision"].startswith(("reject", "no_change",
                                               "significant_but",
                                               "practical_but")):
                why = _failure_rationale(a)
                self.db.add_critique(batch_id, uid, "info",
                                     "failure_analysis: " + why)

        for f in findings:
            sev = "warning" if ("budget" in f or "seeds" in f) else "info"
            self.db.add_critique(batch_id, "*", sev, f)
        return findings


def _failure_rationale(a: dict) -> str:
    parts = [f"delta_pp={a['mean_delta_pp']:+.3f} "
             f"[{a['ci_lo']:+.3f},{a['ci_hi']:+.3f}]",
             f"win={a['win_rate']:.2f}", f"dz={a['cohens_dz']:.2f}",
             f"p_w={a['wilcoxon_p']:.3g}",
             f"rt_x={a['median_runtime_ratio']:.2f}"]
    verdict = a["decision"]
    return "; ".join(parts) + f" => {verdict}"
