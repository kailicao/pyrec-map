## Explanation

**Purpose.** Interpolation by a shape-preserving osculatory quadratic spline, from ACM Algorithm 574 (D. F. McAllister and J. A. Roulier, ACM Transactions on Mathematical Software, September 1981), as the header says. It interpolates the table `(XTAB, YTAB)` of `N` points to the `K` abscissas `XVAL`, and returns the values in `YVAL`.

**How it fits.**
- **Who calls it:** the routines that move quantities between the model grid and an equally spaced grid: [[mixcom.f#MIXCOM|MIXCOM]], [[mixgrid.f#MIXGRID|MIXGRID]], [[rotgrid.f#ROTGRID|ROTGRID]], [[getgrid.f#GETGRID|GETGRID]], [[eq2mod.f#EQ2MOD|EQ2MOD]] and [[hpoint.f#HPOINT|HPOINT]].
- **What it calls:** [[slopes.f#SLOPES|SLOPES]] (the derivatives $m_i$ at the data points) and [[meval.f#MEVAL|MEVAL]] (the evaluation; `EPS` $=10^{-4}$ is a relative error tolerance passed on to MEVAL's internal routine `CHOOSE`).

**The method.** The spline is quadratic between the data points, matches the values and the slopes $m_i$ there, and preserves the data's monotonicity and convexity (hence "shape-preserving"); the details are in `SLOPES` and `MEVAL`. The arrays are dimensioned `JSON` (from `DIMENSIONS_MOD`), the model's maximum number of shells.

**Changed since `rp_1`.** Declarations only: `JSON` from `DIMENSIONS_MOD` instead of a local `PARAMETER`, `IMPLICIT NONE`.

## Questions for the experts

1. **The error flag.** `MEVAL` returns an error code `ERR` (1 if some `XVAL` lies outside the table, 2 if `XVAL` is not increasing), which `OSPLIN` ignores. Should a failure be reported?
