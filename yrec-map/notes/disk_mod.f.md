## Explanation

**Purpose.** `DISK_MOD` holds `SAGE`, the star's age, which the rotation routines compare with the disk-locking time, shared by 5 routines. It replaces what is left of `COMMON/DISK/` (MHP via Claude, 10/14/26): the disk-locking switch and parameters `LDISK`, `TDISK`, `PDISK` are namelist variables now in [`NMLPAR_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L32-L279).

**What its variable holds, who sets it, who reads it.**
- `SAGE` (`REAL*8`): the total age `DAGE` ($`\mathrm{Gyr}`$), stored by the [main program](main.f.md#file-level) after each model ("MHP 9/94 store total age in SAGE"). Read by [`GETW`](getw.f.md#getw), [`SECULR`](https://github.com/yreclab/yrec/blob/7be4133/src/seculr.f#L6-L532), and [`SOLID`](solid.f.md#solid), which hold the surface rotation locked while `LDISK` and `SAGE` $`\le`$ `TDISK`, and by [`MDOT`](mdot.f.md#mdot), which with `LDISK` and accretion shortens the step so that it ends at `TDISK`.

**Design.** A blanket `USE DISK_MOD`. Since `SAGE` is set after the model is computed, the routines of the next step see the age at the start of that step.

**Changed since `rp_1`.** New file: `SAGE` of `COMMON/DISK/` as a module; `LDISK`, `TDISK`, `PDISK` moved to `NMLPAR_MOD`.
