## Explanation

**Purpose.** Quadratic interpolation through three points for the 2006 OPAL equation of state; a copy of `QUAD` and `QUADEOS01` (both removed since `rp_1`) under its own name, with its own cache.

**How it fits.**
- **Who calls it:** [[esac06.f#ESAC06|ESAC06]] and [[t6rinteos06.f#T6RINTEOS06|T6RINTEOS06]].

**The method.** As in `QUAD`: $y(x) = c_1 + c_2 x + c_3 x^2$ through the three points; with `IC = 0` the abscissa factors are computed and cached in slot `I` (up to 30), otherwise reused. It differs from `QUADEOS01` only in its name and in redundant parentheses.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE`.
