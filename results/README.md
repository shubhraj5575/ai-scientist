# Results / Evidence

* `experiments.db` — SQLite experiment database (schema in `ais/db.py`).
  This is the primary evidence store; every number in the reports traces to
  rows here. WAL/SHM sidecars are transient.
* `evidence_export.json` — portable export of hypotheses, candidates,
  analyses, critiques, decisions, reference values, instances.
* `runs_export.csv.gz` — all 16,410 raw runs (one row per candidate ×
  instance × seed: length, runtime, kicks, git commit, env snapshot).
* `phase_*.log`, `budget_check.log`, `longbudget.log` — runner console logs.

Reproduce from scratch: `python scripts/run_overnight.py --phases all`.
