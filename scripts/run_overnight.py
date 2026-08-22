#!/usr/bin/env python3
"""Autonomous overnight research runner.

Usage:
    python scripts/run_overnight.py --budget-hours 8 --phases all
    python scripts/run_overnight.py --phases setup,baselines   # resume
"""
from __future__ import annotations

import argparse
import time

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))

from ais.agents.director import Director  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget-hours", type=float, default=8.0)
    ap.add_argument("--phases", type=str, default="all")
    args = ap.parse_args()

    d = Director()
    phases = (["setup", "bks", "baselines", "ofat", "explore", "scale",
               "robust"] if args.phases == "all" else args.phases.split(","))

    d.log(f"campaign run started: phases={phases} budget={args.budget_hours}h")

    for phase in phases:
        t0 = time.time()
        try:
            if phase == "setup":
                d.phase_setup()
            elif phase == "bks":
                d.phase_bks_bootstrap(budget_s=15.0)
            elif phase == "baselines":
                d.phase_baselines()
            elif phase == "ofat":
                for i in range(2):
                    d.phase_ofat(k_new=5)
            elif phase == "explore":
                while d.remaining_s(args.budget_hours) > 40 * 60:
                    d.phase_explore_round(k_new=6)
                    d.commit_push(f"explore round @ {phase}")
            elif phase == "scale":
                d.phase_scale()
            elif phase == "robust":
                d.phase_robustness()
            else:
                print(f"unknown phase {phase}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            d.log(f"PHASE {phase} FAILED: {e}")
        d.commit_push(f"phase {phase} complete")
        print(f"[phase {phase}] took {time.time()-t0:.0f}s")

    d.commit_push("overnight campaign checkpoint")
    print("done")


if __name__ == "__main__":
    main()
