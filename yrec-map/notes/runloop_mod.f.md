## Explanation

**Purpose.** `RUNLOOP_MOD` holds the state of the run loop that is not in the namelist: for each of up to 50 runs (the kind cards), its kind, its rescaling targets and its stop switches. Shared by 10 routines. It was the first block made a module (the pilot, MHP via Claude, 10/14/26), and replaces `COMMON/CKIND/` and `COMMON/SETT/` of `rp_1`, first merged into `COMMON/RUNLOOP/` (10/13/26); their namelist members (`NMODLS`, `LFIRST`, `NUMRUN`, `ENDAGE`, `SETDT`, `END_DCEN`, `END_XCEN`, `END_YCEN`) moved to [`NMLPAR_MOD`](nmlpar_mod.f.md).

**What its variables hold, who sets them, who reads them.** Each is dimensioned on 50, the maximum number of runs, and indexed by the run `NK`.
- `IRESCA(50)`: the run's kind, copied by [`PARMIN`](parmin.f.md#parmin) from the namelist's `KINDRN` (1 evolve, 2 rescale, 3 rescale and evolve); reset to 1 by [`SETCAL`](setcal.f.md#setcal) and [`SETSCAL`](setscal.f.md#setscal) for the repeated runs of a calibration. Read by the [main program](main.f.md#file-level), [`STARIN`](starin.f.md#starin) (which calls [`RSCALE`](rscale.f.md#rscale) when it is not 1) and [`WRTHEAD`](wrthead.f.md#wrthead).
- `RESCAL(4,50)`: the rescaling targets, in order the mass, $`X`$, $`Z`$ and the core mass, copied by `PARMIN` from `RSCLM`, `RSCLX`, `RSCLZ`, `RSCLCM`; changed by the calibrations (`SETCAL`, `SETSCAL`, [`CHKCAL`](chkcal.f.md#chkcal), [`CHKSCAL`](chkscal.f.md#chkscal), which adjust $`X`$ and $`Z`$ between runs). Read by `RSCALE` (which applies them), `PARMIN` and the main program.
- `LENDAG(50)`: evolve until a stop condition (an age `ENDAGE`, or a central D, X or Y), set by `PARMIN` and by the calibrations; read by the main program, `PARMIN` and [`HTIMER`](htimer.f.md#htimer) (which keeps the step from passing the age).
- `LSETDT(50)`: a fixed time step (`SETDT` > 0), set by `PARMIN`, `SETCAL`, `SETSCAL`; read by `HTIMER` and `PARMIN`.

**Design.** A blanket `USE RUNLOOP_MOD` in each routine. The module's header explains the convention of the whole conversion (a blanket `USE` is safe because every block was declared identically everywhere, and no member's name is in two blocks or names a procedure) and points to KNOWN_ISSUES.md issue 22 for the risk of later edits; since every file now has `IMPLICIT NONE`, a `USE` that would capture a local is a compile error, so the script `shadow_census.py` that checked for it was removed. `IRESCA` is now `INTEGER*4` everywhere; at `rp_1` only PARMIN declared it so, and the other files left it to the default integer kind.

**Changed since `rp_1`.** New file: `COMMON/CKIND/` and `COMMON/SETT/` merged as a module, with their namelist members moved to `NMLPAR_MOD`.

**Changed since `a8a5950`.** The header's advice to run `shadow_census.py` before adding a `USE` is replaced by a note that `IMPLICIT NONE` everywhere makes such a capture a compile error; comments only.
