## Explanation

**Purpose.** `HTIMER` sets the time step of the next model. Several criteria each propose a step, and it takes the most restrictive one (its comment): structure changes ([[ptime.f#PTIME|`PTIME`]]: the change of $T$, $P$, $r$ and $L$ at any point since the previous model), angular-velocity changes for rotating models ([[wtime.f#WTIME|`WTIME`]]: the largest fractional change of $\Omega$), hydrogen burning ([[xtime.f#XTIME|`XTIME`]]: the hydrogen burnt in the core, or in the shell once the core is exhausted), helium burning ([[ytime.f#YTIME|`YTIME`]]: the helium burnt at the temperature maximum) and, since 04/14, the motion of the model in the envelope-fitting "triangle" ([[entime.f#ENTIME|`ENTIME`]]: the change of $\log T_\mathrm{eff}$ and $\log L$); and the step may not grow by more than a factor `ATIME(13)` from the previous one (default 1.5, "originally = 1.5" by [[parmin.f#PARMIN|PARMIN]]'s comment; under its newer name `TIME_MAX_DT_FRAC`, also 1.5, when [[remap.f#REMAP|REMAP]] applies the newer names).

**How it fits.**
- **Who calls it:** the main program, [[main.f#(file level)|main.f]]: at the start of each kind card, and after each converged model to set the next step. main.f always passes $|\Delta t|$ after a model (`DELTS = DABS(DELTS)`), and makes the step negative itself before a relaxation step.
- **Inputs:** the previous step `DELTS` (s); the model (`HD`, `HL`, `HS1`, `HS2`, `HT`, `HP`, `HR`, `HCOMP`, `OMEGA`, `M`, `TEFFL`); `JCORE`, `JXMID`, `JXBEG` (core and burning-shell indices); `TLUMX` (the luminosities by source, in solar units: elements 1–4 hydrogen burning, 5 helium burning, 7 the gravitational term); the age `DAGE` (Gyr); the run number `NK`.
- **Outputs:** the new `DELTS` (s), `DELTSH` (= `DELTS`, except on the relaxation branch, where it is left as passed unless the final-age cut applies), `DDAGE` (the step in years), and `DWMAX` (from `WTIME`: the largest change in $\Omega$, used by the rotational-mixing routines to set their number of substeps).
- **Modules:** [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] holds the settings: `ATIME` (the step controls, formerly `/CTLIM/`); per run, `SETDT` for a fixed step and `ENDAGE` for a final age, and the stop values for the central abundances `END_DCEN`, `END_XCEN`, `END_YCEN` (since 10/24, which is why `LENDAG` alone no longer means a stop age); `LPTIME` (formerly `/CT3/`; `HTIMER` can switch it off; default true, set by [[parmin.f#PARMIN|`PARMIN`]]'s namelist or by [[remap.f#REMAP|`REMAP`]] from `LSTRUCT_TIME`; main.f restores it at each solar-calibration cycle); `LTRIST` (the triangle governor, formerly `/GOVS/`) and `LROT` (formerly `/ROT/`). [[runloop_mod.f#RUNLOOP_MOD|`RUNLOOP_MOD`]] holds the per-run flags `LSETDT` (fixed step) and `LENDAG` (final age); with `SETDT` and `ENDAGE` these were `/SETT/`, set by [[parmin.f#PARMIN|`PARMIN`]] and shared with main.f, [[calcad.f#CALCAD|`CALCAD`]], [[chkscal.f#CHKSCAL|`CHKSCAL`]], [[setcal.f#SETCAL|`SETCAL`]], [[setscal.f#SETSCAL|`SETSCAL`]]. [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]] gives `CSECYR` (seconds per year).

**The method.**
1. A negative `DELTS` means the model is being relaxed, not evolved: skip to the end.

    > **Question** ([[#L85-L89]]; [[#L211-L213]]; [[main.f#L1051-L1057]]). **The relaxation branch.** The comment says a negative `DELTS` marks a model being relaxed, but main.f passes `DABS(DELTS)` after every model, so the branch can only be reached at the first call of a kind card (with the step from `STARIN`); relaxation steps otherwise go through all the criteria. The routine also returns `ABS(DELTS)`, and the `ENDAGE` truncation applies to every branch. Is the negative branch still needed?

2. A fixed step for this run (`LSETDT(NK)`): $\Delta t$ = `SETDT(NK)` years, skip to the end.
3. If $\log T_c > 7.1$ and the gravitational luminosity `TLUMX(7)` is negative, switch the structure criterion off (`LPTIME` = false) for the rest of the job. Its comment is cut short ("this is done when"); the purpose is in REMAP's comment, "this is used only in the pre-MS and disabled for MS stars automatically", and in the documentation of `LSTRUCT_TIME`, "disabled once Lgrav<0 (minimum radius, close to ZAMS)" (settled from the code and the documentation, Nov 9, 2026: [[#L96-L104]]; [[remap.f#L283-L285]]).

    > **Question** ([[#L98-L104]]; [[main.f#L383]]; [[main.f#L1154]]). **The `LPTIME` switch-off lasts for the job.** Once off, `LPTIME` stays off for all later kind cards of the job; main.f restores it only at each solar-calibration cycle. Should a later kind card that starts again from a pre-main-sequence model turn it back on, and should it stay off through the subgiant branch, where the structure changes fast?

4. Collect the proposals, each $10^{20}$ s when not applicable or turned off: $\Delta t_P$ from `PTIME` (if `LPTIME`), $\Delta t_\Omega$ from `WTIME` (if rotating), $\Delta t_H$ from `XTIME` (if the H-burning luminosity exceeds $10^{-34}$), $\Delta t_{He}$ from `YTIME` (likewise for He), $\Delta t_E$ from `ENTIME` (if `LTRIST` and not `LPTIME`). The structure and rotation proposals ($\Delta t_P$, $\Delta t_\Omega$) below 1 s are replaced by $10^{20}$ ("a zero timestep in the model will fritz out the code"); the others are not checked (for `ENTIME`, see bug 1).

    > **Question** ([[#L134-L153]]; [[xtime.f#L65-L68]]; [[ytime.f#L122-L127]]; [[ytime.f#L171-L173]]). **Unchecked burning proposals.** The core branches of `XTIME` and `YTIME` divide by `HL(JCORE)` without checking its sign (YTIME's shell branch does check it), and HTIMER does not protect $\Delta t_H$ and $\Delta t_{He}$ against values below 1 s, so a zero or negative luminosity at `JCORE` would give a negative or infinite step, which passes through the minimum (and comes out as its absolute value at the end). Can `HL(JCORE)` be zero or negative while the central $X$ is at least `ATIME(1)`, or in a helium-burning core?

    > **Question** ([[#L136]]; [[#L146]]; [[#L112]]). **Thresholds.** The cut $10^{-34}\,L_\odot$ for "no burning" and $10^{20}$ s for "no limit" are hard-coded. Are they meant to stay fixed, or should they be settings?

5. The new step:
$$\Delta t = \min\left(f\,\Delta t_\mathrm{prev},\ \Delta t_H,\ \Delta t_{He},\ \Delta t_\Omega,\ \Delta t_P,\ \Delta t_E\right),\qquad f = \texttt{ATIME(13)},$$
leaving out the first term when $\Delta t_\mathrm{prev} \le 1$ s.
6. At the end: $\Delta t \leftarrow |\Delta t|$, `DDAGE` $= \Delta t/$`CSECYR`; if the run stops at an age (`LENDAG(NK)` and `ENDAGE(NK)` > 0), shorten the step so that the age does not pass `ENDAGE` (in years; the age `DAGE` is in Gyr).

**Design.** The switch-off of `LPTIME` changes a module flag (a namelist setting) permanently, and is announced with a bare `WRITE(*,…)`. A block of commented-out code ("Grant added") once tightened `ATIME(5)` and `ATIME(6)` with the helium luminosity.

**From YREC's documentation.** [Physics Options](https://yrec.readthedocs.io/en/latest/namelist_physics.html) (Timestep criteria): `LTRIST` "restricts the timestep during the Hertzsprung gap"; in the code it keeps the model from moving more than `TRIDT` in $\log T_\mathrm{eff}$ or `TRIDL` in $\log L$ in a step (the size of the envelope triangle), at any phase, when the structural criterion (`LPTIME`, `LSTRUCT_TIME`) is off. The step limits `ATIME` are documented under their newer names on [[remap.f#REMAP|REMAP's page]]; `ENDAGE` ([Control Options](https://yrec.readthedocs.io/en/latest/namelist_control.html)) ends a run at an age.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`; the unused `/CONST/` and `/FLAG/` are gone.

## Bugs, by priority

1. **(d)** **A zero previous step passes through the envelope-triangle criterion.** ([[#L158-L162]]; [[#L171-L182]]; [[entime.f#L92-L95]]) ENTIME returns `DELTS/FAC` with `FAC` $\ge 1/$`ATIME(13)`, so a previous step of 0 (or under 1 s) gives an `EDELT` of at most `ATIME(13)` times it. Unlike `PDELT` and `DELTSW` ([[#L116]]; [[#L131]]), it is not replaced by $10^{20}$, and when the previous step is at most 1 s the minimum ([[#L181]]) takes it: The next step is again under 1.5 s, or 0 for every later model. This needs `LTRIST` (off by default) with `LPTIME` off; whether a run reaches HTIMER with such a step was not traced. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to set the envelope-triangle timestep arbitrarily large
    C when it is below 1 s, as is done for PDELT and DELTSW.
          IF(LTRIST .AND. .NOT. LPTIME) THEN
           CALL ENTIME(DELTS,HL,TEFFL,M,EDELT)
          ELSE
           EDELT = 1.0D20
          ENDIF
          IF(EDELT.LT.1.0D0)EDELT=1.0D20
    ```

### HTIMER

Minimum over the step criteria (above), with fixed-step, relaxation and final-age special cases.
