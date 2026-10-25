## Explanation

**Purpose.** `MEVAL` evaluates a shape-preserving (osculatory) quadratic spline at a set of points: McAllister and Roulier's algorithm, "coded by S. L. Dodd and M. Roulier, N.C. State University" (its header). The spline passes through the data with given slopes and keeps the data's monotonicity and convexity.

**How it fits.** Called only by [[osplin.f#OSPLIN|`OSPLIN`]], which computes the slopes and passes `EPS` = $10^{-4}$; `OSPLIN` is the interpolator that [[hpoint.f#HPOINT|`HPOINT`]] uses to move every model variable to the new mass points, and is also called by [[eq2mod.f#EQ2MOD|`EQ2MOD`]] and [[getgrid.f#GETGRID|`GETGRID`]]. It calls [[search.f#SEARCH|`SEARCH`]] (the interval of a point), [[choose.f#CHOOSE|`CHOOSE`]] (which of the spline's cases applies in an interval), [[cases.f#CASES|`CASES`]] (the spline's parameters for that case) and the function [[spline.f#SPLINE|`SPLINE`]] (its value). No COMMON blocks.

**The method.** Its arguments: the points `XVAL(1..NUME)` (nondecreasing), the data `XTAB`, `YTAB` and slopes `MTAB` (`NUM` points), the tolerance `EPS`; the output `YVAL` and the error code `ERR` (0 normal; 1 extrapolation; 2 `XVAL` not sorted, in which case nothing is computed). It walks through the evaluation points and the data intervals together: points equal to a data abscissa get the data value; for each interval containing points it calls `CHOOSE` and `CASES` once and evaluates `SPLINE` at each point; points beyond the ends are extrapolated with the end intervals' splines.

**KC's changes.** 2025-05-30: arithmetic IF statements replaced by block IFs (no change in behaviour intended).

## Questions for the experts

1. **A comment contradicts the code.** "If XVAL(I) .LT. XTAB(1), then XVAL(I)=YTAB(1)" (and the same at the top end): the code extrapolates with the end spline instead, and writes `YVAL`, not `XVAL`. Which behaviour is wanted for the outermost points of a rezoned model?
2. **The error code is ignored.** `ERR` = 2 (unsorted `XVAL`) returns without setting `YVAL`, and `OSPLIN` does not check `ERR` after the call, so the caller gets whatever `YVAL` held. Should `OSPLIN` stop, or warn?
3. **Fixed array size.** The dummy arrays are declared with `JSON` = 5000 rather than with `NUM` and `NUME`.

### MEVAL

Evaluates McAllister–Roulier's shape-preserving quadratic spline at many points (above).
