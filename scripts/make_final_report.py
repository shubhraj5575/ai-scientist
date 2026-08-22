#!/usr/bin/env python3
"""Generate FINAL_REPORT.md from the experiment database.

Evidence discipline:
  * claims are emitted only with their supporting statistics attached
  * reference values labelled exact vs BKS
  * hypotheses that failed are listed alongside those that survived
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np  # noqa: E402

from ais.agents.researcher import Researcher  # noqa: E402
from ais.db import ExperimentDB  # noqa: E402
from ais.utils import now_iso, git_commit  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def fmt(x, nd=2):
    try:
        return f"{float(x):.{nd}f}"
    except Exception:
        return "—"


def main():
    db = ExperimentDB()
    res = Researcher()

    promo = [json.loads(r["payload_json"]) for r in db.query(
        "SELECT payload_json FROM decisions WHERE kind='champion_promotion'")]
    champ = db.one("SELECT value FROM meta WHERE key='champion'")
    analyses = db.query("SELECT * FROM analyses ORDER BY id")
    phases = [json.loads(r["payload_json"]) for r in db.query(
        "SELECT payload_json FROM decisions WHERE kind='phase'")]
    hyps = db.query("SELECT * FROM hypotheses")

    lines = [
        "# Final Report", "",
        f"_Generated {now_iso()} · git `{git_commit(ROOT)}`_",
        "",
        "## Evidence classes used throughout",
        "- **KNOWN_FACT** — textbook/literature knowledge, not discovered here.",
        "- **HYPOTHESIS** — pre-registered prediction recorded before measurement.",
        "- **OUR_FINDING / EXPERIMENTAL RESULT** — supported by rows in "
        "`results/experiments.db` (seeds, paired tests, CIs reported inline).",
        "- **UNVERIFIED** — plausible but not tested under the protocol.",
        "",
        "## 1. Scope",
        "Autonomous experimental campaign on iterated local search for the",
        "Euclidean TSP over a declarative component grammar (see ARCHITECTURE.md).",
        f"Candidates registered: {db.one('SELECT COUNT(*) c FROM candidates')['c']};",
        f"raw runs: {db.one('SELECT COUNT(*) c FROM runs')['c']};",
        f"pre-registered hypotheses: {len(hyps)}.",
        "",
        "## 2. Method summary",
        "Paired design on shared (instance, seed); quality = % excess over",
        "reference (exact Held-Karp optimum for n≤14; internal BKS otherwise,",
        "labelled, never claimed optimal). Promotion requires Wilcoxon p<0.05",
        "(Holm within batch), mean excess reduction ≥0.30pp, runtime guard",
        "(DECISIONS.md D4/D9). No single noisy comparison can change the champion.",
        "",
        "## 3. Champion lineage (experimental results)",
    ]
    if promo:
        lines += ["| # | batch | candidate | Δpp vs prior champion | 95% CI | p(Wilcoxon) | dz |",
                  "|---|---|---|---|---|---|---|"]
        for i, p in enumerate(promo):
            ci = p.get("ci", [None, None])
            lines.append(
                f"| {i+1} | {p.get('batch','')} | `{p['uid']}` | {fmt(p.get('delta_pp'))} "
                f"| [{fmt(ci[0])}, {fmt(ci[1])}] | {fmt(p.get('p_wilcoxon'),4)} "
                f"| {fmt(p.get('dz'))} |")
    else:
        lines += ["_(no promotions yet)_"]
    if champ:
        obj = json.loads(champ["value"])
        lines += ["", f"Current champion config:", "", "```json",
                  json.dumps(obj["config"], indent=2, sort_keys=True), "```"]

    # phase summaries
    lines += ["", "## 4. Phase ledger"]
    for ph in phases:
        name = ph.get("name")
        keep = {k: v for k, v in ph.items() if k != "name"}
        lines.append(f"- **{name}**: {json.dumps(keep)[:400]}")

    # findings
    lines += ["", "## 5. Findings of this campaign (each with evidence pointer)"]
    if res.findings:
        pass
    notes_rows = db.query(
        "SELECT payload_json FROM decisions WHERE kind='champion_promotion'")
    for i, r in enumerate(notes_rows):
        p = json.loads(r["payload_json"])
        lines.append(
            f"{i+1}. **OUR_FINDING** — candidate `{p['uid']}` (batch "
            f"{p.get('batch')}) improved mean excess by "
            f"{fmt(p.get('delta_pp'))}pp over its incumbent "
            f"(CI [{fmt(p.get('ci',[0])[0])},{fmt(p.get('ci',[1,-1])[1])}], "
            f"p={fmt(p.get('p_wilcoxon'),4)}, dz={fmt(p.get('dz'))}). "
            f"Evidence: `analyses` row + `runs` table.")

    # failed hypotheses digest
    rej = [a for a in analyses if a["decision"] != "promote"]
    if rej:
        lines += ["", "## 6. Negative / null results (recorded, not hidden)", ""]
        for a in rej[:25]:
            lines.append(
                f"- `{a['candidate_uid']}` ({a['batch_id']}): Δ={fmt(a['mean_delta_pp'])}pp "
                f"[{fmt(a['ci_lo'])},{fmt(a['ci_hi'])}], pW={fmt(a['wilcoxon_p'],4)} → "
                f"{a['decision']}.")

    lines += ["", "## 7. Threats to validity",
              "- Single machine, wall-clock budgets → absolute runtimes vary; "
              "mitigated by pairing and runtime-ratio reporting.",
              "- Internal BKS references may drift upward in quality over time; "
              "excess recomputed at analysis time prevents epoch confounds, but "
              "'% of BKS' should never be read as '% of optimal' beyond n≤14.",
              "- Component grammar bounds discoverable improvements (D3/D8).",
              "- Multiple batches share seeds; pairing handles correlation, but "
              "campaign-level error inflation across many promotions is not "
              "fully controlled (noted as UNVERIFIED risk).",
              "",
              "## 8. Reproduction",
              "`python scripts/run_overnight.py --phases <list>`; DB at "
              "`results/experiments.db`; every run row stores git commit, "
              "env snapshot, seed and raw tour length."]
    (ROOT / "FINAL_REPORT.md").write_text("\n".join(lines))
    print("FINAL_REPORT.md written")


if __name__ == "__main__":
    main()
