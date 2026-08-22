#!/usr/bin/env python3
"""Budget-sensitivity check: does the champion's ranking vs a fixed rival
hold when budgets are multiplied? Guards conclusion (D9 risk)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from ais.agents.benchmarker import BenchmarkEngineer
from ais.agents.statistician import Statistician, _suite_of
from ais.config import DEFAULT_BUDGETS as B, SEEDS_MEDIUM
from ais.db import ExperimentDB
from ais.utils import now_iso


def main():
    db = ExperimentDB()
    bench = BenchmarkEngineer(db)
    stat = Statistician(db)
    champ = json.loads(db.one("SELECT value FROM meta WHERE key='champion'")["value"])
    uid_c = champ["uid"]
    row_c = db.one("SELECT config_json FROM candidates WHERE uid=?", (uid_c,))
    cfgs = {uid_c: json.loads(row_c["config_json"])}
    # strongest non-promoted challenger with most runs
    rows = db.query(
        """SELECT candidate_uid, COUNT(*) c FROM runs WHERE candidate_uid != ?
           GROUP BY candidate_uid ORDER BY c DESC LIMIT 5""", (uid_c,))
    for r in rows:
        cr = db.one("SELECT config_json FROM candidates WHERE uid=?",
                    (r["candidate_uid"],))
        if cr:
            cfgs[r["candidate_uid"]] = json.loads(cr["config_json"])
            if len(cfgs) >= 2:
                break
    if len(cfgs) < 2:
        print("not enough candidates for budget check")
        return

    batch = f"budget_check_{now_iso()}"
    mults = [1.0, 3.0]
    seeds_map = {"medium": list(SEEDS_MEDIUM), "exact": [],
                 "structured": [], "scale": []}
    for mult in mults:
        budgets = {"medium": B.medium * mult, "exact": B.exact_suite * mult,
                   "structured": B.structured * mult, "scale": B.scale}
        for uid, cfg in cfgs.items():
            bench.benchmark_candidate(f"{batch}_x{mult:g}", uid + f"@x{mult:g}",
                                      cfg, ["medium"], seeds_map, budgets)
    # analyse at each multiplier
    out = {}
    uids = list(cfgs)
    for mult in mults:
        ex_a, _, _ = db.excess_lookup(uids[0] + f"@x{mult:g}")
        ex_b, _, _ = db.excess_lookup(uids[1] + f"@x{mult:g}")
        keys = sorted(set(ex_a) & set(ex_b))
        d = np.mean([ex_a[k] - ex_b[k] for k in keys])
        out[f"x{mult:g}"] = {"delta_pp": round(float(d), 3), "n": len(keys)}
    db.decision("phase", {"name": "budget_sensitivity", "result": out,
                          "uids": uids})
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
