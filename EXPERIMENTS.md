# Experiments

_Regenerated from `results/experiments.db` at 2026-08-24T06:15:35Z._

## Campaign summary

| metric | value |
|---|---|
| candidates registered | 56 |
| pre-registered hypotheses | 18 |
| raw runs | 16410 |
| champion promotions (rule-based) | 1 |

## Champion lineage (each step = statistically-gated promotion)

| batch | candidate | Δpp | CI | p(Wilcoxon) | dz |
|---|---|---|---|---|---|
| explore_2026-08-23T17:41:23Z | `C-3f9cba2784` | 0.20 | [0.13, 0.26] | 0.0000 | 0.44 |

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
| phase_ofat_2026-08-22T21:56:53Z | `C-fea8063352` | medium | 180 | 0.33 | 0.25 | **0.08** [0.05,0.12] | 0.0000 | 0.0000 | 0.39 | 0.23 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T21:56:53Z | `C-c1f72e8082` | medium | 180 | 0.33 | 0.26 | **0.08** [0.05,0.11] | 0.0000 | 0.0000 | 0.40 | 0.23 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T21:56:53Z | `C-ca0dc0bc14` | medium | 180 | 0.33 | 0.20 | **0.14** [0.07,0.20] | 0.0000 | 0.0000 | 0.31 | 0.52 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T21:56:53Z | `C-2a678a76ff` | medium | 180 | 0.33 | 0.19 | **0.14** [0.08,0.21] | 0.0000 | 0.0000 | 0.32 | 0.52 | 1.00 | significant_but_not_practical |
| phase_ofat_2026-08-22T21:56:53Z | `C-3ac98c274c` | medium | 180 | 0.33 | 0.47 | **-0.14** [-0.23,-0.05] | 0.0077 | 0.0028 | -0.23 | 0.38 | 1.00 | null_or_negative |
| explore_2026-08-22T22:42:06Z | `C-6b01698687` | medium | 180 | 0.34 | 0.29 | **0.05** [-0.02,0.12] | 0.0576 | 0.1960 | 0.10 | 0.49 | 1.00 | no_change |
| explore_2026-08-22T22:42:06Z | `C-3e0781131c` | medium | 180 | 0.34 | 0.21 | **0.13** [0.07,0.19] | 0.0000 | 0.0000 | 0.32 | 0.51 | 1.00 | significant_but_not_practical |
| explore_2026-08-22T22:42:06Z | `C-d39a6a8569` | medium | 180 | 0.34 | 0.23 | **0.11** [0.04,0.17] | 0.0006 | 0.0012 | 0.25 | 0.53 | 1.00 | significant_but_not_practical |
| explore_2026-08-22T22:42:06Z | `C-daf5979f68` | medium | 180 | 0.34 | 0.21 | **0.13** [0.06,0.19] | 0.0001 | 0.0002 | 0.28 | 0.54 | 1.00 | significant_but_not_practical |
| explore_2026-08-22T22:42:06Z | `C-3f9cba2784` | medium | 180 | 0.34 | 0.21 | **0.13** [0.07,0.20] | 0.0001 | 0.0001 | 0.29 | 0.56 | 1.00 | significant_but_not_practical |
| explore_2026-08-22T22:42:06Z | `C-5c7ddc5f9e` | medium | 180 | 0.34 | 0.22 | **0.12** [0.06,0.18] | 0.0001 | 0.0002 | 0.28 | 0.55 | 1.00 | significant_but_not_practical |
| postfix_revalidation_A1 | `C-6485ea2a2e` | medium | 180 | 0.34 | 0.28 | **0.06** [-0.01,0.12] | 0.0594 | 0.0973 | 0.12 | 0.32 | 1.00 | no_change |
| postfix_revalidation_A1 | `C-5f9f2c35b6` | medium | 180 | 0.34 | 0.21 | **0.13** [0.06,0.19] | 0.0001 | 0.0002 | 0.29 | 0.57 | 1.00 | significant_but_not_practical |
| postfix_revalidation_A1 | `C-3f9cba2784` | medium | 180 | 0.34 | 0.14 | **0.20** [0.13,0.26] | 0.0000 | 0.0000 | 0.44 | 0.63 | 1.00 | significant_but_not_practical |
| postfix_revalidation_A1 | `C-daf5979f68` | medium | 180 | 0.34 | 0.16 | **0.18** [0.12,0.25] | 0.0000 | 0.0000 | 0.41 | 0.62 | 1.00 | significant_but_not_practical |
| explore_2026-08-23T14:24:29Z | `C-1abefc1e0f` | medium | 180 | 0.34 | 0.20 | **0.14** [0.08,0.21] | 0.0000 | 0.0000 | 0.32 | 0.49 | 1.00 | significant_but_not_practical |
| explore_2026-08-23T14:24:29Z | `C-b56b49cdc8` | medium | 180 | 0.34 | 0.31 | **0.03** [-0.04,0.11] | 0.4070 | 0.4096 | 0.06 | 0.50 | 1.00 | no_change |
| explore_2026-08-23T14:24:29Z | `C-833c6e3b5e` | medium | 180 | 0.34 | 0.46 | **-0.12** [-0.21,-0.04] | 0.0195 | 0.0047 | -0.21 | 0.36 | 1.00 | no_change |
| explore_2026-08-23T14:24:29Z | `C-8c2495eab8` | medium | 180 | 0.34 | 0.27 | **0.07** [0.00,0.14] | 0.0081 | 0.0399 | 0.15 | 0.54 | 1.00 | significant_but_not_practical |
| explore_2026-08-23T14:24:29Z | `C-006b20e16c` | medium | 180 | 0.34 | 0.44 | **-0.11** [-0.20,-0.02] | 0.0550 | 0.0207 | -0.17 | 0.41 | 1.00 | no_change |
| explore_2026-08-23T14:24:29Z | `C-d372a8f2b7` | medium | 180 | 0.34 | 0.39 | **-0.05** [-0.14,0.03] | 0.5083 | 0.2451 | -0.09 | 0.47 | 1.00 | no_change |
| explore_2026-08-23T15:29:42Z | `C-7c808014ec` | medium | 180 | 0.34 | 0.75 | **-0.41** [-0.57,-0.28] | 0.0000 | 0.0000 | -0.40 | 0.30 | 1.00 | significantly_worse |
| explore_2026-08-23T15:29:42Z | `C-f600b92491` | medium | 180 | 0.34 | 0.24 | **0.10** [0.03,0.17] | 0.0081 | 0.0062 | 0.21 | 0.49 | 1.00 | significant_but_not_practical |
| explore_2026-08-23T15:29:42Z | `C-3e79f699cd` | medium | 180 | 0.34 | 0.67 | **-0.33** [-0.44,-0.22] | 0.0000 | 0.0000 | -0.45 | 0.37 | 1.00 | significantly_worse |
| explore_2026-08-23T15:29:42Z | `C-5caf202052` | medium | 180 | 0.34 | 0.53 | **-0.19** [-0.27,-0.11] | 0.0001 | 0.0000 | -0.33 | 0.41 | 1.00 | null_or_negative |
| explore_2026-08-23T15:29:42Z | `C-7fa81bb576` | medium | 180 | 0.34 | 0.66 | **-0.32** [-0.42,-0.22] | 0.0000 | 0.0000 | -0.48 | 0.32 | 1.00 | significantly_worse |
| explore_2026-08-23T15:29:42Z | `C-c24cb2a6e7` | medium | 180 | 0.34 | 0.72 | **-0.38** [-0.48,-0.28] | 0.0000 | 0.0000 | -0.55 | 0.34 | 1.00 | significantly_worse |
| explore_2026-08-23T17:41:23Z | `C-3f9cba2784` | medium | 180 | 0.34 | 0.14 | **0.20** [0.13,0.26] | 0.0000 | 0.0000 | 0.44 | 0.63 | 1.00 | promote_replicated |
| explore_2026-08-23T17:41:23Z | `C-daf5979f68` | medium | 180 | 0.34 | 0.18 | **0.16** [0.09,0.22] | 0.0000 | 0.0000 | 0.35 | 0.58 | 1.00 | promote_replicated |
| explore_2026-08-23T17:41:23Z | `C-72f43e89b2` | medium | 180 | 0.34 | 0.45 | **-0.11** [-0.19,-0.03] | 0.0161 | 0.0065 | -0.21 | 0.40 | 1.00 | null_or_negative |
| explore_2026-08-23T17:41:23Z | `C-0ef37ec3bc` | medium | 180 | 0.34 | 0.43 | **-0.09** [-0.16,-0.03] | 0.0182 | 0.0071 | -0.20 | 0.42 | 1.00 | null_or_negative |
| explore_2026-08-23T17:41:23Z | `C-23fad5d789` | medium | 180 | 0.34 | 0.53 | **-0.19** [-0.28,-0.11] | 0.0002 | 0.0000 | -0.32 | 0.39 | 1.00 | null_or_negative |
| explore_2026-08-23T17:41:23Z | `C-488b7368fe` | medium | 180 | 0.34 | 0.22 | **0.12** [0.05,0.19] | 0.0005 | 0.0010 | 0.25 | 0.56 | 1.00 | significant_but_not_practical |
| explore_2026-08-23T18:46:57Z | `C-9b7217ba36` | medium | 180 | 0.14 | 0.39 | **-0.25** [-0.32,-0.17] | 0.0000 | 0.0000 | -0.48 | 0.29 | 1.00 | null_or_negative |
| explore_2026-08-23T18:46:57Z | `C-734451b438` | medium | 180 | 0.14 | 0.15 | **-0.00** [-0.05,0.05] | 0.6841 | 0.9239 | -0.01 | 0.44 | 1.00 | no_change |
| explore_2026-08-23T18:46:57Z | `C-54635c2b62` | medium | 180 | 0.14 | 0.64 | **-0.49** [-0.60,-0.39] | 0.0000 | 0.0000 | -0.68 | 0.25 | 1.00 | significantly_worse |
| explore_2026-08-23T18:46:57Z | `C-1cad4f213f` | medium | 180 | 0.14 | 0.58 | **-0.44** [-0.53,-0.35] | 0.0000 | 0.0000 | -0.71 | 0.19 | 1.00 | significantly_worse |
| explore_2026-08-23T18:46:57Z | `C-706d7d1525` | medium | 180 | 0.14 | 0.43 | **-0.29** [-0.36,-0.22] | 0.0000 | 0.0000 | -0.57 | 0.29 | 1.00 | null_or_negative |
| explore_2026-08-23T18:46:57Z | `C-da446f5679` | medium | 180 | 0.14 | 0.63 | **-0.48** [-0.59,-0.38] | 0.0000 | 0.0000 | -0.66 | 0.22 | 1.00 | significantly_worse |
| explore_2026-08-23T20:18:26Z | `C-3c91a94a92` | medium | 180 | 0.14 | 0.34 | **-0.19** [-0.26,-0.12] | 0.0000 | 0.0000 | -0.40 | 0.28 | 1.00 | null_or_negative |
| explore_2026-08-23T20:18:26Z | `C-5b6560688a` | medium | 180 | 0.14 | 0.38 | **-0.24** [-0.31,-0.16] | 0.0000 | 0.0000 | -0.45 | 0.16 | 1.00 | null_or_negative |
| explore_2026-08-23T20:18:26Z | `C-a45259383e` | medium | 180 | 0.14 | 0.71 | **-0.57** [-0.68,-0.46] | 0.0000 | 0.0000 | -0.73 | 0.14 | 1.00 | significantly_worse |
| explore_2026-08-23T20:18:26Z | `C-e06b471e93` | medium | 180 | 0.14 | 0.71 | **-0.56** [-0.68,-0.45] | 0.0000 | 0.0000 | -0.69 | 0.16 | 1.00 | significantly_worse |
| explore_2026-08-23T20:18:26Z | `C-ffa5e3a2ee` | medium | 180 | 0.14 | 0.68 | **-0.54** [-0.66,-0.43] | 0.0000 | 0.0000 | -0.71 | 0.18 | 1.00 | significantly_worse |
| explore_2026-08-23T20:18:26Z | `C-7e9c469b93` | medium | 180 | 0.14 | 0.67 | **-0.52** [-0.66,-0.40] | 0.0000 | 0.0000 | -0.60 | 0.19 | 1.00 | significantly_worse |
| robust_2026-08-23T22:31:33Z | `C-3f9cba2784` | structured | 120 | 0.08 | 0.08 | **0.00** [0.00,0.00] | 1.0000 | 1.0000 | 0.00 | 0.00 | 1.00 | no_change |
| robust_2026-08-23T22:31:33Z | `C-31e4c0b1a6` | structured | 120 | 0.08 | 0.77 | **-0.69** [-1.15,-0.31] | 0.0000 | 0.0015 | -0.30 | 0.31 | 1.00 | significantly_worse |

## Experiment graph

Edges: `parent → candidate` shows derivation; each node links its hypothesis and outcome.
```mermaid
graph TD
  ROOT --> "C-873ef5b55e [prior\nbenchmarked]"
  ROOT --> "C-31e4c0b1a6 [prior\nbenchmarked]"
  C-31e4c0b1a6 --> "C-244733be30 [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-dc7bd80eaf [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-46426f6012 [prior\ninvalidated_artifact_A1]"
  C-31e4c0b1a6 --> "C-9a891bf98e [prior\ninvalidated_artifact_A1]"
  C-31e4c0b1a6 --> "C-b078915e46 [prior\nbenchmarked]"
  C-31e4c0b1a6 --> "C-32451e39d9 [mutation\nproposed]"
  C-31e4c0b1a6 --> "C-07d533c9b2 [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-68461f3210 [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-473cdcdb35 [bandit\ninvalidated_artifact_A1]"
  C-31e4c0b1a6 --> "C-f8342ab89d [bandit\ninvalidated_artifact_A1]"
  C-31e4c0b1a6 --> "C-536023d575 [bandit\ninvalidated_artifact_A1]"
  C-31e4c0b1a6 --> "C-fea8063352 [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-c1f72e8082 [mutation\ninvalidated_artifact_A1]"
  C-31e4c0b1a6 --> "C-ca0dc0bc14 [bandit\ninvalidated_artifact_A1]"
  C-31e4c0b1a6 --> "C-2a678a76ff [bandit\ninvalidated_artifact_A1]"
  C-31e4c0b1a6 --> "C-3ac98c274c [bandit\ninvalidated_artifact_A1]"
  C-31e4c0b1a6 --> "C-6b01698687 [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-3e0781131c [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-d39a6a8569 [bandit\ninvalidated_artifact_A1]"
  C-31e4c0b1a6 --> "C-5c7ddc5f9e [bandit\ninvalidated_artifact_A1]"
  C-31e4c0b1a6 --> "C-6485ea2a2e [revalidation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-5f9f2c35b6 [revalidation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-3f9cba2784 [revalidation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-daf5979f68 [revalidation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-1abefc1e0f [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-b56b49cdc8 [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-833c6e3b5e [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-8c2495eab8 [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-006b20e16c [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-d372a8f2b7 [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-7c808014ec [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-f600b92491 [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-3e79f699cd [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-5caf202052 [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-7fa81bb576 [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-c24cb2a6e7 [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-83a6c2d477 [mutation\nbenchmarked]"
  C-31e4c0b1a6 --> "C-7728d0b66c [mutation\nproposed]"
  C-31e4c0b1a6 --> "C-72f43e89b2 [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-0ef37ec3bc [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-23fad5d789 [bandit\nbenchmarked]"
  C-31e4c0b1a6 --> "C-488b7368fe [bandit\nbenchmarked]"
  C-3f9cba2784 --> "C-9b7217ba36 [mutation\nbenchmarked]"
  C-3f9cba2784 --> "C-734451b438 [mutation\nbenchmarked]"
  C-3f9cba2784 --> "C-54635c2b62 [bandit\nbenchmarked]"
  C-3f9cba2784 --> "C-1cad4f213f [bandit\nbenchmarked]"
  C-3f9cba2784 --> "C-706d7d1525 [bandit\nbenchmarked]"
  C-3f9cba2784 --> "C-da446f5679 [bandit\nbenchmarked]"
  C-3f9cba2784 --> "C-3c91a94a92 [mutation\nbenchmarked]"
  C-3f9cba2784 --> "C-5b6560688a [mutation\nbenchmarked]"
  C-3f9cba2784 --> "C-a45259383e [bandit\nbenchmarked]"
  C-3f9cba2784 --> "C-e06b471e93 [bandit\nbenchmarked]"
  C-3f9cba2784 --> "C-ffa5e3a2ee [bandit\nbenchmarked]"
  C-3f9cba2784 --> "C-7e9c469b93 [bandit\nbenchmarked]"
```

### Hypothesis ledger

| uid | statement | expected | prediction |
|---|---|---|---|
| `H-0003` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0004` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0005` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0006` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0007` | Changing ls_operators from two_opt,or_opt1 to or_opt1,two_opt improves mean quality at fixed budget. | Direction unknown a priori; detectable effect >=0.3pp mean excess difference. | Paired Wilcoxon on single-factor diff: p<0.05 after Holm within batch. |
| `H-0008` | Changing construction from nn to greedy improves mean quality at fixed budget. | Direction unknown a priori; detectable effect >=0.3pp mean excess difference. | Paired Wilcoxon on single-factor diff: p<0.05 after Holm within batch. |
| `H-0009` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0010` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0011` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0012` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0013` | Changing perturbation from double_bridge to reversals improves mean quality at fixed budget. | Direction unknown a priori; detectable effect >=0.3pp mean excess difference. | Paired Wilcoxon on single-factor diff: p<0.05 after Holm within batch. |
| `H-0014` | Changing sa_alpha from 0.9 to 0.97 improves mean quality at fixed budget. | Direction unknown a priori; detectable effect >=0.3pp mean excess difference. | Paired Wilcoxon on single-factor diff: p<0.05 after Holm within batch. |
| `H-0015` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0016` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0017` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0018` | Bandit-selected component combination matches or beats champion. | Exploitation step; small positive drift expected if bandit estimates are stable. | No regression vs champion beyond noise. |
| `H-0001` | Champion measured on structured distributions. | reference | descriptive |
| `H-0002` | Challenger 0 generalises to structured distributions. | unknown | descriptive |

## Critic failure analyses (why candidates were not adopted)

- `C-3f9cba2784`: failure_analysis: delta_pp=+0.000 [+0.000,+0.000]; win=0.00; dz=0.00; p_w=1; rt_x=1.00 => no_change
- `C-734451b438`: failure_analysis: delta_pp=-0.002 [-0.049,+0.046]; win=0.44; dz=-0.01; p_w=0.684; rt_x=1.00 => no_change
- `C-488b7368fe`: failure_analysis: delta_pp=+0.122 [+0.051,+0.193]; win=0.56; dz=0.25; p_w=0.000507; rt_x=1.00 => significant_but_not_practical
- `C-daf5979f68`: failure_analysis: delta_pp=+0.157 [+0.093,+0.223]; win=0.58; dz=0.35; p_w=1.73e-06; rt_x=1.00 => significant_but_not_practical
- `C-3f9cba2784`: failure_analysis: delta_pp=+0.200 [+0.134,+0.265]; win=0.63; dz=0.44; p_w=4.69e-10; rt_x=1.00 => significant_but_not_practical
- `C-f600b92491`: failure_analysis: delta_pp=+0.098 [+0.029,+0.168]; win=0.49; dz=0.21; p_w=0.00809; rt_x=1.00 => significant_but_not_practical
- `C-d372a8f2b7`: failure_analysis: delta_pp=-0.051 [-0.137,+0.034]; win=0.47; dz=-0.09; p_w=0.508; rt_x=1.00 => no_change
- `C-006b20e16c`: failure_analysis: delta_pp=-0.105 [-0.196,-0.019]; win=0.41; dz=-0.17; p_w=0.055; rt_x=1.00 => no_change
- `C-8c2495eab8`: failure_analysis: delta_pp=+0.072 [+0.004,+0.139]; win=0.54; dz=0.15; p_w=0.00812; rt_x=1.00 => significant_but_not_practical
- `C-833c6e3b5e`: failure_analysis: delta_pp=-0.122 [-0.208,-0.041]; win=0.36; dz=-0.21; p_w=0.0195; rt_x=1.00 => no_change
- `C-b56b49cdc8`: failure_analysis: delta_pp=+0.032 [-0.044,+0.109]; win=0.50; dz=0.06; p_w=0.407; rt_x=1.00 => no_change
- `C-1abefc1e0f`: failure_analysis: delta_pp=+0.141 [+0.077,+0.205]; win=0.49; dz=0.32; p_w=4.51e-06; rt_x=1.00 => significant_but_not_practical
- `C-daf5979f68`: failure_analysis: delta_pp=+0.182 [+0.118,+0.247]; win=0.62; dz=0.41; p_w=7.87e-09; rt_x=1.00 => significant_but_not_practical
- `C-3f9cba2784`: failure_analysis: delta_pp=+0.199 [+0.134,+0.264]; win=0.63; dz=0.44; p_w=6.09e-10; rt_x=1.00 => significant_but_not_practical
- `C-5f9f2c35b6`: failure_analysis: delta_pp=+0.128 [+0.064,+0.193]; win=0.57; dz=0.29; p_w=5.68e-05; rt_x=1.00 => significant_but_not_practical
- `C-6485ea2a2e`: failure_analysis: delta_pp=+0.057 [-0.009,+0.124]; win=0.32; dz=0.12; p_w=0.0594; rt_x=1.00 => no_change
- `C-5c7ddc5f9e`: failure_analysis: delta_pp=+0.121 [+0.058,+0.184]; win=0.55; dz=0.28; p_w=7.36e-05; rt_x=1.00 => significant_but_not_practical
- `C-3f9cba2784`: failure_analysis: delta_pp=+0.129 [+0.065,+0.195]; win=0.56; dz=0.29; p_w=5.89e-05; rt_x=1.00 => significant_but_not_practical
- `C-daf5979f68`: failure_analysis: delta_pp=+0.126 [+0.062,+0.192]; win=0.54; dz=0.28; p_w=9.92e-05; rt_x=1.00 => significant_but_not_practical
- `C-d39a6a8569`: failure_analysis: delta_pp=+0.109 [+0.045,+0.173]; win=0.53; dz=0.25; p_w=0.000614; rt_x=1.00 => significant_but_not_practical
- `C-3e0781131c`: failure_analysis: delta_pp=+0.129 [+0.072,+0.190]; win=0.51; dz=0.32; p_w=2.74e-05; rt_x=1.00 => significant_but_not_practical
- `C-6b01698687`: failure_analysis: delta_pp=+0.048 [-0.024,+0.121]; win=0.49; dz=0.10; p_w=0.0576; rt_x=1.00 => no_change
- `C-2a678a76ff`: failure_analysis: delta_pp=+0.141 [+0.078,+0.208]; win=0.52; dz=0.32; p_w=1.03e-05; rt_x=1.00 => significant_but_not_practical
- `C-ca0dc0bc14`: failure_analysis: delta_pp=+0.138 [+0.075,+0.205]; win=0.52; dz=0.31; p_w=1.41e-05; rt_x=1.00 => significant_but_not_practical
- `C-c1f72e8082`: failure_analysis: delta_pp=+0.078 [+0.051,+0.107]; win=0.23; dz=0.40; p_w=1.71e-08; rt_x=1.00 => significant_but_not_practical
- `C-fea8063352`: failure_analysis: delta_pp=+0.084 [+0.054,+0.116]; win=0.23; dz=0.39; p_w=1.71e-08; rt_x=1.00 => significant_but_not_practical
- `C-68461f3210`: failure_analysis: delta_pp=-0.034 [-0.103,+0.033]; win=0.48; dz=-0.07; p_w=0.551; rt_x=1.00 => no_change
- `C-07d533c9b2`: failure_analysis: delta_pp=+0.067 [+0.045,+0.092]; win=0.22; dz=0.40; p_w=3.71e-08; rt_x=1.00 => significant_but_not_practical
- `C-dc7bd80eaf`: failure_analysis: delta_pp=+0.043 [+0.003,+0.078]; win=0.18; dz=0.17; p_w=0.00021; rt_x=1.00 => significant_but_not_practical
- `C-b078915e46`: failure_analysis: delta_pp=-1.029 [-1.210,-0.851]; win=0.17; dz=-0.83; p_w=1.54e-19; rt_x=1.00 => significant_but_not_practical
- `C-9a891bf98e`: failure_analysis: delta_pp=-5.371 [-6.070,-4.681]; win=0.04; dz=-1.12; p_w=7.72e-28; rt_x=1.00 => significant_but_not_practical
- `C-46426f6012`: failure_analysis: delta_pp=+0.148 [+0.080,+0.219]; win=0.52; dz=0.31; p_w=0.000196; rt_x=1.00 => significant_but_not_practical
- `C-244733be30`: failure_analysis: delta_pp=-0.022 [-0.104,+0.055]; win=0.41; dz=-0.04; p_w=0.568; rt_x=1.00 => no_change
