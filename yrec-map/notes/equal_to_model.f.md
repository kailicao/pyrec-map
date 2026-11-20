## Explanation

**Purpose.** `EQUAL_TO_MODEL` ends a step of gravitational settling (microscopic diffusion): the diffusion equations are solved on an equally spaced grid in radius, and this routine applies the resulting changes in hydrogen (and, with metal diffusion, in $`Z`$) to the model's own points. It then converts the model's arrays back from the dimensionless units used by the diffusion solver.

**How it fits.**
- **Who calls it:** only [GRSETT](grsett.f.md#grsett), at the end of the settling step; [MODEL_TO_EQUAL](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L3-L275) does the opposite transformation at its start. [MICRODIFF_ETM](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_etm.f#L2-L174) has the same unit conversion for the newer diffusion scheme.
- **Inputs:** the equally spaced radii `ER` (`NPT` points) and the changes `EX` in $`X`$ on them; the range `IBEGIN..IEND` of model points inside the grid; the model arrays `HCOMP`, `HRU` (radius), `HTU` (temperature), `HS1` (mass), `HQPR`, the time step `DT` and the total mass `STOT`, all in the solver's units.
- **What it calls:** [INTRP2](intrp2.f.md#intrp2), four-point Lagrange weights.
- **Outputs:** `HCOMP` updated, and `HRU`, `HTU`, `HS1`, `HQPR`, `DT`, `STOT` back in physical units.
- **Modules:** [`CONFAC_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/confac_mod.f#L19-L29) holds the conversion factors `CON_RAD`, `CON_MASS`, `CON_TEMP`, `CON_TIME`, set by [MICRODIFF_SETUP](https://github.com/yreclab/yrec/blob/7be4133/src/microdiff_setup.f#L4-L169) and `SETUP_GRSETT`; [`GRAVEZ_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/gravez_mod.f#L19-L36) holds the change in $`Z`$ on the grid, `EZ` (with `GRSETT`, `MODEL_TO_EQUAL` and the Lax–Wendroff routines, which use its other entries; this routine reads only `EZ`); [`NMLPAR_MOD`](https://github.com/yreclab/yrec/blob/7be4133/src/nmlpar_mod.f#L32-L279) gives the flag `LDIFZ` (formerly in `/GRAVS3/`); `DIMENSIONS_MOD` gives the array size `JSON`.

**The method.**
1. **Inside the grid** (`IBEGIN` < $`i`$ < `IEND`): for each model point, find the four grid points around its radius, get Lagrange weights $`b_k`$, and
   
   $$\displaystyle \Delta X\_i = \sum\_{k=1}^{4} b\_k\\,\Delta X(r\_k), \qquad X\_i \leftarrow \min(X\_i + \Delta X\_i,\\; 1 - Z\_i - X\_{3,i}),$$
   
   where $`X_3`$ is $`^3\mathrm{He}`$ (`HCOMP(4,·)`). With metal diffusion, $`Z`$ changes the same way, and every metal species (rows 5–11) is scaled by $`Z_\mathrm{new}/Z_\mathrm{old}`$. Helium takes the rest: $`Y = 1 - X - Z - X_3`$. The scaling divides by the old $`Z`$ ([suspected bug 1](#b1)). The line `IF (J .EQ. 0) PRINT*, 'line 47 etm'` ([line 69](https://github.com/yreclab/yrec/blob/7be4133/src/equal_to_model.f#L69)) cannot fire, since `J` starts at `JMIN` $`\ge 2`$ (unused?); nor can `IF (K0 .EQ. 0) K0=1` ([lines 76–77](https://github.com/yreclab/yrec/blob/7be4133/src/equal_to_model.f#L76-L77)), since `NPT` is at least 4 (unused?).
2. **Below the grid** ($`i \le`$ `IBEGIN`) the change at the first grid point is applied; **above it** ($`i \ge`$ `IEND`), the change at the last. The points `IBEGIN` and `IEND` are themselves the grid's end points: `MODEL_TO_EQUAL` puts the first grid point at `HRU(IBEGIN)` and spaces the grid so that the last falls at `HRU(IEND)`, with the model's values there (settled from the code, Nov 9, 2026: [lines 42–44](https://github.com/yreclab/yrec/blob/7be4133/src/equal_to_model.f#L42-L44), [lines 113–116](https://github.com/yreclab/yrec/blob/7be4133/src/equal_to_model.f#L113-L116); [model_to_equal.f, line 73](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L73), [model_to_equal.f, lines 195–198](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L195-L198), [model_to_equal.f, lines 205–206](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L205-L206), [model_to_equal.f, lines 266–267](https://github.com/yreclab/yrec/blob/7be4133/src/model_to_equal.f#L266-L267)). The comment explains the guards: "because metals sink, and hydrogen rises, the failsafes are opposite" ($`X \ge 0`$ and $`Z \le Z_\mathrm{max}`$ below; $`X \le X_\mathrm{max}`$ and $`Z \ge 0`$ above).
3. **Units:** $`r \leftarrow r/c_r`$, $`T \leftarrow T/c_T`$, $`m \leftarrow m/c_m`$, `HQPR` $`\leftarrow`$ `HQPR`$`\cdot c_r`$, $`\Delta t \leftarrow \Delta t\,c_t`$, $`M \leftarrow M/c_m`$.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(not reached)** **Division by $`Z`$.** ([line 52](https://github.com/yreclab/yrec/blob/7be4133/src/equal_to_model.f#L52); [line 103](https://github.com/yreclab/yrec/blob/7be4133/src/equal_to_model.f#L103); [line 122](https://github.com/yreclab/yrec/blob/7be4133/src/equal_to_model.f#L122)) With metal diffusion, each shell's metal species are scaled by `ZZ2 = ZZ/HCOMP(3,I)`, the new $`Z`$ over the old; a shell with $`Z = 0`$ divides by zero, and rows 5–11 become NaN (or infinite). What follows: A metal-free model (Population III) cannot be run with `LDIFZ`. Only with `LDIFZ` (off by default) and `LNEWDIF` false, in a shell with $`Z = 0`$.

    **A possible fix** (the same at lines 103 and 122):

    ```diff
    --- a/src/equal_to_model.f
    +++ b/src/equal_to_model.f
    @@ -49,7 +49,13 @@
              DO I = IBEGIN,1,-1
                 ZMAX = 1.0D0 - HCOMP(1,I) - HCOMP(4,I)
                 ZZ=MIN(HCOMP(3,I)+EZ(1),ZMAX)
    -            ZZ2 = ZZ/HCOMP(3,I)
    +C 11/09/26 KC via Claude
    +C code changed to leave the metal species unscaled where Z was zero.
    +            IF(HCOMP(3,I).GT.0.0D0)THEN
    +               ZZ2 = ZZ/HCOMP(3,I)
    +            ELSE
    +               ZZ2 = 1.0D0
    +            ENDIF
                 HCOMP(3,I) = ZZ
                 DO J = 5,11
                    HCOMP(J,I) = ZZ2*HCOMP(J,I)
    @@ -100,7 +106,13 @@
                 DZMOD = FACINTERP(1)*EZ(K0)+FACINTERP(2)*EZ(K0+1)+
          *             FACINTERP(3)*EZ(K0+2)+FACINTERP(4)*EZ(K0+3)
                 ZZ = MIN(HCOMP(3,I)+DZMOD,ZMAX)
    -            ZZ2 = ZZ/HCOMP(3,I)
    +C 11/09/26 KC via Claude
    +C code changed to leave the metal species unscaled where Z was zero.
    +            IF(HCOMP(3,I).GT.0.0D0)THEN
    +               ZZ2 = ZZ/HCOMP(3,I)
    +            ELSE
    +               ZZ2 = 1.0D0
    +            ENDIF
                 HCOMP(3,I)=ZZ
                 DO J = 5,11
                    HCOMP(J,I) = ZZ2*HCOMP(J,I)
    @@ -119,7 +131,13 @@
              ZMIN = 0.0D0
              DO I = IEND,M
                 ZZ = MAX(HCOMP(3,I)+EZ(NPT),ZMIN)
    -            ZZ2 = ZZ/HCOMP(3,I)
    +C 11/09/26 KC via Claude
    +C code changed to leave the metal species unscaled where Z was zero.
    +            IF(HCOMP(3,I).GT.0.0D0)THEN
    +               ZZ2 = ZZ/HCOMP(3,I)
    +            ELSE
    +               ZZ2 = 1.0D0
    +            ENDIF
                 HCOMP(3,I) = ZZ
                 DO J = 5,11
                    HCOMP(J,I) = ZZ2*HCOMP(J,I)
    ```

    **Checked by running YREC** (Nov 9, 2026; a line added at each suspected path counted how often it was taken, the outputs otherwise unchanged): not reached in any of 34 runs (26 of YREC's cases, from 0.04 to 9 $`M_\odot`$, with rotation, settling, and helium burning, and 8 made-up ones). These lines belong to the old settling routines (`LNEWDIF` false), which no case uses: Every case with settling sets `LNEWDIF` and `LDIFLI`, and the documentation lists `LNEWDIF` among the legacy options (`docs/source/namelist_physics.md`, line 285). Reaching them takes `LDIFY` or `LDIFZ` with `LNEWDIF` false and `LDIFLI` off, since `LDIFLI` forces `LNEWDIF` on ([parmin.f, lines 1239–1251](https://github.com/yreclab/yrec/blob/7be4133/src/parmin.f#L1239-L1251)), and in addition a shell with $`Z = 0`$; no case has a metal-free model. Intent: none found.

### EQUAL_TO_MODEL

Interpolates the settling changes in $`X`$ (and $`Z`$) from the equally spaced grid to the model points with four-point Lagrange weights, enforces the composition limits, and converts the model back to physical units.
