## Explanation

**Purpose.** `LAX_WENDROF2` is the second (full) step of the two-step Lax–Wendroff scheme for the settling term: from the coefficients at the grid midpoints (already updated with the half-step abundances) it adds the change over a full time step to the abundances at the grid points.

**How it fits.** Called by [[grsett.f#GRSETT|`GRSETT`]] and [[microdiff_run.f#MICRODIFF_RUN|`MICRODIFF_RUN`]], after [[lax_wendrof1.f#LAX_WENDROF1|`LAX_WENDROF1`]]. Arguments: `DT`, `ECOD1_H` (coefficients at the midpoints), `EM_H` (masses at the midpoints), `EX` (the abundances on the equal grid, updated in place), `NPT`, `STOT`, `LDOLI`. COMMON blocks as in `LAX_WENDROF1`: `CONST1`, `GRAVS3`, `GRAVEZ` (here `ECOD1Z_H` in, `EZ` updated).

**The method.** With $F_{i+1/2}$ = `ECOD1_H(I)` and $m_{i+1/2}$ = `EM_H(I)`:

$$X_1 \mathrel{+}= \Delta t\,4\pi\,\frac{F_{1/2}}{m_{1/2}},\qquad X_i \mathrel{+}= \Delta t\,4\pi\,\frac{F_{i+1/2}-F_{i-1/2}}{m_{i+1/2}-m_{i-1/2}}\ (i = 2..N-1),\qquad X_N \mathrel{+}= -\Delta t\,4\pi\,\frac{F_{N-1/2}}{M - m_{N-1/2}} .$$

The same for the metals (`EZ`) when `LDIFZ` is true and `LDOLI` is false.

## Questions for the experts

1. **Surface mass.** The surface update divides by $M - m_{N-1/2}$, the mass of half a cell plus whatever lies above point $N$; is the outermost point meant to hold that mass?

### LAX_WENDROF2

Full-step update of $X$ (and $Z$) from the midpoint fluxes (above).
