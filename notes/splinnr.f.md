## Explanation

**Purpose.** `splinnr` is Numerical Recipes' `spline`, in single precision: the second derivatives of a cubic spline through $(x_i, y_i)$, with the first derivatives at the ends given (`yp1`, `ypn`), or a natural spline at an end where the given value exceeds $0.99\times10^{30}$.

**How it fits.** Nothing in `src/` calls it, and it uses no COMMON block. It is identical to [[splnr.f|splnr.f]] except for its name.

**The method.** As in [[splinc.f|splinc.f]], with the end conditions: for a given slope $y'_1$,

$$y''_1 = -\tfrac12, \qquad u_1 = \frac{3}{x_2 - x_1}\left(\frac{y_2 - y_1}{x_2 - x_1} - y'_1\right)$$

start the elimination (and symmetrically at $x_N$).

## Questions for the experts

1. **Unused.** No routine calls `splinnr`, and `splnr` is an identical copy; the double-precision Numerical Recipes `spline` the code does use is [[cspline.f#CSPLINE|CSPLINE]]. Can both be removed?
2. **Precision and size.** It is `REAL` (single precision) and limited to `NMAX = 500` points, unlike the rest of the code (double precision, 5000 shells).

### SPLINNR

Numerical Recipes' cubic spline set-up (single precision, at most 500 points); unused.
