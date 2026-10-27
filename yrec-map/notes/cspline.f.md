## Explanation

**Purpose.** The second derivatives of a cubic spline through tabulated points, from Numerical Recipes (`SPLINE`), in double precision "for opacities".

**How it fits.**
- **Inputs:** `X(N)` (increasing), `Y(N)`, and the end slopes `YP1`, `YPN`; a slope of $10^{30}$ or more asks for a natural spline (zero second derivative) at that end.
- **Who calls it:** the opacity routines [[gtpurz.f#GTPURZ|GTPURZ]] and [[zsulaol.f#ZSULAOL|ZSULAOL]]; at `rp_1` also GTLAOL, GTLAOL2 and SULAOL (removed since `rp_1`).
- **Output:** `Y2(N)`, the second derivatives, for a spline evaluation routine.

**The method.** Continuity of the first derivative at interior points gives the tridiagonal system
$$\frac{h_{i-1}}{6}y''_{i-1} + \frac{h_{i-1} + h_i}{3}y''_i + \frac{h_i}{6}y''_{i+1} = \frac{y_{i+1} - y_i}{h_i} - \frac{y_i - y_{i-1}}{h_{i-1}},$$
with $h_i = x_{i+1} - x_i$, solved by forward elimination and back substitution.

**Changed since `rp_1`.** Declarations only: `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`; three of its callers removed with their files.

## Questions for the experts

1. **Size.** The work array `U` has the fixed size `JSON` (5000, from [[dimensions_mod.f#DIMENSIONS_MOD|`DIMENSIONS_MOD`]]); `N` larger than that would overflow. Fine for opacity tables.
2. **Duplicates.** The code base has several spline routines ([[spline.f|spline.f]], [[splinj.f|splinj.f]], splinnr.f (removed since `rp_1`), …). Could one serve all callers in the overhaul?

### CSPLINE

Numerical Recipes' cubic-spline setup: returns the second derivatives `Y2`, natural or with given end slopes.
