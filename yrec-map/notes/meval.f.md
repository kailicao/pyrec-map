## Explanation

**Purpose.** `MEVAL` evaluates a shape-preserving (osculatory) quadratic spline at a set of points: McAllister and Roulier's algorithm, "coded by S. L. Dodd and M. Roulier, N.C. State University" (its header). The spline passes through the data with given slopes and keeps the data's monotonicity and convexity.

**How it fits.** Called only by [[osplin.f#OSPLIN|`OSPLIN`]], which computes the slopes and passes `EPS` = $10^{-4}$; `OSPLIN` is the interpolator that [[hpoint.f#HPOINT|`HPOINT`]] uses to move every model variable to the new mass points, and is also called by [[eq2mod.f#EQ2MOD|`EQ2MOD`]] and [[getgrid.f#GETGRID|`GETGRID`]]. It calls [[search.f#SEARCH|`SEARCH`]] (the interval of a point), [[choose.f#CHOOSE|`CHOOSE`]] (which of the spline's cases applies in an interval), [[cases.f#CASES|`CASES`]] (the spline's parameters for that case) and the function [[spline.f#SPLINE|`SPLINE`]] (its value). No COMMON blocks; it takes the array size `JSON` from `DIMENSIONS_MOD`.

**The method.** Its arguments: the points `XVAL(1..NUME)` (nondecreasing), the data `XTAB`, `YTAB` and slopes `MTAB` (`NUM` points), the tolerance `EPS`; the output `YVAL` and the error code `ERR` (0 normal; 1 extrapolation; 2 `XVAL` not sorted, in which case nothing is computed). It walks through the evaluation points and the data intervals together: points equal to a data abscissa get the data value; for each interval containing points it calls `CHOOSE` and `CASES` once and evaluates `SPLINE` at each point; points beyond the ends are extrapolated with the end intervals' splines. `OSPLIN` does not check `ERR` ([[osplin.f#b1]]). The dummy arrays are declared with the fixed size `JSON` ([[#L21-L22]]), not with `NUM` and `NUME`.

> **Question** ([[#L102-L103]]; [[#L126-L137]]; [[#L249-L261]]). **A comment contradicts the code.** "If XVAL(I) .LT. XTAB(1), then XVAL(I)=YTAB(1)" (and the same at the top end): the code extrapolates with the end spline instead, and writes `YVAL`, not `XVAL`. Which behavior is wanted for the outermost points of a rezoned model?

**Changed since `rp_1`.** Declarations only: `JSON` from `DIMENSIONS_MOD` instead of a local `PARAMETER(JSON=5000)`, `IMPLICIT NONE`.

## Bugs, by priority

1. **(d)** **No point of evaluation within the data.** ([[#L107-L121]]; [[#L138-L144]]; [[#L242-L243]]) When every `XVAL` lies below `XTAB(1)` and `NUME` > 1, loop 30 leaves `START` = `NUME+1`; after the extrapolation the code goes on to label 80 and calls `SEARCH` with `XVAL(NUME+1)`, outside the points of evaluation, and if that value equals a data abscissa it writes `YVAL(NUME+1)` (label 90). When every `XVAL` lies above `XTAB(NUM)` and `NUME` > 1, loop 50 leaves `END` = 0, the loop over the in-range points is empty, and line 243 reads `XVAL(0)`, outside the array. What follows: The values returned for `1..NUME` are right in both cases (the end interval's spline), but the reads are out of range: `XVAL(0)` is caught by `-fcheck=all` (the flags of the `devel` build) and read as whatever lies before the array otherwise; `XVAL(NUME+1)` and `YVAL(NUME+1)` lie within the declared size `JSON` unless `NUME` = `JSON`. Only when no point of a regridding lies within the old grid, which the callers' grids should not allow (not traced). Read from the code, not run. **A possible fix:**

    ```fortran
    C 11/09/26 KC via Claude
    C code changed to go straight to the extrapolation above XTAB(NUM)
    C when no point of evaluation lies within the data, so that XVAL and
    C YVAL are not used outside 1..NUME.
      80  IF (END .LT. START) GO TO 200
    ```

    With `NUME` = 1 this is the old test (`END` = 0 < `START` = 1); when every point lies below `XTAB(1)`, label 210's loop is then empty.

### MEVAL

Evaluates McAllister–Roulier's shape-preserving quadratic spline at many points (above).
