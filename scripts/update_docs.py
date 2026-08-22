#!/usr/bin/env python3
"""Regenerate EXPERIMENTS.md + experiment graph from the database."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np  # noqa: E402

from ais.db import ExperimentDB  # noqa: E402
from ais.utils import now_iso  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def fmt(x, nd=2):
    if x is None:
        return "—"
    try:
        return f"{float(x):.{nd}f}"
    except Exception:
        return str(x)


def main():
    db = ExperimentDB()
    lines = ["# Experiments", "",
             f"_Regenerated from `results/experiments.db` at {now_iso()}._",
             ""]

    # ---------------- campaign summary --------------------------------
    n_cand = db.one("SELECT COUNT(*) c FROM candidates")["c"]
    n_runs = db.one("SELECT COUNT(*) c FROM runs")["c"]
    n_hyp = db.one("SELECT COUNT(*) c FROM hypotheses")["c"]
    n_promo = db.one(
        "SELECT COUNT(*) c FROM decisions WHERE kind='champion_promotion'")["c"]
    lines += [
        "## Campaign summary",
        "",
        f"| metric | value |",
        f"|---|---|",
        f"| candidates registered | {n_cand} |",
        f"| pre-registered hypotheses | {n_hyp} |",
        f"| raw runs | {n_runs} |",
        f"| champion promotions (rule-based) | {n_promo} |",
        "",
    ]

    # ---------------- champion lineage ---------------------------------
    rows = db.query(
        "SELECT payload_json FROM decisions WHERE kind='champion_promotion'")
    if rows:
        lines += ["## Champion lineage (each step = statistically-gated promotion)",
                  "", "| batch | candidate | Δpp | CI | p(Wilcoxon) | dz |",
                  "|---|---|---|---|---|---|"]
        for r in rows:
            p = json.loads(r["payload_json"])
            lines.append(
                f"| {p.get('batch','')} | `{p['uid']}` | {fmt(p.get('delta_pp'))} "
                f"| [{fmt(p.get('ci',[None,None])[0])}, {fmt(p.get('ci',[None,None])[1])}] "
                f"| {fmt(p.get('p_wilcoxon'), 4)} | {fmt(p.get('dz'))} |")
        lines.append("")

    # ---------------- analyses table ------------------------------------
    rows = db.query("SELECT * FROM analyses ORDER BY id")
    if rows:
        lines += ["## All paired analyses vs incumbent champion", "",
                  "| batch | candidate | suites | n | base% | cand% | Δpp [CI] "
                  "| pW | pT | dz | win | rt× | decision |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            ep = json.loads(r["endpoint_json"]) or {}
            lines.append(
                f"| {r['batch_id']} | `{r['candidate_uid']}` "
                f"| {','.join(ep.get('suites', []))} | {r['n_pairs']} "
                f"| {fmt(r['base_mean_excess'])} | {fmt(r['cand_mean_excess'])} "
                f"| **{fmt(r['mean_delta_pp'])}** [{fmt(r['ci_lo'])},{fmt(r['ci_hi'])}] "
                f"| {fmt(r['wilcoxon_p'],4)} | {fmt(r['ttest_p'],4)} "
                f"| {fmt(r['cohens_dz'])} | {fmt(r['win_rate'])} "
                f"| {fmt(r['median_runtime_ratio'])} | {r['decision']} |")
        lines.append("")

    # ---------------- experiment graph -----------------------------------
    cands = db.query(
        "SELECT uid, family, parent_uid, status FROM candidates ORDER BY id")
    hyps = {h["uid"]: h for h in db.query("SELECT * FROM hypotheses")}
    if cands:
        lines += ["## Experiment graph", "",
                  "Edges: `parent → candidate` shows derivation; each node "
                  "links its hypothesis and outcome.", "```mermaid",
                  "graph TD"]
        for c in cands:
            label = f'{c["uid"]} [{c["family"]}\\n{c["status"]}]'
            parent = c["parent_uid"] or "ROOT"
            lines.append(f'  {parent} --> "{label}"')
        lines.append("```")
        lines.append("")
        lines += ["### Hypothesis ledger", "",
                  "| uid | statement | expected | prediction |",
                  "|---|---|---|---|"]
        for uid, h in list(hyps.items())[:80]:
            st = h["statement"].replace("|", "/")
            lines.append(f"| `{uid}` | {st} | {h['expected_effect'].replace('|','/')} "
                         f"| {h['prediction'].replace('|','/')} |")
        lines.append("")

    # ---------------- critique digest ------------------------------------
    rows = db.query("SELECT * FROM critiques WHERE finding LIKE "
                    "'failure_analysis%' ORDER BY id DESC LIMIT 40")
    if rows:
        lines += ["## Critic failure analyses (why candidates were not adopted)",
                  ""]
        for r in rows:
            lines.append(f"- `{r['candidate_uid']}`: {r['finding']}")
        lines.append("")

    (ROOT / "EXPERIMENTS.md").write_text("\n".join(lines))
    print(f"EXPERIMENTS.md regenerated ({len(lines)} lines)")


if __name__ == "__main__":
    main()
