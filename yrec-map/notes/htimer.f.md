## Explanation

**Purpose.** `HTIMER` sets the time step of the next model. Several criteria each propose a step, and it takes the most restrictive one (its comment): structure changes ([[ptime.f#PTIME|`PTIME`]]), angular-velocity changes for rotating models ([[wtime.f#WTIME|`WTIME`]]), hydrogen burning ([[xtime.f#XTIME|`XTIME`]]), helium burning ([[ytime.f#YTIME|`YTIME`]]) and, since 04/14, the motion of the model in the envelope-fitting "triangle" ([[entime.f#ENTIME|`ENTIME`]]); and the step may not grow by more than a factor `ATIME(13)` from the previous one.

**How it fits.**
- **Who calls it:** the main program, [[main.f#(file level)|main.f]]: at the start of each kind card, and after each converged model to set the next step. main.f always passes $|\Delta t|$ after a model (`DELTS = DABS(DELTS)`), and makes the step negative itself before a relaxation step.
- **Inputs:** the previous step `DELTS` (s); the model (`HD`, `HL`, `HS1`, `HS2`, `HT`, `HP`, `HR`, `HCOMP`, `OMEGA`, `M`, `TEFFL`); `JCORE`, `JXMID`, `JXBEG` (core and burning-shell indices); `TLUMX` (the luminosities by source, in solar units: elements 1–4 hydrogen burning, 5 helium burning, 7 the gravitational term); the age `DAGE` (Gyr); the run number `NK`.
- **Outputs:** the new `DELTS` (s), `DELTSH` (= `DELTS`, except on the relaxation branch, where it is left as passed unless the final-age cut applies), `DDAGE` (the step in years), and `DWMAX` (from `WTIME`: the largest change in $\Omega$, used by the rotational-mixing routines to set their number of substeps).
- **Modules:** [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] holds the settings: `ATIME` (the step controls, formerly `/CTLIM/`); per run, `SETDT` for a fixed step and `ENDAGE` for a final age, and the stop values for the central abundances `END_DCEN`, `END_XCEN`, `END_YCEN` (since 10/24, which is why `LENDAG` alone no longer means a stop age); `LPTIME` (formerly `/CT3/`; `HTIMER` can switch it off; default true, set by [[parmin.f#PARMIN|`PARMIN`]]'s namelist or by [[remap.f#REMAP|`REMAP`]] from `LSTRUCT_TIME`; main.f restores it at each solar-calibration cycle); `LTRIST` (the triangle governor, formerly `/GOVS/`) and `LROT` (formerly `/ROT/`). [[runloop_mod.f#RUNLOOP_MOD|`RUNLOOP_MOD`]] holds the per-run flags `LSETDT` (fixed step) and `LENDAG` (final age); with `SETDT` and `ENDAGE` these were `/SETT/`, set by [[parmin.f#PARMIN|`PARMIN`]] and shared with main.f, [[calcad.f#CALCAD|`CALCAD`]], [[chkscal.f#CHKSCAL|`CHKSCAL`]], [[setcal.f#SETCAL|`SETCAL`]], [[setscal.f#SETSCAL|`SETSCAL`]]. [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]] gives `CSECYR` (seconds per year).

**The method.**
1. A negative `DELTS` means the model is being relaxed, not evolved: skip to the end.
2. A fixed step for this run (`LSETDT(NK)`): $\Delta t$ = `SETDT(NK)` years, skip to the end.
3. If $\log T_c > 7.1$ and the gravitational luminosity `TLUMX(7)` is negative, switch the structure criterion off (`LPTIME` = false) for the rest of the job.
4. Collect the proposals, each $10^{20}$ s when not applicable or turned off: $\Delta t_P$ from `PTIME` (if `LPTIME`), $\Delta t_\Omega$ from `WTIME` (if rotating), $\Delta t_H$ from `XTIME` (if the H-burning luminosity exceeds $10^{-34}$), $\Delta t_{He}$ from `YTIME` (likewise for He), $\Delta t_E$ from `ENTIME` (if `LTRIST` and not `LPTIME`). The structure and rotation proposals ($\Delta t_P$, $\Delta t_\Omega$) below 1 s are replaced by $10^{20}$ ("a zero timestep in the model will fritz out the code"); the others are not checked.
5. The new step:
$$\Delta t = \min\left(f\,\Delta t_\mathrm{prev},\ \Delta t_H,\ \Delta t_{He},\ \Delta t_\Omega,\ \Delta t_P,\ \Delta t_E\right),\qquad f = \texttt{ATIME(13)},$$
leaving out the first term when $\Delta t_\mathrm{prev} \le 1$ s.
6. At the end: $\Delta t \leftarrow |\Delta t|$, `DDAGE` $= \Delta t/$`CSECYR`; if the run stops at an age (`LENDAG(NK)` and `ENDAGE(NK)` > 0), shorten the step so that the age does not pass `ENDAGE` (in years; the age `DAGE` is in Gyr).

**Design.** The switch-off of `LPTIME` changes a module flag (a namelist setting) permanently, and is announced with a bare `WRITE(*,…)`. A block of commented-out code ("Grant added") once tightened `ATIME(5)` and `ATIME(6)` with the helium luminosity.

**KC's changes.** 2025-05-31: the unused arguments `LC`, `QDT` and `QDP` removed from the interface; `JXBEG` no longer passed to `XTIME`, and `QDP`, `QDT` no longer passed to `YTIME`.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the unused `/CONST/` and `/FLAG/` are gone.

## Questions for the experts

1. **The relaxation branch.** The comment says a negative `DELTS` marks a model being relaxed, but main.f passes `DABS(DELTS)` after every model, so the branch can only be reached at the first call of a kind card (with the step from `STARIN`); relaxation steps otherwise go through all the criteria. The routine also returns `ABS(DELTS)`, and the `ENDAGE` truncation applies to every branch. Is the negative branch still needed?
2. **Unchecked proposals.** Only $\Delta t_P$ and $\Delta t_\Omega$ are protected against values below 1 s; a zero or negative step from `XTIME`, `YTIME` or `ENTIME` would pass through the minimum.
3. **The `LPTIME` switch-off.** Its comment is cut short ("this is done when"). Why $\log T_c > 7.1$ with a negative gravitational luminosity, and should it last for all later kind cards of the job (it is restored only in solar calibrations)?
4. **Thresholds.** The cut $10^{-34}\,L_\odot$ for "no burning" and $10^{20}$ s for "no limit" are hard-coded.

### HTIMER

Minimum over the step criteria (above), with fixed-step, relaxation and final-age special cases.
