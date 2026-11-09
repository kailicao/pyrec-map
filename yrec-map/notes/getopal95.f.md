## Explanation

**Purpose.** `GETOPAL95` is the driver for the OPAL 1995 opacity tables ("7/98 MHP"): given $\rho$, $T$, $X$, $Z$, it finds the interpolation stencil and weights in $T$, $R = \rho/T_6^3$, $X$ and $Z$, handles the table's empty corner at high density, and calls a 2D, 3D or 4D interpolator depending on how far the composition is from the tables already prepared.

**How it fits.**
- **Who calls it:** only [[getopac.f#GETOPAC|GETOPAC]], when `LOPAL95` is set (with $Z$ = 0.1 in metal-rich helium-burning cores).
- **Inputs:** `DL`, `TL`, `X`, `Z`.
- **What it calls:** [[interp.f#INTERP|INTERP]] (four-point Lagrange weights with derivative weights, for $T$ and $R$; the file's header speaks of "CUBIC SPLINE INTERPLOATION", which is stale: Settled from the code, Nov 9, 2026: [[#L1-L2]], [[interp.f#L16-L18]]), [[intrp2.f#INTRP2|INTRP2]] (weights only, for $X$ and $Z$), and one of [[op952d.f#OP952D|OP952D]] (2D, in the table for the surface $X$ and $Z$), [[op953d.f#OP953D|OP953D]] (3D, in the tables for the model's $Z$) or [[op954d.f#OP954D|OP954D]] (4D, in the full set).
- **Outputs:** `O`, `OL`, `QOD`, `QOT`, as from `GETOPAC`.
- **Modules** (COMMON blocks until `rp_1`): the tables `LLOT95A_MOD` (the full set `CAPPA2`, indexed by a combined X–Z table number, and the grids `TGR`, `R0GR`, `XXG`, `ZZG`; read by [[ll95tbl.f#LL95TBL|LL95TBL]]), `LLOT95_MOD` (`CAPPA` at the model's $Z$, `ZTAB`, made by [[op95ztab.f#OP95ZTAB|OP95ZTAB]]), `LLOT95E_MOD` (`CAPPAE` at the surface $X$, `XOP95` (formerly `XTAB`), made by [[op95xtab.f#OP95XTAB|OP95XTAB]]); `OP95INTERP_MOD`, which merges the former `/OP95INDX/` (indices), `/OP95FACT/` (weights) and `/OP95EXT/` (extrapolation flags), shared with the `OP95*D` routines, $\log R$ now named `RHO_T63L` (formerly `RL`, which clashed with the radius elsewhere) and its edge value `RHO_T63LL` (formerly `RLL`); `ACDPTH_MOD` for the flags `LADON`, `LACOUT` (acoustic-depth output; shared with [[calcad.f#CALCAD|CALCAD]], [[envint.f#ENVINT|ENVINT]], [[wrtout.f#WRTOUT|WRTOUT]]); `IOUNITS_MOD` for `ISHORT`, the `.short` file that the stop reports to.

**Why three interpolators.** [[setupopac.f#SETUPOPAC|SETUPOPAC]], through [[ll95tbl.f#LL95TBL|LL95TBL]] (which calls [[op95ztab.f#OP95ZTAB|OP95ZTAB]] at `ZOPAL951`) and [[op95xtab.f#OP95XTAB|OP95XTAB]] (at `XENV`), interpolates the full table set ahead of time: `CAPPA` at one $Z$ for every $X$ node, and `CAPPAE` from it at the surface $X$. Most calls (the envelope, the atmosphere, and the outer convection zone, which share the surface composition) then need only the 2D interpolation in $T$ and $R$; the 3D path is needed where hydrogen burning has changed $X$, and the 4D path where $Z$ differs too, for example after settling or in a helium-burning core.

**The method.**
1. $\log R = \log\rho - 3(\log T - 6)$ (`RHO_T63L`). The run stops if $\log T$ is outside the table. Below the smallest $\log R$, the weights are computed at the table edge and the value is extrapolated linearly later (`LEXTL`).
2. Stencils in $\log T$ (`JT`) and $\log R$ (`JD`), each starting from the last one found.
3. **Empty corner.** Values of 9.9 or more mark missing entries. If the stencil's high-density, high-temperature corner is missing, each of the four temperatures gets its own density stencil (`LSHIFT`), and where even that is outside the data, its weights are computed at the last valid density and the value is extrapolated linearly (`LEXH`, `RLH`). The test reads the $X$ table `JX(1,1)` of the previous call, since the current $X$ stencil is found only later; this does not matter, since every table of a file has the same empty region: the last one to five densities of the temperatures from `TGR(58)` up, set to 9.999 by [[ll95tbl.f#LL95TBL|LL95TBL]], and in the OP files of the recent mixtures also every density above $\log T = 8.0$ (bug 2). For the same reason the search for valid densities stops at the 14th density or above, so the start of a shifted stencil, `JD(I) = J - 3`, is at least 11 and never zero or negative; in a row with no data it finds nothing, and `JD(I)` keeps its old value (settled from the code, Nov 9, 2026: [[#L177-L209]], [[ll95tbl.f#L140-L171]]). At low $X$ and the lowest temperatures (`X` < 0.2, `JT` ≤ 5) the comment postpones a check of the low-density, low-temperature empty region to the 2D, 3D or 4D branch, but no branch makes it, and the flag `LCHK` set there is unused? ([[#L162-L172]]; bug 1 below).
4. **Which interpolation.** If $Z$ is within a relative $10^{-4}$ of the model table's $Z$: 2D if $X$ is within $10^{-4}$ of the surface table's $X$, else 3D in $X$, $T$, $R$. Otherwise 4D. The 4D path is forced when acoustic-depth output is on (`LADON` and `LACOUT`, "JVS 04/11").
5. **Missing high-$X$ tables.** The $X$ nodes are 0, 0.1, 0.2, 0.35, 0.5, 0.7, 0.8, 0.9, 0.95, 1. For $X \ge 0.8$: if $0.04 \le Z < 0.1$, the $X = 0.95$ table is absent and the stencil is 0.7, 0.8, 0.9 and the last node, set to $1 - Z$; if $Z \ge 0.1$, the last two are absent and the stencil is 0.5, 0.7, 0.8, 0.9. (In 3D the test is on the model table's $Z$, in 4D on each $Z$ node. [[op95ztab.f#OP95ZTAB|OP95ZTAB]] stops the run for $Z > 0.08$, so the 3D case $Z \ge 0.1$ is never reached; the 4D path can still meet the node $Z = 0.1$.)

**Changed since `rp_1`.** Declarations and names only: COMMON blocks to modules (the three interpolation blocks merged into `OP95INTERP_MOD`), `IMPLICIT NONE`, `RL`, `RLL` and `XTAB` renamed `RHO_T63L`, `RHO_T63LL` and `XOP95`, and the unused parameters `NUMXZ` and `JSON` removed. The computation is unchanged; no question settled.

**Changed since `a8a5950`.** The stop for $\log T$ outside the table now writes its message to the `.short` file as well as the terminal (the routine now uses `IOUNITS_MOD`, for `ISHORT`), and exits with status 1, the code for run-time errors, instead of a bare `STOP` (`KNOWN_ISSUES.md`, issue 38, which this stop prompted).

## Bugs, by priority

1. **(a)** **`LSHIFT` and `LEXTH` left over from the last call.** ([[#L167-L176]], [[#L214]]) When `X` < 0.2 and `JT` ≤ 5, `GOTO 60` jumps past the lines that reset `LSHIFT` and `LEXTH` to false, so their values from the previous call (the routine has `SAVE`) decide the density stencil; on the very first call `LSHIFT` has no value at all. If the previous call was in the empty corner (`LSHIFT` true), the density weights are computed on the stencils `JD(2..4)` and with the flags `LEXH` of that call, at other temperatures, and the opacity is interpolated or extrapolated from the wrong densities. This needs a hydrogen-poor gas ($X$ < 0.2) at the table's first temperatures, which `GETOPAC` reaches only in the ramp between `TMOLMIN` and `TMOLMAX` (by default $\log T$ = 4.0 to 4.1), so a hydrogen-poor surface; hydrogen-rich runs do not take it. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to reset LSHIFT and LEXTH before the low-X, low-T
    C branch, which skips the corner check.
          LSHIFT = .FALSE.
          LEXTH = .FALSE.
          IF(X.LT.0.2D0 .AND. JT. LE. 5)THEN
             LCHK = .TRUE.
             GOTO 60
          ELSE
             LCHK = .FALSE.
          ENDIF
    ...
          IF(CAPPA(JX(1,1),JT+3,JD(1)+3) .GE. 9.9D0) THEN
    ```

    (the two resets at lines 175–176 go).

2. **(a)** **Empty temperatures in the OP tables above $\log T = 8.0$.** ([[#L113-L131]], [[#L177-L209]]; [[op952d.f#L39-L67]]) In the OP tables of the recent mixtures (`AAG2021zx0.0187.tab`, `Magg22_met_zx0.0226.tab`, `Magg22_phot_zx0.0225.tab`, and the other `AAG21*`, `Magg22*` and `Lodders25*` files in `input/opacity/atomic/op05/`), the last four temperatures of every table ($\log T$ = 8.1, 8.3, 8.5, 8.7) hold 9.999 at all densities; `GS98.OP17` has data there. From $\log T$ = 7.9 up, the $T$ stencil includes such a row. The empty-corner search finds no valid density in it, so its `JD(I)` keeps an old value, `LEXH(I)` is set, and the interpolators take $\log\kappa \approx 9.999$ at that temperature (the extrapolation adds nothing, since the slope of a constant row is zero). Between $\log T$ = 7.9 and 8.0 the Lagrange weight of the empty row is down to about $-0.064$, so $\log\kappa$ is too low by up to about 0.7 (and its $T$ derivative is off); above 8.0, with two or more empty rows in the stencil, the value is meaningless. The run neither stops nor warns, since the range check uses `TGR(NUMT)` = 8.7. The README of the tables says the hydrogen-burning tables are also required for helium-burning models (`input/opacity/atomic/README`, line 1), so a run with these tables reaches this path in a helium-burning core, and at the tip of the red giant branch; how much conduction hides it in degenerate cores is not traced. Read from the code and the tables, not run; the test suite uses these tables only in three solar models (`Test_solarAAG21_dif`, `Test_solarM22M_dif`, `Test_solarM22M_difkur`), which stay below this temperature, and `GS98.OP17` in the others. **A possible fix,** a choice for the developers: stop with a message when the stencil's last temperature has no data (`CAPPA(JX(1,1),JT+3,1)` ≥ 9.9), or switch to another table above $\log T = 8.0$.

3. **(d)** **The wrong array in the empty-corner search.** ([[#L193-L199]]) The search for valid densities at each temperature tests `CAPPA2(IXX,ITT,J)`, with `IXX` = `JX(1,1)`, an index into the $X$ tables of `CAPPA`, while the lines above it test `CAPPA`. `CAPPA2`'s first index is the combined X–Z table number ([[llot95a_mod.f#LLOT95A_MOD|LLOT95A_MOD]]; [[op95ztab.f#L56-L64]]), so `IXX` picks the $Z = 0$ table with that $X$ index. The result is right today, since every table has the same empty corner ([[ll95tbl.f#L140-L171]]); a table set whose empty region depends on the composition would get the stencil of the wrong table. Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to search CAPPA, the model-Z tables that IXX indexes,
    C instead of the full set CAPPA2.
                      IF(CAPPA(IXX,ITT,J).LE.9.9D0)THEN
    ```

### GETOPAL95

Driver for the OPAL 1995 opacities: stencils and weights in $T$, $R$, $X$, $Z$, the empty-corner handling, and the choice of 2D, 3D or 4D interpolation (method above).
