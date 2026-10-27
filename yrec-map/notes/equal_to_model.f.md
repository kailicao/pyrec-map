## Explanation

**Purpose.** `EQUAL_TO_MODEL` ends a step of gravitational settling (microscopic diffusion): the diffusion equations are solved on an equally spaced grid in radius, and this routine applies the resulting changes in hydrogen (and, with metal diffusion, in $Z$) to the model's own points. It then converts the model's arrays back from the dimensionless units used by the diffusion solver.

**How it fits.**
- **Who calls it:** only [[grsett.f#GRSETT|GRSETT]], at the end of the settling step; [[model_to_equal.f#MODEL_TO_EQUAL|MODEL_TO_EQUAL]] does the opposite transformation at its start. [[microdiff_etm.f#MICRODIFF_ETM|MICRODIFF_ETM]] has the same unit conversion for the newer diffusion scheme.
- **Inputs:** the equally spaced radii `ER` (`NPT` points) and the changes `EX` in $X$ on them; the range `IBEGIN..IEND` of model points inside the grid; the model arrays `HCOMP`, `HRU` (radius), `HTU` (temperature), `HS1` (mass), `HQPR`, the time step `DT` and the total mass `STOT`, all in the solver's units.
- **What it calls:** [[intrp2.f#INTRP2|INTRP2]], four-point Lagrange weights.
- **Outputs:** `HCOMP` updated, and `HRU`, `HTU`, `HS1`, `HQPR`, `DT`, `STOT` back in physical units.
- **Modules:** [[confac_mod.f#CONFAC_MOD|`CONFAC_MOD`]] holds the conversion factors `CON_RAD`, `CON_MASS`, `CON_TEMP`, `CON_TIME`, set by [[microdiff_setup.f#MICRODIFF_SETUP|MICRODIFF_SETUP]] and `SETUP_GRSETT`; [[gravez_mod.f#GRAVEZ_MOD|`GRAVEZ_MOD`]] holds the change in $Z$ on the grid, `EZ` (with `GRSETT`, `MODEL_TO_EQUAL` and the Lax–Wendroff routines); [[nmlpar_mod.f#NMLPAR_MOD|`NMLPAR_MOD`]] gives the flag `LDIFZ` (formerly in `/GRAVS3/`); `DIMENSIONS_MOD` gives the array size `JSON`.

**The method.**
1. **Inside the grid** (`IBEGIN` < $i$ < `IEND`): for each model point, find the four grid points around its radius, get Lagrange weights $b_k$, and
$$\Delta X_i = \sum_{k=1}^{4} b_k\,\Delta X(r_k), \qquad X_i \leftarrow \min(X_i + \Delta X_i,\; 1 - Z_i - X_{3,i}),$$
where $X_3$ is $^3$He (`HCOMP(4,·)`). With metal diffusion, $Z$ changes the same way, and every metal species (rows 5–11) is scaled by $Z_\mathrm{new}/Z_\mathrm{old}$. Helium takes the rest: $Y = 1 - X - Z - X_3$.
2. **Below the grid** ($i \le$ `IBEGIN`) the change at the first grid point is applied; **above it** ($i \ge$ `IEND`), the change at the last. The comment explains the guards: "because metals sink, and hydrogen rises, the failsafes are opposite" ($X \ge 0$ and $Z \le Z_\mathrm{max}$ below; $X \le X_\mathrm{max}$ and $Z \ge 0$ above).
3. **Units:** $r \leftarrow r/c_r$, $T \leftarrow T/c_T$, $m \leftarrow m/c_m$, `HQPR` $\leftarrow$ `HQPR`$\cdot c_r$, $\Delta t \leftarrow \Delta t\,c_t$, $M \leftarrow M/c_m$.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **Division by $Z$.** The metal scaling divides by `HCOMP(3,I)`; a shell with $Z = 0$ would give a division by zero. Can $Z$ be zero here (for example in Population III models)?
2. **A leftover check.** `IF (J .EQ. 0) PRINT*, 'line 47 etm'` can never be true (`J` starts at `JMIN` ≥ 2). Remove?
3. **Unused module entries.** Of `GRAVEZ_MOD` (formerly `/GRAVEZ/`), only `EZ` is used. Fine as is, or should the routine receive `EZ` as an argument?
4. **Edge points.** The model points `IBEGIN` and `IEND` themselves get the first and last grid values (steps 2), not an interpolated one. Is that consistent with how `MODEL_TO_EQUAL` placed the grid?

### EQUAL_TO_MODEL

Interpolates the settling changes in $X$ (and $Z$) from the equally spaced grid to the model points with four-point Lagrange weights, enforces the composition limits, and converts the model back to physical units.
