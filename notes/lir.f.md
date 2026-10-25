## Explanation

**Purpose.** `LIR` is a general interpolation/extrapolation routine for tables: given a monotonic abscissa `ZI(1..NT)` and `II` ordinates tabulated at each node (`YI`, first dimension `ID`), it returns the `II` values at `Z`, by cubic (4-point Lagrange) interpolation, or linear when `NT` < 4. A second entry point, `LIR1`, forces linear interpolation. It comes with the MHD equation-of-state package (it sits in the group of `MHDPX*`, `MHDST*`).

**How it fits.** Called by [[intpt.f#INTPT|`INTPT`]] (five times per call: in pressure on four temperature rows, then in temperature) and by [[mhdpx1.f#MHDPX1|`MHDPX1`]], both in the MHD EOS interpolation. No call to the `LIR1` entry exists in `src/`. No COMMON blocks, no calls. The output flag `INTER` is 1 for interpolation and 0 for extrapolation.

**The method.** It scans from `N` = 1 (or, when `L` > 1, from the node found by the previous call, kept in the saved `N`) to the first node beyond `Z`, in ascending or descending order. If `Z` falls on a node it copies that node's values. Otherwise it takes the four nodes around `Z` (shifted at the ends, so it extrapolates near and beyond them) and the Lagrange weights

$$A_k = \prod_{j\ne k}\frac{z - z_j}{z_k - z_j},\qquad y_i(z) = \sum_{k=1}^{4} A_k\,y_i(z_k);$$

the weight of node $k$ (`K`: the third of the four, i.e. the first node beyond `Z`, or the nearest end node near the table's ends; the comment calls it the point closest to `Z`) is then reset to $1 + A_k - \sum_j A_j$, so that the weights sum exactly to 1. The linear branch uses $y = w\,y_{n-1} + (1-w)\,y_n$ with $w = (z_n - z)/(z_n - z_{n-1})$. Any result exactly zero also zeroes the next element of `Y` (`Y(I+IR1)`, with `IR1` = 0 here, so it has no effect).

**Design.** The scan position `N` is saved between calls (`DATA N/-1/`, `SAVE`), so with `L` > 1 the result depends on the previous call. The error branches (fewer than 2 points; first and last abscissae equal) return silently without setting `Y`; their messages are commented out.

**KC's changes.** 2025-05-30: arithmetic IF statements replaced by block IFs, and DO loops that ended on a labelled assignment rewritten to end on `CONTINUE` (no change in behaviour intended).

## Questions for the experts

1. **Silent failures.** With `NT` < 2 or `ZI(1)` = `ZI(NT)`, `LIR` returns without setting `Y` and without a message, so the caller uses stale values. Should it stop or warn?
2. **A comment that no longer holds.** "Most of the computation is performed in single precision": the routine is `IMPLICIT REAL*8`.
3. **Unused entry and stride.** `LIR1` is never called, and the stride `IR` is always 1, which makes the `IR1`, `IRD`, `IIR` arithmetic dead weight. Can the routine be simplified?

### LIR

Cubic (or linear) Lagrange interpolation of several tabulated quantities at once, with a remembered search position (above).
