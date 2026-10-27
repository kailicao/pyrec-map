## Explanation

**Purpose.** Solves the diffusion equation for composition across one unstable region, on the equally spaced grid in the coordinate $\chi$ that [[mixgrid.f#MIXGRID|MIXGRID]] and [[getgrid.f#GETGRID|GETGRID]] have set up, and applies the change to the model.

**How it fits.**
- **Inputs:** `DT` (s); `ECOD2` and `EM` on the equal grid, from `MIXGRID`; the shell masses `HS2`; the region `IBEG..IEND`; the convection flags `LCZ`; `LOK`; the species range `JBEG..JEND`; and the grid itself in `EGRID_MOD` (`CHI` at the model points, `ECHI` at the grid points, `DCHI`, `NTOT`).
- **Who calls it:** only [[ndifcom.f#NDIFCOM|NDIFCOM]].
- **What it calls:** [[osplin.f#OSPLIN|OSPLIN]] (interpolation, both ways), [[ccoeft.f#CCOEFT|CCOEFT]] (the tridiagonal coefficients, in `TRIDI_MOD`) and [[ctridi.f#CTRIDI|CTRIDI]] (the solve, result `U` in `TRIDI_MOD`).
- **Output:** `HCOMP`, in place.
- **Modules:** `EGRID_MOD` (shared with GETGRID, MIXGRID, ROTGRID, EQ2MOD, CHECKJ, SECULR), `SPLIN_MOD` (scratch arrays shared with MIXGRID, ROTGRID, EQ2MOD), `TRIDI_MOD` (with CCOEFT, CTRIDI, DCOEFT, GETQUA, TRIDIA), and `DIMENSIONS_MOD` (`JSON`).

**The method.** For each species $k$ in `JBEG..JEND` (except ⁴He, row 2, which follows from closure) that varies by more than $10^{-14}$ over the region:
1. Interpolate $X_k$ from the model points ($\chi$ = `CHI`) to the grid points (`ECHI`) with `OSPLIN`.
2. Solve, implicitly, with $\Delta\chi$ = `DCHI`, $\Delta M_i$ = `EM(I)` and $\mathcal{D}$ = `ECOD2` (`COD2` times $\rho r^2\, d\chi/dr$, see `MIXGRID`):
$$X_i^{n+1} - \frac{\Delta t}{\Delta\chi\,\Delta M_i}\left[\mathcal{D}_{i+1}\,(X^{n+1}_{i+1} - X^{n+1}_i) - \mathcal{D}_i\,(X^{n+1}_i - X^{n+1}_{i-1})\right] = X_i^n,$$
with no flux through the outer edges (`CCOEFT`, `CTRIDI`).
3. Interpolate the *change* $X^{n+1}-X^n$ back to the model points and add it (the comment explains: extrapolating the new abundances past the last grid points "can lead to serious errors").
4. A convection zone adjoining the region below or above takes the abundance of the region's edge point.

Finally, before the last iteration (`LOK = F`), $Y = 1 - X - Z - X_{^3\mathrm{He}}$ over the region and the adjoining convection zones.

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

## Questions for the experts

1. **`I1` not set.** If the region's top point `IEND` is not convective, or is the last point `M`, `I1` is never assigned in this call: it keeps its value from an earlier call (`SAVE`), or is undefined on the first. `I1` bounds the loops that sum the species mass, update the upper convection zone and recompute helium. Should there be `ELSE I1 = IEND`, as there is `I0 = IBEG` for the bottom?
2. **The conservation check is off.** `DCOMP`, `DCOMP2`, `SUMSPEC` and `SUMSPEC2` are computed but only used in a commented-out check that would rescale the species to conserve its mass. Is mass conservation verified elsewhere?
3. **Helium on the final call.** Helium is recomputed only when `LOK` is false. On SECULR's final call (`JBEG = 5`) $X$, $Z$ and ³He do not change, so the closure holds. But [[bursmix.f#BURSMIX|BURSMIX]] passes rows 4 to 11 (or 15), so ³He is mixed; if `LOK` is true there, $Y$ is not recomputed and $X+Y+Z+X_{^3\mathrm{He}}$ may drift from 1. Is it restored elsewhere?
4. **The inner convection zone's change.** `DCOMP2` adds `YVAL(1)*HS2(I)` for the inner zone, but the zone's abundance is set to that of `IBEG`, not changed by `YVAL(1)`. (It matters only for the disabled check.)
