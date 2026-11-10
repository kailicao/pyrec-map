## Explanation

**Purpose.** `SPLINE` evaluates a shape-preserving quadratic spline at one point, in one interval of the table. Its header credits the method to D. F. McAllister and J. A. Roulier, coded by S. L. Dodd and M. Roulier (N.C. State University). The knots and parameters of the spline in the interval are computed beforehand.

**How it fits.**
- **Who calls it:** only [[meval.f#MEVAL|MEVAL]], which controls the evaluation of the osculatory quadratic spline and computes the knots and parameters (through `CHOOSE`, by `MEVAL`'s comments).
- **COMMON blocks:** none; a function of its arguments only.

**The method.** In the interval $[x_0, x_1]$ (`XTABS`, `XTABS1`), with values $f_0, f_1$ (`YTABS`, `YTABS1`), the spline is made of quadratic pieces joined at one knot $z_1$ (`Z1`; cases 1–3) or two knots $\xi_1 < z_1$ (`Y1`, `Z1`; case 4, `NCASE = 4`). Each piece is a quadratic Bézier form; for example, for $x$ between $z_1$ and $x_1$:

$$s(x) = \frac{z_2\,(x_1 - x)^2 + 2 w_2\,(x - z_1)(x_1 - x) + f_1\,(x - z_1)^2}{(x_1 - z_1)^2},$$

where $z_2$ (`Z2`) is the value at the knot and $w_2$ (`W2`) the middle control value. For $x$ between $x_0$ and the knot, `V2` plays the role of `W2`; between the two knots of case 4, `E2` does, with `Y2` the value at the first knot.

**Design.** Where a denominator would vanish (a knot at an end of the interval), linear interpolation between the interval's ends is used instead: "MODIFICATION DUE TO MARC PINSONNEAULT 6/87." Each fallback is reached only when `XVALS` lies outside `[XTABS, XTABS1]` (with the knot at `XTABS1`, only for `XVALS` > `XTABS1`, [[#L66-L73]] and [[#L139-L146]]; with the knot at `XTABS`, only for `XVALS` < `XTABS`, [[#L79-L86]] and [[#L102-L109]]), and the one between the two knots of case 4 ([[#L126-L133]]) never, since it needs `Y1` < `XVALS` < `Z1` with `Z1` = `Y1`. MEVAL passes such points only when it extrapolates beyond the table's ends ([[meval.f#L135]], [[meval.f#L259]]): The fallback is then a linear extrapolation of the end interval (settled from the code, Nov 9, 2026).

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.

### SPLINE

The value of a shape-preserving quadratic spline at `XVALS`, from one or two knots in the interval (equation above).
