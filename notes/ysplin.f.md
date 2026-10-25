## Explanation

**Purpose.** `YSPLIN` (YCK 3/91) computes the coefficients of a cubic spline through $(x_i, y_i)$, $i = 1..N$, with $y_i$ given in `C(1,i)`. On return, for each interval, `C(1..4,i)` give
$$y(x) = c_{1,i} + c_{2,i}\,h + c_{3,i}\,h^2 + c_{4,i}\,h^3,\qquad h = x - x_i ,$$
so that $c_{2,i}$ is the slope at $x_i$. The comment calls it the natural cubic spline.

**How it fits.** Called by [[ykoeff.f#YKOEFF|YKOEFF]] (Kurucz tables), [[ylloc.f#YLLOC|YLLOC]] (OPAL92 tables), [[intpol.f#INTPOL|INTPOL]] and [[ll4th.f#LL4TH|LL4TH]]; the coefficients are evaluated in [[yllo2d.f#YLLO2D|YLLO2D]], [[kurucz.f#KURUCZ|KURUCZ]] and their twins. No COMMON blocks.

**The method.** With $h_i = x_i - x_{i-1}$ and $f_i = (y_i - y_{i-1})/h_i$, the slopes $s_i$ solve the tridiagonal system
$$h_{i+1}\,s_{i-1} + 2(h_i + h_{i+1})\,s_i + h_i\,s_{i+1} = 3\,(h_{i+1} f_i + h_i f_{i+1}),$$
with the natural end conditions ($y'' = 0$) eliminated into the second and next-to-last rows (the factors 1.5) and $s_1 = \tfrac32 f_2 - \tfrac12 s_2$, $s_N = \tfrac32 f_N - \tfrac12 s_{N-1}$. Then, with $d = s_i + s_{i+1} - 2f_{i+1}$,
$$c_{3,i} = \frac{f_{i+1} - s_i - d}{h_{i+1}},\qquad c_{4,i} = \frac{d}{h_{i+1}^2}.$$

## Questions for the experts

1. **Small `N`.** The rows 2 and `N-1` are written separately, so `N` ≥ 4 is needed (with `N` = 3 the two special rows coincide and the second overwrites the first). The callers stop below 25 points (`YKOEFF`) but `YLLOC` only skips `N` ≤ 1.
2. **A fixed size.** `C` is dimensioned `(4, NP = 100)` with no check that `N` ≤ 100.

### YSPLIN

Coefficients of a natural cubic spline in polynomial form per interval (slope, second- and third-order terms), by a tridiagonal solve for the slopes.
