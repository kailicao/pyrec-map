## Explanation

**Purpose.** `KCSURFP` finds the gas pressure at the point where $T = T_\mathrm{eff}$ by interpolating in a table of model-atmosphere pressures as a function of $\log T_\mathrm{eff}$ and $\log g$. It is the version of [[surfp.f#SURFP|`SURFP`]] for the newer Kurucz/Castelli tables (JNT 06/2014), whose size is $76\times11$ (`NTC`, `NGC`).

**How it fits.**
- **Who calls it:** only [[envint.f#ENVINT|`ENVINT`]], the envelope integration, which needs the pressure at the base of the atmosphere.
- **Inputs:** `TEFFL` = $\log T_\mathrm{eff}$, `GL` = $\log g$, `LPRT` (print or not); the table in `ATMOS2C_MOD` (`ATMPLC` = $\log P$, grids `ATMTLC`, `ATMGLC`), filled by [[setups.f#SETUPS|`SETUPS`]], the module's only other user; in `FAC_MOD`, the per-temperature range of valid gravities `IMIN2`, `IMINMAX2` (table entries that are missing in the grid).
- **Outputs:** in `ATMPRT_MOD`, `AP` = $\log P$ and `AT` = $\log T_\mathrm{eff}$; `ATMPRT_MOD` is read by `ENVINT`, [[qatm.f#QATM|`QATM`]], [[massloss.f#MASSLOSS|`MASSLOSS`]] and the other surface-pressure routines. It also sets `JP` and `KP(4)` in `FAC_MOD` (the table corner used). When `LPRT` is true it writes the result to the short output (`ISHORT`) and the model-storage unit (`ISTOR`), both from `IOUNITS_MOD`.
- **Calls:** [[kspline.f#KSPLINE|`KSPLINE`]] and [[ksplint.f#KSPLINT|`KSPLINT`]] (4-point natural splines), [[inter3.f#INTER3|`INTER3`]] (3-point Lagrange).
- **Modules:** `ATMPRT_MOD`, `ATMOS2C_MOD` (with `SETUPS`), `FAC_MOD` (with `SETUPS`, `SURFP`), `IOUNITS_MOD`.

**The method.**
1. Stop if $\log T_\mathrm{eff} < 3.5$ or $\log g < -0.5$.
2. Take four table temperatures around $\log T_\mathrm{eff}$.
3. At each of them, interpolate $\log P$ in $\log g$:
   - for $\log T > 4.55$, linearly between the two highest gravities;
   - for $4.5 < \log T \le 4.55$, by 3-point Lagrange (`INTER3`) over the three highest gravities;
   - otherwise with a 4-point natural spline over the four valid gravities around $\log g$ (the top four if $\log g$ is above the second-highest one, the lowest four valid ones if it is below them).
4. Interpolate the four results in $\log T_\mathrm{eff}$ with a 4-point natural spline: `AP`.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules (`/ATMPRT/`, `/ATMOS2C/`, `/FAC/`; `/LUOUT/` to `IOUNITS_MOD`), the unused `/ATMOS2/` declaration and its parameters `NT`, `NG` dropped, `IMPLICIT NONE`.

## Questions for the experts

1. **Hard-coded table limits.** The bounds 3.5 and −0.5 and the thresholds 4.5 and 4.55 in $\log T$ (above which only the highest gravities are used) are written into the code; they belong to one table. Are they right for every Kurucz/Castelli table the code may read? No upper bounds are checked.
2. **Comments that do not match.** The comment calls the routine "SURFPL", says it uses 4-point Lagrange interpolation in temperature and gravity (it uses natural splines), and that "it will quit if the desired point has Teff or log g more than one table point from the data" (no such check exists beyond step 1).
3. **Linear extrapolation in gravity for hot stars.** For $\log T > 4.55$ the linear formula extrapolates freely in $\log g$ beyond the two highest gravities.

4. **Missing pressures at the highest gravities.** [[setups.f#SETUPS|`SETUPS`]] sets `IMINMAX2(J)` below `NGC` when a temperature's highest-gravity entries are missing (pressure $\le 0$, e.g. −999). The general search (loop over `K` from `IMINMAX2(J)`−3 down to `IMIN2(J)`) then covers $\log g$ only up to `ATMGLC(IMINMAX2(J)-1)`. A $\log g$ between that and `ATMGLC(NGC-1)` matches no interval and falls through to the lowest four valid gravities, a long extrapolation; and a $\log g$ at or above `ATMGLC(NGC-1)` takes the top four gravities, missing entries included. Should both branches use `IMINMAX2(J)` in place of `NGC`?

### KCSURFP

Pressure at $T = T_\mathrm{eff}$ from the Kurucz/Castelli grid: splines in $\log g$ at four temperatures, then in $\log T_\mathrm{eff}$ (above).
