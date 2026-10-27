## Explanation

**Purpose.** `KSPLINT` evaluates at $x$ the 4-point cubic spline whose second derivatives [[kspline.f#KSPLINE|`KSPLINE`]] computed (*Numerical Recipes*' `SPLINT`, with `NM` = 4 fixed).

**How it fits.** Called by the same routines as `KSPLINE`: [[kcsurfp.f#KCSURFP|`KCSURFP`]], [[surfp.f#SURFP|`SURFP`]], [[eqscve.f#EQSCVE|`EQSCVE`]], [[tauintnew.f#TAUINTNEW|`TAUINTNEW`]]. No COMMON blocks, no calls.

**The method.** It finds the interval $[x_\mathrm{lo}, x_\mathrm{hi}]$ by bisection, then with $h = x_\mathrm{hi}-x_\mathrm{lo}$, $A = (x_\mathrm{hi}-x)/h$, $B = (x-x_\mathrm{lo})/h$:

$$y = A\,y_\mathrm{lo} + B\,y_\mathrm{hi} + \frac{h^2}{6}\left[(A^3-A)\,y''_\mathrm{lo} + (B^3-B)\,y''_\mathrm{hi}\right].$$

Outside the 4 points it extrapolates with the end interval's cubic. It stops with "Ksplint failure" if two nodes coincide.

**Changed since `rp_1`.** Declarations only: `IMPLICIT NONE` with explicit declarations.

### KSPLINT

Spline evaluation (above).
