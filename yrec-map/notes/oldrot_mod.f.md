## Explanation

**Purpose.** `OLDROT_MOD` holds the rotation of the model at the start of the step, on the new point distribution, shared by 6 routines. It replaces `COMMON/OLDROT/` (MHP via Claude, 10/14/26); `JSON` comes from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]]. All members are arrays of `JSON`.

**What its variables hold, who sets them, who reads them.** [[hpoint.f#HPOINT|`HPOINT`]] saves them after it has remapped the model ("store the old model structure for use in diffusion"):
- `WOLD`: $\Omega$ at the start of the step (also set by [[starin.f#STARIN|`STARIN`]]). Read by [[wtime.f#WTIME|`WTIME`]] (the largest fractional change of $\Omega$, for the time step), [[checkj.f#CHECKJ|`CHECKJ`]] (whether a gradient was positive before), [[getw.f#GETW|`GETW`]] (the start of the first substep) and HPOINT.
- `HJX` ($J/M$, "MHP 10/91 J/M stored in HJX"), `R0X`, `ETA2X` (the rotational distortion terms): interpolated onto the new grid and copied back into `HJM`, `R0`, `ETA2` by HPOINT itself.
- `HGO`: gravity, read by [[midmod.f#MIDMOD|`MIDMOD`]] (interpolated to mid-step).
- `HIO`: the moment of inertia; read nowhere.

**Design.** A blanket `USE OLDROT_MOD`.

**Changed since `rp_1`.** New file: `COMMON/OLDROT/` as a module.

## Questions for the experts

1. **An unused copy.** `HIO` is saved by HPOINT and read nowhere. Can it go?
