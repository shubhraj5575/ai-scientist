#!/usr/bin/env python3
"""Post-artifact-A1 revalidation: clean answers under fixed local search.

Questions:
  R1: value of ILS kicks vs plain LS (two_opt only), fixed code
  R2: value of richer composite LS ([two_opt,+or_opt]) without kicks
  R3: do the explore-round winners survive re-benchmarking?
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ais.agents.director import Director, budgets_for  # noqa: E402


def main():
    d = Director()
    batch = "postfix_revalidation_A1"

    cands = []
    mk = d.designer._wrap

    # R1a: no-kick plain two_opt (isolates kick contribution cleanly)
    cfg_nokick = {"construction": "nn", "ls_operators": ["two_opt"],
                  "nl_k": None, "perturbation": None}
    cands.append(mk(cfg_nokick, family="revalidation",
                    statement="R1: plain NN+2opt vs champion ILS (fixed code).",
                    rationale="Clean kick-contribution estimate post-A1.",
                    expected_effect="negative delta expected",
                    prediction="significantly worse than champion"))
    # R2: composite two_opt+or_opt, no kicks
    cfg_comp = {"construction": "nn", "ls_operators": ["two_opt", "or_opt"],
                "nl_k": None, "perturbation": None}
    cands.append(mk(cfg_comp, family="revalidation",
                    statement="R2: composite LS without kicks.",
                    rationale="Isolate composite-LS contribution post-A1.",
                    expected_effect="unknown; prior contaminated",
                    prediction="records clean composite-only effect"))
    # R3: strongest explore-round winners, now with working or_opt
    for uid in ("C-3f9cba2784", "C-daf5979f68"):
        row = d.db.one("SELECT config_json FROM candidates WHERE uid=?", (uid,))
        if row:
            cfg = json.loads(row["config_json"])
            cands.append(mk(cfg, family="revalidation",
                            statement=f"Re-benchmark {uid} post-A1 fix.",
                            rationale="Prior +0.13pp result was contaminated.",
                            expected_effect="unknown",
                            prediction="survives or fails cleanly"))

    accepted = d.run_batch(batch, cands, ["medium"],
                           {"exact": [], "medium": list(__import__("ais.config", fromlist=["SEEDS_MEDIUM"]).SEEDS_MEDIUM),
                            "structured": [], "scale": []},
                           budgets_for("medium"), pilot_first=False)
    d.analyse_and_promote(batch, accepted, ("medium",))


if __name__ == "__main__":
    main()
