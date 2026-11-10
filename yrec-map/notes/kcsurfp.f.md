## Explanation

**Purpose.** `KCSURFP` finds the gas pressure at the point where $T = T_\mathrm{eff}$ by interpolating in a table of model-atmosphere pressures as a function of $\log T_\mathrm{eff}$ and $\log g$. It is the version of [[surfp.f#SURFP|`SURFP`]] for the newer Kurucz/Castelli tables (JNT 06/2014), whose size is $76\times11$ (`NTC`, `NGC`).

**How it fits.**
- **Who calls it:** only [[envint.f#ENVINT|`ENVINT`]], the envelope integration, which needs the pressure at the base of the atmosphere.
- **Inputs:** `TEFFL` = $\log T_\mathrm{eff}$, `GL` = $\log g$, `LPRT` (print or not); the table in `ATMOS2C_MOD` (`ATMPLC` = $\log P$, grids `ATMTLC`, `ATMGLC`), filled by [[setups.f#SETUPS|`SETUPS`]], the module's only other user; in `FAC_MOD`, the per-temperature range of valid gravities `IMIN2`, `IMINMAX2` (table entries that are missing in the grid).
- **Outputs:** in `ATMPRT_MOD`, `AP` = $\log P$ and `AT` = $\log T_\mathrm{eff}$; `ATMPRT_MOD` is read by `ENVINT`, [[qatm.f#QATM|`QATM`]], [[massloss.f#MASSLOSS|`MASSLOSS`]] and the other surface-pressure routines. It also sets `JP` and `KP(4)` in `FAC_MOD` (the table corner used). When `LPRT` is true it writes the result to the short output (`ISHORT`) and the model-storage unit (`ISTOR`), both from `IOUNITS_MOD`.
- **Calls:** [[kspline.f#KSPLINE|`KSPLINE`]] and [[ksplint.f#KSPLINT|`KSPLINT`]] (4-point natural splines), [[inter3.f#INTER3|`INTER3`]] (3-point Lagrange).
- **Modules:** `ATMPRT_MOD`, `ATMOS2C_MOD` (with `SETUPS`), `FAC_MOD` (with `SETUPS`, `SURFP`), `IOUNITS_MOD`.

**The method.**
1. Stop if $\log T_\mathrm{eff} < 3.5$ or $\log g < -0.5$, with exit status 1.

    > **Question** ([[#L53]]; [[#L79-L80]]). **Hard-coded table limits.** The bounds 3.5 and −0.5 and the thresholds 4.5 and 4.55 in $\log T$ (above which only the highest gravities are used) are written into the code; they belong to one table. Are they right for every Kurucz/Castelli table the code may read? No upper bounds are checked, and [[surfbc.f#SURFBC|SURFBC]] has no switch to gray for `KTTAU` = 5 ([[surfbc.f#q1]]), so above the tables' last temperature (4.699 in `input/atmos/CastelliKurucz/`) the spline extrapolates silently.

2. Take four table temperatures around $\log T_\mathrm{eff}$.
3. At each of them, interpolate $\log P$ in $\log g$:
   - for $\log T > 4.55$, linearly between the two highest gravities;

    > **Question** ([[#L80-L85]]). **Linear extrapolation in gravity for hot stars.** For $\log T > 4.55$ the linear formula extrapolates freely in $\log g$ beyond the two highest gravities (the tables in `input/atmos/CastelliKurucz/` have no pressure below $\log g$ = 4.5 from $\log T$ = 4.602 up). Is that acceptable for the stars that reach these temperatures?

   - for $4.5 < \log T \le 4.55$, by 3-point Lagrange (`INTER3`) over the three highest gravities;
   - otherwise with a 4-point natural spline over the four valid gravities around $\log g$ (the top four if $\log g$ is above the second-highest one, the lowest four valid ones if it is below them).
4. Interpolate the four results in $\log T_\mathrm{eff}$ with a 4-point natural spline: `AP`.

The comment ([[#L46-L49]]) is from an older routine: It calls the routine "SURFPL," says it interpolates in temperature and gravity with a 4-point Lagrange interpolator (the routine uses natural splines), and that "IT WILL QUIT IF THE DESIRED DATA POINT HAS TEFF OR LOG G MORE THAN ONE TABLE POINT FROM THE DATA" (only the lower limits are checked, [[#L53]]).

> **Question** ([[#L46-L49]]; [[#L79-L93]]). **Comments that do not match.** Not every row uses splines: For table rows with $\log T_\mathrm{eff} > 4.5$, gravity is interpolated linearly (above 4.55, [[#L79-L84]]) or with the 3-point Lagrange [[inter3.f#INTER3|INTER3]] ([[#L86-L93]]). Is that meant, and could a corrected comment describe both?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/ATMPRT/`, `/ATMOS2C/`, `/FAC/`; `/LUOUT/` to `IOUNITS_MOD`), the unused `/ATMOS2/` declaration and its parameters `NT`, `NG` dropped, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The out-of-table stop ends the run with exit status 1 (`STOP 1`) instead of a bare `STOP`, which exited with 0 (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(never occurred)** **Missing pressures at the highest gravities.** ([[#L97-L111]]; [[#L112-L132]]) [[setups.f#SETUPS|`SETUPS`]] sets `IMINMAX2(J)` below `NGC` when a temperature's highest-gravity entries are missing (pressure $\le 0$, e.g. −999) ([[setups.f#L327-L358]]). The general search (loop over `K` from `IMINMAX2(J)`−3 down to `IMIN2(J)`) then covers $\log g$ only up to `ATMGLC(IMINMAX2(J)-1)`. A $\log g$ between that and `ATMGLC(NGC-1)` matches no interval and falls through to the lowest four valid gravities, a long extrapolation; and a $\log g$ at or above `ATMGLC(NGC-1)` takes the top four gravities, missing entries included. Correct with the tables in `input/atmos/CastelliKurucz/`, which have all their highest gravities below $\log T$ = 4.5 (checked: every row of the 16 tables), but not with a table like the metal-poor Kurucz 1990 ones, where the same code in [[surfp.f#SURFP|SURFP]] gives wrong pressures ([[surfp.f#b1]]).

    **A possible fix:**

    ```diff
    --- a/src/kcsurfp.f
    +++ b/src/kcsurfp.f
    @@ -94,11 +94,15 @@
                 ENDIF
                 GOTO 20
              ENDIF
    -         IF(GL.GE.ATMGLC(NGC-1))THEN
    +C 11/09/26 KC via Claude
    +C code changed to use IMINMAX2(J), the highest gravity with a pressure,
    +C in place of NGC, so that missing (-999) values at the top of a row
    +C are not used, and the general search reaches the top of the row.
    +         IF(GL.GE.ATMGLC(IMINMAX2(J)-1))THEN
     C DESIRED LOG G ABOVE SECOND TO TOP TABLE LOG G - USE TOP 4 LOG G VALUES.
                 DO KK = 1,4
    -               QG(KK)=ATMGLC(NGC-4+KK)
    -               PTAB(KK) = ATMPLC(J,NGC-4+KK)
    +               QG(KK)=ATMGLC(IMINMAX2(J)-4+KK)
    +               PTAB(KK) = ATMPLC(J,IMINMAX2(J)-4+KK)
                 END DO
     C            CALL INTRP2(QR,QG,GL)
                 CALL KSPLINE(QG,PTAB,YG)
    @@ -106,7 +110,7 @@
     C            PP(N) = ATMPLC(J,NGC-3)*QG(1)+ATMPLC(J,NGC-2)*QG(2)+
     C     *              ATMPLC(J,NGC-1)*QG(3)+ATMPLC(J,NGC)*QG(4)
                 PP(N) = Y0
    -            KP(N) = NGC-3
    +            KP(N) = IMINMAX2(J)-3
                 GOTO 20
              ENDIF
     C GENERAL CASE - FIND 4 NEAREST POINTS IN GRAVITY THAT ARE IN THE TABLE.
    @@ -115,7 +119,7 @@
              DO K = IMINMAX2(J)-3,IMIN2(J),-1
                 IF(GL.LT.ATMGLC(K+2).AND.GL.GE.ATMGLC(K+1))THEN
                    KK = MAX(IMIN2(J),K)
    -               KK = MIN(NGC-3,KK)
    +               KK = MIN(IMINMAX2(J)-3,KK)
                    DO KKK = 1,4
                       QG(KKK) = ATMGLC(KK+KKK-1)
                       PTAB(KKK) = ATMPLC(J,KK+KKK-1)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): No case of YREC's uses `KTTAU` = 5, so a made-up run was added: `testsuite/Test_solarGS98_kurucz` with `KTTAU` = 5 and `atmk2004p00.tab`, as `input/atmos/CastelliKurucz/README` asks (line 15: "You NEED TO CHANGE KTTAU to 5"). The branch ran 10,156 times, at $\log T_\mathrm{eff}$ = 3.63 to 3.76 and $\log g$ = 2.70 to 4.57, and never met a row with missing highest gravities, as the check of the tables above found. A table with such rows would reach it; none is shipped. No fix was run. Intent: The comment ([[#L113-L114]]) says the change to `IMINMAX2` was made "to prevent using -999"; only the loop's start was changed.

### KCSURFP

Pressure at $T = T_\mathrm{eff}$ from the Kurucz/Castelli grid: splines in $\log g$ at four temperatures, then in $\log T_\mathrm{eff}$ (above).
