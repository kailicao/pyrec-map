## Explanation

**Purpose.** `EQUAL_TO_MODEL` ends a step of gravitational settling (microscopic diffusion): the diffusion equations are solved on an equally spaced grid in radius, and this routine applies the resulting changes in hydrogen (and, with metal diffusion, in $Z$) to the model's own points. It then converts the model's arrays back from the dimensionless units used by the diffusion solver.

**How it fits.**
- **Who calls it:** only [[grsett.f#GRSETT|GRSETT]], at the end of the settling step; [[model_to_equal.f#MODEL_TO_EQUAL|MODEL_TO_EQUAL]] does the opposite transformation at its start. [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] has the same unit conversion for the newer diffusion scheme.
- **Inputs:** the equally spaced radii `ER` (`NPT` points) and the changes `EX` in $X$ on them; the range `IBEGIN..IEND` of model points inside the grid; the model arrays `HCOMP`, `HRU` (radius), `HTU` (temperature), `HS1` (mass), `HQPR`, the time step `DT` and the total mass `STOT`, all in the solver's units.
- **What it calls:** [[intrp2.f#INTRP2|INTRP2]], four-point Lagrange weights.
- **Outputs:** `HCOMP` updated, and `HRU`, `HTU`, `HS1`, `HQPR`, `DT`, `STOT` back in physical units.
- **Modules:** [[confac_mod.f#CONFAC_MOD|`CONFAC_MOD`]] holds the conversion factors `CON_RAD`, `CON_MASS`, `CON_TEMP`, `CON_TIME`, set by [[microdiff_setup.f#MICRODIFF_SETUP|MICRODIFF_SETUP]] and `SETUP_GRSETT`; [[gravez_mod.f#GRAVEZ_MOD|`GRAVEZ_MOD`]] holds the change in $Z$ on the grid, `EZ` (with `GRSETT`, `MODEL_TO_EQUAL` and the Lax–Wendroff routines, which use its other entries; this routine reads only `EZ`); [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] gives the flag `LDIFZ` (formerly in `/GRAVS3/`); `DIMENSIONS_MOD` gives the array size `JSON`.

**The method.**
1. **Inside the grid** (`IBEGIN` < $i$ < `IEND`): for each model point, find the four grid points around its radius, get Lagrange weights $b_k$, and
$$\Delta X_i = \sum_{k=1}^{4} b_k\,\Delta X(r_k), \qquad X_i \leftarrow \min(X_i + \Delta X_i,\; 1 - Z_i - X_{3,i}),$$
where $X_3$ is $^3$He (`HCOMP(4,·)`). With metal diffusion, $Z$ changes the same way, and every metal species (rows 5–11) is scaled by $Z_\mathrm{new}/Z_\mathrm{old}$. Helium takes the rest: $Y = 1 - X - Z - X_3$. The scaling divides by the old $Z$ ([[#b1]]). The line `IF (J .EQ. 0) PRINT*, 'line 47 etm'` ([[#L69]]) cannot fire, since `J` starts at `JMIN` ≥ 2 (unused?); nor can `IF (K0 .EQ. 0) K0=1` ([[#L76-L77]]), since `NPT` is at least 4 (unused?).
2. **Below the grid** ($i \le$ `IBEGIN`) the change at the first grid point is applied; **above it** ($i \ge$ `IEND`), the change at the last. The points `IBEGIN` and `IEND` are themselves the grid's end points: `MODEL_TO_EQUAL` puts the first grid point at `HRU(IBEGIN)` and spaces the grid so that the last falls at `HRU(IEND)`, with the model's values there (settled from the code, Nov 9, 2026: [[#L42-L44]], [[#L113-L116]]; [[model_to_equal.f#L73]], [[model_to_equal.f#L195-L198]], [[model_to_equal.f#L205-L206]], [[model_to_equal.f#L266-L267]]). The comment explains the guards: "because metals sink, and hydrogen rises, the failsafes are opposite" ($X \ge 0$ and $Z \le Z_\mathrm{max}$ below; $X \le X_\mathrm{max}$ and $Z \ge 0$ above).
3. **Units:** $r \leftarrow r/c_r$, $T \leftarrow T/c_T$, $m \leftarrow m/c_m$, `HQPR` $\leftarrow$ `HQPR`$\cdot c_r$, $\Delta t \leftarrow \Delta t\,c_t$, $M \leftarrow M/c_m$.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Bugs, by priority

1. **(b)** **Division by $Z$.** ([[#L52]]; [[#L103]]; [[#L122]]) With metal diffusion, each shell's metal species are scaled by `ZZ2 = ZZ/HCOMP(3,I)`, the new $Z$ over the old; a shell with $Z = 0$ divides by zero, and rows 5–11 become NaN (or infinite). What follows: A metal-free model (Population III) cannot be run with `LDIFZ`. Only with `LDIFZ` (off by default) and `LNEWDIF` false, in a shell with $Z = 0$. Read from the code, not run. **A possible fix** (the same at lines 103 and 122):

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to leave the metal species unscaled where Z was zero.
                IF(HCOMP(3,I).GT.0.0D0)THEN
                   ZZ2 = ZZ/HCOMP(3,I)
                ELSE
                   ZZ2 = 1.0D0
                ENDIF
    ```

### EQUAL_TO_MODEL

Interpolates the settling changes in $X$ (and $Z$) from the equally spaced grid to the model points with four-point Lagrange weights, enforces the composition limits, and converts the model back to physical units.
