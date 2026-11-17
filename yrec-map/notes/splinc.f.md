## Explanation

**Purpose.** `SPLINC` computes the second derivatives of a natural cubic spline through the points $`(x_i, y_i)`$, $`i = 1, \dots, N`$, for interpolation with [SPLINTD2](splintd2.f.md#splintd2). It is the tridiagonal algorithm of Numerical Recipes' `spline`, with the end conditions fixed to a natural spline.

**How it fits.**
- **Who calls it:** only [HPOINT](hpoint.f.md#hpoint), which then calls [SPLINTD2](splintd2.f.md#splintd2) with the result.
- **Outputs:** `Y2`, the second derivatives at the points.
- **COMMON blocks:** none.

**The method.** A natural spline has $`y''_1 = y''_N = 0`$. For the interior points the second derivatives solve

```math
\frac{x_i - x_{i-1}}{6}\,y''_{i-1} + \frac{x_{i+1} - x_{i-1}}{3}\,y''_i + \frac{x_{i+1} - x_i}{6}\,y''_{i+1} = \frac{y_{i+1} - y_i}{x_{i+1} - x_i} - \frac{y_i - y_{i-1}}{x_i - x_{i-1}},
```

which the code solves by forward elimination (`SIG`, `P`, `U`) and back substitution.

**Design.** The arrays have the fixed size `JSON` (5000, from `DIMENSIONS_MOD`). [splinj.f](splinj.f.md) is the same routine with arrays sized `N`.

> **Question** ([line 13](https://github.com/yreclab/yrec/blob/7be4133/src/splinc.f#L13); [splinj.f, line 10](https://github.com/yreclab/yrec/blob/7be4133/src/splinj.f#L10)). **Two copies.** `SPLINC` and [SPLINJ](splinj.f.md#splinj) are the same algorithm; only the array declarations differ. Could one replace the other?

**Changed since `rp_1`.** Declarations only: the array size `JSON` from `DIMENSIONS_MOD`, `IMPLICIT NONE`.

### SPLINC

Natural cubic spline: the second derivatives `Y2` at `N` points (at most 5000).
