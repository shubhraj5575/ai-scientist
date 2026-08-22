"""SQLite experiment database: full provenance for every number we report.

Tables
------
meta            : schema version + key facts
instances       : generated problem instances (digest = identity)
reference_vals  : per-instance reference objective ('exact' or 'bks')
hypotheses      : designer's falsifiable predictions (pre-registered)
candidates      : declarative solver configs under test
runs            : raw measurements, one row per (candidate, instance, seed)
analyses        : statistician's paired comparisons vs incumbent champion
critiques       : critic findings per candidate/batch
decisions       : director decisions (champion promotion, phase events)
"""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any

from .config import DB_PATH
from .utils import now_iso

SCHEMA_VERSION = 1

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS meta(
  key TEXT PRIMARY KEY, value TEXT);

CREATE TABLE IF NOT EXISTS instances(
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  kind TEXT NOT NULL,
  n INTEGER NOT NULL,
  seed INTEGER NOT NULL,
  params_json TEXT NOT NULL,
  digest TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reference_vals(
  instance_id INTEGER NOT NULL REFERENCES instances(id),
  kind TEXT NOT NULL,               -- 'exact' | 'bks'
  value REAL NOT NULL,
  source TEXT NOT NULL,             -- e.g. 'held_karp' | 'best_of_all_runs'
  provenance TEXT NOT NULL,         -- run/candidate that achieved it (for bks)
  updated_at TEXT NOT NULL,
  PRIMARY KEY (instance_id, kind)
);

CREATE TABLE IF NOT EXISTS hypotheses(
  id INTEGER PRIMARY KEY,
  uid TEXT UNIQUE NOT NULL,
  statement TEXT NOT NULL,
  rationale TEXT NOT NULL,
  expected_effect TEXT NOT NULL,
  prediction TEXT NOT NULL,
  literature_basis TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS candidates(
  id INTEGER PRIMARY KEY,
  uid TEXT UNIQUE NOT NULL,
  family TEXT NOT NULL,
  config_json TEXT NOT NULL,
  config_digest TEXT NOT NULL,
  hypothesis_uid TEXT REFERENCES hypotheses(uid),
  parent_uid TEXT,
  code_version TEXT NOT NULL,
  git_commit TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'proposed',   -- proposed|pilot|benchmarked|rejected|promoted
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS runs(
  id INTEGER PRIMARY KEY,
  batch_id TEXT NOT NULL,
  candidate_uid TEXT NOT NULL,
  instance_id INTEGER NOT NULL REFERENCES instances(id),
  seed INTEGER NOT NULL,
  budget_s REAL NOT NULL,
  length REAL NOT NULL,
  excess_pct REAL,                  -- NULL when no reference existed yet
  runtime_s REAL NOT NULL,
  kicks INTEGER NOT NULL,
  ls_moves INTEGER NOT NULL,
  restarts INTEGER NOT NULL,
  peak_rss_mb REAL NOT NULL,
  git_commit TEXT NOT NULL,
  env_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE(batch_id, candidate_uid, instance_id, seed)
);

CREATE TABLE IF NOT EXISTS analyses(
  id INTEGER PRIMARY KEY,
  batch_id TEXT NOT NULL,
  candidate_uid TEXT NOT NULL,
  baseline_uid TEXT NOT NULL,
  n_pairs INTEGER NOT NULL,
  cand_mean_excess REAL NOT NULL,
  base_mean_excess REAL NOT NULL,
  mean_delta_pp REAL NOT NULL,
  ci_lo REAL NOT NULL,
  ci_hi REAL NOT NULL,
  cohens_dz REAL NOT NULL,
  t_stat REAL NOT NULL,
  ttest_p REAL NOT NULL,
  wilcoxon_z REAL NOT NULL,
  wilcoxon_p REAL NOT NULL,
  holm_reject INTEGER NOT NULL,
  win_rate REAL NOT NULL,
  median_runtime_ratio REAL NOT NULL,
  decision TEXT NOT NULL,
  notes TEXT NOT NULL DEFAULT '',
  endpoint_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS critiques(
  id INTEGER PRIMARY KEY,
  batch_id TEXT NOT NULL,
  candidate_uid TEXT NOT NULL,
  severity TEXT NOT NULL,           -- info|warning|blocking
  finding TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS decisions(
  id INTEGER PRIMARY KEY,
  ts TEXT NOT NULL,
  kind TEXT NOT NULL,               -- champion_promotion|phase|protocol|note
  payload_json TEXT NOT NULL
);
"""


class ExperimentDB:
    def __init__(self, path: Path | str = DB_PATH):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.execute(
            "INSERT OR IGNORE INTO meta VALUES ('schema_version', ?)",
            (str(SCHEMA_VERSION),),
        )
        self.conn.commit()

    # -- generic helpers ----------------------------------------------------
    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        cur = self.conn.execute(sql, params)
        self.conn.commit()
        return cur

    def query(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        return self.conn.execute(sql, params).fetchall()

    def one(self, sql: str, params: tuple = ()) -> sqlite3.Row | None:
        return self.conn.execute(sql, params).fetchone()

    def decision(self, kind: str, payload: dict):
        self.execute(
            "INSERT INTO decisions(ts, kind, payload_json) VALUES (?,?,?)",
            (now_iso(), kind, json.dumps(payload, default=str)),
        )

    # -- instances -----------------------------------------------------------
    def upsert_instance(self, inst) -> int:
        row = self.one("SELECT id FROM instances WHERE name=?", (inst.name,))
        if row:
            return int(row["id"])
        cur = self.execute(
            "INSERT INTO instances(name,kind,n,seed,params_json,digest) VALUES (?,?,?,?,?,?)",
            (inst.name, inst.kind, inst.n, inst.seed,
             json.dumps(inst.params), inst.digest()),
        )
        return int(cur.lastrowid)

    # -- reference values ------------------------------------------------------
    def set_reference(self, instance_id: int, kind: str, value: float,
                      source: str, provenance: str):
        self.execute(
            """INSERT INTO reference_vals(instance_id,kind,value,source,provenance,updated_at)
               VALUES (?,?,?,?,?,?)
               ON CONFLICT(instance_id,kind) DO UPDATE SET
                 value=excluded.value, source=excluded.source,
                 provenance=excluded.provenance, updated_at=excluded.updated_at""",
            (instance_id, kind, value, source, provenance, now_iso()),
        )

    def get_reference(self, instance_id: int) -> tuple[float, str]:
        row = self.one(
            """SELECT value,kind FROM reference_vals WHERE instance_id=? ORDER BY
               CASE kind WHEN 'exact' THEN 0 ELSE 1 END LIMIT 1""",
            (instance_id,),
        )
        if not row:
            raise LookupError(f"no reference for instance {instance_id}")
        return float(row["value"]), row["kind"]

    # -- hypotheses / candidates ----------------------------------------------
    def add_hypothesis(self, uid: str, statement: str, rationale: str,
                       expected_effect: str, prediction: str,
                       literature_basis: str) -> str:
        self.execute(
            """INSERT OR REPLACE INTO hypotheses
               (uid,statement,rationale,expected_effect,prediction,literature_basis,created_at)
               VALUES (?,?,?,?,?,?,?)""",
            (uid, statement, rationale, expected_effect, prediction,
             literature_basis, now_iso()),
        )
        return uid

    def add_candidate(self, uid: str, family: str, config: dict,
                      hypothesis_uid: str | None, parent_uid: str | None,
                      code_version: str, git_commit: str) -> str:
        from .utils import stable_digest
        self.execute(
            """INSERT OR REPLACE INTO candidates
               (uid,family,config_json,config_digest,hypothesis_uid,parent_uid,
                code_version,git_commit,status,created_at)
               VALUES (?,?,?,?,?,?,?,?, 'proposed', ?)""",
            (uid, family, json.dumps(config, sort_keys=True),
             stable_digest(config), hypothesis_uid, parent_uid,
             code_version, git_commit, now_iso()),
        )
        return uid

    def set_candidate_status(self, uid: str, status: str):
        self.execute("UPDATE candidates SET status=? WHERE uid=?", (status, uid))

    # -- runs ------------------------------------------------------------------
    def add_run(self, batch_id: str, candidate_uid: str, instance_id: int,
                seed: int, budget_s: float, length: float, excess_pct: float,
                runtime_s: float, kicks: int, ls_moves: int, restarts: int,
                peak_rss_mb: float, git_commit: str, env: dict):
        self.execute(
            """INSERT OR REPLACE INTO runs
               (batch_id,candidate_uid,instance_id,seed,budget_s,length,excess_pct,
                runtime_s,kicks,ls_moves,restarts,peak_rss_mb,git_commit,env_json,created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (batch_id, candidate_uid, instance_id, seed, budget_s, length,
             None if excess_pct is None or excess_pct != excess_pct
             else float(excess_pct),
             runtime_s, kicks, ls_moves, restarts, peak_rss_mb,
             git_commit, json.dumps(env, default=str), now_iso()),
        )

    def excess_lookup(self, candidate_uid: str,
                      prefer_exact: bool = True) -> tuple[dict, dict, dict]:
        """Returns ({(iname,seed): excess_pct}, {..: runtime_s}, {..: length}).

        Excess is RECOMPUTED from raw lengths against the CURRENT reference
        values so that comparisons remain valid even if BKS improved after
        some runs were recorded (prevents reference-epoch confounds).
        """
        rows = self.query(
            """SELECT i.name AS iname, r.seed AS seed, r.length AS L,
                      r.runtime_s AS rt
               FROM runs r JOIN instances i ON i.id=r.instance_id
               WHERE r.candidate_uid=?""",
            (candidate_uid,),
        )
        refs = {
            row["instance_id"]: float(row["value"])
            for row in self.query(
                "SELECT instance_id, value FROM reference_vals "
                "WHERE kind=?", ("bks",))
        }
        refs_exact = {
            row["instance_id"]: float(row["value"])
            for row in self.query(
                "SELECT instance_id, value FROM reference_vals "
                "WHERE kind=?", ("exact",))
        }
        name2id = {r["name"]: r["id"] for r in self.query(
            "SELECT id,name FROM instances")}
        excess, runtime, lengths = {}, {}, {}
        for r in rows:
            iid = name2id[r["iname"]]
            ref = None
            if prefer_exact and iid in refs_exact:
                ref = refs_exact[iid]
            elif iid in refs:
                ref = refs[iid]
            elif iid in refs_exact:
                ref = refs_exact[iid]
            if ref is None or ref <= 0:
                continue          # no usable reference -> excluded from analysis
            key = (r["iname"], r["seed"])
            excess[key] = 100.0 * (r["L"] - ref) / ref
            runtime[key] = r["rt"]
            lengths[key] = r["L"]
        return excess, runtime, lengths

    def add_analysis(self, **kw) -> int:
        cur = self.execute(
            """INSERT INTO analyses
               (batch_id,candidate_uid,baseline_uid,n_pairs,cand_mean_excess,
                base_mean_excess,mean_delta_pp,ci_lo,ci_hi,cohens_dz,t_stat,
                ttest_p,wilcoxon_z,wilcoxon_p,holm_reject,win_rate,
                median_runtime_ratio,decision,notes,endpoint_json,created_at)
               VALUES (:batch_id,:candidate_uid,:baseline_uid,:n_pairs,
                :cand_mean,:base_mean,:mean_delta_pp,:ci_lo,:ci_hi,:cohens_dz,
                :t_stat,:ttest_p,:wilcoxon_z,:wilcoxon_p,:holm_reject,
                :win_rate,:median_runtime_ratio,:decision,:notes,
                :endpoint_json,:created_at)""",
            (
                kw["batch_id"], kw["candidate_uid"], kw["baseline_uid"],
                kw["n_pairs"], kw["cand_mean"], kw["base_mean"],
                kw["mean_delta_pp"], kw["ci_lo"], kw["ci_hi"], kw["cohens_dz"],
                kw["t_stat"], kw["ttest_p"], kw["wilcoxon_z"], kw["wilcoxon_p"],
                int(kw["holm_reject"]), kw["win_rate"],
                kw["median_runtime_ratio"], kw["decision"], kw.get("notes", ""),
                json.dumps(kw.get("endpoint", {})), now_iso(),
            ),
        )
        return int(cur.lastrowid)

    def add_critique(self, batch_id: str, candidate_uid: str, severity: str,
                     finding: str):
        self.execute(
            "INSERT INTO critiques(batch_id,candidate_uid,severity,finding,created_at)"
            " VALUES (?,?,?,?,?)",
            (batch_id, candidate_uid, severity, finding, now_iso()),
        )

    def close(self):
        self.conn.close()
