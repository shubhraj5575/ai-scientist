#!/usr/bin/env python3
"""Does the promotion survive a 3x budget? Champion vs pre-promotion champion."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from ais.agents.benchmarker import BenchmarkEngineer  # noqa: E402
from ais.config import SEEDS_MEDIUM  # noqa: E402
from ais.db import ExperimentDB  # noqa: E402
from ais.utils import now_iso  # noqa: E402


def main():
    db = ExperimentDB()
    bench = BenchmarkEngineer(db)
    champ = db.one("SELECT value FROM meta WHERE key='champion'")
    uid_c = json.loads(champ["value"])["uid"]
    uid_old = "C-31e4c0b1a6"          # pre-promotion champion (seed ILS)
    uids = [uid_c, uid_old]
    cfgs = {}
    for uid in uids:
        row = db.one("SELECT config_json FROM candidates WHERE uid=?", (uid,))
        cfgs[uid] = json.loads(row["config_json"])

    batch = f"longbudget_{now_iso()}"
    seeds_map = {"medium": list(SEEDS_MEDIUM), "exact": [], "structured": [],
                 "scale": []}
    budgets = {"medium": 9.0, "exact": 4.5, "structured": 9.0, "scale": 45.0}
    for uid, cfg in cfgs.items():
        bench.benchmark_candidate(batch, uid + "@x3", cfg, ["medium"],
                                  seeds_map, budgets)

    ex = {uid: db.excess_lookup(uid + "@x3")[0] for uid in uids}
    keys = sorted(set(ex[uid_c]) & set(ex[uid_old]))
    d = np.array([ex[uid_old][k] - ex[uid_c][k] for k in keys])
    from ais.stats import paired_ttest, wilcoxon_signed_rank, mean_ci_bootstrap
    t, tp = paired_ttest(d)
    z, wp = wilcoxon_signed_rank(d)
    lo, hi = mean_ci_bootstrap(d, B=4000)
    out = {"n": len(keys), "mean_delta_pp": float(d.mean()),
           "ci": [float(lo), float(hi)], "wilcoxon_p": wp,
           "win_rate": float((d > 0).mean())}
    db.decision("phase", {"name": "promotion_survives_3x_budget",
                          "result": out})
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
