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

> **Question** ([[#L38-L41]]). **The comment describes another method.** The header says it interpolates "using a 4-point Lagrangian interpolator" and "will quit if the desired data point has Teff or log g more than one table point from the data". The code uses 4-point splines (the Lagrange calls `INTRP2` are commented out), and checks only the lower limits of $T_\mathrm{eff}$ and $g$; extrapolation above the table's top is silent. Should the comment be corrected, or an upper check added?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/ATMOS2/`, `/FAC/`, `/ATMPRT/` and `/LUOUT/` to `ATMOS2_MOD`, `FAC_MOD`, `ATMPRT_MOD` and `IOUNITS_MOD`; the unused parameters `NTC`, `NGC` dropped), `IMPLICIT NONE`.

**Changed since `a8a5950`.** The out-of-table stop ends the run with exit status 1 (`STOP 1`) instead of a bare `STOP`, which exited with 0 (`KNOWN_ISSUES.md`, issue 38).

## Bugs, by priority

1. **(a)** **Missing gravities used at the top of a row.** ([[#L88-L102]]; [[#L104-L123]]) [[setups.f#SETUPS|SETUPS]] sets `IMINMAX(J)`, the highest gravity with a pressure, below `NG` when a temperature's highest-gravity entries are $-999$ ([[setups.f#L270-L299]]). G. Somers limited the general case's search to `IMINMAX(J)` "to prevent using -999", but the top-four branch (`GL.GE.ATMGL(NG-1)`) still takes the gravities `NG-3` … `NG`, and `KK = MIN(NG-3,KK)` still allows them. The general search covers $\log g$ only up to `ATMGL(IMINMAX(J)-1)`. In such a row, a $\log g$ from there up to `ATMGL(NG-1)` = 4.5 matches no interval and falls through to the lowest four valid gravities, a long extrapolation; a $\log g \ge 4.5$ takes the top four, $-999$ entries included, into the spline. The tables in `input/atmos/kurucz/` with $[\mathrm{Fe/H}] \le -2.3$ (`atmk1990m23.tab` to `atmk1990m50.tab`) have such rows at $\log T_\mathrm{eff}$ = 3.53–3.68 (for example `atmk1990m40.tab`: no pressure above $\log g$ = 3.0 at 3.544), where cool dwarfs have $\log g \approx 4.5$–5; the other Kurucz 1990 tables have none below $\log T$ = 4.5, apart from an empty row at 4.041 in `atmk1990p01.tab`, above the switch to gray at 3.95. What follows: a wrong surface pressure `AP` for a cool metal-poor dwarf. Only with `KTTAU` = 3 (the default is 0, gray) and one of these tables. Read from the code and the tables, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to use IMINMAX(J), the highest gravity with a pressure,
    C in place of NG, so that missing (-999) values at the top of a row
    C are not used, and the general search reaches the top of the row.
             IF(GL.GE.ATMGL(IMINMAX(J)-1))THEN
                DO KK = 1,4
                   QG(KK)=ATMGL(IMINMAX(J)-4+KK)
                   PTAB(KK) = ATMPL(J,IMINMAX(J)-4+KK)
                END DO
    ...
                KP(N) = IMINMAX(J)-3
                GOTO 20
             ENDIF
    ...
                   KK = MAX(IMIN(J),K)
                   KK = MIN(IMINMAX(J)-3,KK)
    ...
    ```

### SURFP

$\log P$ at $T = T_\mathrm{eff}$ from the Kurucz atmosphere table, by interpolation in $\log g$ then $\log T_\mathrm{eff}$.
