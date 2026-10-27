## Explanation

**Purpose.** `OLDROT2_MOD` holds the terms of the time derivative of $\theta$ in the Maeder–Zahn (1998) advection–diffusion treatment of angular momentum ("MHP 06/02 added term for the time evolution of the angular velocity distribution"), at the start of the step and during the substeps, shared by 5 routines. It replaces `COMMON/OLDROT2/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]]. All members are arrays of `JSON`.

**What its variables hold, who sets them, who reads them.** At each interface `I` (between shells `I-1` and `I`):
- `THM`: $r^4/(\sqrt{m}\,G)$ (in logs, `2(log r) − ½ log m − log G`), set by [[setupv.f#SETUPV|`SETUPV`]] ("added for $d\theta/dt$ term from Zahn & Maeder 1998").
- `THO`, `QWRST`: $\theta$ = `THM` $\bar\Omega\,d\Omega/dr$ and $d\Omega/dr$ of the old model, set by [[hpoint.f#HPOINT|`HPOINT`]]; [[getw.f#GETW|`GETW`]] copies them into `THP`, `QWRMST` on the first iteration.
- `THP`, `QWRMST`, `WMST`: $\theta$, $d\Omega/dr$ and $\Omega$ at the start of the current substep, set by `GETW` (from the old model on the first iteration, recomputed from the current $\Omega$ after it). `THP` is read by [[vcirc.f#VCIRC|`VCIRC`]]; `WMST` by [[seculr.f#SECULR|`SECULR`]] (the starting surface $\Omega$ for the wind); `QWRMST` nowhere.
- `THN`: the $d\theta/dt$ term, `FESTIME` (`THM` $\bar\Omega\,d\Omega/dr$ − `THP`)/$\Delta t$, set and read by `VCIRC`, which adds it to the circulation velocities.
- `FESTIME`: $P/(g\,\Delta\nabla\,\rho)$ at the interface, set by `SETUPV` (0 where unused) and rescaled by `VCIRC` with the μ-gradient factor.
- `DDELM`: $\nabla_\mathrm{ad} - \nabla$, set by HPOINT from the old model and by SETUPV (with the μ term, not below a floor); read by SETUPV and VCIRC.

**Design.** A blanket `USE OLDROT2_MOD`. `DDELM` has two meanings, set by HPOINT and then overwritten by SETUPV.

**Changed since `rp_1`.** New file: `COMMON/OLDROT2/` as a module.

## Questions for the experts

1. **An unused copy.** `QWRMST` is set by GETW and read nowhere. Can it go?
