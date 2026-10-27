## Explanation

**Purpose.** `DISK_MOD` holds `SAGE`, the star's age, which the rotation routines compare with the disk-locking time, shared by 5 routines. It replaces what is left of `COMMON/DISK/` (MHP via Claude, 10/14/26): the disk-locking switch and parameters `LDISK`, `TDISK`, `PDISK` are namelist variables now in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]].

**What its variable holds, who sets it, who reads it.**
- `SAGE` (`REAL*8`): the total age `DAGE` (Gyr), stored by the [[main.f#(file level)|main program]] after each model ("MHP 9/94 store total age in SAGE"). Read by [[getw.f#GETW|`GETW`]], [[seculr.f#SECULR|`SECULR`]] and [[solid.f#SOLID|`SOLID`]], which hold the surface rotation locked while `LDISK` and `SAGE` ≤ `TDISK`, and by [[mdot.f#MDOT|`MDOT`]], which with `LDISK` and accretion shortens the step so that it ends at `TDISK`.

**Design.** A blanket `USE DISK_MOD`. Since `SAGE` is set after the model is computed, the routines of the next step see the age at the start of that step.

**Changed since `rp_1`.** New file: `SAGE` of `COMMON/DISK/` as a module; `LDISK`, `TDISK`, `PDISK` moved to `NMLPAR_MOD`.
