## Explanation

**Purpose.** `SPLINC` computes the second derivatives of a natural cubic spline through the points $(x_i, y_i)$, $i = 1, \dots, N$, for interpolation with [[splintd2.f#SPLINTD2|SPLINTD2]]. It is the tridiagonal algorithm of Numerical Recipes' `spline`, with the end conditions fixed to a natural spline.

**How it fits.**
- **Who calls it:** only [[hpoint.f#HPOINT|HPOINT]], which then calls [[splintd2.f#SPLINTD2|SPLINTD2]] with the result.
- **Outputs:** `Y2`, the second derivatives at the points.
- **COMMON blocks:** none.

**The method.** A natural spline has $y''_1 = y''_N = 0$. For the interior points the second derivatives solve

$$\frac{x_i - x_{i-1}}{6}\,y''_{i-1} + \frac{x_{i+1} - x_{i-1}}{3}\,y''_i + \frac{x_{i+1} - x_i}{6}\,y''_{i+1} = \frac{y_{i+1} - y_i}{x_{i+1} - x_i} - \frac{y_i - y_{i-1}}{x_i - x_{i-1}},$$

which the code solves by forward elimination (`SIG`, `P`, `U`) and back substitution.

**Design.** The arrays have the fixed size `JSON = 5000`. [[splinj.f|splinj.f]] is the same routine with arrays sized `N`.

## Questions for the experts

1. **Two copies.** `SPLINC` and [[splinj.f#SPLINJ|SPLINJ]] are the same algorithm; only the array declarations differ. Could one replace the other?

### SPLINC

Natural cubic spline: the second derivatives `Y2` at `N` points (at most 5000).
