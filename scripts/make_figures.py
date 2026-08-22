#!/usr/bin/env python3
"""Plot experiment-graph figure + excess-over-time chart from the DB."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from ais.db import ExperimentDB  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FIGS = ROOT / "docs"
FIGS.mkdir(exist_ok=True)


def graph_figure(db):
    cands = db.query("SELECT uid, family, parent_uid, status FROM candidates ORDER BY id")
    if not cands:
        print("no candidates yet")
        return
    fam_color = {"prior": "#4C72B0", "mutation": "#DD8452",
                 "bandit": "#55A868", "seed": "#8172B3"}
    # layered layout: ROOT then by registration order (columns)
    levels = {}
    for i, c in enumerate(cands):
        parent = c["parent_uid"] or "ROOT"
        levels[c["uid"]] = levels.get(parent, -1) + 1 if parent in levels else \
            max([levels.get(c["parent_uid"], -1)]) + 1
    fig, ax = plt.subplots(figsize=(max(8, len(cands) * 0.7), 6))
    pos = {}
    per_level = {}
    for c in cands:
        lv = levels.get(c["uid"], 0)
        per_level.setdefault(lv, []).append(c["uid"])
    for lv, uids in per_level.items():
        for j, uid in enumerate(uids):
            pos[uid] = (lv, j - (len(uids) - 1) / 2)
    pos["ROOT"] = (-1, 0)
    for c in cands:
        parent = c["parent_uid"] or "ROOT"
        x0, y0 = pos[parent]
        x1, y1 = pos[c["uid"]]
        ax.plot([x0, x1], [y0, y1], "-", color="#bbbbbb", lw=0.8, zorder=1)
        color = fam_color.get(c["family"], "#999999")
        edge = "#2ca02c" if c["status"] == "promoted" else (
            "#d62728" if c["status"] == "rejected" else "white")
        ax.scatter([x1], [y1], s=260, c=color, edgecolors=edge,
                   linewidths=2.2 if edge != "white" else 0.8, zorder=2)
    ax.set_yticks([])
    ax.set_xticks(sorted({p[0] for p in pos.values()}))
    ax.set_xlabel("derivation depth →")
    ax.set_title("Experiment graph (colour=family, green ring=promoted, red=rejected)")
    handles = [plt.Line2D([], [], marker="o", ls="", color=v, label=k)
               for k, v in fam_color.items()]
    ax.legend(handles=handles, loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGS / "experiment_graph.png", dpi=130)
    plt.close(fig)
    print("docs/experiment_graph.png written")


def main():
    db = ExperimentDB()
    graph_figure(db)


if __name__ == "__main__":
    main()
