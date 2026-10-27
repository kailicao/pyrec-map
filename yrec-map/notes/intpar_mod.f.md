## Explanation

**Purpose.** `INTPAR_MOD` holds the settings of the Bulirsch–Stoer integration of the atmosphere and envelope, shared by [[parmin.f#PARMIN|`PARMIN`]], [[envint.f#ENVINT|`ENVINT`]] and [[bsstep.f#BSSTEP|`BSSTEP`]]. It replaces `COMMON/INTPAR/` (MHP via Claude, 10/14/26), the first of the conversion's `DATA` migrations: the three defaults come from PARMIN's `DATA STOLR0,IMAX,NUSE/1.0D-3,11,7/`.

**What its variables hold, who sets them, who reads them.** All three are in the `PHYSICS` namelist read by `PARMIN`, so a run can change them; no routine assigns them.
- `STOLR0` (`REAL*8`, 1.0D-3): the integration tolerance. `ENVINT` uses it as such for the atmosphere and scales it by $|$`SENV`$|$ for the envelope.
- `IMAX` (`INTEGER*4`, 11): the largest number of step subdivisions `BSSTEP` tries.
- `NUSE` (`INTEGER*4`, 7): the number of points used in `BSSTEP`'s extrapolation to zero step (passed to [[ratext.f#RATEXT|`RATEXT`]]), and the subdivision count that decides the next step.

**Design.** A blanket `USE INTPAR_MOD`.

**Changed since `rp_1`.** New file: `COMMON/INTPAR/` as a module, with its defaults moved from PARMIN's `DATA` statement.
