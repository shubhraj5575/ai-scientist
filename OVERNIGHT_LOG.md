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
