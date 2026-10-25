## Explanation

**Purpose.** Quadratic interpolation through three points, used by the original OPAL equation of state's table routines. `QUADEOS01` and `QUADEOS06` (in [[quadeos01.f|quadeos01.f]] and [[quadeos06.f|quadeos06.f]]) are copies for the 2001 and 2006 tables.

**How it fits.**
- **Who calls it:** [[esac.f#ESAC|ESAC]] and [[t6rinterp.f#T6RINTERP|T6RINTERP]]. (GETW, GETQUA and VCIRC use an unrelated *array* `QUAD`, in the COMMON block `/QUADRU/`.)

**The method.** Through $(x_1, y_1)$, $(x_2, y_2)$, $(x_3, y_3)$, $y(x) = c_1 + c_2 x + c_3 x^2$ with
$$c_3 = \frac{1}{x_1 - x_3}\left[\frac{y_1 - y_2}{x_1 - x_2} - \frac{y_2 - y_3}{x_2 - x_3}\right],\qquad c_2 = \frac{y_1 - y_2}{x_1 - x_2} - (x_1 + x_2)\,c_3,\qquad c_1 = y_1 - x_1 c_2 - x_1^2 c_3 .$$

**Design.** A cache: when `IC = 0`, the factors that depend only on the abscissas ($1/(x_1-x_2)$, $1/(x_1-x_3)$, $1/(x_2-x_3)$, $x_1^2$, $x_1+x_2$) are computed and stored in slot `I` (up to 30); when `IC` $\ne 0$, the stored factors of slot `I` are reused, so the caller must pass the same abscissas as when the slot was filled.

## Questions for the experts

1. **The cache is unchecked.** Nothing verifies that the abscissas match the cached slot when `IC` $\ne 0$, nor that `I` $\le 30$. A comment at least, or a debug check?
2. **The name clash.** The function `QUAD` and the array `QUAD` in `/QUADRU/` share a name. Renaming the array would spare readers the confusion.
