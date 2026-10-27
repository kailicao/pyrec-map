## Explanation

**Purpose.** `CTOL_MOD` holds `FCORR`, the fraction of the Henyey correction applied in the current iteration, shared by the main program and [[crrect.f#CRRECT|`CRRECT`]]. It replaces what is left of `COMMON/CTOL/` (MHP via Claude, 10/14/26): the block's tolerances and iteration limits (`HTOLER`, `FCORR0`, `FCORRI`, `HPTTOL`, `NITER1`–`NITER3`) are namelist variables now in [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]].

**What its variable holds, who sets it, who reads it.**
- `FCORR` (`REAL*8`): the [[main.f#(file level)|main program]] sets it to $|\mathtt{FCORR0}| - \mathtt{FCORRI}$ at the start of each model; `CRRECT` raises it by `FCORRI` per iteration, up to 1 (when `FCORR0` > 0), and scales the corrections by it.

**Design.** A blanket `USE CTOL_MOD` in both routines.

**Changed since `rp_1`.** New file: `FCORR` of `COMMON/CTOL/` as a module; the block's other members moved to `NMLPAR_MOD`.
