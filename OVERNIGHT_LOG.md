# Overnight Log

Autonomous research campaign log. Newest entries at bottom.

- Campaign started 2026-08-22. Domain: TSP local search (D1). Protocol fixed (D4).
- **2026-08-22T18:05:58Z** setup complete: 70 instances registered
- **2026-08-22T18:06:34Z** BKS bootstrap done (0 runs @ 1.0s)
- **2026-08-22T18:06:36Z** batch smoke: 0 analysed, 0 critiques, promotions=[]
- **2026-08-22T18:09:06Z** setup complete: 70 instances registered
- **2026-08-22T18:09:56Z** BKS bootstrap done (50 runs @ 1.0s)
- **2026-08-22T18:11:39Z** batch smoke: 0 analysed, 0 critiques, promotions=[]
- **2026-08-22T18:16:24Z** batch smoke: 1 analysed, 0 critiques, promotions=[]
- **2026-08-22T18:16:24Z**   C-31e4c0b1a6 (['exact', 'medium']): Δ=+0.00pp CI[+0.00,+0.00] pW=1 dz=0.00 rt×1.00 → no_change
- **2026-08-22T18:19:25Z** campaign run started: phases=['setup', 'bks', 'baselines'] budget=8.0h
- **2026-08-22T18:19:26Z** setup complete: 70 instances registered
- **2026-08-22T18:44:29Z** BKS bootstrap done (100 runs @ 15.0s)
- **2026-08-22T19:12:39Z** baselines: plainLS=0.22% ILS=0.15% Δ=+0.06pp p=1.5e-08
- **2026-08-22T19:15:58Z** campaign run started: phases=['ofat', 'explore'] budget=7.0h
- **2026-08-22T20:01:28Z** PHASE ofat FAILED: 'uniform_n50_s0'
- **2026-08-22T20:08:51Z** batch phase_ofat_2026-08-22T19:15:58Z: 5 analysed, 150 critiques, promotions=[]
- **2026-08-22T20:08:51Z**   C-244733be30 (['medium']): Δ=-0.02pp CI[-0.10,+0.06] pW=0.568 dz=-0.04 rt×1.00 → no_change
- **2026-08-22T20:08:51Z**   C-46426f6012 (['medium']): Δ=+0.15pp CI[+0.08,+0.22] pW=0.000196 dz=0.31 rt×1.00 → significant_but_not_practical
- **2026-08-22T20:08:51Z**   C-9a891bf98e (['medium']): Δ=-5.37pp CI[-6.07,-4.68] pW=7.72e-28 dz=-1.12 rt×1.00 → significant_but_not_practical
- **2026-08-22T20:08:51Z**   C-b078915e46 (['medium']): Δ=-1.03pp CI[-1.21,-0.85] pW=1.54e-19 dz=-0.83 rt×1.00 → significant_but_not_practical
- **2026-08-22T20:08:51Z**   C-dc7bd80eaf (['medium']): Δ=+0.04pp CI[+0.00,+0.08] pW=0.00021 dz=0.17 rt×1.00 → significant_but_not_practical
- **2026-08-22T21:11:42Z** campaign run started: phases=['ofat', 'explore'] budget=6.0h
- **2026-08-22T21:56:53Z** batch phase_ofat_2026-08-22T21:11:42Z: 5 analysed, 0 critiques, promotions=[]
- **2026-08-22T21:56:53Z**   C-07d533c9b2 (['medium']): Δ=+0.07pp CI[+0.04,+0.09] pW=3.71e-08 dz=0.40 rt×1.00 → significant_but_not_practical
- **2026-08-22T21:56:53Z**   C-68461f3210 (['medium']): Δ=-0.03pp CI[-0.10,+0.03] pW=0.551 dz=-0.07 rt×1.00 → no_change
- **2026-08-22T21:56:53Z**   C-473cdcdb35 (['medium']): Δ=-1.79pp CI[-2.02,-1.55] pW=1.13e-23 dz=-1.11 rt×1.00 → significantly_worse
- **2026-08-22T21:56:53Z**   C-f8342ab89d (['medium']): Δ=-1.81pp CI[-2.04,-1.57] pW=1.08e-23 dz=-1.11 rt×1.00 → significantly_worse
- **2026-08-22T21:56:53Z**   C-536023d575 (['medium']): Δ=-1.82pp CI[-2.05,-1.58] pW=1.04e-23 dz=-1.12 rt×1.00 → significantly_worse
- **2026-08-22T22:05Z** MANUAL ANALYSIS NOTE (Director): OFAT batch 2 decoded —
  all three ~-1.8pp losers share `perturbation=None`, quantifying the ILS-kick
  contribution at ~1.8pp on medium suite @3s. `perturb_base=best` gives small
  significant gain (+0.07pp, dz=0.40). Bandit now avoids perturbation=None.
  Designer extended with 'combo' family (D12): greedy assembly of arms with
  net-positive rewards to force replication attempts of moderate winners.
- **2026-08-22T22:42:04Z** batch phase_ofat_2026-08-22T21:56:53Z: 5 analysed, 0 critiques, promotions=[]
- **2026-08-22T22:42:04Z**   C-fea8063352 (['medium']): Δ=+0.08pp CI[+0.05,+0.12] pW=1.71e-08 dz=0.39 rt×1.00 → significant_but_not_practical
- **2026-08-22T22:42:04Z**   C-c1f72e8082 (['medium']): Δ=+0.08pp CI[+0.05,+0.11] pW=1.71e-08 dz=0.40 rt×1.00 → significant_but_not_practical
- **2026-08-22T22:42:04Z**   C-ca0dc0bc14 (['medium']): Δ=+0.14pp CI[+0.07,+0.20] pW=1.41e-05 dz=0.31 rt×1.00 → significant_but_not_practical
- **2026-08-22T22:42:04Z**   C-2a678a76ff (['medium']): Δ=+0.14pp CI[+0.08,+0.21] pW=1.03e-05 dz=0.32 rt×1.00 → significant_but_not_practical
- **2026-08-22T22:42:04Z**   C-3ac98c274c (['medium']): Δ=-0.14pp CI[-0.23,-0.05] pW=0.0077 dz=-0.23 rt×1.00 → null_or_negative
- **2026-08-23T13:34:12Z** batch explore_2026-08-22T22:42:06Z: 6 analysed, 1 critiques, promotions=[]
- **2026-08-23T13:34:12Z**   C-6b01698687 (['medium']): Δ=+0.05pp CI[-0.02,+0.12] pW=0.0576 dz=0.10 rt×1.00 → no_change
- **2026-08-23T13:34:12Z**   C-3e0781131c (['medium']): Δ=+0.13pp CI[+0.07,+0.19] pW=2.74e-05 dz=0.32 rt×1.00 → significant_but_not_practical
- **2026-08-23T13:34:12Z**   C-d39a6a8569 (['medium']): Δ=+0.11pp CI[+0.04,+0.17] pW=0.000614 dz=0.25 rt×1.00 → significant_but_not_practical
- **2026-08-23T13:34:12Z**   C-daf5979f68 (['medium']): Δ=+0.13pp CI[+0.06,+0.19] pW=9.92e-05 dz=0.28 rt×1.00 → significant_but_not_practical
- **2026-08-23T13:34:12Z**   C-3f9cba2784 (['medium']): Δ=+0.13pp CI[+0.07,+0.20] pW=5.89e-05 dz=0.29 rt×1.00 → significant_but_not_practical
- **2026-08-23T13:34:12Z**   C-5c7ddc5f9e (['medium']): Δ=+0.12pp CI[+0.06,+0.18] pW=7.36e-05 dz=0.28 rt×1.00 → significant_but_not_practical
- **2026-08-23T13:50Z** ARTIFACT A1 FOUND AND FIXED (see DECISIONS D13):
  don't-look-bit leak in or-opt caused order-dependent premature convergence
  (up to ~30%). 13 pre-fix candidates quarantined; Coder gate extended with
  automatic LS-soundness probe; regression tests added (25 passing).
- **2026-08-23T14:23:43Z** batch postfix_revalidation_A1: 4 analysed, 0 critiques, promotions=[]
- **2026-08-23T14:23:43Z**   C-6485ea2a2e (['medium']): Δ=+0.06pp CI[-0.01,+0.12] pW=0.0594 dz=0.12 rt×1.00 → no_change
- **2026-08-23T14:23:43Z**   C-5f9f2c35b6 (['medium']): Δ=+0.13pp CI[+0.06,+0.19] pW=5.68e-05 dz=0.29 rt×1.00 → significant_but_not_practical
- **2026-08-23T14:23:43Z**   C-3f9cba2784 (['medium']): Δ=+0.20pp CI[+0.13,+0.26] pW=6.09e-10 dz=0.44 rt×1.00 → significant_but_not_practical
- **2026-08-23T14:23:43Z**   C-daf5979f68 (['medium']): Δ=+0.18pp CI[+0.12,+0.25] pW=7.87e-09 dz=0.41 rt×1.00 → significant_but_not_practical
- **2026-08-23T14:24Z** POST-FIX REVALIDATION (batch postfix_revalidation_A1):
  * R1 plain NN+2opt no-kick: +0.06pp ns vs champion → true kick contribution
    is SMALL (~0.06pp at 3s budget), NOT the 1.8pp previously recorded
    (that figure was an A1 confound — quarantine vindicated).
  * R2 composite [two_opt,or_opt] no-kick: +0.13pp (p=6e-5) — richer local
    search is the dominant component effect found so far.
  * R3 winners re-benchmarked: C-3f9cba2784 +0.20pp (p=6e-10),
    C-daf5979f68 +0.18pp (p=8e-9). One more independent >=0.15pp batch
    triggers D11 replication promotion.
- **2026-08-23T14:24:29Z** campaign run started: phases=['explore'] budget=4.0h
- **2026-08-23T15:29:40Z** batch explore_2026-08-23T14:24:29Z: 6 analysed, 0 critiques, promotions=[]
- **2026-08-23T15:29:40Z**   C-1abefc1e0f (['medium']): Δ=+0.14pp CI[+0.08,+0.21] pW=4.51e-06 dz=0.32 rt×1.00 → significant_but_not_practical
- **2026-08-23T15:29:40Z**   C-b56b49cdc8 (['medium']): Δ=+0.03pp CI[-0.04,+0.11] pW=0.407 dz=0.06 rt×1.00 → no_change
- **2026-08-23T15:29:40Z**   C-833c6e3b5e (['medium']): Δ=-0.12pp CI[-0.21,-0.04] pW=0.0195 dz=-0.21 rt×1.00 → no_change
- **2026-08-23T15:29:40Z**   C-8c2495eab8 (['medium']): Δ=+0.07pp CI[+0.00,+0.14] pW=0.00812 dz=0.15 rt×1.00 → significant_but_not_practical
- **2026-08-23T15:29:40Z**   C-006b20e16c (['medium']): Δ=-0.11pp CI[-0.20,-0.02] pW=0.055 dz=-0.17 rt×1.00 → no_change
- **2026-08-23T15:29:40Z**   C-d372a8f2b7 (['medium']): Δ=-0.05pp CI[-0.14,+0.03] pW=0.508 dz=-0.09 rt×1.00 → no_change
- **2026-08-23T16:34:51Z** batch explore_2026-08-23T15:29:42Z: 6 analysed, 0 critiques, promotions=[]
- **2026-08-23T16:34:51Z**   C-7c808014ec (['medium']): Δ=-0.41pp CI[-0.57,-0.28] pW=2.17e-09 dz=-0.40 rt×1.00 → significantly_worse
- **2026-08-23T16:34:51Z**   C-f600b92491 (['medium']): Δ=+0.10pp CI[+0.03,+0.17] pW=0.00809 dz=0.21 rt×1.00 → significant_but_not_practical
- **2026-08-23T16:34:51Z**   C-3e79f699cd (['medium']): Δ=-0.33pp CI[-0.44,-0.22] pW=2.02e-07 dz=-0.45 rt×1.00 → significantly_worse
- **2026-08-23T16:34:51Z**   C-5caf202052 (['medium']): Δ=-0.19pp CI[-0.27,-0.11] pW=7.56e-05 dz=-0.33 rt×1.00 → null_or_negative
- **2026-08-23T16:34:51Z**   C-7fa81bb576 (['medium']): Δ=-0.32pp CI[-0.42,-0.22] pW=1.39e-08 dz=-0.48 rt×1.00 → significantly_worse
- **2026-08-23T16:34:51Z**   C-c24cb2a6e7 (['medium']): Δ=-0.38pp CI[-0.48,-0.28] pW=2.12e-11 dz=-0.55 rt×1.00 → significantly_worse
- **2026-08-23T16:50:34Z** campaign run started: phases=['explore'] budget=3.5h
- **2026-08-23T16:50:34Z** PHASE explore FAILED: Director._replication_candidates() got an unexpected keyword argument 'k_new'
- **2026-08-23T17:41:23Z** campaign run started: phases=['explore'] budget=3.5h
- **2026-08-23T18:46:55Z** batch explore_2026-08-23T17:41:23Z: 6 analysed, 0 critiques, promotions=['C-3f9cba2784']
- **2026-08-23T18:46:55Z**   C-3f9cba2784 (['medium']): Δ=+0.20pp CI[+0.13,+0.26] pW=4.69e-10 dz=0.44 rt×1.00 → promote_replicated
- **2026-08-23T18:46:55Z**   C-daf5979f68 (['medium']): Δ=+0.16pp CI[+0.09,+0.22] pW=1.73e-06 dz=0.35 rt×1.00 → promote_replicated
- **2026-08-23T18:46:55Z**   C-72f43e89b2 (['medium']): Δ=-0.11pp CI[-0.19,-0.03] pW=0.0161 dz=-0.21 rt×1.00 → null_or_negative
- **2026-08-23T18:46:55Z**   C-0ef37ec3bc (['medium']): Δ=-0.09pp CI[-0.16,-0.03] pW=0.0182 dz=-0.20 rt×1.00 → null_or_negative
- **2026-08-23T18:46:55Z**   C-23fad5d789 (['medium']): Δ=-0.19pp CI[-0.28,-0.11] pW=0.000188 dz=-0.32 rt×1.00 → null_or_negative
- **2026-08-23T18:46:55Z**   C-488b7368fe (['medium']): Δ=+0.12pp CI[+0.05,+0.19] pW=0.000507 dz=0.25 rt×1.00 → significant_but_not_practical
- **2026-08-23T18:47Z** MILESTONE — first rule-gated champion promotion:
  C-3f9cba2784 promoted via D11 replication path (Δ=+0.20pp CI[+0.13,+0.26],
  p=4.7e-10, dz=0.44, replicated in 2 independent batches vs prior champion).
  Runner-up C-daf5979f68 also replicated (+0.16pp). New champion = NN +
  [two_opt→or_opt1] LS + double-bridge kick from current + SA(T0=0.5%·len,
  α=0.90) acceptance. Full loop demonstrated: hypothesis → evidence →
  replication → promotion.
