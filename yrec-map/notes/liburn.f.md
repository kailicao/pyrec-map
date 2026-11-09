## Explanation

**Purpose.** `LIBURN` burns the light elements ⁶Li, ⁷Li and ⁹Be (`HCOMP(13)`, `HCOMP(14)`, `HCOMP(15)`) over one time step: in the radiative interior shell by shell, and in the surface convection zone as one mixed reservoir, with the rates changing during the step. Its accuracy is controlled by Richardson-type extrapolation over ever finer substeps. Its comment: "lithium and beryllium burning in a non-rotating model".

**How it fits.**
- **Who calls it:** the main program, [[main.f#(file level)|main.f]], at the end of each step when light elements are followed (`LEXCOM`) and the model is not rotating with rotational mixing; and [[getw.f#GETW|`GETW`]] for rotating models. The cheaper variant [[liburn2.f#LIBURN2|`LIBURN2`]] (one step, no extrapolation) is used by `GETW` and [[bursmix.f#BURSMIX|`BURSMIX`]].
- **Inputs:** `DELTS` (the step; main.f passes it in seconds), `HCOMP`, `HR`, `HS1`, `HS2`, `HT`, `M`; `JNENV0` and `JNENV`, the index of the base of the surface convection zone at the start and at the end of the step. The rates at the start (`OLDRAT_MOD`) and end (`NEWRAT_MOD`) of the step, from [[lirate88.f#LIRATE88|`LIRATE88`]].

    > **Question** ([[#L204-L208]]; [[#L382-L385]]; [[main.f#L1068]]). **Units of the step.** The comments call `DELT` "the fractional timestep in years", but main.f passes `DELTS` in seconds, and the rates from `LIRATE88` are probably per second ($\rho X N_A\langle\sigma v\rangle$). Is the comment's "in years" stale?

- **Output:** the new `HCOMP(13..15)`.
- **Calls:** [[ratext.f#RATEXT|`RATEXT`]] (rational extrapolation) and `SAFEDIVEXP` (below).
- **Modules:** `NEWRAT_MOD`, `OLDRAT_MOD` (the rates; with `LIRATE88`, `LIBURN2`, `GETW`, `BURSMIX`); `SCRTCH_MOD` (`SDEL`, the gradients $\nabla_\mathrm{rad}$, $\nabla$, $\nabla_\mathrm{ad}$ from `PHYSIC`); `MDPHY_MOD` (the same for rotating models); `OLDMOD_MOD` (`HRO`, the old radii); `LIOV_MOD` (`PSCAL0`, `PSCAL1`, the overshoot distances at the start and end of the step, set in main.f); `PREVCZ_MOD` (`RBASE0`, the end-of-step rates `BLI6OLD`… with the flag `LBLIOLD` that says they are valid, and `JENVOS`, kept for the next step); `DEUTER_MOD` (`FMASSACC`, for mass accretion); `NMLPAR_MOD` (the namelist switches and values: `LOVSTE`, envelope overshoot; `LROT`, `LINSTB`; for accretion `LMDOT`, `DMDT0`, `COMPACC`); `CONSTANTS_MOD`, `IOUNITS_MOD`, `DIMENSIONS_MOD`.

**The method.**
1. **Base of the convection zone.** Locate the base between the last convective point and the one below by linear interpolation of $\nabla_\mathrm{ad} - \nabla_\mathrm{rad}$: an offset $f_x \in [-\tfrac12, \tfrac12]$ of a zone. With envelope overshoot, move the base down by the overshoot distance (`PSCAL0`, `PSCAL1`) at the start and end of the step. At the start, the base's radius is the midpoint between `HRO(JNENV0)` and the point below; if the start-of-step model is fully convective (`JNENV0` = 1), the radius below shell 1 is taken as zero. At the end, the offset of the new base is measured in the zone width of the end-of-step model (`HR`).
2. **Radiative interior** (points below both bases, from the centre out, stopping at the first point where the ⁹Be rate, at the start or at the end, is at most $10^{-32}$; points where all three abundances are below $10^{-24}$ are skipped). Above $\log T = 7$ the elements are destroyed outright. Elsewhere, for $n$ = 2, 4, 6, 8, 12, … , 96 substeps of $h = \Delta t/n$: the rate at substep $k$ is interpolated linearly in its log between start and end,
$$\ln\lambda_k = \ln\lambda_0 + \tfrac{k - 1/2}{n}\,(\ln\lambda_1 - \ln\lambda_0),$$
and the abundance decays as $x \leftarrow x\,e^{-\lambda_k h}$ (set to 0 when $\lambda_k h \ge 30$). The results for successive $n$ are extrapolated to $h \to 0$ in $h^2$ by `RATEXT`; it stops when the relative error estimates are below $10^{-6}$. Values below $10^{-24}$ are set to 0.

    > **Question** ([[#L194]]; [[liburn2.f#L158]]). **The radiative loop's exit.** It leaves the loop at the first point (from the centre) where the ⁹Be rate is at most $10^{-32}$, assuming the rates only fall outward; `LIBURN2` skips such points instead. Which is meant?

    > **Question** ([[#L93-L94]]; [[#L197]]; [[#L232-L246]]; [[#L280-L284]]). **Hard-coded values.** The destruction temperature $\log T = 7$, the cut $\lambda h \ge 30$, the floor $10^{-24}$, the substep counts and the tolerances $10^{-6}$ are fixed in the code. Are they meant to stay fixed, or should any be a namelist setting (a run with tolerances ten times smaller would show whether the results depend on them)?
3. **Convection zone.** The zone's starting abundance is the mass-weighted mean over the zone at the start (or at the end, if the zone deepened). Its rate is the mass-weighted mean $\bar\lambda = \sum\lambda_i\Delta m_i/\sum\Delta m_i$ at the start (or the previous step's end value, `BLI6OLD`…, when the flag `LBLIOLD` is set) and at the end, the bottom point's mass and rate adjusted for the offset $f_x$. The same substepping and extrapolation as in step 2 follow. With accretion (`LMDOT`, `DMDT0` > 0), accreted material of composition `COMPACC` is added at each substep, assumed to burn for half a substep on arrival, and mixed in by mass with the factor `FMASSACC`. All points from the shallower of the two bases (`MAXJ`) to the surface get the result, and the end rates are stored for the next step with `LBLIOLD` set. The flag is cleared by [[main.f#(file level)|main.f]] at each kind card, by `LIBURN` when the whole zone is below the burning threshold (the zone is skipped), and by [[liburn2.f#LIBURN2|`LIBURN2`]], which always computes its start rates. The adjusted rates of the bottom point stay in `NEWRAT_MOD` (only its mass is restored).
4. **Region left by a retreating zone** (points `JENV0`..`JENV`−1, between the old and the new base): each is burned once with a rate weighted geometrically between its own end-of-step rate and the zone's start rate,
$$x \leftarrow x\,\exp\!\left(-\Delta t\,\lambda_\mathrm{rad}^{\,f}\,\bar\lambda_0^{\,1-f}\right),\qquad f = \frac{m - m_\mathrm{beg}}{m_\mathrm{beg} - m_\mathrm{end}},$$
with $m$ = `HS1` (the mass inside the point, in g), and $m_\mathrm{beg}$, $m_\mathrm{end}$ the masses at the old and the new base (`HSBEG`, `HSEND`; midpoints between the base point and the one below). The comment says that a point a fraction $f$ of the way (in mass) from the old base to the new one spent the fraction $f$ of the step in the zone, so $f$ should lie between 0 and 1; as written, $f$ is negative (bug 1 below).

**Design.** With accretion it prints a line to the terminal (`WRITE(*,913)`) at every level of the extrapolation.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (the namelist members of `/DPMIX/`, `/ROT/` and `/MASSCHG/` to `NMLPAR_MOD`, `/CONST1/` to `CONSTANTS_MOD`, `/LUOUT/` to `IOUNITS_MOD`), `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE` (also in `SAFEDIVEXP`).

**Changed since `a8a5950`.** The previous step's end-of-step zone rates are now reused, through the new flag `LBLIOLD` in `PREVCZ_MOD`; the old test `BLI6OLD.LE.0` was always true for the log of a small rate, so the start rates were always recomputed. A fully convective start-of-step model no longer reads `HRO(0)`. The overshoot zone width is taken from the end-of-step model alone (`HR(J+1)`, not `HRO(J+1)`), which settles former question 2; the later questions are renumbered.

## Bugs, by priority

1. **(a)** **The sign of `FRAD`.** ([[#L509-L528]]) For the points left by a retreating zone (`JENV` > `JENV0`), `DMASS = HSBEG - HSEND` is negative, since `HS1` grows outward, while `HS1(I) - HSBEG` is positive, so `FRAD` lies between −1 and 0. The rate $\lambda_\mathrm{rad}^{f}\bar\lambda_0^{1-f}$ then extrapolates beyond the zone's rate instead of interpolating between the two rates. Even with the sign corrected, the code gives the radiative rate the weight $f$, while the comment (lines 509–512) says that a point the fraction $f$ of the way from the old base to the new one spent the fraction $f$ of the step in the zone, which calls for the weight $f$ on the zone's rate: A point at the old base ($f$ = 0) left the zone at once. What follows: The light elements in the region a retreating zone leaves are burned at a rate up to $\bar\lambda_0^2/\lambda_\mathrm{rad}$, outside the range of the two rates. Only with `LEXCOM` (off by default), on steps where the zone retreats. Read from the code, not run. `LIBURN2` has the same lines ([[liburn2.f#b1]]). **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to make FRAD the fraction of the step spent in the CZ,
    C between 0 at the old base and 1 at the new one, as the comment above
    C says, and to give it the weight of the convective rate.
          DMASS = HSEND - HSBEG
    ...
             FRAD = (HS1(I)-HSBEG)/DMASS
    C USE FRAD*CONVECTIVE RATE AND (1-FRAD)*RADIATIVE RATE.
             DLI6 = DELTS*EXP((1.0D0-FRAD)*LOG(RLI6(I))+FRAD*BLI60)
             DLI7 = DELTS*EXP((1.0D0-FRAD)*LOG(RLI7(I))+FRAD*BLI70)
             DBE9 = DELTS*EXP((1.0D0-FRAD)*LOG(RBE9(I))+FRAD*BBE90)
    ```

2. **(a)** **Points newly in a deepened zone are not burned.** ([[#L191-L193]]; [[#L373-L379]]; [[#L496-L500]]) When the zone deepens (`JENV` < `JENV0`), its starting abundance is the mean over the end-of-step zone, `JENV` to `M`, which includes the points `JENV` to `JENV0`−1; but the result is written only from `MAXJ` = `JENV0` outward, and the radiative loop stops below `JENV`. Those points keep their abundances from before the step, so the zone is left with an unburned bottom and a burned top until it is next mixed (at the latest by [[mixcz.f#MIXCZ|MIXCZ]], which main.f calls once the next step's structure has converged, [[main.f#L977]]), and the burning of their mass over this step is lost. Only with `LEXCOM` (off by default), on steps where the zone deepens. Read from the code, not run; how much this changes the surface lithium was not traced. `LIBURN2` has the same lines ([[liburn2.f#b2]]). **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to give the burned abundances to the whole zone at the
    C end of the step, including points that joined it as it deepened.
          DO 130 I = JENV,M
    ```

3. **(d)** **⁹Be is not guarded against overflow.** ([[#L529-L538]]) In the last loop, ⁶Li and ⁷Li go through `SAFEDIVEXP`, but ⁹Be is still divided by `EXP(DBE9)`, and the comment "remember to add failsafes for large depletion" remains. For `DBE9` above 709.78, `EXP` overflows: In the default build the quotient is then 0, the intended result; in the development build, with `-ffpe-trap=overflow` (`GNU_DEV_FFLAGS`, `src/Makefile` line 61), the run stops. Since ⁹Be burns at higher temperatures than ⁶Li and ⁷Li, its exponent is probably the smallest of the three, so this needs a point where the lithium exponents are larger still. Only with `LEXCOM` (off by default). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to guard Be9 as Li6 and Li7 are.
             CALL SAFEDIVEXP(HCOMP(15,I),DBE9)
             IF(HCOMP(15,I).LT.1.0D-24)HCOMP(15,I)=0.0D0
    ```

4. **(d)** **The bottom point's rates are left adjusted.** ([[#L334-L343]]; [[#L371-L372]]) The comment says the rate and mass of the bottom point are adjusted for the offset $f_x$; afterwards only `HS2(JENV)` is restored, and `RLI6`, `RLI7`, `RBE9` at `JENV` keep the adjusted values in `NEWRAT_MOD`. In main.f nothing reads them before `LIRATE88` recomputes both sets at the next step; but [[getw.f#GETW|`GETW`]] copies them into the start rates `OLDRAT_MOD` for the next substep ([[getw.f#L409-L413]]), where a later mean start rate (loop 68, when `LBLIOLD` is false) weights the adjusted rate with the unadjusted mass. Correct for main.f, fragile for `GETW`. Read from the code, not run; the size of the effect was not traced. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to restore the bottom point's rates with its mass.
          HS2SAV = HS2(JENV)
          RLI6SV = RLI6(JENV)
          RLI7SV = RLI7(JENV)
          RBE9SV = RBE9(JENV)
    ...
    C RESTORE ORIGINAL MASS AND RATES TO BASE OF C.Z.
          HS2(JENV) = HS2SAV
          RLI6(JENV) = RLI6SV
          RLI7(JENV) = RLI7SV
          RBE9(JENV) = RBE9SV
    ```

    with `RLI6SV`, `RLI7SV`, `RBE9SV` added to the `REAL*8` declarations.

### LIBURN

Light-element burning with substeps and extrapolation, radiative and convective parts (above).

### SAFEDIVEXP

KC's guard (2025-05-31): replaces $x$ by $x/e^{a}$ when $a < 709.78$ (the largest argument for which $e^a$ fits in double precision), and by 0 otherwise.
