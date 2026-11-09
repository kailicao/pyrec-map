## Explanation

**Purpose.** Prepares the list of runs for the automatic calibration of a star to a given luminosity and effective temperature (or radius): 50 runs, 25 repetitions of a two-run pattern. The adjustment between repetitions is done in [[chkscal.f#CHKSCAL|`CHKSCAL`]]. It is the analogue, for any star, of [[setcal.f#SETCAL|`SETCAL`]] for the Sun.

**How it fits.**
- **Who calls it:** the main program ([[main.f|`main.f`]]), when `LCALST` is true, before the loop over runs.
- **Arguments:** the state of the search, which the main program keeps and passes on to `CHKSCAL`: `ALRI` (named "log(R/Rsun) of the previous model", though [[chkscal.f#CHKSCAL|`CHKSCAL`]] stores $R/R_\odot$; set to 0, [[#L107]], which makes a track that starts above $R_*$ cross at once: [[chkscal.f#b1]]) and the flags `LSTAR`, `LPASSR` (set to false); the comments in the routine define each.
- **Through modules:** `NMLPAR_MOD`, the target (`XLS` the luminosity in solar units, `XLSTOL` its tolerance, `LTEFF`, `STEFF`, `SR`) and the run list's arrays, and `RUNLOOP_MOD`, as in `SETCAL`; `CONSTANTS_MOD`; `IOUNITS_MOD` (`ITRACK`).
- **Outputs:** the run list; the target's radius or temperature; a line "Evolve to R*, L* =" on the terminal and in the track file (`ITRACK`).

**The method.** From $L = 4\pi R^2\sigma T_\mathrm{eff}^4$, the missing one of $R$ and $T_\mathrm{eff}$ is computed:

$$\frac{R}{R_\odot} = \frac{\sqrt{L/(4\pi\sigma)}}{T_\mathrm{eff}^2\,R_\odot}\quad(\texttt{LTEFF}\ \text{true}),\qquad T_\mathrm{eff} = \left(\frac{L}{4\pi\sigma R^2}\right)^{1/4}\quad(\text{otherwise}),$$

with $L$ = `XLS`·`CLSUN` (erg s$^{-1}$), $\sigma$ = `CSIG`, $R_\odot$ = `CRSUN` (cm). Then `NUMRUN` = 50: runs 3, 5, …, 49 repeat run 1 (a new starting model), and runs 4, 6, …, 50 repeat run 2 (evolution from the previous model).

> **Question** ([[#L108-L112]]). **The comment's count.** The comment speaks of "THE NEXT SERIES OF 24 CALIBRATING RUNS"; the code fills 48 runs after the first two, that is, 24 repetitions of the two-run pattern. Is "24" meant as pairs of runs, and can the comment say so?

> **Question** ([[#L131-L139]]; [[nmlpar_mod.f#L261-L263]]). **The new stop criteria are not copied.** As in [[setcal.f#SETCAL|`SETCAL`]], `END_DCEN`, `END_XCEN` and `END_YCEN` ("MHP 10/24 ADDED STOP CRITERIA", [[#L57]]) are not copied to the repeated runs, unlike `ENDAGE` and `SETDT`, so a value set for run 2 is used only in the first repetition. Should they be copied?

**Changed since `rp_1`.** `ALRI`, `LSTAR` and `LPASSR` are arguments (formerly in `/CALSTAR/`); declarations only otherwise: COMMON blocks to modules, `IMPLICIT NONE`.
