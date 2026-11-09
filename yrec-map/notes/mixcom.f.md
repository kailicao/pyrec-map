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
4. A convection zone adjoining the region below or above (whether or not the region's edge point is itself convective, the test [[mixgrid.f#MIXGRID|MIXGRID]]'s sums use) takes the abundance of the region's edge point if that point is convective, since it was mixed with its neighbor; if the edge point is radiative, the zone gets the end cell's change added instead.

Finally, before the last iteration (`LOK = F`), $Y = 1 - X - Z - X_{^3\mathrm{He}}$ over the region and the adjoining convection zones ([[#L196-L200]]). On the last iteration the closure needs no update when SECULR calls (rows 5 and up, so $X$, $Z$ and ³He do not change, [[seculr.f#L466-L475]]); BURSMIX, which mixes rows 4 and up with ³He among them, sets $Y = 1 - X - Z - X_{^3\mathrm{He}}$ itself after its extrapolation ([[bursmix.f#L132-L136]]) (settled from the code, Nov 9, 2026).

The sums `DCOMP`, `DCOMP2`, `SUMSPEC` and `SUMSPEC2` ([[#L99-L104]], [[#L144-L182]]) feed only a conservation check that is commented out, which would rescale the species to keep its mass ([[#L184-L193]]): unused?

**Changed since `rp_1`.** Declarations only: COMMON blocks to modules, `IMPLICIT NONE`.

**Changed since `a8a5950`.** The adjoining convection zones are found whether or not the end zone is convective, and a radiative end zone's neighbors get the end cell's change added rather than a copy, so that species are conserved; `I1` is set to `IEND` when the top zone has no convective neighbor (settles former question 1).
