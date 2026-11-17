## Explanation

**Purpose.** `OLDROT2_MOD` holds the terms of the time derivative of $`\theta`$ in the Maeder–Zahn ([1998](https://ui.adsabs.harvard.edu/abs/1998A%26A...334.1000M)) advection–diffusion treatment of angular momentum ("MHP 06/02 added term for the time evolution of the angular velocity distribution"), at the start of the step and during the substeps, shared by 5 routines. It replaces `COMMON/OLDROT2/` (MHP via Claude, 10/14/26); `JSON` comes from [`DIMENSIONS_MOD`](dimensions_mod.f.md#dimensions_mod). All members are arrays of `JSON`.

**What its variables hold, who sets them, who reads them.** At each interface `I` (between shells `I-1` and `I`):
- `THM`: $`r^4/(\sqrt{m}\,G)`$ (in logs, `2(log r) − ½ log m − log G`), set by [`SETUPV`](setupv.f.md#setupv) ("added for $`d\theta/dt`$ term from Zahn & Maeder 1998").
- `THO`, `QWRST`: $`\theta`$ = `THM` $`\bar\Omega\,d\Omega/dr`$ and $`d\Omega/dr`$ of the old model, set by [`HPOINT`](hpoint.f.md#hpoint); [`GETW`](getw.f.md#getw) copies them into `THP`, `QWRMST` on the first iteration.
- `THP`, `QWRMST`, `WMST`: $`\theta`$, $`d\Omega/dr`$ and $`\Omega`$ at the start of the current substep, set by `GETW` (from the old model on the first iteration, recomputed from the current $`\Omega`$ after it). `THP` is read by [`VCIRC`](vcirc.f.md#vcirc); `WMST` by [`SECULR`](seculr.f.md#seculr) (the starting surface $`\Omega`$ for the wind); `QWRMST` nowhere ([getw.f, line 275](https://github.com/yreclab/yrec/blob/7be4133/src/getw.f#L275), [getw.f, line 287](https://github.com/yreclab/yrec/blob/7be4133/src/getw.f#L287)): unused?
- `THN`: the $`d\theta/dt`$ term, `FESTIME` (`THM` $`\bar\Omega\,d\Omega/dr`$ − `THP`)/$`\Delta t`$, set and read by `VCIRC`, which adds it to the circulation velocities.
- `FESTIME`: $`P/(g\,\Delta\nabla\,\rho)`$ at the interface, set by `SETUPV` (0 where unused) and rescaled by `VCIRC` with the $`\mu`$-gradient factor.
- `DDELM`: $`\nabla_\mathrm{ad} - \nabla`$, set by HPOINT from the old model and by SETUPV (with the $`\mu`$ term, not below a floor); read by SETUPV and VCIRC.

**Design.** A blanket `USE OLDROT2_MOD`. `DDELM` has two meanings, set by HPOINT and then overwritten by SETUPV.

**Changed since `rp_1`.** New file: `COMMON/OLDROT2/` as a module.
