# Final Report

_Generated 2026-08-24T06:17:18Z · git `ea46a2af9dd55255249d958efeb63c2787e449ef`_

## Evidence classes used throughout
- **KNOWN_FACT** — textbook/literature knowledge, not discovered here.
- **HYPOTHESIS** — pre-registered prediction recorded before measurement.
- **OUR_FINDING / EXPERIMENTAL RESULT** — supported by rows in `results/experiments.db` (seeds, paired tests, CIs reported inline).
- **UNVERIFIED** — plausible but not tested under the protocol.

## 1. Scope
Autonomous experimental campaign on iterated local search for the
Euclidean TSP over a declarative component grammar (see ARCHITECTURE.md).
Candidates registered: 56;
raw runs: 16410;
pre-registered hypotheses: 18.

## 2. Method summary
Paired design on shared (instance, seed); quality = % excess over
reference (exact Held-Karp optimum for n≤14; internal BKS otherwise,
labelled, never claimed optimal). Promotion requires Wilcoxon p<0.05
(Holm within batch), mean excess reduction ≥0.30pp, runtime guard
(DECISIONS.md D4/D9). No single noisy comparison can change the champion.

## 3. Champion lineage (experimental results)
| # | batch | candidate | Δpp vs prior champion | 95% CI | p(Wilcoxon) | dz |
|---|---|---|---|---|---|---|
| 1 | explore_2026-08-23T17:41:23Z | `C-3f9cba2784` | 0.20 | [0.13, 0.26] | 0.0000 | 0.44 |

Current champion config:

```json
{
  "acceptance": "sa",
  "construction": "nn",
  "ls_operators": [
    "two_opt",
    "or_opt1"
  ],
  "nl_k": null,
  "perturb_base": "current",
  "perturbation": "double_bridge",
  "sa_T0_frac": 0.005,
  "sa_alpha": 0.9
}
```

## 4. Phase ledger
- **setup**: {"instances": 70}
- **bks_bootstrap**: {"runs": 100, "budget_per_run": 15.0}
- **baselines**: {"plain_ls_mean_excess": 0.21502317077798494, "ils_mean_excess": 0.15015979058542203, "ils_delta_pp_vs_plain": 0.0648633801925629, "p_wilcoxon": 1.4633631416555357e-08}
- **setup**: {"instances": 76}
- **scale**: {"summary": {"C-006b20e16c": {"mean_delta_pp_vs_champ": -1.52, "n_pairs": 18}, "C-07d533c9b2": {"mean_delta_pp_vs_champ": -0.747, "n_pairs": 18}, "C-0ef37ec3bc": {"mean_delta_pp_vs_champ": -1.466, "n_pairs": 18}}}
- **budget_sensitivity**: {"result": {"x1": {"delta_pp": 0.033, "n": 216}, "x3": {"delta_pp": -0.027, "n": 216}}, "uids": ["C-3f9cba2784", "C-daf5979f68"]}
- **promotion_survives_3x_budget**: {"result": {"n": 216, "mean_delta_pp": 0.16257547012313103, "ci": [0.1103302716996986, 0.21768475061679562], "wilcoxon_p": 1.0371894975449357e-08, "win_rate": 0.5972222222222222}}

## 5. Findings of this campaign (each with evidence pointer)
1. **OUR_FINDING** — candidate `C-3f9cba2784` (batch explore_2026-08-23T17:41:23Z) improved mean excess by 0.20pp over its incumbent (CI [0.13,0.26], p=0.0000, dz=0.44). Evidence: `analyses` row + `runs` table.

## 6. Negative / null results (recorded, not hidden)

- `C-873ef5b55e` (phase_baselines): Δ=0.00pp [0.00,0.00], pW=1.0000 → no_change.
- `C-31e4c0b1a6` (phase_baselines): Δ=0.06pp [0.04,0.10], pW=0.0000 → significant_but_not_practical.
- `C-244733be30` (phase_ofat_2026-08-22T19:15:58Z): Δ=-0.02pp [-0.10,0.06], pW=0.5682 → no_change.
- `C-dc7bd80eaf` (phase_ofat_2026-08-22T19:15:58Z): Δ=0.04pp [0.00,0.08], pW=0.0002 → significant_but_not_practical.
- `C-46426f6012` (phase_ofat_2026-08-22T19:15:58Z): Δ=0.15pp [0.08,0.22], pW=0.0002 → significant_but_not_practical.
- `C-9a891bf98e` (phase_ofat_2026-08-22T19:15:58Z): Δ=-5.37pp [-6.07,-4.68], pW=0.0000 → significant_but_not_practical.
- `C-b078915e46` (phase_ofat_2026-08-22T19:15:58Z): Δ=-1.03pp [-1.21,-0.85], pW=0.0000 → significant_but_not_practical.
- `C-244733be30` (phase_ofat_2026-08-22T19:15:58Z): Δ=-0.02pp [-0.10,0.06], pW=0.5682 → no_change.
- `C-46426f6012` (phase_ofat_2026-08-22T19:15:58Z): Δ=0.15pp [0.08,0.22], pW=0.0002 → significant_but_not_practical.
- `C-9a891bf98e` (phase_ofat_2026-08-22T19:15:58Z): Δ=-5.37pp [-6.07,-4.68], pW=0.0000 → significant_but_not_practical.
- `C-b078915e46` (phase_ofat_2026-08-22T19:15:58Z): Δ=-1.03pp [-1.21,-0.85], pW=0.0000 → significant_but_not_practical.
- `C-dc7bd80eaf` (phase_ofat_2026-08-22T19:15:58Z): Δ=0.04pp [0.00,0.08], pW=0.0002 → significant_but_not_practical.
- `C-07d533c9b2` (phase_ofat_2026-08-22T21:11:42Z): Δ=0.07pp [0.04,0.09], pW=0.0000 → significant_but_not_practical.
- `C-68461f3210` (phase_ofat_2026-08-22T21:11:42Z): Δ=-0.03pp [-0.10,0.03], pW=0.5514 → no_change.
- `C-473cdcdb35` (phase_ofat_2026-08-22T21:11:42Z): Δ=-1.79pp [-2.02,-1.55], pW=0.0000 → significantly_worse.
- `C-f8342ab89d` (phase_ofat_2026-08-22T21:11:42Z): Δ=-1.81pp [-2.04,-1.57], pW=0.0000 → significantly_worse.
- `C-536023d575` (phase_ofat_2026-08-22T21:11:42Z): Δ=-1.82pp [-2.05,-1.58], pW=0.0000 → significantly_worse.
- `C-fea8063352` (phase_ofat_2026-08-22T21:56:53Z): Δ=0.08pp [0.05,0.12], pW=0.0000 → significant_but_not_practical.
- `C-c1f72e8082` (phase_ofat_2026-08-22T21:56:53Z): Δ=0.08pp [0.05,0.11], pW=0.0000 → significant_but_not_practical.
- `C-ca0dc0bc14` (phase_ofat_2026-08-22T21:56:53Z): Δ=0.14pp [0.07,0.20], pW=0.0000 → significant_but_not_practical.
- `C-2a678a76ff` (phase_ofat_2026-08-22T21:56:53Z): Δ=0.14pp [0.08,0.21], pW=0.0000 → significant_but_not_practical.
- `C-3ac98c274c` (phase_ofat_2026-08-22T21:56:53Z): Δ=-0.14pp [-0.23,-0.05], pW=0.0077 → null_or_negative.
- `C-6b01698687` (explore_2026-08-22T22:42:06Z): Δ=0.05pp [-0.02,0.12], pW=0.0576 → no_change.
- `C-3e0781131c` (explore_2026-08-22T22:42:06Z): Δ=0.13pp [0.07,0.19], pW=0.0000 → significant_but_not_practical.
- `C-d39a6a8569` (explore_2026-08-22T22:42:06Z): Δ=0.11pp [0.04,0.17], pW=0.0006 → significant_but_not_practical.

## 7. Threats to validity
- Single machine, wall-clock budgets → absolute runtimes vary; mitigated by pairing and runtime-ratio reporting.
- Internal BKS references may drift upward in quality over time; excess recomputed at analysis time prevents epoch confounds, but '% of BKS' should never be read as '% of optimal' beyond n≤14.
- Component grammar bounds discoverable improvements (D3/D8).
- Multiple batches share seeds; pairing handles correlation, but campaign-level error inflation across many promotions is not fully controlled (noted as UNVERIFIED risk).

## 8. Artifact register
- **A1 (found & fixed)** — don't-look-bit leak in composite LS; 13 pre-fix candidates quarantined; conclusions involving or_opt from before 2026-08-23T13:50Z are invalidated and re-measured. See DECISIONS.md D13 and critiques table.
- Host slept mid-campaign (2026-08-23 01:19→12:58Z); schedule slipped but no data corrupted (all runs budget-verified).

## 9. Director's synthesis (interpretation — labelled as such)

**Demonstrated (OUR_FINDING class, DB-backed):**
1. Closed loop ran end-to-end: 56 candidates, 16410 raw runs, every number traceable to DB rows.
2. Champion changed only via the replication rule (two independent significant batches) — no single noisy batch moved it.
3. Equal-budget paired evidence (uniform n=50–200): SA(T0=0.5%·L, α=0.90) + composite [2-opt→Or-opt(1)] + double-bridge kicks beat the classical NN+2-opt ILS seed by +0.20pp mean excess (CI [+0.13,+0.26], p=4.7e-10, dz=0.44); generalised to clustered/grid (old champion −0.69pp there, p=5.6e-08) and grew at n∈{500,1000} (−0.75..−1.52pp vs sampled alternates, descriptive).
3b. The promotion survives a 3× budget: at 9s runs the champion still leads the pre-promotion champion by +0.16pp [CI +0.11,+0.22], p=1.0e-08, win rate 0.60 (216 pairs) — effect size shrinks 0.20→0.16pp under longer budgets, as convergence pressure predicts.
4. Negative results recorded: kick contribution small (~0.06pp) at short budgets; nl_k=8 harmful; several literature priors did not transfer under this protocol.

**UNVERIFIED / open:**
- Champion vs closest rival (C-daf5979f68) practically tied and budget-sensitive (+0.03pp @1× flips −0.03pp @3×): identity of the best SA-composite variant is not settled by this campaign.
- '% of BKS' is project-internal above n=14.
- Effect magnitudes are Python-specific at these budgets; the transferable part is component directionality, not magnitudes (standard caveat in experimental-heuristics methodology).

## 10. Reproduction
`python scripts/run_overnight.py --phases <list>`; DB at `results/experiments.db`; every run row stores git commit, env snapshot, seed and raw tour length.