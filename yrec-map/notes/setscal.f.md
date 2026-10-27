## Explanation

**Purpose.** Prepares the list of runs for the automatic calibration of a star to a given luminosity and effective temperature (or radius): 50 runs, 25 repetitions of a two-run pattern. The adjustment between repetitions is done in [[chkscal.f#CHKSCAL|`CHKSCAL`]]. It is the analogue, for any star, of [[setcal.f#SETCAL|`SETCAL`]] for the Sun.

**How it fits.**
- **Who calls it:** the main program ([[main.f|`main.f`]]), when `LCALST` is true, before the loop over runs.
- **Arguments:** the state of the search, which the main program keeps and passes on to `CHKSCAL`: `ALRI` ($\log R/R_\odot$ of the previous model, set to 0) and the flags `LSTAR`, `LPASSR` (set to false); the comments in the routine define each.
- **Through modules:** `NMLPAR_MOD`, the target (`XLS` the luminosity in solar units, `XLSTOL` its tolerance, `LTEFF`, `STEFF`, `SR`) and the run list's arrays, and `RUNLOOP_MOD`, as in `SETCAL`; `CONSTANTS_MOD`; `IOUNITS_MOD` (`ITRACK`).
- **Outputs:** the run list; the target's radius or temperature; a line "Evolve to R*, L* =" on the terminal and in the track file (`ITRACK`).

**The method.** From $L = 4\pi R^2\sigma T_\mathrm{eff}^4$, the missing one of $R$ and $T_\mathrm{eff}$ is computed:

$$\frac{R}{R_\odot} = \frac{\sqrt{L/(4\pi\sigma)}}{T_\mathrm{eff}^2\,R_\odot}\quad(\texttt{LTEFF}\ \text{true}),\qquad T_\mathrm{eff} = \left(\frac{L}{4\pi\sigma R^2}\right)^{1/4}\quad(\text{otherwise}),$$

with $L$ = `XLS`·`CLSUN` (erg s$^{-1}$), $\sigma$ = `CSIG`, $R_\odot$ = `CRSUN` (cm). Then `NUMRUN` = 50: runs 3, 5, …, 49 repeat run 1 (a new starting model), and runs 4, 6, …, 50 repeat run 2 (evolution from the previous model).

**Changed since `rp_1`.** `ALRI`, `LSTAR` and `LPASSR` are arguments (formerly in `/CALSTAR/`); declarations only otherwise: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **The new stop criteria are not copied.** As in `SETCAL`, `END_DCEN`, `END_XCEN` and `END_YCEN` are not copied to the repeated runs.
2. **Stale comment.** The comment speaks of "THE NEXT SERIES OF 24 CALIBRATING RUNS"; it is 48 runs after the first two.
