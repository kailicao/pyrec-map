## Explanation

**Purpose.** `GETALEX06` returns the low-temperature (molecular) opacity from the low-temperature opacities of Ferguson et al. (2005), called ALEX06 in the code ([[readalex06.f#READALEX06|`READALEX06`]]; "Alexander low T opacities," per its header, MHP 3/09) for a given $\rho$, $T$, $X$, $Z$, with its logarithmic derivatives.

**How it fits.**
- **Who calls it:** only [[getopac.f#GETOPAC|GETOPAC]], when $\log T \le$ `TMOLMAX` and `LALEX06` is set.
- **Inputs:** `DL`, `TL` ($\log\rho$, $\log T$), `X`, `Z`.
- **What it calls:** [[alex06tab.f#ALEX06TAB|ALEX06TAB]], which builds a table for the current $X$, $Z$ from the full set, and [[interp.f#INTERP|INTERP]] (four-point Lagrange weights and derivative weights).
- **Outputs:** `O` ($\kappa$, cm$^2$ g$^{-1}$), `OL` ($\log\kappa$), `QOD` $=\partial\log\kappa/\partial\log\rho|_T$, `QOT` $=\partial\log\kappa/\partial\log T|_\rho$.
- **Modules:** [[galot06_mod.f#GALOT06_MOD|`GALOT06_MOD`]] (the grids `TGR06`, `R0GR06`, `XXG06`, `ZZG06`) and [[alot06_mod.f#ALOT06_MOD|`ALOT06_MOD`]] (the table `CAPALEX06` at the composition `XE`, `ZE`, and the last indices `IT`, `ID`), shared with `ALEX06TAB` and [[readalex06.f#READALEX06|READALEX06]]; $\ln 10$ from [[constants_mod.f#CONSTANTS_MOD|`CONSTANTS_MOD`]].

**The method.**
1. If $X$ or $Z$ differs from the stored `XE`, `ZE` by more than $10^{-8}$, rebuild the table with `ALEX06TAB` ([[#L26-L33]]).

    > **Question** ([[#L26-L33]]). **Table rebuilt per composition.** Every change of $X$ or $Z$ beyond $10^{-8}$ rebuilds the whole table (85 × 19 values, from 16 tables). Where the points below `TMOLMAX` differ in composition (with settling, or with a gradient in the cool envelope), this happens at almost every call. Is that cost acceptable, or should the routine interpolate in $X$ and $Z$ directly? A profile of a run with diffusion would show the share of time spent in `ALEX06TAB`.

2. The table is in $\log T$ and $\log R$, with $\log R = \log\rho - 3(\log T - 6)$ (that is, $R = \rho/T_6^3$).
3. Find the 4×4 stencil from the last indices, get Lagrange weights in $\log T$ and $\log R$, and interpolate $\log\kappa$ and $\partial\log\kappa/\partial\log R$.

    > **Question** ([[#L37-L59]]; [[#L66-L88]]). **No lower-edge handling.** Below the smallest $\log R$ ($-8$), or outside the $\log T$ range (2.70 to 4.50), the stencil stays at the edge and the Lagrange weights extrapolate the cubic silently; only above the largest $\log R$ is the extrapolation made linear (step 4). Should there be a check, or a linear extrapolation at the other edges too? (Above $\log T$ = 4.50 is reached only if `TMOLMAX` is set above it; its default is 4.1.)

4. Above the largest $\log R$ of the table, extrapolate $\log\kappa$ linearly from the last two columns ([[#L90-L96]]; [[#L113-L120]]); the derivative is not extrapolated (bug 1).
5. Convert the temperature derivative from fixed $R$ to fixed $\rho$:
$$\left.\frac{\partial\log\kappa}{\partial\log T}\right|_\rho = \left.\frac{\partial\log\kappa}{\partial\log T}\right|_R - 3\left.\frac{\partial\log\kappa}{\partial\log R}\right|_T.$$

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(harmless in the runs)** **The derivative is not extrapolated with the value.** ([[#L90-L96]]; [[#L108-L111]]; [[#L113-L120]]; [[#L126-L129]]) Above the largest $\log R$ of the table ($\log R > 1$), $\log\kappa$ is extrapolated linearly from the last two columns, but `QOPR`, and so `QOD` $=\partial\log\kappa/\partial\log\rho|_T$, is the derivative of the cubic at the table edge, not the slope of the extrapolation. `QOT` is then converted to fixed $\rho$ with this `QOD` (line 129). What follows: There, the returned derivatives do not match the returned opacity; where they are used (the linearized equations) was not traced. Only with `LALEX06` (off by default in the code; recommended by YREC's User Guide) and at $\log T \le$ `TMOLMAX`.

    **A possible fix:**

    ```diff
    --- a/src/getalex06.f
    +++ b/src/getalex06.f
    @@ -110,11 +110,16 @@
          *           FXRD(3)*CAPALEX06(II,ID+2) +
          *           FXRD(4)*CAPALEX06(II,ID+3)
           END DO
    +C 11/09/26 KC via Claude
    +C code changed to give the extrapolated opacity its own derivative
    +C in log R, the slope of the linear extrapolation.
           IF(LINEAR)THEN
              DO I = 1,4
                 II = IT+I-1
                 OP(I) = OP(I)+(RR-R)*(CAPALEX06(II,NUMD)-
          *      CAPALEX06(II,NUMD-1))/(R0GR06(NUMD)-R0GR06(NUMD-1))
    +            QOPR(I) = (CAPALEX06(II,NUMD)-CAPALEX06(II,NUMD-1))/
    +     *      (R0GR06(NUMD)-R0GR06(NUMD-1))
              END DO
              R = RR
           ENDIF
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): 34 runs, 26 of YREC's cases (from a 0.04 $M_\odot$ brown dwarf and the solar models to 9 $M_\odot$, rotation, and helium burning) and 8 made-up ones (each one of YREC's cases with a few settings changed), of which one stopped in its first second. The extrapolation ran in five of the 33 others, all low-mass stars: 12 million times in the 0.04 $M_\odot$ brown dwarf `examples/run_from_dbl_to_zams/Test_m0040_feh0_noGS_ZAMS`, fewer in the 0.1, 0.3, and 0.8 $M_\odot$ cases, at $\log T$ = 2.71 to 4.10 and $\log R$ = 1 to 15.6, that is, up to 14.6 beyond the table's last column. In the brown dwarf the derivative differed from the slope by more than 0.001 at 45 million of the 49 million temperature points (four a call). With the fix, the brown dwarf moves by up to $9.4\times10^{-5}$ dex in $\log L$ and $7.7\times10^{-6}$ dex in $\log T_c$, against $2.5\times10^{-5}$ and $1.5\times10^{-6}$ for the null change used as a noise floor (nearly every opacity, all with $3 \le \log T \le 9$ and $-6 \le \log\rho \le 9.75$, times $1 + 10^{-10}$): four to five times the noise, so small, and not clearly real (748 models in both, end age 8,683 Gyr instead of 8,681). The track of `testsuite/Test_m0p3feh+0p0GS98_scv_ZAMS` is identical with the fix. The returned derivative disagrees with the returned opacity at 45 million of 49 million points, whatever the track does; its effect on the track is the same size as that of [[condopacpint.f#CONDOPACPINT|CONDOPACPINT]]'s bug 4 on the same case, so likely the same amplified noise. Intent: none found.

### GETALEX06

Ferguson et al. (2005) molecular opacity (ALEX06): four-point Lagrange interpolation in $\log T$ and $\log R$, with the derivative converted to fixed $\rho$ (method above).
