# Experiments

_Regenerated from `results/experiments.db` at 2026-08-22T19:21:24Z._

## Campaign summary

| metric | value |
|---|---|
| candidates registered | 3 |
| pre-registered hypotheses | 3 |
| raw runs | 967 |
| champion promotions (rule-based) | 0 |

## All paired analyses vs incumbent champion

| batch | candidate | suites | n | base% | cand% | Δpp [CI] | pW | pT | dz | win | rt× | decision |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| phase_baselines | `C-873ef5b55e` | exact,medium | 380 | 0.22 | 0.22 | **0.00** [0.00,0.00] | 1.0000 | 1.0000 | 0.00 | 0.00 | 1.00 | no_change |
| phase_baselines | `C-31e4c0b1a6` | exact,medium | 380 | 0.22 | 0.15 | **0.06** [0.04,0.10] | 0.0000 | 0.0000 | 0.23 | 0.15 | 1.00 | significant_but_not_practical |

## Experiment graph

Edges: `parent → candidate` shows derivation; each node links its hypothesis and outcome.
```mermaid
graph TD
  ROOT --> "C-873ef5b55e [prior\nbenchmarked]"
  ROOT --> "C-31e4c0b1a6 [prior\nbenchmarked]"
  C-31e4c0b1a6 --> "C-244733be30 [mutation\nproposed]"
```

### Hypothesis ledger

| uid | statement | expected | prediction |
|---|---|---|---|
| `H-0002` | Plain NN construction + full-scan 2-opt to convergence is the classical baseline. | Reference point only. | Dominated by any working ILS variant at equal budget. |
| `H-0003` | Basic ILS (NN + 2-opt + double-bridge kick, better-acceptance) improves over plain LS at fixed budget. | +2..15pp mean excess reduction vs plain LS. | Wilcoxon p<0.05, positive delta across suites. |
| `H-0001` | Changing perturbation from double_bridge to reversals improves mean quality at fixed budget. | Direction unknown a priori; detectable effect >=0.3pp mean excess difference. | Paired Wilcoxon on single-factor diff: p<0.05 after Holm within batch. |
