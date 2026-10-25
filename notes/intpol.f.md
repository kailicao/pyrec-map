## Explanation

**Purpose.** `INTPOL` interpolates a tabulated function with a cubic spline and returns its value and first derivative at one point (YCK 3/91). The header comment speaks of a choice between Hermite and spline interpolation, but only the spline is in the code.

**How it fits.** Called by the Kurucz opacity routines [[kurucz.f#KURUCZ|`KURUCZ`]] and [[kurucz2.f#KURUCZ2|`KURUCZ2`]] (interpolation in temperature) and by the Livermore routines [[yllo2d.f#YLLO2D|`YLLO2D`]] and [[yllo2d2.f#YLLO2D2|`YLLO2D2`]]. It calls [[ysplin.f#YSPLIN|`YSPLIN`]] for the spline coefficients. COMMON: only `LUOUT`, for the error message.

**The method.** `YSPLIN` returns the coefficients $c_{1..4}$ of the cubic on each interval. With $k$ the interval containing $\bar x$ (found by bisection; the first or last interval when $\bar x$ is outside) and $\Delta = \bar x - x_k$:

$$y = ((c_4\Delta + c_3)\Delta + c_2)\Delta + c_1,\qquad y' = (3c_4\Delta + 2c_3)\Delta + c_2 .$$

**Design.** The coefficient array `C(4,NP)` has `NP` = 100 columns and is `SAVE`d; `N` is not checked against it. The spline is recomputed on every call.

## Questions for the experts

1. **The missing Hermite option.** The comment says the routine "gives the right for selection to user" between Hermite and spline; only the spline exists. Remove the comment, or was Hermite removed by mistake?
2. **Silent extrapolation.** Outside the table the end cubic is used without a warning. Do all callers check the range first? (`KURUCZ` does.)
3. **Error message.** The message "ERROR COX OP: INTERPOLATION" names the Cox opacities; the routine is generic.
4. **Bounds.** `N` > 100 would overflow `C`.

### INTPOL

Cubic-spline value and derivative at one point (above).
