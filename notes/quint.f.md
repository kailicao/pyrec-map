## Explanation

**Purpose.** A small helper: quadratic interpolation through three equally spaced points (Newton's forward-difference form).

**How it fits.** Its only caller is [[mhdpx1.f#MHDPX1|`MHDPX1`]], which interpolates the MHD equation-of-state tables. It uses no COMMON blocks and calls nothing.

**The method.** With $y_0 = y(x_0)$, $y_1 = y(x_0+h)$, $y_2 = y(x_0+2h)$ and $t = (x - x_0)/h$:

$$y(x) = y_0 + t\,\Delta_1 + \tfrac12\,t\,(t-1)\,\Delta_2, \qquad \Delta_1 = y_1 - y_0,\quad \Delta_2 = y_2 - 2y_1 + y_0 .$$

In the code, `X0`, `H`, `Y0`, `Y1`, `Y2` are $x_0$, $h$, $y_0$, $y_1$, $y_2$, and the result is returned in `Y`. Nothing stops $t$ from lying outside $[0, 2]$, so it also extrapolates. The caller only checks that the three points are equally spaced; its extrapolation warning is commented out.

## Questions for the experts

1. **SAVE.** The routine has a `save` statement but keeps no state between calls. Is it a leftover, harmless?
