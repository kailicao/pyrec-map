## Explanation

**Purpose.** `LAX_WENDROF2` is the second (full) step of the two-step Lax–Wendroff scheme for the settling term: from the coefficients at the grid midpoints (already updated with the half-step abundances) it adds the change over a full time step to the abundances at the grid points.

**How it fits.** Called by [[grsett.f#GRSETT|`GRSETT`]] and [[microdiff_run.f#MICRODIFF_RUN|`MICRODIFF_RUN`]], after [[lax_wendrof1.f#LAX_WENDROF1|`LAX_WENDROF1`]]. Arguments: `DT`, `ECOD1_H` (coefficients at the midpoints), `EM_H` (masses at the midpoints), `EX` (the abundances on the equal grid, updated in place), `NPT`, `STOT`, `LDOLI`. Modules as in `LAX_WENDROF1`: `CONSTANTS_MOD`, `NMLPAR_MOD`, `GRAVEZ_MOD` (here `ECOD1Z_H` in, `EZ` updated), and `DIMENSIONS_MOD`.

**The method.** With $F_{i+1/2}$ = `ECOD1_H(I)` and $m_{i+1/2}$ = `EM_H(I)`:

$$X_1 \mathrel{+}= \Delta t\,4\pi\,\frac{F_{1/2}}{m_{1/2}},\qquad X_i \mathrel{+}= \Delta t\,4\pi\,\frac{F_{i+1/2}-F_{i-1/2}}{m_{i+1/2}-m_{i-1/2}}\ (i = 2..N-1),\qquad X_N \mathrel{+}= -\Delta t\,4\pi\,\frac{F_{N-1/2}}{M - m_{N-1/2}} .$$

The same for the metals (`EZ`) when `LDIFZ` is true and `LDOLI` is false.

The end points hold the reservoirs beyond the grid: The surface update divides by $M - m_{N-1/2}$, half a cell plus all the mass above point $N$, and the central one by $m_{1/2}$, all the mass below the first midpoint; [[equal_to_model.f#EQUAL_TO_MODEL|`EQUAL_TO_MODEL`]] then applies the end points' changes to every shell beyond them (settled from the code, Nov 9, 2026: [[#L43-L45]], [[#L54-L56]]; [[equal_to_model.f#L42-L44]], [[equal_to_model.f#L113-L116]]).

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/CONST1/` to `CONSTANTS_MOD`, `LDIFZ` from `/GRAVS3/` to `NMLPAR_MOD`, `/GRAVEZ/` to `GRAVEZ_MOD`), `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

### LAX_WENDROF2

Full-step update of $X$ (and $Z$) from the midpoint fluxes (above).
