# Decision Log

Each decision is recorded before the evidence that could bias it.

## D1 — Research domain (2026-08-22, pre-experiment)
**Choice:** Euclidean TSP local search / ILS.
**Why:** strong documented baselines; seconds-per-experiment enables hundreds
of controlled paired comparisons overnight; exact reference values obtainable
for small n (Held-Karp); quality metric (% excess) continuous and
interpretable. Rejected: compression/numerical methods (harder to isolate
algorithmic contribution from library effects).

## D2 — Reference values
n≤14: Held-Karp optimum, verified against brute force for n≤8 in tests.
n>14: internal BKS = best objective found by ANY campaign run so far,
stored with provenance (candidate uid + batch). BKS is explicitly **not**
claimed optimal. All analyses recompute excess vs current references to avoid
epoch confounds.

## D3 — Candidates are declarative configs over a component grammar
Not free-form code. Reasons: ablations stay interpretable; config digests
give exact reproducibility; the search space is enumerable so coverage gaps
are visible. Trade-off: candidate creativity is bounded by the grammar; the
grammar itself can grow across iterations (recorded here when extended).

## D4 — Pre-registered promotion rule (fixed before any batch)
Promote iff: Wilcoxon p<0.05 after Holm within batch AND mean excess
reduction ≥0.30pp AND median runtime ratio ≤1.25× (relaxed to ≤2× if effect
≥0.90pp). Seeds {0..9}. Suites: exact+medium primary; structured robustness;
scale descriptive-only (never promotes). Rationale: single noisy comparisons
must never flip the champion; runtime guard prevents "better because we gave
it more compute".

## D5 — No scipy dependency
Statistics implemented in-house (incomplete beta via continued fraction,
Wilcoxon normal approximation w/ tie handling, bootstrap). Reason: fewer
environment failure modes overnight; every function unit-tested. Risk noted:
approximation error for very small n — mitigated by requiring n_pairs ≥ 20
in primary analyses.

## D6 — Agents are deterministic code, not LLM calls
Reproducibility and auditability. The "intelligence" of the system lives in:
curated literature priors, the grammar, the bandit over components, and the
critic's failure analyses. This bounds what can be discovered but keeps
every claim traceable to a queryable row.

## D7 — Float coordinates, no TSPLIB integer rounding
Avoids EUC_2D rounding ambiguity; instances are our own generated families
(uniform/clustered/grid) rather than public benchmark copies, chosen for
exact reproducibility from (kind,n,seed).

## D8 — Known limitations accepted at design time
* SA temperature reheats on restart not implemented (restarts rare under
  current protocol).
* Or-opt insertion candidates restricted to neighbour lists of segment ends
  (standard practice; makes neighbourhood incomplete).
* Wall-clock budgets make runs machine-dependent; all analyses are paired
  within the same machine/session, and runtime ratios are reported.

## D9 — Budget rebalancing (before campaign launch, after pipeline smoke test)
Initial budgets (5s/10s per run) would cost ~65 min per full candidate —
infeasible for the planned number of batches. Revised: exact 1.5s (all 10
seeds), medium/structured 3.0s (6 seeds), scale 15s. Full candidate now
~13-15 min; pilot screen ~2 min. Risk: conclusions might differ at longer
budgets — mitigated by (a) a dedicated budget-sensitivity check on the final
champion, (b) reporting kick counts so speed-normalised comparisons are
possible post hoc.

## D10 — Primary endpoint refined after baseline evidence (2026-08-23 ~19:15Z)
EXPERIMENTAL OBSERVATION: all 400 exact-suite runs (n≤14, both baselines,
10 seeds) reached the proven optimum → zero variance, no discriminative
power; medium n=50 nearly saturated (0.03%), n=200 carries the signal
(mean 0.83%, range 0–3%). DECISION: primary analyses restricted to the
medium suite; exact suite retained as a correctness/sanity guard only.
This is a data-driven protocol refinement recorded BEFORE adaptive batches.

## D11 — Replication-based promotion path (2026-08-23 ~20:15Z)
First OFAT batch showed real effects exist but the strongest positive one
(+0.15pp, p=2e-4) sits below the 0.30pp practical bar. Rather than lowering
the bar (noise risk), we add a second promotion pathway: a candidate that
significantly beats the CURRENT champion by >=0.15pp in TWO independent
batches (Holm-rejected in both) is promoted as `promote_replicated`.
Single-batch >=0.30pp promotions unchanged. This mirrors the replication
logic used in experimental sciences and is decided before seeing batch 2.

## D12 — Combo proposal family (2026-08-22 ~22:05Z)
Designer now includes greedy assembly of components whose arms accumulated
net-positive mean rewards over >=2 batches. Purpose: deliberately re-test
moderate winners together (supports D11 replication path) instead of waiting
for random mutation collisions.

## D13 — Artifact A1: don't-look-bit leak in composite local search (2026-08-23 ~13:45Z)
DISCOVERY PATH: explore-round "winners" (+0.11–0.13pp) all had
perturbation=None (inert ILS loop), while batch-2's big losers (-1.8pp)
differed mainly in operator ORDER — contradiction demanding investigation.
ROOT CAUSE: or_opt consulted/SET the shared don't-look mask. Unlike 2-opt
(whose move deltas change only at 4 splice endpoints, making endpoint
masking sound), relocation profitability changes globally; masked cities
never re-examined ⇒ premature convergence, order-dependent severity:
(or_opt1,two_opt)=11345 vs (two_opt,or_opt1)=8704 on one n=100 instance.
FIX: or-opt no longer consults/sets masks (still unmasks splice cities);
composite driver resets mask each additional round. Regression tests added;
Coder sanity gate now probes order-agreement automatically.
IMPACT ASSESSMENT (integrity action):
 - Champion (pure two_opt ILS) unaffected → prior paired comparisons vs it
   remain internally valid as measurements.
 - All pre-fix conclusions INVOLVING or_opt operators are quarantined:
   "kicks worth ~1.8pp" (batch-2 losers were broken-LS confounded),
   the +0.12–0.14pp or_opt cluster, and SA/LAHC interpretations from those
   batches. Re-validation batch scheduled post-fix.
LESSON: automated order-agreement probing now part of every candidate gate.
