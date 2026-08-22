# Experiments

_Regenerated from `results/experiments.db` at 2026-08-22T22:38:35Z._

## Campaign summary

| metric | value |
|---|---|
| candidates registered | 18 |
| pre-registered hypotheses | 10 |
| raw runs | 3683 |
| champion promotions (rule-based) | 0 |

## All paired analyses vs incumbent champion

| batch | candidate | suites | n | base% | cand% | Δpp [CI] | pW | pT | dz | win | rt× | decision |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| phase_baselines | `C-873ef5b55e` | exact,medium | 380 | 0.22 | 0.22 | **0.00** [0.00,0.00] | 1.0000 | 1.0000 | 0.00 | 0.00 | 1.00 | no_change |
| phase_baselines | `C-31e4c0b1a6` | exact,medium | 380 | 0.22 | 0.15 | **0.06** [0.04,0.10] | 0.0000 | 0.0000 | 0.23 | 0.15 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T19:15:58Z | `C-244733be30` | medium | 180 | 0.33 | 0.35 | **-0.02** [-0.10,0.06] | 0.5682 | 0.5832 | -0.04 | 0.41 | 1.00 | no_change |
| phase_ofat_2026-08-22T19:15:58Z | `C-dc7bd80eaf` | medium | 180 | 0.33 | 0.29 | **0.04** [0.00,0.08] | 0.0002 | 0.0262 | 0.17 | 0.18 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T19:15:58Z | `C-46426f6012` | medium | 180 | 0.33 | 0.18 | **0.15** [0.08,0.22] | 0.0002 | 0.0001 | 0.31 | 0.52 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T19:15:58Z | `C-9a891bf98e` | medium | 180 | 0.33 | 5.70 | **-5.37** [-6.07,-4.68] | 0.0000 | 0.0000 | -1.12 | 0.04 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T19:15:58Z | `C-b078915e46` | medium | 180 | 0.33 | 1.36 | **-1.03** [-1.21,-0.85] | 0.0000 | 0.0000 | -0.83 | 0.17 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T19:15:58Z | `C-244733be30` | medium | 180 | 0.33 | 0.35 | **-0.02** [-0.10,0.06] | 0.5682 | 0.5832 | -0.04 | 0.41 | 1.00 | no_change |
| phase_ofat_2026-08-22T19:15:58Z | `C-46426f6012` | medium | 180 | 0.33 | 0.18 | **0.15** [0.08,0.22] | 0.0002 | 0.0001 | 0.31 | 0.52 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T19:15:58Z | `C-9a891bf98e` | medium | 180 | 0.33 | 5.70 | **-5.37** [-6.07,-4.68] | 0.0000 | 0.0000 | -1.12 | 0.04 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T19:15:58Z | `C-b078915e46` | medium | 180 | 0.33 | 1.36 | **-1.03** [-1.21,-0.85] | 0.0000 | 0.0000 | -0.83 | 0.17 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T19:15:58Z | `C-dc7bd80eaf` | medium | 180 | 0.33 | 0.29 | **0.04** [0.00,0.08] | 0.0002 | 0.0262 | 0.17 | 0.18 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T21:11:42Z | `C-07d533c9b2` | medium | 180 | 0.33 | 0.26 | **0.07** [0.04,0.09] | 0.0000 | 0.0000 | 0.40 | 0.22 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T21:11:42Z | `C-68461f3210` | medium | 180 | 0.33 | 0.37 | **-0.03** [-0.10,0.03] | 0.5514 | 0.3219 | -0.07 | 0.48 | 1.00 | no_change |
| phase_ofat_2026-08-22T21:11:42Z | `C-473cdcdb35` | medium | 180 | 0.33 | 2.12 | **-1.79** [-2.02,-1.55] | 0.0000 | 0.0000 | -1.11 | 0.14 | 1.00 | significantly_worse |
| phase_ofat_2026-08-22T21:11:42Z | `C-f8342ab89d` | medium | 180 | 0.33 | 2.14 | **-1.81** [-2.04,-1.57] | 0.0000 | 0.0000 | -1.11 | 0.13 | 1.00 | significantly_worse |
| phase_ofat_2026-08-22T21:11:42Z | `C-536023d575` | medium | 180 | 0.33 | 2.15 | **-1.82** [-2.05,-1.58] | 0.0000 | 0.0000 | -1.12 | 0.13 | 1.00 | significantly_worse |

## Experiment graph

Edges: `parent → candidate` shows derivation; each node links its hypothesis and outcome.
```mermaid
graph TD
  ROOT --> "C-873ef5b55e [prior\nbenchmarked]"
  ROOT --> "C-31e4c0b1a6 [prior\nbenchmarked]"
  C-31e4c0b1a6 --> "C-244733be30 [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-dc7bd80eaf [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-46426f6012 [prior\nbenchmarked]"
  C-31e4c0b1a6 --> "C-9a891bf98e [prior\nbenchmarked]"
  C-31e4c0b1a6 --> "C-b078915e46 [prior\nbenchmarked]"
  C-31e4c0b1a6 --> "C-32451e39d9 [mutation\nproposed]"
  C-31e4c0b1a6 --> "C-07d533c9b2 [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-68461f3210 [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-473cdcdb35 [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-f8342ab89d [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-536023d575 [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-fea8063352 [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-c1f72e8082 [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-ca0dc0bc14 [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-2a678a76ff [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-3ac98c274c [bandit\nproposed]"
```

### Hypothesis ledger

| uid | statement | expected | prediction |
|---|---|---|---|
| `H-0001` | Changing perturb_base from current to best improves mean quality at fixed budget. | Direction unknown a priori; detectable effect >=0.3pp mean excess difference. | Paired Wilcoxon on single-factor diff: p<0.05 after Holm within batch. |
| `H-0002` | Changing acceptance from better to threshold improves mean quality at fixed budget. | Direction unknown a priori; detectable effect >=0.3pp mean excess difference. | Paired Wilcoxon on single-factor diff: p<0.05 after Holm within batch. |
| `H-0003` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0004` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0005` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0006` | Changing perturb_strength from 1 to 2 improves mean quality at fixed budget. | Direction unknown a priori; detectable effect >=0.3pp mean excess difference. | Paired Wilcoxon on single-factor diff: p<0.05 after Holm within batch. |
| `H-0007` | Changing ls_operators from two_opt to two_opt,or_opt1 improves mean quality at fixed budget. | Direction unknown a priori; detectable effect >=0.3pp mean excess difference. | Paired Wilcoxon on single-factor diff: p<0.05 after Holm within batch. |
| `H-0008` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0009` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0010` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |

## Critic failure analyses (why candidates were not adopted)

- `C-68461f3210`: failure_analysis: delta_pp=-0.034 [-0.103,+0.033]; win=0.48; dz=-0.07; p_w=0.551; rt_x=1.00 => no_change
- `C-07d533c9b2`: failure_analysis: delta_pp=+0.067 [+0.045,+0.092]; win=0.22; dz=0.40; p_w=3.71e-08; rt_x=1.00 => significant_but_not_practical
- `C-dc7bd80eaf`: failure_analysis: delta_pp=+0.043 [+0.003,+0.078]; win=0.18; dz=0.17; p_w=0.00021; rt_x=1.00 => significant_but_not_practical
- `C-b078915e46`: failure_analysis: delta_pp=-1.029 [-1.210,-0.851]; win=0.17; dz=-0.83; p_w=1.54e-19; rt_x=1.00 => significant_but_not_practical
- `C-9a891bf98e`: failure_analysis: delta_pp=-5.371 [-6.070,-4.681]; win=0.04; dz=-1.12; p_w=7.72e-28; rt_x=1.00 => significant_but_not_practical
- `C-46426f6012`: failure_analysis: delta_pp=+0.148 [+0.080,+0.219]; win=0.52; dz=0.31; p_w=0.000196; rt_x=1.00 => significant_but_not_practical
- `C-244733be30`: failure_analysis: delta_pp=-0.022 [-0.104,+0.055]; win=0.41; dz=-0.04; p_w=0.568; rt_x=1.00 => no_change
