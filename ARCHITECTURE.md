# Architecture

## Overview

```
┌─────────────────────────────── Director ───────────────────────────────┐
│  phase orchestration · champion state · promotion rule · docs/git      │
└──┬──────────┬───────────┬──────────────┬──────────────┬───────────────┘
   ▼          ▼           ▼              ▼              ▼
Researcher  Designer     Coder       Benchmark      Statistician → Critic
 (priors,    (candidates  (sanity      Engineer       (paired tests,
  gaps)       + hyp.)      gate)       (protocol,     Holm, CIs)
                                        DB writes)
```

All agents share one SQLite database (`results/experiments.db`), which is the
single source of truth. Agents are deterministic software modules — there is
no LLM inside the loop — so the whole campaign is reproducible from seeds +
git commit.

## Data model

| table | purpose |
|---|---|
| `instances` | generated TSP instances; identity = digest of coords |
| `reference_vals` | per-instance reference: `exact` (Held-Karp, n≤14) or `bks` |
| `hypotheses` | pre-registered falsifiable predictions per candidate |
| `candidates` | declarative configs in the component grammar |
| `runs` | one row per (candidate, instance, seed): length, runtime, kicks… |
| `analyses` | paired statistics vs champion at analysis time |
| `critiques` | critic findings incl. structured failure rationales |
| `decisions` | champion promotions and phase events |

Key integrity mechanism: **excess is recomputed from raw tour lengths against
the current reference at analysis time** (`db.excess_lookup`). If BKS improves
mid-campaign, historical runs are not silently compared against different
denominators.

## Candidate space (grammar)

A candidate is a dict over components:

```
construction ∈ {nn, greedy, cheapest_ins, random}
ls_operators ⊆ {two_opt, or_opt(1..3), or_opt1} ordered sequence
nl_k         ∈ {None(full), 8, 16, 40}
perturbation ∈ {None, double_bridge, reversals, relocations}
perturb_strength / perturb_base / acceptance ∈ {better, threshold,
record_to_record, sa(T0,α), lahc(L)} + params
```

The Designer samples this space via: one-factor mutations of the champion
(clean causal attribution), untried literature priors, and UCB1-guided
combinations whose rewards update from observed batch results.

## Measurement protocol

* Suites: `exact` (n∈{8,10,12,14}, optimum known), `medium`
  (uniform n∈{50,100,200}), `structured` (clustered/grid n=100), `scale`
  (n∈{500,1000}).
* Seeds S={0..9}; analyses pair runs on identical (instance, seed).
* Budgets fixed per suite (wall clock); runtime ratio guarded at promotion.
* Quality = % excess over reference (exact or BKS — always labelled).

## Statistics

Paired Wilcoxon signed-rank (tie/zero corrected) + paired t-test;
percentile bootstrap CIs on mean difference; Cohen's dz; Holm step-down
within each batch; promotion requires significance **and** ≥0.30pp practical
effect **and** runtime guard (see DECISIONS.md D4). All implemented in
`ais/stats.py` without scipy; special functions verified against textbook
values in tests.
