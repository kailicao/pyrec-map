## Explanation

**Purpose.** `SURFP` gives the pressure at $T = T_\mathrm{eff}$ in a model atmosphere, by interpolating a table of $\log P$ in $\log T_\mathrm{eff}$ and $\log g$. It is the outer boundary of the envelope integration with Kurucz atmospheres (`KTTAU = 3`). With `KTTAU = 4` `SETUPS` reads the same table, but `SURFP` is not called: a run with Allard atmospheres that leaves their table falls back to the gray atmosphere, not to this one ([[atmos2_mod.f#q1]]).

**How it fits.**
- **Inputs:** $\log T_\mathrm{eff}$ (`TEFFL`) and $\log g$ (`GL`); the table in `ATMOS2_MOD` (`ATMPL(57,11)`, the grids `ATMTL`, `ATMGL`), read by [[setups.f#SETUPS|SETUPS]]; and in `FAC_MOD`, the lowest and highest valid gravity index for each temperature (`IMIN`, `IMINMAX`), also set by `SETUPS`.
- **Who calls it:** [[envint.f#ENVINT|ENVINT]], for `KTTAU = 3`. Its siblings are [[kcsurfp.f#KCSURFP|KCSURFP]] (Kurucz–Castelli tables, `KTTAU = 5`) and [[alsurfp.f#ALSURFP|ALSURFP]] (Allard tables, `KTTAU = 4`).
- **What it calls:** [[inter3.f#INTER3|INTER3]] (3-point Lagrange weights), [[kspline.f#KSPLINE|KSPLINE]] and [[ksplint.f#KSPLINT|KSPLINT]] (a natural cubic spline through four points).
- **Outputs:** in `ATMPRT_MOD`, `AP` = $\log P$ and `AT` = $\log T_\mathrm{eff}$, read by `ENVINT` (and [[qatm.f#QATM|QATM]], [[massloss.f#MASSLOSS|MASSLOSS]]); `JP` and `KP` in `FAC_MOD`, the table cell used. With `LPRT`, a line on `ISHORT` and `ISTOR` (units from `IOUNITS_MOD`).

**The method.**
1. Stop the run if $\log T_\mathrm{eff} < 3.5$ or $\log g < -0.5$, with exit status 1.

    > **Question** ([[#L44]]; [[#L70-L71]]). **Hard-coded limits.** 3.5, $-0.5$, 4.5 and 4.55 are written in the code and tie it to one table; a different table would need them changed (the Kurucz 1990 tables start at $\log T_\mathrm{eff}$ = 3.544, so between 3.5 and 3.544 the spline extrapolates). Should they come from the table's grid (`ATMTL`, `ATMGL`)?

2. Find four table temperatures around $T_\mathrm{eff}$.
3. At each of them, interpolate $\log P$ in $\log g$: for $\log T > 4.55$ linearly between the two highest gravities; for $4.5 < \log T \le 4.55$ with the 3-point Lagrange formula on the three highest gravities; otherwise with a natural cubic spline through the four valid gravities nearest $\log g$ (the top four, a bracketing four, or the bottom four).

    > **Question** ([[#L70-L87]]). **Hot temperatures.** For $\log T > 4.5$ only the two or three highest gravities are used, whatever $\log g$ is: probably because the table has no low-gravity values there (the Kurucz 1990 tables have $-999$ below $\log g$ = 4.0 at $\log T \ge 4.50$). Is linear extrapolation to low gravity acceptable? [[surfbc.f#SURFBC|SURFBC]] switches a Kurucz run to the gray atmosphere above $\log T_\mathrm{eff} = 3.95$ ([[surfbc.f#L83-L95]]), so the four table temperatures stay below about 4.0 there; these branches would be reached only by a call of ENVINT with `KTTAU` = 3 for a hotter model before that switch (not traced).

4. Interpolate the four values in $\log T_\mathrm{eff}$ with a natural cubic spline through four points.

The four-point spline, for points $x_1 < \dots < x_4$, is the cubic-spline formula of [[splint.f|splint.f]] with natural ends.

The header ([[#L38-L41]]) describes an older method: It says the routine interpolates "USING A 4-POINT LAGRANGIAN INTERPOLATOR" and "WILL QUIT IF THE DESIRED DATA POINT HAS TEFF OR LOG G MORE THAN ONE TABLE POINT FROM THE DATA," but the code uses 4-point splines (the Lagrange calls `INTRP2` are commented out), except for table rows with $\log T_\mathrm{eff} > 4.5$, where gravity is interpolated linearly (above 4.55, [[#L71-L75]]) or with the 3-point Lagrange [[inter3.f#INTER3|INTER3]] ([[#L77-L82]]), and it checks only the lower limits of $T_\mathrm{eff}$ and $g$ ([[#L44]]).

> **Question** ([[#L44]]). **The comment describes another method.** Extrapolation above the table's top is silent. Besides a corrected comment, should an upper check be added?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/ATMOS2/`, `/FAC/`, `/ATMPRT/` and `/LUOUT/` to `ATMOS2_MOD`, `FAC_MOD`, `ATMPRT_MOD` and `IOUNITS_MOD`; the unused parameters `NTC`, `NGC` dropped), `IMPLICIT NONE`.

**Changed since `a8a5950`.** The out-of-table stop ends the run with exit status 1 (`STOP 1`) instead of a bare `STOP`, which exited with 0 (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(never occurred)** **Missing gravities used at the top of a row.** ([[#L88-L102]]; [[#L104-L123]]) [[setups.f#SETUPS|SETUPS]] sets `IMINMAX(J)`, the highest gravity with a pressure, below `NG` when a temperature's highest-gravity entries are $-999$ ([[setups.f#L270-L299]]). G. Somers limited the general case's search to `IMINMAX(J)` "to prevent using -999," but the top-four branch (`GL.GE.ATMGL(NG-1)`) still takes the gravities `NG-3` … `NG`, and `KK = MIN(NG-3,KK)` still allows them. The general search covers $\log g$ only up to `ATMGL(IMINMAX(J)-1)`. In such a row, a $\log g$ from there up to `ATMGL(NG-1)` = 4.5 matches no interval and falls through to the lowest four valid gravities, a long extrapolation; a $\log g \ge 4.5$ takes the top four, $-999$ entries included, into the spline. The tables in `input/atmos/kurucz/` with $[\mathrm{Fe/H}] \le -2.3$ (`atmk1990m23.tab` to `atmk1990m50.tab`) have such rows at $\log T_\mathrm{eff}$ = 3.53–3.68 (for example `atmk1990m40.tab`: no pressure above $\log g$ = 3.0 at 3.544), where cool dwarfs have $\log g \approx 4.5$–5; the other Kurucz 1990 tables have none below $\log T$ = 4.5, apart from an empty row at 4.041 in `atmk1990p01.tab`, above the switch to gray at 3.95. What follows: a wrong surface pressure `AP` for a cool metal-poor dwarf. Only with `KTTAU` = 3 (the default is 0, gray) and one of these tables.

    **A possible fix:**

    ```diff
    --- a/src/surfp.f
    +++ b/src/surfp.f
    @@ -85,11 +85,15 @@
                 ENDIF
                 GOTO 20
              ENDIF
    -         IF(GL.GE.ATMGL(NG-1))THEN
    +C 11/09/26 KC via Claude
    +C code changed to use IMINMAX(J), the highest gravity with a pressure,
    +C in place of NG, so that missing (-999) values at the top of a row
    +C are not used, and the general search reaches the top of the row.
    +         IF(GL.GE.ATMGL(IMINMAX(J)-1))THEN
     C DESIRED LOG G ABOVE SECOND TO TOP TABLE LOG G - USE TOP 4 LOG G VALUES.
                 DO KK = 1,4
    -               QG(KK)=ATMGL(NG-4+KK)
    -               PTAB(KK) = ATMPL(J,NG-4+KK)
    +               QG(KK)=ATMGL(IMINMAX(J)-4+KK)
    +               PTAB(KK) = ATMPL(J,IMINMAX(J)-4+KK)
                 END DO
     C            CALL INTRP2(QR,QG,GL)
                 CALL KSPLINE(QG,PTAB,YG)
    @@ -97,7 +101,7 @@
     C            PP(N) = ATMPL(J,NG-3)*QG(1)+ATMPL(J,NG-2)*QG(2)+
     C     *              ATMPL(J,NG-1)*QG(3)+ATMPL(J,NG)*QG(4)
                 PP(N) = Y0
    -            KP(N) = NG-3
    +            KP(N) = IMINMAX(J)-3
                 GOTO 20
              ENDIF
     C GENERAL CASE - FIND 4 NEAREST POINTS IN GRAVITY THAT ARE IN THE TABLE.
    @@ -106,7 +110,7 @@
              DO K = IMINMAX(J)-3,IMIN(J),-1
                 IF(GL.LT.ATMGL(K+2).AND.GL.GE.ATMGL(K+1))THEN
                    KK = MAX(IMIN(J),K)
    -               KK = MIN(NG-3,KK)
    +               KK = MIN(IMINMAX(J)-3,KK)
                    DO KKK = 1,4
                       QG(KKK) = ATMGL(KK+KKK-1)
                       PTAB(KKK) = ATMPL(J,KK+KKK-1)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): The branch ran in the two runs of 34 runs (26 of YREC's cases, from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning, and 8 made-up ones; one of these, with `FCORE` = 1.0, stopped in its first second) with `KTTAU` = 3, `testsuite/Test_solarGS98_kurucz` (10,264 times) and `testsuite/Test_solarM22M_difkur` (14,236 times), both with `atmk1990p00.tab`, at $\log T_\mathrm{eff}$ = 3.63 to 3.76 and $\log g$ = 2.70 to 4.57; no row with missing highest gravities was met, as expected for that table. A cool dwarf with one of the metal-poor tables ($[\mathrm{Fe/H}] \le -2.3$) would reach it; none was run. No fix was run. Intent: The comment ([[#L104-L105]]) says the change to `IMINMAX` was made "to prevent using -999"; only the loop's start was changed.

### SURFP

$\log P$ at $T = T_\mathrm{eff}$ from the Kurucz atmosphere table, by interpolation in $\log g$ then $\log T_\mathrm{eff}$.
