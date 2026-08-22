# AI Scientist — Autonomous Experimental Algorithm Research

An autonomous computational-scientist system that runs a closed research loop:
**literature → baseline → hypothesis → candidate → benchmark → analysis →
critique → modification → repeat**, with an experiment database, pre-registered
statistics protocol, and full provenance for every reported number.

**First research domain:** Euclidean Travelling Salesman Problem — local
search / Iterated Local Search (ILS). Chosen because baselines are strong and
well documented, single experiments run in seconds (enabling hundreds of
controlled comparisons), and quality is exactly quantifiable as % excess over
a reference solution.

## Status

Live research log: [`OVERNIGHT_LOG.md`](OVERNIGHT_LOG.md) ·
Current evidence table: [`EXPERIMENTS.md`](EXPERIMENTS.md) ·
Design rationale: [`DECISIONS.md`](DECISIONS.md) ·
Synthesis: [`FINAL_REPORT.md`](FINAL_REPORT.md)

## Quick start

```bash
pip install -r requirements.txt   # numpy (+ pytest, matplotlib)
python -m pytest tests/ -q        # 20 correctness tests must pass first
python scripts/run_overnight.py --budget-hours 8 --phases all
```

## What is honest here

* Everything labelled **KNOWN_FACT** comes from textbook-level literature
  knowledge encoded by the Researcher agent (Bentley 1992, Johnson & McGeoch
  1997, Lourenço/Martin/Stützle 2003, etc.) — not discovered by this system.
* Everything labelled **OUR_FINDING** is supported by paired experiments in
  `results/experiments.db` with seeds, effect sizes, confidence intervals,
  Wilcoxon p-values and Holm correction. Queryable via SQLite.
* **HYPOTHESIS** rows are pre-registered before measurement; their verdicts
  are recorded whether they survive or not.
* Internal reference solutions on instances where optimality is unknown are
  labelled BKS ("best known so far *within this project*") and never treated
  as proven optima.

## Repository layout

See [ARCHITECTURE.md](ARCHITECTURE.md).
