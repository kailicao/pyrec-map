## Explanation

**Purpose.** `RUNLOOP_MOD` holds the state of the run loop that is not in the namelist: for each of up to 50 runs (the kind cards), its kind, its rescaling targets and its stop switches. Shared by 10 routines. It was the first block made a module (the pilot, MHP via Claude, 10/14/26), and replaces `COMMON/CKIND/` and `COMMON/SETT/` of `rp_1`, first merged into `COMMON/RUNLOOP/` (10/13/26); their namelist members (`NMODLS`, `LFIRST`, `NUMRUN`, `ENDAGE`, `SETDT`, `END_DCEN`, `END_XCEN`, `END_YCEN`) moved to [[nmlpar_mod.f|`NMLPAR_MOD`]].

**What its variables hold, who sets them, who reads them.** Each is dimensioned on 50, the maximum number of runs, and indexed by the run `NK`.
- `IRESCA(50)`: the run's kind, copied by [[parmin.f#PARMIN|`PARMIN`]] from the namelist's `KINDRN` (1 evolve, 2 rescale, 3 rescale and evolve); reset to 1 by [[setcal.f#SETCAL|`SETCAL`]] and [[setscal.f#SETSCAL|`SETSCAL`]] for the repeated runs of a calibration. Read by the [[main.f#(file level)|main program]], [[starin.f#STARIN|`STARIN`]] (which calls [[rscale.f#RSCALE|`RSCALE`]] when it is not 1) and [[wrthead.f#WRTHEAD|`WRTHEAD`]].
- `RESCAL(4,50)`: the rescaling targets, in order the mass, $X$, $Z$ and the core mass, copied by `PARMIN` from `RSCLM`, `RSCLX`, `RSCLZ`, `RSCLCM`; changed by the calibrations (`SETCAL`, `SETSCAL`, [[chkcal.f#CHKCAL|`CHKCAL`]], [[chkscal.f#CHKSCAL|`CHKSCAL`]], which adjust $X$ and $Z$ between runs). Read by `RSCALE` (which applies them), `PARMIN` and the main program.
- `LENDAG(50)`: evolve until a stop condition (an age `ENDAGE`, or a central D, X or Y), set by `PARMIN` and by the calibrations; read by the main program, `PARMIN` and [[htimer.f#HTIMER|`HTIMER`]] (which keeps the step from passing the age).
- `LSETDT(50)`: a fixed time step (`SETDT` > 0), set by `PARMIN`, `SETCAL`, `SETSCAL`; read by `HTIMER` and `PARMIN`.

**Design.** A blanket `USE RUNLOOP_MOD` in each routine. The module's header explains the convention of the whole conversion (a blanket `USE` is safe because every block was declared identically everywhere, and no member's name is in two blocks or names a procedure) and points to `shadow_census.py` and KNOWN_ISSUES.md issue 22 for the risk of later edits. `IRESCA` is now `INTEGER*4` everywhere; at `rp_1` only PARMIN declared it so, and the other files left it to the default integer kind.

**Changed since `rp_1`.** New file: `COMMON/CKIND/` and `COMMON/SETT/` merged as a module, with their namelist members moved to `NMLPAR_MOD`.
